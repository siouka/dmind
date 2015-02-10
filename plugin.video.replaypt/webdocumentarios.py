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

webdocumentarios_url = 'http://www.webdocumentarios.com/'
##################################################

def CATEGORIES_webdocumentarios():
	addDir('[B]Mudar para categorias[/B]',webdocumentarios_url,440,addonfolder+artfolder+'webdocumentarios.png',True)
	listar_episodios(webdocumentarios_url)

def alterar_vista(url):
	addDir('[B]Mudar para últimas[/B]',url,437,addonfolder+artfolder+'webdocumentarios.png');
	try:
		codigo_fonte = abrir_url(url)
	except:
		codigo_fonte = ''
	if codigo_fonte:
		match = re.search('<h4>Categorias</h4>(.+?)</div>', codigo_fonte, re.DOTALL)
		if match:
			addDir('[COLOR blue][B]Categorias[/B][/COLOR]','',437,addonfolder+artfolder+'webdocumentarios.png',False)
			match_2 = re.findall('<li.*?><a href="(.+?)".*?>(.+?)</a></li>', match.group(1))
			for link, name in match_2:
				addDir(h.unescape(name).encode('utf-8'),link,438,addonfolder+artfolder+'webdocumentarios.png')
		match = re.search('<h4>Tags</h4>(.+?)</div>', codigo_fonte, re.DOTALL)
		if match:
			addDir('[COLOR blue][B]Tags[/B][/COLOR]','',437,addonfolder+artfolder+'webdocumentarios.png',False)
			match_2 = re.findall('<a href="(.+?)".*?>(.+?)</a>', match.group(1))
			for link, name in match_2:
				addDir(name,link,438,addonfolder+artfolder+'webdocumentarios.png')

def listar_episodios(url):
	try:
		codigo_fonte = abrir_url(url)
	except:
		codigo_fonte = ''
	if codigo_fonte:
		match = re.findall('<div class=["]?pm-li-video["]?>.*?<span class=["]?pm-thumb-fix-clip["]?><img src="(.+?)".*?>.*?<a href="(.+?)" class=["]?pm-title-link.*?".*?>(.+?)</a></h3>.*?</div>', codigo_fonte, re.DOTALL)
		for iconimage, link, name in match:
			addDir(name,link,439,iconimage,False)
		html_pagination = re.search('<li class="">\n<a href="(.+?)">&raquo;</a>\n</li>', codigo_fonte)
		if html_pagination:
			addDir('[B]Próxima >>[/B]',html_pagination.group(1),438,addonfolder+artfolder+'webdocumentarios.png')

def procurar_fontes(url,name,iconimage):
	progress = xbmcgui.DialogProgress()
	progress.create('Replay PT', 'Procurando fontes...')
	progress.update(0)
	try:
		codigo_fonte = abrir_url(url)
	except:
		codigo_fonte = ''
	if codigo_fonte:
		jwplayer = re.search("[^_]file:'(.+?)',", codigo_fonte)
		if jwplayer:
			if jwplayer.group(1).find('youtube') > -1:
				video_url = youtube_resolver(jwplayer.group(1))
			else:
				video_url = jwplayer.group(1)
		if progress.iscanceled():
			sys.exit(0)
		progress.update(100)
		progress.close()
		if video_url:
			if video_url != 'youtube_nao resolvido':
				listitem = xbmcgui.ListItem(label=name, iconImage=str(iconimage), thumbnailImage=str(iconimage), path=url)
				listitem.setProperty('IsPlayable', 'true')
				try:
					xbmc.Player().play(item=video_url, listitem=listitem)
				except:
					pass
			else:
				dialog = xbmcgui.Dialog()
				ok = dialog.ok('Replay PT', 'Erro ao resolver youtube...')
		else:
			dialog = xbmcgui.Dialog()
			ok = dialog.ok('Replay PT', 'Nenhuma fonte suportada encontrada...')

def youtube_resolver(url):
	match = re.compile('.*?youtube.com/embed/([^?"]+).*?').findall(url)
	if match:
		return 'plugin://plugin.video.youtube/?action=play_video&videoid=' + str(match[0])
	match = re.compile('.*?youtube.com/watch\?v=([^&"]+).*?').findall(url)
	if match:
		return 'plugin://plugin.video.youtube/?action=play_video&videoid=' + str(match[0])
	return 'youtube_nao resolvido'
						
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