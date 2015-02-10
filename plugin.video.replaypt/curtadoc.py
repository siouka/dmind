#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Copyright 2014 Techdealer

##############BIBLIOTECAS A IMPORTAR E DEFINICOES####################
import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,xbmc,xbmcaddon,xbmcvfs,socket,HTMLParser
h = HTMLParser.HTMLParser()

addon_id = 'plugin.video.replaypt'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = '/resources/img/'

curtadoc_url = 'http://curtadoc.tv/'
##################################################

def listar_categorias():
	try:
		codigo_fonte = abrir_url(curtadoc_url+'acervo/')
	except:
		codigo_fonte = ''
	if codigo_fonte:
		match = re.findall('<div class="box-content darkcyan">.*?<h3 class="dark">(.+?)</h3>.*?<div class="destaque">.*?<img src="(.*?)".*?>.*?<a href="(.+?)" class="more_info">ver mais ([\d]+)  curtas</a>.*?</div>', codigo_fonte, re.DOTALL)
		for name, iconimage, url, count in match:
			addDir(name + ' - ' + count + ' curtas',url,446,iconimage)
		
def listar_episodios(url):
    try:
		codigo_fonte = abrir_url(url)
    except:
		codigo_fonte = ''
    if codigo_fonte:
		match = re.findall('<div class="curta-box span4">.*?<div class="destaque">.*?<a href=\'(.+?)\'>.*?<img src=["\'](.*?)["\'].*?>.*?<div class="fancy">.*?<div class="title">.*?<h4>[\W]+(.+?)                                        </h4>.*?<div class=\'sinopse\'>.*?</div>', codigo_fonte, re.DOTALL)
		for url, iconimage, name in match:
			addDir(name,url,447,iconimage,False)	
		next_page = re.search('<a class="next page-numbers" href="(.+?)">Próxima »</a>', codigo_fonte)
		if next_page != None:
				addDir('[B]Próxima >>[/B]',next_page.group(1),446,addonfolder+artfolder+'curtadoc.png')

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
				iframe = re.compile('src="(.+?)"').findall(trunk)[0]
			except:
				iframe = ''
			if iframe:
				if iframe.find('youtube') > -1:
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
				elif iframe.find('videolog.tv') > -1:
					resolver_iframe = videologtv_resolver(iframe)
					if resolver_iframe != 'videologtv_nao resolvido':
						playlist.add(resolver_iframe,xbmcgui.ListItem(name, thumbnailImage=iconimage))
				elif iframe.find('portacurtas.org.br') > -1:
					resolver_iframe = portacurtas_resolver(iframe)
					if resolver_iframe != 'portacurtas_nao resolvido':
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
    else:
		return 'daily_nao resolvido'
	
def vimeo_resolver(url):
	match = re.search('/([0-9]+)', url)
	if match:
		return 'plugin://plugin.video.vimeo/?action=play_video&videoid='+match.group(1)
	else:
		return 'vimeo_nao resolvido'

def videologtv_resolver(url):
	try:
		url = url.split("id_video=")[-1].split("?")[0]
		codigo_fonte = abrir_url('http://api.videolog.tv/video/'+url+'.json')
		return json.loads(codigo_fonte)['video']['url_mp4']
	except:
		return 'videologtv_nao resolvido'

def portacurtas_resolver(url):
	match = re.search('&shortName=([^&]+)', url)
	if match:
		return 'http://www.videosrelevantes.com.br/flvpc/'+match.group(1)+'.flv'
	else:
		return 'portacurtas_nao resolvido'
						
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