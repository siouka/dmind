#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Copyright 2014 Techdealer

##############BIBLIOTECAS A IMPORTAR E DEFINICOES####################
import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,xbmc,xbmcaddon,xbmcvfs,socket,HTMLParser
import json
h = HTMLParser.HTMLParser()

addon_id = 'plugin.video.replaypt'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = '/resources/img/'

docverdade_url = 'http://docverdade.blogspot.com/'
##################################################

def CATEGORIES_docverdade():
	addDir('[B]Mudar para categorias[/B]',docverdade_url,435,addonfolder+artfolder+'docverdade.png',True)
	listar_episodios(docverdade_url)

def alterar_vista(url):
	addDir('[B]Mudar para últimas[/B]',url,432,addonfolder+artfolder+'docverdade.png');
	try:
		codigo_fonte = abrir_url(url)
	except:
		codigo_fonte = ''
	if codigo_fonte:
		match = re.findall("<li>.*?<a dir='ltr' href='(.+?)'>(.+?)</a>.*?<span dir='ltr'>(.+?)</span>.*?</li>", codigo_fonte, re.DOTALL)
		for url, name, quantidade in match:
			try:
				addDir(name+' - '+quantidade,url,433,addonfolder+artfolder+'docverdade.png')
			except:
				pass			

def listar_episodios(url):
	try:
		codigo_fonte = abrir_url(url)
	except:
		codigo_fonte = ''
	if codigo_fonte:
		match = re.findall("<h3 class='post-title entry-title' itemprop='name'>.*?<a href='(.+?)'>(.+?)</a>.*?</h3>.*?<div class='post-header'>.*?(?:<img[^\r\n]*?src=\"([^\"\r\n]+?)\".*?<div class='post-footer'>|<div class='post-footer'>)", codigo_fonte, re.DOTALL)
		for link, name, iconimage in match:
			try:
				if iconimage:
					addDir(name,link,434,iconimage,False)
				else:
					addDir(name,link,434,addonfolder+artfolder+'docverdade.png',False)
			except: pass
	match_2 = re.search("<a class='blog-pager-older-link' href='(.+?)'.*?>Postagens mais antigas</a>", codigo_fonte)
	if match_2:
		try:
			url_2 = h.unescape(match_2.group(1))
			codigo_fonte_2 = abrir_url(url_2)
			match_3 = re.findall("<h3 class='post-title entry-title' itemprop='name'>.*?<a href='(.+?)'>(.+?)</a>.*?</h3>.*?<div class='post-header'>.*?(?:<img[^\r\n]*?src=\"([^\"\r\n]+?)\".*?<div class='post-footer'>|<div class='post-footer'>)", codigo_fonte_2, re.DOTALL)
			if match_3:
				addDir('[B]Próxima >>[/B]',url_2,433,addonfolder+artfolder+'docverdade.png')
		except:
			pass

def procurar_fontes(url,name,iconimage):
	progress = xbmcgui.DialogProgress()
	progress.create('Replay PT', 'Procurando fontes...')
	progress.update(0)
	playlist = xbmc.PlayList(1)
	playlist.clear()
	try:
		codigo_fonte = abrir_url(url)
	except:
		codigo_fonte = ''
	if codigo_fonte:
		html_source_trunk = re.findall('<iframe(.*?)</iframe>', codigo_fonte, re.DOTALL)
		for trunk in html_source_trunk:
			try:
				iframe = re.compile('src=["\'](.+?)["\']').findall(trunk)[0]
			except: iframe = ''
			if iframe:
				if iframe.find('youtube.com/embed/videoseries?list=') > -1: # função para listar playlists do youtube
					match = re.compile('.*?youtube.com/embed/videoseries\?list=([^&"]+).*?').findall(iframe)
					playlist_id = str(match[0])
					page = 1
					videos_per_page = 20
					index = 1 + ((int(page)-1)*videos_per_page)
					count = 0
					checker = True
					while checker:
						codigo_fonte = abrir_url('https://gdata.youtube.com/feeds/api/playlists/' + playlist_id + '?max-results=' + str(videos_per_page) + '&start-index=' + str(index) + '&v=2&alt=json')
						decoded_data = json.loads(codigo_fonte)
						for x in range(0, len(decoded_data['feed']['entry'])):
							count += 1
							youtube_id = decoded_data['feed']['entry'][x]['media$group']['yt$videoid']['$t'].encode("utf8")
							if count == int(decoded_data['feed']['openSearch$totalResults']['$t']):
								playlist.add('plugin://plugin.video.youtube/?action=play_video&videoid='+youtube_id,xbmcgui.ListItem(name, thumbnailImage=iconimage))
								checker = False
								break
							else:
								playlist.add('plugin://plugin.video.youtube/?action=play_video&videoid='+youtube_id,xbmcgui.ListItem(name, thumbnailImage=iconimage))
						if index<=500-videos_per_page+1 and index-1+videos_per_page<int(decoded_data['feed']['openSearch$totalResults']['$t']):
							page += 1
							index = 1 + ((int(page)-1)*videos_per_page)
				elif iframe.find('youtube') > -1:
					resolver_iframe = youtube_resolver(iframe)
					if resolver_iframe != 'youtube_nao resolvido':
						playlist.add(resolver_iframe,xbmcgui.ListItem(name, thumbnailImage=iconimage))
				elif iframe.find('dailymotion') > -1:
					resolver_iframe = daily_resolver(iframe)
					if resolver_iframe != 'daily_nao resolvido':
						playlist.add(resolver_iframe,xbmcgui.ListItem(name, thumbnailImage=iconimage))
				elif iframe.find('vimeo.com') > -1:
					resolver_iframe = vimeo_resolver(iframe)
					if resolver_iframe != 'vimeo_nao resolvido':
						playlist.add(resolver_iframe,xbmcgui.ListItem(name, thumbnailImage=iconimage))
		#players em flash (não iframe)
		match = re.compile('<embed src=".*?youtube.com/v/([^?"]+).*?"').findall(codigo_fonte)
		if match:
			for youtube_id in match:
				playlist.add('plugin://plugin.video.youtube/?action=play_video&videoid='+youtube_id,xbmcgui.ListItem(name, thumbnailImage=iconimage))
		if progress.iscanceled():
			sys.exit(0)
		progress.update(100)
		progress.close()
		if len(playlist) == 0:
			dialog = xbmcgui.Dialog()
			ok = dialog.ok('Replay PT', 'Nenhuma fonte suportada encontrada...')
		else:
			try:
				xbmc.Player().play(playlist)		
			except:
				pass

def youtube_resolver(url):
	match = re.compile('.*?youtube.com/embed/([^?"]+).*?').findall(url)
	if match:
		return 'plugin://plugin.video.youtube/?action=play_video&videoid=' + str(match[0])
	else: return 'youtube_nao resolvido'
    
def daily_resolver(url):
    if url.find('syndication') > -1: match = re.compile('/embed/video/(.+?)\?syndication').findall(url)
    else: match = re.compile('/embed/video/(.*)').findall(url)
    if match:
        return 'plugin://plugin.video.dailymotion_com/?mode=playVideo&url=' + str(match[0])
    else: return 'daily_nao resolvido'
	
def vimeo_resolver(url):
    match = re.compile('/([0-9]+)').findall(url)
    if match:
        return 'plugin://plugin.video.vimeo/?action=play_video&videoid=' + str(match[0])
    else: return 'vimeo_nao resolvido'
						
############################################################################################################################

def abrir_url(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

def addDir(name,url,mode,iconimage,pasta=True):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta)
        return ok
        
############################################################################################################
          
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param
      
params=get_params()
url=None
name=None
mode=None
iconimage=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass
try:        
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass

#print "Mode: "+str(mode)
#print "URL: "+str(url)
#print "Name: "+str(name)
#print "Iconimage: "+str(iconimage)