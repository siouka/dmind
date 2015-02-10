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
import sys
import os
import re
import datetime
import time
import xbmcplugin
import xbmcgui
import xbmc
import xbmcvfs
import urllib2
from addon.common.addon import Addon
from salts_lib.db_utils import DB_Connection
from salts_lib.url_dispatcher import URL_Dispatcher
from salts_lib.srt_scraper import SRT_Scraper
from salts_lib.trakt_api import Trakt_API, TransientTraktError
from salts_lib import utils
from salts_lib import log_utils
from salts_lib.constants import *
from scrapers import * # import all scrapers into this namespace
from scrapers import ScraperVideo

_SALTS = Addon('plugin.video.salts', sys.argv)
ICON_PATH = os.path.join(_SALTS.get_path(), 'icon.png')
username=_SALTS.get_setting('username')
password=_SALTS.get_setting('password')
TOKEN=utils.get_trakt_token()
use_https=_SALTS.get_setting('use_https')=='true'
trakt_timeout=int(_SALTS.get_setting('trakt_timeout'))
list_size=int(_SALTS.get_setting('list_size'))

trakt_api=Trakt_API(username,password, TOKEN, use_https, list_size, trakt_timeout)
url_dispatcher=URL_Dispatcher()
db_connection=DB_Connection()

global urlresolver

@url_dispatcher.register(MODES.MAIN)
def main_menu():
    db_connection.init_database()
    if not TOKEN:
        remind_count = int(_SALTS.get_setting('remind_count'))
        remind_max=5
        if remind_count<remind_max:
            remind_count += 1
            log_utils.log('Showing Config reminder')
            builtin = 'XBMC.Notification(%s,(%s/%s) Configure Trakt Account for more options, 7500, %s)'
            xbmc.executebuiltin(builtin % (_SALTS.get_name(), remind_count, remind_max, ICON_PATH))
            _SALTS.set_setting('remind_count', str(remind_count))
    else:
        _SALTS.set_setting('remind_count', '0')
    
    if _SALTS.get_setting('auto-disable') != DISABLE_SETTINGS.OFF:
        utils.do_disable_check()

    _SALTS.add_directory({'mode': MODES.BROWSE, 'section': SECTIONS.MOVIES}, {'title': 'Movies'}, img=utils.art('movies.png'), fanart=utils.art('fanart.jpg'))
    _SALTS.add_directory({'mode': MODES.BROWSE, 'section': SECTIONS.TV}, {'title': 'TV Shows'}, img=utils.art('television.png'), fanart=utils.art('fanart.jpg'))
    _SALTS.add_directory({'mode': MODES.SETTINGS}, {'title': 'Settings'}, img=utils.art('settings.png'), fanart=utils.art('fanart.jpg'))
    xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=False)

@url_dispatcher.register(MODES.SETTINGS)
def settings_menu():
    _SALTS.add_directory({'mode': MODES.SCRAPERS}, {'title': 'Scraper Sort Order'}, img=utils.art('settings.png'), fanart=utils.art('fanart.jpg'))
    _SALTS.add_directory({'mode': MODES.RES_SETTINGS}, {'title': 'Url Resolver Settings'}, img=utils.art('settings.png'), fanart=utils.art('fanart.jpg'))
    _SALTS.add_directory({'mode': MODES.ADDON_SETTINGS}, {'title': 'Add-on Settings'}, img=utils.art('settings.png'), fanart=utils.art('fanart.jpg'))
    _SALTS.add_directory({'mode': MODES.SHOW_VIEWS}, {'title': 'Set Default Views'}, img=utils.art('settings.png'), fanart=utils.art('fanart.jpg'))
    _SALTS.add_directory({'mode': MODES.BROWSE_URLS}, {'title': 'Remove Cached Url(s)'}, img=utils.art('settings.png'), fanart=utils.art('fanart.jpg'))
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

@url_dispatcher.register(MODES.SHOW_VIEWS)
def show_views():
    for content_type in ['movies', 'tvshows', 'seasons', 'episodes']:
        _SALTS.add_directory({'mode': MODES.BROWSE_VIEW, 'content_type': content_type}, {'title': 'Set Default %s View' % (content_type.capitalize())}, img=utils.art('settings.png'), fanart=utils.art('fanart.jpg'))
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

@url_dispatcher.register(MODES.BROWSE_VIEW, ['content_type'])
def browse_view(content_type):
    _SALTS.add_directory({'mode': MODES.SET_VIEW, 'content_type': content_type}, {'title': 'Set a view then select this item to set the default %s view' % (content_type.capitalize())}, img=utils.art('settings.png'), fanart=utils.art('fanart.jpg'))
    utils.set_view(content_type, False)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

@url_dispatcher.register(MODES.SET_VIEW, ['content_type'])
def set_default_view(content_type):
    current_view = utils.get_current_view()
    if current_view:
        _SALTS.set_setting('%s_view' % (content_type), current_view)
        view_name = xbmc.getInfoLabel('Container.Viewmode')
        builtin = "XBMC.Notification(Import,%s View Set to: %s,2000, %s)" % (content_type.capitalize(), view_name, ICON_PATH)
        xbmc.executebuiltin(builtin)

@url_dispatcher.register(MODES.BROWSE_URLS)
def browse_urls():
    urls = db_connection.get_all_urls(order_matters=True)
    _SALTS.add_directory({'mode': MODES.FLUSH_CACHE}, {'title': '***Delete [B][COLOR red]ENTIRE[/COLOR][/B] Url Cache***'}, img=utils.art('settings.png'), fanart=utils.art('fanart.jpg'))
    for url in urls:
        _SALTS.add_directory({'mode': MODES.DELETE_URL, 'url': url[0]}, {'title': url[0]}, img=utils.art('settings.png'), fanart=utils.art('fanart.jpg'))
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
        
@url_dispatcher.register(MODES.DELETE_URL, ['url'])
def delete_url(url):
    db_connection.delete_cached_url(url)
    xbmc.executebuiltin("XBMC.Container.Refresh")

@url_dispatcher.register(MODES.RES_SETTINGS)
def resolver_settings():
    global urlresolver
    import urlresolver
    urlresolver.display_settings()

@url_dispatcher.register(MODES.ADDON_SETTINGS)
def addon_settings():
    _SALTS.show_settings()

@url_dispatcher.register(MODES.BROWSE, ['section'])
def browse_menu(section):
    if section==SECTIONS.TV:
        section_label='TV Shows'
        search_img='television_search.png'
    else:
        section_label='Movies'
        search_img='movies_search.png'

    if utils.menu_on('trending'): _SALTS.add_directory({'mode': MODES.TRENDING, 'section': section}, {'title': 'Trending %s' % (section_label)}, img=utils.art('trending.png'), fanart=utils.art('fanart.jpg'))
    if utils.menu_on('popular'): _SALTS.add_directory({'mode': MODES.POPULAR, 'section': section}, {'title': 'Popular %s' % (section_label)}, img=utils.art('popular.png'), fanart=utils.art('fanart.jpg'))
    if utils.menu_on('recent'): _SALTS.add_directory({'mode': MODES.RECENT, 'section': section}, {'title': 'Recently Updated %s' % (section_label)}, img=utils.art('recent.png'), fanart=utils.art('fanart.jpg'))
    if TOKEN:
        if utils.menu_on('recommended'): _SALTS.add_directory({'mode': MODES.RECOMMEND, 'section': section}, {'title': 'Recommended %s' % (section_label)}, img=utils.art('recommended.png'), fanart=utils.art('fanart.jpg'))
        if utils.menu_on('collection'): add_refresh_item({'mode': MODES.SHOW_COLLECTION, 'section': section}, 'My %s Collection' % (section_label[:-1]), utils.art('collection.png'), utils.art('fanart.jpg'))
        if utils.menu_on('favorites'): _SALTS.add_directory({'mode': MODES.SHOW_FAVORITES, 'section': section}, {'title': 'My Favorites'}, img=utils.art('my_favorites.png'), fanart=utils.art('fanart.jpg'))
        if utils.menu_on('subscriptions'): _SALTS.add_directory({'mode': MODES.MANAGE_SUBS, 'section': section}, {'title': 'My Subscriptions'}, img=utils.art('my_subscriptions.png'), fanart=utils.art('fanart.jpg'))
        if utils.menu_on('watchlist'): _SALTS.add_directory({'mode': MODES.SHOW_WATCHLIST, 'section': section}, {'title': 'My Watchlist'}, img=utils.art('my_watchlist.png'), fanart=utils.art('fanart.jpg'))
        if utils.menu_on('my_lists'): _SALTS.add_directory({'mode': MODES.MY_LISTS, 'section': section}, {'title': 'My Lists'}, img=utils.art('my_lists.png'), fanart=utils.art('fanart.jpg'))
#     if utils.menu_on('other_lists'): _SALTS.add_directory({'mode': MODES.OTHER_LISTS, 'section': section}, {'title': 'Other Lists'}, img=utils.art('other_lists.png'), fanart=utils.art('fanart.jpg'))
    if section==SECTIONS.TV:
        if TOKEN: 
            if utils.menu_on('progress'): add_refresh_item({'mode': MODES.SHOW_PROGRESS}, 'My Next Episodes', utils.art('my_progress.png'), utils.art('fanart.jpg'))
            if utils.menu_on('my_cal'): add_refresh_item({'mode': MODES.MY_CAL}, 'My Calendar', utils.art('my_calendar.png'), utils.art('fanart.jpg'))
        if utils.menu_on('general_cal'): add_refresh_item({'mode': MODES.CAL}, 'General Calendar', utils.art('calendar.png'), utils.art('fanart.jpg'))
        if utils.menu_on('premiere_cal'): add_refresh_item({'mode': MODES.PREMIERES}, 'Premiere Calendar', utils.art('premiere_calendar.png'), utils.art('fanart.jpg'))
#         if TOKEN:
#             if utils.menu_on('friends'): add_refresh_item({'mode': MODES.FRIENDS_EPISODE, 'section': section}, 'Friends Episode Activity [COLOR red][I](Temporarily Broken)[/I][/COLOR]', utils.art('friends_episode.png'), utils.art('fanart.jpg'))
#     if TOKEN:
#         if utils.menu_on('friends'): add_refresh_item({'mode': MODES.FRIENDS, 'section': section}, 'Friends Activity [COLOR red][I](Temporarily Broken)[/I][/COLOR]', utils.art('friends.png'), utils.art('fanart.jpg'))
    if utils.menu_on('search'): _SALTS.add_directory({'mode': MODES.SEARCH, 'section': section}, {'title': 'Search'}, img=utils.art(search_img), fanart=utils.art('fanart.jpg'))
    if utils.menu_on('search'): _SALTS.add_directory({'mode': MODES.RECENT_SEARCH, 'section': section}, {'title': 'Recent Searches'}, img=utils.art(search_img), fanart=utils.art('fanart.jpg'))
    if utils.menu_on('search'): _SALTS.add_directory({'mode': MODES.SAVED_SEARCHES, 'section': section}, {'title': 'Saved Searches'}, img=utils.art(search_img), fanart=utils.art('fanart.jpg'))
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def add_refresh_item(queries, label, thumb, fanart):
    liz = xbmcgui.ListItem(label, iconImage=thumb, thumbnailImage=thumb)
    liz.setProperty('fanart_image', fanart)
    menu_items = []
    refresh_queries = {'mode': MODES.FORCE_REFRESH, 'refresh_mode': queries['mode']}
    if 'section' in queries: refresh_queries.update({'section': queries['section']})
    menu_items.append(('Force Refresh', 'RunPlugin(%s)' % (_SALTS.build_plugin_url(refresh_queries))), )
    liz.addContextMenuItems(menu_items)
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), _SALTS.build_plugin_url(queries), liz, isFolder=True) 
    
@url_dispatcher.register(MODES.FORCE_REFRESH, ['refresh_mode'], ['section', 'slug', 'username'])
def force_refresh(refresh_mode, section=None, slug=None, username=None):
    builtin = "XBMC.Notification(%s,Forcing Refresh, 2000, %s)" % (_SALTS.get_name(), ICON_PATH)
    xbmc.executebuiltin(builtin)
    log_utils.log('Forcing refresh for mode: |%s|%s|%s|%s|' % (refresh_mode, section, slug, username))
    now = datetime.datetime.now()
    offset = int(_SALTS.get_setting('calendar-day'))
    start_date = now + datetime.timedelta(days=offset)
    start_date = datetime.datetime.strftime(start_date,'%Y-%m-%d')
    if refresh_mode == MODES.SHOW_COLLECTION:
        trakt_api.get_collection(section, cached=False)
    elif refresh_mode == MODES.SHOW_PROGRESS:
        get_progress(cache_override = True)
    elif refresh_mode == MODES.MY_CAL:
        trakt_api.get_my_calendar(start_date, cached=False)
    elif refresh_mode == MODES.CAL:
        trakt_api.get_calendar(start_date, cached=False)
    elif refresh_mode == MODES.PREMIERES:
        trakt_api.get_premieres(start_date, cached=False)
    elif refresh_mode == MODES.FRIENDS_EPISODE:
        trakt_api.get_friends_activity(section, True)
    elif refresh_mode == MODES.FRIENDS:
        trakt_api.get_friends_activity(section)
    elif refresh_mode == MODES.SHOW_LIST: 
        trakt_api.show_list(slug, section, username, cached=False)
    else:
        log_utils.log('Force refresh on unsupported mode: |%s|' % (refresh_mode)) 
        return
        
    log_utils.log('Force refresh complete: |%s|%s|%s|%s|' % (refresh_mode, section, slug, username))
    builtin = "XBMC.Notification(%s,Force Refresh Complete, 2000, %s)" % (_SALTS.get_name(), ICON_PATH)
    xbmc.executebuiltin(builtin)

@url_dispatcher.register(MODES.SCRAPERS)
def scraper_settings():
    scrapers=utils.relevant_scrapers(None, True, True)
    if _SALTS.get_setting('toggle_enable')=='true':
        label='**Enable All Scrapers**'
    else:
        label='**Disable All Scrapers**'
    _SALTS.add_directory({'mode': MODES.TOGGLE_ALL}, {'title': label}, img=utils.art('scraper.png'), fanart=utils.art('fanart.jpg'))
    
    for i, cls in enumerate(scrapers):
        label = '%s (Provides: %s)' % (cls.get_name(), str(list(cls.provides())).replace("'", ""))
        label = '%s (Success: %s%%)' % (label, utils.calculate_success(cls.get_name()))
        if not utils.scraper_enabled(cls.get_name()): 
            label = '[COLOR darkred]%s[/COLOR]' % (label)
            toggle_label='Enable Scraper'
        else:
            toggle_label='Disable Scraper'
        liz = xbmcgui.ListItem(label=label, iconImage=utils.art('scraper.png'), thumbnailImage=utils.art('scraper.png'))
        liz.setProperty('fanart_image', utils.art('fanart.jpg'))
        liz.setProperty('IsPlayable', 'false')
        liz.setInfo('video', {'title': label})
        liz_url = _SALTS.build_plugin_url({'mode': MODES.TOGGLE_SCRAPER, 'name': cls.get_name()})
        
        menu_items=[]
        if i>0:
            queries = {'mode': MODES.MOVE_SCRAPER, 'name': cls.get_name(), 'direction': DIRS.UP, 'other': scrapers[i-1].get_name()}
            menu_items.append(('Move Up', 'RunPlugin(%s)' % (_SALTS.build_plugin_url(queries))), )
        if i<len(scrapers)-1:
            queries = {'mode': MODES.MOVE_SCRAPER, 'name': cls.get_name(), 'direction': DIRS.DOWN, 'other': scrapers[i+1].get_name()}
            menu_items.append(('Move Down', 'RunPlugin(%s)' % (_SALTS.build_plugin_url(queries))), )

        queries = {'mode': MODES.MOVE_TO, 'name': cls.get_name()}
        menu_items.append(('Move To...', 'RunPlugin(%s)' % (_SALTS.build_plugin_url(queries))), )

        queries = {'mode': MODES.TOGGLE_SCRAPER, 'name': cls.get_name()}
        menu_items.append((toggle_label, 'RunPlugin(%s)' % (_SALTS.build_plugin_url(queries))), )
        liz.addContextMenuItems(menu_items, replaceItems=True)
        
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), liz_url, liz, isFolder=False)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

@url_dispatcher.register(MODES.MOVE_TO, ['name'])
def move_to(name):
    dialog = xbmcgui.Dialog()
    sort_key = utils.make_source_sort_key()
    new_pos = dialog.numeric(0, 'Enter New Position (1 - %s)' % (len(sort_key)))
    if new_pos:
        new_pos = int(new_pos)
        old_key = sort_key[name]
        new_key=-new_pos+1
        if (new_pos<=0 or new_pos>len(sort_key)) or old_key==new_key:
            return
        
        for key in sort_key:
            this_key = sort_key[key]
            # moving scraper up
            if new_key>old_key:
                # move everything between the old and new down
                if this_key>old_key and this_key<=new_key:
                    sort_key[key] -= 1
            # moving scraper down
            else:
                # move everything between the old and new up
                if this_key>new_key and this_key<=new_key:
                    sort_key[key] += 1    
            
        sort_key[name]=new_key
    _SALTS.set_setting('source_sort_order', utils.make_source_sort_string(sort_key))
    xbmc.executebuiltin("XBMC.Container.Refresh")

@url_dispatcher.register(MODES.MOVE_SCRAPER, ['name', 'direction', 'other'])
def move_scraper(name, direction, other):
    sort_key = utils.make_source_sort_key()
    if direction == DIRS.UP:
        sort_key[name] +=1
        sort_key[other] -= 1
    elif direction == DIRS.DOWN:
        sort_key[name] -= 1
        sort_key[other] += 1
    _SALTS.set_setting('source_sort_order', utils.make_source_sort_string(sort_key))
    xbmc.executebuiltin("XBMC.Container.Refresh")

@url_dispatcher.register(MODES.TOGGLE_ALL)
def toggle_scrapers():
    cur_toggle = _SALTS.get_setting('toggle_enable')
    scrapers=utils.relevant_scrapers(None, True, True)
    for scraper in scrapers:
        _SALTS.set_setting('%s-enable' % (scraper.get_name()), cur_toggle)
        
    new_toggle = 'false' if cur_toggle=='true' else 'true'
    _SALTS.set_setting('toggle_enable', new_toggle)
    xbmc.executebuiltin("XBMC.Container.Refresh")

@url_dispatcher.register(MODES.TOGGLE_SCRAPER, ['name'])
def toggle_scraper(name):
    if utils.scraper_enabled(name):
        setting='false'
    else:
        setting='true'
    _SALTS.set_setting('%s-enable' % (name), setting)
    xbmc.executebuiltin("XBMC.Container.Refresh")
    
@url_dispatcher.register(MODES.TRENDING, ['section'], ['page'])
def browse_trending(section, page = 1):
    list_data = trakt_api.get_trending(section, page)
    make_dir_from_list(section, list_data, query = {'mode': MODES.TRENDING, 'section': section}, page = page)

@url_dispatcher.register(MODES.POPULAR, ['section'], ['page'])
def browse_popular(section, page = 1):
    list_data = trakt_api.get_popular(section, page)
    make_dir_from_list(section, list_data, query = {'mode': MODES.POPULAR, 'section': section}, page = page)

@url_dispatcher.register(MODES.RECENT, ['section'], ['page'])
def browse_recent(section, page = 1):
    now = datetime.datetime.now()
    start_date = now - datetime.timedelta(days=7)
    start_date = datetime.datetime.strftime(start_date,'%Y-%m-%d')
    list_data = trakt_api.get_recent(section, start_date, page)
    make_dir_from_list(section, list_data, query = {'mode': MODES.RECENT, 'section': section}, page = page)

@url_dispatcher.register(MODES.RECOMMEND, ['section'])
def browse_recommendations(section):
    list_data = trakt_api.get_recommendations(section)
    make_dir_from_list(section, list_data)

@url_dispatcher.register(MODES.FRIENDS, ['mode', 'section'])
@url_dispatcher.register(MODES.FRIENDS_EPISODE, ['mode', 'section'])
def browse_friends(mode, section):
    section_params=utils.get_section_params(section)
    activities=trakt_api.get_friends_activity(section, mode==MODES.FRIENDS_EPISODE)
    totalItems=len(activities)
    
    for activity in activities['activity']:
        if 'episode' in activity:
            show=activity['show']
            liz, liz_url = make_episode_item(show, activity['episode'], show_subs=False)
            folder=(liz.getProperty('isPlayable')!='true')
            label=liz.getLabel()
            label = '%s (%s) - %s' % (show['title'], show['year'], label.decode('utf-8', 'replace'))
            liz.setLabel(label) 
        else:
            liz, liz_url = make_item(section_params, activity[TRAKT_SECTIONS[section][:-1]])
            folder = section_params['folder']

        label=liz.getLabel()
        action = ' [[COLOR blue]%s[/COLOR] [COLOR green]%s' % (activity['user']['username'], activity['action'])
        if activity['action']=='rating': action += ' - %s' % (activity['rating'])
        action += '[/COLOR]]'
        label = '%s %s' % (action, label.decode('utf-8', 'replace'))
        liz.setLabel(label)
        
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), liz_url, liz,isFolder=folder,totalItems=totalItems)        
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

@url_dispatcher.register(MODES.MY_CAL, ['mode'], ['start_date'])
@url_dispatcher.register(MODES.CAL, ['mode'], ['start_date'])
@url_dispatcher.register(MODES.PREMIERES, ['mode'], ['start_date'])
def browse_calendar(mode, start_date=None):
    if start_date is None:
        now = datetime.datetime.now()
        offset = int(_SALTS.get_setting('calendar-day'))
        start_date = now + datetime.timedelta(days=offset)
        start_date = datetime.datetime.strftime(start_date,'%Y-%m-%d')
    if mode == MODES.MY_CAL:
        days=trakt_api.get_my_calendar(start_date)
    elif mode == MODES.CAL:
        days=trakt_api.get_calendar(start_date)
    elif mode == MODES.PREMIERES:
        days=trakt_api.get_premieres(start_date)
    make_dir_from_cal(mode, start_date, days)

@url_dispatcher.register(MODES.MY_LISTS, ['section'])
def browse_lists(section):
    lists = trakt_api.get_lists()
    lists.insert(0, {'name': 'watchlist', 'ids': {'slug': utils.WATCHLIST_SLUG}})
    totalItems=len(lists)
    for user_list in lists:
        ids = user_list['ids']
        liz = xbmcgui.ListItem(label=user_list['name'], iconImage=utils.art('list.png'), thumbnailImage=utils.art('list.png'))
        liz.setProperty('fanart_image', utils.art('fanart.jpg'))
        queries = {'mode': MODES.SHOW_LIST, 'section': section, 'slug': ids['slug']}
        liz_url = _SALTS.build_plugin_url(queries)
        
        menu_items=[]
        queries={'mode': MODES.SET_FAV_LIST, 'slug': ids['slug'], 'section': section}
        menu_items.append(('Set as Favorites List', 'RunPlugin(%s)' % (_SALTS.build_plugin_url(queries))), )
        queries={'mode': MODES.SET_SUB_LIST, 'slug': ids['slug'], 'section': section}
        menu_items.append(('Set as Subscription List', 'RunPlugin(%s)' % (_SALTS.build_plugin_url(queries))), )
        queries={'mode': MODES.COPY_LIST, 'slug': COLLECTION_SLUG, 'section': section, 'target_slug': ids['slug']}
        menu_items.append(('Import from Collection', 'RunPlugin(%s)' % (_SALTS.build_plugin_url(queries))), )
        liz.addContextMenuItems(menu_items, replaceItems=True)
        
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), liz_url, liz,isFolder=True,totalItems=totalItems)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

@url_dispatcher.register(MODES.OTHER_LISTS, ['section'])
def browse_other_lists(section):
    liz = xbmcgui.ListItem(label='Add another user\'s list', iconImage=utils.art('add_other.png'), thumbnailImage=utils.art('add_other.png'))
    liz.setProperty('fanart_image', utils.art('fanart.jpg'))
    liz_url = _SALTS.build_plugin_url({'mode': MODES.ADD_OTHER_LIST, 'section': section})
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), liz_url, liz, isFolder=False)    
    
    lists = db_connection.get_other_lists(section)
    totalItems=len(lists)
    for other_list in lists:
        try:
            header = trakt_api.get_list_header(other_list[1], other_list[0])
        except urllib2.HTTPError as e:
            if e.code == 404:
                header = None
            else:
                raise

        if header:
            found=True
            if other_list[2]:
                name=other_list[2]
            else:
                name=header['name']
        else:
            name = other_list[1]
            found=False
            
        label = '[[COLOR blue]%s[/COLOR]] %s' % (other_list[0], name)

        liz = xbmcgui.ListItem(label=label, iconImage=utils.art('list.png'), thumbnailImage=utils.art('list.png'))
        liz.setProperty('fanart_image', utils.art('fanart.jpg'))
        if found:
            queries = {'mode': MODES.SHOW_LIST, 'section': section, 'slug': other_list[1], 'username': other_list[0]}
        else:
            queries = {'mode': MODES.OTHER_LISTS, 'section': section}
        liz_url = _SALTS.build_plugin_url(queries)
        
        menu_items=[]
        if found:
            queries = {'mode': MODES.FORCE_REFRESH, 'refresh_mode': MODES.SHOW_LIST, 'section': section, 'slug': other_list[1], 'username': other_list[0]}
            menu_items.append(('Force Refresh', 'RunPlugin(%s)' % (_SALTS.build_plugin_url(queries))), )
            queries={'mode': MODES.COPY_LIST, 'section': section, 'slug': other_list[1], 'username': other_list[0]}
            menu_items.append(('Copy to My List', 'RunPlugin(%s)' % (_SALTS.build_plugin_url(queries))), )
        queries={'mode': MODES.ADD_OTHER_LIST, 'section': section, 'username': other_list[0]}
        menu_items.append(('Add more from %s' % (other_list[0]), 'RunPlugin(%s)' % (_SALTS.build_plugin_url(queries))), )
        queries={'mode': MODES.REMOVE_LIST, 'section': section, 'slug': other_list[1], 'username': other_list[0]}
        menu_items.append(('Remove List', 'RunPlugin(%s)' % (_SALTS.build_plugin_url(queries))), )
        queries={'mode': MODES.RENAME_LIST, 'section': section, 'slug': other_list[1], 'username': other_list[0], 'name': name}
        menu_items.append(('Rename List', 'RunPlugin(%s)' % (_SALTS.build_plugin_url(queries))), )
        liz.addContextMenuItems(menu_items, replaceItems=True)

        xbmcplugin.addDirectoryItem(int(sys.argv[1]), liz_url, liz,isFolder=True,totalItems=totalItems)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    
@url_dispatcher.register(MODES.REMOVE_LIST, ['section', 'username', 'slug'])
def remove_list(section, username, slug):
    db_connection.delete_other_list(section, username, slug)
    xbmc.executebuiltin("XBMC.Container.Refresh")

@url_dispatcher.register(MODES.RENAME_LIST, ['section', 'slug', 'username', 'name'])
def rename_list(section, slug, username, name):
    keyboard = xbmc.Keyboard()
    keyboard.setHeading('Enter the new name (blank to reset)')
    keyboard.setDefault(name)
    keyboard.doModal()
    if keyboard.isConfirmed():
        new_name=keyboard.getText()
        db_connection.rename_other_list(section, username, slug, new_name)
    xbmc.executebuiltin("XBMC.Container.Refresh")
    
@url_dispatcher.register(MODES.ADD_OTHER_LIST, ['section'], ['username'])
def add_other_list(section, username=None):
    if username is None:
        keyboard = xbmc.Keyboard()
        keyboard.setHeading('Enter username of list owner')
        keyboard.doModal()
        if keyboard.isConfirmed():
            username=keyboard.getText()
    slug=pick_list(None, section, username)
    if slug:
        db_connection.add_other_list(section, username, slug)
    xbmc.executebuiltin("XBMC.Container.Refresh")

@url_dispatcher.register(MODES.SHOW_LIST, ['section', 'slug'], ['username'])
def show_list(section, slug, username=None):
    if slug == utils.WATCHLIST_SLUG:
        items = trakt_api.show_watchlist(section)
    else:
        items = trakt_api.show_list(slug, section, username)
    make_dir_from_list(section, items, slug)

@url_dispatcher.register(MODES.SHOW_WATCHLIST, ['section'])
def show_watchlist(section):
    show_list(section, utils.WATCHLIST_SLUG)

@url_dispatcher.register(MODES.SHOW_COLLECTION, ['section'])
def show_collection(section):
    items = trakt_api.get_collection(section, cached=_SALTS.get_setting('cache_collection')=='true')
    sort_key = int(_SALTS.get_setting('sort_collection'))
    if sort_key == 1:
        items.reverse()
    elif sort_key > 0:
        items.sort(key=lambda x:x[['title', 'year'][sort_key - 2]])
    make_dir_from_list(section, items, COLLECTION_SLUG)
    
def get_progress(cache_override=False):
    cached = _SALTS.get_setting('cache_watched') =='true' and not cache_override
    max_progress = int(_SALTS.get_setting('progress_size'))
    watched_list = trakt_api.get_watched(SECTIONS.TV, full=True, cached = cached)
    episodes = []
    for i, watched in enumerate(watched_list):
        if i != 0 and i >= max_progress:
            break
        
        progress = trakt_api.get_show_progress(watched['show']['ids']['slug'], full=True, cached = cached)
        if 'next_episode' in progress and progress['next_episode']:
            episode = {'show': watched['show'], 'episode': progress['next_episode']}
            episode['last_watched_at']=watched['last_watched_at']
            episode['percent_completed'] = (progress['completed'] * 100) / progress['aired'] if progress['aired']>0 else 0
            episode['completed']=progress['completed']
            episodes.append(episode)

    return utils.sort_progress(episodes, sort_order=SORT_MAP[int(_SALTS.get_setting('sort_progress'))])
    
@url_dispatcher.register(MODES.SHOW_PROGRESS)
def show_progress():
    for episode in get_progress():
        log_utils.log('Episode: Sort Keys: Tile: |%s| Last Watched: |%s| Percent: |%s%%| Completed: |%s|' % (episode['show']['title'], episode['last_watched_at'], episode['percent_completed'], episode['completed']), xbmc.LOGDEBUG)
        first_aired_utc = utils.iso_2_utc(episode['episode']['first_aired'])
        if _SALTS.get_setting('show_unaired_next')=='true' or first_aired_utc <=time.time():
            show=episode['show']
            fanart=show['images']['fanart']['full']
            date=utils.make_day(time.strftime('%Y-%m-%d', time.localtime(first_aired_utc)))
             
            menu_items=[]
            queries = {'mode': MODES.SEASONS, 'slug': show['ids']['slug'], 'fanart': fanart}
            menu_items.append(('Browse Seasons', 'Container.Update(%s)' % (_SALTS.build_plugin_url(queries))), )
             
            liz, liz_url = make_episode_item(show, episode['episode'], menu_items=menu_items)
            label=liz.getLabel()
            label = '[[COLOR deeppink]%s[/COLOR]] %s - %s' % (date, show['title'], label.decode('utf-8', 'replace'))
            liz.setLabel(label) 
        
            xbmcplugin.addDirectoryItem(int(sys.argv[1]), liz_url, liz,isFolder=(liz.getProperty('isPlayable')!='true'))        
    xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=False)

@url_dispatcher.register(MODES.MANAGE_SUBS, ['section'])
def manage_subscriptions(section):
    slug=_SALTS.get_setting('%s_sub_slug' % (section))
    if slug:
        next_run = utils.get_next_run(MODES.UPDATE_SUBS)
        label = 'Update Subscriptions: (Next Run: [COLOR %s]%s[/COLOR])'
        if _SALTS.get_setting('auto-'+MODES.UPDATE_SUBS) == 'true':
            color = 'green'
            run_str = next_run.strftime("%Y-%m-%d %I:%M:%S %p")
        else:
            color = 'red'
            run_str = 'DISABLED'
        label = label % (color, run_str)
        liz = xbmcgui.ListItem(label=label, iconImage=utils.art('update_subscriptions.png'), thumbnailImage=utils.art('update_subscriptions.png'))
        liz.setProperty('fanart_image', utils.art('fanart.jpg'))
        liz_url = _SALTS.build_plugin_url({'mode': MODES.UPDATE_SUBS, 'section': section})
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), liz_url, liz, isFolder=False)    
        if section == SECTIONS.TV:
            liz = xbmcgui.ListItem(label='Clean-Up Subscriptions', iconImage=utils.art('clean_up.png'), thumbnailImage=utils.art('clean_up.png'))
            liz.setProperty('fanart_image', utils.art('fanart.jpg'))
            liz_url = _SALTS.build_plugin_url({'mode': MODES.CLEAN_SUBS})
            xbmcplugin.addDirectoryItem(int(sys.argv[1]), liz_url, liz, isFolder=False)    
    show_pickable_list(slug, 'Pick a list to use for Subscriptions', MODES.PICK_SUB_LIST, section)

@url_dispatcher.register(MODES.SHOW_FAVORITES, ['section'])
def show_favorites(section):
    slug=_SALTS.get_setting('%s_fav_slug' % (section))
    show_pickable_list(slug, 'Pick a list to use for Favorites', MODES.PICK_FAV_LIST, section)

@url_dispatcher.register(MODES.PICK_SUB_LIST, ['mode', 'section'])
@url_dispatcher.register(MODES.PICK_FAV_LIST, ['mode', 'section'])
def pick_list(mode, section, username=None):
    slug=utils.choose_list(username)
    if slug:
        if mode == MODES.PICK_FAV_LIST:
            set_list(MODES.SET_FAV_LIST, slug, section)
        elif mode == MODES.PICK_SUB_LIST:
            set_list(MODES.SET_SUB_LIST, slug, section)
        else:
            return slug
        xbmc.executebuiltin("XBMC.Container.Refresh")

@url_dispatcher.register(MODES.SET_SUB_LIST, ['mode', 'slug', 'section'])
@url_dispatcher.register(MODES.SET_FAV_LIST, ['mode', 'slug', 'section'])
def set_list(mode, slug, section):
    if mode == MODES.SET_FAV_LIST:
        setting='%s_fav_slug' % (section)
    elif mode == MODES.SET_SUB_LIST:
        setting='%s_sub_slug' % (section)
    _SALTS.set_setting(setting, slug)

@url_dispatcher.register(MODES.SEARCH, ['section'])
def search(section, search_text=None):
    keyboard = xbmc.Keyboard()
    keyboard.setHeading('Search %s' % (section))
    while True:
        keyboard.doModal()
        if keyboard.isConfirmed():
            search_text = keyboard.getText()
            if not search_text:
                msg = 'Blank Searches are not allowed'
                builtin = 'XBMC.Notification(%s,%s, 5000, %s)'
                xbmc.executebuiltin(builtin % (_SALTS.get_name(), msg, ICON_PATH))
                return
            else:
                break
        else:
            break

    if keyboard.isConfirmed():
        search_text = keyboard.getText()
        utils.keep_search(section, search_text)
        queries = {'mode': MODES.SEARCH_RESULTS, 'section': section, 'query': search_text}
        pluginurl = _SALTS.build_plugin_url(queries)
        builtin = 'Container.Update(%s)' %(pluginurl)
        xbmc.executebuiltin(builtin)
    
@url_dispatcher.register(MODES.RECENT_SEARCH, ['section'])
def recent_searches(section):
    if section==SECTIONS.TV:
        search_img='television_search.png'
    else:
        search_img='movies_search.png'
    head = int(_SALTS.get_setting('%s_search_head' % (section)))
    for i in reversed(range(0,SEARCH_HISTORY)):
        index = (i + head + 1) % SEARCH_HISTORY
        search_text =db_connection.get_setting('%s_search_%s' % (section, index))
        if not search_text:
            break
        
        label = '[%s Search] %s' % (section, search_text)
        liz = xbmcgui.ListItem(label=label, iconImage=utils.art(search_img), thumbnailImage=utils.art(search_img))
        liz.setProperty('fanart_image', utils.art('fanart.png'))
        menu_items = []
        refresh_queries = {'mode': MODES.SAVE_SEARCH, 'section': section, 'query': search_text}
        menu_items.append(('Save Search', 'RunPlugin(%s)' % (_SALTS.build_plugin_url(refresh_queries))), )
        liz.addContextMenuItems(menu_items)
        queries = {'mode': MODES.SEARCH_RESULTS, 'section': section, 'query': search_text}
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), _SALTS.build_plugin_url(queries), liz, isFolder=True) 
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

@url_dispatcher.register(MODES.SAVED_SEARCHES, ['section'])
def saved_searches(section):
    if section==SECTIONS.TV:
        search_img='television_search.png'
    else:
        search_img='movies_search.png'
    for search in db_connection.get_searches(section, order_matters=True):
        label = '[%s Search] %s' % (section, search[1])
        liz = xbmcgui.ListItem(label=label, iconImage=utils.art(search_img), thumbnailImage=utils.art(search_img))
        liz.setProperty('fanart_image', utils.art('fanart.png'))
        menu_items = []
        refresh_queries = {'mode': MODES.DELETE_SEARCH, 'search_id': search[0]}
        menu_items.append(('Delete Search', 'RunPlugin(%s)' % (_SALTS.build_plugin_url(refresh_queries))), )
        liz.addContextMenuItems(menu_items)
        queries = {'mode': MODES.SEARCH_RESULTS, 'section': section, 'query': search[1]}
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), _SALTS.build_plugin_url(queries), liz, isFolder=True) 
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

@url_dispatcher.register(MODES.SAVE_SEARCH, ['section', 'query'])
def save_search(section, query):
    db_connection.save_search(section, query)

@url_dispatcher.register(MODES.DELETE_SEARCH, ['search_id'])
def delete_search(search_id):
    db_connection.delete_search(search_id)
    xbmc.executebuiltin("XBMC.Container.Refresh")

@url_dispatcher.register(MODES.SEARCH_RESULTS, ['section', 'query'], ['page'])
def search_results(section, query, page = 1):
    results = trakt_api.search(section, query, page)
    make_dir_from_list(section, results, query = {'mode': MODES.SEARCH_RESULTS, 'section': section, 'query': query}, page = page)

@url_dispatcher.register(MODES.SEASONS, ['slug', 'fanart'])
def browse_seasons(slug, fanart):
    seasons=trakt_api.get_seasons(slug)
    info={}
    if TOKEN:
        progress = trakt_api.get_show_progress(slug, cached=_SALTS.get_setting('cache_watched')=='true')
        info = utils.make_seasons_info(progress)

    totalItems=len(seasons)
    for season in seasons:
        if _SALTS.get_setting('show_season0') == 'true' or season['number'] != 0:
            liz=make_season_item(season, info.get(str(season['number']), {'season': season['number']}), slug, fanart)
            queries = {'mode': MODES.EPISODES, 'slug': slug, 'season': season['number']}
            liz_url = _SALTS.build_plugin_url(queries)
            xbmcplugin.addDirectoryItem(int(sys.argv[1]), liz_url, liz,isFolder=True,totalItems=totalItems)
    utils.set_view(CONTENT_TYPES.SEASONS, False)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

@url_dispatcher.register(MODES.EPISODES, ['slug', 'season'])
def browse_episodes(slug, season):
    show=trakt_api.get_show_details(slug)
    episodes=trakt_api.get_episodes(slug, season)
    if TOKEN:
        progress = trakt_api.get_show_progress(slug, cached=_SALTS.get_setting('cache_watched')=='true')
        episodes = utils.make_episodes_watched(episodes, progress)

    totalItems=len(episodes)
    now=time.time()
    for episode in episodes:
        utc_air_time = utils.iso_2_utc(episode['first_aired'])
        if _SALTS.get_setting('show_unaired')=='true' or utc_air_time <= now:
            if _SALTS.get_setting('show_unknown')=='true' or utc_air_time:
                liz, liz_url =make_episode_item(show, episode)
                xbmcplugin.addDirectoryItem(int(sys.argv[1]), liz_url, liz,isFolder=(liz.getProperty('isPlayable')!='true'),totalItems=totalItems)
    utils.set_view(CONTENT_TYPES.EPISODES, False)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

@url_dispatcher.register(MODES.GET_SOURCES, ['mode', 'video_type', 'title', 'year', 'slug'], ['season', 'episode', 'ep_title', 'dialog'])
@url_dispatcher.register(MODES.SELECT_SOURCE, ['mode', 'video_type', 'title', 'year', 'slug'], ['season', 'episode', 'ep_title'])
@url_dispatcher.register(MODES.DOWNLOAD_SOURCE, ['mode', 'video_type', 'title', 'year', 'slug'], ['season', 'episode', 'ep_title'])
def get_sources(mode, video_type, title, year, slug, season='', episode='', ep_title='', dialog=None):
    timeout = max_timeout = int(_SALTS.get_setting('source_timeout'))
    if max_timeout == 0: timeout=None
    max_results = int(_SALTS.get_setting('source_results'))
    worker_count=0
    hosters=[]
    workers=[]
    video=ScraperVideo(video_type, title, year, slug, season, episode, ep_title)
    if utils.P_MODE != P_MODES.NONE: q = utils.Queue()
    begin = time.time()
    fails={}
    got_timeouts = False
    for cls in utils.relevant_scrapers(video_type):
        if utils.P_MODE == P_MODES.NONE:
            hosters += cls(max_timeout).get_sources(video)
            if max_results> 0 and len(hosters) >= max_results:
                break
        else:
            worker=utils.start_worker(q, utils.parallel_get_sources, [cls, video])
            utils.increment_setting('%s_try' % (cls.get_name()))
            worker_count+=1
            workers.append(worker)
            fails[cls.get_name()]=True

    # collect results from workers
    if utils.P_MODE != P_MODES.NONE:
        while worker_count>0:
            try:
                log_utils.log('Calling get with timeout: %s' %(timeout), xbmc.LOGDEBUG)
                result = q.get(True, timeout)
                log_utils.log('Got %s Source Results' %(len(result['hosters'])), xbmc.LOGDEBUG)
                worker_count -=1
                hosters += result['hosters']
                del fails[result['name']]
                if max_timeout>0:
                    timeout = max_timeout - (time.time() - begin)
                    if timeout<0: timeout=0
            except utils.Empty:
                log_utils.log('Get Sources Process Timeout', xbmc.LOGWARNING)
                utils.record_timeouts(fails)
                got_timeouts=True
                break
            
            if max_results> 0 and len(hosters) >= max_results:
                log_utils.log('Exceeded max results: %s/%s' % (max_results, len(hosters)))
                break

        else:
            got_timeouts = False
            log_utils.log('All source results received')
        
    total = len(workers)
    timeouts = len(fails)
    workers=utils.reap_workers(workers)
    try:
        timeout_msg = 'Scraper Timeouts: %s/%s' % (timeouts, total) if got_timeouts and timeouts else ''
        if not hosters:
            log_utils.log('No Sources found for: |%s|' % (video))
            msg = ' (%s)' % timeout_msg if timeout_msg else ''
            builtin = 'XBMC.Notification(%s,No Sources Found%s, 5000, %s)'
            xbmc.executebuiltin(builtin % (_SALTS.get_name(), msg, ICON_PATH))
            return False

        if timeout_msg:
            builtin = 'XBMC.Notification(%s,%s, 5000, %s)'
            xbmc.executebuiltin(builtin % (_SALTS.get_name(), timeout_msg, ICON_PATH))
            
        hosters = utils.filter_exclusions(hosters)
        hosters = utils.filter_quality(video_type, hosters)
        
        if _SALTS.get_setting('enable_sort')=='true':
            if _SALTS.get_setting('filter-unknown')=='true':
                hosters = utils.filter_unknown_hosters(hosters)
        SORT_KEYS['source'] = utils.make_source_sort_key()
        hosters.sort(key = utils.get_sort_key)

        global urlresolver
        import urlresolver
        
        hosters = filter_unusable_hosters(hosters)
        
        if not hosters:
            log_utils.log('No Useable Sources found for: |%s|' % (video))
            msg = ' (%s)' % timeout_msg if timeout_msg else ''
            builtin = 'XBMC.Notification(%s,No Useable Sources Found%s, 5000, %s)'
            xbmc.executebuiltin(builtin % (_SALTS.get_name(), msg, ICON_PATH))
            return False
        
        pseudo_tv = xbmcgui.Window(10000).getProperty('PseudoTVRunning')
        if pseudo_tv=='True' or (mode == MODES.GET_SOURCES and _SALTS.get_setting('auto-play')=='true'):
            auto_play_sources(hosters, video_type, slug, season, episode)
        else:
            if dialog or (dialog is None and _SALTS.get_setting('source-win') == 'Dialog'):
                stream_url = pick_source_dialog(hosters)
                return play_source(mode, stream_url, video_type, slug, season, episode)
            else:
                pick_source_dir(mode, hosters, video_type, slug, season, episode)
    finally:
        utils.reap_workers(workers, None)

def filter_unusable_hosters(hosters):
    filtered_hosters=[]
    filter_max = int(_SALTS.get_setting('filter_unusable'))
    for i, hoster in enumerate(hosters):
        if i<filter_max and 'direct' in hoster and hoster['direct']==False:
            hmf = urlresolver.HostedMediaFile(host=hoster['host'], media_id='dummy') # use dummy media_id to force host validation
            if not hmf:
                log_utils.log('Unusable source %s (%s) from %s' % (hoster['url'], hoster['host'], hoster['class'].get_name()), xbmc.LOGINFO)
                continue
        filtered_hosters.append(hoster)
    return filtered_hosters
    
@url_dispatcher.register(MODES.RESOLVE_SOURCE, ['mode', 'class_url', 'video_type', 'slug', 'class_name'], ['season', 'episode'])
@url_dispatcher.register(MODES.DIRECT_DOWNLOAD, ['mode', 'class_url', 'video_type', 'slug', 'class_name'], ['season', 'episode'])
def resolve_source(mode, class_url, video_type, slug, class_name, season='', episode=''):
    for cls in utils.relevant_scrapers(video_type):
        if cls.get_name() == class_name:
            scraper_instance=cls()
            break
    else:
        log_utils.log('Unable to locate scraper with name: %s' % (class_name))
        return False
        
    hoster_url = scraper_instance.resolve_link(class_url)
    if mode == MODES.DIRECT_DOWNLOAD:
        _SALTS.end_of_directory()
    return play_source(mode, hoster_url, video_type, slug, season, episode)

@url_dispatcher.register(MODES.PLAY_TRAILER,['stream_url'])
def play_trailer(stream_url):
    xbmc.Player().play(stream_url)

def download_subtitles(language, title, year, season, episode):
    srt_scraper=SRT_Scraper()
    tvshow_id=srt_scraper.get_tvshow_id(title, year)
    if tvshow_id is None:
        return
     
    subs=srt_scraper.get_episode_subtitles(language, tvshow_id, season, episode)
    sub_labels=[]
    for sub in subs:
        sub_labels.append(utils.format_sub_label(sub))
     
    index=0
    if len(sub_labels)>1:
        dialog = xbmcgui.Dialog()       
        index = dialog.select('Choose a subtitle to download', sub_labels)
         
    if subs and index > -1:
        return srt_scraper.download_subtitle(subs[index]['url'])
    
def play_source(mode, hoster_url, video_type, slug, season='', episode=''):
    global urlresolver
    import urlresolver

    if hoster_url is None:
        return False

    hmf = urlresolver.HostedMediaFile(url=hoster_url)
    if not hmf:
        log_utils.log('hoster_url not supported by urlresolver: %s' % (hoster_url))
        stream_url = hoster_url
    else:
        stream_url = hmf.resolve()
        if not stream_url or not isinstance(stream_url, basestring):
            try: msg = stream_url.msg
            except: msg = hoster_url
            builtin = 'XBMC.Notification(%s,Link Resolve Failed: %s, 7500, %s)'
            xbmc.executebuiltin(builtin % (_SALTS.get_name(), msg, ICON_PATH))
            return False

    resume_point = 0
    if mode not in [MODES.DOWNLOAD_SOURCE, MODES.DIRECT_DOWNLOAD]:
        if utils.bookmark_exists(slug, season, episode):
            if utils.get_resume_choice(slug, season, episode):
                resume_point = utils.get_bookmark(slug, season, episode)
                log_utils.log('Resume Point: %s' % (resume_point), xbmc.LOGDEBUG)
        
    try:
        win = xbmcgui.Window(10000)
        win.setProperty('salts.playing', 'True')
        win.setProperty('salts.playing.slug', slug)
        win.setProperty('salts.playing.season', str(season))
        win.setProperty('salts.playing.episode', str(episode))
        if _SALTS.get_setting('trakt_bookmark')=='true':
            win.setProperty('salts.playing.trakt_resume', str(resume_point))

        art={'thumb': '', 'fanart': ''}
        info={}
        show_meta = {}
        if video_type == VIDEO_TYPES.EPISODE:
            path = _SALTS.get_setting('tv-download-folder')
            file_name = utils.filename_from_title(slug, VIDEO_TYPES.TVSHOW)
            file_name = file_name % ('%02d' % int(season), '%02d' % int(episode))
            
            ep_meta = trakt_api.get_episode_details(slug, season, episode)
            show_meta = trakt_api.get_show_details(slug)
            people = trakt_api.get_people(SECTIONS.TV, slug) if _SALTS.get_setting('include_people')=='true' else None
            info = utils.make_info(ep_meta, show_meta, people)
            images={}
            images['images']=show_meta['images']
            images['images'].update(ep_meta['images'])
            art=utils.make_art(images)
            
            path = make_path(path, VIDEO_TYPES.TVSHOW, show_meta['title'], season=season)
            file_name = utils.filename_from_title(show_meta['title'], VIDEO_TYPES.TVSHOW)
            file_name = file_name % ('%02d' % int(season), '%02d' % int(episode))
        else:
            path = _SALTS.get_setting('movie-download-folder')
            file_name = utils.filename_from_title(slug, video_type)
            
            item = trakt_api.get_movie_details(slug)
            people = trakt_api.get_people(SECTIONS.MOVIES, slug) if _SALTS.get_setting('include_people')=='true' else None
            info = utils.make_info(item, people=people)
            art=utils.make_art(item)
            
            path = make_path(path, video_type, item['title'], item['year'])
            file_name = utils.filename_from_title(item['title'], video_type, item['year'])
    except TransientTraktError as e:
        log_utils.log('During Playback: %s' % (str(e)), xbmc.LOGWARNING) # just log warning if trakt calls fail and leave meta and art blank
    
    if mode in [MODES.DOWNLOAD_SOURCE, MODES.DIRECT_DOWNLOAD]:
        utils.download_media(stream_url, path, file_name)
        return True
    
    if video_type == VIDEO_TYPES.EPISODE and utils.srt_download_enabled() and show_meta:
        srt_path = download_subtitles(_SALTS.get_setting('subtitle-lang'), show_meta['title'], show_meta['year'], season, episode)
        if utils.srt_show_enabled() and srt_path:
            log_utils.log('Setting srt path: %s' % (srt_path), xbmc.LOGDEBUG)
            win.setProperty('salts.playing.srt', srt_path)

    listitem = xbmcgui.ListItem(path=stream_url, iconImage=art['thumb'], thumbnailImage=art['thumb'])
    if _SALTS.get_setting('trakt_bookmark')!='true':
        listitem.setProperty('ResumeTime', str(resume_point))
        listitem.setProperty('Totaltime', str(99999)) # dummy value to force resume to work
    listitem.setProperty('fanart_image', art['fanart'])
    try: listitem.setArt(art)
    except:pass
    listitem.setProperty('IsPlayable', 'true')
    listitem.setPath(stream_url)
    listitem.setInfo('video', info)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
    return True

def auto_play_sources(hosters, video_type, slug, season, episode):
    for item in hosters:
        if item['multi-part']:
            continue

        hoster_url=item['class'].resolve_link(item['url'])
        log_utils.log('Auto Playing: %s' % (hoster_url), xbmc.LOGDEBUG)
        if play_source(MODES.GET_SOURCES, hoster_url, video_type, slug, season, episode):
            return True
    else:
        msg = 'All sources failed to play'
        log_utils.log(msg, xbmc.LOGERROR)
        builtin = 'XBMC.Notification(%s,%s, 5000, %s)'
        xbmc.executebuiltin(builtin % (_SALTS.get_name(), msg, ICON_PATH))

def pick_source_dialog(hosters):
    for item in hosters:
        if item['multi-part']:
            continue

        label = item['class'].format_source_label(item)
        label = '[%s] %s' % (item['class'].get_name(),label)
        item['label']=label
    
    dialog = xbmcgui.Dialog() 
    index = dialog.select('Choose your stream', [item['label'] for item in hosters if 'label' in item])
    if index>-1:
        try:
            if hosters[index]['url']:
                hoster_url=hosters[index]['class'].resolve_link(hosters[index]['url'])
                log_utils.log('Attempting to play url: %s' % hoster_url)
                return hoster_url
        except Exception as e:
            log_utils.log('Error (%s) while trying to resolve %s' % (str(e), hosters[index]['url']), xbmc.LOGERROR)
    
def pick_source_dir(mode, hosters, video_type, slug, season='', episode=''):
    if mode == MODES.DOWNLOAD_SOURCE:
        next_mode = MODES.DIRECT_DOWNLOAD
        folder = True
    else:
        next_mode = MODES.RESOLVE_SOURCE
        folder = False

    hosters_len=len(hosters)
    for item in hosters:
        if item['multi-part']:
            continue

        label = item['class'].format_source_label(item)
        label = '[%s] %s' % (item['class'].get_name(),label)
        item['label']=label
    
        #log_utils.log(item, xbmc.LOGDEBUG)
        queries={'mode': next_mode, 'class_url': item['url'], 'video_type': video_type, 'slug': slug, 'season': season, 'episode': episode, 'class_name': item['class'].get_name()}
        _SALTS.add_directory(queries, infolabels={'title': item['label']}, is_folder=folder, img='', fanart='', total_items=hosters_len)
    
    _SALTS.end_of_directory()

@url_dispatcher.register(MODES.SET_URL_MANUAL, ['mode', 'video_type', 'title', 'year', 'slug'], ['season', 'episode', 'ep_title'])
@url_dispatcher.register(MODES.SET_URL_SEARCH, ['mode', 'video_type', 'title', 'year', 'slug'], ['season', 'episode', 'ep_title'])
def set_related_url(mode, video_type, title, year, slug, season='', episode='', ep_title=''):
    related_list=[]
    timeout = max_timeout = int(_SALTS.get_setting('source_timeout'))
    if max_timeout == 0: timeout=None
    worker_count=0
    workers=[]
    if utils.P_MODE != P_MODES.NONE: q = utils.Queue()
    begin = time.time()
    video=ScraperVideo(video_type, title, year, slug, season, episode, ep_title)
    for cls in utils.relevant_scrapers(video_type, order_matters=True):
        if utils.P_MODE == P_MODES.NONE:
            related={}
            related['class']=cls(max_timeout)
            url=related['class'].get_url(video)
            if not url: url=''
            related['url']=url
            related['name']=related['class'].get_name()
            related['label'] = '[%s] %s' % (related['name'], related['url'])
            related_list.append(related)
        else:
            worker = utils.start_worker(q, utils.parallel_get_url, [cls, video])
            utils.increment_setting('%s_try' % (cls.get_name()))
            worker_count += 1
            workers.append(worker)
            related={'class': cls(max_timeout), 'name': cls.get_name(), 'label': '[%s]' % (cls.get_name()), 'url': ''}
            related_list.append(related)
    
    # collect results from workers
    if utils.P_MODE != P_MODES.NONE:
        fails = dict.fromkeys([item['name'] for item in related_list], True)
        while worker_count>0:
            try:
                log_utils.log('Calling get with timeout: %s' %(timeout), xbmc.LOGDEBUG)
                result = q.get(True, timeout)
                log_utils.log('Got result: %s' %(result), xbmc.LOGDEBUG)
                #related_list.append(result)
                for i, item in enumerate(related_list):
                    if item['name']==result['name']:
                        related_list[i]=result
                        del fails[result['name']] 
                worker_count -=1
                if max_timeout>0:
                    timeout = max_timeout - (time.time() - begin)
                    if timeout<0: timeout=0
            except utils.Empty:
                log_utils.log('Get Url Timeout', xbmc.LOGWARNING)
                utils.record_timeouts(fails)
                break
        else:
            log_utils.log('All source results received')

    total = len(workers)
    timeouts = len(fails)
    timeout_msg = 'Scraper Timeouts: %s/%s' % (timeouts, total) if timeouts else ''
    if timeout_msg:
        builtin = 'XBMC.Notification(%s,%s, 5000, %s)'
        xbmc.executebuiltin(builtin % (_SALTS.get_name(), timeout_msg, ICON_PATH))
        for related in related_list:
            if related['name'] in fails:
                related['label']='[COLOR darkred]%s[/COLOR]' % (related['label'])

    workers=utils.reap_workers(workers)
    try:
        dialog=xbmcgui.Dialog()
        index = dialog.select('Url To Change (%s)' % (video_type), [related['label'] for related in related_list])
        if index>-1:
            if mode == MODES.SET_URL_MANUAL:
                keyboard = xbmc.Keyboard()
                keyboard.setHeading('Related %s url at %s' % (video_type, related_list[index]['name']))
                keyboard.setDefault(related_list[index]['url'])
                keyboard.doModal()
                if keyboard.isConfirmed():
                    new_url = keyboard.getText()
                    utils.update_url(video_type, title, year, related_list[index]['name'], related_list[index]['url'], new_url, season, episode)
                    builtin = 'XBMC.Notification(%s,[COLOR blue]%s[/COLOR] Related Url Set, 5000, %s)'
                    xbmc.executebuiltin(builtin % (_SALTS.get_name(), related_list[index]['name'], ICON_PATH))
            elif mode == MODES.SET_URL_SEARCH:
                temp_title = title
                temp_year = year
                while True:
                    dialog=xbmcgui.Dialog()
                    choices = ['Manual Search']
                    try:
                        log_utils.log('Searching for: |%s|%s|' % (temp_title, temp_year), xbmc.LOGDEBUG)
                        results = related_list[index]['class'].search(video_type, temp_title, temp_year)
                        for result in results:
                            choice = result['title']
                            if result['year']: choice = '%s (%s)' % (choice, result['year'])
                            choices.append(choice)
                        results_index = dialog.select('Select Related', choices)
                        if results_index==0:
                            keyboard = xbmc.Keyboard()
                            keyboard.setHeading('Enter Search')
                            text = temp_title
                            if temp_year: text = '%s (%s)' % (text, temp_year)
                            keyboard.setDefault(text)
                            keyboard.doModal()
                            if keyboard.isConfirmed():
                                match = re.match('([^\(]+)\s*\(*(\d{4})?\)*', keyboard.getText())
                                temp_title = match.group(1).strip()
                                temp_year = match.group(2) if match.group(2) else '' 
                        elif results_index>0:
                            utils.update_url(video_type, title, year, related_list[index]['name'], related_list[index]['url'], results[results_index-1]['url'], season, episode)
                            builtin = 'XBMC.Notification(%s,[COLOR blue]%s[/COLOR] Related Url Set, 5000, %s)'
                            xbmc.executebuiltin(builtin % (_SALTS.get_name(), related_list[index]['name'], ICON_PATH))
                            break
                        else:
                            break
                    except NotImplementedError:
                        log_utils.log('%s Scraper does not support searching.' % (related_list[index]['class'].get_name()))
                        builtin = 'XBMC.Notification(%s,%s Scraper does not support searching, 5000, %s)'
                        xbmc.executebuiltin(builtin % (_SALTS.get_name(), related_list[index]['class'].get_name(), ICON_PATH))
                        break
    finally:
        utils.reap_workers(workers, None)

@url_dispatcher.register(MODES.RATE, ['section', 'id_type', 'show_id'], ['season', 'episode'])
def rate_media(section, id_type, show_id, season='', episode=''):
    # disabled until fixes for rating are made in official addon
    if False and xbmc.getCondVisibility('System.HasAddon(script.trakt)'):
        run = 'RunScript(script.trakt, action=rate, media_type=%s, remoteid=%s'
        if section == SECTIONS.MOVIES:
            run = (run + ')') % ('movie', show_id)
        else:
            if season and episode:
                run = (run +', season=%s, episode=%s)') % ('episode', show_id, season, episode)
            else:
                run = (run + ')') % ('show', show_id)
        xbmc.executebuiltin(run)
    else:
        item = {id_type: show_id}
        keyboard = xbmc.Keyboard()
        keyboard.setHeading('Enter Rating (unrate, or 1-10)')
        while True:
            keyboard.doModal()
            if keyboard.isConfirmed():
                rating = keyboard.getText()
                rating = rating.lower()
                if rating in ['unrate'] + [str(i) for i in range(1, 11)]:
                    break
            else:
                return
             
        if rating == 'unrate': rating = None
        trakt_api.rate(section, item, rating, season, episode)

@url_dispatcher.register(MODES.EDIT_TVSHOW_ID, ['title'], ['year'])
def edit_tvshow_id(title, year=''):
    srt_scraper=SRT_Scraper()
    tvshow_id=srt_scraper.get_tvshow_id(title, year)
    keyboard = xbmc.Keyboard()
    keyboard.setHeading('Input TVShow ID')
    if tvshow_id:
        keyboard.setDefault(str(tvshow_id))
    keyboard.doModal()
    if keyboard.isConfirmed():
        db_connection.set_related_url(VIDEO_TYPES.TVSHOW, title, year, SRT_SOURCE, keyboard.getText())
                
@url_dispatcher.register(MODES.REM_FROM_LIST, ['slug', 'section', 'id_type', 'show_id'])
def remove_from_list(slug, section, id_type, show_id):
    item={'type': TRAKT_SECTIONS[section][:-1], id_type: show_id}
    remove_many_from_list(section, item, slug)
    xbmc.executebuiltin("XBMC.Container.Refresh")
    
def remove_many_from_list(section, items, slug):
    if slug==utils.WATCHLIST_SLUG:
        response=trakt_api.remove_from_watchlist(section, items)
    else:
        response=trakt_api.remove_from_list(section, slug, items)
    return response
    
@url_dispatcher.register(MODES.ADD_TO_COLL, ['mode', 'section', 'id_type', 'show_id'])
@url_dispatcher.register(MODES.REM_FROM_COLL, ['mode', 'section', 'id_type', 'show_id'])
def manage_collection(mode, section, id_type, show_id):
    item={id_type: show_id}
    if mode == MODES.ADD_TO_COLL:
        trakt_api.add_to_collection(section, item)
        msg = 'Item Added to Collection'
    else:
        trakt_api.remove_from_collection(section, item)
        msg = 'Item Removed from Collection'
    builtin = "XBMC.Notification(%s,%s, 2000, %s)" % (_SALTS.get_name(), msg, ICON_PATH)
    xbmc.executebuiltin(builtin)
    xbmc.executebuiltin("XBMC.Container.Refresh")

@url_dispatcher.register(MODES.ADD_TO_LIST, ['section', 'id_type', 'show_id'], ['slug'])
def add_to_list(section, id_type, show_id, slug=None):
    add_many_to_list(section, {id_type: show_id}, slug)
    builtin = "XBMC.Notification(%s,Item Added to List, 2000, %s)" % (_SALTS.get_name(), ICON_PATH)
    xbmc.executebuiltin(builtin)
    xbmc.executebuiltin("XBMC.Container.Refresh")

def add_many_to_list(section, items, slug=None):
    if not slug: slug=utils.choose_list()
    if slug==utils.WATCHLIST_SLUG:
        response=trakt_api.add_to_watchlist(section, items)
    elif slug:
        response=trakt_api.add_to_list(section, slug, items)
    return response
    
@url_dispatcher.register(MODES.COPY_LIST, ['section', 'slug'], ['username', 'target_slug'])
def copy_list(section, slug, username=None, target_slug=None):
    if slug == COLLECTION_SLUG:
        items = trakt_api.get_collection(section)
    else:
        items = trakt_api.show_list(slug, section, username)
    copy_items=[]
    for item in items:
        query=utils.show_id(item)
        copy_item={'type': TRAKT_SECTIONS[section][:-1], query['id_type']: query['show_id']}
        copy_items.append(copy_item)
    response=add_many_to_list(section, copy_items, target_slug)
    builtin = "XBMC.Notification(%s,List Copied: (A:%s/ E:%s/ S:%s), 5000, %s)" % (_SALTS.get_name(), response['inserted'], response['already_exist'], response['skipped'], ICON_PATH)
    xbmc.executebuiltin(builtin)

@url_dispatcher.register(MODES.TOGGLE_TITLE, ['slug'])
def toggle_title(slug):
    filter_list = utils.get_force_title_list()
    if slug in filter_list:
        del filter_list[filter_list.index(slug)]
    else:
        filter_list.append(slug)
    filter_str = '|'.join(filter_list)
    _SALTS.set_setting('force_title_match', filter_str)
    xbmc.executebuiltin("XBMC.Container.Refresh")

@url_dispatcher.register(MODES.TOGGLE_WATCHED, ['section', 'id_type', 'show_id'], ['watched', 'season', 'episode'])
def toggle_watched(section, id_type, show_id, watched=True, season='', episode=''):
    log_utils.log('In Watched: |%s|%s|%s|%s|%s|%s|' % (section, id_type, show_id, season, episode, watched), xbmc.LOGDEBUG)
    item = {id_type: show_id}
    trakt_api.set_watched(section, item, season, episode, watched)
    w_str='Watched' if watched else 'Unwatched'
    builtin = "XBMC.Notification(%s,Marked as %s,5000,%s)" % (_SALTS.get_name(), w_str, ICON_PATH)
    xbmc.executebuiltin(builtin)
    xbmc.executebuiltin("XBMC.Container.Refresh")

@url_dispatcher.register(MODES.URL_EXISTS, ['slug'])
def toggle_url_exists(slug):
    show_str = _SALTS.get_setting('exists_list')
    if show_str:
        show_list = show_str.split('|')
    else:
        show_list = []

    if slug in show_list:
        show_list.remove(slug)
    else:
        show_list.append(slug)

    show_str = '|'.join(show_list)
    _SALTS.set_setting('exists_list', show_str)
    xbmc.executebuiltin("XBMC.Container.Refresh")

@url_dispatcher.register(MODES.UPDATE_SUBS)
def update_subscriptions():
    log_utils.log('Updating Subscriptions', xbmc.LOGDEBUG)
    dialog = None
    if _SALTS.get_setting(MODES.UPDATE_SUBS+'-notify')=='true':
        dialog = xbmcgui.DialogProgressBG()
        dialog.create('Stream All The Sources', 'Updating Subscriptions...')
        dialog.update(0)

    update_strms(SECTIONS.TV, dialog)
    if _SALTS.get_setting('include_movies') == 'true':
        update_strms(SECTIONS.MOVIES, dialog)
    if _SALTS.get_setting('library-update') == 'true':
        xbmc.executebuiltin('UpdateLibrary(video)')
    if _SALTS.get_setting('cleanup-subscriptions') == 'true':
        clean_subs()

    now = datetime.datetime.now()
    db_connection.set_setting('%s-last_run' % MODES.UPDATE_SUBS, now.strftime("%Y-%m-%d %H:%M:%S.%f"))

    if _SALTS.get_setting(MODES.UPDATE_SUBS+'-notify')=='true':
        dialog.close()
        if _SALTS.get_setting('auto-'+MODES.UPDATE_SUBS)=='true':
            builtin = "XBMC.Notification(%s,Next Update in %0.1f hours,5000, %s)" % (_SALTS.get_name(), float(_SALTS.get_setting(MODES.UPDATE_SUBS+'-interval')), ICON_PATH)
            xbmc.executebuiltin(builtin)
    xbmc.executebuiltin("XBMC.Container.Refresh")
    
def update_strms(section, dialog=None):
    section_params = utils.get_section_params(section)
    slug=_SALTS.get_setting('%s_sub_slug' % (section))
    if not slug:
        return
    elif slug == utils.WATCHLIST_SLUG:
        items = trakt_api.show_watchlist(section)
    else:
        items = trakt_api.show_list(slug, section)
    
    length=len(items)
    for i, item in enumerate(items):
        if dialog:
            percent_progress = i*100 / length
            dialog.update(percent_progress, 'Stream All The Sources', 'Updating %s: %s (%s)' % (section, re.sub(' \(\d{4}\)$','',item['title']), item['year']))
        add_to_library(section_params['video_type'], item['title'], item['year'], item['ids']['slug'])

@url_dispatcher.register(MODES.CLEAN_SUBS)
def clean_subs():
    slug=_SALTS.get_setting('TV_sub_slug')
    if not slug:
        return
    elif slug == utils.WATCHLIST_SLUG:
        items = trakt_api.show_watchlist(SECTIONS.TV)
    else:
        items = trakt_api.show_list(slug, SECTIONS.TV)
    
    del_items = []
    for item in items:
        show_slug=item['ids']['slug']
        show=trakt_api.get_show_details(show_slug)
        if show['status'].upper()=='ENDED':
            show_id = utils.show_id(item)
            del_items.append({show_id['id_type']:show_id['show_id']})
            
    if del_items:
        if slug == utils.WATCHLIST_SLUG:
            trakt_api.remove_from_watchlist(SECTIONS.TV, del_items)
        else:
            trakt_api.remove_from_list(SECTIONS.TV, slug, del_items)

@url_dispatcher.register(MODES.FLUSH_CACHE)
def flush_cache():
    dlg = xbmcgui.Dialog()
    ln1 = 'Are you sure you want to delete the url cache?'
    ln2 = 'This will slow things down until all urls are re-cached'
    ln3 = ''
    yes = 'Keep'
    no = 'Delete'
    if dlg.yesno('Flush web cache', ln1, ln2, ln3, yes, no):
        db_connection.flush_cache()

@url_dispatcher.register(MODES.RESET_DB)
def reset_db():
    if db_connection.reset_db():
        message='DB Reset Successful'
    else:
        message='Reset only allowed on sqlite DBs'
    
    builtin = "XBMC.Notification(PrimeWire,%s,2000, %s)" % (message, ICON_PATH)
    xbmc.executebuiltin(builtin)        

@url_dispatcher.register(MODES.EXPORT_DB)
def export_db():
    try:
        dialog = xbmcgui.Dialog()
        export_path = dialog.browse(0, 'Select Export Directory', 'files')
        if export_path:
            export_path = xbmc.translatePath(export_path)
            keyboard = xbmc.Keyboard('export.csv', 'Enter Export Filename')
            keyboard.doModal()
            if keyboard.isConfirmed():
                export_filename = keyboard.getText()
                export_file = export_path + export_filename
                db_connection.export_from_db(export_file)
                builtin = "XBMC.Notification(Export Successful,Exported to %s,2000, %s)" % (export_file, ICON_PATH)
                xbmc.executebuiltin(builtin)
    except Exception as e:
        log_utils.log('Export Failed: %s' % (e), xbmc.LOGERROR)
        builtin = "XBMC.Notification(Export,Export Failed,2000, %s)" % (ICON_PATH)
        xbmc.executebuiltin(builtin)

@url_dispatcher.register(MODES.IMPORT_DB)
def import_db():
    try:
        dialog = xbmcgui.Dialog()
        import_file = dialog.browse(1, 'Select Import File', 'files')
        if import_file:
            import_file = xbmc.translatePath(import_file)
            db_connection.import_into_db(import_file)
            builtin = "XBMC.Notification(Import Success,Imported from %s,5000, %s)" % (import_file, ICON_PATH)
            xbmc.executebuiltin(builtin)
    except Exception as e:
        log_utils.log('Import Failed: %s' % (e), xbmc.LOGERROR)
        builtin = "XBMC.Notification(Import,Import Failed,2000, %s)" % (ICON_PATH)
        xbmc.executebuiltin(builtin)
        raise

@url_dispatcher.register(MODES.ADD_TO_LIBRARY, ['video_type', 'title', 'year', 'slug'])
def add_to_library(video_type, title, year, slug):
    log_utils.log('Creating .strm for |%s|%s|%s|%s|' % (video_type, title, year, slug), xbmc.LOGDEBUG)
    if video_type == VIDEO_TYPES.TVSHOW:
        save_path = _SALTS.get_setting('tvshow-folder')
        save_path = xbmc.translatePath(save_path)
        show = trakt_api.get_show_details(slug)
        show['title'] = re.sub(' \(\d{4}\)$','',show['title']) # strip off year if it's part of show title
        seasons = trakt_api.get_seasons(slug)
        include_unknown = _SALTS.get_setting('include_unknown')=='true'

        if not seasons:
            log_utils.log('No Seasons found for %s (%s)' % (show['title'], show['year']), xbmc.LOGERROR)

        for season in seasons:
            season_num = season['number']
            if _SALTS.get_setting('include_specials')=='true' or season_num != 0: 
                episodes = trakt_api.get_episodes(slug, season_num)
                for episode in episodes:
                    if utils.show_requires_source(slug):
                        require_source=True
                    else:
                        if (episode['first_aired'] != None and utils.iso_2_utc(episode['first_aired'])<=time.time()) or (include_unknown and episode['first_aired'] == None):
                            require_source = False
                        else:
                            continue
                    
                    ep_num = episode['number']
                    filename = utils.filename_from_title(show['title'], video_type)
                    filename = filename % ('%02d' % int(season_num), '%02d' % int(ep_num))
                    final_path = os.path.join(make_path(save_path, video_type, show['title'], season=season_num), filename)
                    strm_string = _SALTS.build_plugin_url({'mode': MODES.GET_SOURCES, 'video_type': VIDEO_TYPES.EPISODE, 'title': title, 'year': year, 'season': season_num, 
                                                           'episode': ep_num, 'slug': slug, 'ep_title': episode['title'], 'dialog': True})
                    write_strm(strm_string, final_path, VIDEO_TYPES.EPISODE, show['title'], show['year'], slug, season_num, ep_num, require_source=require_source)
                
    elif video_type == VIDEO_TYPES.MOVIE:
        save_path = _SALTS.get_setting('movie-folder')
        save_path = xbmc.translatePath(save_path)
        strm_string = _SALTS.build_plugin_url({'mode': MODES.GET_SOURCES, 'video_type': video_type, 'title': title, 'year': year, 'slug': slug, 'dialog': True})
        filename = utils.filename_from_title(title, VIDEO_TYPES.MOVIE, year)
        final_path = os.path.join(make_path(save_path, video_type, title, year), filename)
        write_strm(strm_string, final_path, VIDEO_TYPES.MOVIE, title, year, slug, require_source=_SALTS.get_setting('require_source')=='true')

def make_path(base_path, video_type, title, year = '', season = ''):
    path = base_path
    if video_type == VIDEO_TYPES.TVSHOW:
        show_folder = re.sub(r'([^\w\-_\. ]|\.$)', '_', title)
        path = os.path.join(base_path, show_folder, 'Season %s' % (season))
    else:
        dir_name = title if not year else '%s (%s)' % (title, year)
        path = os.path.join(base_path, dir_name)
    return path

def write_strm(stream, path, video_type, title, year, slug, season='', episode='', require_source=False):
    path = xbmc.makeLegalFilename(path)
    if not xbmcvfs.exists(os.path.dirname(path)):
        try:
            try: xbmcvfs.mkdirs(os.path.dirname(path))
            except: os.mkdir(os.path.dirname(path))
        except Exception as e:
            log_utils.log('Failed to create directory %s: %s' % path, xbmc.LOGERROR, str(e))

    old_strm_string=''
    try:
        f = xbmcvfs.File(path, 'r')
        old_strm_string = f.read()
        f.close()
    except:  pass
    
    #print "Old String: %s; New String %s" %(old_strm_string,strm_string)
    # string will be blank if file doesn't exist or is blank
    if stream != old_strm_string:
        try:
            if not require_source or utils.url_exists(ScraperVideo(video_type, title, year, slug, season, episode)):
                log_utils.log('Writing strm: %s' % stream)
                file_desc = xbmcvfs.File(path, 'w')
                file_desc.write(stream)
                file_desc.close()
            else:
                log_utils.log('No strm written for |%s|%s|%s|%s|%s|' % (video_type, title, year, season, episode), xbmc.LOGWARNING)
        except Exception as e:
            log_utils.log('Failed to create .strm file (%s): %s' % (path, e), xbmc.LOGERROR)
    
def show_pickable_list(slug, pick_label, pick_mode, section):
    if not slug:
        liz = xbmcgui.ListItem(label=pick_label)
        liz_url = _SALTS.build_plugin_url({'mode': pick_mode, 'section': section})
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), liz_url, liz, isFolder=False)    
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
    else:
        show_list(section, slug)

def make_dir_from_list(section, list_data, slug=None, query = None, page = None):
    section_params=utils.get_section_params(section)
    totalItems=len(list_data)
    
    cache_watched = _SALTS.get_setting('cache_watched')=='true'
    watched={}
    in_collection={}
    if TOKEN:
        watched_history = trakt_api.get_watched(section, cached=cache_watched)
        for item in watched_history:
            if section == SECTIONS.MOVIES:
                watched[item['movie']['ids']['slug']] = item['plays']>0
            else:
                watched[item['show']['ids']['slug']] = len([e for s in item['seasons'] if s['number'] != 0 for e in s['episodes']]) 
        collection = trakt_api.get_collection(section, full=False, cached=_SALTS.get_setting('cache_collection')=='true')
        in_collection = dict.fromkeys([show['ids']['slug'] for show in collection], True)

    for show in list_data:
        menu_items=[]
        show_id=utils.show_id(show)
        if slug and slug != COLLECTION_SLUG:
            queries = {'mode': MODES.REM_FROM_LIST, 'slug': slug, 'section': section}
            queries.update(show_id)
            menu_items.append(('Remove from List', 'RunPlugin(%s)' % (_SALTS.build_plugin_url(queries))), )
                
        sub_slug=_SALTS.get_setting('%s_sub_slug' % (section))
        if TOKEN and sub_slug:
            if sub_slug != slug:
                queries = {'mode': MODES.ADD_TO_LIST, 'section': section_params['section'], 'slug': sub_slug}
                queries.update(show_id)
                menu_items.append(('Subscribe', 'RunPlugin(%s)' % (_SALTS.build_plugin_url(queries))), )
            elif section == SECTIONS.TV:
                show_slug = show['ids']['slug']
                if utils.show_requires_source(show_slug):
                    label='Require Aired Only?'
                else:
                    label = 'Require Page Only?'
                queries = {'mode': MODES.URL_EXISTS, 'slug': show_slug}                
                menu_items.append((label, 'RunPlugin(%s)' % (_SALTS.build_plugin_url(queries))), )
        
        if section == SECTIONS.MOVIES:
            show['watched'] = watched.get(show['ids']['slug'], False)
        else:
            try:
                show['watched'] = watched[show['ids']['slug']] >= show['aired_episodes']
                show['watched_count'] = watched[show['ids']['slug']]
            except: show['watched'] = False

        show['in_collection']=in_collection.get(show['ids']['slug'],False)
            
        liz, liz_url = make_item(section_params, show, menu_items)
        
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), liz_url, liz, isFolder=section_params['folder'], totalItems=totalItems)

    if query and page and totalItems>=int(_SALTS.get_setting('list_size')):
        meta = {'title': 'Next Page >>'}
        query['page']=int(page) + 1
        _SALTS.add_directory(query, meta, img=utils.art('nextpage.png'), fanart=utils.art('fanart.jpg'), is_folder=True)

    utils.set_view(section_params['content_type'], False)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def make_dir_from_cal(mode, start_date, days):
    try: start_date=datetime.datetime.strptime(start_date,'%Y-%m-%d')
    except TypeError: start_date = datetime.datetime(*(time.strptime(start_date, '%Y-%m-%d')[0:6]))
    last_week = start_date - datetime.timedelta(days=7)
    next_week = start_date + datetime.timedelta(days=7)
    last_str = datetime.datetime.strftime(last_week, '%Y-%m-%d')
    next_str = datetime.datetime.strftime(next_week, '%Y-%m-%d')
    
    liz = xbmcgui.ListItem(label='<< Previous Week', iconImage=utils.art('previous.png'), thumbnailImage=utils.art('previous.png'))
    liz.setProperty('fanart_image', utils.art('fanart.jpg'))
    
    liz_url = _SALTS.build_plugin_url({'mode': mode, 'start_date': last_str})
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), liz_url, liz, isFolder=True)
    
    cache_watched = _SALTS.get_setting('cache_watched')=='true'
    watched={}
    if TOKEN:
        watched_history = trakt_api.get_watched(SECTIONS.TV, cached=cache_watched)
        for item in watched_history:
            slug = item['show']['ids']['slug']
            watched[slug] = {}
            for season in item['seasons']:
                watched[slug][season['number']]={}
                for episode in season['episodes']:
                    watched[slug][season['number']][episode['number']]=True

    totalItems=len(days)
    for day in sorted(days.items()):
        for item in day[1]:
            episode = item['episode']
            show=item['show']
            fanart=show['images']['fanart']['full']
            utc_secs = utils.iso_2_utc(episode['first_aired'])
            show_date = datetime.date.fromtimestamp(utc_secs)
            
            try: episode['watched']=watched[show['ids']['slug']][episode['season']][episode['number']]
            except: episode['watched']=False
            
            if show_date < start_date.date():
                log_utils.log('Skipping show before start: |%s| before |%s|' % (show_date, start_date.date()), xbmc.LOGDEBUG)
                continue
            elif show_date > next_week.date():
                log_utils.log('Stopping because show after end: |%s| before |%s|' % (show_date, next_week.date()), xbmc.LOGDEBUG)
                break
            
            date = utils.make_day(datetime.date.fromtimestamp(utc_secs).isoformat())
            if _SALTS.get_setting('calendar_time')!='0':
                date_time = '%s@%s' % (date,utils.make_time(utc_secs))
            else:
                date_time = date

            menu_items=[]
            queries = {'mode': MODES.SEASONS, 'slug': show['ids']['slug'], 'fanart': fanart}
            menu_items.append(('Browse Seasons', 'Container.Update(%s)' % (_SALTS.build_plugin_url(queries))), )
 
            liz, liz_url = make_episode_item(show, episode, show_subs=False, menu_items=menu_items)
            label=liz.getLabel()
            label = '[[COLOR deeppink]%s[/COLOR]] %s - %s' % (date_time, show['title'], label.decode('utf-8', 'replace'))
            if episode['season']==1 and episode['number']==1:
                label = '[COLOR green]%s[/COLOR]' % (label)
            liz.setLabel(label)
            xbmcplugin.addDirectoryItem(int(sys.argv[1]), liz_url, liz,isFolder=(liz.getProperty('isPlayable')!='true'),totalItems=totalItems)

    liz = xbmcgui.ListItem(label='Next Week >>', iconImage=utils.art('next.png'), thumbnailImage=utils.art('next.png'))
    liz.setProperty('fanart_image', utils.art('fanart.jpg'))
    liz_url = _SALTS.build_plugin_url({'mode': mode, 'start_date': next_str})
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), liz_url, liz, isFolder=True)    
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def make_season_item(season, info, slug, fanart):
    label = 'Season %s' % (season['number'])
    season['images']['fanart']={}
    season['images']['fanart']['full']=fanart
    liz=utils.make_list_item(label, season)
    log_utils.log('Season Info: %s' % (info), xbmc.LOGDEBUG)
    liz.setInfo('video', info)
    menu_items=[]

    if 'playcount' in info and info['playcount']:
        watched=False
        label='Mark as Unwatched'
    else:
        watched=True
        label='Mark as Watched'
    
    if TOKEN:
        queries = {'mode': MODES.TOGGLE_WATCHED, 'section': SECTIONS.TV, 'season': season['number'], 'id_type': 'slug', 'show_id': slug, 'watched': watched}
        menu_items.append((label, 'RunPlugin(%s)' % (_SALTS.build_plugin_url(queries))), )

    queries = {'mode': MODES.SET_VIEW, 'content_type': CONTENT_TYPES.SEASONS}
    menu_items.append(('Set as Season View', 'RunPlugin(%s)' % (_SALTS.build_plugin_url(queries))), )
    
    liz.addContextMenuItems(menu_items, replaceItems=True)
    return liz

def make_episode_item(show, episode, show_subs=True, menu_items=None):
    log_utils.log('Make Episode: Show: %s, Episode: %s, Show Subs: %s' % (show, episode, show_subs), xbmc.LOGDEBUG)
    log_utils.log('Make Episode: Episode: %s' % (episode), xbmc.LOGDEBUG)
    if menu_items is None: menu_items = []
    folder = _SALTS.get_setting('source-win')=='Directory' and _SALTS.get_setting('auto-play')=='false'
    show['title']=re.sub(' \(\d{4}\)$','',show['title'])
    label = '%sx%s %s' % (episode['season'], episode['number'], episode['title'])
    
    if 'first_aired' in episode: utc_air_time = utils.iso_2_utc(episode['first_aired'])
    try: time_str = time.asctime(time.localtime(utc_air_time))
    except: time_str = 'Unavailable'
    
    log_utils.log('First Aired: Title: %s S/E: %s/%s fa: %s, utc: %s, local: %s' %
                  (show['title'], episode['season'], episode['number'], episode['first_aired'], utc_air_time, time_str), xbmc.LOGDEBUG)
    
    if _SALTS.get_setting('unaired_indicator')=='true' and (not episode['first_aired'] or utc_air_time>time.time()):
        label = '[I][COLOR chocolate]%s[/COLOR][/I]' % (label)

    if show_subs and utils.srt_indicators_enabled():
        srt_scraper=SRT_Scraper()
        language=_SALTS.get_setting('subtitle-lang')
        tvshow_id=srt_scraper.get_tvshow_id(show['title'], show['year'])
        if tvshow_id is not None:
            srts=srt_scraper.get_episode_subtitles(language, tvshow_id, episode['season'], episode['number'])
        else:
            srts=[]
        label = utils.format_episode_label(label, episode['season'], episode['number'], srts)
            
    meta=utils.make_info(episode, show)
    meta['images']=show['images']
    if episode['images']['screenshot']: meta['images']['thumb']=episode['images']['screenshot']
    
    liz=utils.make_list_item(label, meta)
    if not folder:
        liz.setProperty('isPlayable', 'true')

    del meta['images']
    liz.setInfo('video', meta)
    queries = {'mode': MODES.GET_SOURCES, 'video_type': VIDEO_TYPES.EPISODE, 'title': show['title'], 'year': show['year'], 'season': episode['season'], 'episode': episode['number'], 
               'ep_title': episode['title'], 'slug': show['ids']['slug']}
    liz_url = _SALTS.build_plugin_url(queries)
    
    if _SALTS.get_setting('auto-play')=='true':
        queries = {'mode': MODES.SELECT_SOURCE, 'video_type': VIDEO_TYPES.EPISODE, 'title': show['title'], 'year': show['year'], 'season': episode['season'], 'episode': episode['number'], 
                   'ep_title': episode['title'], 'slug': show['ids']['slug']}
        if _SALTS.get_setting('source-win')=='Dialog':
            runstring = 'PlayMedia(%s)' % _SALTS.build_plugin_url(queries)
        else:
            runstring = 'Container.Update(%s)' % _SALTS.build_plugin_url(queries)
        menu_items.insert(0, ('Select Source', runstring), )
        
    if _SALTS.get_setting('show_download')=='true':
        queries = {'mode': MODES.DOWNLOAD_SOURCE, 'video_type': VIDEO_TYPES.EPISODE, 'title': show['title'], 'year': show['year'], 'season': episode['season'], 'episode': episode['number'], 
                   'ep_title': episode['title'], 'slug': show['ids']['slug']}
        if _SALTS.get_setting('source-win')=='Dialog':
            runstring = 'RunPlugin(%s)' % _SALTS.build_plugin_url(queries)
        else:
            runstring = 'Container.Update(%s)' % _SALTS.build_plugin_url(queries)
        menu_items.append(('Download Source', runstring), )
    
    if menu_items and menu_items[0][0]=='Select Source':
        menu_items.append(('Show Information', 'XBMC.Action(Info)'), )
    else:
        menu_items.insert(0, ('Show Information', 'XBMC.Action(Info)'), )

    show_id=utils.show_id(show)
    queries = {'mode': MODES.ADD_TO_LIST, 'section': SECTIONS.TV}
    queries.update(show_id)
    menu_items.append(('Add Show to List', 'RunPlugin(%s)' % (_SALTS.build_plugin_url(queries))), )
        
    if 'watched' in episode and episode['watched']:
        watched=False
        label='Mark as Unwatched'
    else:
        watched=True
        label='Mark as Watched'
        
    if TOKEN:
        show_id=utils.show_id(show)
        queries = {'mode': MODES.RATE, 'section': SECTIONS.TV, 'season': episode['season'], 'episode': episode['number']}
        queries.update(show_id)
        menu_items.append(('Rate on trakt.tv', 'RunPlugin(%s)' % (_SALTS.build_plugin_url(queries))), )

        queries = {'mode': MODES.TOGGLE_WATCHED, 'section': SECTIONS.TV, 'season': episode['season'], 'episode': episode['number'], 'watched': watched}
        queries.update(show_id)
        menu_items.append((label, 'RunPlugin(%s)' % (_SALTS.build_plugin_url(queries))), )

    queries = {'mode': MODES.SET_URL_SEARCH, 'video_type': VIDEO_TYPES.TVSHOW, 'title': show['title'], 'year': show['year'], 'slug': show['ids']['slug']}
    menu_items.append(('Set Related Show Url (Search)', 'RunPlugin(%s)' % (_SALTS.build_plugin_url(queries))), )
    queries = {'mode': MODES.SET_URL_MANUAL, 'video_type': VIDEO_TYPES.EPISODE, 'title': show['title'], 'year': show['year'], 'season': episode['season'], 
               'episode': episode['number'], 'ep_title': episode['title'], 'slug': show['ids']['slug']}
    menu_items.append(('Set Related Url (Manual)', 'RunPlugin(%s)' % (_SALTS.build_plugin_url(queries))), )
 
    liz.addContextMenuItems(menu_items, replaceItems=True)
    return liz, liz_url

def make_item(section_params, show, menu_items=None):
    if menu_items is None: menu_items=[]
    if not isinstance(show['title'],basestring): show['title']=''
    show['title']=re.sub(' \(\d{4}\)$','',show['title'])
    label = '%s (%s)' % (show['title'], show['year'])
    liz=utils.make_list_item(label, show)
    slug=show['ids']['slug']
    liz.setProperty('slug', slug)
    people = trakt_api.get_people(section_params['section'], slug) if _SALTS.get_setting('include_people')=='true' else None 
    info = utils.make_info(show, people=people)
    if not section_params['folder']:
        liz.setProperty('IsPlayable', 'true')
    
    if 'TotalEpisodes' in info:
        liz.setProperty('TotalEpisodes', str(info['TotalEpisodes']))
        liz.setProperty('WatchedEpisodes', str(info['WatchedEpisodes']))
        liz.setProperty('UnWatchedEpisodes', str(info['UnWatchedEpisodes']))
 
    if section_params['section']==SECTIONS.TV:
        queries = {'mode': section_params['next_mode'], 'slug': slug, 'fanart': liz.getProperty('fanart_image')}
        info['TVShowTitle']=info['title']
    else:
        queries = {'mode': section_params['next_mode'], 'video_type': section_params['video_type'], 'title': show['title'], 'year': show['year'], 'slug': slug}
 
    liz.setInfo('video', info)
    liz_url = _SALTS.build_plugin_url(queries)
 
    if section_params['next_mode']==MODES.GET_SOURCES and _SALTS.get_setting('auto-play')=='true':
        queries = {'mode': MODES.SELECT_SOURCE, 'video_type': section_params['video_type'], 'title': show['title'], 'year': show['year'], 'slug': slug}
        if _SALTS.get_setting('source-win')=='Dialog':
            runstring = 'PlayMedia(%s)' % _SALTS.build_plugin_url(queries)
        else:
            runstring = 'Container.Update(%s)' % _SALTS.build_plugin_url(queries)
        menu_items.insert(0, ('Select Source', runstring), )

    if section_params['next_mode']==MODES.GET_SOURCES and _SALTS.get_setting('show_download')=='true':
        queries = {'mode': MODES.DOWNLOAD_SOURCE, 'video_type': section_params['video_type'], 'title': show['title'], 'year': show['year'], 'slug': slug}
        if _SALTS.get_setting('source-win')=='Dialog':
            runstring = 'RunPlugin(%s)' % _SALTS.build_plugin_url(queries)
        else:
            runstring = 'Container.Update(%s)' % _SALTS.build_plugin_url(queries)
        menu_items.append(('Download Source', runstring), )
        
    if TOKEN:
        show_id=utils.show_id(show)
        if 'in_collection' in show and show['in_collection']:
            queries = {'mode': MODES.REM_FROM_COLL, 'section': section_params['section']}
            queries.update(show_id)
            menu_items.append(('Remove from Collection', 'RunPlugin(%s)' % (_SALTS.build_plugin_url(queries))), )
        else:
            queries = {'mode': MODES.ADD_TO_COLL, 'section': section_params['section']}
            queries.update(show_id)
            menu_items.append(('Add to Collection', 'RunPlugin(%s)' % (_SALTS.build_plugin_url(queries))), )
        
        queries = {'mode': MODES.ADD_TO_LIST, 'section': section_params['section']}
        queries.update(show_id)
        menu_items.append(('Add to List', 'RunPlugin(%s)' % (_SALTS.build_plugin_url(queries))), )
        
        queries = {'mode': MODES.RATE, 'section': section_params['section']}
        queries.update(show_id)
        menu_items.append(('Rate on trakt.tv', 'RunPlugin(%s)' % (_SALTS.build_plugin_url(queries))), )
        
        
    queries = {'mode': MODES.ADD_TO_LIBRARY, 'video_type': section_params['video_type'], 'title': show['title'], 'year': show['year'], 'slug': slug}
    menu_items.append(('Add to Library', 'RunPlugin(%s)' % (_SALTS.build_plugin_url(queries))), )

    if TOKEN:
        if 'watched' in show and show['watched']:
            watched=False
            label='Mark as Unwatched'
        else:
            watched=True
            label='Mark as Watched'
        
        if watched or section_params['section']==SECTIONS.MOVIES:
            queries = {'mode': MODES.TOGGLE_WATCHED, 'section': section_params['section'], 'watched': watched}
            queries.update(show_id)
            menu_items.append((label, 'RunPlugin(%s)' % (_SALTS.build_plugin_url(queries))), )

    if section_params['section']==SECTIONS.TV and _SALTS.get_setting('enable-subtitles')=='true':
        queries = {'mode': MODES.EDIT_TVSHOW_ID, 'title': show['title'], 'year': show['year']}
        runstring = 'RunPlugin(%s)' % _SALTS.build_plugin_url(queries)
        menu_items.append(('Set Addic7ed TVShowID', runstring,))

    if section_params['section'] == SECTIONS.TV:
        if slug in utils.get_force_title_list():
            label = 'Use Default episode matching'
        else:
            label = 'Use Episode Title matching'
        queries = {'mode': MODES.TOGGLE_TITLE, 'slug': slug}
        runstring = 'RunPlugin(%s)' % _SALTS.build_plugin_url(queries)
        menu_items.append((label, runstring,))

    queries = {'mode': MODES.SET_URL_SEARCH, 'video_type': section_params['video_type'], 'title': show['title'], 'year': show['year'], 'slug': slug}
    menu_items.append(('Set Related Url (Search)', 'RunPlugin(%s)' % (_SALTS.build_plugin_url(queries))), )
    queries = {'mode': MODES.SET_URL_MANUAL, 'video_type': section_params['video_type'], 'title': show['title'], 'year': show['year'], 'slug': slug}
    menu_items.append(('Set Related Url (Manual)', 'RunPlugin(%s)' % (_SALTS.build_plugin_url(queries))), )

    if len(menu_items)<10 and 'trailer' in info:
        queries = {'mode': MODES.PLAY_TRAILER, 'stream_url': info['trailer']}
        menu_items.insert(-3, ('Play Trailer', 'RunPlugin(%s)' % (_SALTS.build_plugin_url(queries))), )

    if len(menu_items)<10:
        menu_items.insert(0, ('Show Information', 'XBMC.Action(Info)'), )

    liz.addContextMenuItems(menu_items, replaceItems=True)
 

    liz.setProperty('resumetime',str(0))
    liz.setProperty('totaltime',str(1))
    return liz, liz_url

def main(argv=None):
    if sys.argv: argv=sys.argv

    log_utils.log('Version: |%s| Queries: |%s|' % (_SALTS.get_version(),_SALTS.queries))
    log_utils.log('Args: |%s|' % (argv))
    
    # don't process params that don't match our url exactly. (e.g. plugin://plugin.video.1channel/extrafanart)
    plugin_url = 'plugin://%s/' % (_SALTS.get_id())
    if argv[0] != plugin_url:
        return

    try:
        mode = _SALTS.queries.get('mode', None)
        url_dispatcher.dispatch(mode, _SALTS.queries)
    except TransientTraktError as e:
        log_utils.log(str(e), xbmc.LOGERROR)
        builtin = 'XBMC.Notification(%s,%s, 5000, %s)'
        xbmc.executebuiltin(builtin % (_SALTS.get_name(), str(e), ICON_PATH))

if __name__ == '__main__':
    sys.exit(main())
