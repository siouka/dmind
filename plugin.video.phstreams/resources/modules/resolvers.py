# -*- coding: cp1252 -*-
#Custom vipplaylist by Blazetamer 
import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,urlresolver,xbmc,os,xbmcaddon,main,math,cookielib,os.path, string
from resources.modules import main
import urlresolver
import vipplaylist
from addon.common.addon import Addon
#from addon.common.net import Net as net
from addon.common.net import Net
from t0mm0.common.net import Net as net
addon_id = 'plugin.video.phstreams'
selfAddon = xbmcaddon.Addon(id=addon_id)
addon = Addon('plugin.video.phstreams', sys.argv)
ADDON = xbmcaddon.Addon(id='plugin.video.phstreams')
#net = Net(http_debug=True)
datapath = xbmc.translatePath(selfAddon.getAddonInfo('profile'))
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
headers = addon.queries.get('headers', '')
loggedin = addon.queries.get('loggedin', '')
header_dict = addon.queries.get('header_dict', '')
fanart = addon.queries.get('fanart', '')
console = addon.queries.get('console', '')
dlfoldername = addon.queries.get('dlfoldername', '')
ext = addon.queries.get('ext', '')
#======================== END Alternate Param Stuff=======================
#newagent ='Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36'
#net.set_user_agent(newagent)
#cookiejar = xbmc.translatePath(ADDON.getAddonInfo('profile'))
cookiejar = addon.get_profile()
cookiejar = os.path.join(cookiejar,'cookies.lwp')
settings = xbmcaddon.Addon(id='plugin.video.phstreams')
elogo = ''
datapaths = xbmc.translatePath(ADDON.getAddonInfo('profile'))
CookiePath=os.path.join(datapaths,'Cookies')
try: os.makedirs(CookiePath)
except: pass

def LogNotify(title,message,times,icon):
        xbmc.executebuiltin("XBMC.Notification("+title+","+message+","+times+","+icon+")")

#####Start Resolvers========================
class ResolverError(Exception):
    def __init__(self, value, value2):
        value = value
        value2 = value2
    def __str__(self):
        return repr(value,value2)

def resolve_url(murl):
    #stream_url = False
    
    if(murl):
        #try:
            
            if 'project-free-upload' in murl:
                stream_url=resolve_projectfreeupload(murl)
                return stream_url
        
            if 'veehd' in murl :
                stream_url=resolve_veehd(murl)
                print "STREAMURL IS ="+stream_url
                return stream_url
        
            if 'videomega'in murl :
                stream_url=resolve_videomega(murl)
                return stream_url

            if 'youtube' in murl:
                try:murl=murl.split('watch?v=')[1]
                except:
                    try:murl=murl.split('com/v/')[1]
                    except:
                        try:murl=murl.split('videoid=') [1]
                           
                        except: murl=murl.split('com/embed/') [1]
                print "MURL AFTER IS  "+ murl               
                stream_url='plugin://plugin.video.youtube/?action=play_video&videoid=' +str(murl)
                return stream_url    
                
            if 'epicshare'in murl:
                stream_url=resolve_epicshare(murl)
                return stream_url

                
            if 'lemuploads'in murl :
                stream_url=resolve_lemupload(murl)
                return stream_url
                
                           
            if 'hugefiles'in murl:
                stream_url=resolve_hugefiles(murl)
                return stream_url

                
            if 'megarelease' in murl:
                stream_url=resolve_megarelease(murl)
                return stream_url
                
            
            if 'bayfiles' in murl:
                stream_url=resolve_bayfiles(murl)
                return stream_url
            
            
            if 'vidspot' in murl:
                stream_url=resolve_vidspot(murl)
                return stream_url

                
            if 'youwatch' in murl:
                stream_url=resolve_youwatch(murl)
                return stream_url

                
            if 'vk.com' in murl:
                stream_url=resolve_VK(murl)
                return stream_url

                
            if '(?i)(firedrive|putlocker)' in murl:
                stream_url=resolve_firedrive(murl)
                return stream_url

                
            
            if 'yify.tv' in murl:
                stream_url=resolve_yify(murl)
                return stream_url

                
            if 'mail.ru' in murl:
                stream_url=resolve_mailru(murl)
                return stream_url

                
            if 'g2g.fm' in murl:
                stream_url=resolve_g2g(murl)
                return stream_url

                
            if 'docs.google' in murl:
                stream_url=resolve_googleDocs(murl)
                return stream_url

                
            if 'mrfile' in murl:
                stream_url=resolve_mrfile(murl)
                return stream_url
                
            
            if 'picasaweb.google' in murl:
                stream_url=resolve_picasaWeb(murl)

            #if 'billionuploads' in murl:
                #stream_url=resolve_billionuploads(murl,'')
                #return stream_url    
            
            else:
                
                hmf = urlresolver.HostedMediaFile(murl)
                if hmf:
                     host = hmf.get_host()
                     dlurl = urlresolver.resolve(murl)
                     return dlurl
  
                else:
                     return murl
            
    

def logerror(log):
    xbmc.log(log, xbmc.LOGERROR)

    
def grab_cloudflare(url):

    class NoRedirection(urllib2.HTTPErrorProcessor):
        # Stop Urllib2 from bypassing the 503 page.    
        def http_response(self, request, response):
            code, msg, hdrs = response.code, response.msg, response.info()

            return response
        https_response = http_response

    cj = cookielib.CookieJar()
    
    opener = urllib2.build_opener(NoRedirection, urllib2.HTTPCookieProcessor(cj))
    opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36')]
    response = opener.open(url).read()
        
    jschl=re.compile('name="jschl_vc" value="(.+?)"/>').findall(response)
    if jschl:
        import time
        jschl = jschl[0]    
    
        maths=re.compile('value = (.+?);').findall(response)[0].replace('(','').replace(')','')

        domain_url = re.compile('(https?://.+?/)').findall(url)[0]
        domain = re.compile('https?://(.+?)/').findall(domain_url)[0]
        
        time.sleep(5)
        
        normal = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        normal.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36')]
        final= normal.open(domain_url+'cdn-cgi/l/chk_jschl?jschl_vc=%s&jschl_answer=%s'%(jschl,eval(maths)+len(domain))).read()
        
        response = normal.open(url).read()

    return response

def millis():
      import time as time_
      return int(round(time_.time() * 1000))
    
def load_json(data):
      def to_utf8(dct):
            rdct = {}
            for k, v in dct.items() :
                  if isinstance(v, (str, unicode)) :
                        rdct[k] = v.encode('utf8', 'ignore')
                  else :
                        rdct[k] = v
            return rdct
      try :        
            from lib import simplejson
            json_data = simplejson.loads(data, object_hook=to_utf8)
            return json_data
      except:
            try:
                  import json
                  json_data = json.loads(data, object_hook=to_utf8)
                  return json_data
            except:
                  import sys
                  for line in sys.exc_info():
                        print "%s" % line
      return None


        
def resolve_mrfile(url):
    try:
        import jsunpack
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving Phoenix  Link...')       
        dialog.update(0)
        print 'Phoenix MR.File - Requesting GET URL: %s' % url
        html = net().http_GET(url).content
        embed=re.findall('<IFRAME SRC="(http://mrfile[^"]+)"',html)
        html = net().http_GET(embed[0]).content
        r = re.findall(r'(eval\(function\(p,a,c,k,e,d\)\{while.+?)</script>',html,re.M|re.DOTALL)
        try:unpack=jsunpack.unpack(r[1])
        except:unpack=jsunpack.unpack(r[0])
        try:stream_url=re.findall('<param name="src"value="(.+?)"/>',unpack)[0]
        except:stream_url=re.findall("file: '([^']+)'",html)[0]
        return stream_url
        if dialog.iscanceled(): return None
    except Exception:
        logerror('**** MR.File Error occured: %s' % e)
        xbmc.executebuiltin('[B][COLOR white]MR.File[/COLOR][/B]','[COLOR red]%s[/COLOR]' % e, 5000, elogo)

  

def resolve_g2g(url):
    html3 = net().http_GET(url).content 
    url2 = re.findall('(?sim)<iframe src="(http://g2g.fm/pasmov3p.php.+?)"', html3)[0]
    req = urllib2.Request(url2)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    req.add_header('Referer', url)
    response = urllib2.urlopen(req)
    html=response.read()
    response.close()
    phpUrl = re.findall('(?sim)<iframe id="ggplayer" src="(.+?php)"', html)[0]
    req = urllib2.Request(phpUrl)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    req.add_header('Referer', url)   
    response = urllib2.urlopen(req)
    html2=response.read()
    response.close()
    googleUrl = re.findall('(?sim)<iframe src="(.+?preview)"', html2)[0]
    return resolve_googleDocs(googleUrl)
     
def unescapes(text):
    if text:
        rep = {"\u003d":"=","\u0026":"&","u003d":"=","u0026":"&","%26":"&","&#38;":"&","&amp;":"&","&#044;": ",","&nbsp;": " ","\n": "","\t": "","\r": "","%5B": "[","%5D": "]",
               "%3a": ":","%3A":":","%2f":"/","%2F":"/","%3f":"?","%3F":"?","%3d":"=","%3D":"=","%2C":",","%2c":",","%3C":"<",
               "%20":" ","%22":'"',"%3D":"=","%3A":":","%2F":"/","%3E":">","%3B":",","%27":"'","%0D":"","%0A":"","%92":"'",
               "&lt;": "<","&gt;": ">","&quot": '"',"&rsquo;": "'","&acute;": "'"}
        for s, r in rep.items():
            text = text.replace(s, r) 
    #except TypeError: pass
    return text

def resolve_picasaWeb(url):
    run = net().http_GET(url)
    cjList=[]
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj), urllib2.HTTPHandler())
    req = urllib2.Request(url)
    f = opener.open(req)
    html = f.read()
    for cookie in cj:
            cjList.append(str(cookie).replace('<Cookie ','').replace(' for picasaweb.google.com/>','').replace('for .google.com/>',''))
    Lid=re.search('https://picasaweb.google.com/(.+?)/.+?authkey=(.+?)#([^<]+)',url)
    url='https://picasaweb.google.com/data/entry/base/user/'+Lid.group(1)+'/photoid/'+Lid.group(3)+'?alt=rss&authkey='+Lid.group(2)
    namelist=[]
    urllist=[]
    dialog = xbmcgui.DialogProgress()
    dialog.create('Resolving', 'Resolving Phoenix  Link...')       
    dialog.update(0)
    print 'Phoenix GoogleDoc - Requesting GET URL: %s' % url
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36')
    req.add_header('cookie', 'xnfo=1; PREF=ID=85556f1a24007f7a:U=dc2692c0a6061b26:FF=0:LD=en:TM=1373784453:LM=1389395973:GM=1:S=qR9eOdnLEbmW_TLb; HSID=A20CRcfWXDjH2t8pM; SSID=AT-HtXZJKl-_80o2K; APISID=Oxz2q50wC6cLlo6-/AGZzvI9THf_52xvSO; SAPISID=kF1H8rjAwWjKPFU6/AjxdPvG1MVo2oU8aT; lh=DQAAAM4AAACjRFpk1gWTm8hUwNXV8b4iTC6-IIL6RsAD8urndnSZYTYKgkuDD4aOktLrRQXWX4--37oGvyHC4c07ooRuZ0AxVdGINz5UCX5n4-63PwQDpKnqvJnFiv4SaS3UQlLrlXsoeSPDs2-bWOpBNn9b7BCfQr9XJXC5OJrpiDFlKOJ3XIjJ8Kh3M0Z2K84u2k3pb7l2ODvIFGjk38GLmn-gPSHENZEmCgV-KsqpgDTQ0EnPU-h03OHch9xEmof7HD4TzzV71YS5X9hNGbYzp3ux5asE;  '+cjList[1]+'; noRedirect=1; SID=DQAAAMwAAABwVBj_2BKoFX1DvzaYSC2Vd7ieIUcNRpOHAmwDkKE4KEmzBiIUPoGedSnY91jnlOUk7wysRSWIaT_NiI6SfpFHRS9FA59wG7XETqInr0vUA2si8J1IefoooMj6i3JBxdsc6wZ-XUYu57czbICcBshac3_al7xJLQJnGd1kz-2Zxn3IVi3c5sDL21pCc_1SegSDBFughkCAY7p7T8prVX6XLqf_JGv34RIx6pPYZ_emGzjEOVbbjswVvX-9uKLvARvYgsjXseS5k3_TMHNLYQWp; '+cjList[0])
    
    response = urllib2.urlopen(req)
    html=response.read()
    response.close()
    dialog.update(100)
    link2=unescapes(html)
    streams_map = str(link2)
    stream= re.compile("url='(http://redirector.googlevideo.com[^']+)' height='([^']+)'").findall(streams_map)
    for stream_url,stream_quality in reversed(stream):
        stream_url = unescapes(stream_url)
        urllist.append(stream_url)
        stream_qlty = stream_quality.upper()
        if (stream_qlty == '720'):
            stream_qlty = 'HD-720p'
        elif (stream_qlty == '480'):
            stream_qlty = 'SD-480p'
        elif (stream_qlty == '360'):
            stream_qlty = 'SD-360p'
        elif (stream_qlty == '240'):
            stream_qlty = 'SD-240p'
        namelist.append(stream_qlty)
    dialog = xbmcgui.Dialog()
    answer =dialog.select("Quality Select", namelist)
    if answer==-1:
        return
    else:
        return urllist[int(answer)]
    
def resolve_googleDocs(url):
    namelist=[]
    urllist=[]
    dialog = xbmcgui.DialogProgress()
    dialog.create('Resolving', 'Resolving Phoenix  Link...')       
    dialog.update(0)
    print 'Phoenix GoogleDoc - Requesting GET URL: %s' % url
    html = net().http_GET(url).content
    dialog.update(100)
    link2=unescapes(html)
    match= re.compile('url_encoded_fmt_stream_map":"(.+?),"').findall(link2)[0]
    if match:
        streams_map = str(match)
    else:
        streams_map = str(link2)
    stream= re.compile('url=(.+?)&type=.+?&quality=(.+?),').findall(streams_map)
    for stream_url,stream_quality in stream:
        stream_url = stream_url
        stream_url = unescapes(stream_url)
        urllist.append(stream_url)
        stream_qlty = stream_quality.upper()
        if (stream_qlty == 'hd1080'):
            stream_qlty = 'HD-1080p'
        elif (stream_qlty == 'hd720'):
            stream_qlty = 'HD-720p'
        elif (stream_qlty == 'latge'):
            stream_qlty = 'SD-480p'
        elif (stream_qlty == 'medium'):
            stream_qlty = 'SD-360p'
        namelist.append(stream_qlty)
    dialog = xbmcgui.Dialog()
    answer =dialog.select("Quality Select", namelist)
    if answer==-1:
        return
    else:
        return urllist[int(answer)]

def resolve_firedrive(url):
    try:
        url=url.replace('putlocker.com','firedrive.com').replace('putlocker.to','firedrive.com')
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving Phoenix  Link...')       
        dialog.update(0)
        print 'Phoenix Firedrive - Requesting GET URL: %s' % url
        html = net().http_GET(url).content
        dialog.update(50)
        if dialog.iscanceled(): return None
        post_data = {}
        r = re.findall(r'(?i)<input type="hidden" name="(.+?)" value="(.+?)"', html)
        for name, value in r:
            post_data[name] = value
        post_data['referer'] = url
        html = net().http_POST(url, post_data).content
        print html
        embed=re.findall('(?sim)href="([^"]+?)">Download file</a>',html)
        if not embed:
            embed=re.findall("(?sim)'(http://dl.firedrive.com/[^']+?)'",html)
        if dialog.iscanceled(): return None
        if embed:
            dialog.update(100)
            return embed[0]
        else:
            #logerror('Phoenix: Resolve Firedrive - File Not Found')
            #xbmc.executebuiltin("XBMC.Notification(File Not Found,Firedrive,2000)")
            return False
    except Exception:
        xbmc.executebuiltin("XBMC.Notification(Resolver Failed,FireDrive,2000)")


def resolve_mailru(url):
    try:
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving Phoenix  Link...')       
        dialog.update(0)
        print 'Phoenix MailRU - Requesting GET URL: %s' % url
        link = net().http_GET(url).content
        match=re.compile('videoSrc = "(.+?)",',re.DOTALL).findall(link)
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj), urllib2.HTTPHandler())
        req = urllib2.Request(url)
        f = opener.open(req)
        html = f.read()
        for cookie in cj:
            cookie=str(cookie)

        rcookie=cookie.replace('<Cookie ','').replace(' for .video.mail.ru/>','')

        vlink=match[0]+'&Cookie='+rcookie
        return vlink
    except Exception:
        logerror('**** MailRU Error occured: %s' % e)
        xbmc.executebuiltin('[B][COLOR white]MailRU[/COLOR][/B]','[COLOR red]%s[/COLOR]' % e, 5000, elogo)


def resolve_yify(url):
    try:
        referer = url
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving Phoenix  Link...')       
        dialog.update(0)
        print 'Phoenix Yify - Requesting GET URL: %s' % url
        html = net().http_GET(url).content
        url = re.compile('showPkPlayer[(]"(.+?)"[)]').findall(html)[0]
        key=url
        url = 'http://yify.tv/reproductor2/pk/pk/plugins/player_p2.php?url=' + url
        print url
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36')
        req.add_header('Referer', referer)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        print link
        
        if 'captcha' in link:
            print link
            captcha=re.search('{"captcha":(.+?),"k":"([^"]+)"}',link)
            curl='http://www.google.com/recaptcha/api/challenge?k='+captcha.group(2)+'&ajax=1&cachestop=0.7698786298278719'
            html = net().http_GET(curl).content
            print html
            image_id=re.findall("challenge : '([^']+)'",html)
            img_id=image_id[0]
            image_url='http://www.google.com/recaptcha/api/image?c='+img_id
            img = xbmcgui.ControlImage(450,15,400,130, image_url)
            wdlg = xbmcgui.WindowDialog()
            wdlg.addControl(img)
            wdlg.show()
        
            kb = xbmc.Keyboard('', 'Type the letters in the image', False)
            kb.doModal()
            capcode = kb.getText()
   
            if (kb.isConfirmed()):
                userInput = kb.getText()
                if userInput != '':
                    solution = kb.getText()
                elif userInput == '':
                    xbmc.executebuiltin('big', 'No text entered', 'You must enter text in the image to access video', '')
                    return False
            else:
                return False
               
            wdlg.close()
            url = 'http://yify.tv/reproductor2/pk/pk/plugins/player_p2.php'
            user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36'
            values = {'url' : key,'chall' : img_id,'type' :  captcha.group(1),'res':solution,'':'','':''}
            headers = { 'User-Agent' : user_agent,'Referer':'referer'}

            data = urllib.urlencode(values)
            req = urllib2.Request(url, data, headers)
            response = urllib2.urlopen(req)
            link = response.read()
        if '.pdf' in link:
            html = re.findall('{"url":"([^"]+.pdf)",',link)[0]
        else:
            html = re.compile('{"url":"([^"]+)"').findall(link)[1]
        stream_url = html
        return stream_url
    except Exception:
        xbmc.executebuiltin("XBMC.Notification(Resolver Failed,YiFi,2000)")


def resolve_VK(url):
    try:
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving Phoenix Link...')       
        dialog.update(0)
        print 'Phoenix VK - Requesting GET URL: %s' % url
        useragent='Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7'
        link2 = net(user_agent=useragent).http_GET(url).content
        if re.search('This video has been removed', link2, re.I):
            logerror('***** Phoenix VK - This video has been removed')
            xbmc.executebuiltin("XBMC.Notification(This video has been removed,VK,2000)")
            return Fals
        urllist=[]
        quaList=[]
        match=re.findall('(?sim)<source src="([^"]+)"',link2)
        for url in match:
            print url
            urllist.append(url)
            qua=re.findall('(?sim).(\d+).mp4',url)
            quaList.append(str(qua[0]))
        dialog2 = xbmcgui.Dialog()
        ret = dialog2.select('[COLOR=FF67cc33][B]Select Quality[/COLOR][/B]',quaList)
        if ret == -1:
            return False
        stream_url = urllist[ret]
        if match: 
            return stream_url.replace("\/",'/')
    except Exception:
        #logerror('**** VK Error occured: %s' % e)
        xbmc.executebuiltin("XBMC.Notification(Resolver Failed,VK,2000)")

def resolve_youwatch(url):
    try:
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving Phoenix  Link...')       
        dialog.update(0)
        print 'Phoenix Youwatch - Requesting GET URL: %s' % url
        if 'embed' not in url:
            mediaID = re.findall('http://youwatch.org/([^<]+)', url)[0]
            url='http://youwatch.org/embed-'+mediaID+'.html'
        else:url=url
        html = net().http_GET(url).content
        try:
                html=html.replace('|','/')
                stream=re.compile('/mp4/video/(.+?)/(.+?)/(.+?)/setup').findall(html)
                for id,socket,server in stream:
                    continue
        except:
                raise ResolverError('This file is not available on',"Youwatch")
        stream_url='http://'+server+'.youwatch.org:'+socket+'/'+id+'/video.mp4?start=0'
        return stream_url
    except Exception:
        xbmc.executebuiltin("XBMC.Notification(Resolver Failed,YouWatch,2000)")

def resolve_projectfreeupload(url):
    try:
        import jsunpack
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving Phoenix  Link...')       
        dialog.update(0)
        print 'Phoenix Project Free - Requesting GET URL: %s' % url
        html = net().http_GET(url).content
        r = re.findall(r'\"hidden\"\sname=\"?(.+?)\"\svalue=\"?(.+?)\"\>', html, re.I)
        post_data = {}
        for name, value in r:
            post_data[name] = value
        post_data['referer'] = url
        post_data['method_premium']=''
        post_data['method_free']=''
        html = net().http_POST(url, post_data).content
        embed=re.findall('<IFRAME SRC="(.+?)"',html)
        html = net().http_GET(embed[0]).content
        r = re.findall(r'(eval\(function\(p,a,c,k,e,d\)\{while.+?)</script>',html,re.M|re.DOTALL)
        try:unpack=jsunpack.unpack(r[1])
        except:unpack=jsunpack.unpack(r[0])
        stream_url=re.findall('<param name="src"value="(.+?)"/>',unpack)[0]
        return stream_url
        if dialog.iscanceled(): return None
    except Exception:
        xbmc.executebuiltin("XBMC.Notification(Resolver Failed,Project Free,2000)")

def resolve_videomega(url):
    try:
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving Phoenix  Link...')       
        dialog.update(0)
        print 'Phoenix Videomega - Requesting GET URL: %s' % url
        try:
            mediaID = re.findall('http://videomega.tv/.?ref=([^<]+)', url)[0]
            url='http://videomega.tv/iframe.php?ref='+mediaID
        except:url=url
        html = net().http_GET(url).content
        try:
                encodedurl=re.compile('unescape.+?"(.+?)"').findall(html)
        except:
                raise ResolverError('This file is not available on',"VideoMega")
        url2=urllib.unquote(encodedurl[0])
        stream_url=re.compile('file: "(.+?)"').findall(url2)[0]
        return stream_url
    except Exception:
        xbmc.executebuiltin("XBMC.Notification(Resolver Failed,Video Mega,2000)")
    
def resolve_vidspot(url):
    try:
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving Phoenix  Link...')       
        dialog.update(0)
        print 'Phoenix Vidspot - Requesting GET URL: %s' % url
        mediaID=re.findall('http://vidspot.net/([^<]+)',url)[0]
        url='http://vidspot.net/embed-'+mediaID+'.html'
        print url
        html = net().http_GET(url).content
        r = re.search('"file" : "(.+?)",', html)
        if r:
            stream_url = urllib.unquote(r.group(1))

        return stream_url

    except Exception:
        xbmc.executebuiltin("XBMC.Notification(Resolver Failed,VidSpot,2000)")
        


def resolve_megarelease(url):
    try:
        #Show dialog box so user knows something is happening
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving Phoenix  Link...')
        dialog.update(0)
        
        print 'MegaRelease Phoenix - Requesting GET URL: %s' % url
        html = net().http_GET(url).content

        dialog.update(50)
        
        #Check page for any error msgs
        if re.search('This server is in maintenance mode', html):
            logerror('***** MegaRelease - Site reported maintenance mode')
            xbmc.executebuiltin("XBMC.Notification(File is currently unavailable,MegaRelease in maintenance,2000)")                                
            return False
        if re.search('<b>File Not Found</b>', html):
            logerror('Phoenix: Resolve MegaRelease - File Not Found')
            xbmc.executebuiltin("XBMC.Notification(File Not Found,MegaRelease,2000)")
            return False

        filename = re.search('You have requested <font color="red">(.+?)</font>', html).group(1)
        filename = filename.split('/')[-1]
        extension = re.search('(\.[^\.]*$)', filename).group(1)
        guid = re.search('http://megarelease.org/(.+)$', url).group(1)
        
        vid_embed_url = 'http://megarelease.org/vidembed-%s%s' % (guid, extension)
        UserAgent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
        ACCEPT = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        request = urllib2.Request(vid_embed_url)
        request.add_header('User-Agent', UserAgent)
        request.add_header('Accept', ACCEPT)
        request.add_header('Referer', url)
        response = urllib2.urlopen(request)
        redirect_url = re.search('(http://.+?)video', response.geturl()).group(1)
        download_link = redirect_url + filename
        
        dialog.update(100)

        return download_link
        
    except Exception:
        xbmc.executebuiltin("XBMC.Notification(Resolver Failed,MegaRelease,2000)")
    finally:
        dialog.close()
        
def setCookie(url):

        
    username = settings.getSetting('vhd_user')
    password = settings.getSetting('vhd_pass')
    cookieExpired = False
    name = "veeHD"
    userName = username
    ref = 'http://veehd.com'
    submit = 'Login'
    terms = 'on'
    remember_me = 'on'
    net().http_GET(url)
    net().http_POST('http://veehd.com/login',{'ref': ref, 'uname': userName, 'pword': password, 'submit': submit, 'terms': terms,'remember_me':remember_me})

        
def resolve_veehd(url):
    if settings.getSetting('vhd_account') == 'false':
                dialog = xbmcgui.Dialog()
                ok = dialog.ok('VEE HD Account Login Not Enabled', '            Please Choose Vee HD Account Tab and Enable')
                if ok:
                        LogNotify('Vee HD Account Tab ', 'Please Enable Account', '5000', '')        
                        print 'YOU HAVE NOT SET THE USERNAME OR PASSWORD!'
                        addon.show_settings()
    
    try:
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving Phoenix  Link...')       
        dialog.update(0)
        if dialog.iscanceled(): return False
        dialog.update(33)
        headers = {}
        headers = {'User-Agent': 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7','Referer':url}
        print 'Phoenix VeeHD - Requesting GET URL: %s' % url
        setCookie('http://veehd.com')
        html = net().http_GET(url, headers).content
        if dialog.iscanceled(): return False
        dialog.update(66)
        fragment = re.findall('playeriframe".+?attr.+?src : "(.+?)"', html)
        for frags in fragment:
            pass
        frag = 'http://%s%s'%('veehd.com',frags)
        setCookie('http://veehd.com')
        html = net().http_GET(frag, headers).content
        va=re.search('iframe" src="([^"]+?)"',html)
        if va:
            poop='http://veehd.com'+va.group(1)
            headers = {'User-Agent': 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7','Referer':frag,'Cache-Control':'max-age=0'}
            setCookie(poop)
            html = net().http_GET(frag, headers).content
        r = re.search('"video/divx" src="(.+?)"', html)
        if r:
            stream_url = r.group(1)
        if not r:
            a = re.search('"url":"(.+?)"', html)
            if a:
                r=urllib.unquote(a.group(1))
                if r:
                    stream_url = r
                else:
                    logerror('***** VeeHD - File Not Found')
                    xbmc.executebuiltin("XBMC.Notification(File Not Found,VeeHD,2000)")
                    return False
            if not a:
                a = re.findall('href="(.+?)">', html)
                stream_url = a[1]
        if dialog.iscanceled(): return False
        dialog.update(100)
        return stream_url
    except Exception:
        xbmc.executebuiltin("XBMC.Notification(Resolver Failed,VeeHD,2000)")


                


def resolve_epicshare(url):
    try:
        puzzle_img = os.path.join(datapath, "epicshare_puzzle.png")
        #Show dialog box so user knows something is happening
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving Phoenix  Link...')
        dialog.update(0)
        
        print 'EpicShare - Phoenix Requesting GET URL: %s' % url
        html = net().http_GET(url).content
        if dialog.iscanceled(): return False
        dialog.update(50)
        
        #Check page for any error msgs
        if re.search('This server is in maintenance mode', html):
            logerror('***** EpicShare - Site reported maintenance mode')
            xbmc.executebuiltin("XBMC.Notification(File is currently unavailable,EpicShare in maintenance,2000)")  
            return False
        if re.search('<b>File Not Found</b>', html):
            logerror('***** EpicShare - File not found')
            xbmc.executebuiltin("XBMC.Notification(File Not Found,EpicShare,2000)")
            return False

        data = {}
        r = re.findall(r'type="hidden" name="(.+?)" value="(.+?)">', html)

        if r:
            for name, value in r:
                data[name] = value
        else:
            logerror('***** EpicShare - Cannot find data values')
            raise Exception('Unable to resolve EpicShare Link')
        
        #Check for SolveMedia Captcha image
        solvemedia = re.search('<iframe src="(http://api.solvemedia.com.+?)"', html)

        if solvemedia:
           dialog.close()
           html = net().http_GET(solvemedia.group(1)).content
           hugekey=re.search('id="adcopy_challenge" value="(.+?)">', html).group(1)
           open(puzzle_img, 'wb').write(net().http_GET("http://api.solvemedia.com%s" % re.search('<img src="(.+?)"', html).group(1)).content)
           img = xbmcgui.ControlImage(450,15,400,130, puzzle_img)
           wdlg = xbmcgui.WindowDialog()
           wdlg.addControl(img)
           wdlg.show()
        
           kb = xbmc.Keyboard('', 'Type the letters in the image', False)
           kb.doModal()
           capcode = kb.getText()
   
           if (kb.isConfirmed()):
               userInput = kb.getText()
               if userInput != '':
                   solution = kb.getText()
               elif userInput == '':
                   Notify('big', 'No text entered', 'You must enter text in the image to access video', '')
                   return False
           else:
               return False
               
           wdlg.close()
           dialog.create('Resolving', 'Resolving Phoenix  Link...') 
           dialog.update(50)
           if solution:
               data.update({'adcopy_challenge': hugekey,'adcopy_response': solution})

        print 'EpicShare - Phoenix Requesting POST URL: %s' % url
        html = net().http_POST(url, data).content
        if dialog.iscanceled(): return False
        dialog.update(100)
        
        link = re.search('<a id="lnk_download"  href=".+?product_download_url=(.+?)">', html)
        if link:
            print 'Phoenix EpicShare Link Found: %s' % link.group(1)
            return link.group(1)
        else:
            xbmc.executebuiltin("XBMC.Notification(Resolver Failed,Epic Share,2000)")
        
    except Exception:
        xbmc.executebuiltin("XBMC.Notification(Resolver Failed,Epic Share,2000)")
    finally:
        dialog.close()

def resolve_lemupload(url):
    try:
        #Show dialog box so user knows something is happening
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving Phoenix  Link...')       
        dialog.update(0)
#         
        print 'LemUpload - Phoenix Requesting GET URL: %s' % url
        html = net().http_GET(url).content
        if dialog.iscanceled(): return False
        dialog.update(50)
        
        #Check page for any error msgs
        if re.search('<b>File Not Found</b>', html):
            print '***** LemUpload - File Not Found'
            xbmc.executebuiltin("XBMC.Notification(File Not Found,LemUpload,2000)")
            return False
        
        if re.search('This server is in maintenance mode', html):
            print '***** LemUpload - Server is in maintenance mode'
            xbmc.executebuiltin("XBMC.Notification(Site In Maintenance,LemUpload,2000)")
            return False

        filename = re.search('<h2>(.+?)</h2>', html).group(1)
        extension = re.search('(\.[^\.]*$)', filename).group(1)
        guid = re.search('http://lemuploads.com/(.+)$', url).group(1)
        vid_embed_url = 'http://lemuploads.com/vidembed-%s%s' % (guid, extension)
        request = urllib2.Request(vid_embed_url)
        request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36')
        request.add_header('Referer', url)
        response = urllib2.urlopen(request)
        if dialog.iscanceled(): return False
        dialog.update(100)
        link = response.geturl()
        if link:
            redirect_url = re.search('(http://.+?)video', link)
            if redirect_url:
                link = redirect_url.group(1) + filename
            print 'Phoenix LemUpload Link Found: %s' % link
            return  link
        else:
            
            raise Exception('Unable to resolve LemUpload Link')

    except Exception:
        xbmc.executebuiltin("XBMC.Notification(Resolver Failed,Lem Upload,2000)")
    finally:
        dialog.close()
        
def resolve_hugefiles(url):
    import jsunpack
    try:
        import time
        puzzle_img = os.path.join(datapath, "hugefiles_puzzle.png")
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving Phoenix  Link...')       
        dialog.update(0)
        html = net().http_GET(url).content
        r = re.findall('File Not Found',html)
        if r:
            xbmc.log('Phoenix: Resolve HugeFiles - File Not Found or Removed', xbmc.LOGERROR)
            xbmc.executebuiltin("XBMC.Notification(File Not Found or Removed,HugeFiles,2000)")
            return False
        data = {}
        r = re.findall(r'type="hidden" name="(.+?)"\s* value="?(.+?)">', html)
        for name, value in r:
            data[name] = value
            data.update({'method_free':'Free Download'})
        if data['fname'] and re.search('\.(rar|zip)$', data['fname'], re.I):
            dialog.update(100)
            logerror('Phoenix: Resolve HugeFiles - No Video File Found')
            xbmc.executebuiltin("XBMC.Notification(No Video File Found,HugeFiles,2000)")
            return False
        if dialog.iscanceled(): return False
        dialog.update(33)
        #Check for SolveMedia Captcha image
        solvemedia = re.search('<iframe src="(http://api.solvemedia.com.+?)"', html)
        recaptcha = re.search('<script type="text/javascript" src="(http://www.google.com.+?)">', html)
    
        if solvemedia:
            html = net().http_GET(solvemedia.group(1)).content
            hugekey=re.search('id="adcopy_challenge" value="(.+?)">', html).group(1)
            open(puzzle_img, 'wb').write(net().http_GET("http://api.solvemedia.com%s" % re.search('img src="(.+?)"', html).group(1)).content)
            img = xbmcgui.ControlImage(450,15,400,130, puzzle_img)
            wdlg = xbmcgui.WindowDialog()
            wdlg.addControl(img)
            wdlg.show()
            
            xbmc.sleep(3000)
    
            kb = xbmc.Keyboard('', 'Type the letters in the image', False)
            kb.doModal()
            capcode = kb.getText()
       
            if (kb.isConfirmed()):
                userInput = kb.getText()
                if userInput != '':
                    solution = kb.getText()
                elif userInput == '':
                    xbmc.executebuiltin("XBMC.Notification(No text entered, You must enter text in the image to access video,2000)")
                    return False
            else:
                return False
                   
            wdlg.close()
            dialog.update(66)
            if solution:
                data.update({'adcopy_challenge': hugekey,'adcopy_response': solution})

        elif recaptcha:
            html = net().http_GET(recaptcha.group(1)).content
            part = re.search("challenge \: \\'(.+?)\\'", html)
            captchaimg = 'http://www.google.com/recaptcha/api/image?c='+part.group(1)
            img = xbmcgui.ControlImage(450,15,400,130,captchaimg)
            wdlg = xbmcgui.WindowDialog()
            wdlg.addControl(img)
            wdlg.show()
        
            time.sleep(3)
        
            kb = xbmc.Keyboard('', 'Type the letters in the image', False)
            kb.doModal()
            capcode = kb.getText()
        
            if (kb.isConfirmed()):
                userInput = kb.getText()
                if userInput != '':
                    solution = kb.getText()
                elif userInput == '':
                    raise Exception ('You must enter text in the image to access video')
            else:
                raise Exception ('Captcha Error')
            wdlg.close()
            dialog.update(66)
            data.update({'recaptcha_challenge_field':part.group(1),'recaptcha_response_field':solution})

        else:
            captcha = re.compile("left:(\d+)px;padding-top:\d+px;'>&#(.+?);<").findall(html)
            result = sorted(captcha, key=lambda ltr: int(ltr[0]))
            solution = ''.join(str(int(num[1])-48) for num in result)
            dialog.update(66)
            data.update({'code':solution})
        html = net().http_POST(url, data).content
        if dialog.iscanceled(): return False
        if 'reached the download-limit' in html:
            
            xbmc.executebuiltin("XBMC.Notification(Daily Limit Reached,HugeFiles,2000)")
            return False
        r = re.findall('var fileUrl = "([^"]+)"', html, re.DOTALL + re.IGNORECASE)
        if r:
            dialog.update(100)
            return r[0]
        if not r:
            sPattern = '''<div id="player_code">.*?<script type='text/javascript'>(eval.+?)</script>'''
            jpack = re.findall(sPattern, html, re.DOTALL|re.I)
            if jpack:
                dialog.update(100)
                sUnpacked = jsunpack.unpack(jpack[0])
                sUnpacked = sUnpacked.replace("\\'","")
                r = re.findall('file,(.+?)\)\;s1',sUnpacked)
                if not r:
                  r = re.findall('"src"value="(.+?)"/><embed',sUnpacked)
                return r[0]
            else:
                logerror('***** HugeFiles - Cannot find final link')
                raise Exception('Unable to resolve HugeFiles Link')
    except Exception:
        xbmc.executebuiltin("XBMC.Notification(Resolver Failed,Huge Files,2000)")        


def resolve_billionuploads(url, filename):
    try:        
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving Phoenix  Link...')  
        dialog.update(0)
        url = re.sub('(?i)^(.*?\.com/.+?)/.*','\\1',url)
        print 'Phoenix BillionUploads - Requesting GET URL: %s' % url
                   
        cookie_file = os.path.join(os.path.join(datapaths,'Cookies'), 'billionuploads.cookies')
        #cookie_file = os.path.join(cookiejar,'billionuploads.cookies')
        cj = cookielib.LWPCookieJar()
        if os.path.exists(cookie_file):
            try: cj.load(cookie_file,True)
            except: cj.save(cookie_file,True)
        else: cj.save(cookie_file,True)

        normal = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        headers = [
            ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:25.0) Gecko/20100101 Firefox/25.0'),
            ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
            ('Accept-Language', 'en-US,en;q=0.5'),
            ('Accept-Encoding', ''),
            ('DNT', '1'),
            ('Connection', 'keep-alive'),
            ('Pragma', 'no-cache'),
            ('Cache-Control', 'no-cache')
        ]
        normal.addheaders = headers
        class NoRedirection(urllib2.HTTPErrorProcessor):
            # Stop Urllib2 from bypassing the 503 page.
            def http_response(self, request, response):
                code, msg, hdrs = response.code, response.msg, response.info()
                return response
            https_response = http_response
        opener = urllib2.build_opener(NoRedirection, urllib2.HTTPCookieProcessor(cj))
        opener.addheaders = normal.addheaders
        response = opener.open(url).read()
        decoded = re.search('(?i)var z="";var b="([^"]+?)"', response)
        if decoded:
            decoded = decoded.group(1)
            z = []
            for i in range(len(decoded)/2):
                z.append(int(decoded[i*2:i*2+2],16))
            decoded = ''.join(map(unichr, z))
            incapurl = re.search('(?i)"GET","/_Incapsula_Resource[^"]+?"', decoded)
            if incapurl:
                incapurl = 'http://billionuploads.com'+incapurl.group(1)
                opener.open(incapurl)
                cj.save(cookie_file,True)
                response = opener.open(url).read()
        captcha = re.search('(?i)<iframe src="/_Incapsula_Resource[^"]+?"', response)
        if captcha:
            captcha = 'http://billionuploads.com'+captcha.group(1)
            opener.addheaders.append(('Referer', url))
            response = opener.open(captcha).read()
            formurl = 'http://billionuploads.com'+re.search('(?i)<form action="/_Incapsula_Resource[^"]+?"', response).group(1)
            resource = re.search('(?i)src=" /_Incapsula_Resource[^"]+?"', response)
            if resource:
                import random
                resourceurl = 'http://billionuploads.com'+resource.group(1) + str(random.random())
                opener.open(resourceurl)
            recaptcha = re.search('(?i)<script type="text/javascript" src="(https://www.google.com/recaptcha/api[^"]+?)"', response)
            if recaptcha:
                response = opener.open(recaptcha.group(1)).read()
                challenge = re.search('''(?i)challenge : '([^']+?)',''', response)
                if challenge:
                    challenge = challenge.group(1)
                    captchaimg = 'https://www.google.com/recaptcha/api/image?c=' + challenge
#                     site = re.search('''(?i)site : '([^']+?)',''', response).group(1)
#                     reloadurl = 'https://www.google.com/recaptcha/api/reload?c=' + challenge + '&' + site + '&reason=[object%20MouseEvent]&type=image&lang=en'
                    img = xbmcgui.ControlImage(550,15,300,57,captchaimg)
                    wdlg = xbmcgui.WindowDialog()
                    wdlg.addControl(img)
                    wdlg.show()
                    
                    kb = xbmc.Keyboard('', 'Please enter the text in the image', False)
                    kb.doModal()
                    capcode = kb.getText()
                    if (kb.isConfirmed()):
                        userInput = kb.getText()
                        if userInput != '': capcode = kb.getText()
                        elif userInput == '':
                            logerror('BillionUploads - Image-Text not entered')
                            xbmc.executebuiltin("XBMC.Notification(Image-Text not entered.,BillionUploads,2000)")              
                            return None
                    else: return None
                    wdlg.close()
                    captchadata = {}
                    captchadata['recaptcha_challenge_field'] = challenge
                    captchadata['recaptcha_response_field'] = capcode
                    opener.addheaders = headers
                    opener.addheaders.append(('Referer', captcha))
                    resultcaptcha = opener.open(formurl,urllib.urlencode(captchadata)).info()
                    opener.addheaders = headers
                    response = opener.open(url).read()
                    
        ga = re.search('(?i)"text/javascript" src="(/ga[^"]+?)"', response)
        if ga:
            jsurl = 'http://billionuploads.com'+ga.group(1)
            p  = "p=%7B%22appName%22%3A%22Netscape%22%2C%22platform%22%3A%22Win32%22%2C%22cookies%22%3A1%2C%22syslang%22%3A%22en-US%22"
            p += "%2C%22userlang%22%3A%22en-US%22%2C%22cpu%22%3A%22WindowsNT6.1%3BWOW64%22%2C%22productSub%22%3A%2220100101%22%7D"
            opener.open(jsurl, p)
            response = opener.open(url).read()
#         pid = re.search('(?i)PID=([^"]+?)"', response)
#         if pid:
#             normal.addheaders += [('Cookie','D_UID='+pid.group(1)+';')]
#             opener.addheaders = normal.addheaders
        if re.search('(?i)url=/distil_r_drop.html', response) and filename:
            url += '/' + filename
            response = normal.open(url).read()
        jschl=re.compile('name="jschl_vc" value="(.+?)"/>').findall(response)
        if jschl:
            jschl = jschl[0]    
            maths=re.compile('value = (.+?);').findall(response)[0].replace('(','').replace(')','')
            domain_url = re.compile('(https?://.+?/)').findall(url)[0]
            domain = re.compile('https?://(.+?)/').findall(domain_url)[0]
            final= normal.open(domain_url+'cdn-cgi/l/chk_jschl?jschl_vc=%s&jschl_answer=%s'%(jschl,eval(maths)+len(domain))).read()
            html = normal.open(url).read()
        else: html = response
        
        if dialog.iscanceled(): return None
        dialog.update(25)
        
        #Check page for any error msgs            
        if re.search('This server is in maintenance mode', html):
            logerror('***** BillionUploads - Site reported maintenance mode')
            xbmc.executebuiltin("XBMC.Notification(File is currently unavailable,BillionUploads in maintenance,2000)")                                
            return None
        if re.search('File Not Found', html, re.I):
            logerror('***** BillionUploads - File Not Found')
            xbmc.executebuiltin("XBMC.Notification(File Not Found,BillionUploads,2000)")
            return False

        data = {}
        r = re.findall(r'type="hidden" name="(.+?)" value="(.*?)">', html)
        for name, value in r: data[name] = value
        if not data:
            logerror('Phoenix: Resolve BillionUploads - No Data Found')
            xbmc.executebuiltin("XBMC.Notification(No Data Found,BillionUploads,2000)")               
            return None
        
        if dialog.iscanceled(): return None
        
        captchaimg = re.search('<img src="((?:http://|www\.)?BillionUploads.com/captchas/.+?)"', html)            
        if captchaimg:

            img = xbmcgui.ControlImage(550,15,240,100,captchaimg.group(1))
            wdlg = xbmcgui.WindowDialog()
            wdlg.addControl(img)
            wdlg.show()
            
            kb = xbmc.Keyboard('', 'Please enter the text in the image', False)
            kb.doModal()
            capcode = kb.getText()
            if (kb.isConfirmed()):
                userInput = kb.getText()
                if userInput != '': capcode = kb.getText()
                elif userInput == '':
                    showpopup('BillionUploads','[B]You must enter the text from the image to access video[/B]',5000, elogo)
                    return None
            else: return None
            wdlg.close()
            
            data.update({'code':capcode})
        
        if dialog.iscanceled(): return None
        dialog.update(50)
        
        data.update({'submit_btn':''})
        enc_input = re.compile('decodeURIComponent\("(.+?)"\)').findall(html)
        if enc_input:
            dec_input = urllib2.unquote(enc_input[0])
            r = re.findall(r'type="hidden" name="(.+?)" value="(.*?)">', dec_input)
            for name, value in r:
                data[name] = value
        extradata = re.compile("append\(\$\(document.createElement\('input'\)\).attr\('type','hidden'\).attr\('name','(.*?)'\).val\((.*?)\)").findall(html)
        if extradata:
            for attr, val in extradata:
                if 'source="self"' in val:
                    val = re.compile('<textarea[^>]*?source="self"[^>]*?>([^<]*?)<').findall(html)[0]
                data[attr] = val.strip("'")
        r = re.findall("""'input\[name="([^"]+?)"\]'\)\.remove\(\)""", html)
        
        for name in r: del data[name]
        
        normal.addheaders.append(('Referer', url))
        html = normal.open(url, urllib.urlencode(data)).read()
        cj.save(cookie_file,True)
        
        if dialog.iscanceled(): return None
        dialog.update(75)
        
        def custom_range(start, end, step):
            while start <= end:
                yield start
                start += step

        def checkwmv(e):
            s = ""
            i=[]
            u=[[65,91],[97,123],[48,58],[43,44],[47,48]]
            for z in range(0, len(u)):
                for n in range(u[z][0],u[z][1]):
                    i.append(chr(n))
            t = {}
            for n in range(0, 64): t[i[n]]=n
            for n in custom_range(0, len(e), 72):
                a=0
                h=e[n:n+72]
                c=0
                for l in range(0, len(h)):            
                    f = t.get(h[l], 'undefined')
                    if f == 'undefined': continue
                    a = (a<<6) + f
                    c = c + 6
                    while c >= 8:
                        c = c - 8
                        s = s + chr( (a >> c) % 256 )
            return s

        dll = re.compile('<input type="hidden" id="dl" value="(.+?)">').findall(html)
        if dll:
            dl = dll[0].split('GvaZu')[1]
            dl = checkwmv(dl);
            dl = checkwmv(dl);
        else:
            alt = re.compile('<source src="([^"]+?)"').findall(html)
            if alt:
                dl = alt[0]
            else:
                logerror('Phoenix: Resolve BillionUploads - No Video File Found')
                xbmc.executebuiltin("XBMC.Notification(No Video File Found,BillionUploads,2000)")
                return None
        
        if dialog.iscanceled(): return None
        dialog.update(100)                    

        return dl
        
    except Exception, e:
        logerror('BillionUploads - Exception occured: %s' % e)
        #raise ResolverError(str(e),"BillionUploads")
        return None
    finally:
        dialog.close()


        

def LIVERESOLVE(name,url,thumb):
         print "THUMBNAIL IS " +thumb
         params = {'url':url, 'name':name, 'thumb':thumb}
         addon.add_video_item(params, {'title':name}, img=thumb)
         liz=xbmcgui.ListItem(name, iconImage=thumb, thumbnailImage=thumb)
         xbmc.Player ().play(str(url), liz, False)
         return   

               
#########################Blazetamer's VeeHD  Module########################################




def VHDLOGIN():
    username = settings.getSetting('vhd_user')
    password = settings.getSetting('vhd_pass')    
    header_dict = {}
    header_dict['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    header_dict['Connection'] = 'keep-alive'
    header_dict['Content-Type'] = 'application/x-www-form-urlencoded'
    header_dict['Host'] = 'veehd.com'
    header_dict['Referer'] = 'http://veehd/'
    header_dict['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36'    
    form_data = {'ref':'http://veehd.com/login','uname':username, 'pword':password,'submit':'Login', 'terms':'on','remember_me':'on'}
    net.set_cookies(cookiejar)
    login = net.http_POST('http://veehd/', form_data=form_data, headers=header_dict)
    net.save_cookies(cookiejar)
    link = net.http_GET('http://veehd.com').content
    logincheck=re.compile('<h3><a href="/dashboard">My (.+?)</a></h3>').findall(link)
    for nolog in logincheck:
                    print 'Login Check Return is ' + nolog
                    if 'Dashboard' in nolog :
                        LogNotify('Login Failed at VeeHD', 'Check settings', '5000', '')
                        return True
    else:
                        LogNotify('Welcome Back ' + username, 'Enjoy your stay!', '5000', '')
                        net.save_cookies(cookiejar)
                        return False
  

        
def VHDSTARTUP():
        username = settings.getSetting('vhd_user')
        password = settings.getSetting('vhd_pass')
        cookiejar = addon.get_profile()
        cookiejar = os.path.join(cookiejar,'cookies.lwp')
        if username is '' or password is '':
                dialog = xbmcgui.Dialog()
                ok = dialog.ok('Username or Password Not Set', '            Please Choose VeeHD Account Tab and Set')
                if ok:
                        LogNotify('VeeHD Account Tab ', 'Please set Username & Password!', '5000', '')        
                        print 'YOU HAVE NOT SET THE USERNAME OR PASSWORD!'
                        addon.show_settings()
        


        VHDLOGIN()      
                       
        
#************************End Login**************************************
