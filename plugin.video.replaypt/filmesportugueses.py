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

filmesportugueses_url = 'http://filmesportugueses.com/'
##################################################

def listar_categorias():
	addDir('Animações',filmesportugueses_url+'category/animacoes-portuguesas/',430,addonfolder+artfolder+'foldericon.png')
	addDir('Curtas Metragens',filmesportugueses_url+'category/curtas-metragens-portuguesas/',430,addonfolder+artfolder+'foldericon.png')
	addDir('Filmes Completos',filmesportugueses_url+'category/filmes-completos/',430,addonfolder+artfolder+'foldericon.png')
		
def listar_episodios(url):
	try: codigo_fonte = abrir_url(url)
	except: codigo_fonte = ''
	if codigo_fonte:
		match = re.findall('<h2 class="post-title"><a href="(.+?)" rel="bookmark" title=".+?">(.+?)</a></h2>(?:\r\n.*?<strong>.*?um filme de (.+?)<)?', codigo_fonte)
		for url, name, realizador in match:
			try:
				if realizador:
					addDir(name+' - um filme de '+realizador,url,431,'',False)
				else:
					addDir(name,url,431,'',False)
			except: pass
		try:	
			match_2 = re.compile('<a class="nextpostslink" href="(.+?)">').findall(codigo_fonte)
			for urlnext in match_2:
				addDir('[B]Próxima >>[/B]',urlnext,430,'')
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
					#função colocada aqui para poder alterar o iconimage para o do video no vimeo
					match = re.search('/([0-9]+)', iframe)
					if match:
						try:
							iconimage = json.loads(abrir_url('http://vimeo.com/api/v2/video/'+match.group(1)+'.json'))[0]['thumbnail_medium']
							playlist.add('plugin://plugin.video.vimeo/?action=play_video&videoid='+match.group(1),xbmcgui.ListItem(name, thumbnailImage=iconimage))
						except:
							pass
		#Resolver videos do youtube linkados
		match = re.compile('\<a href\=".*?youtube\.com/watch\?v\=([^&"]+).*?').findall(codigo_fonte)
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
						
############################################################################################################################

def abrir_url(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:28.0) Gecko/20100101 Firefox/28.0')
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