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
from salts_lib.db_utils import DB_Connection
from salts_lib.constants import VIDEO_TYPES
from salts_lib.constants import QUALITIES

BASE_URL = 'http://movies-online.li'
QUALITY_MAP = {'HD': QUALITIES.HIGH, 'CAM': QUALITIES.LOW, 'BR-RIP': QUALITIES.HD, 'UNKNOWN': QUALITIES.MEDIUM, 'DVD-RIP': QUALITIES.HIGH}

class WMO_Scraper(scraper.Scraper):
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
        return 'wmo.ch'
    
    def resolve_link(self, link):
        if self.base_url in link:
            url = urlparse.urljoin(self.base_url, link)
            html = self._http_get(url, cache_limit=.5)
            match = re.search('id="redirectButton[^>]+href=(?:\'|")([^"\']+)', html)
            if match:
                return match.group(1)
        else:
            return link
    
    def format_source_label(self, item):
        label='[%s] %s (%s views)' % (item['quality'], item['host'], item['views'])
        return label
    
    def get_sources(self, video):
        source_url=self.get_url(video)
        hosters = []
        if source_url:
            url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(url, cache_limit=.5)
            
            match = re.search('Quality</label>: ([^<]+)', html)
            if match:
                quality=QUALITY_MAP.get(match.group(1))
            else:
                quality = None
                                         
            pattern = 'id="hovered".*?href="([^"]+)">([^<]+).*?class="[^"]+link_views[^>]+>([\d\.]+)(k?)'
            for match in re.finditer(pattern, html, re.DOTALL):
                stream_url, host, views, k = match.groups()
                if k:
                    views = float(views) * 1000
            
                hoster = {'multi-part': False, 'host': host.lower(), 'class': self, 'url': stream_url, 'quality': self._get_quality(video, host, quality), 'views': int(views), 'rating': None, 'direct': False}
                hosters.append(hoster)
        return hosters

    def get_url(self, video):
        return super(WMO_Scraper, self)._default_get_url(video)
    
    def search(self, video_type, title, year):
        url = urlparse.urljoin(self.base_url, '/?s=%s&search=' % urllib.quote_plus(title))
        html = self._http_get(url, cache_limit=8)

        results=[]
        pattern = 'class="PostHeader".*?href="([^"]+)[^>]+>\s*(.*?) \((\d+)\)'
        for match in re.finditer(pattern, html, re.DOTALL):
            url, match_title, match_year = match.groups()
            if not year or not match_year or year == match_year:
                result={'url': url.replace(self.base_url, ''), 'title': match_title, 'year': ''}
                results.append(result)

        return results
    
    def _http_get(self, url, data=None, cache_limit=8):
        return super(WMO_Scraper, self)._cached_http_get(url, self.base_url, self.timeout, data=data, cache_limit=cache_limit)
