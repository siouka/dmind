#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Copyright 2014 Mafarricos

##############BIBLIOTECAS A IMPORTAR E DEFINICOES####################
import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,xbmc,xbmcaddon,xbmcvfs,socket,HTMLParser
import json
h = HTMLParser.HTMLParser()

addon_id = 'plugin.video.replaypt'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = '/resources/img/'

g1novelas_url = 'http://www.g1novelas.org/'
################################################## 

def CATEGORIES_g1():
	addDir('[B]Mudar para categorias[/B]',g1novelas_url,406,addonfolder+artfolder+'g1novelas.png',True)
	listar_episodiosg1(g1novelas_url)

def alterar_vistag1(url):
	addDir('[B]Mudar para últimas[/B]',url,403,addonfolder+artfolder+'g1novelas.png');
	try: codigo_fonte = abrir_url(url)
	except: codigo_fonte = ''
	if codigo_fonte:
		match = re.compile('class="level-0" value="(.+?)">(.+?)</option>').findall(codigo_fonte)
		for cat,titulo in match:
			addDir(titulo,url + '?cat=' + str(cat),404,addonfolder+artfolder+'g1novelas.png')
		
def listar_episodiosg1(url):
    try:
		codigo_fonte = abrir_url(url)
    except:
		codigo_fonte = ''
    if codigo_fonte:
		html_source_trunk = re.findall('Click here to instantly play this video(.*?)</h2></div>', codigo_fonte, re.DOTALL)
		for trunk in html_source_trunk:
			urletitulo = re.compile('href="(.+?)">(.+?)</a>').findall(trunk)
			img = re.compile('src="(.+?)"').findall(trunk)
			try:
				addDir(urletitulo[0][1].replace('&#8211;',''),urletitulo[0][0],405,img[0],False)
			except: pass
		try:	
			match = re.compile('class="nextpostslink" href="(.+?)">').findall(codigo_fonte)
			for urlnext in match:
				addDir('[B]Próxima >>[/B]',urlnext,404,addonfolder+artfolder+'g1novelas.png')
		except:
			pass

def procurar_fontesg1(url,name,iconimage):
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