import urllib,urllib2,re,cookielib,os,sys
import xbmc, xbmcgui, xbmcaddon, xbmcplugin,time
from resources.modules import main, vipplaylist,resolvers
import subprocess
import FuckNeulionClient

from addon.common.addon import Addon
addon_id = 'plugin.video.phstreams'
selfAddon = xbmcaddon.Addon(id=addon_id)
addon = Addon('plugin.video.phstreams', sys.argv)
art = main.art


addonp = xbmcaddon.Addon('plugin.video.phstreams')
addonPath = addonp.getAddonInfo('path')
jarPath = addonPath + '/jars/'

jarfile = jarPath +'FuckNeulionV2.jar'
artPath = addonPath + '/art/'


def MAINNHL(murl):
    source_media = {}
    from datetime import datetime
    datex=datetime.now().strftime('%Y%m%d')
    xml='http://live.nhl.com/GameData/SeasonSchedule-20142015.json'
    link=main.OPEN_URL(xml)
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('  ','')
    main.addDir('[COLOR red]Archived Games Click Here[/COLOR]','Archived','mainnhlarch',artPath+'hockey.jpg','','','','')
    if 'Archived' not in murl:
        main.addLink("[COLOR gold]Live Games , Requires some modifications to get working visit forum.[/COLOR]",'','')
        main.addLink("[COLOR gold]If list returns BLANK, Feed is not up yet.[/COLOR]",'','')
    match=re.compile('{"id":(.+?),"est":"(.+?)","a":"(.+?)","h":"(.+?)"}',re.DOTALL).findall(link)
    for id,timed,ateam,hteam in match:
        split= re.search('(.+?)\s(\d+:\d+):\d+',timed)
        split1=str(split.group(1))
        split2=str(split.group(2))
        if 'Archived' in murl:
            if int(split1)<=int(datex):
                dates= re.search('(\d{4})(\d{2})(\d{2})',split1)
                date=str(dates.group(2))+"/"+str(dates.group(3))+"/"+str(dates.group(1))
                timed = time.strftime("%I:%M %p", time.strptime(split2, "%H:%M"))
                main.addDir(ateam+' at '+hteam+' [COLOR gold]('+timed+')[/COLOR] [COLOR red]('+date+')[/COLOR]',id,'nhllistreams',art+'/nhl.png','','','','')
        else:
            if datex == split1:
                
                dates= re.search('(\d{4})(\d{2})(\d{2})',split1)
                date=str(dates.group(2))+"/"+str(dates.group(3))+"/"+str(dates.group(1))
                timed = time.strftime("%I:%M %p", time.strptime(split2, "%H:%M"))
                main.addDir(ateam+' at '+hteam+' [COLOR gold]('+timed+')[/COLOR] [COLOR red]('+date+')[/COLOR]',id,'nhllistreams',art+'/nhl.png','','','','')
                

def MAINNHLARCH(murl):
    source_media = {}
    from datetime import datetime
    datex=datetime.now().strftime('%Y%m%d')
    xml='http://live.nhl.com/GameData/SeasonSchedule-20142015.json'
    link=main.OPEN_URL(xml)
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('  ','')
    main.addDir('[COLOR red]Return to LIVE Games Click Here[/COLOR]','none','mainnhl',artPath+'hockey.jpg','','','','')
    #if 'Archived' not in murl:
        #main.addLink("[COLOR gold]Live Games , Requires some modifications to get working visit forum.[/COLOR]",'','')
        #main.addLink("[COLOR gold]If list returns BLANK, Feed is not up yet.[/COLOR]",'','')
    match=re.compile('{"id":(.+?),"est":"(.+?)","a":"(.+?)","h":"(.+?)"}',re.DOTALL).findall(link)
    for id,timed,ateam,hteam in match:
        split= re.search('(.+?)\s(\d+:\d+):\d+',timed)
        split1=str(split.group(1))
        split2=str(split.group(2))
        if 'Archived' in murl:
            if int(split1)<=int(datex):
                dates= re.search('(\d{4})(\d{2})(\d{2})',split1)
                date=str(dates.group(2))+"/"+str(dates.group(3))+"/"+str(dates.group(1))
                timed = time.strftime("%I:%M %p", time.strptime(split2, "%H:%M"))
                main.addDir(ateam+' at '+hteam+' [COLOR gold]('+timed+')[/COLOR] [COLOR red]('+date+')[/COLOR]',id,'nhllistreams',art+'/nhl.png','','','','')
        else:
            if datex == split1:
                
                dates= re.search('(\d{4})(\d{2})(\d{2})',split1)
                date=str(dates.group(2))+"/"+str(dates.group(3))+"/"+str(dates.group(1))
                timed = time.strftime("%I:%M %p", time.strptime(split2, "%H:%M"))
                main.addDir(ateam+' at '+hteam+' [COLOR gold]('+timed+')[/COLOR] [COLOR red]('+date+')[/COLOR]',id,'nhllistreams',art+'/nhl.png','','','','')
                



def LISTSTREAMS(mname,murl):
    mname=main.removeColoredText(mname)
    id= re.search('(\d{4})(\d{2})(\d{4})',murl)
    #print "HERE IS THE GROUPS = " +str(id.group(1)) +str(id.group(2)) +str(id.group(3))
    xml='http://smb.cdnak.neulion.com/fs/nhl/mobile/feed_new/data/streams/'+str(id.group(1))+'/ipad/'+str(id.group(2))+'_'+str(id.group(3))+'.json'
    #print "THE NEW XML IS =" +xml
    #xml ='http://smb.cdnak.neulion.com/fs/nhl/mobile/feed_new/data/streams/2014/ipad/02_0335.json'
    link=main.OPEN_URL(xml)
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('  ','')
    match=re.compile('"vod-condensed":{"bitrate0":"([^"]+)"},"vod-continuous":{"bitrate0":"([^"]+)","image":"([^"]+)"},"vod-whole":{"bitrate0":"([^"]+)"}',re.DOTALL).findall(link)
    for cond,cont,thumb,whole in match:
        if '_h_condensed' in cond:
            main.addPlayc(mname+' [COLOR red]Home Condensed[/COLOR]',cond,'nhllink',thumb,'','','','','')
        else:
            main.addPlayc(mname+' [COLOR red]Away Condensed[/COLOR]',cond,'nhllink',thumb,'','','','','')
        if '_h_continuous' in cont:
            main.addPlayc(mname+' [COLOR red]Home Continuous[/COLOR]',cont,'nhllink',thumb,'','','','','')
        else:
            main.addPlayc(mname+' [COLOR red]Away Continuous[/COLOR]',cont,'nhllink',thumb,'','','','','')
        if '_h_whole' in whole:
            main.addPlayc(mname+' [COLOR red]Home Whole[/COLOR]',whole,'nhllink',thumb,'','','','','')
        else:
            main.addPlayc(mname+' [COLOR red]Away Whole[/COLOR]',whole,'nhllink',thumb,'','','','','')
    match2=re.compile('"away".+?"live":{"bitrate0":"([^"]+)"},.+?"image":"([^"]+)"',re.DOTALL).findall(link)
    for live,thumb in match2:
        main.addPlayc(mname+' [COLOR gold]Away Live[/COLOR]',live+'x0xe'+str(murl),'nhllink',thumb,'','','','','')
    match3=re.compile('"home".+?"live":{"bitrate0":"([^"]+)"},.+?"image":"([^"]+)"',re.DOTALL).findall(link)
    for live,thumb in match3:
        main.addPlayc(mname+' [COLOR gold]Home LIVE[/COLOR]',live+'x0xe'+str(murl),'nhllink',thumb,'','','','','')


def LINK(mname,murl,thumb):
        print "LIVE MURL IS =" + murl
        ok=True
        namelist=[]
        urllist=[]
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        if '_whole' in murl:
            link=main.OPEN_URL(murl)
            link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('  ','')
            part= re.findall('/([^/]+)ipad.mp4.m3u8',murl)[0]
            match=re.compile('BANDWIDTH=.+?'+part+'(.+?)_ipad.mp4.m3u8',re.DOTALL).findall(link)
            for band in sorted(match):
                namelist.append(band)
            dialog = xbmcgui.Dialog()
            answer =dialog.select("Pick A Bandwidth", namelist)
            if answer != -1:
                nurl=murl.split('ipad.mp4.m3u8')[0]
                stream_url=nurl+namelist[int(answer)]+'_ipad.mp4.m3u8'+'|User-Agent=PS4 libhttp/1.76 (PlayStation 4)'
                NHLRESOLVE(mname,stream_url,thumb)
            else:
                return
        elif '/live/' in murl:
            import subprocess
            #jarfile = xbmc.translatePath('special://home/addons/plugin.video.phstreams/FuckNeulionV2.jar')
            #jarfile = selfAddon + '/resources/modules/FuckNeulionV2.jar'
            print "JARFILE IS = " + jarfile
            if 'Home' in mname:
                Side='home'
            if 'Away' in mname:
                Side='away'
            SelectGame=murl.split('x0xe')[1]
            murl=murl.split('x0xe')[0]
            startupinfo = None
            if os.name == 'nt':
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

                
            command=['java','-jar',jarfile,SelectGame,Side]
            proxy_hack_process = subprocess.Popen(command,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT,
                          startupinfo=startupinfo)
            if os.name == 'posix':
                # Run the proxy hack before playing the stream
                success = False
                
                success, output = FuckNeulionClient.request_proxy_hack(SelectGame,Side)

            xbmc.sleep(1000)
            link=main.OPEN_URL(murl)
            link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('  ','')
            part= re.findall('/([^/]+)ipad.m3u8',murl)[0]
            match=re.compile('BANDWIDTH=.+?'+part+'(.+?)_ipad.m3u8',re.DOTALL).findall(link)
            for band in sorted(match):
                namelist.append(band)
            dialog = xbmcgui.Dialog()
            answer =dialog.select("Pick A Bandwidth", namelist)
            if answer != -1:
                nurl=murl.split('ipad.m3u8')[0]
                stream_url=nurl+namelist[int(answer)]+'_ipad.m3u8'+'|User-Agent=PS4 libhttp/1.76 (PlayStation 4)'
                NHLRESOLVE(mname,stream_url,thumb)
            else:
                return
        else:
            stream_url = murl+'|User-Agent=PS4 libhttp/1.76 (PlayStation 4)'
            NHLRESOLVE(mname,stream_url,thumb)

def NHLRESOLVE(name,url,thumb):
         #print "RESOLVE THUMBNAIL IS " +thumb
         params = {'url':url, 'name':name, 'thumb':thumb}
         addon.add_video_item(params, {'title':name}, img=thumb)
         liz=xbmcgui.ListItem(name, iconImage=thumb, thumbnailImage=thumb)
         #liz.setInfo( type="Video", infoLabels={ "Title": name} )
         #liz.setPath(url)

         #xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
         xbmc.Player ().play(str(url), liz, False)
         return
            
        
