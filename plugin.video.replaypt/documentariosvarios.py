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

documentariosvarios_url = 'http://documentariosvarios.wordpress.com/'
##################################################

def CATEGORIES_documentariosvarios():
	addDir('[B]Mudar para categorias[/B]',documentariosvarios_url,424,addonfolder+artfolder+'documentariosvarios.png',True)
	listar_episodios(documentariosvarios_url)

def alterar_vista(url):
	addDir('[B]Mudar para últimas[/B]',url,421,addonfolder+artfolder+'documentariosvarios.png');
	try:
		codigo_fonte = abrir_url(url)
	except:
		codigo_fonte = ''
	if codigo_fonte:
		html_source_trunk = re.search('<aside id="categories-2" class="widget widget_categories">(.+?)</aside>', codigo_fonte, re.DOTALL)
		if html_source_trunk:
			match = re.findall('<li.*?><a href="(.+?)".*?>(.+?)</a>(.+?)(?:</li>|<ul class=\'children\'>)', html_source_trunk.group(1), re.DOTALL)
			for url, name, quantidade in match:
				try:
					addDir(name+' - '+quantidade.strip(),url,422,addonfolder+artfolder+'documentariosvarios.png')
				except: pass			

def listar_episodios(url):
    try: codigo_fonte = abrir_url(url)
    except: codigo_fonte = ''
    if codigo_fonte:
		match = re.findall('<article.+?>(?:.*?<div class="entry-thumbnail">.*?<img.+?src="(.+?)".*?>.*?</div>.*?<h1 class="entry-title">|.*?<h1 class="entry-title">)<a.+?href="(.+?)".+?>(.+?)</a></h1>', codigo_fonte, re.DOTALL)
		for iconimage, link, name in match:
			name = name.replace("&nbsp;"," ")
			try:
				if iconimage:
					addDir(name,link,423,iconimage,False)
				else:
					addDir(name,link,423,addonfolder+artfolder+'documentariosvarios.png',False)
			except: pass
		match_2 = re.search('/page/[\d]+', url)
		if match_2 == None:
			url = url+'page/1'
		url_2 = re.sub('/([\d]+)$',  lambda p: '/'+str(int(p.group(1))+1), url)
		try:
			codigo_fonte_2 = abrir_url(url_2)
			match_3 = re.findall('<article.+?>(?:.*?<div class="entry-thumbnail">.*?<img.+?src="(.+?)".*?>.*?</div>.*?<h1 class="entry-title">|.*?<h1 class="entry-title">)<a.+?href="(.+?)".+?>(.+?)</a></h1>', codigo_fonte_2, re.DOTALL)
			if match_3:
				addDir('[B]Próxima >>[/B]',url_2,422,addonfolder+artfolder+'documentariosvarios.png')
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
				elif iframe.find('vk.com') > -1:
					resolver_iframe = vkcom_resolver(iframe)
					if resolver_iframe != 'vkcom_nao resolvido':
						playlist.add(resolver_iframe,xbmcgui.ListItem(name, thumbnailImage=iconimage))
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
	
def vkcom_resolver(url):
	match = re.compile('http://vk.com/video_ext.php\?oid=([\d]+?)&.*?id=([\d]+?)&.*?hash=([A-Za-z0-9]+).*?').findall(url)
	if match != None:
		for oid, id, hash in match:
			codigo_fonte_2 = abrir_url('http://vk.com/video_ext.php?oid=' + oid + '&id=' + id + '&hash=' + hash)
			match_2 = re.search('url1080=(.+?).1080.mp4', codigo_fonte_2)
			if match_2 != None:
				return match_2.group(1)+'.1080.mp4'
			match_2 = re.search('url720=(.+?).720.mp4', codigo_fonte_2)
			if match_2 != None:
				return match_2.group(1)+'.720.mp4'
			match_2 = re.search('url480=(.+?).480.mp4', codigo_fonte_2)
			if match_2 != None:
				return match_2.group(1)+'.480.mp4'
			match_2 = re.search('url360=(.+?).360.mp4', codigo_fonte_2)
			if match_2 != None:
				return match_2.group(1)+'.360.mp4'
			match_2 = re.search('url240=(.+?).240.mp4', codigo_fonte_2)
			if match_2 != None:
				return match_2.group(1)+'.240.mp4'
	else:
		return 'vkcom_nao resolvido'
						
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