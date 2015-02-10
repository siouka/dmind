#Custom vipplaylist by Blazetamer Ported from Mash
import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,urlresolver,xbmc,os,xbmcaddon,main,math,cookielib
from resources.modules import main,resolvers
import urlresolver
import hashlib,string,md5
from addon.common.addon import Addon
from addon.common.net import Net as net
#from addon.common.net import Net
addon_id = 'plugin.video.phstreams'
selfAddon = xbmcaddon.Addon(id=addon_id)
addon = Addon('plugin.video.phstreams', sys.argv)
ADDON = xbmcaddon.Addon(id='plugin.video.phstreams')
#net = Net(http_debug=True)
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
console = addon.queries.get('console', '')
dlfoldername = addon.queries.get('dlfoldername', '')
ext = addon.queries.get('ext', '')
data = addon.queries.get('data', '')
labels = addon.queries.get('labels', '')
mname= addon.queries.get('mname', '')
vip = addon.queries.get('vip', '')
mysort = addon.queries.get('mysort', '')
#======================== END Alternate Param Stuff=======================
datapaths = xbmc.translatePath(ADDON.getAddonInfo('profile'))
Cachepathpl=os.path.join(datapaths,'Cache/playlists/')

Cachepathim=os.path.join(datapaths,'Cache/images/')

Cachepathhd=os.path.join(datapaths,'Cache/hostdata/')

settings = xbmcaddon.Addon(id='plugin.video.phstreams')
getinfo  = settings.getSetting('md_switch')
addonp = xbmcaddon.Addon('plugin.video.phstreams')
addonPath = addonp.getAddonInfo('path')
artPath = addonPath + '/art/'

#fanart = artPath +'fanart.jpg'

#Meta Bypass Repleacement===================
nonMetaInfo = {'rating':'None','duration':'unknown','genre':'unknown','mpaa':"Not Enabled"'',
        'plot': 'MetaData is not enabled in addon settings','title':mname,'writer':'Phoenix Poster','cover_url':thumb,
        'director':'','backdrop_url':fanart,'tmdb_id':'','year':''}
#END Meta Replacement ============================


def OPEN_URL(url):
  if settings.getSetting('cache_enable') == 'true':
      response=main.OPEN_URL(url)
      req=urllib2.Request(url)
      req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
      #response=urllib2.urlopen(req)
      response=main.OPEN_URL(url)
      link=response
      #link=response.read()
      #response.close()
      return link
  else:
      req=urllib2.Request(url)
      req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
      response=urllib2.urlopen(req)
      link=response.read()
      response.close()
      return link
    





def LogNotify(title,message,times,icon):
        xbmc.executebuiltin("XBMC.Notification("+title+","+message+","+times+","+icon+")")



def DMODE(murl):
        link=OPEN_URL(murl)
        #link=OPEN_URL(murl)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        r=re.findall('<poster>(.+?)</poster>',link)
        if r:
                vip=r[0]
        else:
                vip=''
        f=re.findall('<fanart>(.+?)</fanart>',link)
        if f:
                fanart=f[0]
        else:
                fanart=''
        #print 'FANART IS ' +fanart
        md=re.findall('<meta>(.+?)</meta>',link)
        if md:
                mymeta=md[0]
        else:
                mymeta=''
        srt=re.findall('<sort>(.+?)</sort>',link)
        if srt:
                mysort=srt[0]
        else:
                mysort=''
        #print "SORT METHOD IS = " +mysort        
        match=re.compile('<notify><new>(.+?)</new><message1>(.+?)</message1><message2>(.+?)</message2><message3>(.+?)</message3><old>(.+?)</old></notify>').findall(link)
        if len(match)>0:
            for new,mes1,mes2,mes3,old in match: continue
            if new != ' ':
                new=vip+new
                onetime=os.path.join(main.datapath,'OneTime')
                notified=os.path.join(onetime,str(new))
                if not os.path.exists(notified):
                    open(notified,'w').write('version="%s",'%new)
                    dialog = xbmcgui.Dialog()
                    ok=dialog.ok('[B] Announcement From '+vip+'![/B]', str(mes1) ,str(mes2),str(mes3))
                if old != ' ':
                    old=vip+old
                    notified=os.path.join(onetime,str(old))
                    if  os.path.exists(notified):
                        os.remove(notified)
            else: print 'No Messages'
        else: print 'Link Down'
        match3=re.compile('<name>([^<]+)</name><link>([^<]+)</link><thumbnail>([^<]+)</thumbnail><mode>([^<]+)</mode>').findall(link)
        if mysort == 'yes':
          for name,url,thumb,mode in sorted(match3):
                if re.findall('http',thumb):
                        thumbs=thumb
                else:
                        thumbs=art+'/'+thumb+'.png'
                       
                data = '' 
                if getinfo == 'true' and mymeta =='movies':
                  try:
                    inc = 0
                    movie_name = name[:-6]
                    year = name[-6:]
                    movie_name = movie_name.decode('UTF-8','ignore')
                  
                    data = main.GRABMETA(movie_name,year)
                    thumb = data['cover_url']               
                    yeargrab = data['year']
                    year = str(yeargrab)
                  except:return
                elif getinfo == 'true' and mymeta =='tv':
                  try:
                    inc = 0
                    #movie_name = name[:-6]
                    #year = name[-6:]
                    name = name.decode('UTF-8','ignore')
                  
                    data = main.GRABTVMETA(name,'')
                    thumb = data['cover_url']               
                    #yeargrab = data['year']
                    #year = str(yeargrab)
                  except:return  
                
                favtype = 'movie'        
                main.addDir(name,url,mode,thumbs,fanart,data,favtype,'')
        else:    
           for name,url,thumb,mode in match3:
                if re.findall('http',thumb):
                        thumbs=thumb
                else:
                        thumbs=art+'/'+thumb+'.png'
                       
                data = '' 
                if getinfo == 'true' and mymeta =='movies':
                  try:
                    inc = 0
                    movie_name = name[:-6]
                    year = name[-6:]
                    movie_name = movie_name.decode('UTF-8','ignore')
                  
                    data = main.GRABMETA(movie_name,year)
                    thumb = data['cover_url']               
                    yeargrab = data['year']
                    year = str(yeargrab)
                  except:return
                elif getinfo == 'true' and mymeta =='tv':
                  try:
                    inc = 0
                    #movie_name = name[:-6]
                    #year = name[-6:]
                    name = name.decode('UTF-8','ignore')
                  
                    data = main.GRABTVMETA(name,'')
                    thumb = data['cover_url']               
                    #yeargrab = data['year']
                    #year = str(yeargrab)
                  except:return  
                
                favtype = 'movie'        
                main.addDir(name,url,mode,thumbs,fanart,data,favtype,'')
        match=re.compile('<name>([^<]+)</name><link>([^<]+)</link><thumbnail>([^<]+)</thumbnail><date>([^<]+)</date>').findall(link)
        for name,url,thumb,date in match:
            main.addDir(name+' [COLOR red] Updated '+date+'[/COLOR]',url,'ndmode',thumb,fanart,'','','')
        info=re.findall('<info><message>(.+?)</message><thumbnail>(.+?)</thumbnail></info>',link)
        if info:
            for msg,pic in info:
                main.addLink(msg,'',pic)
        popup=re.compile('<popup><name>([^<]+)</name.+?popImage>([^<]+)</popImage.+?thumbnail>([^<]+)</thumbnail.+?sound>([^<]+)</sound></popup>').findall(link)
        for name,image,thumb,sound in popup:
                
                main.addDir(name,image,'vpop',thumb,fanart,'','',sound)
      
def NDMODE(mname,murl):
        link=OPEN_URL(murl)
        #link=OPEN_URL(murl)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        r=re.findall('<poster>(.+?)</poster>',link)
        if r:
                vip=r[0]
        else:
                vip=''
        f=re.findall('<fanart>(.+?)</fanart>',link)
        if f:
                fanart=f[0]
        else:
                fanart=''
        #print 'FANART IS ' +fanart
        md=re.findall('<meta>(.+?)</meta>',link)
        if md:
                mymeta=md[0]
        else:
                mymeta=''
        srt=re.findall('<sort>(.+?)</sort>',link)
        if srt:
                mysort=srt[0]
        else:
                mysort=''
        #print "SORT METHOD IS = " +mysort         
        info=re.findall('<info><message>(.+?)</message><thumbnail>(.+?)</thumbnail></info>',link)
        if info:
            for msg,pic in info:
                main.addLink(msg,'',pic)
        popup=re.compile('<popup><name>([^<]+)</name.+?popImage>([^<]+)</popImage.+?thumbnail>([^<]+)</thumbnail></popup>').findall(link)
        for name,image,thumb in popup:
                main.addDir(name,image,'vpop',thumb,fanart,'','','')
        directory=re.compile('<dir><name>([^<]+)</name.+?link>([^<]+)</link.+?thumbnail>([^<]+)</thumbnail><fanart>([^<]+)</fanart></dir>').findall(link)
          #for name,url,thumb,fanart in directory:
       
        for name,url,thumb,fanart2 in directory:
          main.addDir(name,url,'ndmode',thumb,fanart2,'','','') 
         
        directory2=re.compile('<dir><name>([^<]+)</name.+?link>([^<]+)</link.+?thumbnail>([^<]+)</thumbnail></dir>').findall(link)
        for name,url,thumb in directory2:
          main.addDir(name,url,'ndmode',thumb,fanart,'','','')
        match=re.compile('<title>([^<]+)</title.+?link>(.+?)</link.+?thumbnail>([^<]+)</thumbnail>').findall(link)
        if mysort=='yes':
          for name,url,thumb in sorted(match):
            sitethumb = thumb
            data = ''
            if getinfo == 'true' and mymeta =='movies':
              try:
                    inc = 0
                    movie_name = name[:-6]
                    year = name[-6:]
                    movie_name = movie_name.decode('UTF-8','ignore')
                  
                    data = main.GRABMETA(movie_name,year)
                    thumb = data['cover_url']               
                    yeargrab = data['year']
                    year = str(yeargrab)
                    if thumb == '':
                        thumb = sitethumb
              except:return         
            if getinfo == 'true' and mymeta =='tv':
                  try:
                    inc = 0
                    #movie_name = name[:-6]
                    #year = name[-6:]
                    name = name.decode('UTF-8','ignore')
                  
                    data = main.GRABTVMETA(name,'')
                    thumb = data['cover_url']               
                    #yeargrab = data['year']
                    #year = str(yeargrab)
                    if thumb == '':
                        thumb = sitethumb
                  except:return  
            if 'sublink' in url:
              main.addDir(name,url,'sublinks',thumb,fanart,'','','')
            else:
              favtype = 'movie'
              #print "DL DIR THUMBNAIL IS =" +thumb
              main.addDLDir(name,url,'linkmode',thumb,fanart,'','',data,isFolder=False, isPlayable=True)


        else:    
          for name,url,thumb in match:
              sitethumb = thumb
              data = ''
              if getinfo == 'true' and mymeta =='movies':
                try:
                      inc = 0
                      movie_name = name[:-6]
                      year = name[-6:]
                      movie_name = movie_name.decode('UTF-8','ignore')
                    
                      data = main.GRABMETA(movie_name,year)
                      thumb = data['cover_url']               
                      yeargrab = data['year']
                      year = str(yeargrab)
                      if thumb == '':
                          thumb = sitethumb
                except:return         
              if getinfo == 'true' and mymeta =='tv':
                    try:
                      inc = 0
                      #movie_name = name[:-6]
                      #year = name[-6:]
                      name = name.decode('UTF-8','ignore')
                    
                      data = main.GRABTVMETA(name,'')
                      thumb = data['cover_url']               
                      #yeargrab = data['year']
                      #year = str(yeargrab)
                      if thumb == '':
                          thumb = sitethumb
                    except:return  
              if 'sublink' in url:
                main.addDir(name,url,'sublinks',thumb,fanart,'','','')
              else:
                favtype = 'movie'
                #print "DL DIR THUMBNAIL IS =" +thumb
                main.addDLDir(name,url,'linkmode',thumb,fanart,'','',data,isFolder=False, isPlayable=True)


def LINKMODE(mname,murl,thumb):
        #print "LINKMODE thumb IS "+thumb 
        thumb = thumb
        namelist=[]
        urllist=[]
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        if '.f4m'in murl:
                from resources.mobules import F4mProxy
                player=F4mProxy.f4mProxyHelper()
                proxy=None
                use_proxy_for_chunks=False
                player.playF4mLink(murl, mname, proxy, use_proxy_for_chunks,'',thumb)
                
        else:
                if '</regex>'in murl: 
                        murl=main.doRegex(murl)        
                        '''match=re.compile('<sublink>(.+?)</sublink>').findall(murl)
                        if match:
                                i=1
                                for url in match:
                                        if getinfo == 'true':        
                                                inc = 0
                                                movie_name = mname[:-6]
                                                year = mname[-6:]
                                                movie_name = movie_name.decode('UTF-8','ignore')
                                              
                                                data = main.GRABMETA(movie_name,year)
                                                thumb = data['cover_url']               
                                                yeargrab = data['year']
                                                year = str(yeargrab)               
                                        if getinfo == 'false':
                                          data = nonMetaInfo
                                  
                                        name= mname+ " Link "+str(i)
                                        namelist.append(name)        
                                        urllist.append(url)
                                        i=i+1
                                main.addDLDir(name,url,'liveresolver',thumb,fanart,'','',data)'''
                                
                else:
                  stream_url = murl
                  urls = murl
                  stream_url=resolvers.resolve_url(murl)
                  xbmc.sleep(1000)
                  LIVERESOLVE(mname,stream_url,thumb)
                  

def LIVERESOLVE(name,url,thumb):
         #print "RESOLVE THUMBNAIL IS " +thumb
         #params = {'url':url, 'name':name, 'thumb':thumb}
         #addon.add_video_item(params, {'title':name}, img=thumb)
         liz=xbmcgui.ListItem(name, iconImage=thumb, thumbnailImage=thumb)
         liz.setInfo( type="Video", infoLabels={ "Title": name} )
         url = str(url)
         liz.setPath(url)

         xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
         #xbmc.Player ().play(str(url), liz, False)
         #return
         

def LIVERESOLVER(name,url,thumb):
        stream_url = url
        urls = url
        stream_url=resolvers.resolve_url(url)
        xbmc.sleep(1000)
        LIVERESOLVE(name,stream_url,thumb) 


def SUBLINKS(mname,murl,thumb):
  thumb = thumb
  namelist=[]
  urllist=[]
  playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
  playlist.clear()
  #link=OPEN_URL(murl)
  match=re.compile('<sublink>(.+?)</sublink>').findall(murl)
  if match:
          i=1
          for url in match:
                  if getinfo == 'true':        
                          inc = 0
                          movie_name = mname[:-6]
                          year = mname[-6:]
                          movie_name = movie_name.decode('UTF-8','ignore')
                        
                          data = main.GRABMETA(movie_name,year)
                          thumb = data['cover_url']               
                          yeargrab = data['year']
                          year = str(yeargrab)               
                  if getinfo == 'false':
                    data = nonMetaInfo
            
                  name= mname+ " Link "+str(i)
                  namelist.append(name)        
                  urllist.append(url)
                  i=i+1
                  main.addDLDir(name,url,'liveresolver',thumb,fanart,'','',data,isFolder=False, isPlayable=True)
          

   

