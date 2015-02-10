

import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,xbmc,os,xbmcaddon

import threading
import time

downloadPause = False
running = True
killed = False
type='unknown'
version=''
name=''
description=''
date='',
thumb='default'
icon='default',
URL=''
DLloc=''
player='default'
processor=''
playpath=''
swfplayer=''
pageurl=''
referer=''
agent=''
background='default'
rating=''
infotag=''
view='default'
headers=''
processed=False
data={}


        

def run(name,url,thumb,ext, localfile):
    while not killed:
        filename = name+ext
        time.sleep(1.0) #delay 1 second
        #check if there are files in the download queue.
        while (killed == False) and (running == True): #and (playlist_src.size() > 0):
            #there are files to be downloaded.
            #self.download_queue()
            #entry = self.metaList(url,name,download_path,thumb)
            download_file(url, localfile, filename)
            #download_file(url, localfile+name+ext)

def download_start(shutdown = False):
    shutdown = shutdown
    running = True

def download_stop():
    running = False

def download_isrunning():
    return running

def pause():
    downloadPause = True

def resume():
    downloadPause = False

def kill():
    killed = True

#####   passes a download path, name , Thumb image AND url

# Set up  file info into a list
def metaList(URL,name,DLloc,thumb):
    entry= []
    entry.type = type    #(required) type (playlist, image, video, audio, text)
    entry.version = version #(optional) playlist version
    entry.name = name    #(required) name as displayed in list view
    entry.description = description    #(optional) description of this item
    entry.date = date    #(optional) release date of this item (yyyy-mm-dd)
    entry.thumb = thumb  #(optional) URL to thumb image or 'default'
    entry.icon = icon  #(optional) URL to icon image or 'default'
    entry.URL = URL      #(required) URL to playlist entry
    entry.DLloc = DLloc  #(optional) Download location
    entry.player = player #(optional) player core to use for playback
    entry.processor = processor #(optional) URL to mediaitem processing server
    entry.playpath = playpath #(optional)
    entry.swfplayer = swfplayer #(optional)
    entry.pageurl = pageurl #(optional)
    entry.background = background #(optional) background image
    entry.rating = rating #(optional) rating value
    infotag = infotag
    referer = referer #(optional)
    agent = agent #(optional)
    entry.view = view #(optional) List view option (list, panel)
    entry.processed = processed
    entry.data = data #(optional) multi-purpose slot for Python dictionaries

    meta.append(entry)
    return entry


# For adding playlist entries for incomplete downloads and things
def add_list(entry,item_list):
    # adds the file to the lists with the following info for resuming and stuff
    if item_list == 'incdl': loc_list = datapaths + incomplete_downloads; playlist = playlist_inc
    elif item_list== 'cmpdl': loc_list = datapaths + downloads_complete; playlist = playlist_dst

    # you have the queue so just need the info to match what you have
    else: item_list ='queue'; loc_list = datapaths + downloads_queue; playlist = playlist_src
    state = 0 #success

    ###  creates a playlist entry and is called before and after  the download
    #tmp = CMediaItem()  # create new item
    #tmp.type = entry.type   # you wont need
    tmp.name = name
    tmp.thumb = thumb
    tmp.URL = URL
    tmp.DLloc = DLloc
    #tmp.player = entry.player   # you might not need
    #tmp.processor = entry.processor   # you wont need
    #tmp.background = entry.background   # you wont need
    #### remove duplicates from list then add new item
    pos = 0
    for line in open(loc_list,'r'):
        if line == '#\n' : pos+=1
        elif DLloc in line: playlist.remove(pos-1)
    playlist.save(loc_list)
    playlist.add(tmp); playlist.save(loc_list)

######################################################

#########################################################################
# Call Description ex: string_size, raw_size = self.file_size(size,req)
# Parameters : size = number
#              requ format example = [urllib2.Request(URL, None, headers)]
# Returns: ts_size as a rounded string ex:(1.1 KB) or Unknown
#          fl_size as a number ex:(1132)
#########################################################################
def file_size(r_size=0,requ=''):
    ts_size = 'Unknown'; fl_size = 0
    if (r_size == 0 or r_size == 'Unknown') and requ == '': return ts_size, fl_size
    try:
        if r_size == 0 and requ != '':
            fr = urllib2.urlopen(requ)
            #print(fr.headers)
            if 'Content-Length' not in fr.headers: return ts_size, fl_size
            fl_size = fr.headers['Content-Length']; fr.close()
            r_size = (fl_size)
        size_bt = float(r_size)
        if fl_size  >= 0 and r_size != 0:
            if (size_bt / 10**3 ) < 1  : ts_size = str(size_bt) +' Bs'
            elif (size_bt / 10**6)  < 1 : ts_size = str(round(size_bt / 10**3,1)) +' KB'
            elif (size_bt / 10**9)  < 1 : ts_size = str(round(size_bt / 10**6,1)) +' MB'
            elif (size_bt / 10**12)  < 1: ts_size = str(round(size_bt / 10**9,1)) +' GB'
            else: ts_size = str(round(size_bt /10**12,1)) +' TB'
    except Exception, e: print('ERROR fl_size function: '+'e = ' + str(e))
    return  ts_size, fl_size
    #end of function


#######################################################
#def download_file(self, entry, header=""):
def download_file(URL,localfile,filename, header=""):
    #print "URL AND LOCAL FOLDER ARE = " +url +localfile
    state = 0 #success

    url = URL           # resolved url
    localfile = localfile     # download location

    #download of FTP file is handled in a separte function    ## use this to filter out ftp sites?
    if URL[:3] == 'ftp':
        #self.download_fileFTP(entry, header)
        state = -1
        return

    if URL[:4] != 'http':
        state = -1 #URL does not point to internet file.
        return

    #Continue with HTTP download
    #self.MainWindow.dlinfotekst.setLabel('(' + header + ')' + " Retrieving file info...")

    #URL = urlopener.loc_url
    url = url.replace('http://','')
    existSize=0          # existing size = 0 Bytes

    # check for localfile and find resume point
    
    if  os.path.exists(localfile+filename)== "True":
        #os.makedirs(localfile)
    #if os.path.exists(localfile+url):
        existSize = os.path.getsize(localfile+filename)
        #Message("Exist size: " + str(existSize))
        #If the file exists, then only download the remainder
        NoRangeEntry = headers
        for RangeEntry in 'Ranges','Range','':
            if RangeEntry != '':
                try:            #### test for range support
                    headers[RangeEntry] = 'bytes=%s-' % existSize
                    req = urllib2.Request(URL, None, headers)
                    f = urllib2.urlopen(req)  # check if byte range in header
                    break
                except: pass         #Expected error: HTTP Error 416: Requested Range Not Satisfiable'
            else:           #### if ranges are not supported
                try:
                    req = urllib2.Request(URL, None, NoRangeEntry)
                    f = urllib2.urlopen(req)
                except Exception as e:
                    state = -1; print('ERROR URL= ' + str(URL)); print('failed to open the URL file' + str(e))
                    return

    else:   # if the loacal file does not exist
        try: os.makedirs(localfile)
        except: pass
        #print('URL = ' +str(URL)); print('headers = ' + str(headers))
        #file = open(localfile+filename, 'w+')
        try:
            req = urllib2.Request(URL, None)
            f = urllib2.urlopen(req)
        except Exception as e:
            state = -1; print ('failed to open the URL file', str(e))
            return

    try: size_string,size_raw = file_size(0,req)     #### gets size of remote URL file or sets size_string = Unknown and size_raw = 0
    except Exception as e:
        state = -1; print ('failed to open the URL file', str(e))
        return

    # If the file exists, but we already have the whole thing, don't download again
    size = size_raw  #The remaining bytes
    file = open(localfile+filename, 'w+')
    #file = open(localfile+url,'ab+')           #### opens and/or creates the destination file with append

    if ((size > 0) and (size != existSize)) or size == 0:
        bytes = existSize   # bytes downloaded already
        size = int(size) + int(existSize)   # total size
        total_chunks = 0


        # init DL-speed calculation for GUI
        starttime=time.time()
        startSize = bytes
        deltatime = 0
        deltasize = 0
        dlspeed = 0

        #add_list(entry,'incdl')             #### add to incomplete downloads playlist, removing existing duplicate entries
        try:
            #self.MainWindow.dlinfotekst.setLabel('(' + header + ')' + " Downloading file...")   # GUI output

            # Main download engine
            #download in chunks of 100kBytes
            while ((bytes < size) or (size == 0) or (size_string == 'Unknown')) and (killed == False) and (running == True):
                chunk = 100 * 1024   # 100kBytes chunks    #### can be increased if you want
                total_chunks += chunk           #### total chunks read
                if ((bytes + chunk) > size and size!=0) and (size_string != 'Unknown'):
                    chunk = size-bytes #remainder
                # Read the open url file
                data = f.read(chunk)
                #### if total_chunks <= whats already downloaded dont write it for unknown file size (append issue)
                if data !='' and (size_string == 'Unknown') and (total_chunks > os.path.getsize(localfile)):
                    file.write(data)           #### write statement for files of known size
                elif data !='' and (size_string != 'Unknown'):
                    file.write(data)           #### write statement for files of known size
                bytes = bytes + chunk

                # Setup for GUI
                if size == 0 or size_string == 'Unknown' : percent = 'Unknown %'
                else: percent = str(100 * bytes / size) + '%'
                size_string,r_size = file_size(size,req)
                done,r_size = file_size(bytes,'')

                deltatime = time.time() - starttime
                if deltatime >=5: #update every 5 seconds
                    #calculate the download speed
                    deltasize = bytes - startSize
                    dlspeed = (deltasize / 1024) / deltatime
                    starttime = time.time()
                    startsize = bytes

                # Format GUI output
                line2 = '(%s) %s of %s - %s - %dkB/s' % (header, done, size_string, percent, dlspeed)
                #self.MainWindow.dlinfotekst.setLabel(line2)   # GUI output

                # stops downloader when no more data
                if (size >= 0 or size_string == 'Unknown') and data == '':
                    break
                # Pause download
                while downloadPause and running and not kill: pass
            f.close() #close the URL

        except Exception as e:
            state = -1; print ('failed to download the file', str(e))
            line2 = '%s  %s' % ('failed to download', str(name))   # Format GUI output
            #self.MainWindow.dlinfotekst.setLabel(line2)   # GUI output

        if (killed == True) or (running == False):
            state = -2   # failed to download the file

    file.close() #close the destination file

    #add the downloaded file to the downloaded playlist
    if state == 0:
        add_list(entry,'cmpdl')

        #### remove from Incomplete Downloads playlist
        pos = 0; incdl = datapaths + incomplete_downloads
        for line in open(incdl,'r'):
            if line == '#\n' : pos+=1
            elif DLloc in line: playlist_inc.remove(pos-1)
        playlist_inc.save(incdl)
