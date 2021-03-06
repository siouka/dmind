import os
import time
import _strptime
import re
import datetime
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import xbmcvfs
import log_utils
import sys
import hashlib
import urlparse
import shutil
import urllib
from constants import *
from scrapers import * # import all scrapers into this namespace
from addon.common.addon import Addon
from trakt_api import Trakt_API
from db_utils import DB_Connection

ADDON = Addon('plugin.video.salts')
ICON_PATH = os.path.join(ADDON.get_path(), 'icon.png')
SORT_FIELDS =  [(SORT_LIST[int(ADDON.get_setting('sort1_field'))], SORT_SIGNS[ADDON.get_setting('sort1_order')]),
                (SORT_LIST[int(ADDON.get_setting('sort2_field'))], SORT_SIGNS[ADDON.get_setting('sort2_order')]),
                (SORT_LIST[int(ADDON.get_setting('sort3_field'))], SORT_SIGNS[ADDON.get_setting('sort3_order')]),
                (SORT_LIST[int(ADDON.get_setting('sort4_field'))], SORT_SIGNS[ADDON.get_setting('sort4_order')]),
                (SORT_LIST[int(ADDON.get_setting('sort5_field'))], SORT_SIGNS[ADDON.get_setting('sort5_order')])]

username=ADDON.get_setting('username')
password=ADDON.get_setting('password')
token = ADDON.get_setting('trakt_token')
use_https=ADDON.get_setting('use_https')=='true'
trakt_timeout=int(ADDON.get_setting('trakt_timeout'))
list_size=int(ADDON.get_setting('list_size'))

P_MODE = int(ADDON.get_setting('parallel_mode'))
if P_MODE == P_MODES.THREADS:
    import threading
    from Queue import Queue, Empty
elif P_MODE == P_MODES.PROCESSES:
    try:
        import multiprocessing
        from multiprocessing import Queue
        from Queue import Empty
    except ImportError:
        import threading
        from Queue import Queue, Empty
        P_MODE = P_MODES.THREADS
        builtin = 'XBMC.Notification(%s,Process Mode not supported on this platform falling back to Thread Mode, 7500, %s)'
        xbmc.executebuiltin(builtin % (ADDON.get_name(), ICON_PATH))

trakt_api=Trakt_API(username,password, token, use_https, list_size, trakt_timeout)
db_connection=DB_Connection()

THEME_LIST = ['Shine', 'Luna_Blue', 'Iconic']
THEME = THEME_LIST[int(ADDON.get_setting('theme'))]
if xbmc.getCondVisibility('System.HasAddon(script.salts.themepak)'):
    themepak_path = xbmcaddon.Addon('script.salts.themepak').getAddonInfo('path')
else:
    themepak_path=ADDON.get_path()
THEME_PATH = os.path.join(themepak_path, 'art', 'themes', THEME)

def art(name): 
    return os.path.join(THEME_PATH, name)

def choose_list(username=None):
    lists = trakt_api.get_lists(username)
    if username is None: lists.insert(0, {'name': 'watchlist', 'ids': {'slug': WATCHLIST_SLUG}})
    if lists:
        dialog=xbmcgui.Dialog()
        index = dialog.select('Pick a list', [list_data['name'] for list_data in lists])
        if index>-1:
            return lists[index]['ids']['slug']
    else:
        builtin = 'XBMC.Notification(%s,No Lists exist for user: %s, 5000, %s)'
        xbmc.executebuiltin(builtin % (ADDON.get_name(), username, ICON_PATH))

def show_id(show):
    queries={}
    ids = show['ids']
    if 'slug' in ids and ids['slug']:
        queries['id_type']='slug'
        queries['show_id']=ids['slug']
    elif 'trakt' in ids and ids['trakt']:
        queries['id_type']='trakt'
        queries['show_id']=ids['trakt']
    elif 'imdb' in ids and ids['imdb']:
        queries['id_type']='imdb'
        queries['show_id']=ids['imdb']
    elif 'tvdb' in ids and ids['tvdb']:
        queries['id_type']='tvdb'
        queries['show_id']=ids['tvdb']
    elif 'tmdb' in ids and ids['tmdb']:
        queries['id_type']='tmdb'
        queries['show_id']=ids['tmdb']
    elif 'tvrage' in ids and ids['tvrage']:
        queries['id_type']='tvrage'
        queries['show_id']=ids['tvrage']
    return queries
    
def update_url(video_type, title, year, source, old_url, new_url, season, episode):
    log_utils.log('Setting Url: |%s|%s|%s|%s|%s|%s|%s|%s|' % (video_type, title, year, source, old_url, new_url, season, episode), xbmc.LOGDEBUG)
    if new_url:
        db_connection.set_related_url(video_type, title, year, source, new_url, season, episode)
    else:
        db_connection.clear_related_url(video_type, title, year, source, season, episode)

    # clear all episode local urls if tvshow url changes
    if video_type == VIDEO_TYPES.TVSHOW and new_url != old_url:
        db_connection.clear_related_url(VIDEO_TYPES.EPISODE, title, year, source)

def make_seasons_info(progress):
    season_info={}
    if progress:
        for season in progress['seasons']:
            info={}
            if 'aired' in season: info['episode']=info['TotalEpisodes']=season['aired']
            if 'completed' in season: info['WatchedEpisodes']=season['completed']
            if 'aired' in season and 'completed' in season:
                info['UnWatchedEpisodes']=season['aired'] - season['completed']
                info['playcount']=season['aired'] if season['completed']==season['aired'] else 0
                
            if 'number' in season: info['season']=season['number']
            season_info[str(season['number'])]=info
    return season_info

def make_episodes_watched(episodes, progress):
    watched={}
    for season in progress['seasons']:
        watched[str(season['number'])]={}
        for ep_status in season['episodes']:
            watched[str(season['number'])][str(ep_status['number'])]=ep_status['completed']
    
    for episode in episodes:
        season_str = str(episode['season'])
        episode_str = str(episode['number'])
        if season_str in watched and episode_str in watched[season_str]:
            episode['watched']=watched[season_str][episode_str]
        else:
            episode['watched']=False

    return episodes

def make_list_item(label, meta):
    art=make_art(meta)
    listitem = xbmcgui.ListItem(label, iconImage=art['thumb'], thumbnailImage=art['thumb'])
    listitem.setProperty('fanart_image', art['fanart'])
    try: listitem.setArt(art)
    except: pass
    if 'ids' in meta and 'imdb' in meta['ids']: listitem.setProperty('imdb_id', str(meta['ids']['imdb']))
    if 'ids' in meta and 'tvdb' in meta['ids']: listitem.setProperty('tvdb_id', str(meta['ids']['tvdb']))
    return listitem

def make_art(show):
    min_size = int(ADDON.get_setting('image_size'))
    art_dict={'banner': '', 'fanart': art('fanart.jpg'), 'thumb': '', 'poster': PLACE_POSTER}
    if 'images' in show:
        images = show['images']
        for i in range(0,min_size+1):
            if 'banner' in images and IMG_SIZES[i] in images['banner'] and images['banner'][IMG_SIZES[i]]: art_dict['banner']=images['banner'][IMG_SIZES[i]]
            if 'fanart' in images and IMG_SIZES[i] in images['fanart'] and images['fanart'][IMG_SIZES[i]]: art_dict['fanart']=images['fanart'][IMG_SIZES[i]]
            if 'poster' in images and IMG_SIZES[i] in images['poster'] and images['poster'][IMG_SIZES[i]]: art_dict['thumb']=art_dict['poster']=images['poster'][IMG_SIZES[i]]
            if 'thumb' in images and IMG_SIZES[i] in images['thumb'] and images['thumb'][IMG_SIZES[i]]: art_dict['thumb']=images['thumb'][IMG_SIZES[i]]
            if 'screen' in images and IMG_SIZES[i] in images['screen'] and images['screen'][IMG_SIZES[i]]: art_dict['thumb']=images['screen'][IMG_SIZES[i]]
            if 'screenshot' in images and IMG_SIZES[i] in images['screenshot'] and images['screenshot'][IMG_SIZES[i]]: art_dict['thumb']=images['screenshot'][IMG_SIZES[i]]
            if 'logo' in images and IMG_SIZES[i] in images['logo'] and images['logo'][IMG_SIZES[i]]: art_dict['clearlogo']=images['logo'][IMG_SIZES[i]]
            if 'clearart' in images and IMG_SIZES[i] in images['clearart'] and images['clearart'][IMG_SIZES[i]]: art_dict['clearart']=images['clearart'][IMG_SIZES[i]]
    return art_dict

def make_info(item, show=None, people=None):
    if people is None: people = {}
    if show is None: show={}
    #log_utils.log('Making Info: Show: %s' % (show), xbmc.LOGDEBUG)
    #log_utils.log('Making Info: Item: %s' % (item), xbmc.LOGDEBUG)
    info={}
    info['title']=item['title']
    if 'overview' in item: info['plot']=info['plotoutline']=item['overview']
    if 'runtime' in item: info['duration']=item['runtime']
    if 'certification' in item: info['mpaa']=item['certification']
    if 'year' in item: info['year']=item['year']
    if 'season' in item: info['season']=item['season'] # needs check
    if 'episode' in item: info['episode']=item['episode'] # needs check
    if 'number' in item: info['episode']=item['number'] # needs check
    if 'genres' in item:
        genres = dict((genre['slug'],genre['name']) for genre in trakt_api.get_genres(SECTIONS.TV))
        genres.update(dict((genre['slug'],genre['name']) for genre in trakt_api.get_genres(SECTIONS.MOVIES)))
        item_genres = [genres[genre] for genre in item['genres'] if genre in genres]
        info['genre']=', '.join(item_genres)
    if 'network' in item: info['studio']=item['network']
    if 'status' in item: info['status']=item['status']
    if 'tagline' in item: info['tagline']=item['tagline']
    if 'watched' in item and item['watched']: info['playcount']=1
    if 'plays' in item and item['plays']: info['playcount']=item['plays']
    if 'rating' in item: info['rating']=item['rating']
    if 'votes' in item: info['votes']=item['votes']
    if 'released' in item: info['premiered']=item['released']
    if 'trailer' in item and item['trailer']: info['trailer']=make_trailer(item['trailer'])
    info.update(make_ids(item))
    
    if 'first_aired' in item:
        utc_air_time = iso_2_utc(item['first_aired'])
        try: info['aired']=info['premiered']=time.strftime('%Y-%m-%d', time.localtime(utc_air_time))
        except ValueError: # windows throws a ValueError on negative values to localtime  
            d=datetime.datetime.fromtimestamp(0) + datetime.timedelta(seconds=utc_air_time)
            info['aired']=info['premiered']=d.strftime('%Y-%m-%d')
     
    if 'aired_episodes' in item:
        info['episode']=info['TotalEpisodes']=item['aired_episodes']
        info['WatchedEpisodes']=item['watched_count'] if 'watched_count' in item else 0
        info['UnWatchedEpisodes']=info['TotalEpisodes'] - info['WatchedEpisodes']
        
    # override item params with show info if it exists
    if 'certification' in show: info['mpaa']=show['certification']
    if 'year' in show: info['year']=show['year']
    if 'runtime' in show: info['duration']=show['runtime']
    if 'title' in show: info['tvshowtitle']=show['title']
    if 'network' in show: info['studio']=show['network']
    if 'status' in show: info['status']=show['status']
    if 'trailer' in show and show['trailer']: info['trailer']=make_trailer(show['trailer'])
    info.update(make_ids(show))
    info.update(make_people(people))
    return info
    
def make_trailer(trailer_url):
    match=re.search('\?v=(.*)', trailer_url)
    if match:
        return 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % (match.group(1)) 
    
def make_ids(item):
    info={}
    if 'ids' in item:
        ids=item['ids']
        if 'imdb' in ids: info['code']=info['imdbnumber']=info['imdb_id']=ids['imdb']
        if 'tmdb' in ids: info['tmdb_id']=ids['tmdb']
        if 'tvdb' in ids: info['tvdb_id']=ids['tvdb']
        if 'trakt' in ids: info['trakt_id']=ids['trakt']
        if 'slug' in ids: info['slug']=ids['slug']
    return info
    
def make_people(item):
    people={}
    if 'cast' in item: people['cast']=[person['person']['name'] for person in item['cast']]
    if 'cast' in item: people['castandrole']=['%s as %s' % (person['person']['name'], person['character']) for person in item['cast']]
    if 'crew' in item and 'directing' in item['crew']:
        directors = [director['person']['name'] for director in item['crew']['directing'] if director['job'].lower() == 'director']
        people['director']=', '.join(directors)
    if 'crew' in item and 'writing' in item['crew']:
        writers = [writer['person']['name'] for writer in item['crew']['writing'] if writer['job'].lower() in ['writer', 'screenplay', 'author']]
        people['writer']=', '.join(writers)
    
    return people
    
def get_section_params(section):
    section_params={}
    section_params['section']=section
    if section==SECTIONS.TV:
        section_params['next_mode']=MODES.SEASONS
        section_params['folder']=True
        section_params['video_type']=VIDEO_TYPES.TVSHOW
        section_params['content_type']=CONTENT_TYPES.TVSHOWS
    else:
        section_params['next_mode']=MODES.GET_SOURCES
        section_params['folder']=ADDON.get_setting('source-win')=='Directory' and ADDON.get_setting('auto-play')=='false'
        section_params['video_type']=VIDEO_TYPES.MOVIE
        section_params['content_type']=CONTENT_TYPES.MOVIES
    return section_params

def filename_from_title(title, video_type, year=None):
    if video_type == VIDEO_TYPES.TVSHOW:
        filename = '%s S%sE%s.strm'
        filename = filename % (title, '%s', '%s')
    else:
        if year: title = '%s (%s)' % (title, year)
        filename = '%s.strm' % title

    filename = re.sub(r'(?!%s)[^\w\-_\.]', '.', filename)
    filename = re.sub('\.+', '.', filename)
    xbmc.makeLegalFilename(filename)
    return filename

def filter_unknown_hosters(hosters):
    filtered_hosters=[]
    for host in hosters:
        for key, _ in SORT_FIELDS:
            if key in host and host[key] is None:
                break
        else:
            filtered_hosters.append(host)
    return filtered_hosters

def filter_exclusions(hosters):
    exclusions = ADDON.get_setting('excl_list')
    exclusions = exclusions.replace(' ', '')
    exclusions = exclusions.lower()
    if not exclusions: return hosters
    filtered_hosters=[]
    for hoster in hosters:
        if hoster['host'].lower() in exclusions:
            log_utils.log('Excluding %s (%s) from %s' % (hoster['url'], hoster['host'], hoster['class'].get_name()), xbmc.LOGDEBUG)
            continue
        filtered_hosters.append(hoster)
    return filtered_hosters

def filter_quality(video_type, hosters):
    qual_filter = int(ADDON.get_setting('%s_quality' % video_type))
    if qual_filter==0:
        return hosters
    elif qual_filter==1:
        keep_qual=[QUALITIES.HD]
    else:
        keep_qual=[QUALITIES.LOW, QUALITIES.MEDIUM, QUALITIES.HIGH]
    
    filtered_hosters = []
    for hoster in hosters:
        if hoster['quality'] in keep_qual:
            filtered_hosters.append(hoster)
    return filtered_hosters

def get_sort_key(item):
    item_sort_key = []
    for field, sign in SORT_FIELDS:
        if field=='none':
            break
        elif field in SORT_KEYS:
            if field == 'source':
                value=item['class'].get_name()
            else:
                value=item[field]
            
            if value in SORT_KEYS[field]:
                item_sort_key.append(sign*int(SORT_KEYS[field][value]))
            else: # assume all unlisted values sort as worst
                item_sort_key.append(sign*-1)
        else:
            if item[field] is None:
                item_sort_key.append(sign*-1)
            else:
                item_sort_key.append(sign*int(item[field]))
    #print 'item: %s sort_key: %s' % (item, item_sort_key)
    return tuple(item_sort_key)

def make_source_sort_key():
    sso=ADDON.get_setting('source_sort_order')
    sort_key={}
    i=0
    scrapers = relevant_scrapers(include_disabled=True)
    scraper_names = [scraper.get_name() for scraper in scrapers]
    if sso:
        sources = sso.split('|')
        sort_key={}
        for i,source in enumerate(sources):
            if source in scraper_names:
                sort_key[source]=-i
        
    for j, scraper in enumerate(scrapers):
        if scraper.get_name() not in sort_key:
            sort_key[scraper.get_name()]=-(i+j)
    
    return sort_key

def get_source_sort_key(item):
    sort_key=make_source_sort_key()
    return -sort_key[item.get_name()]
        
def make_source_sort_string(sort_key):
    sorted_key = sorted(sort_key.items(), key=lambda x: -x[1])
    sort_string = '|'.join([element[0] for element in sorted_key])
    return sort_string

def start_worker(q, func, args):
    if P_MODE == P_MODES.THREADS:
        worker=threading.Thread(target=func, args=([q] + args))
    elif P_MODE == P_MODES.PROCESSES:
        worker=multiprocessing.Process(target=func, args=([q] + args))
    worker.daemon=True
    worker.start()
    return worker

def reap_workers(workers, timeout=0):
    """
    Reap thread/process workers; don't block by default; return un-reaped workers
    """
    log_utils.log('In Reap: %s' % (workers), xbmc.LOGDEBUG)
    living_workers=[]
    for worker in workers:
        log_utils.log('Reaping: %s' % (worker.name), xbmc.LOGDEBUG)
        worker.join(timeout)
        if worker.is_alive():
            log_utils.log('Worker %s still running' % (worker.name), xbmc.LOGDEBUG)
            living_workers.append(worker)
    return living_workers

def parallel_get_sources(q, cls, video):
    scraper_instance=cls(int(ADDON.get_setting('source_timeout')))
    if P_MODE == P_MODES.THREADS:
        worker=threading.current_thread()
    elif P_MODE == P_MODES.PROCESSES:
        worker=multiprocessing.current_process()
        
    log_utils.log('Starting %s (%s) for %s sources' % (worker.name, worker, cls.get_name()), xbmc.LOGDEBUG)
    hosters=scraper_instance.get_sources(video)
    log_utils.log('%s returned %s sources from %s' % (cls.get_name(), len(hosters), worker), xbmc.LOGDEBUG)
    result = {'name': cls.get_name(), 'hosters': hosters}
    q.put(result)

def parallel_get_url(q, cls, video):
    scraper_instance=cls(int(ADDON.get_setting('source_timeout')))
    if P_MODE == P_MODES.THREADS:
        worker=threading.current_thread()
    elif P_MODE == P_MODES.PROCESSES:
        worker=multiprocessing.current_process()
        
    log_utils.log('Starting %s (%s) for %s url' % (worker.name, worker, cls.get_name()), xbmc.LOGDEBUG)
    url=scraper_instance.get_url(video)
    log_utils.log('%s returned url %s from %s' % (cls.get_name(), url, worker), xbmc.LOGDEBUG)
    related={}
    related['class']=scraper_instance
    if not url: url=''
    related['url']=url
    related['name']=related['class'].get_name()
    related['label'] = '[%s] %s' % (related['name'], related['url'])
    q.put(related)

# Run a task on startup. Settings and mode values must match task name
def do_startup_task(task):
    run_on_startup=ADDON.get_setting('auto-%s' % task)=='true' and ADDON.get_setting('%s-during-startup' % task) == 'true' 
    if run_on_startup and not xbmc.abortRequested:
        log_utils.log('Service: Running startup task [%s]' % (task))
        now = datetime.datetime.now()
        xbmc.executebuiltin('RunPlugin(plugin://%s/?mode=%s)' % (ADDON.get_id(), task))
        db_connection.set_setting('%s-last_run' % (task), now.strftime("%Y-%m-%d %H:%M:%S.%f"))
    
# Run a recurring scheduled task. Settings and mode values must match task name
def do_scheduled_task(task, isPlaying):
    now = datetime.datetime.now()
    if ADDON.get_setting('auto-%s' % task) == 'true':
        next_run=get_next_run(task)
        #log_utils.log("Update Status on [%s]: Currently: %s Will Run: %s" % (task, now, next_run), xbmc.LOGDEBUG)
        if now >= next_run:
            is_scanning = xbmc.getCondVisibility('Library.IsScanningVideo')
            if not is_scanning:
                during_playback = ADDON.get_setting('%s-during-playback' % (task))=='true'
                if during_playback or not isPlaying:
                    log_utils.log('Service: Running Scheduled Task: [%s]' % (task))
                    builtin = 'RunPlugin(plugin://%s/?mode=%s)' % (ADDON.get_id(), task)
                    xbmc.executebuiltin(builtin)
                    db_connection.set_setting('%s-last_run' % task, now.strftime("%Y-%m-%d %H:%M:%S.%f"))
                else:
                    log_utils.log('Service: Playing... Busy... Postponing [%s]' % (task), xbmc.LOGDEBUG)
            else:
                log_utils.log('Service: Scanning... Busy... Postponing [%s]' % (task), xbmc.LOGDEBUG)

def get_next_run(task):
    # strptime mysteriously fails sometimes with TypeError; this is a hacky workaround
    # note, they aren't 100% equal as time.strptime loses fractional seconds but they are close enough
    try:
        last_run_string = db_connection.get_setting(task+'-last_run')
        if not last_run_string: last_run_string=LONG_AGO
        last_run=datetime.datetime.strptime(last_run_string, "%Y-%m-%d %H:%M:%S.%f")
    except (TypeError, ImportError):
        last_run=datetime.datetime(*(time.strptime(last_run_string, '%Y-%m-%d %H:%M:%S.%f')[0:6]))
    interval=datetime.timedelta(hours=float(ADDON.get_setting(task+'-interval')))
    return (last_run+interval)

def url_exists(video):
    """
    check each source for a url for this video; return True as soon as one is found. If none are found, return False
    """
    max_timeout = int(ADDON.get_setting('source_timeout'))
    log_utils.log('Checking for Url Existence: |%s|' % (video), xbmc.LOGDEBUG)
    for cls in relevant_scrapers(video.video_type):
        if ADDON.get_setting('%s-sub_check' % (cls.get_name()))=='true':
            scraper_instance=cls(max_timeout)
            url = scraper_instance.get_url(video)
            if url:
                log_utils.log('Found url for |%s| @ %s: %s' % (video, cls.get_name(), url), xbmc.LOGDEBUG)
                return True

    log_utils.log('No url found for: |%s|' % (video))
    return False

def relevant_scrapers(video_type=None, include_disabled=False, order_matters=False):
    classes=scraper.Scraper.__class__.__subclasses__(scraper.Scraper)
    relevant=[]
    for cls in classes:
        if video_type is None or video_type in cls.provides():
            if include_disabled or scraper_enabled(cls.get_name()):
                relevant.append(cls)
    
    if order_matters:
        relevant.sort(key=get_source_sort_key)
    return relevant

def scraper_enabled(name):
    # return true if setting exists and set to true, or setting doesn't exist (i.e. '')
    return ADDON.get_setting('%s-enable' % (name)) in ['true', '']

def set_view(content, set_sort):
    # set content type so library shows more views and info
    if content:
        xbmcplugin.setContent(int(sys.argv[1]), content)
    
    view = ADDON.get_setting('%s_view' % (content))
    if view != '0':
        log_utils.log('Setting View to %s (%s)' % (view, content), xbmc.LOGDEBUG)
        xbmc.executebuiltin('Container.SetViewMode(%s)' % (view))

    # set sort methods - probably we don't need all of them
    if set_sort:
        xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_UNSORTED)
        xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_LABEL)
        xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RATING)
        xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_DATE)
        xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_PROGRAM_COUNT)
        xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RUNTIME)
        xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_GENRE)

def make_day(date):
    try: date=datetime.datetime.strptime(date,'%Y-%m-%d').date()
    except TypeError: date = datetime.datetime(*(time.strptime(date, '%Y-%m-%d')[0:6])).date()
    today=datetime.date.today()
    day_diff = (date - today).days
    if day_diff == -1:
        date='YDA'
    elif day_diff == 0:
        date='TDA'
    elif day_diff == 1:
        date='TOM'
    elif day_diff > 1 and day_diff < 7:
        date = date.strftime('%a')

    return date

def make_time(utc_ts):
    local_time = time.localtime(utc_ts)
    if ADDON.get_setting('calendar_time')=='1':
        time_format = '%H:%M'
        time_str = time.strftime(time_format, local_time)
    else:
        time_format = '%I%p' if local_time.tm_min == 0 else '%I:%M%p'
        time_str = time.strftime(time_format, local_time)
        if time_str[0] == '0': time_str = time_str[1:]
    return time_str

def iso_2_utc(iso_ts):
    if not iso_ts or iso_ts is None: return 0
    delim = -1
    if not iso_ts.endswith('Z'):
        delim = iso_ts.rfind('+')
        if delim == -1:  delim = iso_ts.rfind('-')
    
    if delim>-1:
        ts = iso_ts[:delim]
        sign = iso_ts[delim]
        tz = iso_ts[delim+1:]
    else:
        ts = iso_ts
        tz = None
    
    if ts.find('.')>-1:
        ts  = ts[:ts.find('.')]
        
    try: d=datetime.datetime.strptime(ts,'%Y-%m-%dT%H:%M:%S')
    except TypeError: d = datetime.datetime(*(time.strptime(ts, '%Y-%m-%dT%H:%M:%S')[0:6]))
    
    dif=datetime.timedelta()
    if tz:
        hours, minutes = tz.split(':')
        hours = int(hours)
        minutes= int(minutes)
        if sign == '-':
            hours = -hours
            minutes = -minutes
        dif = datetime.timedelta(minutes=minutes, hours=hours)
    utc_dt = d - dif
    epoch = datetime.datetime.utcfromtimestamp(0)
    delta = utc_dt - epoch
    try: seconds = delta.total_seconds() # works only on 2.7
    except: seconds = delta.seconds + delta.days * 24 * 3600 # close enough
    return seconds

def get_trakt_token():
    username=ADDON.get_setting('username')
    password=ADDON.get_setting('password')
    token=ADDON.get_setting('trakt_token')
    last_hash=ADDON.get_setting('last_hash')
    cur_hash = hashlib.md5(username+password).hexdigest()
    
    if not token or cur_hash != last_hash:
        try:
            token=trakt_api.login()
            log_utils.log('Token Returned: %s' % (token), xbmc.LOGDEBUG)
        except Exception as e:
            log_utils.log('Login Failed: %s' % (e), xbmc.LOGWARNING)
            builtin = 'XBMC.Notification(%s,Login Failed: %s, 7500, %s)'
            xbmc.executebuiltin(builtin % (ADDON.get_name(), e, ICON_PATH))
            token=''
        
        if token:
            ADDON.set_setting('last_hash', cur_hash)
            
    ADDON.set_setting('trakt_token', token)
    return token

def format_sub_label(sub):
    label = '%s - [%s] - (' % (sub['language'], sub['version'])
    if sub['completed']:
        color='green'
    else:
        label += '%s%% Complete, ' % (sub['percent'])
        color='yellow'
    if sub['hi']: label += 'HI, '
    if sub['corrected']: label += 'Corrected, '
    if sub['hd']: label += 'HD, '
    if not label.endswith('('):
        label = label[:-2] + ')'
    else:
        label = label[:-4]
    label='[COLOR %s]%s[/COLOR]' % (color, label)
    return label

def srt_indicators_enabled():
    return (ADDON.get_setting('enable-subtitles')=='true' and (ADDON.get_setting('subtitle-indicator')=='true'))

def srt_download_enabled():
    return (ADDON.get_setting('enable-subtitles')=='true' and (ADDON.get_setting('subtitle-download')=='true'))

def srt_show_enabled():
    return (ADDON.get_setting('enable-subtitles')=='true' and (ADDON.get_setting('subtitle-show')=='true'))

def format_episode_label(label, season, episode, srts):
    req_hi = ADDON.get_setting('subtitle-hi')=='true'
    req_hd = ADDON.get_setting('subtitle-hd')=='true'
    color='red'
    percent=0
    hi=None
    hd=None
    corrected=None
    
    for srt in srts:
        if str(season)==srt['season'] and str(episode)==srt['episode']:
            if not req_hi or srt['hi']:
                if not req_hd or srt['hd']:
                    if srt['completed']:
                        color='green'
                        if not hi: hi=srt['hi']
                        if not hd: hd=srt['hd']
                        if not corrected: corrected=srt['corrected']
                    elif color!='green':
                        color='yellow'
                        if float(srt['percent'])>percent:
                            if not hi: hi=srt['hi']
                            if not hd: hd=srt['hd']
                            if not corrected: corrected=srt['corrected']
                            percent=srt['percent']
    
    if color!='red':
        label += ' [COLOR %s](SRT: ' % (color)
        if color=='yellow':
            label += ' %s%%, ' % (percent)
        if hi: label += 'HI, '
        if hd: label += 'HD, '
        if corrected: label += 'Corrected, '
        label = label[:-2]
        label+= ')[/COLOR]'
    return label

def get_force_title_list():
    filter_str = ADDON.get_setting('force_title_match')
    filter_list = filter_str.split('|') if filter_str else []
    return filter_list

def calculate_success(name):
    tries=ADDON.get_setting('%s_try' % (name))
    fail = ADDON.get_setting('%s_fail' % (name))
    tries = int(tries) if tries else 0
    fail = int(fail) if fail else 0
    rate = int(round((fail*100.0)/tries)) if tries>0 else 0
    rate = 100 - rate
    return rate

def record_timeouts(fails):
    for key in fails:
        if fails[key]==True:
            log_utils.log('Recording Timeout of %s' % (key), xbmc.LOGWARNING)
            increment_setting('%s_fail' % key)

def do_disable_check():
    scrapers=relevant_scrapers()
    auto_disable=ADDON.get_setting('auto-disable')
    check_freq=int(ADDON.get_setting('disable-freq'))
    disable_thresh=int(ADDON.get_setting('disable-thresh'))
    for cls in scrapers:
        last_check = db_connection.get_setting('%s_check' % (cls.get_name()))
        last_check = int(last_check) if last_check else 0
        tries=ADDON.get_setting('%s_try' % (cls.get_name()))
        tries = int(tries) if tries else 0
        if tries>0 and tries/check_freq>last_check/check_freq:
            ADDON.set_setting('%s_check' % (cls.get_name()), str(tries))
            success_rate=calculate_success(cls.get_name())
            if success_rate<disable_thresh:
                if auto_disable == DISABLE_SETTINGS.ON:
                    ADDON.set_setting('%s-enable' % (cls.get_name()), 'false')
                    builtin = "XBMC.Notification(%s,[COLOR blue]%s[/COLOR] Scraper Automatically Disabled, 5000, %s)" % (ADDON.get_name(), cls.get_name(), ICON_PATH)
                    xbmc.executebuiltin(builtin)
                elif auto_disable == DISABLE_SETTINGS.PROMPT:
                    dialog=xbmcgui.Dialog()
                    line1='The [COLOR blue]%s[/COLOR] scraper timed out on [COLOR red]%s%%[/COLOR] of %s requests'  % (cls.get_name(), 100-success_rate, tries)
                    line2= 'Each timeout wastes system resources and time.'
                    line3='([I]If you keep it enabled, consider increasing the scraper timeout.[/I])'
                    ret = dialog.yesno('SALTS', line1, line2, line3, 'Keep Enabled', 'Disable It')
                    if ret:
                        ADDON.set_setting('%s-enable' % (cls.get_name()), 'false')

def menu_on(menu):
    return ADDON.get_setting('show_%s' % (menu))=='true'

def get_setting(setting):
    return ADDON.get_setting(setting)

def set_setting(setting, value):
    ADDON.set_setting(setting, str(value))

def increment_setting(setting):
    cur_value = get_setting(setting)
    cur_value = int(cur_value) if cur_value else 0
    set_setting(setting, cur_value+1)

def show_requires_source(slug):
    show_str = ADDON.get_setting('exists_list')
    show_list = show_str.split('|')
    if slug in show_list:
        return True
    else:
        return False

def keep_search(section, search_text):
    head = int(ADDON.get_setting('%s_search_head' % (section)))
    new_head = (head + 1) % SEARCH_HISTORY
    log_utils.log('Setting %s to %s' % (new_head, search_text), xbmc.LOGDEBUG)
    db_connection.set_setting('%s_search_%s' % (section, new_head), search_text)
    ADDON.set_setting('%s_search_head' % (section), str(new_head))

def get_current_view():
    skinPath = xbmc.translatePath('special://skin/')
    xml = os.path.join(skinPath,'addon.xml')
    f = xbmcvfs.File(xml)
    read = f.read()
    f.close()
    try: src = re.search('defaultresolution="([^"]+)', read, re.DOTALL).group(1)
    except: src = re.search('<res.+?folder="([^"]+)', read, re.DOTALL).group(1)
    src = os.path.join(skinPath, src, 'MyVideoNav.xml')
    f = xbmcvfs.File(src)
    read = f.read()
    f.close()
    match = re.search('<views>([^<]+)', read, re.DOTALL)
    if match:
        views = match.group(1)
        for view in views.split(','):
            if xbmc.getInfoLabel('Control.GetLabel(%s)' % (view)): return view

def bookmark_exists(slug, season, episode):
    if ADDON.get_setting('trakt_bookmark')=='true':
        bookmark = trakt_api.get_bookmark(slug, season, episode)
        return bookmark is not None
    else:
        return db_connection.bookmark_exists(slug, season, episode)

# returns true if user chooses to resume, else false
def get_resume_choice(slug, season, episode):
    if ADDON.get_setting('trakt_bookmark')=='true':
        resume_point = '%s%%' % (trakt_api.get_bookmark(slug, season, episode))
        header = 'Trakt Bookmark Exists'
    else:
        resume_point = format_time(db_connection.get_bookmark(slug, season, episode))
        header = 'Local Bookmark Exists'
    question = 'Resume from %s' % (resume_point)
    return xbmcgui.Dialog().yesno(header, question, '', '', 'Start from beginning', 'Resume')==1

def get_bookmark(slug, season, episode):
    if ADDON.get_setting('trakt_bookmark')=='true':
        bookmark = trakt_api.get_bookmark(slug, season, episode)
    else:
        bookmark = db_connection.get_bookmark(slug, season, episode)
    return bookmark

def format_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    if minutes > 60:
        hours, minutes = divmod(minutes, 60)
        return "%02d:%02d:%02d" % (hours, minutes, seconds)
    else:
        return "%02d:%02d" % (minutes, seconds)

def download_media(url, path, file_name):
    try:
        progress = int(ADDON.get_setting('down_progress'))
        import urllib2
        request = urllib2.Request(url)
        request.add_header('User-Agent', USER_AGENT)
        request.add_unredirected_header('Host', request.get_host())
        response = urllib2.urlopen(request)
        
        content_length = 0
        if 'Content-Length' in response.info():
            content_length = int(response.info()['Content-Length'])
            
        file_name = file_name.replace('.strm', get_extension(url, response))
        full_path = os.path.join(path, file_name)
        log_utils.log('Downloading: %s -> %s' % (url, full_path), xbmc.LOGDEBUG)
        
        path = xbmc.makeLegalFilename(path)
        if not xbmcvfs.exists(path):
            try:
                try: xbmcvfs.mkdirs(path)
                except: os.mkdir(path)
            except Exception as e:
                raise Exception('Failed to create directory')

        file_desc = xbmcvfs.File(full_path, 'w')
        total_len = 0
        if progress:
            if progress == PROGRESS.WINDOW:
                dialog = xbmcgui.DialogProgress()
            else:
                dialog = xbmcgui.DialogProgressBG()
                
            dialog.create('Stream All The Sources', 'Downloading: %s...' % (file_name))
            dialog.update(0)
        while True:
            data = response.read(CHUNK_SIZE)
            if not data:
                break
            
            if progress == PROGRESS.WINDOW and dialog.iscanceled():
                break 
            
            total_len += len(data)
            if not file_desc.write(data):
                raise Exception('Failed to write file')
            
            percent_progress = (total_len)*100/content_length if content_length>0 else 0
            log_utils.log('Position : %s / %s = %s%%' % (total_len, content_length, percent_progress), xbmc.LOGDEBUG)
            if progress == PROGRESS.WINDOW:
                dialog.update(percent_progress)
            elif progress == PROGRESS.BACKGROUND:
                dialog.update(percent_progress, 'Stream All The Sources')
        else:
            builtin = 'XBMC.Notification(%s,Download Complete: %s, 5000, %s)'
            xbmc.executebuiltin(builtin % (ADDON.get_name(), file_name, ICON_PATH))
            log_utils.log('Download Complete: %s -> %s' % (url, full_path), xbmc.LOGDEBUG)

        file_desc.close()
        if progress:
            dialog.close()
            
    except Exception as e:
        msg = 'Error (%s) during download: %s' % (str(e), file_name)
        log_utils.log('Error (%s) during download: %s -> %s' % (str(e), url, file_name), xbmc.LOGERROR)
        builtin = 'XBMC.Notification(%s,%s, 5000, %s)'
        xbmc.executebuiltin(builtin % (ADDON.get_name(), msg, ICON_PATH))

def get_extension(url, response):
    filename = url2name(url)
    if 'Content-Disposition' in response.info():
        cd_list = response.info()['Content-Disposition'].split('filename=')
        if len(cd_list)>1:
            filename = cd_list[-1]
            if filename[0] == '"' or filename[0] == "'":
                filename = filename[1:-1]
    elif response.url != url: 
        filename = url2name(response.url)
    ext=os.path.splitext(filename)[1]
    if not ext: ext = DEFAULT_EXT
    return ext
    
def url2name(url):
    return os.path.basename(urllib.unquote(urlparse.urlsplit(url)[2]))

def sort_progress(episodes, sort_order):
    if sort_order == TRAKT_SORT.TITLE:
        return sorted(episodes, key=lambda x:x['show']['title'].lstrip('The '))
    elif sort_order == TRAKT_SORT.ACTIVITY:
        return sorted(episodes, key=lambda x:iso_2_utc(x['last_watched_at']), reverse=True)
    elif sort_order == TRAKT_SORT.LEAST_COMPLETED:
        return sorted(episodes, key=lambda x:(x['percent_completed'], x['completed']))
    elif sort_order == TRAKT_SORT.MOST_COMPLETED:
        return sorted(episodes, key=lambda x:(x['percent_completed'], x['completed']), reverse=True)
    elif sort_order == TRAKT_SORT.PREVIOUSLY_AIRED:
        return sorted(episodes, key=lambda x:iso_2_utc(x['episode']['first_aired']))
    elif sort_order == TRAKT_SORT.RECENTLY_AIRED:
        return sorted(episodes, key=lambda x:iso_2_utc(x['episode']['first_aired']), reverse=True)
    else: # default sort set to activity
        return sorted(episodes, key=lambda x:x['last_watched_at'], reverse=True)

