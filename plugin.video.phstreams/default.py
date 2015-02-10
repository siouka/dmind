# -*- coding: utf-8 -*-


import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc, xbmcaddon, os, sys, os.path
import hashlib,string,md5
import urlresolver
import pyxbmct.addonwindow as pyxbmct
from metahandler import metahandlers
import cookielib
import time,re
import datetime
import shutil
from resources.modules import main, vipplaylist,resolvers,nhl
from addon.common.addon import Addon
from addon.common.net import Net
try:
     from sqlite3 import dbapi2 as lite
except:
     from pysqlite2 import dbapi2 as lite

net = Net(http_debug=True)
ADDON = xbmcaddon.Addon(id='plugin.video.phstreams')
art = 'http://artpathg'
addon_id = 'plugin.video.phstreams'
addon = main.addon
addonp = xbmcaddon.Addon('plugin.video.phstreams')
selfAddon = xbmcaddon.Addon(id=addon_id)
settings = xbmcaddon.Addon(id='plugin.video.phstreams')
#===========Add Main File Here=======================================
listmaker ='http://mecca.watchkodi.com/phstreams.xml'
#========================Alternate Param Stuff=======================
mode = addon.queries["mode"]
url = addon.queries.get('url', '')
name = addon.queries.get('name', '')
thumb = addon.queries.get('thumb', '')
favtype = addon.queries.get('favtype', '')
mainimg = addon.queries.get('mainimg', '')
gomode = addon.queries.get('gomode', '')
iconimage = addon.queries.get('iconimage', '')
artwork = addon.queries.get('aretwork', '')
art = addon.queries.get('art', '')
fanart = addon.queries.get('fanart', '')
headers = addon.queries.get('headers', '')
loggedin = addon.queries.get('loggedin', '')
header_dict = addon.queries.get('header_dict', '')
sound = addon.queries.get('sound', '')
console = addon.queries.get('console', '')
dlfoldername = addon.queries.get('dlfoldername', '')
ext = addon.queries.get('ext', '')

addonPath = addonp.getAddonInfo('path')
artPath = addonPath + '/art/'

fanart = artPath +'fanart.jpg'
print "FANART AT MAIN IS = " +fanart
#======================== END Alternate Param Stuff=======================
#========================Start DataPaths==================================
datapaths = xbmc.translatePath(ADDON.getAddonInfo('profile'))
PlaylistPath=os.path.join(datapaths,'Playlists')
try: os.makedirs(PlaylistPath)
except: pass
UpdatePath=os.path.join(datapaths,'Update')
try: os.makedirs(UpdatePath)
except: pass
StreamPath=os.path.join(datapaths,'Stream Files')
try: os.makedirs(StreamPath)
except: pass
OneTime=os.path.join(datapaths,'OneTime')
try: os.makedirs(OneTime)
except: pass
Cachepath=os.path.join(datapaths,'Cache')
try: os.makedirs(Cachepath)
except: pass
Cachepathpl=os.path.join(datapaths,'Cache/playlists/')
try: os.makedirs(Cachepathpl)
except: pass
Cachepathim=os.path.join(datapaths,'Cache/images/')
try: os.makedirs(Cachepathim)
except: pass
Cachepathhd=os.path.join(datapaths,'Cache/hostdata/')
try: os.makedirs(Cachepathhd)
except: pass
#=======================End DataPaths===================================

# Global Stuff

     
def LogNotify(title,message,times,icon):
        xbmc.executebuiltin("XBMC.Notification("+title+","+message+","+times+","+icon+")")

#########################################################################
#GET LISTMAKER PATHS
def CATEGORIES():
    
    url = listmaker
    #if 'watchkodi'  in url: values = {'jibberish'} ###### used to stop from connecting to server

    link=vipplaylist.OPEN_URL(url).replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('type=playlistname=Sorted by user-assigned order','').replace('name=Sorted [COLOR=FF00FF00]by user-assigned order[/COLOR]','').replace('name=Live Tv Channels Twothumb','')
    match=re.compile('<name>(.+?)</name><link>(.+?)</link><thumbnail>(.+?)</thumbnail><mode>(.+?)</mode>').findall(link)
    for name,url,thumb,mode in match:
        if re.findall('http',thumb):
            thumbs=thumb
        else:
            thumbs=art+'/'+thumb+'.png'
        main.addDir(name,url,mode,thumbs,fanart,'','','')
        
    main.addDir('NHL','none','mainnhl',artPath+'hockey.jpg',fanart,'','','')  
    main.addDir('Manage Downloads','none','viewQueue','http://theredbadge.com/wp-content/uploads/2013/01/icon-folder.red_.download.png',fanart,'','','') 
    main.AUTO_VIEW('menu')    
    #main.addDir('Test VHD Login','none','vhdstartup','','','')

def DLVIDPAGE(url,name):
        params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb, 'dlfoldername':dlfoldername,}
        main.RESOLVEDL(name,url,thumb)
#=====================Optional Function for Poup Messages================================
def VPOP(image,sound):
    sound = sound
    print 'MUSIC IS  '+sound
    path = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.phstreams/resources/skins/DefaultSkin','media'))
    popimage=os.path.join(path, 'tempimage.jpg')
    main.downloadFile(image,popimage)
    musicsound=os.path.join(path, 'tempsound.mp3')
    main.downloadFile(sound,musicsound)
    if xbmc.getCondVisibility('system.platform.ios'):
        if not xbmc.getCondVisibility('system.platform.atv'):
            popup = HUBx('pop1.xml',selfAddon.getAddonInfo('path'),'DefaultSkin',close_time=20,logo_path='%s/resources/skins/DefaultSkin/media/Logo/'%selfAddon.getAddonInfo('path'),)
    if xbmc.getCondVisibility('system.platform.android'):
        popup = HUBx('pop1.xml',selfAddon.getAddonInfo('path'),'DefaultSkin',close_time=20,logo_path='%s/resources/skins/DefaultSkin/media/Logo/'%selfAddon.getAddonInfo('path'))
    else:
        popup = HUBx('pop.xml',selfAddon.getAddonInfo('path'),'DefaultSkin',close_time=20,logo_path='%s/resources/skins/DefaultSkin/media/Logo/'%selfAddon.getAddonInfo('path'))
    popup.doModal()
    del popup


class HUBx( xbmcgui.WindowXMLDialog ):
    def __init__( self, *args, **kwargs ):
        self.shut = kwargs['close_time'] 
        xbmc.executebuiltin( "Skin.Reset(AnimeWindowXMLDialogClose)" )
        xbmc.executebuiltin( "Skin.SetBool(AnimeWindowXMLDialogClose)" )
                                   
    def onInit( self):
        xbmc.Player().play('%s/resources/skins/DefaultSkin/media/tempsound.mp3'%selfAddon.getAddonInfo('path'))# Music   
        #xbmc.Player().play(musicsound)# Music
        while self.shut > 0:
            xbmc.sleep(1000)
            self.shut -= 1
        xbmc.Player().stop()
        self._close_dialog()
            
    def onFocus( self, controlID ): pass

    def onClick( self, controlID ): 
        if controlID == 12 or controlID == 7:
            xbmc.Player().stop()
            self._close_dialog()

    def onAction( self, action ):
        if action in [ 5, 6, 7, 9, 10, 92, 117 ] or action.getButtonCode() in [ 275, 257, 261 ]:
            xbmc.Player().stop()
            self._close_dialog()

    def _close_dialog( self ):
        path = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.phstreams/resources/skins/DefaultSkin','media'))
        popimage=os.path.join(path, 'tempimage.jpg')
        musicsound=os.path.join(path, 'tempsound.mp3')
        xbmc.executebuiltin( "Skin.Reset(AnimeWindowXMLDialogClose)" )
        time.sleep( .4 )
        self.close()
        os.remove(popimage)
        os.remove(musicsound)
            
################################################################################ Message ##########################################################################################################

def Message():
    help = SHOWMessage()
    help.doModal()
    del help


class SHOWMessage(xbmcgui.Window):
    def __init__(self):
        self.addControl(xbmcgui.ControlImage(0,0,1280,720,art+'/infoposter.png'))
    def onAction(self, action):
        if action == 92 or action == 10:
            xbmc.Player().stop()
            self.close()

def TextBoxes(heading,anounce):
    class TextBox():
        """Thanks to BSTRDMKR for this code:)"""
            # constants
        WINDOW = 10147
        CONTROL_LABEL = 1
        CONTROL_TEXTBOX = 5

        def __init__( self, *args, **kwargs):
            # activate the text viewer window
            xbmc.executebuiltin( "ActivateWindow(%d)" % ( self.WINDOW, ) )
            # get window
            self.win = xbmcgui.Window( self.WINDOW )
            # give window time to initialize
            xbmc.sleep( 500 )
            self.setControls()

        def setControls( self ):
            # set heading
            self.win.getControl( self.CONTROL_LABEL ).setLabel(heading)
            try:
                f = open(anounce)
                text = f.read()
            except: text=anounce
            self.win.getControl( self.CONTROL_TEXTBOX ).setText(text)
            return
    TextBox()
################################################################################ Modes ##########################################################################################################



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



try: name=urllib.unquote_plus(params["name"])
except: pass
try: url=urllib.unquote_plus(params["url"])
except: pass
try: mode=int(params["mode"])
except: pass
try:
    iconimage=urllib.unquote_plus(params["iconimage"])
    iconimage = iconimage.replace(' ','%20')
except: pass
try: plot=urllib.unquote_plus(params["plot"])
except: pass
try:
    fanart=urllib.unquote_plus(params["fanart"])
    fanart = fanart.replace(' ','%20')
except: pass
try: genre=urllib.unquote_plus(params["genre"])
except: pass
try: title=urllib.unquote_plus(params["title"])
except: pass
try: episode=int(params["episode"])
except: pass
try: season=int(params["season"])
except: pass
try: location=urllib.unquote_plus(params["location"])
except: pass
try: path=urllib.unquote_plus(params["path"])
except: pass
try: sound=urllib.unquote_plus(params["sound"])
except: pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "Thumb: "+str(iconimage)


if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
        

elif mode=='dmode':
    print ""+url
    vipplaylist.DMODE(url)

elif mode=='ndmode':
    print ""+url
    vipplaylist.NDMODE(name,url)

elif mode=='vpop':
    VPOP(url,sound)

elif mode=='linkmode':
    print ""+url
    vipplaylist.LINKMODE(name,url,thumb)

elif mode=='sublinks':
    print ""+url
    vipplaylist.SUBLINKS(name,url,thumb)    

elif mode=='liveresolver':
    print ""+url
    vipplaylist.LIVERESOLVER(name,url,thumb)

elif mode=='liveresolve':
    print ""+url
    vipplaylist.LIVERESOLVE(name,url,thumb)

elif mode=='vhdlogin':
    resolvers.VHDLOGIN()

elif mode=='vhdstartup':
    resolvers.VHDSTARTUP() 
    
elif mode=='dlvidpage':
        print ""+url
        DLVIDPAGE(url,name) 
        
elif mode=='viewQueue':
        print ""+url
        main.viewQueue()

elif mode=='download':
        print ""+url
        main.download()
        
elif mode=='killq':

        main.KILLQ()
        

elif mode=='removeFromQueue':
        print ""+url
        main.removeFromQueue(name,url,thumb,ext,console)

elif mode=='killsleep':
        print ""+url
        main.KILLSLEEP()
        
elif mode=='mainnhl':
        print ""+url
        nhl.MAINNHL(url)

elif mode=='mainnhlarch':
        print ""+url
        nhl.MAINNHLARCH(url)

elif mode=='nhllistreams':
    print ""+url
    nhl.LISTSTREAMS(name,url)
    
elif mode=='nhllink':
    print ""+url
    nhl.LINK(name,url,iconimage)

elif mode == 'trailer':
    main.trailer(url)
elif mode == 'trailersearch':
    main.TRAILERSEARCH(url, name, iconimage)    

xbmcplugin.endOfDirectory(int(sys.argv[1]))        
