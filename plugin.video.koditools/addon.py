#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Copyright 2014 Anonymous
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


##############BIBLIOTECAS A IMPORTAR E DEFINICOES####################

import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,HTMLParser,os,sys,time,subprocess,shutil,hashlib
from resources.lib.lib import librtmp
librtmp = librtmp()
h = HTMLParser.HTMLParser()

versao = '1.1.6'
addon_id = 'plugin.video.xbmctools'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
if not os.path.exists(addonfolder): addonfolder = addonfolder.decode('utf-8')
artfolder = addonfolder + '/resources/img/'
dialog = xbmcgui.Dialog()
xbmc_version = int(xbmc.getInfoLabel("System.BuildVersion" )[0:2])
traducaoma= selfAddon.getLocalizedString

def traducao(texto):
	return traducaoma(texto).encode('utf-8')
	
if selfAddon.getSetting('force-openelec') == "false": forcar_openelec = False
else: forcar_openelec = True
if selfAddon.getSetting('first_run') == "true": first_run = True
else: first_run = False
################################################## 

#MENUS############################################

def CATEGORIES():
	if xbmc.getCondVisibility('system.platform.windows'):
	#WINDOWS
		if first_run:
			mensagem_os("Windows")
			dialog.ok(traducao(2000), traducao(2001))
			selfAddon.setSetting('first_run',value='false')
		if xbmc_version < 14: addDir(traducao(2002),"windows",1,artfolder + "keyboard.png")
		addDir(traducao(2003),"windows",3,artfolder + "dll.png",False)
		addDir(traducao(2004),"windows",9,artfolder + "backup.png")
		addLink('','','nothing')
		librtmp.VersionChecker("windows")
	#-----------------------------------------------------------------------
	elif xbmc.getCondVisibility('System.Platform.OSX'):
		if first_run:
			mensagem_os("macOS")
			if os.uname()[4] == "i686" or os.uname()[4] == "i386": selfAddon.setSetting('mac_bits',value=str(0))
			else:
				if librtmp.xbmc_bit_version() == "x32": selfAddon.setSetting('mac_bits',value=str(0))
				elif librtmp.xbmc_bit_version() == "x64": selfAddon.setSetting('mac_bits',value=str(1))
				else:
					ret = dialog.select(traducao(2056), ['x86', 'x64'])
					if ret == -1: sys.exit(0); return;
					selfAddon.setSetting('mac_bits',value=str(ret))
			selfAddon.setSetting('first_run',value='false')
		
		addDir(traducao(2003),"macos",3,artfolder + "dll.png",False)
		addDir(traducao(2004),"macos",9,artfolder + "backup.png")
		addLink('','','nothing')
		librtmp.VersionChecker("macos")
	elif xbmc.getCondVisibility('system.platform.linux') and not xbmc.getCondVisibility('system.platform.Android'):
		if os.uname()[4] == 'armv6l': 
			#RASPBERRY
			if re.search(os.uname()[1],"openelec",re.IGNORECASE) or forcar_openelec:
				mensagem_os("Openelec",True)
				addDir(traducao(2003),"raspberry",8,artfolder + "dll.png",False)
				addDir(traducao(2004),"openelec",9,artfolder + "backup.png")
				addLink('','','nothing')
				librtmp.VersionChecker("openelec")
			else:
				mensagem_os("RaspberryPI (OS)",True)
				librtmp.set_librtmp_path()
				if xbmc_version < 14: addDir(traducao(2002),"linux",1,artfolder + "keyboard.png")
				addDir(traducao(2003),"raspberry",7,artfolder + "dll.png",False)
				addDir(traducao(2004),"raspberry",9,artfolder + "backup.png")
				addLink('','','nothing')
				librtmp.VersionChecker("raspberry")
			#-------------------------------------------------------------------
		elif os.uname()[4] == 'armv7l':
			#ARMv7
			erro_os()
			'''if re.search(os.uname()[1],"openelec",re.IGNORECASE) or forcar_openelec:
				mensagem_os("Openelec",True)
				addDir(traducao(2003),"raspberry",8,artfolder + "dll.png",False)
				addDir(traducao(2004),"openelec",9,artfolder + "backup.png")
				addLink('','','nothing')
				librtmp.VersionChecker("openelec")
			else:
				mensagem_os("Linux",True)
				librtmp.set_librtmp_path()
				addDir(traducao(2003),"armv7",3,artfolder + "dll.png",False) 
				addDir(traducao(2004),"armv7",9,artfolder + "backup.png")
				addLink('','','nothing')
				librtmp.VersionChecker("raspberry")'''
		else: 
			#LINUX
			if re.search(os.uname()[1],"openelec",re.IGNORECASE) or forcar_openelec: 
				mensagem_os("Openelec",True)
				addDir(traducao(2003),"-",8,artfolder + "dll.png",False)
				addDir(traducao(2004),"openelec",9,artfolder + "backup.png")
				addLink('','','nothing')
				librtmp.VersionChecker("openelec pc")
			else:
				mensagem_os("Linux",True)
				librtmp.set_librtmp_path()
				if xbmc_version < 14: addDir(traducao(2002),"linux",1,artfolder + "keyboard.png")
				addDir(traducao(2003),"linux",7,artfolder + "dll.png",False)
				addDir(traducao(2004),"linux",9,artfolder + "backup.png")
				addLink('','','nothing')
				librtmp.VersionChecker("linux")
			#-------------------------------------------------------------------
	elif xbmc.getCondVisibility('system.platform.Android'): 
	#ANDROID
		mensagem_os("Android",True)
		if xbmc_version < 14: addDir(traducao(2002),"android",1,artfolder + "keyboard.png")
		addDir("Download APK","-",11,artfolder + "apk.png",False)
		addDir(traducao(2003)+" [COLOR blue](XBMC Gotham 13)[/COLOR]","-",5,artfolder + "dll.png",False)
		if librtmp.android_hack_checker(): addDir(traducao(2059)+" [COLOR blue](On)[/COLOR]","-",12,artfolder + "hack.png",False)
		else: addDir(traducao(2059)+" [COLOR red](Off)[/COLOR]","-",13,artfolder + "hack.png",False)
		addDir(traducao(2004),"android",9,artfolder + "backup.png")
		addLink('','','nothing')
		librtmp.VersionChecker("android")
	#-------------------------------------------------------------------
	elif xbmc.getCondVisibility('system.platform.IOS'): 
	#IOS
		mensagem_os("iOS",True)
		addDir(traducao(2003),"ios",3,artfolder + "dll.png",False)
		addDir(traducao(2004),"ios",9,artfolder + "backup.png")
		addLink('','','nothing')
		librtmp.VersionChecker("ios")
	#-------------------------------------------------------------------
	else: erro_os()
	
	addDir(traducao(2064),"-",14,artfolder + "settings.png", False)
	disponivel=versao_disponivel() # nas categorias
	if disponivel==versao: addLink('[B][COLOR white]'+traducao(2005)+' (' + versao + ')[/COLOR][/B]','',artfolder + 'versao.png')
	elif disponivel=='Erro ao verificar a versão!': addLink('[B][COLOR white]' + traducao(2006) + '[/COLOR][/B]','',artfolder + 'versao.png')
	else: addLink('[B][COLOR white]'+traducao(2007)+' ('+ disponivel + '). '+traducao(2008)+'[/COLOR][/B]','',artfolder + 'versao.png')
	print "--------- XBMC Tools ---------"

###################################################################################
def mensagem_os(so_name,on_first_run = False):
	if on_first_run:
		if first_run: 
			dialog.ok(traducao(2016), traducao(2035) + so_name +".",traducao(2036))
			selfAddon.setSetting('first_run',value='false')
	else: dialog.ok(traducao(2016), traducao(2035) + so_name +".",traducao(2036))
	

def erro_os():
	dialog.ok(traducao(2014), traducao(2037))
	sys.exit(0)

def versao_disponivel():
	try:
		codigo_fonte=abrir_url('http://anonymous-repo.googlecode.com/svn/trunk/anonymous-repo/plugin.video.xbmctools/addon.xml')
		match=re.compile('<addon id="plugin.video.xbmctools" name="K0di Tools" version="(.+?)"').findall(codigo_fonte)[0]
	except:
		match='Erro ao verificar a versão!'
	return match

def abrir_url(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

def addLink(name,url,iconimage,total=1):
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', addonfolder + '/fanart.jpg')
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,totalItems=total)
	return ok

def addDir(name,url,mode,iconimage,pasta = True,total=1):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', addonfolder + '/fanart.jpg')
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)
	return ok

############################################################################################################
#                                               GET PARAMS                                                 #
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

try: url=urllib.unquote_plus(params["url"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: mode=int(params["mode"])
except: pass
try: iconimage=urllib.unquote_plus(params["iconimage"])
except: pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "Iconimage: "+str(iconimage)

###############################################################################################################
#                                                   MODOS                                                     #
###############################################################################################################

if mode==None or url==None or len(url)<1: CATEGORIES()
elif mode==1: librtmp.keyboard(url)
elif mode==2: librtmp.change_keyboard(url)
elif mode==3: librtmp.librtmp_updater(url)
elif mode==5: librtmp.librtmp_android()
elif mode==6: librtmp.change_keyboard_linux(url)
elif mode==7: librtmp.librtmp_linux(url)
elif mode==8: librtmp.librtmp_openelec(url)
elif mode==9: librtmp.backup(url)
elif mode==10: librtmp.backup_(url)
elif mode==11: librtmp.download_apk()
elif mode==12: librtmp.android_hack_off()
elif mode==13: librtmp.android_hack_on()
elif mode==14: selfAddon.openSettings()
	
xbmcplugin.endOfDirectory(int(sys.argv[1]))
