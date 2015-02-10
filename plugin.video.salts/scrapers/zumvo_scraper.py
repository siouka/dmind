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
import base64
from salts_lib import GKDecrypter
from salts_lib import log_utils
from salts_lib.constants import VIDEO_TYPES
from salts_lib.db_utils import DB_Connection
from salts_lib.constants import QUALITIES

BASE_URL = 'http://zumvo.com'
QUALITY_MAP = {'HD': QUALITIES.HIGH, 'CAM': QUALITIES.LOW, 'BR-RIP': QUALITIES.HD, 'UNKNOWN': QUALITIES.MEDIUM, 'SD': QUALITIES.HIGH}


class Zumvo_Scraper(scraper.Scraper):
    base_url=BASE_URL
    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout=timeout
        self.db_connection = DB_Connection()
        self.base_url = xbmcaddon.Addon().getSetting('%s-base_url' % (self.get_name()))
    
    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.MOVIE])
    
    @classmethod
    def get_name(cls):
        return 'zumvo.com'
    
    def resolve_link(self, link):
        return link
    
    def format_source_label(self, item):
        return '[%s] %s (%s views)' % (item['quality'], item['host'], item['views'])
    
    def get_sources(self, video):
        source_url= self.get_url(video)
        hosters=[]
        if source_url:
            url = urlparse.urljoin(self.base_url,source_url)
            html = self._http_get(url, cache_limit=.5)
            quality = QUALITIES.LOW
            match = re.search('class="status">([^<]+)', html)
            if match:
                quality = QUALITY_MAP.get(match.group(1), QUALITIES.LOW)
            
            views = None
            match = re.search('Views:</dt>\s*<dd>(\d+)', html, re.DOTALL)
            if match:
                views = match.group(1)

            match = re.search('href="([^"]+)"\s*class="btn-watch"', html)
            if match:
                html = self._http_get(match.group(1), cache_limit=.5)
            
                    
                match = re.search('proxy\.link":\s*"([^"&]+)', html)
                if match:
                    proxy_link = match.group(1)
                    proxy_link = proxy_link.split('*', 1)[-1]
                    stream_url = GKDecrypter.decrypter(198,128).decrypt(proxy_link, base64.urlsafe_b64decode('NlFQU1NQSGJrbXJlNzlRampXdHk='),'ECB').split('\0')[0]
                    if 'picasaweb' in stream_url:
                        html = self._http_get(stream_url, cache_limit=.5)                    
                        sources = self.__parse_google(html)
                        if sources:
                            for source in sources:
                                hoster = {'multi-part': False, 'url': source, 'class': self, 'quality': sources[source], 'host': 'zumvo.com', 'rating': None, 'views': views, 'direct': True}
                                hosters.append(hoster)
                    else:
                        hoster = {'multi-part': False, 'url': stream_url, 'class': self, 'quality': quality, 'host': urlparse.urlsplit(stream_url).hostname, 'rating': None, 'views': views, 'direct': False}
                        hosters.append(hoster)
                        
        return hosters

    def __parse_google(self, html):
        pattern='"url"\s*:\s*"([^"]+)"\s*,\s*"height"\s*:\s*\d+\s*,\s*"width"\s*:\s*(\d+)\s*,\s*"type"\s*:\s*"video/'
        sources={}
        for match in re.finditer(pattern, html):
            url, width = match.groups()
            url = url.replace('%3D', '=')
            sources[url]=self._width_get_quality(width)
        return sources
    
    def get_url(self, video):
        return super(Zumvo_Scraper, self)._default_get_url(video)

    def search(self, video_type, title, year):
        search_url = urlparse.urljoin(self.base_url, '/search/')
        search_url += urllib.quote_plus(title)
        html = self._http_get(search_url, cache_limit=.25)
        results=[]
        match = re.search('ul class="list-film"(.*?)</ul>', html, re.DOTALL)
        if match:
            result_fragment = match.group(1)
            pattern ='class="name">\s*<a\s+href="([^"]+)"\s+title="Watch\s+(.*?)\s+\((\d{4})\)'
            for match in re.finditer(pattern, result_fragment, re.DOTALL):
                url, title, match_year = match.groups('')
                if not year or not match_year or year == match_year:
                    result={'url': url.replace(self.base_url, ''), 'title': title, 'year': match_year}
                    results.append(result)
        return results

    def _http_get(self, url, cache_limit=8):
        return super(Zumvo_Scraper, self)._cached_http_get(url, self.base_url, self.timeout, cache_limit=cache_limit)
