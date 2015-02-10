"""
    SALTS XBMC Addon
    Copyright (C) 2014 tknorris

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
"""
import scraper
import urllib
import urlparse
import re
import xbmcaddon
import xbmc
import json
from salts_lib import log_utils
from salts_lib.constants import VIDEO_TYPES
from salts_lib.db_utils import DB_Connection
from salts_lib.constants import QUALITIES

BASE_URL = 'http://directdownload.tv'
LOGOUT = 'href="/index/logout"'
SEARCH_URL = '/index/search/keyword/%s/qualities/%s/from/0/search'

Q_ORDER = ['pdtv', 'dsr', 'dvdrip', 'hdtv', 'realhd', 'webdl', 'webdl1080p']
Q_DICT = dict((quality,i) for i,quality in enumerate(Q_ORDER))
QUALITY_MAP = {'pdtv': QUALITIES.MEDIUM, 'dsr': QUALITIES.MEDIUM, 'dvdrip': QUALITIES.HIGH, 'hdtv': QUALITIES.HIGH, 'realhd': QUALITIES.HD, 'webdl': QUALITIES.HD, 'webdl1080p': QUALITIES.HD}

class DirectDownload_Scraper(scraper.Scraper):
    base_url=BASE_URL
    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout=timeout
        self.db_connection = DB_Connection()
        self.base_url = xbmcaddon.Addon().getSetting('%s-base_url' % (self.get_name()))
        self.username = xbmcaddon.Addon().getSetting('%s-username' % (self.get_name()))
        self.password = xbmcaddon.Addon().getSetting('%s-password' % (self.get_name()))
    
    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.EPISODE])
    
    @classmethod
    def get_name(cls):
        return 'DirectDownload.tv'
    
    def resolve_link(self, link):
        return link

    def format_source_label(self, item):
        return '[%s] (%s) %s' % (item['quality'], item['dd_qual'], item['host'])
    
    def get_sources(self, video):
        source_url= self.get_url(video)
        hosters=[]
        if source_url:
            url = urlparse.urljoin(self.base_url,source_url)
            html = self._http_get(url, cache_limit=.5)            
            if html:
                js_result = json.loads(html)
                query = urlparse.parse_qs(urlparse.urlparse(url).query)
                match_quality = Q_ORDER
                if 'quality' in query:
                    temp_quality = re.sub('\s','',query['quality'][0])
                    match_quality = temp_quality.split(',')
                     
                import urlresolver
                for result in js_result:
                    if result['quality'] in match_quality:
                        for link in result['links']:
                            # validate url since host validation fails for real-debrid; mark links direct to avoid unusable check
                            if urlresolver.HostedMediaFile(link['url']):
                                hostname = urlparse.urlparse(link['url']).hostname
                                hoster={'multi-part': False, 'class': self, 'views': None, 'url': link['url'], 'rating': None, 'host': hostname, 
                                        'quality': QUALITY_MAP[result['quality']], 'dd_qual': result['quality'], 'direct': True}
                                hosters.append(hoster)

        return hosters
    
    def get_url(self, video):
        url = None
        result = self.db_connection.get_related_url(video.video_type, video.title, video.year, self.get_name(), video.season, video.episode)
        if result:
            url=result[0][0]
            log_utils.log('Got local related url: |%s|%s|%s|%s|%s|' % (video.video_type, video.title, video.year, self.get_name(), url))
        else:
            search_title = '%s S%02dE%02d' % (video.title, int(video.season), int(video.episode))
            results = self.search(video.video_type, search_title, '')
            best_q_index = -1
            for result in results:
                if Q_DICT[result['quality']]>best_q_index:
                    best_q_index = Q_DICT[result['quality']]
                    url = result['url']
            self.db_connection.set_related_url(video.video_type, video.title, video.year, self.get_name(), url)
        return url

    @classmethod
    def get_settings(cls):
        settings = super(DirectDownload_Scraper, cls).get_settings()
        settings = cls._disable_sub_check(settings)
        name=cls.get_name()
        settings.append('         <setting id="%s-username" type="text" label="     Username" default="" visible="eq(-6,true)"/>' % (name))
        settings.append('         <setting id="%s-password" type="text" label="     Password" option="hidden" default="" visible="eq(-7,true)"/>' % (name))
        return settings

    def search(self, video_type, title, year):
        search_url = urlparse.urljoin(self.base_url, '/search?query=')
        search_url += title
        html = self._http_get(search_url, cache_limit=.25)
        results=[]
        if html:
            js_result = json.loads(html)
            for match in js_result:
                url = search_url  + '&quality=%s' % match['quality']
                result={'url': url.replace(self.base_url, ''), 'title': match['release'], 'quality': match['quality'], 'year': ''}
                results.append(result)
        return results

    def _http_get(self, url, data=None, cache_limit=8):
        # return all uncached blank pages if no user or pass
        if not self.username or not self.password:
            return ''
        
        if 'search?query' in url:
            log_utils.log('Translating Search Url: %s' % (url), xbmc.LOGDEBUG)
            url = self.__translate_search(url)
        
        html=super(DirectDownload_Scraper, self)._cached_http_get(url, self.base_url, self.timeout, data=data, cache_limit=cache_limit)
        
        fake = None
        try:
            js_result=json.loads(html)
            fake = False
            fake = js_result[0]['fake']
        except: pass
        
        if fake or (fake is None and not re.search(LOGOUT, html)):
            log_utils.log('Logging in for url (%s)' % (url), xbmc.LOGDEBUG)
            self.__login()
            html=super(DirectDownload_Scraper, self)._cached_http_get(url, self.base_url, self.timeout, data=data, cache_limit=0)
        
        return html

    def __translate_search(self, url):
        query = urlparse.parse_qs(urlparse.urlparse(url).query)
        quality = re.sub('\s', '', query['quality'][0]) if 'quality' in query else ','.join(Q_ORDER)
        return urlparse.urljoin(self.base_url, (SEARCH_URL % (urllib.quote(query['query'][0]), quality)))
    
    def __login(self):
        url = self.base_url
        data = {'username': self.username, 'password': self.password, 'Login': 'Login'}
        html = super(DirectDownload_Scraper, self)._cached_http_get(url, self.base_url, self.timeout, data=data, cache_limit=0)
        if not re.search(LOGOUT, html):
            raise Exception('directdownload.tv login failed')
