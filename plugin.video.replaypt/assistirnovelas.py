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

assistirnovelas_url = 'http://www.assistirnovelas.tv/'
##################################################

def CATEGORIES_assistirnovelas():
	listar_categorias(assistirnovelas_url)

def listar_categorias(url):
	try: codigo_fonte = abrir_url(url)
	except: codigo_fonte = ''
	if codigo_fonte:
		match = re.compile('<li class=".+?"><a href="(.+?)".*?>(.+?)</a>\n</li>').findall(codigo_fonte)
		for url,name in match:
			addDir(name,url,416,addonfolder+artfolder+'assistirnovelas.png')
		
def listar_episodios(url):
    try: codigo_fonte = abrir_url(url)
    except: codigo_fonte = ''
    if codigo_fonte:
		match = re.findall("<div class=\"post-content\">.*?<h2><a href='(.+?)'.*?>(.+?)</a></h2>.+?<div class=\"post-thumb-container clearfix\">.+?<img.+?src=\"(.+?)\".*?>.+?</div>", codigo_fonte, re.DOTALL)
		for url, name, iconimage in match:
			try:
				addDir(name,url,417,iconimage,False)
			except: pass
		try:	
			html_pagination = re.search("<div class='pagination clearfix'>(.+?)</div>", codigo_fonte)
			if html_pagination != None:
				next_page = re.search("<span class='current'>.+?</span><a href='(.+?)' class='inactive'.+?>.+?</a>", html_pagination.group(1))
				if next_page != None:
					addDir('[B]Próxima >>[/B]',next_page.group(1),416,addonfolder+artfolder+'assistirnovelas.png')
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
			print 'Assistirnovelas: html5 new player detectado...'
			codigo_fonte_2 = abrir_url('http://nossocanal.net/player/player.php?novela='+html5_new_player.group(1)+'&data='+html5_new_player.group(2)+'&categoria='+html5_new_player.group(3)+'&partes='+html5_new_player.group(4))
			mp4_match = re.compile("file: '(.+?)',").findall(codigo_fonte_2)
			for url in mp4_match:
				playlist.add(url,xbmcgui.ListItem(name, thumbnailImage=iconimage))
		html5_player = re.search("<script type=\"text/javascript\">.+?<!\[CDATA\[.+?data='(.+?)'; novela='(.+?)'; partes='(.+?)'; width='(.+?)'; height='(.+?)';.*?// ]]&gt;</script><script type=\"text/javascript\" src=\"http://www.novelasgravadas.com/asassistirnovelaa.js\"></script>", codigo_fonte, re.DOTALL)
		if html5_player != None:
			print 'Assistirnovelas: html5 old player detectado...'
			codigo_fonte_2 = abrir_url('http://novelasgravadas.com/asplayernovelas.php?data='+html5_player.group(1)+'&novela='+html5_player.group(2)+'&partes='+html5_player.group(3)+'&width='+html5_player.group(4)+'&height='+html5_player.group(5))
			mp4_match = re.compile("file: '(.+?)',").findall(codigo_fonte_2)
			for url in mp4_match:
				playlist.add(url,xbmcgui.ListItem(name, thumbnailImage=iconimage))
		partes_player = re.search("\<script type\=\"text/javascript\"\>// \<\!\[CDATA\[(.+?)// \]\]&gt;\</script\>\<script type\=\"text/javascript\" src\=\"http\://www\.novelasgravadas\.com/partesvideo\.js\"\>\</script\>", codigo_fonte, re.DOTALL)
		if partes_player != None:
			print 'Assistirnovelas: partes player detectado...'
			total_partes = re.search("partes\='([\d]+?)';", partes_player.group(1))
			if total_partes:
				for x in range(0, int(total_partes.group(1))):
					vid = re.search('vid'+str(x+1)+"='(.+?)';", partes_player.group(1))
					if vid:
						playlist.add('plugin://plugin.video.dailymotion_com/?mode=playVideo&url='+vid.group(1),xbmcgui.ListItem(name, thumbnailImage=iconimage))
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