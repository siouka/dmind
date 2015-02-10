# -*- coding: utf-8 -*-

'''
    Genesis Add-on
    Copyright (C) 2015 lambda

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import urllib,urllib2,urlparse,re,os,xbmc,xbmcgui,xbmcaddon,xbmcvfs

try:
    import CommonFunctions as common
except:
    import commonfunctionsdummy as common
try:
    import json
except:
    import simplejson as json


def get(url):
    pz = premiumize(url)
    if not pz == None: return pz
    rd = realdebrid(url)
    if not rd == None: return rd

    try:
        u = None
        u = urlparse.urlparse(url).netloc
        u = u.replace('www.', '').replace('embed.', '')
        u = u.lower()
    except:
        pass

    if u == '180upload.com': url = _180upload(url)
    elif u == 'allmyvideos.net': url = allmyvideos(url)
    elif u == 'bestreams.net': url = bestreams(url)
    elif u == 'billionuploads.com': url = billionuploads(url)
    elif u == 'cloudyvideos.com': url = cloudyvideos(url)
    elif u == 'cloudzilla.to': url = cloudzilla(url)
    elif u == 'daclips.in': url = daclips(url)
    elif u == 'datemule.com': url = datemule(url)
    elif u == 'divxstage.eu': url = coolcdn(url)
    elif u == 'divxstage.to': url = coolcdn(url)
    elif u == 'fastvideo.in': url = fastvideo(url)
    elif u == 'filecloud.io': url = filecloud(url)
    elif u == 'filehoot.com': url = filehoot(url)
    elif u == 'filenuke.com': url = filenuke(url)
    elif u == 'docs.google.com': url = googledocs(url)
    elif u == 'plus.google.com': url = googleplus(url)
    elif u == 'gorillavid.in': url = gorillavid(url)
    elif u == 'gorillavid.com': url = gorillavid(url)
    elif u == 'grifthost.com': url = grifthost(url)
    elif u == 'hostingbulk.com': url = hostingbulk(url)
    elif u == 'hugefiles.net': url = hugefiles(url)
    elif u == 'ipithos.to': url = ipithos(url)
    elif u == 'ishared.eu': url = ishared(url)
    elif u == 'kingfiles.net': url = kingfiles(url)
    elif u == 'my.mail.ru': url = mailru(url)
    elif u == 'mail.ru': url = mailru(url)
    elif u == 'mightyupload.com': url = mightyupload(url)
    elif u == 'mooshare.biz': url = mooshare(url)
    elif u == 'movdivx.com': url = movdivx(url)
    elif u == 'movpod.in': url = movpod(url)
    elif u == 'movpod.net': url = movpod(url)
    elif u == 'movreel.com': url = movreel(url)
    elif u == 'movshare.net': url = coolcdn(url)
    elif u == 'movzap.com': url = hostingbulk(url)
    elif u == 'mrfile.me': url = mrfile(url)
    elif u == 'nosvideo.com': url = nosvideo(url)
    elif u == 'novamov.com': url = coolcdn(url)
    elif u == 'nowvideo.sx': url = coolcdn(url)
    elif u == 'played.to': url = played(url)
    elif u == 'primeshare.tv': url = primeshare(url)
    elif u == 'promptfile.com': url = promptfile(url)
    elif u == 'sharerepo.com': url = sharerepo(url)
    elif u == 'sharesix.com': url = filenuke(url)
    elif u == 'stagevu.com': url = stagevu(url)
    elif u == 'streamcloud.eu': url = streamcloud(url)
    elif u == 'streamin.to': url = streamin(url)
    elif u == 'thefile.me': url = thefile(url)
    elif u == 'thevideo.me': url = thevideo(url)
    elif u == 'uploadc.com': url = uploadc(url)
    elif u == 'uploadrocket.net': url = uploadrocket(url)
    elif u == 'v-vids.com': url = v_vids(url)
    elif u == 'vidbull.com': url = vidbull(url)
    elif u == 'videomega.tv': url = videomega(url)
    elif u == 'videoweed.es': url = coolcdn(url)
    elif u == 'vidspot.net': url = vidspot(url)
    elif u == 'vidto.me': url = vidto(url)
    elif u == 'vidzi.tv': url = vidzi(url)
    elif u == 'vimeo.com': url = vimeo(url)
    elif u == 'vk.com': url = vk(url)
    elif u == 'vodlocker.com': url = vodlocker(url)
    elif u == 'xvidstage.com': url = xvidstage(url)
    elif u == 'youtube.com': url = youtube(url)
    elif u == 'zalaa.com': url = uploadc(url)
    elif u == 'zettahost.tv': url = zettahost(url)

    return url


class getUrl(object):
    def __init__(self, url, close=True, proxy=None, post=None, mobile=False, referer=None, cookie=None, output='', timeout='10'):
        if not proxy == None:
            proxy_handler = urllib2.ProxyHandler({'http':'%s' % (proxy)})
            opener = urllib2.build_opener(proxy_handler, urllib2.HTTPHandler)
            opener = urllib2.install_opener(opener)
        if output == 'cookie' or not close == True:
            import cookielib
            cookie_handler = urllib2.HTTPCookieProcessor(cookielib.LWPCookieJar())
            opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
            opener = urllib2.install_opener(opener)
        if not post == None:
            request = urllib2.Request(url, post)
        else:
            request = urllib2.Request(url,None)
        if mobile == True:
            request.add_header('User-Agent', 'Mozilla/5.0 (iPhone; CPU; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7')
        else:
            request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:34.0) Gecko/20100101 Firefox/34.0')
        if not referer == None:
            request.add_header('Referer', referer)
        if not cookie == None:
            request.add_header('cookie', cookie)
        request.add_header('Accept-Language', 'en-US')
        response = urllib2.urlopen(request, timeout=int(timeout))
        if output == 'cookie':
            result = str(response.headers.get('Set-Cookie'))
        elif output == 'geturl':
            result = response.geturl()
        else:
            result = response.read()
        if close == True:
            response.close()
        self.result = result

def jsunpack(script):
    def __itoa(num, radix):
        result = ""
        while num > 0:
            result = "0123456789abcdefghijklmnopqrstuvwxyz"[num % radix] + result
            num /= radix
        return result

    def __unpack(p, a, c, k, e, d):
        while (c > 1):
            c = c -1
            if (k[c]):
                p = re.sub('\\b' + str(__itoa(c, a)) +'\\b', k[c], p)
        return p

    aSplit = script.split(";',")
    p = str(aSplit[0])
    aSplit = aSplit[1].split(",")
    a = int(aSplit[0])
    c = int(aSplit[1])
    k = aSplit[2].split(".")[0].replace("'", '').split('|')
    e = ''
    d = ''
    sUnpacked = str(__unpack(p, a, c, k, e, d))
    return sUnpacked.replace('\\', '')

def captcha(data):
    try:
        captcha = {}

        def get_response(response):
            try:
                dataPath = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo("profile"))
                i = os.path.join(dataPath.decode("utf-8"),'img')
                f = xbmcvfs.File(i, 'w')
                f.write(getUrl(response).result)
                f.close()
                f = xbmcgui.ControlImage(450,5,375,115, i)
                d = xbmcgui.WindowDialog()
                d.addControl(f)
                xbmcvfs.delete(i)
                d.show()
                xbmc.sleep(3000)
                t = 'Type the letters in the image'
                c = common.getUserInput(t, '')
                d.close()
                return c
            except:
                return

        solvemedia = common.parseDOM(data, "iframe", ret="src")
        solvemedia = [i for i in solvemedia if 'api.solvemedia.com' in i]

        if len(solvemedia) > 0:
            url = solvemedia[0]
            result = getUrl(url).result
            challenge = common.parseDOM(result, "input", ret="value", attrs = { "id": "adcopy_challenge" })[0]
            response = common.parseDOM(result, "iframe", ret="src")
            response += common.parseDOM(result, "img", ret="src")
            response = [i for i in response if '/papi/media' in i][0]
            response = 'http://api.solvemedia.com' + response
            response = get_response(response)
            captcha.update({'adcopy_challenge': challenge, 'adcopy_response': response})
            return captcha

        recaptcha = []
        if data.startswith('http://www.google.com'): recaptcha += [data]
        recaptcha += common.parseDOM(data, "script", ret="src", attrs = { "type": "text/javascript" })
        recaptcha = [i for i in recaptcha if 'http://www.google.com' in i]

        if len(recaptcha) > 0:
            url = recaptcha[0]
            result = getUrl(url).result
            challenge = re.compile("challenge\s+:\s+'(.+?)'").findall(result)[0]
            response = 'http://www.google.com/recaptcha/api/image?c=' + challenge
            response = get_response(response)
            captcha.update({'recaptcha_challenge_field': challenge, 'recaptcha_challenge': challenge, 'recaptcha_response_field': response, 'recaptcha_response': response})
            return captcha

        numeric = re.compile("left:(\d+)px;padding-top:\d+px;'>&#(.+?);<").findall(data)

        if len(numeric) > 0:
            result = sorted(numeric, key=lambda ltr: int(ltr[0]))
            response = ''.join(str(int(num[1])-48) for num in result)
            captcha.update({'code': response})
            return captcha

    except:
        return captcha



def premiumize(url):
    try:
        user = xbmcaddon.Addon().getSetting("premiumize_user")
        password = xbmcaddon.Addon().getSetting("premiumize_password")

        if (user == '' or password == ''): raise Exception()

        url = 'https://api.premiumize.me/pm-api/v1.php?method=directdownloadlink&params[login]=%s&params[pass]=%s&params[link]=%s' % (user, password, url)

        result = getUrl(url, close=False).result
        url = json.loads(result)['result']['location']
        return url
    except:
        return

def premiumize_hosts():
    try:
        user = xbmcaddon.Addon().getSetting("premiumize_user")
        password = xbmcaddon.Addon().getSetting("premiumize_password")

        if (user == '' or password == ''): raise Exception()

        pz = getUrl('https://api.premiumize.me/pm-api/v1.php?method=hosterlist&params[login]=%s&params[pass]=%s' % (user, password)).result
        pz = json.loads(pz)['result']['hosterlist']
        pz = [i.rsplit('.' ,1)[0].lower() for i in pz]
        return pz
    except:
        return

def realdebrid(url):
    try:
        user = xbmcaddon.Addon().getSetting("realdedrid_user")
        password = xbmcaddon.Addon().getSetting("realdedrid_password")

        if (user == '' or password == ''): raise Exception()

        login_data = urllib.urlencode({'user' : user, 'pass' : password})
        login_link = 'https://real-debrid.com/ajax/login.php?%s' % login_data
        result = getUrl(login_link, close=False).result
        result = json.loads(result)
        error = result['error']
        if not error == 0: raise Exception()

        url = 'https://real-debrid.com/ajax/unrestrict.php?link=%s' % url
        url = url.replace('filefactory.com/stream/', 'filefactory.com/file/')
        result = getUrl(url).result
        result = json.loads(result)
        url = result['generated_links'][0][-1]
        return url
    except:
        return

def realdebrid_hosts():
    try:
        rd = getUrl('https://real-debrid.com/api/hosters.php').result
        rd = json.loads('[%s]' % rd)
        rd = [i.rsplit('.' ,1)[0].lower() for i in rd]
        return rd
    except:
        return



def _180upload(url):
    try:
        url = re.compile('//.+?/([\w]+)').findall(url)[0]
        url = 'http://180upload.com/embed-%s.html' % url

        result = getUrl(url).result

        post = {}
        f = common.parseDOM(result, "form", attrs = { "id": "captchaForm" })[0]
        k = common.parseDOM(f, "input", ret="name", attrs = { "type": "hidden" })
        for i in k: post.update({i: common.parseDOM(f, "input", ret="value", attrs = { "name": i })[0]})
        post = urllib.urlencode(post)

        result = getUrl(url, post=post).result

        result = re.compile('(eval.*?\)\)\))').findall(result)[-1]
        result = jsunpack(result)

        url = re.compile("'file' *, *'(.+?)'").findall(result)
        url += re.compile("file *: *[\'|\"](.+?)[\'|\"]").findall(result)
        url += common.parseDOM(result, "embed", ret="src")
        url = 'http://' + url[-1].split('://', 1)[-1]
        return url
    except:
        return

def allmyvideos(url):
    try:
        url = url.replace('/embed-', '/')
        url = re.compile('//.+?/([\w]+)').findall(url)[0]
        url = 'http://allmyvideos.net/embed-%s.html' % url

        result = getUrl(url, mobile=True).result
        url = re.compile('"file" *: *"(http.+?)"').findall(result)[-1]
        return url
    except:
        return

def bestreams(url):
    try:
        url = url.replace('/embed-', '/')
        url = re.compile('//.+?/([\w]+)').findall(url)[0]
        url = 'http://bestreams.net/embed-%s.html' % url

        result = getUrl(url, mobile=True, referer=url).result
        url = re.compile('file *: *"(http.+?)"').findall(result)[-1]
        return url
    except:
        return

def billionuploads(url):
    try:
        import cookielib
        cj = cookielib.CookieJar()

        agent = 'Mozilla/5.0 (Windows NT 6.1; rv:34.0) Gecko/20100101 Firefox/34.0'
        base = 'http://billionuploads.com'

        class NoRedirection(urllib2.HTTPErrorProcessor):
            def http_response(self, request, response):
                return response

        opener = urllib2.build_opener(NoRedirection, urllib2.HTTPCookieProcessor(cj))
        opener.addheaders = [('User-Agent', agent)]
        response = opener.open(base)
        response = opener.open(base)
        result = response.read()

        z = []
        decoded = re.compile('(?i)var z="";var b="([^"]+?)"').findall(result)[0]
        for i in range(len(decoded)/2): z.append(int(decoded[i*2:i*2+2],16))
        decoded = ''.join(map(unichr, z))

        incapurl = re.compile('(?i)"GET","(/_Incapsula_Resource[^"]+?)"').findall(decoded)[0]
        incapurl = base + incapurl

        response = opener.open(incapurl)
        response = opener.open(url)
        result = response.read()

        post = {}
        f = common.parseDOM(result, "form", attrs = { "method": "post" })[-1]
        k = common.parseDOM(f, "input", ret="name", attrs = { "type": "hidden" })
        for i in k: post.update({i: common.parseDOM(f, "input", ret="value", attrs = { "name": i })[0]})
        post.update({'method_free': 'Download or watch'})
        post = urllib.urlencode(post)

        response = opener.open(url, post)
        result = response.read()
        response.close()

        url = common.parseDOM(result, "a", ret="href", attrs = { "class": "download" })[0]
        return url
    except:
        return

def cloudyvideos(url):
    try:
        result = getUrl(url).result

        post = {}
        f = common.parseDOM(result, "Form", attrs = { "name": "F1" })[-1]
        k = common.parseDOM(f, "input", ret="name", attrs = { "type": "hidden" })
        for i in k: post.update({i: common.parseDOM(f, "input", ret="value", attrs = { "name": i })[0]})
        post.update({'method_free': '', 'method_premium': ''})
        post = urllib.urlencode(post)

        import time
        request = urllib2.Request(url, post)

        for i in range(0, 4):
            try:
                response = urllib2.urlopen(request, timeout=5)
                result = response.read()
                response.close()
                btn = common.parseDOM(result, "input", ret="value", attrs = { "class": "graybt.+?" })[0]
                url = re.compile('href=[\'|\"](.+?)[\'|\"]><input.+?class=[\'|\"]graybt.+?[\'|\"]').findall(result)[0]
                return url
            except:
                time.sleep(1)
    except:
        return

def cloudzilla(url):
    try:
        url = url.replace('/share/file/', '/embed/')
        result = getUrl(url).result
        url = re.compile('var\s+vurl *= *"(http.+?)"').findall(result)[0]
        return url
    except:
        return

def coolcdn(url):
    try:
        netloc = urlparse.urlparse(url).netloc
        netloc = netloc.replace('www.', '').replace('embed.', '')
        netloc = netloc.lower()

        id = re.compile('//.+?/.+?/([\w]+)').findall(url)
        id += re.compile('//.+?/.+?v=([\w]+)').findall(url)
        id = id[0]

        url = 'http://embed.%s/embed.php?v=%s' % (netloc, id)

        result = getUrl(url).result

        key = re.compile('flashvars.filekey=(.+?);').findall(result)[-1]
        try: key = re.compile('\s+%s="(.+?)"' % key).findall(result)[-1]
        except: pass

        url = 'http://www.%s/api/player.api.php?key=%s&file=%s' % (netloc, key, id)
        result = getUrl(url).result

        url = re.compile('url=(.+?)&').findall(result)[0]
        return url
    except:
        return

def daclips(url):
    try:
        result = getUrl(url, mobile=True).result
        url = re.compile('file *: *"(http.+?)"').findall(result)[-1]
        return url
    except:
        return

def datemule(url):
    try:
        result = getUrl(url, mobile=True).result
        url = re.compile('file *: *"(http.+?)"').findall(result)[0]
        return url
    except:
        return

def fastvideo(url):
    try:
        url = url.replace('/embed-', '/')
        url = re.compile('//.+?/([\w]+)').findall(url)[0]
        url = 'http://fastvideo.in/embed-%s.html' % url

        result = getUrl(url, mobile=True, referer=url).result
        url = re.compile('file *: *"(http.+?)"').findall(result)[-1]
        return url
    except:
        return

def filecloud(url):
    try:
        result = getUrl(url, close=False).result
        result = getUrl('http://filecloud.io/download.html').result

        url = re.compile("__requestUrl\s+=\s+'(.+?)'").findall(result)[0]

        ukey = re.compile("'ukey'\s+:\s+'(.+?)'").findall(result)[0]
        __ab1 = re.compile("__ab1\s+=\s+(\d+);").findall(result)[0]
        ctype = re.compile("'ctype'\s+:\s+'(.+?)'").findall(result)[0]

        challenge = re.compile("__recaptcha_public\s+=\s+'(.+?)'").findall(result)[0]
        challenge = 'http://www.google.com/recaptcha/api/challenge?k=' + challenge

        post = {'ukey': ukey, '__ab1': str(__ab1), 'ctype': ctype}
        post.update(captcha(challenge))
        post = urllib.urlencode(post)

        result = getUrl(url, post=post).result
        result = getUrl('http://filecloud.io/download.html').result

        url = common.parseDOM(result, "a", ret="href", attrs = { "id": "downloadBtn" })[0]
        return url
    except:
        return

def filehoot(url):
    try:
        url = url.replace('/embed-', '/')
        url = re.compile('//.+?/([\w]+)').findall(url)[0]
        url = 'http://filehoot.com/embed-%s.html' % url

        result = getUrl(url, mobile=True, referer=url).result
        url = re.compile('file *: *"(http.+?)"').findall(result)[0]
        return url
    except:
        return

def filenuke(url):
    try:
        result = getUrl(url).result

        post = {}
        try: f = common.parseDOM(result, "form", attrs = { "method": "POST" })[0]
        except: f = ''
        k = common.parseDOM(f, "input", ret="name", attrs = { "type": "hidden" })
        for i in k: post.update({i: common.parseDOM(f, "input", ret="value", attrs = { "name": i })[0]})
        post.update({'method_free': 'Free', 'usr_login': '', 'op': 'download1', 'referer': url})
        post = urllib.urlencode(post)

        result = getUrl(url, post=post).result

        url = re.compile("var\s+lnk1 *= *'(http.+?)'").findall(result)[0]
        url += '|User-Agent=%s' % urllib.quote_plus('Mozilla/5.0 (Windows NT 6.1; rv:34.0) Gecko/20100101 Firefox/34.0')
        return url
    except:
        return

def google(url):
    try:
        if any(x in url for x in ['&itag=37&', '&itag=137&', '&itag=299&', '&itag=96&', '&itag=248&', '&itag=303&', '&itag=46&']): quality = '1080p'
        elif any(x in url for x in ['&itag=22&', '&itag=84&', '&itag=136&', '&itag=298&', '&itag=120&', '&itag=95&', '&itag=247&', '&itag=302&', '&itag=45&', '&itag=102&']): quality = 'HD'
        else: raise Exception()

        url = [{'quality': quality, 'url': url}]
        return url
    except:
        return

def googledocs(url):
    try:
        url = url.split('/preview', 1)[0]

        result = getUrl(url).result
        result = re.compile('"fmt_stream_map",(".+?")').findall(result)[0]
        result = json.loads(result)

        u = [i.split('|')[-1] for i in result.split(',')]

        url = []
        try: url += [[{'quality': '1080p', 'url': i} for i in u if any(x in i for x in ['&itag=37&', '&itag=137&', '&itag=299&', '&itag=96&', '&itag=248&', '&itag=303&', '&itag=46&'])][0]]
        except: pass
        try: url += [[{'quality': 'HD', 'url': i} for i in u if any(x in i for x in ['&itag=22&', '&itag=84&', '&itag=136&', '&itag=298&', '&itag=120&', '&itag=95&', '&itag=247&', '&itag=302&', '&itag=45&', '&itag=102&'])][0]]
        except: pass

        if url == []: return
        return url
    except:
        return

def googleplus(url):
    try:
        result = getUrl(url).result

        u = re.compile('"(http.+?videoplayback[?].+?)"').findall(result)
        u = [i.replace('\\u003d','=').replace('\\u0026','&') for i in u]

        d = []
        try: d += [[{'quality': '1080p', 'url': i} for i in u if any(x in i for x in ['&itag=37&', '&itag=137&', '&itag=299&', '&itag=96&', '&itag=248&', '&itag=303&', '&itag=46&'])][0]]
        except: pass
        try: d += [[{'quality': 'HD', 'url': i} for i in u if any(x in i for x in ['&itag=22&', '&itag=84&', '&itag=136&', '&itag=298&', '&itag=120&', '&itag=95&', '&itag=247&', '&itag=302&', '&itag=45&', '&itag=102&'])][0]]
        except: pass

        url = []
        for i in d:
            try: url.append({'quality': i['quality'], 'url': getUrl(i['url'], output='geturl').result})
            except: pass

        if url == []: return
        return url
    except:
        return

def gorillavid(url):
    try:
        url = url.replace('/embed-', '/')
        url = re.compile('//.+?/([\w]+)').findall(url)[0]
        url = 'http://gorillavid.in/embed-%s.html' % url

        result = getUrl(url, mobile=True).result
        url = re.compile('file *: *"(http.+?)"').findall(result)[-1]

        request = urllib2.Request(url)
        response = urllib2.urlopen(request, timeout=30)
        response.close()

        type = str(response.info()["Content-Type"])
        if type == 'text/html': raise Exception()

        return url
    except:
        return

def grifthost(url):
    try:
        url = url.replace('/embed-', '/')
        url = re.compile('//.+?/([\w]+)').findall(url)[0]
        url = 'http://grifthost.com/embed-%s.html' % url

        result = getUrl(url).result

        try:
            post = {}
            f = common.parseDOM(result, "Form", attrs = { "method": "POST" })[0]
            f = f.replace('"submit"', '"hidden"')
            k = common.parseDOM(f, "input", ret="name", attrs = { "type": "hidden" })
            for i in k: post.update({i: common.parseDOM(f, "input", ret="value", attrs = { "name": i })[0]})
            post = urllib.urlencode(post)
            result = getUrl(url, post=post).result
        except:
            pass

        result = re.compile('(eval.*?\)\)\))').findall(result)[-1]
        result = jsunpack(result)

        url = re.compile("'file' *, *'(.+?)'").findall(result)
        url += re.compile("file *: *[\'|\"](.+?)[\'|\"]").findall(result)
        url += common.parseDOM(result, "embed", ret="src")
        url = 'http://' + url[-1].split('://', 1)[-1]
        return url
    except:
        return

def hostingbulk(url):
    try:
        result = getUrl(url, mobile=True).result

        result = re.compile('(eval.*?\)\)\))').findall(result)[-1]
        result = jsunpack(result)

        url = re.compile("'file' *, *'(.+?)'").findall(result)
        url += re.compile("file *: *[\'|\"](.+?)[\'|\"]").findall(result)
        url += common.parseDOM(result, "embed", ret="src")
        url = 'http://' + url[-1].split('://', 1)[-1]
        return url
    except:
        return

def hugefiles(url):
    try:
        result = getUrl(url).result

        post = {}
        f = common.parseDOM(result, "Form", attrs = { "action": "" })
        k = common.parseDOM(f, "input", ret="name", attrs = { "type": "hidden" })
        for i in k: post.update({i: common.parseDOM(f, "input", ret="value", attrs = { "name": i })[0]})
        post.update({'method_free': 'Free Download'})
        post.update(captcha(result))
        post = urllib.urlencode(post)

        result = getUrl(url, post=post).result

        post = {}
        f = common.parseDOM(result, "Form", attrs = { "action": "" })
        k = common.parseDOM(f, "input", ret="name", attrs = { "type": "hidden" })
        for i in k: post.update({i: common.parseDOM(f, "input", ret="value", attrs = { "name": i })[0]})
        post.update({'method_free': 'Free Download'})
        post = urllib.urlencode(post)

        u = getUrl(url, output='geturl', post=post).result
        if not url == u: return u
    except:
        return

def ipithos(url):
    try:
        url = url.replace('/embed-', '/')
        url = re.compile('//.+?/([\w]+)').findall(url)[0]
        url = 'http://ipithos.to/embed-%s.html' % url

        result = getUrl(url, mobile=True).result

        result = re.compile('(eval.*?\)\)\))').findall(result)[-1]
        result = jsunpack(result)

        url = re.compile("'file' *, *'(.+?)'").findall(result)
        url += re.compile("file *: *[\'|\"](.+?)[\'|\"]").findall(result)
        url += common.parseDOM(result, "embed", ret="src")
        url = 'http://' + url[-1].split('://', 1)[-1]
        return url
    except:
        return

def ishared(url):
    try:
        result = getUrl(url).result
        url = re.compile('path *: *"(http.+?)"').findall(result)[-1]
        return url
    except:
        return

def kingfiles(url):
    try:
        result = getUrl(url).result

        post = {}
        f = common.parseDOM(result, "Form", attrs = { "action": "" })[0]
        k = common.parseDOM(f, "input", ret="name", attrs = { "type": "hidden" })
        for i in k: post.update({i: common.parseDOM(f, "input", ret="value", attrs = { "name": i })[0]})
        post.update({'method_free': ' '})
        post = urllib.urlencode(post)

        result = getUrl(url, post=post).result

        post = {}
        f = common.parseDOM(result, "Form", attrs = { "action": "" })[0]
        k = common.parseDOM(f, "input", ret="name", attrs = { "type": "hidden" })
        for i in k: post.update({i: common.parseDOM(f, "input", ret="value", attrs = { "name": i })[0]})
        post.update({'method_free': ' '})
        post.update(captcha(result))
        post = urllib.urlencode(post)

        result = getUrl(url, post=post).result

        url = re.compile("var\s+download_url *= *'(.+?)'").findall(result)[0]
        return url
    except:
        return

def mailru(url):
    try:
        url = url.replace('/my.mail.ru/video/', '/api.video.mail.ru/videos/embed/')
        url = url.replace('/videoapi.my.mail.ru/', '/api.video.mail.ru/')
        result = getUrl(url).result

        url = re.compile('"metadataUrl" *: *"(.+?)"').findall(result)[0]
        cookie = getUrl(url, output='cookie').result
        h = "|Cookie=%s" % urllib.quote(cookie)

        result = getUrl(url).result
        result = json.loads(result)
        result = result['videos']

        url = []
        url += [{'quality': '1080p', 'url': i['url'] + h} for i in result if i['key'] == '1080p']
        url += [{'quality': 'HD', 'url': i['url'] + h} for i in result if i['key'] == '720p']
        url += [{'quality': 'SD', 'url': i['url'] + h} for i in result if not (i['key'] == '1080p' or i ['key'] == '720p')]

        if url == []: return
        return url
    except:
        return

def mightyupload(url):
    try:
        url = url.replace('/embed-', '/')
        url = re.compile('//.+?/([\w]+)').findall(url)[0]
        url = 'http://www.mightyupload.com/embed-%s.html' % url

        result = getUrl(url, mobile=True).result

        url = re.compile("file *: *'(.+?)'").findall(result)

        result = re.compile('(eval.*?\)\)\))').findall(result)[-1]
        result = jsunpack(result)

        url += re.compile("'file' *, *'(.+?)'").findall(result)
        url += re.compile("file *: *[\'|\"](.+?)[\'|\"]").findall(result)
        url += common.parseDOM(result, "embed", ret="src")
        url = 'http://' + url[-1].split('://', 1)[-1]
        return url
    except:
        return

def mooshare(url):
    try:
        url = url.replace('/embed-', '/')
        url = re.compile('//.+?/([\w]+)').findall(url)[0]
        url = 'http://mooshare.biz/embed-%s.html?play=1&confirm=Close+Ad+and+Watch+as+Free+User' % url

        result = getUrl(url, referer=url).result
        url = re.compile('file *: *"(http.+?)"').findall(result)[-1]
        return url
    except:
        return

def movdivx(url):
    try:
        url = re.compile('//.+?/([\w]+)').findall(url)[0]
        url = 'http://www.movdivx.com/%s' % url
 
        result = getUrl(url).result

        post = {}
        f = common.parseDOM(result, "Form", attrs = { "name": "myForm" })[0]
        k = common.parseDOM(f, "input", ret="name", attrs = { "type": "hidden" })
        for i in k: post.update({i: common.parseDOM(f, "input", ret="value", attrs = { "name": i })[0]})
        post.update({'method_free': 'Continue to Stream'})
        post = urllib.urlencode(post)

        result = getUrl(url, post=post).result

        result = re.compile('(eval.*?\)\)\))').findall(result)[-1]
        result = jsunpack(result)

        url = re.compile("'file' *, *'(.+?)'").findall(result)
        url += re.compile("file *: *[\'|\"](.+?)[\'|\"]").findall(result)
        url += common.parseDOM(result, "embed", ret="src")
        url = 'http://' + url[-1].split('://', 1)[-1]
        return url
    except:
        return

def movpod(url):
    try:
        url = url.replace('/embed-', '/')
        url = url.replace('/vid/', '/')

        url = re.compile('//.+?/([\w]+)').findall(url)[0]
        url = 'http://movpod.in/embed-%s.html' % url

        result = getUrl(url).result
        url = re.compile('file *: *"(http.+?)"').findall(result)[-1]

        request = urllib2.Request(url)
        response = urllib2.urlopen(request, timeout=30)
        response.close()

        type = str(response.info()["Content-Type"])
        if type == 'text/html': raise Exception()

        if type == 'text/html': raise Exception()

        return url
    except:
        return

def movreel(url):
    try:
        user = xbmcaddon.Addon().getSetting("movreel_user")
        password = xbmcaddon.Addon().getSetting("movreel_password")

        login = 'http://movreel.com/login.html'
        post = {'op': 'login', 'login': user, 'password': password, 'redirect': url}
        post = urllib.urlencode(post)
        result = getUrl(url, close=False).result
        result += getUrl(login, post=post, close=False).result

        post = {}
        f = common.parseDOM(result, "Form", attrs = { "name": "F1" })[-1]
        k = common.parseDOM(f, "input", ret="name", attrs = { "type": "hidden" })
        for i in k: post.update({i: common.parseDOM(f, "input", ret="value", attrs = { "name": i })[0]})
        post.update({'method_free': '', 'method_premium': ''})
        post = urllib.urlencode(post)

        import time
        request = urllib2.Request(url, post)

        for i in range(0, 3):
            try:
                response = urllib2.urlopen(request, timeout=5)
                result = response.read()
                response.close()
                url = re.compile('(<a .+?</a>)').findall(result)
                url = [i for i in url if 'Download Link' in i][-1]
                url = common.parseDOM(url, "a", ret="href")[0]
                return url
            except:
                time.sleep(1)
    except:
        return

def mrfile(url):
    try:
        result = getUrl(url).result

        post = {}
        f = common.parseDOM(result, "Form", attrs = { "name": "F1" })[-1]
        k = common.parseDOM(f, "input", ret="name", attrs = { "type": "hidden" })
        for i in k: post.update({i: common.parseDOM(f, "input", ret="value", attrs = { "name": i })[0]})
        post.update({'method_free': '', 'method_premium': ''})
        post = urllib.urlencode(post)

        result = getUrl(url, post=post).result

        url = re.compile('(<a\s+href=.+?>Download\s+.+?</a>)').findall(result)[-1]
        url = common.parseDOM(url, "a", ret="href")[0]
        return url
    except:
        return

def nosvideo(url):
    try:
        result = getUrl(url).result

        post = {}
        f = common.parseDOM(result, "Form", attrs = { "method": "POST" })[0]
        k = common.parseDOM(f, "input", ret="name", attrs = { "type": "hidden" })
        for i in k: post.update({i: common.parseDOM(f, "input", ret="value", attrs = { "name": i })[0]})
        post.update({'method_free': 'Free Download'})
        post = urllib.urlencode(post)

        result = getUrl(url, post=post).result

        result = re.compile('(eval.*?\)\)\))').findall(result)[0]
        result = jsunpack(result)

        url = re.compile("playlist=(.+?)&").findall(result)[0]

        result = getUrl(url).result
        url = common.parseDOM(result, "file")[0]
        return url
    except:
        return

def played(url):
    try:
        url = url.replace('/embed-', '/')
        url = url.replace('//', '/')
        url = re.compile('/.+?/([\w]+)').findall(url)[0]
        url = 'http://played.to/embed-%s.html' % url

        result = getUrl(url, mobile=True).result
        url = re.compile('file *: *"(http.+?)"').findall(result)[-1]
        return url
    except:
        return

def primeshare(url):
    try:
        result = getUrl(url, mobile=True).result

        url = common.parseDOM(result, "video")[0]
        url = common.parseDOM(url, "source", ret="src", attrs = { "type": ".+?" })[0]
        return url
    except:
        return

def promptfile(url):
    try:
        result = getUrl(url).result

        post = {}
        f = common.parseDOM(result, "form", attrs = { "method": "post" })[0]
        k = common.parseDOM(f, "input", ret="name", attrs = { "type": "hidden" })
        for i in k: post.update({i: common.parseDOM(f, "input", ret="value", attrs = { "name": i })[0]})
        post = urllib.urlencode(post)

        result = getUrl(url, post=post).result

        url = common.parseDOM(result, "a", ret="href", attrs = { "class": "view_dl_link" })[0]
        url = getUrl(url, output='geturl', post=post).result
        return url
    except:
        return

def sharerepo(url):
    try:
        result = getUrl(url).result
        url = re.compile("file *: *'(http.+?)'").findall(result)[-1]
        url += '|User-Agent=%s' % urllib.quote_plus('Mozilla/5.0 (Windows NT 6.1; rv:34.0) Gecko/20100101 Firefox/34.0')
        return url
    except:
        return

def stagevu(url):
    try:
        result = getUrl(url).result

        url = common.parseDOM(result, "embed", ret="src", attrs = { "type": "video.+?" })[0]
        return url
    except:
        return

def streamcloud(url):
    try:
        url = re.compile('//.+?/([\w]+)').findall(url)[0]
        url = 'http://streamcloud.eu/%s' % url
 
        result = getUrl(url).result

        post = {}
        f = common.parseDOM(result, "form", attrs = { "class": "proform" })[0]
        k = common.parseDOM(f, "input", ret="name", attrs = { "type": "hidden" })
        for i in k: post.update({i: common.parseDOM(f, "input", ret="value", attrs = { "name": i })[0]})
        post = urllib.urlencode(post)
        post = post.replace('op=download1', 'op=download2')

        result = getUrl(url, post=post).result

        url = re.compile('file *: *"(http.+?)"').findall(result)[-1]
        return url
    except:
        return

def streamin(url):
    try:
        url = url.replace('/embed-', '/')
        url = re.compile('//.+?/([\w]+)').findall(url)[0]
        url = 'http://streamin.to/embed-%s.html' % url

        result = getUrl(url, mobile=True).result
        url = re.compile("file *: *'(http.+?)'").findall(result)[-1]
        return url
    except:
        return

def thefile(url):
    try:
        url = url.replace('/embed-', '/')
        url = re.compile('//.+?/([\w]+)').findall(url)[0]
        url = 'http://thefile.me/embed-%s.html' % url

        result = getUrl(url, mobile=True).result

        result = re.compile('(eval.*?\)\)\))').findall(result)[-1]
        result = jsunpack(result)

        url = re.compile("'file' *, *'(.+?)'").findall(result)
        url += re.compile("file *: *[\'|\"](.+?)[\'|\"]").findall(result)
        url += common.parseDOM(result, "embed", ret="src")
        url = 'http://' + url[-1].split('://', 1)[-1]
        return url
    except:
        return

def thevideo(url):
    try:
        url = url.replace('/embed-', '/')
        url = re.compile('//.+?/([\w]+)').findall(url)[0]
        url = 'http://thevideo.me/embed-%s.html' % url

        result = getUrl(url, mobile=True).result

        result = re.compile('(eval.*?\)\)\))').findall(result)[-1]
        result = jsunpack(result)

        url = re.compile("'file' *, *'(.+?)'").findall(result)
        url += re.compile("file *: *[\'|\"](.+?)[\'|\"]").findall(result)
        url += common.parseDOM(result, "embed", ret="src")
        url = 'http://' + url[0].split('://', 1)[-1]
        return url
    except:
        return

def uploadc(url):
    try:
        url = url.replace('/embed-', '/')
        url = re.compile('//.+?/([\w]+)').findall(url)[0]
        url = 'http://uploadc.com/embed-%s.html' % url

        result = getUrl(url, mobile=True).result

        url = re.compile("'file' *, *'(.+?)'").findall(result)

        try:
            result = re.compile('(eval.*?\)\)\))').findall(result)[-1]
            result = jsunpack(result)
        except:
            pass

        url += re.compile("'file' *, *'(.+?)'").findall(result)
        url += re.compile("file *: *[\'|\"](.+?)[\'|\"]").findall(result)
        url += common.parseDOM(result, "embed", ret="src")
        url = 'http://' + url[-1].split('://', 1)[-1]
        url += '|Referer=%s' % urllib.quote_plus('http://uploadc.com')
        return url
    except:
        return

def uploadrocket(url):
    try:
        result = getUrl(url).result

        post = {}
        f = common.parseDOM(result, "Form", attrs = { "name": "freeorpremium" })[0]
        k = common.parseDOM(f, "input", ret="name", attrs = { "type": "hidden" })
        for i in k: post.update({i: common.parseDOM(f, "input", ret="value", attrs = { "name": i })[0]})
        post.update({'method_free': 'Free Download'})
        post = urllib.urlencode(post)

        result = getUrl(url, post=post).result

        post = {}
        f = common.parseDOM(result, "Form", attrs = { "name": "F1" })[0]
        k = common.parseDOM(f, "input", ret="name", attrs = { "type": "hidden" })
        for i in k: post.update({i: common.parseDOM(f, "input", ret="value", attrs = { "name": i })[0]})
        post.update(captcha(result))
        post = urllib.urlencode(post)

        result = getUrl(url, post=post).result

        url = common.parseDOM(result, "a", ret="href", attrs = { "onclick": "window[.]open.+?" })[0]
        return url
    except:
        return

def v_vids(url):
    try:
        result = getUrl(url).result

        post = {}
        f = common.parseDOM(result, "Form", attrs = { "name": "F1" })[0]
        k = common.parseDOM(f, "input", ret="name", attrs = { "type": "hidden" })
        for i in k: post.update({i: common.parseDOM(f, "input", ret="value", attrs = { "name": i })[0]})
        post.update({'method_free': '', 'method_premium': ''})
        post = urllib.urlencode(post)

        result = getUrl(url, post=post).result

        url = common.parseDOM(result, "a", ret="href", attrs = { "id": "downloadbutton" })[0]
        return url
    except:
        return

def vidbull(url):
    try:
        result = getUrl(url, mobile=True).result
        url = common.parseDOM(result, "source", ret="src", attrs = { "type": "video.+?" })[0]
        return url
    except:
        return

def videomega(url):
    try:
        url = urlparse.urlparse(url).query
        url = urlparse.parse_qs(url)['ref'][0]
        url = 'http://videomega.tv/iframe.php?ref=%s' % url

        result = getUrl(url, referer=url).result

        url = re.compile('document.write.unescape."(.+?)"').findall(result)[-1]
        url = urllib.unquote_plus(url)
        url = re.compile('file *: *"(.+?)"').findall(url)[0]
        return url
    except:
        return

def vidspot(url):
    try:
        url = url.replace('/embed-', '/')
        url = re.compile('//.+?/([\w]+)').findall(url)[0]
        url = 'http://vidspot.net/embed-%s.html' % url

        result = getUrl(url, mobile=True).result
        url = re.compile('"file" *: *"(http.+?)"').findall(result)[-1]

        query = urlparse.urlparse(url).query
        url = url[:url.find('?')]
        url = '%s?%s&direct=false' % (url, query)
        return url
    except:
        return

def vidto(url):
    try:
        url = url.replace('/embed-', '/')
        url = re.compile('//.+?/([\w]+)').findall(url)[0]
        url = 'http://vidto.me/embed-%s.html' % url

        result = getUrl(url).result

        result = re.compile('(eval.*?\)\)\))').findall(result)[-1]
        result = re.sub(r'(\',\d*,\d*,)', r';\1', result)
        result = jsunpack(result)

        url = re.compile("'file' *, *'(.+?)'").findall(result)
        url += re.compile("file *: *[\'|\"](.+?)[\'|\"]").findall(result)
        url += common.parseDOM(result, "embed", ret="src")
        url = 'http://' + url[-1].split('://', 1)[-1]
        return url
    except:
        return

def vidzi(url):
    try:
        result = getUrl(url, mobile=True).result
        result = result.replace('\n','')
        result = re.compile('sources *: *\[.+?\]').findall(result)[-1]

        url = re.compile('file *: *"(http.+?)"').findall(result)
        url = [i for i in url if not '.m3u8' in i][-1]
        url += '|Referer=%s' % urllib.quote_plus('http://vidzi.tv')
        return url
    except:
        return

def vimeo(url):
    try:
        url = [i for i in url.split('/') if i.isdigit()][-1]
        url = 'http://player.vimeo.com/video/%s/config' % url

        result = getUrl(url).result
        result = json.loads(result)
        u = result['request']['files']['h264']

        url = None
        try: url = u['hd']['url']
        except: pass
        try: url = u['sd']['url']
        except: pass

        return url
    except:
        return

def vk(url):
    try:
        url = url.replace('http://', 'https://')
        result = getUrl(url).result

        u = re.compile('url(720|540|480)=(.+?)&').findall(result)

        url = []
        try: url += [[{'quality': 'HD', 'url': i[1]} for i in u if i[0] == '720'][0]]
        except: pass
        try: url += [[{'quality': 'SD', 'url': i[1]} for i in u if i[0] == '540'][0]]
        except: pass
        try: url += [[{'quality': 'SD', 'url': i[1]} for i in u if i[0] == '480'][0]]
        except: pass

        if url == []: return
        return url
    except:
        return

def vodlocker(url):
    try:
        url = url.replace('/embed-', '/')
        url = re.compile('//.+?/([\w]+)').findall(url)[0]
        url = 'http://vodlocker.com/embed-%s.html' % url

        result = getUrl(url, mobile=True).result
        url = re.compile('file *: *"(http.+?)"').findall(result)[-1]
        return url
    except:
        return

def xvidstage(url):
    try:
        url = url.replace('/embed-', '/')
        url = re.compile('//.+?/([\w]+)').findall(url)[0]
        url = 'http://xvidstage.com/embed-%s.html' % url

        result = getUrl(url, mobile=True).result

        result = re.compile('(eval.*?\)\)\))').findall(result)[-1]
        result = jsunpack(result)

        url = re.compile("'file' *, *'(.+?)'").findall(result)
        url += re.compile("file *: *[\'|\"](.+?)[\'|\"]").findall(result)
        url += common.parseDOM(result, "embed", ret="src")
        url = 'http://' + url[-1].split('://', 1)[-1]
        return url
    except:
        return

def youtube(url):
    try:
        id = url.split("?v=")[-1].split("/")[-1].split("?")[0].split("&")[0]
        result = getUrl('http://gdata.youtube.com/feeds/api/videos/%s?v=2' % id).result

        state, reason = None, None
        try: state = common.parseDOM(result, "yt:state", ret="name")[0]
        except: pass
        try: reason = common.parseDOM(result, "yt:state", ret="reasonCode")[0]
        except: pass
        if state == 'deleted' or state == 'rejected' or state == 'failed' or reason == 'requesterRegion' : return

        url = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % id
        return url
    except:
        return

def zettahost(url):
    try:
        url = url.replace('/embed-', '/')
        url = re.compile('//.+?/([\w]+)').findall(url)[0]
        url = 'http://zettahost.tv/embed-%s.html' % url

        result = getUrl(url, mobile=True).result

        result = re.compile('(eval.*?\)\)\))').findall(result)[-1]
        result = jsunpack(result)

        url = re.compile("'file' *, *'(.+?)'").findall(result)
        url += re.compile("file *: *[\'|\"](.+?)[\'|\"]").findall(result)
        url += common.parseDOM(result, "embed", ret="src")
        url = 'http://' + url[-1].split('://', 1)[-1]
        return url
    except:
        return


