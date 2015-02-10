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

podflix_url = 'http://podflix.com.br/'
##################################################

def listar_categorias():
	addDir('Lançamentos','?catGroup=1',449,addonfolder+artfolder+'podflix.png')
	addDir('Novos Projetos','?catGroup=2',449,addonfolder+artfolder+'podflix.png')
	addDir('Culturas e Tradições Religiosas','?catGroup=12',449,addonfolder+artfolder+'podflix.png')
	addDir('Entretenimento','?catGroup=10',449,addonfolder+artfolder+'podflix.png')
	addDir('Entrevistas','?catGroup=8',449,addonfolder+artfolder+'podflix.png')
	addDir('Esporte','?catGroup=11',449,addonfolder+artfolder+'podflix.png')
	addDir('Filmes','?catGroup=3',449,addonfolder+artfolder+'podflix.png')
	addDir('Jogos','?catGroup=4',449,addonfolder+artfolder+'podflix.png')
	addDir('História Geral','?catGroup=13',449,addonfolder+artfolder+'podflix.png')
	addDir('Livros e HQs','?catGroup=5',449,addonfolder+artfolder+'podflix.png')
	addDir('Música','?catGroup=9',449,addonfolder+artfolder+'podflix.png')
	addDir('Tecnologia','?catGroup=6',449,addonfolder+artfolder+'podflix.png')
	addDir('Variedades','?catGroup=7',449,addonfolder+artfolder+'podflix.png')
		
def listar_episodios(url):
    try:
		codigo_fonte = abrir_url(podflix_url+'lib/player/functions/json.php'+url)
    except:
		codigo_fonte = ''
    if codigo_fonte:
		decoded_data = json.loads(codigo_fonte)
		try:
			if len(decoded_data) > 0:
				for x in range(0, len(decoded_data)):
					podcast = decoded_data[x]['podcast'].encode("utf8")
					title = decoded_data[x]['title'].encode("utf8")
					audiofile = decoded_data[x]['audiofile'].encode("utf8")
					iconimage = decoded_data[x]['thumbnail'].encode("utf8")
					addDir('[B]'+podcast+'[/B] - '+title,audiofile,99,iconimage,False)
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