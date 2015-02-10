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

BASE_URL = 'http://www.hdmoviezone.net'

class hdmz_Scraper(scraper.Scraper):
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
        return 'hdmz'
    
    def resolve_link(self, link):
        return link
    
    def format_source_label(self, item):
        return '[%s] %s' % (item['quality'], item['host'])
    
    def get_sources(self, video):
        source_url= self.get_url(video)
        hosters=[]
        if source_url:
            url = urlparse.urljoin(self.base_url,source_url)
            html = self._http_get(url, cache_limit=.5)
            php_url = re.findall('server\d*_php\s*=\s*"([^"]+)', html)[-1]
            match = re.search('file\s*=\s*"([^"]+)', html)
            if match:
                file_hash = match.group(1)
                data = self._http_get(php_url, data = {'url': file_hash}, headers = {'Origin': self.base_url, 'Referer': self.base_url}, cache_limit = 0)
                if data:
                    js_data = json.loads(data)
                    for item in js_data['content']:
                        if 'type' in item and item['type'].lower().startswith('video'):
                            hoster={'multi-part': False, 'host': 'hdmoviezone.net', 'url': item['url'], 'class': self, 'rating': None, 'views': None, 'quality': self._width_get_quality(item['width']), 'direct': True}
                            hosters.append(hoster)
            
        return hosters

    def get_url(self, video):
        return super(hdmz_Scraper, self)._default_get_url(video)

    def search(self, video_type, title, year):
        results=[]
        search_url = urlparse.urljoin(self.base_url, '/feeds/posts/summary?alt=json&start-index=1&max-results=500&q=')        
        search_url += urllib.quote_plus(title)
        data = self._http_get(search_url, cache_limit=.25)
        if data:
            js_data = json.loads(data)
            if 'entry' in js_data['feed']:
                for item in js_data['feed']['entry']:
                    for link in item['link']:
                        if link['rel'].lower() == 'alternate':
                            url = link['href']
                            title_year = link['title']
                            match = re.search('(.*?)\s*\((\d{4})\)$', title_year)
                            if match:
                                match_title, match_year = match.groups()
                            else:
                                match_title = title_year
                                match_year = ''
                            break
                            
                    if not year or not match_year or year == match_year:
                        result={'url': url.replace(self.base_url, ''), 'title': match_title, 'year': match_year}
                        results.append(result)
            
        return results

    def _http_get(self, url, data=None, headers=None, cache_limit=8):
        return super(hdmz_Scraper, self)._cached_http_get(url, self.base_url, self.timeout, data=data, headers=headers, cache_limit=cache_limit)
