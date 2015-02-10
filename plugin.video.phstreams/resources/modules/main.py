'''# -*- coding: cp1252 -*-'''
# -*- coding: utf-8 -*-
# Main Module by: Blazetamer

import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,urlresolver,xbmc,os,xbmcaddon
import threading
import pyxbmct.addonwindow as pyxbmct
import hashlib,string,md5
#from urllib.request import urlopen
#from urllib.request import Request
from metahandler import metahandlers
try:
        from addon.common.addon import Addon

except:
        from t0mm0.common.addon import Addon
addon_id = 'plugin.video.phstreams'

addon = Addon(addon_id, sys.argv)
try:
        from addon.common.net import Net

except:  
        from t0mm0.common.net import Net
net = Net()
        
try:
     import StorageServer
except:
     import storageserverdummy as StorageServer

import time
settings = xbmcaddon.Addon(id=addon_id)
ADDON = xbmcaddon.Addon(id='plugin.video.phstreams')
download_path = settings.getSetting('download_folder')
cache = StorageServer.StorageServer("Phoenix", 0)
supportsite = 'tvaddons.ag'
selfAddon = xbmcaddon.Addon(id=addon_id)
datapath = xbmc.translatePath(selfAddon.getAddonInfo('profile'))
settings = xbmcaddon.Addon(id='plugin.video.phstreams')
#========================Alternate Param Stuff=======================
mode = addon.queries['mode']
url = addon.queries.get('url', '')
name = addon.queries.get('name', '')
thumb = addon.queries.get('thumb', '')
favtype = addon.queries.get('favtype', '')
mainimg = addon.queries.get('mainimg', '')
gomode = addon.queries.get('gomode', '')
iconimage = addon.queries.get('iconimage', '')
artwork = addon.queries.get('artwork', '')
art = addon.queries.get('art', '')
fanart = addon.queries.get('fanart', '')
sound = addon.queries.get('sound', '')
console = addon.queries.get('console', '')
dlfoldername = addon.queries.get('dlfoldername', '')
ext = addon.queries.get('ext', '')
fanartimage = addon.queries.get('fanartimage', '')
data = addon.queries.get('data', '')

stop = addon.queries.get('stop', '')
file_name = addon.queries.get('file_name', '')
#======================== END Alternate Param Stuff=======================

phpath = selfAddon.getAddonInfo('path')
getinfo  = settings.getSetting('md_switch')
addonp = xbmcaddon.Addon('plugin.video.phstreams')
addonPath = addonp.getAddonInfo('path')
artPath = addonPath + '/art/'
mainicon = artPath +'icon.png'
fanart = artPath +'fanart.jpg'
#START CACHE SESSION================================

grab=metahandlers.MetaData()

def GRABMETA(name,year):
        
        meta = grab.get_meta('movie',name,year,None,None)
        infoLabels = {'rating': meta['rating'],'duration': meta['duration'],'genre': meta['genre'],'mpaa':"rated %s"%meta['mpaa'],
        'plot': meta['plot'],'title': meta['title'],'writer': meta['writer'],'cover_url': meta['cover_url'],
        'director': meta['director'],'cast': meta['cast'],'backdrop_url': meta['backdrop_url'],'tmdb_id': meta['tmdb_id'],'year': meta['year']}
                
        return infoLabels
        
        

def GRABTVMETA(name,year):
        
        meta = grab.get_meta('tvshow',name,year,None,None)
        infoLabels = {'rating': meta['rating'],'duration': meta['duration'],'genre': meta['genre'],'mpaa':"rated %s"%meta['mpaa'],
        'plot': meta['plot'],'title': meta['title'],'cover_url': meta['cover_url'],
        'cast': meta['cast'],'backdrop_url': meta['backdrop_url'],'imdb_id': meta['imdb_id'],'year': meta['year']}
                
        return infoLabels
        

def GRABEPISODEMETA(name,imdb_id,season,episode):
        
        meta = grab.get_episode_meta('tvshow',name,imdb_id,season,episode)
        infoLabels = {'rating': meta['rating'],'duration': meta['duration'],'genre': meta['genre'],'mpaa':"rated %s"%meta['mpaa'],
        'plot': meta['plot'],'title': meta['title'],'writer': meta['writer'],'cover_url': meta['cover_url'],
        'director': meta['director'],'backdrop_url': meta['backdrop_url'],'imdb_id': meta['imdb_id']}
                
        return infoLabels
                



def OPEN_URL(url, proxy='',contentType='', timeout='60',header=''):
    # define function using cache, metacache, no cache, or auto
    #       in settings.metacache or pass in with the function call
    #       default is auto
    # default page expiration is 2 hours unless overridden by expires on page
    #      or settings.metaExpires thumbs expires are set seperatly to 3 days
    #  needs a clear cache, clear page, thumbs, ect. in the main code
    #  to do this delete the metafile and/or thumbs and send it back into the page call

    import hashlib,string,md5,xbmc
    

    
    
    datapaths = xbmc.translatePath(selfAddon.getAddonInfo('profile'))
    Cachepathhd=os.path.join(datapaths,'Cache/hostdata')
    Cachepathim=os.path.join(datapaths,'Cache/images')
    Cachepathpl=os.path.join(datapaths,'Cache/playlists')

    images = ['.png', '.jpg', '.jpeg', '.bmp', '.gif', '.psx']
    playlists = ['.txt', '.plx', '.xml']
    hostdata = ['.test' ]

    contentType = ''
    contentDir = ''
    metadata = { 'expires':'0' }

    myproxy = settings.getSetting('cache_proxy')
    #print "MY PROXY SETTING IS  =" +myproxy
    if myproxy == "0":
            proxy = "cache"
    if myproxy == "1":
            proxy = "metacache"   # if set, get value from addon settings
    #print "PROXY IS  = "+ proxy
    expires = settings.getSetting('cache_expires')
    #print "EXPIRES IS  = "+ expires

    debug = False
    if debug: print '\t\t\t\t\t url= ' +str(url),'\t\t\t\t\t proxy= ' + str(proxy), '\t\t\t\t\t timeout= ' + str(timeout), '\t\t\t\t\t header= '+ str(header)

    # get extension of url
    ext = url[-4:]
    ext = ext.lower()

    # set proxy, contentType, and cache directories according to extension
    if proxy == '': proxy = 'auto'
    #if ext in hostdata:
    if ext == '.test' :
        if contentType == '':
            contentType = 'hostdata'
        contentDir = Cachepathhd
        try: os.makedirs(Cachepathhd)
        except: pass
        if proxy == 'auto':
            proxy = 'cache'
    #elif ext in playlists:
    elif ext == '.txt' or ext == '.plx' or ext == '.xml' :
        if contentType == '':
            contentType = 'playlist'
        contentDir = Cachepathpl
        try: os.makedirs(Cachepathpl)
        except: pass
        if proxy == 'auto':
            proxy = 'metacache'
    #elif ext in images:
    elif ext == '.png' or ext == '.jpg' or ext == '.jpeg' or ext == '.bmp' or ext == '.gif' or ext == '.psx':
        if contentType == '':
            contentType = 'image'
        contentDir = Cachepathim
        try: os.makedirs(Cachepathim)
        except: pass
        if proxy == 'auto':
            proxy = 'cache'
        if proxy == 'metacache':
            expires = 259200  # 3 days in seconds
    else:
        proxy = 'nocache'
    if debug: print '\t\t\t\t\t extension = ' + str(ext), '\t\t\t\t\t contentType = ' + str(contentType), '\t\t\t\t\t contentDir = ' + str(contentDir)

    # start caching proccess
    if proxy != 'nocache':
        # get hashtag of url
        hashtag = md5.new(url).hexdigest()

        localCachedDir = contentDir
        localCacheFile = localCachedDir+'/'+contentType+ hashtag + ext
        if debug: print '\t\t\t\t\t localCacheFile = ' + str(localCacheFile)

        # see if localCacheFile exists
        if os.path.exists(localCacheFile):
            if ext != '':
                localCacheFile = os.path.join(localCachedDir, (contentType + hashtag + ext))
            else:
                localCacheFile = os.path.join(localCachedDir, (contentType + hashtag))

            # if using metacache
            if proxy == 'metacache':
                # read metadata
                if os.path.exists(localCacheFile + '.meta'):
                    try:
                        f = open(localCacheFile + '.meta','r')
                        metafile = f.readlines()
                        f.close()
                        for line in metafile:
                            key,value = line.strip().split("=")
                            metadata[key.strip()] = value
                            if debug: print '\t\t\t\t\t It read the metafile'

                        # check expiration and return data if not expired
                        if metadata['expires'] != '0':
                            expires = int(metadata['expires'])
                            creationtime = os.path.getmtime(localCacheFile)
                            currenttime = time.time()
                            deltatime = currenttime - creationtime
                            if debug: print '\t\t\t\t\t It got deltatime ' + str(deltatime)
                            if deltatime < expires:
                                try:
                                    f = open(localCacheFile,'r')
                                    link = f.read()
                                    f.close()
                                    if debug: print '\t\t\t\t\t Its returning the unexpired page ' + str(localCacheFile)
                                    return link
                                except Exception.e:
                                    print 'ERROR could not read the file' + str(e)
                            if debug: print '\t\t\t\t\t page has expired going to server'
                    except Exception,e:
                        print 'ERROR could not read metafile' + str(e)

    # query the server to get the data or error
    try:
        req = urllib2.Request(url)
        if header != '':
            req.add_header(header)  # allow for custom headers
        else:
            req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req,None,timeout=60)
    except Exception,e:
        print '\t\t\t\t\t ERROR server call' +str(e)
        response = -1
        link = response

    #return data or return error if server down for no caching
    if proxy == 'nocache':
        try:
            if debug: print '\t\t\t\t\t Its returning page or error'
            link = response.read()
        except Exception,e:
            print 'ERROR server cannot connect nocache ' + str(e)
        return link

    #if metacache or cache and server down return cached data
    if response == -1:
        try:
            if debug: print '\t\t\t\t\t It got a server error'
            f=open(localCacheFile, 'r')
            link = f.read()
        except Exception,e:
            print  'ERROR server cannot connect cache ' + str(e)
            link=''
        return link

    #rename LocalCachefile to localCacheFile + '.old'
    if os.path.exists(localCacheFile):
         os.rename(localCacheFile,localCacheFile + ".old")

    #write new data to disk location based on contentType
    link = response.read()
    f=open(localCacheFile,'wb')
    f.write(link)
    f.close()
    response.close()

    #delete localCacheFile.old if it exists
    if os.path.exists(localCacheFile + '.old'):
        os.remove(localCacheFile + '.old')

    #get or create expiration time
    if proxy == 'metacache':
        try:
            lineCount = 0
            with open(localCacheFile,'r') as data:
                for line in data:
                    if line and line[0] != '#':
                        index=line.find('=')
                        if index!= -1:
                            key=line[:index]
                            value=line[index+1:]
                            if key=='expires':
                                expires=((int(value) * 60) * 60)  # convert hour value on page into seconds
                                if debug: print 'expirationt time from page ' + str(expires)
                                break
                            elif key=='type':
                                break
                    if lineCount >= 10:  # only read the first 10 lines
                        break
                    lineCount += 1
            data.close()
        except Exception,e:
            print 'ERROR expiration setting default time '+str(e)
        if debug: print '\t\t\t\t\t expirationt time is set for ' + str(expires)

        #build metadata file if metacaching
        if proxy == 'metacache':
            metadata["expires"] = str(expires)
            try:
                f = open(localCacheFile + '.meta','w')
                for line in metadata:
                    f.write(line + '=' + metadata[line] + '\n')
                f.close()
            except Exception,e:
                print 'could not write to metadata file' + str(e)
    if debug: print '\t\t\t\t\t metacache function complete. returning page'
    return link

#END CACHE SESSION==================



# Global Stuff
settings = xbmcaddon.Addon(id=addon_id)


#Add Directory Stuff
def removeColorTags(text):
    return re.sub('\[COLOR[^\]]{,15}\]','',text.replace("[/COLOR]", ""),re.I|re.DOTALL).strip()
    
def removeColoredText(text):
    return re.sub('\[COLOR.*?\[/COLOR\]','',text,re.I|re.DOTALL).strip()
     
# Standard addDir
def addDir(name,url,mode,thumb,fanart,labels,favtype,sound):
        params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb,  'dlfoldername':dlfoldername, 'mainimg':mainimg}
        contextMenuItems = []
        gomode=mode
       
        sitethumb = thumb
        sitename = name
        #fanart = fanart
        #print "LABELS ARE = "+ str(labels)
        try:
                name = data['title']
                thumb = data['cover_url']
                fanart = data['backdrop_url']
        except:
                name = sitename
                
        if thumb == '':
                thumb = sitethumb       
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&sound="+urllib.quote_plus(sound)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumb)
        liz.setInfo( type="Video", infoLabels=labels )
        if favtype == 'movie':
                contextMenuItems.append(('[COLOR gold]Movie Information[/COLOR]', 'XBMC.Action(Info)'))
        elif favtype == 'tvshow':
                contextMenuItems.append(('[COLOR gold]TV Show  Information[/COLOR]', 'XBMC.Action(Info)'))
        elif favtype == 'episode':
                contextMenuItems.append(('[COLOR gold]Episode  Information[/COLOR]', 'XBMC.Action(Info)'))       
                
        liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        try:
             liz.setProperty( "Fanart_Image", labels['backdrop_url'] )
        except:
             liz.setProperty( "Fanart_Image", fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok



#******************For Movie Download*********************************
def addDLDir2(name,url,mode,thumb,fanart,sound,dlfolder,labels):
        sitethumb = thumb
        sitename = name
        fanart = fanart
        contextMenuItems = []
        params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb, 'dlfoldername':dlfoldername, 'favtype':favtype, 'mainimg':mainimg}
        try:
                name = data['title']
                thumb = data['cover_url']
                fanart = data['backdrop_url']
        except:
                name = sitename
                thumb = sitethumb
                
        if thumb == '':
                thumb = sitethumb  
        contextMenuItems.append(('[COLOR gold]Meta Information[/COLOR]', 'XBMC.Action(Info)'))
        
        contextMenuItems.append(('[COLOR gold]Search for Trailer[/COLOR]','XBMC.RunPlugin(%s)'% addon.build_plugin_url({ 'mode':'trailersearch','name':name, 'url':url})))
        
        contextMenuItems.append(('[COLOR gold]Download This File[/COLOR]', 'XBMC.RunPlugin(%s)' % addon.build_plugin_url({'url':url, 'mode':'dlvidpage', 'name':name, 'thumb':thumb, 'console':console, 'dlfoldername':dlfoldername,'favtype':favtype})))
        addon.add_directory(params, {'title':name}, contextmenu_items=contextMenuItems, img= thumb)                             
       





def addDLDir(name,url,mode,thumb,fanart,sound,dlfolder,labels, isFolder=True, isPlayable=False):
      
        contextMenuItems = []
        sitethumb = thumb
        sitename = name
        fanart = fanart
        #print "DL THUMBS ARE  = "+ thumb
        try:
                name = data['title']
                thumb = data['cover_url']
                fanart = data['backdrop_url']
        except:
                name = sitename
                thumb = sitethumb
                
        if thumb == '':
                thumb = sitethumb
        params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb}        
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&sound="+urllib.quote_plus(sound)+"&thumb="+urllib.quote_plus(thumb)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumb)
        liz.setInfo( type="Video", infoLabels=labels )
        #if favtype == 'movie':
        contextMenuItems.append(('[COLOR gold]Meta Information[/COLOR]', 'XBMC.Action(Info)'))
        
        contextMenuItems.append(('[COLOR gold]Search for Trailer[/COLOR]','XBMC.RunPlugin(%s)'% addon.build_plugin_url({ 'mode':'trailersearch','name':name, 'url':url})))
        
        contextMenuItems.append(('[COLOR gold]Download This File[/COLOR]', 'XBMC.RunPlugin(%s)' % addon.build_plugin_url({'url':url, 'mode':'dlvidpage', 'name':name, 'thumb':thumb, 'console':console, 'dlfoldername':dlfoldername,'favtype':favtype})))
        if favtype == 'tvshow':
                contextMenuItems.append(('[COLOR gold]TV Show  Information[/COLOR]', 'XBMC.Action(Info)'))
        elif favtype == 'episode':
                contextMenuItems.append(('[COLOR gold]Episode  Information[/COLOR]', 'XBMC.Action(Info)'))       
                
        liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        try:
             liz.setProperty( "Fanart_Image", labels['backdrop_url'] )
        except:
             liz.setProperty( "Fanart_Image", fanart )


        if isPlayable:
            liz.setProperty("IsPlayable","true")
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=isFolder)
        return ok
        #ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        #return ok



#contextMenuItems.append(('[COLOR gold]Download This File[/COLOR]', 'XBMC.RunPlugin(%s)' % addon.build_plugin_url({'url':url, 'mode':'dlvidpage', 'name':name, 'thumb':mainimg, 'console':console, 'dlfoldername':dlfoldername,'favtype':favtype})))
#Resolve Functions
     
def RESOLVE(name,url,iconimage):
         url = urlresolver.HostedMediaFile(url=url).resolve()
         ok=True
         liz=xbmcgui.ListItem(name, iconImage=iconimage,thumbnailImage=iconimage); liz.setInfo( type="Video", infoLabels={ "Title": name } )
         ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=str(url),listitem=liz)
         xbmc.sleep(1000)
         xbmc.Player ().play(str(url), liz, False)

         AUTO_VIEW('')

#Resolve 2

    

def RESOLVE2(name,url,thumb):
         
    
     data=0
    
     url = urlresolver.resolve(url)
          
     params = {'url':url, 'name':name, 'thumb':thumb}
     if data == 0:
          addon.add_video_item(params, {'title':name}, img=thumb)
          liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumb)

     else:
          addon.add_video_item(params, {'title':name}, img=data['cover_url'])
          liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=data['cover_url'])
          liz.setInfo('video',infoLabels=data)

     xbmc.sleep(1000)
        
     xbmc.Player ().play(url, liz, False)

     

#AutoView
def AUTO_VIEW(content):
        if content:
                xbmcplugin.setContent(int(sys.argv[1]), content)
                if settings.getSetting('auto-view') == 'true':
                        
                        
        
                   xbmc.executebuiltin("Container.SetViewMode(%s)" % settings.getSetting('default-view') )

        


     

#Returns the host thumbnail so that you can pass it as and argument 
def GETHOSTTHUMB(host):
     if host.endswith('.com'):
          host = host[:-4]
     if host.endswith('.org'):
          host = host[:-4]
     if host.endswith('.eu'):
          host = host[:-3]
     if host.endswith('.ch'):
          host = host[:-3]
     if host.endswith('.in'):
          host = host[:-3]
     if host.endswith('.es'):
          host = host[:-3]
     if host.endswith('.tv'):
          host = host[:-3]
     if host.endswith('.net'):
          host = host[:-4]
     if host.endswith('.me'):
          host = host[:-3]
     if host.endswith('.ws'):
          host = host[:-3]
     if host.endswith('.sx'):
          host = host[:-3]
     if host.startswith('www.'):
             host = host[4:]
     
     if settings.getSetting('theme') == '0':
             host = 'https://raw.githubusercontent.com/Blazetamer/commoncore/master/xbmchub/moviedb/showgunart/images/hosts/' + host +'.png'
     else:
             host = 'https://raw.githubusercontent.com/Blazetamer/commoncore/master/xbmchub/moviedb/showgunart/images/hosts/' + host +'.jpg'
     return(host)

#========================Returns Hostname For Directory ======================
def GETHOSTNAME(host):
     if host.endswith('.com'):
          host = host[:-4]
     if host.endswith('.org'):
          host = host[:-4]
     if host.endswith('.eu'):
          host = host[:-3]
     if host.endswith('.ch'):
          host = host[:-3]
     if host.endswith('.in'):
          host = host[:-3]
     if host.endswith('.es'):
          host = host[:-3]
     if host.endswith('.tv'):
          host = host[:-3]
     if host.endswith('.net'):
          host = host[:-4]
     if host.endswith('.me'):
          host = host[:-3]
     if host.endswith('.ws'):
          host = host[:-3]
     if host.endswith('.sx'):
          host = host[:-3]
     if host.startswith('www.'):
             host = host[4:]
     hostname=' '+host+'' 
     
     return(hostname)



def LIVERESOLVE(name,url,iconimage):
         url = str(url)            
         liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
 
         liz.setInfo( type="Video", infoLabels={ "Title": name} )
         liz.setPath(url)

         xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
         

#====================Standard Favorites===================================



def doRegex(murl):
    #rname=rname.replace('><','').replace('>','').replace('<','')
    import urllib2
    url=re.compile('([^<]+)<regex>',re.DOTALL).findall(murl)[0]
    doRegexs = re.compile('\$doregex\[([^\]]*)\]').findall(url)
    for k in doRegexs:
        if k in murl:
            regex=re.compile('<name>'+k+'</name><expres>(.+?)</expres><page>(.+?)</page><referer>(.+?)</referer></regex>',re.DOTALL).search(murl)
            referer=regex.group(3)
            if referer=='':
                referer=regex.group(2)
            req = urllib2.Request(regex.group(2))
            req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:10.0a1) Gecko/20111029 Firefox/10.0a1')
            req.add_header('Referer',referer)
            response = urllib2.urlopen(req)
            link=response.read()
            response.close()
            link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\/','/')
            r=re.compile(regex.group(1),re.DOTALL).findall(link)[0]
            url = url.replace("$doregex[" + k + "]", r)
   
    return url

def getRegexParsed(regexs, url):
        #regexs = eval(urllib.unquote(regexs))
        cachedPages = {}
        doRegexs = re.compile('\$doregex\[([^\]]*)\]').findall(url)
        for k in doRegexs:
            if k in regexs:
                m = regexs[k]
                if m['page'] in cachedPages:
                    link = cachedPages[m['page']]
                else:
                    addon_log('get regexs: %s' %m['page'])
                    req = urllib2.Request(m['page'])
                    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:14.0) Gecko/20100101 Firefox/14.0.1')
                    if 'refer' in m:
                        req.add_header('Referer', m['refer'])
                    if 'agent' in m:
                        req.add_header('User-agent', m['agent'])
                    if 'data' in m:
                        req.add_data(m['data'])
                    if m.has_key('function') and m['function'] == 'NoRedirection':
                        addon_log('regex function NoRedirection')
                        opener = urllib2.build_opener(NoRedirection)
                        urllib2.install_opener(opener)
                        link = urllib2.urlopen(req)
                    else:
                        response = urllib2.urlopen(req)
                        link = response.read()
                        response.close()
                    cachedPages[m['page']] = link
                reg = re.compile(m['expre']).search(link)
                data = reg.group(1).strip()
                if m.has_key('function') and m['function'] == 'unquote':
                    data = urllib.unquote(data)
                    addon_log('Reg urllib.unquote(data): %s' %data)
                addon_log('Reg data: %s' %data)
                url = url.replace("$doregex[" + k + "]", data)
        item = xbmcgui.ListItem(path=url)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)

        

def addLink(name,url,iconimage):
    liz=xbmcgui.ListItem(name, iconImage=art+'/link.png', thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    liz.setProperty('fanart_image', fanart)
    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)

def downloadFile(url,dest,silent = False,cookie = None):
    try:
        import urllib2
        file_name = url.split('/')[-1]
        print "Downloading: %s" % (file_name)
        if cookie:
            import cookielib
            cookie_file = os.path.join(os.path.join(datapath,'Cookies'), cookie+'.cookies')
            cj = cookielib.LWPCookieJar()
            if os.path.exists(cookie_file):
                try: cj.load(cookie_file,True)
                except: cj.save(cookie_file,True)
            else: cj.save(cookie_file,True)
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        else:
            opener = urllib2.build_opener()
        opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')]
        u = opener.open(url)
        f = open(dest, 'wb')
        meta = u.info()
        if meta.getheaders("Content-Length"):
            file_size = int(meta.getheaders("Content-Length")[0])
        else: file_size = 'Unknown'
        file_size_dl = 0
        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer: break
            file_size_dl += len(buffer)
            f.write(buffer)
        print "Downloaded: %s %s Bytes" % (file_name, file_size)
        f.close()
        return True
    except Exception:
        print 'Error downloading file ' + url.split('/')[-1]
        #ErrorReport(e)
        if not silent:
            dialog = xbmcgui.Dialog()
            dialog.ok("Phoenix Streams", "Report any errors  at " + supportsite,  "We will try our best to help you")
        return False

def AUTO_VIEW(content):
        if content:
                xbmcplugin.setContent(int(sys.argv[1]), content)
                if settings.getSetting('auto-view') == 'true':
                        
                        if content == 'menu':
                                xbmc.executebuiltin("Container.SetViewMode(%s)" % settings.getSetting('default-view') )
                        
                                
                else:
                        xbmc.executebuiltin("Container.SetViewMode(%s)" % settings.getSetting('default-view') )

        



#MYDOWNLOADS CLASS=============\


#NEW DL FUNCTION CRZEN


############## Start DownloadThread Class ################
class downloadThread (threading.Thread):
    def __init__(self, name, url, thumb, console, ext):
        threading.Thread.__init__(self)
        self.thumb = thumb
        self.kill = False
        #self.kill = threading.Event()
        basename = 'TEST NAME'
    def kill(self):
        self.kill = True
        
    def stop(self):
        print ('killing queue ') + str(self.kill)
        self.kill = True
        print ('killing queue ') + str(self.kill)
        
#NEW INFO Q==============

    def addInfoQueue(self,file_name,percent,dlspeed,file_thumb,file_total_size):

             infoqueue = cache.get('infoqueue')
             infoqueue_items = []
             if infoqueue:
                  cache.delete('infoqueue')   
                  
             infoqueue_items.append((file_name,percent,dlspeed,file_thumb,file_total_size))         
             cache.set('infoqueue', str(infoqueue_items))
             #addon.show_small_popup(title='[COLOR gold]Item Added To Your Queue [/COLOR]', msg=name + ' Was Added To Your Download Queue', delay=int(5000), image=thumb)
            

    def run(self):
        queue = cache.get('queue')
        if queue:
            queue_items = sorted(eval(queue), key=lambda item: item[1])
            for item in queue_items:
                self.name = item[0]
                self.url = item[1]
                self.ext = item[3]
                self.console = item[4]
                thumb = item[2]
                #global file_name
                #basename = 'TEST NAME'
                

                #print queue_items               
                self.path = download_path + self.console
                if not os.path.exists(self.path):
                    os.makedirs(self.path)

                self.file_name = self.name + self.ext

                
                addon.show_small_popup(title='[COLOR gold]Downloads Started[/COLOR]', msg=self.name + ' Is Downloading', delay=int(7000), image=thumb)
                u = urllib2.urlopen(self.url)
                meta = u.info()
                #print meta
                if 'Content-Length' not in meta:
                    file_size_string = 'Unknown'
                    file_size = 1  #
                else:
                    file_size_string = ''
                    file_size =  int(meta.getheaders("Content-Length")[0])
                    #print file_size
                f = open(os.path.join(self.path,self.file_name), 'ab')                    
                existSize = os.path.getsize(os.path.join(self.path,self.file_name))
                if file_size_string != 'Unknown':
                    # only download the remaining bytes using byte range
                    #for RangeEntry in 'Ranges','Range','':
                    for RangeEntry in 'Ranges','Range','':        
                        headers = u.info()
                        if RangeEntry != '':
                            #print "TRYING BYTE SIZES"    
                            try:
                                
                                # this request sets the pointer to where you want to start
                                req = urllib2.Request(self.url)
                                # reopen url with preset byte range in header
                                req.headers["Range"] = 'bytes=%s-' %existSize
                                u = urllib2.urlopen(req)
                                # Set the begining write point
                                file_size_dl = existSize
                                break
                            except Exception, e:
                                file_size_dl = 0
                                print '\t\t error byte range not supported ' + str(e)  # Expected error: HTTP Error 416: Requested Range Not Satisfiable'
                else:
                    print ('\t\t\t Remote file size is unknown')
                    file_size_dl = 0  # byte range not supported continue as usual
                    
                # Number of bytes to read at a time
                block_sz = 500 * 1024

                # Download init
                starttime = time.time()
                startSize = file_size_dl
                
                
                while (file_size_string == 'Unknown' or (existSize <= file_size and file_size >= 1)) \
                          and queue and not self.kill:
                        #print ('\t\t\t checking kill ') + str(self.kill)
                        # keep from adding empty bytes after end of file
                        if (existSize + block_sz) > file_size and file_size > 1:
                            block_sz = file_size - existSize  # only read the remainder
                        buffer = u.read(block_sz)
                        if buffer == '':  # end of file
                            break
                        # dont overwrite existing data
                        if file_size_dl >= existSize:
                                f.write(buffer)
                        file_size_dl += block_sz 
                        
                        try:  # calculate the percentage downloaded                        
                            deltatime = time.time() - starttime
                            if file_size <= 1 or file_size_string == 'Unknown' :
                                if deltatime >= 150:  # in seconds. update display every 2.5 min
                                    addon.show_small_popup(title=self.name, msg='Downloading...',delay=int(10), image=thumb)
                            else:
                                    percent = file_size_dl * 100 / file_size
                                #if percent in range(10,101,10):
                                                        
                                    #Actual size info
                                    totalsize = file_size /1000000
                                    if totalsize < 1000:
                                        full_size = str(totalsize) +"MB"
                                    else  :
                                         totalgbsize = totalsize /float(1000)
                                         full_size =str(totalgbsize) +"GB"
                                    truesize = file_size_dl /1000000
                                    if truesize < 1000:
                                        dl_size = str(truesize) +"MB"
                                    else  :
                                         truegbsize = truesize /float(1000)
                                         dl_size =str(truegbsize) +"GB"
                                    #Actual Size Info
                                       
                                         
                                    #addon.show_small_popup(title=self.name, msg= str(percent) + '% Complete of '+ full_size,delay=int(10),image='http://mecca.watchkodi.com/images/phoenix_icon.png')


                                    #calculate the download speed
                                    deltasize = file_size_dl - startSize
                                    dlspeed = (deltasize / 1024) / deltatime                        

                                    starttime = time.time()
                                    startSize = file_size_dl
                                    #print ('\t\t\t Download Speed= ' + str(dlspeed) + ' kbs')
                                    #START INFO Q APPEND==========
                                    
                                    self.addInfoQueue(self.name,percent,dlspeed,thumb,full_size)   
                        except Exception,e:
                           print('\t\t\t ERROR DISPLAY ' + str(e))
                        

                try:
                    addon.show_small_popup(title='[COLOR gold]Download Complete[/COLOR]', msg=self.name + ' Completed', delay=int(5000), image='http://mecca.watchkodi.com/images/phoenix_icon.png')

                except:
                    addon.show_small_popup(title='Error', msg=self.name + ' Failed To Download File', delay=int(5000), image=thumb)
                    print 'ERROR - File Failed To Download'
                   
                f.close()
                
                cache.delete('infoqueue')
                removeFromQueue(self.name,self.url,thumb,self.ext,self.console)
                 
                addon.show_small_popup(title='[COLOR gold]Process Complete[/COLOR]', msg=self.name + ' is in your downloads folder', delay=int(5000), image='http://mecca.watchkodi.com/images/phoenix_icon.png')



                

#END CRZEN DL FUNCTION

def KILLQ():
        window = MyDownloads('Download Status/Information')
        window.doModal()
        # Destroy the instance explicitly because
        # underlying xbmcgui classes are not garbage-collected on exit.
        del window
        

def addDirpop(name,url,mode,thumb,fanart,sound):
        fanart = fanart
        params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb, 'fanart':fanart, 'sound':sound}        
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&fanart="+urllib.quote_plus(fanart)+"&sound="+urllib.quote_plus(sound)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumb)
        liz.setInfo( type="Video", infoLabels={ "title": name, "Plot": ''} )
        liz.setProperty( "Fanart_Image", fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok


def addQDir(name,url,mode,thumb,console):
     contextMenuItems = []

     params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb,'console':console, 'ext':ext}

     contextMenuItems.append(('[COLOR red]Remove From Queue[/COLOR]', 'XBMC.RunPlugin(%s)' % addon.build_plugin_url({'mode': 'removeFromQueue', 'name': name,'url': url,'thumb': thumb,'ext': ext,'console': console})))

     addon.add_directory(params, {'title':name}, contextmenu_items=contextMenuItems, img= thumb)
     
def addToQueue(name,url,thumb,ext,console):
     queue = cache.get('queue')
     queue_items = []
     if queue:
          queue_items = eval(queue)
          if queue_items:
               if thumb == "": thumb =mainicon   
               if (name,url,thumb,ext,console) in queue_items:
                    addon.show_small_popup(title='[COLOR red]Item Already In Your Queue[/COLOR]', msg=name + ' Is Already In Your Download Queue', delay=int(5000), image=thumb)
                    return
     queue_items.append((name,url,thumb,ext,console))         
     cache.set('queue', str(queue_items))
     addon.show_small_popup(title='[COLOR gold]Item Added To Your Queue [/COLOR]', msg=name + ' Was Added To Your Download Queue', delay=int(5000), image=thumb)

def viewQueue():
     addDir('[COLOR blue]Start Downloads[/COLOR]','none','download',artwork +'downloadsstart.jpg','','','','')
     #addDir('[COLOR red]Download Status[/COLOR]','none','killq',artwork +'downloadsstop.jpg','','','','')
     queue = cache.get('queue')
     if queue:
          queue_items = sorted(eval(queue), key=lambda item: item[1])
          print queue_items
          for item in queue_items:
               addQDir(item[0],item[1],'viewQueue',item[2],item[4])
     infoqueue = cache.get('infoqueue')
     if infoqueue:   
               addDir('[COLOR gold]Download Status[/COLOR]','none','killq',artwork +'downloadsstop.jpg','','','','') 


def KILLSLEEP(self):
     queue = cache.get('queue')
     if queue:
          queue_items = sorted(eval(queue), key=lambda item: item[1])
          for item in queue_items:
               self.name = item[0]
               self.url = item[1]
               self.ext = item[3]
               self.console = item[4]
               self.thumb = item[2]

               time.sleep(3)
     removeFromQueue(self.name,self.url,self.thumb,self.ext,self.console)
     
     
          
def removeFromQueue(name,url,thumb,ext,console):
     queue = cache.get('queue')
     if queue:
          queue_items = sorted(eval(queue), key=lambda item: item[1])
          #print queue_items
          try:
               queue_items.remove((name,url,thumb,'.mp4',console))
          except:
               try:
                    queue_items.remove((name,url,thumb,'.flv',console))
               except:
                  try:     
                    queue_items.remove((name,url,thumb,'.avi',console))
                  except:
                       try:   
                          queue_items.remove((name,url,thumb,'.mkv',console))
                       except:
                            try:   
                                 queue_items.remove((name,url,thumb,'',console))
                            except:

                                 try:   
                                    queue_items.remove((name,url,thumb,'.mpg',console))
                                 except:   
                                    addon.show_small_popup(title='Can not remove from Queue', msg='You need to remove file manually ', delay=int(5000), image='http://mecca.watchkodi.com/images/phoenix_icon.png')
                    
          cache.set('queue', str(queue_items))
          xbmc.executebuiltin("XBMC.Container.Refresh")
          

def download():
     download_path = settings.getSetting('download_folder')
     if download_path == '':
          addon.show_small_popup(title='File Not Downloadable', msg='You need to set your download folder in addon settings first', delay=int(5000), image='http://mecca.watchkodi.com/images/phoenix_icon.png')
     else:
        queue = cache.get('queue')
        if queue:
          queue_items = sorted(eval(queue), key=lambda item: item[1])
          print queue_items
          for item in queue_items:
                     
                
                dlThread = downloadThread(item[0], item[1], item[2], item[4], item[3])
                dlThread.start() 
                   

#=============END DLFUNCTION======================================================================================================================
     
#******************For Download*********************************

    
#Resolve Movie DL Links******************************************
def RESOLVEDL(name,url,thumb):  
        data=0
        try:
          data = GRABMETA(movie_name,year)
        except:
          data=0
          import resolvers
          url = resolvers.resolve_url(url)
          #vipplaylist.liveresolver(name,url,thumb)
          ext = ''
          if '.mp4' in url:
                    ext = '.mp4'
          elif '.flv' in url:
                    ext = '.flv'
          elif '.avi' in url:
                    ext = '.avi'

          elif '.mkv' in url:
                    ext = '.mkv'
                    
          elif '.mpg' in url:
                    ext = '.mpg'
                    
        console = 'Phoenix/'+ dlfoldername
        params = {'url':url, 'name':name, 'thumb':thumb, 'dlfoldername':dlfoldername} 


        xbmc.sleep(1000)

        addToQueue(name,url,thumb,ext,console)

def SPECIALDL(name,url,thumb):
        data=0
        try:
          data = GRABMETA(movie_name,year)
        except:
           data=0
        hmf = urlresolver.HostedMediaFile(url)
        host = ''
        if hmf:
          url = urlresolver.resolve(url)
          host = hmf.get_host()
          ext = ''
          if '.mp4' in url:
                    ext = '.mp4'
          elif '.flv' in url:
                    ext = '.flv'
          elif '.avi' in url:
                    ext = '.avi'
                    
          elif '.mkv' in url:
                    ext = '.mkv'          
          
          
          console = 'Downloads/Specials/'+ dlfoldername
          params = {'url':url, 'name':name, 'thumb':thumb, 'dlfoldername':dlfoldername} 


          xbmc.sleep(1000)

          addToQueue(name,url,thumb,ext,console)         

def addPlayc(name,url,mode,iconimage,plot,fanart,dur,genre,year):
    return addDirX(name,url,mode,iconimage,plot,fanart,dur,genre,year,isFolder=0,addToFavs=0)


def addDirX(name,url,mode,iconimage,plot='',fanart='',dur=0,genre='',year='',imdb='',tmdb='',isFolder=True,searchMeta=False,addToFavs=True,
            id=None,fav_t='',fav_addon_t='',fav_sub_t='',metaType='Movies',menuItemPos=None,menuItems=None,down=False,replaceItems=True):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&plot="+urllib.quote_plus(plot)+"&fanart="+urllib.quote_plus(fanart)+"&genre="+urllib.quote_plus(genre)
    Commands = []
    liz=xbmcgui.ListItem(name, iconImage=art+'/vidicon.png', thumbnailImage=iconimage)
    liz.addContextMenuItems( Commands, replaceItems=False)
    if searchMeta:
        liz.setInfo( type="Video", infoLabels=infoLabels )
    liz.setProperty('fanart_image', fanart)
    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=isFolder)



def trailer(tmdbid):
    if tmdbid == '':
        addon.show_small_popup(title='OOPPS..', msg='Sorry!,No Trailer Available',delay=int(10), image='http://mecca.watchkodi.com/images/phoenix_icon.png')
    else:
        import urllib2
        xbmc.executebuiltin("XBMC.Notification(Please Wait!,Searching for Trailer,1500)")
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:10.0a1) Gecko/20111029 Firefox/10.0a1'
        request= 'http://api.themoviedb.org/3/movie/' + tmdbid + '/trailers?api_key=d5da2b7895972fffa2774ff23f40a92f'
        txheaders= {'Accept': 'application/json','User-Agent':user_agent}
        req = urllib2.Request(request,None,txheaders)
        response=urllib2.urlopen(req).read()
        if re.search('"size":"HD"',response):
            quality=re.compile('"size":"HD","source":"(.+?)"').findall(response)[0]
            youtube='http://www.youtube.com/watch?v=' + quality
            stream_url= "plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid="+quality+"&hd=1"
            xbmc.Player().play(stream_url)
        elif re.search('"size":"HQ"',response):
            quality=re.compile('"size":"HQ","source":"(.+?)"').findall(response)[0]
            youtube='http://www.youtube.com/watch?v=' + quality
            stream_url= "plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid="+quality+"&hd=1"
            xbmc.Player().play(stream_url)
        elif re.search('"size":"Standard"',response):
            quality=re.compile('"size":"Standard","source":"(.+?)"').findall(response)[0]
            youtube='http://www.youtube.com/watch?v=' + quality
            stream_url= "plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid="+quality+"&hd=1"
            xbmc.Player().play(stream_url)
        else:
           
            addon.show_small_popup(title='OOPPS..', msg='Sorry!,No Trailer Available',delay=int(10), image='http://mecca.watchkodi.com/images/phoenix_icon.png')    
def TRAILERSEARCH(url, name, imdb=''):
    
    addon.show_small_popup(title='Please Wait..', msg='Getting Trailers',delay=int(10), image='http://mecca.watchkodi.com/images/phoenix_icon.png')
    #name = re.split(':\s\[',name)
    search      = name
    #setGrab()
    #infoLabels = grab._cache_lookup_by_name('movie', search.strip(), year='')
    #print infoLabels
    res_name    = []
    res_url     = []
    res_name.append('[COLOR gold][B]Cancel & Return[/B][/COLOR]')
    
    site = ' site:http://www.youtube.com '
    results = SearchGoogle(search+' official trailer', site)
    for res in results:
        if res.url.encode('utf8').startswith('http://www.youtube.com/watch'):
            res_name.append(res.title.encode('utf8'))
            res_url.append(res.url.encode('utf8'))
    results = SearchGoogle(search[:(len(search)-7)]+' official trailer', site)
    
    for res in results:
        if res.url.encode('utf8').startswith('http://www.youtube.com/watch') and res.url.encode('utf8') not in res_url:
            res_name.append(res.title.encode('utf8'))
            res_url.append(res.url.encode('utf8'))
            
    dialog = xbmcgui.Dialog()
    ret = dialog.select(search + ' trailer search',res_name)

    if ret == 0:
        return
    elif ret >= 1:
        trailer_url = res_url[ret - 0]
        try:
            xbmc.executebuiltin(
                "PlayMedia(plugin://plugin.video.youtube/?action=play_video&videoid=%s)" 
                % str(trailer_url)[str(trailer_url).rfind("v=")+2:] )
            if re.findall('Darwin iOS',PLATFORM):
                grab.update_trailer('movie', imdb, trailer_url)
                xbmc.executebuiltin("XBMC.Container.Refresh")

        except:
            return    


def SearchGoogle(search, site):
    from searchit.search import GoogleSearch
    gs = GoogleSearch(''+search+' '+site)
    gs.results_per_page = 25
    gs.page = 0
    try:
        results = gs.get_results()
    except Exception, e:
        print '***** Error: %s' % e
        return None
    return results
#################



class MyDownloads(pyxbmct.AddonDialogWindow):

    def __init__(self, title='downloadThread'):
        super(MyDownloads, self).__init__(title)
        self.setGeometry(700, 450, 9, 3)
        self.set_info_controls()
        self.set_active_controls()
        #self.set_navigation()
        # Connect a key action (Backspace) to close the window.
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
        #self.connect(pyxbmct.ACTION_NAV_BACK, self.stop)
        #print "FILE NAME IS = "+file_name
        
    def set_info_controls(self):
        infoqueue = cache.get('infoqueue')
        #print "HERE IS THE INFO Q = "+infoqueue
        if infoqueue:
          infoqueue_items = sorted(eval(infoqueue), key=lambda item: item[1])
          #print infoqueue_items
          for item in infoqueue_items:
                     
                self.name = item[0]
                self.percent = item[1]
                self.thumb = item[3]
                self.totalsize = item[4]
                self.dlspeed = item[2]
                if self.thumb == '':
                        self.thumb ='http://mecca.watchkodi.com/images/phoenix_icon.png'
                #file_name = dlvars.basename
                file_name = self.name 
                percent = self.percent 
                file_thumb = self.thumb 
                file_total_size = self.totalsize 
                dlspeed = self.dlspeed 
        # Demo for PyXBMCt UI controls.
        no_int_label = pyxbmct.Label('[B][COLOR gold]'+file_name+'[/COLOR][/B]', alignment=pyxbmct.ALIGN_CENTER)
        self.placeControl(no_int_label, 0, 1, 1, 1)
        #
        label_label = pyxbmct.Label('Total File Size', alignment=pyxbmct.ALIGN_CENTER)
        self.placeControl(label_label, 1, 0)
        totalsize_label = pyxbmct.Label(file_total_size, alignment=pyxbmct.ALIGN_CENTER)
        self.placeControl(totalsize_label, 2, 0)
        # Label
        dld_label = pyxbmct.Label('Downloaded', alignment=pyxbmct.ALIGN_CENTER)
        self.placeControl(dld_label, 1, 1)
        dld_label = pyxbmct.Label(str(percent) +"%", alignment=pyxbmct.ALIGN_CENTER)
        self.placeControl(dld_label, 2, 1)
        #
        #
        dlSpeed_label = pyxbmct.Label('Download Speed', alignment=pyxbmct.ALIGN_CENTER)
        self.placeControl(dlSpeed_label, 1, 2)
        speed_label = pyxbmct.Label(str(dlspeed), alignment=pyxbmct.ALIGN_CENTER)
        self.placeControl(speed_label, 2, 2)
        # TextBox
        #
        #image_label = pyxbmct.Label('Cover Art>>')
        #self.placeControl(image_label, 5, 0)
        self.image = pyxbmct.Image(file_thumb)
        self.placeControl(self.image, 3, 1, 6, 1)
        

    def set_active_controls(self):
        '''int_label = pyxbmct.Label(file_name, alignment=pyxbmct.ALIGN_CENTER)
        self.placeControl(int_label, 0, 2, 1, 2)'''
        
        # Close Button
        self.button = pyxbmct.Button('Close')
        self.placeControl(self.button, 8, 2)
        # Connect control to close the window.
        self.connect(self.button, self.close)
        
        #Stop DL Button
        #self.button = pyxbmct.Button('Stop DL')
        #self.placeControl(self.button, 8, 0)
        # Connect control to stop the download.
        #self.connect(self.button, self.close)

    

    def radio_update(self):
        # Update radiobutton caption on toggle
        if self.radiobutton.isSelected():
            self.radiobutton.setLabel('On')
        else:
            self.radiobutton.setLabel('Off')

    def list_update(self):
        # Update list_item label when navigating through the list.
        try:
            if self.getFocus() == self.list:
                self.list_item_label.setLabel(self.list.getListItem(self.list.getSelectedPosition()).getLabel())
            else:
                self.list_item_label.setLabel('')
        except (RuntimeError, SystemError):
            pass

    def setAnimation(self, control):
        # Set fade animation for all add-on window controls
        control.setAnimations([('WindowOpen', 'effect=fade start=0 end=100 time=500',),
                                ('WindowClose', 'effect=fade start=100 end=0 time=500',)])


'''if __name__ == '__main__':
    window = MyDownloads('Download Status/Information')
    window.doModal()
    # Destroy the instance explicitly because
    # underlying xbmcgui classes are not garbage-collected on exit.
    del window'''
