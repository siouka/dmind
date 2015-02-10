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
from salts_lib import log_utils
from salts_lib.constants import VIDEO_TYPES
from salts_lib.db_utils import DB_Connection
from salts_lib.constants import QUALITIES

BASE_URL = 'http://watchyourflix.com'

class WYF_Scraper(scraper.Scraper):
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
        return 'WatchYourFlix'
    
    def resolve_link(self, link):
        return link
    
    def format_source_label(self, item):
        return '[%s] %s (%s Views)' % (item['quality'], item['host'], item['views'])
    
    def get_sources(self, video):
        source_url= self.get_url(video)
        hosters=[]
        if source_url:
            url = urlparse.urljoin(self.base_url,source_url)
            html = self._http_get(url, cache_limit=.5)
            
            views=None
            match = re.search('class="views-infos">(\d+)', html)
            if match: views=match.group(1)
            
            match = re.search('type="video[^"]+"\s+src="([^"]+)', html)
            if not match:
                match = re.search('href="([^"]+mp4)', html)
            
            if match:
                stream_url = match.group(1)
                hoster={'multi-part': False, 'host': 'watchyourflix.com', 'url': stream_url, 'class': self, 'rating': None, 'views': views, 'quality': QUALITIES.HD, 'direct': True}
                hosters.append(hoster)

            
        return hosters

    def get_url(self, video):
        return super(WYF_Scraper, self)._default_get_url(video)

    def search(self, video_type, title, year):
        results=[]
        search_url = urlparse.urljoin(self.base_url, '/?s=')        
        search_url += urllib.quote_plus(title)
        html = self._http_get(search_url, cache_limit=.25)
        if not re.search('nothing matched your search criteria', html):
            match = re.search('class="listing-videos(.*?)</ul>', html, re.DOTALL)
            if match:
                results_container = match.group(1)
                pattern ='href="([^"]+)"\s+title="([^"]+)'
                for match in re.finditer(pattern, results_container):
                    url, match_title = match.groups('')
                    result={'url': url.replace(self.base_url,''), 'title': match_title, 'year': ''}
                    results.append(result)
            
        return results

    def _http_get(self, url, data=None, cache_limit=8):
        return super(WYF_Scraper, self)._cached_http_get(url, self.base_url, self.timeout, data=data, cache_limit=cache_limit)
