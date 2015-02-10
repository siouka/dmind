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
import re
import urlparse
import xbmcaddon
import urllib
import base64
from salts_lib import GKDecrypter
from salts_lib.db_utils import DB_Connection
from salts_lib.constants import VIDEO_TYPES
from salts_lib.constants import QUALITIES

BASE_URL = 'http://clickplay.to'

class ClickPlay_Scraper(scraper.Scraper):
    base_url=BASE_URL
    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout=timeout
        self.db_connection = DB_Connection()
        self.base_url = xbmcaddon.Addon().getSetting('%s-base_url' % (self.get_name()))
   
    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.TVSHOW, VIDEO_TYPES.SEASON, VIDEO_TYPES.EPISODE])
    
    @classmethod
    def get_name(cls):
        return 'clickplay.to'
    
    def resolve_link(self, link):
        return link
    
    def format_source_label(self, item):
        label='[%s] %s ' % (item['quality'], item['host'])
        return label
    
    def get_sources(self, video):
        source_url=self.get_url(video)
        hosters = []
        if source_url:
            url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(url, cache_limit=.5)
            
            match = re.search('proxy\.link=([^"&]+)', html)
            if match:
                proxy_link = match.group(1)
                proxy_link = proxy_link.split('*', 1)[-1]
                stream_url = GKDecrypter.decrypter(198,128).decrypt(proxy_link, base64.urlsafe_b64decode('bW5pcUpUcUJVOFozS1FVZWpTb00='),'ECB').split('\0')[0]
                if 'vk.com' in stream_url.lower():
                    hoster = {'multi-part': False, 'host': 'vk.com', 'class': self, 'url': stream_url, 'quality': QUALITIES.HD, 'views': None, 'rating': None, 'direct': False}
                    hosters.append(hoster)
        return hosters

    def get_url(self, video):
        return super(ClickPlay_Scraper, self)._default_get_url(video)
    
    def _get_episode_url(self, show_url, video):
        season_url = show_url + 'season-%d/' % (int(video.season))
        episode_pattern = 'href="([^"]+/season-%d/episode-%d[^"]+)' % (int(video.season), int(video.episode))
        title_pattern = 'href="([^"]+)"\s+title="[^"]+/\s*([^"]+)'
        return super(ClickPlay_Scraper, self)._default_get_episode_url(season_url, video, episode_pattern, title_pattern)
        
    def search(self, video_type, title, year):
        url = urlparse.urljoin(self.base_url, '/search/')
        url += urllib.quote(title)
        html = self._http_get(url, cache_limit=8)

        results=[]
        pattern = 'href="([^"]+)"\s+class="article.*?class="article-title">([^<]+)'
        for match in re.finditer(pattern, html, re.DOTALL):
            url, match_title_year = match.groups()
            r = re.search('(.*?)\s+\((\d{4})\)', match_title_year)
            if r:
                match_title, match_year = r.groups()
            else:
                match_title=match_title_year
                match_year=''
                
            if not year or not match_year or year == match_year:
                result={'url': url.replace(self.base_url, ''), 'title': match_title, 'year': match_year}
                results.append(result)

        return results
    
    def _http_get(self, url, data=None, cache_limit=8):
        return super(ClickPlay_Scraper, self)._cached_http_get(url, self.base_url, self.timeout, data=data, cache_limit=cache_limit)
