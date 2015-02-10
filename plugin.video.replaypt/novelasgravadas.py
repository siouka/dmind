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

novelasgravadas_url = 'http://www.novelasgravadas.com/'
##################################################

def listar_categorias():
	try:
		codigo_fonte = abrir_url(novelasgravadas_url+'/home/')
	except:
		codigo_fonte = ''
	if codigo_fonte:
		match = re.findall('<li id="menu-item.*?".*?>.*?<span class="link_text">(.+?)</span>.*?<ul class="mega_dropdown">(.+?)</ul>.*?<!-- /.mega_dropdown -->.*?</li>', codigo_fonte, re.DOTALL)
		if match:
			for categoria, html_source in match:
				categoria = categoria.strip()
				if categoria == 'Início':
					categoria = 'Novelas'
				match_2 = re.findall('<li.*?>.*?<a href="(.+?)".*?>.*?<span class="link_text">(.+?)</span>.*?</span>.*?</a>.*?</li>', html_source, re.DOTALL)
				if match_2:
					addDir('[COLOR blue][B]'+categoria+'[/B][/COLOR]','',411,addonfolder+artfolder+'novelasgravadas.png',False)
					for url, name in match_2:
						name = name.strip()
						addDir(name,url,412,addonfolder+artfolder+'novelasgravadas.png')
		
def listar_episodios(url):
    try:
		codigo_fonte = abrir_url(url)
    except:
		codigo_fonte = ''
    if codigo_fonte:
		match = re.findall('<div class="post">.*?<div class="post_img_box">.*?<img.*?src="(.+?)".*?>.*?</div>.*?<h1><a.*?href="(.+?)".*?>(.+?)</a></h1>', codigo_fonte, re.DOTALL)
		for iconimage, url, name in match:
			try:
				addDir(name,url,413,iconimage,False)
			except:
				pass
		try:	
			html_pagination = re.search("<a href='([^\"']+?)'>&rsaquo;</a>", codigo_fonte)
			if html_pagination != None:
				addDir('[B]Próxima >>[/B]',html_pagination.group(1),412,addonfolder+artfolder+'novelasgravadas.png')
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
		print 'iniciando procura de fontes...'
		#players proprietários do site
		html5_new_player = re.search("<script>.+?<!\[CDATA\[.*?novela='(.+?)'; data='(.+?)'; categoria='(.+?)';.*? partes='(.+?)';.*?// ]]&gt;</script><script src=\"http://nossocanal.net/player/novela.js\"></script>", codigo_fonte, re.DOTALL)
		if html5_new_player != None:
			print 'Novelasgravadas: html5 new player detectado...'
			codigo_fonte_2 = abrir_url('http://nossocanal.net/player/player.php?novela='+html5_new_player.group(1)+'&data='+html5_new_player.group(2)+'&categoria='+html5_new_player.group(3)+'&partes='+html5_new_player.group(4))
			mp4_match = re.compile("file: '(.+?)',").findall(codigo_fonte_2)
			for url in mp4_match:
				playlist.add(url,xbmcgui.ListItem(name, thumbnailImage=iconimage))
		html5_player = re.search("<script type=\"text/javascript\">.+?<!\[CDATA\[.+?data='(.+?)'; novela='(.+?)'; partes='(.+?)'; width='(.+?)'; height='(.+?)';.*?// ]]&gt;</script><script type=\"text/javascript\" src=\"http://www.novelasgravadas.com/assistirnovela.js\"></script>", codigo_fonte, re.DOTALL)
		if html5_player != None:
			print 'Novelasgravadas: html5 old player detectado...'
			codigo_fonte_2 = abrir_url('http://novelasgravadas.com/playernovelas.php?data='+html5_player.group(1)+'&novela='+html5_player.group(2)+'&partes='+html5_player.group(3)+'&width='+html5_player.group(4)+'&height='+html5_player.group(5))
			mp4_match = re.compile("file: '(.+?)',").findall(codigo_fonte_2)
			for url in mp4_match:
				playlist.add(url,xbmcgui.ListItem(name, thumbnailImage=iconimage))
		old_player = re.search("<script type=\"text/javascript\">.+?<!\[CDATA\[.+?data='(.+?)'; novela='(.+?)'; width='(.+?)'; height='(.+?)';.*?// ]]&gt;</script><script type=\"text/javascript\" src=\"http://www.novelasgravadas.com/novelas.js\"></script>", codigo_fonte, re.DOTALL)
		if old_player != None:
			print 'Novelasgravadas: old player detectado...'
			codigo_fonte_2 = abrir_url('http://novelasgravadas.com/xml/'+old_player.group(2)+'/'+old_player.group(1)+'.xml')
			file_match = re.compile("<location>(.+?)</location>").findall(codigo_fonte_2)
			for url in file_match:
				playlist.add(url,xbmcgui.ListItem(name, thumbnailImage=iconimage))
		partes_player = re.search("\<script type\=\"text/javascript\"\>// \<\!\[CDATA\[(.+?)// \]\]&gt;\</script\>\<script type\=\"text/javascript\" src\=\"http\://www\.novelasgravadas\.com/partesvideo\.js\"\>\</script\>", codigo_fonte, re.DOTALL)
		if partes_player != None:
			print 'Novelasgravadas: partes player detectado...'
			total_partes = re.search("partes\='([\d]+?)';", partes_player.group(1))
			if total_partes:
				for x in range(0, int(total_partes.group(1))):
					vid = re.search('vid'+str(x+1)+"='(.+?)';", partes_player.group(1))
					if vid:
						playlist.add('plugin://plugin.video.dailymotion_com/?mode=playVideo&url='+vid.group(1),xbmcgui.ListItem(name, thumbnailImage=iconimage))
		#outros tipos de players externos
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
				elif iframe.find('vk.com') > -1:
					resolver_iframe = vkcom_resolver(iframe)
					if resolver_iframe != 'vkcom_nao resolvido':
						playlist.add(resolver_iframe,xbmcgui.ListItem(name, thumbnailImage=iconimage))
				elif iframe.find('r7.com') > -1:
					resolver_iframe = r7_resolver(iframe)
					if resolver_iframe != 'r7_nao resolvido':
						playlist.add(resolver_iframe,xbmcgui.ListItem(name, thumbnailImage=iconimage))
				elif iframe.find('sbt.com.br') > -1:
					resolver_iframe = sbtcombr_resolver(iframe)
					if resolver_iframe != 'sbtcombr_nao resolvido':
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
			return 'vkcom_nao resolvido'
	else:
		return 'vkcom_nao resolvido'

def r7_resolver(url):
    source = abrir_url(url)
    match = re.compile("media src='(.+?)'").findall(source)
    if match: return match[0]
    else: return 'r7_nao resolvido'
	
def sbtcombr_resolver(url):
	codigo_fonte = abrir_url(h.unescape(url))
	match = re.search('<iframe.+?src="(.+?)"', codigo_fonte)
	if match != None:
		codigo_fonte_2 = abrir_url(match.group(1))
		match_2 = re.search('window.mediaJson = (.+?);', codigo_fonte_2)
		if match_2 != None:
			try:
				decoded_data = json.loads(match_2.group(1))
				for x in range(0, len(decoded_data['deliveryRules'])):
					if decoded_data['deliveryRules'][x]['rule']['ruleName'] == 'r1':
						return decoded_data['deliveryRules'][x]['outputList'][0]['url']
			except:
				pass
	else:
		return 'sbtcombr_nao resolvido'
						
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