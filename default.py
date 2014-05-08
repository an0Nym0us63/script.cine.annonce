# -*- coding: latin-1 -*-
import xbmcgui
import xbmcaddon
addon = xbmcaddon.Addon()
addon_path = addon.getAddonInfo('path')

REMOTE_DBG = False

# append pydev remote debugger
if REMOTE_DBG:
    # Make pydev debugger works for auto reload.
    # Note pydevd module need to be copied in XBMC\system\python\Lib\pysrc
    try:
        import pysrc.pydevd as pydevd
    # stdoutToServer and stderrToServer redirect stdout and stderr to eclipse console
        pydevd.settrace('localhost', stdoutToServer=True, stderrToServer=True)
    except ImportError:
        sys.stderr.write("Error: " +
            "You must add org.python.pydev.debug.pysrc to your PYTHONPATH.")
        sys.exit(1)

class blankWindow(xbmcgui.WindowXML):
    def onInit(self):
        pass

def selectchoice():
    success = False  
    Choice = ['Proposition de films','Voir mes bandes annonces', 'Suggestions','Rechercher un film']
    selectedchoice = xbmcgui.Dialog().select(u"Que voulez vous faire ?", Choice)
    if not selectedchoice == -1:
        selectedchoice = Choice[selectedchoice]
        if selectedchoice == 'Proposition de films':
            selectedchoice = 1
            success = True
        elif selectedchoice == 'Voir mes bandes annonces':
            selectedchoice = 2
            success = True
        elif selectedchoice == 'Suggestions':
            selectedchoice = 3
            success = True
        elif selectedchoice == 'Rechercher un film':
            selectedchoice=4
            success = True
        else:
            success = False
    return success, selectedchoice
bs = blankWindow('script-BlankWindow.xml', addon_path,'default',)
bs.show()
success, choix = selectchoice()
if success:
    if choix==1:
        import xbmc
        import xbmcgui
        import xbmcaddon
        import random
        import simplejson
        import time
        import SelectionFilters as sf
        from datetime import date
        ACTION_PREVIOUS_MENU = 10
        ACTION_SELECT_ITEM = 7
        ACTION_MOUSE_LEFT_CLICK = 100
        filterGenres=None
        filterYear=None
        filterlast=None
        filterUnwatched=None
        filterdisney=None
        _A_ = xbmcaddon.Addon()
        _S_ = _A_.getSetting
        
        
        actualyear = date.today().year
        addon = xbmcaddon.Addon()
        addon_path = addon.getAddonInfo('path')
        hide_info = addon.getSetting('hide_info_sur')
        exit_requested = False
        class movieWindow(xbmcgui.WindowXMLDialog):
        
            def onInit(self):
                
                global trailer
                global do_timeout
                if hide_info == 'false':
                    w=infoWindow('script-DialogVideoInfo.xml',addon_path,'default')
                    do_timeout=True
                    w.doModal()
                    do_timeout=False
                    del w
                    if exit_requested:
                        xbmc.Player().stop()
                else:
                    xbmc.Player().play(trailer["trailer"])
                self.getControl(30011).setLabel(trailer["title"] + ' - ' + str(trailer["year"]))
                self.getControl(30011).setVisible(True)
                while xbmc.Player().isPlaying():                
                    xbmc.sleep(250)
                self.close()
                
            def onAction(self, action):
                ACTION_PREVIOUS_MENU = 10
                ACTION_BACK = 92
                ACTION_ENTER = 7
                ACTION_I = 11
                ACTION_LEFT = 1
                ACTION_RIGHT = 2
                ACTION_UP = 3
                ACTION_DOWN = 4
                ACTION_TAB = 18
                ACTION_STOP = 13
                
                xbmc.log('action  =' + str(action.getId()))
                
                global exit_requested
                global movie_file
                if action == ACTION_PREVIOUS_MENU or action == ACTION_LEFT or action == ACTION_BACK or action == ACTION_STOP:
                    xbmc.Player().stop()
                    exit_requested = True
                    self.close()
        
                if action == ACTION_RIGHT or action == ACTION_TAB:
                    xbmc.Player().stop()
                    
                if action == ACTION_ENTER:
                    exit_requested = True
                    xbmc.Player().stop()
                    movie_file = trailer["file"]
                    self.getControl(30011).setVisible(False)
                    self.close()
                
                if action == ACTION_I or action == ACTION_UP:
                    self.getControl(30011).setVisible(False)
                    w=infoWindow('script-DialogVideoInfo.xml',addon_path,'default')
                    w.doModal()
                    self.getControl(30011).setVisible(True)
                    
        class infoWindow(xbmcgui.WindowXMLDialog):
        
            def onInit(self):
                self.getControl(30001).setImage(trailer["thumbnail"])
                self.getControl(30003).setImage(trailer["fanart"])
                self.getControl(30002).setLabel(trailer["title"])
                directors = trailer["director"]
                movieDirector=''
                for director in directors:
                    movieDirector = movieDirector + director + ', '
                    if not movieDirector =='':
                        movieDirector = movieDirector[:-2]
                self.getControl(30005).setLabel(movieDirector)
                writers = trailer["writer"]
                movieWriter=''
                for writer in writers:
                    movieWriter = movieWriter + writer + ', '
                    if not movieWriter =='':
                        movieWriter = movieWriter[:-2]
                actors = trailer["cast"]
                movieActor=''
                actorcount=0
                for actor in actors:
                    actorcount = actorcount + 1
                    movieActor = movieActor + actor['name'] + ", "
                    if actorcount == 6: break
                    if not movieActor == '':
                        movieActor = movieActor[:-2]
                self.getControl(30007).setLabel(movieWriter)
                self.getControl(30006).setLabel(movieActor)
                
                self.getControl(30009).setText(trailer["plot"])
                movieStudio=''
                studios=trailer["studio"]
                for studio in studios:
                    movieStudio = movieStudio + studio + ', '
                    if not movieStudio =='':
                        movieStudio = movieStudio[:-2]
                self.getControl(30010).setLabel(movieStudio + ' - ' + str(trailer["year"]))
                movieGenre=''
                genres = trailer["genre"]
                for genre in genres:
                    movieGenre = movieGenre + genre + ' / '
                if not movieGenre =='':
                    movieGenre = movieGenre[:-3]
                self.getControl(30011).setLabel(str(trailer["runtime"] / 60) + ' Minutes - ' + movieGenre)
                imgRating='ratings/notrated.png'
                if trailer["mpaa"].startswith('G'): imgRating='ratings/g.png'
                if trailer["mpaa"] == ('G'): imgRating='ratings/g.png'
                if trailer["mpaa"].startswith('Rated G'): imgRating='ratings/g.png'
                if trailer["mpaa"].startswith('PG '): imgRating='ratings/pg.png'
                if trailer["mpaa"] == ('PG'): imgRating='ratings/pg.png'
                if trailer["mpaa"].startswith('Rated PG'): imgRating='ratings/pg.png'
                if trailer["mpaa"].startswith('PG-13 '): imgRating='ratings/pg13.png'
                if trailer["mpaa"] == ('PG-13'): imgRating='ratings/pg13.png'
                if trailer["mpaa"].startswith('Rated PG-13'): imgRating='ratings/pg13.png'
                if trailer["mpaa"].startswith('R '): imgRating='ratings/r.png'
                if trailer["mpaa"] == ('R'): imgRating='ratings/r.png'
                if trailer["mpaa"].startswith('Rated R'): imgRating='ratings/r.png'
                if trailer["mpaa"].startswith('NC17'): imgRating='ratings/nc17.png'
                if trailer["mpaa"].startswith('Rated NC17'): imgRating='ratings/nc1.png'
                self.getControl(30013).setImage(imgRating)
                if do_timeout:
                    xbmc.sleep(5000)
                    xbmc.Player().play(trailer["trailer"])
                    self.close()
                
            def onAction(self, action):
                ACTION_PREVIOUS_MENU = 10
                ACTION_BACK = 92
                ACTION_ENTER = 7
                ACTION_I = 11
                ACTION_LEFT = 1
                ACTION_RIGHT = 2
                ACTION_UP = 3
                ACTION_DOWN = 4
                ACTION_TAB = 18                
                ACTION_STOP = 13
                
                xbmc.log('action  =' + str(action.getId()))
                global do_timeout
                global exit_requested
                global movie_file
                if action == ACTION_PREVIOUS_MENU or action == ACTION_LEFT or action == ACTION_BACK or action == ACTION_STOP:
                    do_timeout=False
                    xbmc.Player().stop()
                    exit_requested=True
                    self.close()
                    
                if action == ACTION_I or action == ACTION_DOWN:
                    self.close()
                    
                if action == ACTION_RIGHT or action == ACTION_TAB:
                    xbmc.Player().stop()
                    self.close()
        
                if action == ACTION_ENTER:
                    movie_file = trailer["file"]
                    xbmc.Player().stop()
                    exit_requested=True
                    self.close()
                
        class blankWindow(xbmcgui.WindowXML):
            def onInit(self):
                pass
        
        class XBMCPlayer(xbmc.Player):
            def __init__( self, *args, **kwargs ):
                pass
            def onPlayBackStarted(self):
                pass
            
            def onPlayBackStopped(self):
                global exit_requested
                pass
        
        def log(txt):
            message = 'script.watchlist: %s' % txt
            xbmc.log(msg=message, level=xbmc.LOGDEBUG)
        
        #####################
        # set our preferences
        #####################
        
        # Defaults
        numRuntime = int(float(_S_( "longruntime" ) ) )
        numTrailers = 3
        promptGenres = promptYear = promptUnwatched = promptdisney = fanartMode = playlistMode = promptlast = False
        
        if (_S_("runmode")) == "1":
            # User has set defined mode in settings
            promptUser = False
            if (_S_("filtergenres")) == "0":
                promptGenres = True
            elif (_S_("filtergenres")) == "1":
                promptGenres = False
                filterGenres = True
            else:
                promptGenres = False
                filterGenres = False
            if (_S_("filteryear")) == "0":
                promptYear = True
            elif (_S_("filteryear")) == "1":
                promptYear = False
                filterYear = True
            else:
                promptYear = False
                filterYear = False
            if (_S_("filterdisney")) == "0":
                promptdisney = True
            elif (_S_("filterdisney")) == "1":
                promptdisney = False
                filterdisney = True
            else:
                promptdisney = False
                filterdisney = False
            if (_S_("filterlast")) == "0":
                promptlast = True
            elif (_S_("filterlast")) == "1":
                promptlast = False
                filterlast = True
            else:
                promptlast = False
                filterlast = False
            if (_S_("filterunwatched")) == "0":
                promptUnwatched = True
            elif (_S_("filterunwatched")) == "1":
                promptUnwatched = False
                filterUnwatched = True
            else:
                promptUnwatched = False
                filterUnwatched = False
          
            trailerMode = _S_( "trailermode" ) == "true"
          
            numTrailers = int(float(_S_( "numtrailers" ) ) )
            
            playlistMode = _S_("playlistmode") == "true"
          
        else: 
            # if not, we're in prompt mode
            promptUser = True
            filterUnwatched = filterYear = filterGenres = filterdisney = trailerMode = filterlast = False
            playlistMode = _S_("playlistmode") == "true"
        
        def getMovieLibrary():
            # get the raw JSON output
            try:
                moviestring = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params": { "fields": ["genre", "playcount", "file"]}, "id": 1}')
                moviestring = unicode(moviestring, 'utf-8', errors='ignore')
                movies = simplejson.loads(moviestring)
                testError = movies["result"]
            except:
                moviestring = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params": { "properties": ["title","playcount", "lastplayed", "studio", "writer", "plot", "votes", "top250", "originaltitle", "director", "tagline", "fanart", "runtime", "mpaa", "rating", "thumbnail", "file", "year", "genre", "trailer","set","dateadded","cast"]}, "id": 1}')
                moviestring = unicode(moviestring, 'utf-8', errors='ignore')                                                            
                movies = simplejson.loads(moviestring)
            return movies
          
        def BuildFilter(movies):
            filter = sf.SelectionFilters()
          
            askGenres = askYear = askdisney = askUnwatched = askTrailer = asklast = runtime = 0
            
            if promptUser or promptUnwatched:  
                askUnwatched = xbmcgui.Dialog().yesno("Films vus","Seulement les films non vus ?")
        
            if askUnwatched or filterUnwatched:
                filter.SetFilter("unwatched", True)
                unwatched = True
            else:
                unwatched = False
          
            if promptUser:  
                askTrailer = xbmcgui.Dialog().yesno("Voir des bandes-annonces", "Voulez vous voir des bandes annonces ?")
        
            if askTrailer:
                global trailerMode
                trailerMode = True
              
            if promptUser or promptGenres:
                askGenres = xbmcgui.Dialog().yesno("Filtrer sur un genre", "Voulez-vous choisir un genre ?")
        
            if askGenres or filterGenres:
                success, genre = selectGenre(unwatched, trailerMode)
                if success:
                    filter.SetFilter("genre", True, genre=genre)
          
            if promptUser or promptYear:    
                askYear = xbmcgui.Dialog().yesno(u"Filtrer sur l'année", u"Voulez-vous filtrer sur l'année ?")
            
            if askYear or filterYear:
                success, year = selectYear(unwatched, trailerMode)
                if success:
                    filter.SetFilter("year", True, year=year)
          
            if promptUser or promptlast:    
                asklast = xbmcgui.Dialog().yesno(u"Date de téléchargement", u"Voulez-vous filtrer sur la date de téléchargement?")
            
            if asklast or filterlast:
                success, last = selectlast(unwatched, trailerMode)
                if success:
                    filter.SetFilter("last", True, last=last)
          
            askRuntime = xbmcgui.Dialog().yesno(u"Filtrer durée", "Voulez-vous ignorer les films longs ?")
            
            if askRuntime:# or filterYear:
                runtime = numRuntime*60
                filter.SetFilter("runtime", True, runtime=runtime)
          
            if promptUser or promptdisney:
                askdisney = xbmcgui.Dialog().yesno("Filtrer les Disney", "Voulez-vous ignorer les Walt Disney ?")
        
            if askdisney or filterdisney:
                disney = u"Walt Disney"    
                filter.SetFilter("disney", True, disney=disney)
                
            return filter
        
        
        def selectGenre(filterWatched, trailer):
            success = False
            selectedGenre = ""
            myGenres = []
          
            for movie in moviesJSON["result"]["movies"]:
                # Let's get the movie genres
                # If we're only looking at unwatched movies then restrict list to those movies
                if (( filterWatched and movie["playcount"] == 0 ) or not filterWatched) and ((trailer and not movie["trailer"] == "") or not trailer):
                    #print movie["trailer"]
                    test = simplejson.dumps(movie["genre"],ensure_ascii=False, encoding='utf8')
                    #test = unicode(test, 'utf8', errors='ignore')
                    test = test.replace('"','')
                    test = test.replace(']','')
                    test = test.replace('[','')       
                    genres = test.split(", ")
                    for genre in genres:
                        # check if the genre is a duplicate
                        if not genre in myGenres:
                            # if not, add it to our list
                            myGenres.append(genre)
            myGenres.append("3D")
            # sort the list alphabetically        
            mySortedGenres = sorted(myGenres)
            # prompt user to select genre
            selectGenre = xbmcgui.Dialog().select("Choisissez le genre :", mySortedGenres)
            # check whether user cancelled selection
            if not selectGenre == -1:
                # get the user's chosen genre
                selectedGenre = mySortedGenres[selectGenre]
                success = True
            else:
                success = False
            # return the genre and whether the choice was successfull
            return success, selectedGenre
        
        
        def selectYear(filterWatched, trailer):
            success = False
            selectedYear = ""
            # sort the list alphabetically        
            myYear = [u'Cette année',u'2 dernières années', u'5 dernières années', u'10 dernières années', u'15 dernières années', u'20 dernières années', u'30 dernières années',u'50 dernières années']
            # prompt user to select genre
            selectYear = xbmcgui.Dialog().select(u"A partir de quelle année ", myYear)
            # check whether user cancelled selection
            if not selectYear == -1:
                # get the user's chosen genre
                selectedYear = myYear[selectYear].encode('utf-8')
                if selectedYear == u'Cette année'.encode('utf-8'):
                    selectedYear = int(actualyear) - 0
                    success = True
                elif selectedYear == u'2 dernières années'.encode('utf-8'):
                    selectedYear = int(actualyear) - 2
                    success = True
                elif selectedYear == u'5 dernières années'.encode('utf-8'):
                    selectedYear = int(actualyear) - 5
                    success = True
                elif selectedYear == u'10 dernières années'.encode('utf-8'):
                    selectedYear = int(actualyear) - 10
                    success = True
                elif selectedYear == u'15 dernières années'.encode('utf-8'):
                    selectedYear = int(actualyear) - 15
                    success = True
                elif selectedYear == u'20 dernières années'.encode('utf-8'):
                    selectedYear = int(actualyear) - 20
                    success = True
                elif selectedYear == u'30 dernières années'.encode('utf-8'):
                    selectedYear = int(actualyear) - 30
                    success = True
                elif selectedYear == u'50 dernières années'.encode('utf-8'):
                    selectedYear = int(actualyear) - 50
                    success = True
            else:
                success = False
            # return the year and whether the choice was successfult
            return success, selectedYear 
        
        def selectlast(filterWatched, trailer):
            success = False
            selectedlast = ""
            # sort the list alphabetically        
            mylast = [u'Aujourdhui',u'Cette semaine', u'Ces 15 derniers jours', u'Ce mois', u'Ces 2 derniers mois', u'Ces 3 derniers mois', u'Ces 6 derniers mois',u'Cette année']
            # prompt user to select genre
            selectlast = xbmcgui.Dialog().select(u"Téléchargé depuis quand ?", mylast)
            # check whether user cancelled selection
            if not selectlast == -1:
                # get the user's chosen genre
                selectedlast = mylast[selectlast]
                if selectedlast == u'Aujourdhui':
                    selectedlast = 1
                    success = True
                elif selectedlast == u'Cette semaine':
                    selectedlast = 7
                    success = True
                elif selectedlast == u'Ces 15 derniers jours':
                    selectedlast = 15
                    success = True
                elif selectedlast == u'Ce mois':
                    selectedlast = 31
                    success = True
                elif selectedlast == u'Ces 2 derniers mois':
                    selectedlast = 62
                    success = True
                elif selectedlast == u'Ces 3 derniers mois':
                    selectedlast = 93
                    success = True
                elif selectedlast == u'Ces 6 derniers mois':
                    selectedlast = 186
                    success = True
                elif selectedlast == u'Cette année'.encode('utf-8'):
                    selectedlast = 365
                    success = True
            else:
                success = False
            # return the year and whether the choice was successfult
            return success, selectedlast
          
        def getVideoPlaylists():
            videostring = unicode(xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Files.GetDirectory", "params": {"directory": "special://videoplaylists"}, "id": 1}'), errors='ignore')
            myVideoPlaylists = simplejson.loads(videostring)  
            return myVideoPlaylists
        
        def chooseVideoPlaylist(videoPlaylists):
            myPlaylists = {}
            selectPlaylist = []
            for playlist in videoPlaylists["result"]["files"]:
                myPlaylists[playlist["label"]] = playlist["file"]
                selectPlaylist.append(playlist["label"])
                #selectPlaylist.append("Cancel")
        
            a = xbmcgui.Dialog().select("Select playlist",selectPlaylist)  
            if not a == -1:
                playliststring = unicode(xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Files.GetDirectory", "params": {"directory": "' + myPlaylists[selectPlaylist[a]] + '", "media": "video"}, "id": 1}'), errors='ignore')
                myVideoPlaylists = simplejson.loads(playliststring)
                showfiles = []
                for movie in myVideoPlaylists["result"]["files"]:
                    showfiles.append(movie["file"])
            
                return True, showfiles
            else:
                return False, ""
        
        def getTrailers(movieList, numTrailers):
            trailerList = []
            global trailer
            global do_timeout
            global exit_requested  
            global trailerMode
            global movie_file
            movie_file=''
            exit_requested = False
            player = XBMCPlayer()
            # We need to check that we have enough trailers to meet our user's requirements  
            if len(movieList) <= numTrailers:
                # if we don't then we need to limit the number of trailers to show
                listLimit = len(movieList)
            else:
                listLimit = numTrailers
          
            # Build list of trailers
            myRandomMovies = []        
            while len(trailerList) < listLimit:
                movieN = random.choice(movieList)
                if not movieN in trailerList:
                    trailerList.append(movieN)           
                    myRandomMovies.append(movieN)
            if trailerMode:
                while not exit_requested:
                    for item in trailerList:
                        trailer=item
                        myMovieWindow=movieWindow('script-trailerwindow.xml', addon_path,'default',)
                        myMovieWindow.doModal()
                        del myMovieWindow
                        if exit_requested:
                            break
                    if not exit_requested:
                        while player.isPlaying():
                            xbmc.sleep(250)
                    exit_requested=True
                
            randomList = []
            i = 1
            for movie in myRandomMovies:
                movietitle = simplejson.dumps(movie["label"],ensure_ascii=False, encoding='utf8')
                movietitle = movietitle.replace('"','')
                movieyear = simplejson.dumps(movie["year"],ensure_ascii=False, encoding='utf8')
                movieyear = movieyear.replace('"','')
                moviegenre = simplejson.dumps(movie["genre"],ensure_ascii=False, encoding='utf8')
                moviegenre = moviegenre.replace('"','')
                movielenghth = simplejson.dumps(movie["runtime"]/3600,ensure_ascii=False, encoding='utf8')
                movielenghth = movielenghth.replace('"','')
                movielenghtm = simplejson.dumps((movie["runtime"] -(int(movielenghth)*3600))/60,ensure_ascii=False, encoding='utf8')
                movielenghth = movielenghth.replace('"','')
                movielenghtm = movielenghtm.replace('"','')
                randomList.append(str(i) + ' : '+ movietitle + ' (' +movieyear+') - ' + moviegenre +' - ' +movielenghth + 'h' + movielenghtm +'min')
                i+=1
            if movie_file:
                success = True
                myMovie=movie_file
            else:    
                if randomList == []:
                    a = xbmcgui.Dialog().ok('Dommage', u'Aucun de vos films ne repond aux critères')
                else:
                    a = xbmcgui.Dialog().select("Quel film voulez-vous lancer :", randomList)
                if not a == -1 and not randomList == []:
                    success = True
                    myMovie = simplejson.dumps(myRandomMovies[a]["file"],ensure_ascii=False, encoding='utf8')
                else:
                    success = False
                    myMovie = ""
            
            return success, myMovie
        
        def FilterMovies(movies, filter, trailer):
            filteredlist = []
            for movie in movies["result"]["movies"]:
                if ((trailer and not movie["trailer"] == '') or not trailer):
                    if filter.MeetsCriteria(movie):
                        filteredlist.append(movie)
        
            return filteredlist
        global movie_file
        moviesJSON = getMovieLibrary()
        
        filter = BuildFilter(moviesJSON)
        # apply filter to our library
        filteredMovies = FilterMovies(moviesJSON, filter, trailerMode)
        success, myMovie = getTrailers(filteredMovies, numTrailers)
        if success:
            xbmc.executebuiltin('Playmedia(' + myMovie.encode('utf-8') + ')')
        elif _S_( "randommode" )=='true':
            randomMovie = random.choice(filteredMovies)
            xbmc.executebuiltin('Playmedia(' + randomMovie["file"].encode('utf-8') + ')')
        del bs
    elif choix==2:
        import randomtrailer
    elif choix==3:
        # Random trailer player
        import xbmc
        import xbmcvfs
        import xbmcgui
        from urllib import quote_plus, unquote_plus
        import datetime
        import urllib
        import urllib2
        import re
        import sys
        import os
        import random
        import json
        import time
        import xbmcaddon
        import unicodedata
        from bs4 import BeautifulSoup
        import xml.dom.minidom
        from xml.dom.minidom import Node
        from allocine import allocine
        api = allocine()
        api.configure('100043982026','29d185d98c984a359e6e6f26a0474269')
        addon = xbmcaddon.Addon()
        number_trailers =  addon.getSetting('number_trailers_sug')
        do_curtains = 'false'
        hide_info = addon.getSetting('hide_info_sug')
        hide_title = addon.getSetting('hide_title_sug')
        addon_path = addon.getAddonInfo('path')
        resources_path = xbmc.translatePath( os.path.join( addon_path, 'resources' ) ).decode('utf-8')
        media_path = xbmc.translatePath( os.path.join( resources_path, 'media' ) ).decode('utf-8')
        open_curtain_path = xbmc.translatePath( os.path.join( media_path, 'OpenSequence.mp4' ) ).decode('utf-8')
        close_curtain_path = xbmc.translatePath( os.path.join( media_path, 'ClosingSequence.mp4' ) ).decode('utf-8')
        exit_requested = False
        movie_file = ''
        opener = urllib2.build_opener()
        
        if len(sys.argv) == 2:
            do_genre ='false'
        
        trailer=''
        info=''
        do_timeout = False
        played = []
        
        def getTitleFont():
            title_font='font13'
            base_size=20
            multiplier=1
            skin_dir = xbmc.translatePath("special://skin/")
            list_dir = os.listdir( skin_dir )
            fonts=[]
            fontxml_path =''
            font_xml=''
            for item in list_dir:
                item = os.path.join( skin_dir, item )
                if os.path.isdir( item ):
                    font_xml = os.path.join( item, "Font.xml" )
                if os.path.exists( font_xml ):
                    fontxml_path=font_xml
                    break
            dom =  xml.dom.minidom.parse(fontxml_path)
            fontlist=dom.getElementsByTagName('font')
            for font in fontlist:
                name = font.getElementsByTagName('name')[0].childNodes[0].nodeValue
                size = font.getElementsByTagName('size')[0].childNodes[0].nodeValue
                fonts.append({'name':name,'size':float(size)})
            fonts =sorted(fonts, key=lambda k: k['size'])
            for f in fonts:
                if f['name']=='font13':
                    multiplier=f['size'] / 20
                    break
            for f in fonts:
                if f['size'] >= 38 * multiplier:
                    title_font=f['name']
                    break
            return title_font
        
        def getInfo(title,year):
            data = {}
            data['query'] = title
            data['year'] = str(year)
            data['api_key'] = '99e8b7beac187a857152f57d67495cf4'
            data['language'] ='fr'
            url_values = urllib.urlencode(data)
            url = 'https://api.themoviedb.org/3/search/movie'
            full_url = url + '?' + url_values
            req = urllib2.Request(full_url)
            infostring = urllib2.urlopen(req).read()
            infostring = json.loads(infostring)
            if len(infostring['results']) > 0:
                results=infostring['results'][0]
                movieId=str(results['id'])
                if not movieId == '':
                    data = {}
                    data['api_key'] = '99e8b7beac187a857152f57d67495cf4'
                    data['append_to_response'] ='credits'
                    url_values = urllib.urlencode(data)
                    url = 'https://api.themoviedb.org/3/movie/' + movieId
                    full_url = url + '?' + url_values
                    req = urllib2.Request(full_url)
                    infostring = urllib2.urlopen(req).read()
                    infostring = json.loads(infostring)
                    director=[]
                    writer=[]
                    cast=[]
                    plot=''
                    runtime=''
                    genre=[]
                    plot=infostring['overview']
                    runtime=infostring['runtime']
                    genres=infostring['genres']
                    for g in genres:
                        genre.append(g['name'])
                    castMembers = infostring['credits']['cast']
                    castcount=0
                    for castMember in castMembers:
                        castcount = castcount + 1
                        cast.append(castMember['name'])     
                        if castcount == 6:break
                    crewMembers = infostring['credits']['crew']
                    for crewMember in crewMembers:
                        if crewMember['job'] =='Director':
                            director.append(crewMember['name'])
                        if crewMember['department']=='Writing':
                            writer.append(crewMember['name'])
            else:
                director=['Unavailable']
                writer=['Unavailable']
                cast=['Unavailable']
                plot='Unavailable'
                runtime=0
                genre=['Unavailable']
            dictInfo = {'director':director,'writer':writer,'plot':plot,'cast':cast,'runtime':runtime,'genre':genre}
            return dictInfo
              
        def getTmdbTrailers(choice):
            tmdbTrailers=[]
            if choice=='conf':
                if addon.getSetting("tmdb_source") == '0':source='popular'
                if addon.getSetting("tmdb_source") == '1':source='top_rated'
                if addon.getSetting("tmdb_source") == '2':source='upcoming'
                if addon.getSetting("tmdb_source") == '3':source='now_playing'
                if addon.getSetting("tmdb_source") == '4':source='dvd'
                if addon.getSetting("tmdb_source") == '5':source='all'
            elif choice=='none':
                source='all'
            else:
                source=choice
            
            if source=='all':
                data = {}
                data['api_key'] = '99e8b7beac187a857152f57d67495cf4'
                data['sort_by'] ='popularity.desc'
                data['language'] ='fr'
                url_values = urllib.urlencode(data)
                url = 'http://api.themoviedb.org/3/discover/movie'
                full_url = url + '?' + url_values
                req = urllib2.Request(full_url)
                infostring = urllib2.urlopen(req).read()
                infostring = json.loads(infostring)
                total_pages=infostring['total_pages']
                if total_pages > 1000: total_pages=1000
                for i in range(1,11):
                    data = {}
                    data['api_key'] = '99e8b7beac187a857152f57d67495cf4'
                    data['sort_by'] ='popularity.desc'
                    data['language'] ='fr'
                    data['page']=random.randrange(1,total_pages+1)
                    url_values = urllib.urlencode(data)
                    url = 'http://api.themoviedb.org/3/discover/movie'
                    full_url = url + '?' + url_values
                    req = urllib2.Request(full_url)
                    infostring = urllib2.urlopen(req).read()
                    infostring = json.loads(infostring)
                    for movie in infostring['results']:
                        id=movie['id']
                        dict={'trailer':'tmdb','id': id,'source':'tmdb','title':movie['title']}
                        tmdbTrailers.append(dict)
        
            elif source=='dvd':
                data={}
                data['apikey']='99dgtphe3c29y85m2g8dmdmt'
                data['country'] = 'us'
                url_values = urllib.urlencode(data)
                url = 'http://api.rottentomatoes.com/api/public/v1.0/lists/dvds/new_releases.json'
                full_url = url + '?' + url_values
                req = urllib2.Request(full_url)
                response = urllib2.urlopen(req).read()
                infostring = json.loads(response)
                for movie in infostring['movies']:
                    data={}
                    data['api_key']='99e8b7beac187a857152f57d67495cf4'
                    data['query']=movie['title']
                    data['year']=movie['year']
                    url_values = urllib.urlencode(data)
                    url = 'https://api.themoviedb.org/3/search/movie'
                    full_url = url + '?' + url_values
                    req = urllib2.Request(full_url)
                    infostring = urllib2.urlopen(req).read()
                    infostring = json.loads(infostring)
                    for m in infostring['results']:
                        id=m['id']
                        dict={'trailer':'tmdb','id': id,'source':'tmdb','title':movie['title']}
                        tmdbTrailers.append(dict)
                        break
            
            elif source=='upcoming':
                movies=getallocinetrailer('comingsoon')
                for movie in movies['feed']['movie']:
                        title=movie['title']
                        try:
                            year=movie['productionYear']
                        except:
                            year=''
                        try:
                            plot=movie['synopsisShort'].encode("utf-8").replace('<p>','').replace('</p>','')
                        except:
                            plot=''
                        try:
                            releasedate=movie['release']['releaseDate']
                            if len(releasedate)>=4:
                                if len(releasedate)>=7:
                                    releasedate=releasedate[8:10]+'/'+releasedate[5:7]+'/'+releasedate[0:4]
                                else:releasedate=releasedate[5:7]+'/'+releasedate[0:4]
                                                                
                        except:
                            releasedate=year
                        try:
                            runtime=str(int(movie['runtime'])/60)
                        except:
                            runtime=''
                        try:
                            thumbs=movie['defaultMedia']['media']['thumbnail']['href']
                        except:
                            thumbs=''
                        try:
                            poster=movie['poster']['href']
                        except:
                            poster=''
                        
                        pagetrailer=''
                        for x in movie['link']:
                            if x.has_key('name') and 'Bandes annonces' in x['name']:
                                pagetrailer=x['href']
                            else:
                                continue
                            title=title.encode("utf-8")
                            dict={'trailer':pagetrailer,'id': [title,year,plot,releasedate,runtime,thumbs,poster],'source':'allo','title':movie['title']}
                            tmdbTrailers.append(dict)
            
            elif source=='now_playing':
                movies=getallocinetrailer('nowshowing')
                for movie in movies['feed']['movie']:
                        title=movie['title']
                        try:
                            year=movie['productionYear']
                        except:
                            year=''
                        try:
                            plot=movie['synopsisShort'].encode("utf-8").replace('<p>','').replace('</p>','')
                        except:
                            plot=''
                        try:
                            releasedate=movie['release']['releaseDate']
                            if len(releasedate)>=4:
                                if len(releasedate)>=7:
                                    releasedate=releasedate[8:10]+'/'+releasedate[5:7]+'/'+releasedate[0:4]
                                else:releasedate=releasedate[5:7]+'/'+releasedate[0:4]
                                                                
                        except:
                            releasedate=year
                        try:
                            runtime=str(int(movie['runtime'])/60)
                        except:
                            runtime=''
                        try:
                            thumbs=movie['defaultMedia']['media']['thumbnail']['href']
                        except:
                            thumbs=''
                        try:
                            poster=movie['poster']['href']
                        except:
                            poster=''
                        pagetrailer=''
                        for x in movie['link']:
                            if x.has_key('name') and 'Bandes annonces' in x['name']:
                                pagetrailer=x['href']
                            else:
                                continue
                            title=title.encode("utf-8")
                            print str(movie)
                            dict={'trailer':pagetrailer,'id': [title,year,plot,releasedate,runtime,thumbs,poster],'source':'allo','title':movie['title']}
                            tmdbTrailers.append(dict)
            
            else:
                page=0
                for i in range(0,11):
                    page=page+1
                    data = {}
                    data['api_key'] = '99e8b7beac187a857152f57d67495cf4'
                    data['page'] = page
                    data['language']='fr'
                    data['sort_by'] ='popularity.desc'
                    url_values = urllib.urlencode(data)
                    url = 'https://api.themoviedb.org/3/movie/' + source
                    full_url = url + '?' + url_values
                    req = urllib2.Request(full_url)
                    infostring = urllib2.urlopen(req).read()
                    infostring = json.loads(infostring)
                    for result in infostring['results']:
                        id=result['id']
                        dict={'trailer':'tmdb','id': id,'source':'tmdb','title':result['title']}
                        tmdbTrailers.append(dict)
                    if infostring['total_pages']==page:
                        break
            return tmdbTrailers
        
        def search_tmdb(query,year):
            id=''
            data = {}
            data['api_key'] = '99e8b7beac187a857152f57d67495cf4'
            data['page']='1'
            data['query']=query
            data['language']='fr'
            url_values = urllib.urlencode(data)
            url = 'https://api.themoviedb.org/3/search/movie'
            full_url = url + '?' + url_values
            req = urllib2.Request(full_url)
            infostring = urllib2.urlopen(req).read()
            infostring = json.loads(infostring)
            results=infostring['results']
            for movie in results:
                if not movie['release_date']=='' and int(movie['release_date'][:4])>int(year)-2 and int(movie['release_date'][:4])<int(year)+2:
                    id=movie['id']
                    break
            return id    
        
        def alloba(allo):
            soup = BeautifulSoup( urllib2.urlopen(allo), "html.parser" )
            rows = soup.findAll("a")
            linkallovf=[]
            linkallovost=[]
            linkallovo=[]
            for lien in rows:
                if 'annonce' in str(lien).lower() and 'vf' in str(lien).lower():
                    lienid=lien['href'][:lien['href'].find('&')].replace('/video/player_gen_cmedia=','')
                    trailerallo = api.trailer(lienid)
                    try:
                        longueur=len(trailerallo['media']['rendition'])
                        linkallovf.append(trailerallo['media']['rendition'][longueur-1]['href'])
                        continue
                    except:
                        continue
                elif 'annonce' in str(lien).lower() and 'vost' in str(lien).lower():
                    lienid=lien['href'][:lien['href'].find('&')].replace('/video/player_gen_cmedia=','')
                    trailerallo = api.trailer(lienid)
                    try:
                        longueur=len(trailerallo['media']['rendition'])
                        linkallovost.append(trailerallo['media']['rendition'][longueur-1]['href'])
                        continue
                    except:
                        continue               
                elif 'annonce' in str(lien).lower() and ' VO' in str(lien):
                    lienid=lien['href'][:lien['href'].find('&')].replace('/video/player_gen_cmedia=','') 
                    trailerallo = api.trailer(lienid)
                    try:
                        longueur=len(trailerallo['media']['rendition'])
                        linkallo=trailerallo['media']['rendition'][longueur-1]['href']
                        if hasattr(trailerallo['media'],'subtitles') and trailerallo['media']['subtitles']['$'].lower().replace('ç','c') ==u'francais':
                            linkallovost.append(linkallo)
                            continue
                        else:
                            linkallovo.append(linkallo)
                            continue
                    except:
                        continue
                else:
                    continue
                
            if linkallovf:
                linkallo=linkallovf[0]
                return linkallo
            elif linkallovost:
                linkallo=linkallovost[0]
                return linkallo
            elif linkallovo:
                linkallo=linkallovo[0]
                return linkallo
            else:
                linkallo=''
                return linkallo
            
        def getTmdbTrailer(movieId,allo=''):
            movieIdori=movieId
            if allo<>'':
                infomovie=search_tmdb(movieId[0],movieId[1])
                if not infomovie:
                    linkallo=alloba(allo)
                    if linkallo:
                        trailer_url=linkallo
                        source='Allocine'
                        dictInfo = {'title':movieId[0],'trailer': trailer_url,'year':movieId[1],'studio':[],'mpaa':'','file':'','thumbnail':movieId[6],'fanart':movieId[5],'director':[],'writer':[],'plot':movieId[2],'cast':'','runtime':movieIdori[4],'genre':[],'source': 'Allocine','type':''} 
                    else:
                        dictInfo = {'title':'','trailer': '','year':0,'studio':[],'mpaa':'','file':'','thumbnail':'','fanart':'','director':[],'writer':[],'plot':'','cast':'','runtime':0,'genre':[],'source': 'tmdb','type':''} 
                    return dictInfo
                else:
                    movieId=infomovie
            trailer_url=''
            type=''
            you_tube_base_url='plugin://plugin.video.youtube/?action=play_video&videoid='
            image_base_url='http://image.tmdb.org/t/p/'
            data = {}
            data['append_to_response']='credits,trailers,releases'
            data['api_key'] = '99e8b7beac187a857152f57d67495cf4'
            data['language'] ='fr'
            url_values = urllib.urlencode(data)
            url = 'http://api.themoviedb.org/3/movie/' + str(movieId)
            full_url = url + '?' + url_values
            req = urllib2.Request(full_url)
            try:
                movieString = urllib2.urlopen(req).read()        
                movieString = unicode(movieString, 'utf-8', errors='ignore')
                movieString = json.loads(movieString)
            except:
                dictInfo = {'title':'','trailer': '','year':0,'studio':[],'mpaa':'','file':'','thumbnail':'','fanart':'','director':[],'writer':[],'plot':'','cast':'','runtime':0,'genre':[],'source': 'tmdb','type':''} 
            else:
                for trailer in movieString['trailers']['youtube']:
                    if 'source' in trailer:
                        trailer_url=you_tube_base_url + trailer['source']
                        type=trailer['type']
                        break
                    
                countries = movieString['releases']['countries']
                mpaa=''
                for c in countries:
                    if c['iso_3166_1'] =='US':
                        mpaa=c['certification']
                if mpaa=='':mpaa='NR'
                year=movieString['release_date'][:-6]
                fanart=image_base_url + 'w300'+str(movieString['backdrop_path'])
                thumbnail=image_base_url + 'w342'+str(movieString['poster_path'])
                title=movieString['title']                
                plot=movieString['overview']                
                runtime=movieString['runtime']
                if allo<>'':
                    year = movieIdori[3]
                    title = movieIdori[0]
                    if not plot or plot=='':
                        plot = movieIdori[2]
                    if not runtime or runtime==0:
                        runtime = movieIdori[4]
                    if 'jpg' not in thumbnail[len(thumbnail)-4:]:
                        thumbnail=movieIdori[6]
                    if 'jpg' not in fanart[len(fanart)-4:]:
                        fanart=movieIdori[5]
                studios=movieString['production_companies']
                studio=[]
                for s in studios:
                    studio.append(s['name'])
                genres=movieString['genres']
                genre=[]
                for g in genres:
                    genre.append(g['name'])
                castMembers = movieString['credits']['cast']
                cast=[]
                castcount=0
                for castMember in castMembers:
                    castcount=castcount +1
                    cast.append(castMember['name'])
                    if castcount == 6:break     
                crewMembers = movieString['credits']['crew']
                director=[]
                writer=[]
                for crewMember in crewMembers:
                    if crewMember['job'] =='Director':
                        director.append(crewMember['name'])
                    if crewMember['department']=='Writing':
                        writer.append(crewMember['name'])
                addMovie=False
                for s in movieString['spoken_languages']:
                    if s['name'] in ['English','French']:
                        addMovie=True
                if movieString['adult']=='true':addMovie = False
                source='tmdb'
                if allo<>'':
                    linkallo=alloba(allo)
                    if linkallo:
                        addMovie=True
                        trailer_url=linkallo
                        source='Allocine'
                if not addMovie:
                    dictInfo = {'title':'','trailer': '','year':0,'studio':[],'mpaa':'','file':'','thumbnail':'','fanart':'','director':[],'writer':[],'plot':'','cast':'','runtime':0,'genre':[],'source': 'tmdb','type':''} 
                else:
                    dictInfo = {'title':title,'trailer': trailer_url,'year':year,'studio':studio,'mpaa':mpaa,'file':'','thumbnail':thumbnail,'fanart':fanart,'director':director,'writer':writer,'plot':plot,'cast':cast,'runtime':runtime,'genre':genre,'source': source,'type':type} 
            return dictInfo
         
        class trailerWindow(xbmcgui.WindowXMLDialog):
        
            def onInit(self):
                windowstring = xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"GUI.GetProperties","params":{"properties":["currentwindow"]},"id":1}')
                windowstring=json.loads(windowstring)
                xbmc.log('Trailer_Window_id = ' + str(windowstring['result']['currentwindow']['id']))
                global played
                global SelectedGene
                global trailer
                global info
                global do_timeout
                global NUMBER_TRAILERS
                global trailercountF
                global source
                random.shuffle(trailers)
                
                try:
                    trailer=trailers[0]
                except:
                    NUMBER_TRAILERS = 0
                    self.close()
                if trailer['trailer'] in ['tmdb']:
                    trailer=getTmdbTrailer(trailer['id'])
                else:
                    trailer=getTmdbTrailer(trailer['id'],trailer['trailer'])
                del trailers[0]
                source=trailer['source']
                               
                lastPlay = True
                       
                url = trailer['trailer'].encode('ascii', 'ignore')
                xbmc.log(str(trailer))
                if  trailer["trailer"] != '' and lastPlay:
                    NUMBER_TRAILERS = NUMBER_TRAILERS -1
                    if hide_info == 'false':
                        w=infoWindow('script-DialogVideoInfo.xml',addon_path,'default')
                        do_timeout=True
                        w.doModal()
                        if not exit_requested:
                            xbmc.Player().play(url)
                        do_timeout=False
                        del w
                        if exit_requested:
                            xbmc.Player().play(trailer['file'])
                    else:
                        xbmc.Player().play(url)
                        NUMBER_TRAILERS = NUMBER_TRAILERS -1
                    self.getControl(30011).setLabel('[B]'+trailer["title"] + ' - ' + str(trailer["year"])+'[/B]')
                    if hide_title == 'false':
                        self.getControl(30011).setVisible(True)
                    else:
                        self.getControl(30011).setVisible(False)
                    while xbmc.Player().isPlaying():                
                        xbmc.sleep(250)
                self.close()
                
            def onAction(self, action):
                ACTION_PREVIOUS_MENU = 10
                ACTION_BACK = 92
                ACTION_ENTER = 7
                ACTION_I = 11
                ACTION_LEFT = 1
                ACTION_RIGHT = 2
                ACTION_UP = 3
                ACTION_DOWN = 4
                ACTION_TAB = 18
                ACTION_M = 122
                ACTION_Q=34
                ACTION_STOP = 13
                
                global exit_requested
                global movie_file
                global source
                global trailer
                movie_file=''
                xbmc.log(str(action.getId()))
                if action == ACTION_Q:
                    strCouchPotato='plugin://plugin.video.couchpotato_manager/movies/add?title='+trailer['title']
                    xbmc.executebuiltin('XBMC.RunPlugin('+strCouchPotato+')')
                
                if action == ACTION_PREVIOUS_MENU or action == ACTION_LEFT or action == ACTION_BACK or action == ACTION_STOP:
                    xbmc.Player().stop()
                    exit_requested = True
                    self.close()
        
                if action == ACTION_RIGHT or action == ACTION_TAB:
                    xbmc.Player().stop()
                                    
                if action == ACTION_M:
                    self.getControl(30011).setVisible(True)
                    xbmc.sleep(2000)
                    self.getControl(30011).setVisible(False)
                
                if action == ACTION_I or action == ACTION_UP:
                    if source !='folder':
                        self.getControl(30011).setVisible(False)
                        w=infoWindow('script-DialogVideoInfo.xml',addon_path,'default')
                        w.doModal()
                    if hide_title == 'false':
                        self.getControl(30011).setVisible(True)
                    else:
                        self.getControl(30011).setVisible(False)
                                      
        class infoWindow(xbmcgui.WindowXMLDialog):
            def onInit(self):
                source = trailer['source']
                try:
                    trailername=trailer['title'].encode('utf-8')
                except:
                    try:
                        trailername=trailer['title'].encode('latin-1')
                    except:
                        trailername=trailer['title']
                info=getInfo(trailername,trailer['year'])
                self.getControl(30001).setImage(trailer["thumbnail"])
                self.getControl(30003).setImage(trailer["fanart"])
                title_font=getTitleFont()
                title_string =trailer["title"] + ' - ' + trailer['source'] + ' - ' + str(trailer["year"])
                title=xbmcgui.ControlLabel(10,40,800,40,title_string,title_font)
                title=self.addControl(title)
                title=self.getControl(3001)
                title.setAnimations([('windowclose', 'effect=fade end=0 time=1000')])          
                movieDirector=''
                movieWriter=''
                if source=='iTunes':
                    writers = info['writer']
                    directors = info['director']
                    actors = info['cast']
                    plot = info['plot']
                    movieActor=''
                    actorcount=0        
                    for actor in actors:
                        actorcount=actorcount+1
                        movieActor = movieActor + actor + ", "
                        if actorcount == 6: break
                    if not movieActor == '':
                        movieActor = movieActor[:-2]    
                else:
                    plot=trailer["plot"]
                    writers = trailer["writer"]
                    directors = trailer["director"]
                    actors = trailer["cast"]
                    movieActor=''
                    actorcount=0
                    if source=='library':
                        for actor in actors:
                            actorcount=actorcount+1
                            movieActor = movieActor + actor['name'] + ", "
                            if actorcount == 6: break
                        if not movieActor == '':
                            movieActor = movieActor[:-2] 
                    else:
                        movieActor=''
                        actorcount=0        
                        for actor in actors:
                            actorcount=actorcount+1
                            movieActor = movieActor + actor + ", "
                            if actorcount == 6: break
                        if not movieActor == '':
                            movieActor = movieActor[:-2]    
                for director in directors:
                    movieDirector = movieDirector + director + ", "
                if not movieDirector =='':
                    movieDirector = movieDirector[:-2]
                for writer in writers:
                    movieWriter = movieWriter + writer + ", "
                if not movieWriter =='':
                    movieWriter = movieWriter[:-2]                
                self.getControl(30005).setLabel(movieDirector)
                self.getControl(30006).setLabel(movieActor)
                self.getControl(30005).setLabel(movieDirector)
                self.getControl(30007).setLabel(movieWriter)
                self.getControl(30009).setText(plot)
                movieStudio=''
                if source == 'iTunes':
                    studios=trailer["studio"]        
                    movieStudio=studios
                if source =='library' or source == 'tmdb':
                    studios=trailer["studio"]
                    for studio in studios:
                        movieStudio = movieStudio + studio + ", "
                        if not movieStudio =='':
                            movieStudio = movieStudio[:-2]
                self.getControl(30010).setLabel(movieStudio)
                movieGenre=''
                genres = trailer["genre"]
                for genre in genres:
                    movieGenre = movieGenre + genre + " / "
                if not movieGenre =='':
                    movieGenre = movieGenre[:-3]
                runtime=str(trailer["runtime"])
                if source == 'iTunes':runtime=''
                if source == 'library':runtime=str(trailer["runtime"] / 60)
                
                if runtime != '':runtime=runtime + ' Minutes - '
                self.getControl(30011).setLabel(runtime + movieGenre)
                imgRating='ratings/notrated.png'
                if trailer["mpaa"].startswith('G'): imgRating='ratings/g.png'
                if trailer["mpaa"] == ('G'): imgRating='ratings/g.png'
                if trailer["mpaa"].startswith('Rated G'): imgRating='ratings/g.png'
                if trailer["mpaa"].startswith('PG '): imgRating='ratings/pg.png'
                if trailer["mpaa"] == ('PG'): imgRating='ratings/pg.png'
                if trailer["mpaa"].startswith('Rated PG'): imgRating='ratings/pg.png'
                if trailer["mpaa"].startswith('PG-13 '): imgRating='ratings/pg13.png'
                if trailer["mpaa"] == ('PG-13'): imgRating='ratings/pg13.png'
                if trailer["mpaa"].startswith('Rated PG-13'): imgRating='ratings/pg13.png'
                if trailer["mpaa"].startswith('R '): imgRating='ratings/r.png'
                if trailer["mpaa"] == ('R'): imgRating='ratings/r.png'
                if trailer["mpaa"].startswith('Rated R'): imgRating='ratings/r.png'
                if trailer["mpaa"].startswith('NC17'): imgRating='ratings/nc17.png'
                if trailer["mpaa"].startswith('Rated NC17'): imgRating='ratings/nc1.png'
                self.getControl(30013).setImage(imgRating)
                if do_timeout:
                    xbmc.sleep(5000)
                    self.close()
                
            def onAction(self, action):
                ACTION_PREVIOUS_MENU = 10
                ACTION_BACK = 92
                ACTION_ENTER = 7
                ACTION_I = 11
                ACTION_LEFT = 1
                ACTION_RIGHT = 2
                ACTION_UP = 3
                ACTION_DOWN = 4
                ACTION_TAB = 18
                ACTION_Q = 34
                ACTION_STOP=13
                
                global do_timeout
                global exit_requested
                global trailer
                global movie_file
                movie_file=''
                
                if action == ACTION_PREVIOUS_MENU or action == ACTION_LEFT or action == ACTION_BACK or ACTION_STOP:
                    do_timeout=False
                    xbmc.Player().stop()
                    exit_requested=True
                    self.close()
                
                if action == ACTION_Q:
                    strCouchPotato='plugin://plugin.video.couchpotato_manager/movies/add?title='+trailer['title']
                    xbmc.executebuiltin('XBMC.RunPlugin('+strCouchPotato+')') 
                    
                if action == ACTION_I or action == ACTION_DOWN:
                    self.close()
                    
                if action == ACTION_RIGHT or action == ACTION_TAB:
                    xbmc.Player().stop()
                    self.close()
                                                            
        def playTrailers():
            global exit_requested
            global movie_file
            global NUMBER_TRAILERS
            global trailercount
            movie_file = ''
            exit_requested = False
            DO_CURTIANS = addon.getSetting('do_animation_sug')
            NUMBER_TRAILERS =  int(addon.getSetting('number_trailers_sug'))
            trailercount = 0
            while not exit_requested:
                if NUMBER_TRAILERS == 0:
                    while not exit_requested and not xbmc.abortRequested:
                        mytrailerWindow = trailerWindow('script-trailerwindow.xml', addon_path,'default',)
                        mytrailerWindow.doModal()
                        del mytrailerWindow
                                        
                else:
                    while NUMBER_TRAILERS > 0:
                        mytrailerWindow = trailerWindow('script-trailerwindow.xml', addon_path,'default',)
                        mytrailerWindow.doModal()
                        del mytrailerWindow
                        if exit_requested:
                            break
                if not exit_requested:
                    if DO_CURTIANS == 'true':
                        xbmc.Player().play(close_curtain_path)
                        while xbmc.Player().isPlaying():
                            xbmc.sleep(250)
                exit_requested=True
        
        def check_for_xsqueeze():
            KEYMAPDESTFILE = os.path.join(xbmc.translatePath('special://userdata/keymaps'), "xsqueeze.xml")
            if os.path.isfile(KEYMAPDESTFILE):
                return True
            else:
                return False
        
        def get_mpaa(trailer):
            Rating='NR'
            if trailer["mpaa"].startswith('G'): Rating='G'
            if trailer["mpaa"] == ('G'): Rating='G'
            if trailer["mpaa"].startswith('Rated G'): Rating='G'
            if trailer["mpaa"].startswith('PG '): Rating='PG'
            if trailer["mpaa"] == ('PG'): Rating='PG'
            if trailer["mpaa"].startswith('Rated PG'): Rating='PG'
            if trailer["mpaa"].startswith('PG-13 '): Rating='PG-13'
            if trailer["mpaa"] == ('PG-13'): Rating='PG-13'
            if trailer["mpaa"].startswith('Rated PG-13'): Rating='PG-13'
            if trailer["mpaa"].startswith('R '): Rating='R'
            if trailer["mpaa"] == ('R'): Rating='R'
            if trailer["mpaa"].startswith('Rated R'): Rating='R'
            if trailer["mpaa"].startswith('NC17'): Rating='NC17'
            if trailer["mpaa"].startswith('Rated NC17'): 'NC17'
            return Rating
        
        def getallocinetrailer(typev):
            movielist=api.movielist(typev)
            return movielist
        
        if not xbmc.Player().isPlaying() and not check_for_xsqueeze():
            DO_CURTIANS = addon.getSetting('do_animation_sug')
            if DO_CURTIANS == 'true':
                xbmc.Player().play(open_curtain_path)
                while xbmc.Player().isPlaying():
                    xbmc.sleep(250)
            trailers = []
            filtergenre = False
            trailerNumber = 0
            library_trailers=[]
            iTunes_trailers=[]
            folder_trailers=[]
            tmdb_trailers=''
            choice='conf'
            if addon.getSetting("tmdb_source") == '6':
                success = False
                selected = ""
                # sort the list alphabetically        
                mychoice = [addon.getLocalizedString(32051),
                            addon.getLocalizedString(32050),
                            addon.getLocalizedString(32049),
                            addon.getLocalizedString(32052),
                            addon.getLocalizedString(32047),
                            addon.getLocalizedString(32048)]
                # prompt user to select genre
                selectChoice = xbmcgui.Dialog().select(u"Type de bandes annnonces", mychoice)
                if selectChoice==4:
                    choice='popular'
                elif selectChoice==5:
                    choice='top_rated'
                elif selectChoice==2:
                    choice='upcoming'
                elif selectChoice==1:
                    choice='now_playing'
                elif selectChoice==0:
                    choice='all'
                elif selectChoice==3:
                    choice='dvd'   
                else:
                    choice='none'        
            dp=xbmcgui.DialogProgress()
            dp.create('Suggestions','','','Chargement des bande-annonces')
            tmdbTrailers=getTmdbTrailers(choice)
            for trailer in tmdbTrailers:
                trailers.append(trailer)    
            exit_requested=False
            if dp.iscanceled():exit_requested=True 
            dp.close()
            if len(trailers) > 0 and not exit_requested:
                playTrailers()
            del bs
                    
        else:
            xbmc.log('Random Trailers: ' + 'Exiting Random Trailers Screen Saver Something is playing!!!!!!')
    
    elif choix==4:
        # Search trailer player
        import xbmc
        import xbmcvfs
        import xbmcgui
        from urllib import quote_plus, unquote_plus
        import datetime
        import urllib
        import urllib2
        import re
        import sys
        import os
        import random
        import json
        import time
        import xbmcaddon
        import unicodedata
        from bs4 import BeautifulSoup
        import xml.dom.minidom
        from xml.dom.minidom import Node
        from allocine import allocine
        api = allocine()
        api.configure('100043982026','29d185d98c984a359e6e6f26a0474269')
        addon = xbmcaddon.Addon()
        do_curtains = 'false'
        hide_info = addon.getSetting('hide_info_search')
        hide_title = addon.getSetting('hide_title_search')
        addon_path = addon.getAddonInfo('path')
        resources_path = xbmc.translatePath( os.path.join( addon_path, 'resources' ) ).decode('utf-8')
        media_path = xbmc.translatePath( os.path.join( resources_path, 'media' ) ).decode('utf-8')
        open_curtain_path = xbmc.translatePath( os.path.join( media_path, 'OpenSequence.mp4' ) ).decode('utf-8')
        close_curtain_path = xbmc.translatePath( os.path.join( media_path, 'ClosingSequence.mp4' ) ).decode('utf-8')
        exit_requested = False
        movie_file = ''
        opener = urllib2.build_opener()
        
        if len(sys.argv) == 2:
            do_genre ='false'
        
        trailer=''
        info=''
        do_timeout = False
        played = []
        
        def getTitleFont():
            title_font='font13'
            base_size=20
            multiplier=1
            skin_dir = xbmc.translatePath("special://skin/")
            list_dir = os.listdir( skin_dir )
            fonts=[]
            fontxml_path =''
            font_xml=''
            for item in list_dir:
                item = os.path.join( skin_dir, item )
                if os.path.isdir( item ):
                    font_xml = os.path.join( item, "Font.xml" )
                if os.path.exists( font_xml ):
                    fontxml_path=font_xml
                    break
            dom =  xml.dom.minidom.parse(fontxml_path)
            fontlist=dom.getElementsByTagName('font')
            for font in fontlist:
                name = font.getElementsByTagName('name')[0].childNodes[0].nodeValue
                size = font.getElementsByTagName('size')[0].childNodes[0].nodeValue
                fonts.append({'name':name,'size':float(size)})
            fonts =sorted(fonts, key=lambda k: k['size'])
            for f in fonts:
                if f['name']=='font13':
                    multiplier=f['size'] / 20
                    break
            for f in fonts:
                if f['size'] >= 38 * multiplier:
                    title_font=f['name']
                    break
            return title_font
        
        def getInfo(title,year):
            data = {}
            data['query'] = title
            data['year'] = str(year)
            data['api_key'] = '99e8b7beac187a857152f57d67495cf4'
            data['language'] ='fr'
            url_values = urllib.urlencode(data)
            url = 'https://api.themoviedb.org/3/search/movie'
            full_url = url + '?' + url_values
            req = urllib2.Request(full_url)
            infostring = urllib2.urlopen(req).read()
            infostring = json.loads(infostring)
            if len(infostring['results']) > 0:
                results=infostring['results'][0]
                movieId=str(results['id'])
                if not movieId == '':
                    data = {}
                    data['api_key'] = '99e8b7beac187a857152f57d67495cf4'
                    data['append_to_response'] ='credits'
                    url_values = urllib.urlencode(data)
                    url = 'https://api.themoviedb.org/3/movie/' + movieId
                    full_url = url + '?' + url_values
                    req = urllib2.Request(full_url)
                    infostring = urllib2.urlopen(req).read()
                    infostring = json.loads(infostring)
                    director=[]
                    writer=[]
                    cast=[]
                    plot=''
                    runtime=''
                    genre=[]
                    plot=infostring['overview']
                    runtime=infostring['runtime']
                    genres=infostring['genres']
                    for g in genres:
                        genre.append(g['name'])
                    castMembers = infostring['credits']['cast']
                    castcount=0
                    for castMember in castMembers:
                        castcount = castcount + 1
                        cast.append(castMember['name'])     
                        if castcount == 6:break
                    crewMembers = infostring['credits']['crew']
                    for crewMember in crewMembers:
                        if crewMember['job'] =='Director':
                            director.append(crewMember['name'])
                        if crewMember['department']=='Writing':
                            writer.append(crewMember['name'])
            else:
                director=['Unavailable']
                writer=['Unavailable']
                cast=['Unavailable']
                plot='Unavailable'
                runtime=0
                genre=['Unavailable']
            dictInfo = {'director':director,'writer':writer,'plot':plot,'cast':cast,'runtime':runtime,'genre':genre}
            return dictInfo
              
        def getTmdbTrailers(choice):
            tmdbTrailers=[]
            if choice=='conf':
                if addon.getSetting("tmdb_source") == '0':source='popular'
                if addon.getSetting("tmdb_source") == '1':source='top_rated'
                if addon.getSetting("tmdb_source") == '2':source='upcoming'
                if addon.getSetting("tmdb_source") == '3':source='now_playing'
                if addon.getSetting("tmdb_source") == '4':source='dvd'
                if addon.getSetting("tmdb_source") == '5':source='all'
            elif choice=='none':
                source='all'
            else:
                source=choice
            
            if source=='all':
                data = {}
                data['api_key'] = '99e8b7beac187a857152f57d67495cf4'
                data['sort_by'] ='popularity.desc'
                data['language'] ='fr'
                url_values = urllib.urlencode(data)
                url = 'http://api.themoviedb.org/3/discover/movie'
                full_url = url + '?' + url_values
                req = urllib2.Request(full_url)
                infostring = urllib2.urlopen(req).read()
                infostring = json.loads(infostring)
                total_pages=infostring['total_pages']
                if total_pages > 1000: total_pages=1000
                for i in range(1,11):
                    data = {}
                    data['api_key'] = '99e8b7beac187a857152f57d67495cf4'
                    data['sort_by'] ='popularity.desc'
                    data['language'] ='fr'
                    data['page']=random.randrange(1,total_pages+1)
                    url_values = urllib.urlencode(data)
                    url = 'http://api.themoviedb.org/3/discover/movie'
                    full_url = url + '?' + url_values
                    req = urllib2.Request(full_url)
                    infostring = urllib2.urlopen(req).read()
                    infostring = json.loads(infostring)
                    for movie in infostring['results']:
                        id=movie['id']
                        dict={'trailer':'tmdb','id': id,'source':'tmdb','title':movie['title']}
                        tmdbTrailers.append(dict)
        
            elif source=='dvd':
                data={}
                data['apikey']='99dgtphe3c29y85m2g8dmdmt'
                data['country'] = 'us'
                url_values = urllib.urlencode(data)
                url = 'http://api.rottentomatoes.com/api/public/v1.0/lists/dvds/new_releases.json'
                full_url = url + '?' + url_values
                req = urllib2.Request(full_url)
                response = urllib2.urlopen(req).read()
                infostring = json.loads(response)
                for movie in infostring['movies']:
                    data={}
                    data['api_key']='99e8b7beac187a857152f57d67495cf4'
                    data['query']=movie['title']
                    data['year']=movie['year']
                    url_values = urllib.urlencode(data)
                    url = 'https://api.themoviedb.org/3/search/movie'
                    full_url = url + '?' + url_values
                    req = urllib2.Request(full_url)
                    infostring = urllib2.urlopen(req).read()
                    infostring = json.loads(infostring)
                    for m in infostring['results']:
                        id=m['id']
                        dict={'trailer':'tmdb','id': id,'source':'tmdb','title':movie['title']}
                        tmdbTrailers.append(dict)
                        break
            
            elif source=='upcoming':
                movies=getallocinetrailer('comingsoon')
                for movie in movies['feed']['movie']:
                        title=movie['title']
                        try:
                            year=movie['productionYear']
                        except:
                            year=''
                        try:
                            plot=movie['synopsisShort'].encode("utf-8").replace('<p>','').replace('</p>','')
                        except:
                            plot=''
                        try:
                            releasedate=movie['release']['releaseDate']
                            if len(releasedate)>=4:
                                if len(releasedate)>=7:
                                    releasedate=releasedate[8:10]+'/'+releasedate[5:7]+'/'+releasedate[0:4]
                                else:releasedate=releasedate[5:7]+'/'+releasedate[0:4]
                                                                
                        except:
                            releasedate=year
                        try:
                            runtime=str(int(movie['runtime'])/60)
                        except:
                            runtime=''
                        try:
                            thumbs=movie['defaultMedia']['media']['thumbnail']['href']
                        except:
                            thumbs=''
                        try:
                            poster=movie['poster']['href']
                        except:
                            poster=''
                        
                        pagetrailer=''
                        for x in movie['link']:
                            if x.has_key('name') and 'Bandes annonces' in x['name']:
                                pagetrailer=x['href']
                            else:
                                continue
                            title=title.encode("utf-8")
                            dict={'trailer':pagetrailer,'id': [title,year,plot,releasedate,runtime,thumbs,poster],'source':'allo','title':movie['title']}
                            tmdbTrailers.append(dict)
            
            elif source=='now_playing':
                movies=getallocinetrailer('nowshowing')
                for movie in movies['feed']['movie']:
                        title=movie['title']
                        try:
                            year=movie['productionYear']
                        except:
                            year=''
                        try:
                            plot=movie['synopsisShort'].encode("utf-8").replace('<p>','').replace('</p>','')
                        except:
                            plot=''
                        try:
                            releasedate=movie['release']['releaseDate']
                            if len(releasedate)>=4:
                                if len(releasedate)>=7:
                                    releasedate=releasedate[8:10]+'/'+releasedate[5:7]+'/'+releasedate[0:4]
                                else:releasedate=releasedate[5:7]+'/'+releasedate[0:4]
                                                                
                        except:
                            releasedate=year
                        try:
                            runtime=str(int(movie['runtime'])/60)
                        except:
                            runtime=''
                        try:
                            thumbs=movie['defaultMedia']['media']['thumbnail']['href']
                        except:
                            thumbs=''
                        try:
                            poster=movie['poster']['href']
                        except:
                            poster=''
                        pagetrailer=''
                        for x in movie['link']:
                            if x.has_key('name') and 'Bandes annonces' in x['name']:
                                pagetrailer=x['href']
                            else:
                                continue
                            title=title.encode("utf-8")
                            print str(movie)
                            dict={'trailer':pagetrailer,'id': [title,year,plot,releasedate,runtime,thumbs,poster],'source':'allo','title':movie['title']}
                            tmdbTrailers.append(dict)
            
            else:
                page=0
                for i in range(0,11):
                    page=page+1
                    data = {}
                    data['api_key'] = '99e8b7beac187a857152f57d67495cf4'
                    data['page'] = page
                    data['language']='fr'
                    data['sort_by'] ='popularity.desc'
                    url_values = urllib.urlencode(data)
                    url = 'https://api.themoviedb.org/3/movie/' + source
                    full_url = url + '?' + url_values
                    req = urllib2.Request(full_url)
                    infostring = urllib2.urlopen(req).read()
                    infostring = json.loads(infostring)
                    for result in infostring['results']:
                        id=result['id']
                        dict={'trailer':'tmdb','id': id,'source':'tmdb','title':result['title']}
                        tmdbTrailers.append(dict)
                    if infostring['total_pages']==page:
                        break
            return tmdbTrailers
        
        def search_tmdb(query,year):
            id=''
            data = {}
            data['api_key'] = '99e8b7beac187a857152f57d67495cf4'
            data['page']='1'
            data['query']=query
            data['language']='fr'
            url_values = urllib.urlencode(data)
            url = 'https://api.themoviedb.org/3/search/movie'
            full_url = url + '?' + url_values
            req = urllib2.Request(full_url)
            infostring = urllib2.urlopen(req).read()
            infostring = json.loads(infostring)
            results=infostring['results']
            for movie in results:
                if not movie['release_date']=='' and int(movie['release_date'][:4])>int(year)-2 and int(movie['release_date'][:4])<int(year)+2:
                    id=movie['id']
                    break
            return id    
        
        def alloba(allo):
            soup = BeautifulSoup( urllib2.urlopen(allo), "html.parser" )
            rows = soup.findAll("a")
            linkallovf=[]
            linkallovost=[]
            linkallovo=[]
            for lien in rows:
                if 'annonce' in str(lien).lower() and 'vf' in str(lien).lower():
                    lienid=lien['href'][:lien['href'].find('&')].replace('/video/player_gen_cmedia=','')
                    trailerallo = api.trailer(lienid)
                    try:
                        longueur=len(trailerallo['media']['rendition'])
                        linkallovf.append(trailerallo['media']['rendition'][longueur-1]['href'])
                        continue
                    except:
                        continue
                elif 'annonce' in str(lien).lower() and 'vost' in str(lien).lower():
                    lienid=lien['href'][:lien['href'].find('&')].replace('/video/player_gen_cmedia=','')
                    trailerallo = api.trailer(lienid)
                    try:
                        longueur=len(trailerallo['media']['rendition'])
                        linkallovost.append(trailerallo['media']['rendition'][longueur-1]['href'])
                        continue
                    except:
                        continue               
                elif 'annonce' in str(lien).lower() and ' VO' in str(lien):
                    lienid=lien['href'][:lien['href'].find('&')].replace('/video/player_gen_cmedia=','') 
                    trailerallo = api.trailer(lienid)
                    try:
                        longueur=len(trailerallo['media']['rendition'])
                        linkallo=trailerallo['media']['rendition'][longueur-1]['href']
                        if hasattr(trailerallo['media'],'subtitles') and trailerallo['media']['subtitles']['$'].lower().replace('ç','c') ==u'francais':
                            linkallovost.append(linkallo)
                            continue
                        else:
                            linkallovo.append(linkallo)
                            continue
                    except:
                        continue
                else:
                    continue
                
            if linkallovf:
                linkallo=linkallovf[0]
                return linkallo
            elif linkallovost:
                linkallo=linkallovost[0]
                return linkallo
            elif linkallovo:
                linkallo=linkallovo[0]
                return linkallo
            else:
                linkallo=''
                return linkallo
            
        def getTmdbTrailer(movieId,allo=''):
            movieIdori=movieId
            if allo<>'':
                infomovie=search_tmdb(movieId[0],movieId[1])
                if not infomovie:
                    linkallo=alloba(allo)
                    if linkallo:
                        trailer_url=linkallo
                        source='Allocine'
                        dictInfo = {'title':movieId[0],'trailer': trailer_url,'year':movieId[1],'studio':[],'mpaa':'','file':'','thumbnail':movieId[6],'fanart':movieId[5],'director':[],'writer':[],'plot':movieId[2],'cast':'','runtime':movieIdori[4],'genre':[],'source': 'Allocine','type':''} 
                    else:
                        dictInfo = {'title':'','trailer': '','year':0,'studio':[],'mpaa':'','file':'','thumbnail':'','fanart':'','director':[],'writer':[],'plot':'','cast':'','runtime':0,'genre':[],'source': 'tmdb','type':''} 
                    return dictInfo
                else:
                    movieId=infomovie
            trailer_url=''
            type=''
            you_tube_base_url='plugin://plugin.video.youtube/?action=play_video&videoid='
            image_base_url='http://image.tmdb.org/t/p/'
            data = {}
            data['append_to_response']='credits,trailers,releases'
            data['api_key'] = '99e8b7beac187a857152f57d67495cf4'
            data['language'] ='fr'
            url_values = urllib.urlencode(data)
            url = 'http://api.themoviedb.org/3/movie/' + str(movieId)
            full_url = url + '?' + url_values
            req = urllib2.Request(full_url)
            try:
                movieString = urllib2.urlopen(req).read()        
                movieString = unicode(movieString, 'utf-8', errors='ignore')
                movieString = json.loads(movieString)
            except:
                dictInfo = {'title':'','trailer': '','year':0,'studio':[],'mpaa':'','file':'','thumbnail':'','fanart':'','director':[],'writer':[],'plot':'','cast':'','runtime':0,'genre':[],'source': 'tmdb','type':''} 
            else:
                for trailer in movieString['trailers']['youtube']:
                    if 'source' in trailer:
                        trailer_url=you_tube_base_url + trailer['source']
                        type=trailer['type']
                        break
                    
                countries = movieString['releases']['countries']
                mpaa=''
                for c in countries:
                    if c['iso_3166_1'] =='US':
                        mpaa=c['certification']
                if mpaa=='':mpaa='NR'
                year=movieString['release_date'][:-6]
                fanart=image_base_url + 'w300'+str(movieString['backdrop_path'])
                thumbnail=image_base_url + 'w342'+str(movieString['poster_path'])
                title=movieString['title']                
                plot=movieString['overview']                
                runtime=movieString['runtime']
                if allo<>'':
                    year = movieIdori[3]
                    title = movieIdori[0]
                    if not plot or plot=='':
                        plot = movieIdori[2]
                    if not runtime or runtime==0:
                        runtime = movieIdori[4]
                    if 'jpg' not in thumbnail[len(thumbnail)-4:]:
                        thumbnail=movieIdori[6]
                    if 'jpg' not in fanart[len(fanart)-4:]:
                        fanart=movieIdori[5]
                studios=movieString['production_companies']
                studio=[]
                for s in studios:
                    studio.append(s['name'])
                genres=movieString['genres']
                genre=[]
                for g in genres:
                    genre.append(g['name'])
                castMembers = movieString['credits']['cast']
                cast=[]
                castcount=0
                for castMember in castMembers:
                    castcount=castcount +1
                    cast.append(castMember['name'])
                    if castcount == 6:break     
                crewMembers = movieString['credits']['crew']
                director=[]
                writer=[]
                for crewMember in crewMembers:
                    if crewMember['job'] =='Director':
                        director.append(crewMember['name'])
                    if crewMember['department']=='Writing':
                        writer.append(crewMember['name'])
                addMovie=False
                for s in movieString['spoken_languages']:
                    if s['name'] in ['English','French']:
                        addMovie=True
                if movieString['adult']=='true':addMovie = False
                source='tmdb'
                if allo<>'':
                    linkallo=alloba(allo)
                    if linkallo:
                        addMovie=True
                        trailer_url=linkallo
                        source='Allocine'
                if not addMovie:
                    dictInfo = {'title':'','trailer': '','year':0,'studio':[],'mpaa':'','file':'','thumbnail':'','fanart':'','director':[],'writer':[],'plot':'','cast':'','runtime':0,'genre':[],'source': 'tmdb','type':''} 
                else:
                    dictInfo = {'title':title,'trailer': trailer_url,'year':year,'studio':studio,'mpaa':mpaa,'file':'','thumbnail':thumbnail,'fanart':fanart,'director':director,'writer':writer,'plot':plot,'cast':cast,'runtime':runtime,'genre':genre,'source': source,'type':type} 
            return dictInfo
         
        class trailerWindow(xbmcgui.WindowXMLDialog):
        
            def onInit(self):
                windowstring = xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"GUI.GetProperties","params":{"properties":["currentwindow"]},"id":1}')
                windowstring=json.loads(windowstring)
                xbmc.log('Trailer_Window_id = ' + str(windowstring['result']['currentwindow']['id']))
                global played
                global SelectedGene
                global trailer
                global info
                global do_timeout
                global NUMBER_TRAILERS
                global trailercountF
                global source
                random.shuffle(trailers)
                
                trailer=trailers[0]
                
                trailerori=trailer
                trailer=getTmdbTrailer(trailer['id'],trailer['trailer'])
                del trailers[0]
                source=trailer['source']
                               
                lastPlay = True
                       
                url = trailer['trailer'].encode('ascii', 'ignore')
                xbmc.log(str(trailer))
                if  trailer["trailer"] != '' and lastPlay:
                    if hide_info == 'false':
                        w=infoWindow('script-DialogVideoInfo.xml',addon_path,'default')
                        do_timeout=True
                        w.doModal()
                        if not exit_requested:
                            xbmc.Player().play(url)
                        do_timeout=False
                        del w
                        if exit_requested:
                            xbmc.Player().play(trailer['file'])
                    else:
                        xbmc.Player().play(url)
                    self.getControl(30011).setLabel('[B]'+trailer["title"] + ' - ' + str(trailer["year"])+'[/B]')
                    if hide_title == 'false':
                        self.getControl(30011).setVisible(True)
                    else:
                        self.getControl(30011).setVisible(False)
                    while xbmc.Player().isPlaying():                
                        xbmc.sleep(250)
                else:
                    xbmcgui.Dialog().notification(u'Aucune bande-annonce', trailerori['title'], xbmcgui.NOTIFICATION_INFO, 5000)
                self.close()
                
            def onAction(self, action):
                ACTION_PREVIOUS_MENU = 10
                ACTION_BACK = 92
                ACTION_ENTER = 7
                ACTION_I = 11
                ACTION_LEFT = 1
                ACTION_RIGHT = 2
                ACTION_UP = 3
                ACTION_DOWN = 4
                ACTION_TAB = 18
                ACTION_M = 122
                ACTION_Q=34
                ACTION_STOP=13
                
                global exit_requested
                global movie_file
                global source
                global trailer
                movie_file=''
                xbmc.log(str(action.getId()))
                if action == ACTION_Q:
                    strCouchPotato='plugin://plugin.video.couchpotato_manager/movies/add?title='+trailer['title']
                    xbmc.executebuiltin('XBMC.RunPlugin('+strCouchPotato+')')
                
                if action == ACTION_PREVIOUS_MENU or action == ACTION_LEFT or action == ACTION_BACK or action==ACTION_STOP:
                    xbmc.Player().stop()
                    exit_requested = True
                    self.close()
        
                if action == ACTION_RIGHT or action == ACTION_TAB:
                    xbmc.Player().stop()
                 
                if action == ACTION_M:
                    self.getControl(30011).setVisible(True)
                    xbmc.sleep(2000)
                    self.getControl(30011).setVisible(False)
                
                if action == ACTION_I or action == ACTION_UP:
                    if source !='folder':
                        self.getControl(30011).setVisible(False)
                        w=infoWindow('script-DialogVideoInfo.xml',addon_path,'default')
                        w.doModal()
                    if hide_title == 'false':
                        self.getControl(30011).setVisible(True)
                    else:
                        self.getControl(30011).setVisible(False)
                                      
        class infoWindow(xbmcgui.WindowXMLDialog):
            def onInit(self):
                source = trailer['source']
                try:
                    trailername=trailer['title'].encode('utf-8')
                except:
                    try:
                        trailername=trailer['title'].encode('latin-1')
                    except:
                        trailername=trailer['title']
                info=getInfo(trailername,trailer['year'])
                self.getControl(30001).setImage(trailer["thumbnail"])
                self.getControl(30003).setImage(trailer["fanart"])
                title_font=getTitleFont()
                title_string =trailer["title"] + ' - ' + trailer['source'] + ' - ' + str(trailer["year"])
                title=xbmcgui.ControlLabel(10,40,800,40,title_string,title_font)
                title=self.addControl(title)
                title=self.getControl(3001)
                title.setAnimations([('windowclose', 'effect=fade end=0 time=1000')])          
                movieDirector=''
                movieWriter=''
                if source=='iTunes':
                    writers = info['writer']
                    directors = info['director']
                    actors = info['cast']
                    plot = info['plot']
                    movieActor=''
                    actorcount=0        
                    for actor in actors:
                        actorcount=actorcount+1
                        movieActor = movieActor + actor + ", "
                        if actorcount == 6: break
                    if not movieActor == '':
                        movieActor = movieActor[:-2]    
                else:
                    plot=trailer["plot"]
                    writers = trailer["writer"]
                    directors = trailer["director"]
                    actors = trailer["cast"]
                    movieActor=''
                    actorcount=0
                    if source=='library':
                        for actor in actors:
                            actorcount=actorcount+1
                            movieActor = movieActor + actor['name'] + ", "
                            if actorcount == 6: break
                        if not movieActor == '':
                            movieActor = movieActor[:-2] 
                    else:
                        movieActor=''
                        actorcount=0        
                        for actor in actors:
                            actorcount=actorcount+1
                            movieActor = movieActor + actor + ", "
                            if actorcount == 6: break
                        if not movieActor == '':
                            movieActor = movieActor[:-2]    
                for director in directors:
                    movieDirector = movieDirector + director + ", "
                if not movieDirector =='':
                    movieDirector = movieDirector[:-2]
                for writer in writers:
                    movieWriter = movieWriter + writer + ", "
                if not movieWriter =='':
                    movieWriter = movieWriter[:-2]                
                self.getControl(30005).setLabel(movieDirector)
                self.getControl(30006).setLabel(movieActor)
                self.getControl(30005).setLabel(movieDirector)
                self.getControl(30007).setLabel(movieWriter)
                self.getControl(30009).setText(plot)
                movieStudio=''
                if source == 'iTunes':
                    studios=trailer["studio"]        
                    movieStudio=studios
                if source =='library' or source == 'tmdb':
                    studios=trailer["studio"]
                    for studio in studios:
                        movieStudio = movieStudio + studio + ", "
                        if not movieStudio =='':
                            movieStudio = movieStudio[:-2]
                self.getControl(30010).setLabel(movieStudio)
                movieGenre=''
                genres = trailer["genre"]
                for genre in genres:
                    movieGenre = movieGenre + genre + " / "
                if not movieGenre =='':
                    movieGenre = movieGenre[:-3]
                runtime=str(trailer["runtime"])
                if source == 'iTunes':runtime=''
                if source == 'library':runtime=str(trailer["runtime"] / 60)
                
                if runtime != '':runtime=runtime + ' Minutes - '
                self.getControl(30011).setLabel(runtime + movieGenre)
                imgRating='ratings/notrated.png'
                if trailer["mpaa"].startswith('G'): imgRating='ratings/g.png'
                if trailer["mpaa"] == ('G'): imgRating='ratings/g.png'
                if trailer["mpaa"].startswith('Rated G'): imgRating='ratings/g.png'
                if trailer["mpaa"].startswith('PG '): imgRating='ratings/pg.png'
                if trailer["mpaa"] == ('PG'): imgRating='ratings/pg.png'
                if trailer["mpaa"].startswith('Rated PG'): imgRating='ratings/pg.png'
                if trailer["mpaa"].startswith('PG-13 '): imgRating='ratings/pg13.png'
                if trailer["mpaa"] == ('PG-13'): imgRating='ratings/pg13.png'
                if trailer["mpaa"].startswith('Rated PG-13'): imgRating='ratings/pg13.png'
                if trailer["mpaa"].startswith('R '): imgRating='ratings/r.png'
                if trailer["mpaa"] == ('R'): imgRating='ratings/r.png'
                if trailer["mpaa"].startswith('Rated R'): imgRating='ratings/r.png'
                if trailer["mpaa"].startswith('NC17'): imgRating='ratings/nc17.png'
                if trailer["mpaa"].startswith('Rated NC17'): imgRating='ratings/nc1.png'
                self.getControl(30013).setImage(imgRating)
                if do_timeout:
                    xbmc.sleep(5000)
                    self.close()
                
            def onAction(self, action):
                ACTION_PREVIOUS_MENU = 10
                ACTION_BACK = 92
                ACTION_ENTER = 7
                ACTION_I = 11
                ACTION_LEFT = 1
                ACTION_RIGHT = 2
                ACTION_UP = 3
                ACTION_DOWN = 4
                ACTION_TAB = 18
                ACTION_Q = 34
                ACTION_STOP = 13
                
                global do_timeout
                global exit_requested
                global trailer
                global movie_file
                movie_file=''
                
                if action == ACTION_PREVIOUS_MENU or action == ACTION_LEFT or action == ACTION_BACK or action ==ACTION_STOP:
                    do_timeout=False
                    xbmc.Player().stop()
                    exit_requested=True
                    self.close()
                
                if action == ACTION_Q:
                    strCouchPotato='plugin://plugin.video.couchpotato_manager/movies/add?title='+trailer['title']
                    xbmc.executebuiltin('XBMC.RunPlugin('+strCouchPotato+')') 
                    
                if action == ACTION_I or action == ACTION_DOWN:
                    self.close()
                    
                if action == ACTION_RIGHT or action == ACTION_TAB:
                    xbmc.Player().stop()
                    self.close()
                  
        def playTrailers():
            global exit_requested
            global movie_file
            global trailercount
            movie_file = ''
            exit_requested = False
            DO_CURTIANS = addon.getSetting('do_animation_search')
            trailercount = 0
            while not exit_requested:
                    mytrailerWindow = trailerWindow('script-trailerwindow.xml', addon_path,'default',)
                    mytrailerWindow.doModal()
                    del mytrailerWindow
                    if exit_requested:
                        break
                    if not exit_requested:
                        if DO_CURTIANS == 'true':
                            xbmc.Player().play(close_curtain_path)
                            while xbmc.Player().isPlaying():
                                xbmc.sleep(250)
                    exit_requested=True
        
        def check_for_xsqueeze():
            KEYMAPDESTFILE = os.path.join(xbmc.translatePath('special://userdata/keymaps'), "xsqueeze.xml")
            if os.path.isfile(KEYMAPDESTFILE):
                return True
            else:
                return False
        
        def get_mpaa(trailer):
            Rating='NR'
            if trailer["mpaa"].startswith('G'): Rating='G'
            if trailer["mpaa"] == ('G'): Rating='G'
            if trailer["mpaa"].startswith('Rated G'): Rating='G'
            if trailer["mpaa"].startswith('PG '): Rating='PG'
            if trailer["mpaa"] == ('PG'): Rating='PG'
            if trailer["mpaa"].startswith('Rated PG'): Rating='PG'
            if trailer["mpaa"].startswith('PG-13 '): Rating='PG-13'
            if trailer["mpaa"] == ('PG-13'): Rating='PG-13'
            if trailer["mpaa"].startswith('Rated PG-13'): Rating='PG-13'
            if trailer["mpaa"].startswith('R '): Rating='R'
            if trailer["mpaa"] == ('R'): Rating='R'
            if trailer["mpaa"].startswith('Rated R'): Rating='R'
            if trailer["mpaa"].startswith('NC17'): Rating='NC17'
            if trailer["mpaa"].startswith('Rated NC17'): 'NC17'
            return Rating
        
        def getallocinetrailer(typev):
            movielist=api.movielist(typev)
            return movielist
        def searchallocine(movie):
            movielist=api.search(movie,"movie")
            return movielist
        if not xbmc.Player().isPlaying() and not check_for_xsqueeze():
            DO_CURTIANS = addon.getSetting('do_animation_search')
            hidenoba=addon.getSetting('hide_noba')
            if DO_CURTIANS == 'true':
                xbmc.Player().play(open_curtain_path)
                while xbmc.Player().isPlaying():
                    xbmc.sleep(250)
            trailers = []
            filtergenre = False
            trailerNumber = 0
            library_trailers=[]
            iTunes_trailers=[]
            folder_trailers=[]
            tmdb_trailers=''
            # prompt user to type movie
            moviechoice = xbmcgui.Dialog().input(u"Quel film ?")
            dp=xbmcgui.DialogProgress()
            dp.create('Recherche','','','En cours')
            if len(moviechoice)>0:
                movielist=searchallocine(moviechoice)
                resultat=[]
                titres=[]
                try:
                    for movie in movielist['feed']['movie']:
                        ficheresult=api.movie(movie['code'])
                        if hidenoba:
                            pagetrailer=''
                            for x in ficheresult['movie']['link']:
                                if x.has_key('name') and 'Bandes annonces' in x['name']:
                                    pagetrailer=x['href']
                                    break
                                else:
                                    continue
                            if pagetrailer<>'':
                                soup = BeautifulSoup( urllib2.urlopen(pagetrailer), "html.parser" )
                                rows = soup.findAll("a")
                                hasba=0
                                for lien in rows:
                                    if 'annonce' in str(lien):
                                        hasba=1
                                        break
                                if hasba==0:
                                    continue
                            else:
                                continue
                        ficheresulttitle=ficheresult['movie']['title'].encode('utf-8')
                        ficheresulttitleori=ficheresult['movie']['originalTitle']
                        try:
                            yearresult=ficheresult['movie']['productionYear']
                        except:
                            yearresult=''
                        if yearresult<>'':
                            dictres={'titre' : ficheresulttitle, 'annee' : yearresult, 'infos':ficheresult['movie']}
                            resultat.append(dictres)
                            titres.append(ficheresulttitle+' - '+str(yearresult))
                    selectChoice = xbmcgui.Dialog().select(u"Résultats de recherche", titres)
                    if selectChoice<>-1:
                        titrefull=titres[selectChoice]
                        titre=titrefull[:titrefull.find('-')-1]
                        year=titrefull[titrefull.find('-')+2:]
                        ficheresult={}
                        for item in resultat:
                            if item['titre']==titre and item['annee']==int(year):
                                ficheresult=item['infos']
                                break
                        if ficheresult:
                            title=ficheresult['title']
                            try:
                                year=ficheresult['productionYear']
                            except:
                                year=''
                            try:
                                plot=ficheresult['synopsisShort'].encode("utf-8").replace('<p>','').replace('</p>','')
                            except:
                                plot=''
                            try:
                                releasedate=ficheresult['release']['releaseDate']
                                if len(releasedate)>=4:
                                    if len(releasedate)>=7:
                                        releasedate=releasedate[8:10]+'/'+releasedate[5:7]+'/'+releasedate[0:4]
                                    else:
                                        releasedate=releasedate[5:7]+'/'+releasedate[0:4]
                                                                        
                            except:
                                releasedate=year
                            try:
                                runtime=str(int(ficheresult['runtime'])/60)
                            except: 
                                runtime=''
                            try:
                                thumbs=ficheresult['defaultMedia']['media']['thumbnail']['href']
                            except:
                                thumbs=''
                            try:
                                poster=ficheresult['poster']['href']
                            except: 
                                poster=''
                                
                            pagetrailer=''
                            for x in ficheresult['link']:
                                if x.has_key('name') and 'Bandes annonces' in x['name']:
                                    pagetrailer=x['href']
                                else:
                                    continue
                            title=title.encode("utf-8")
                            dict={'trailer':pagetrailer,'id': [title,year,plot,releasedate,runtime,thumbs,poster],'source':'allo','title':title}
                            trailers.append(dict)
                    else:
                        trailers=[]                            
                except:
                    xbmcgui.Dialog().notification(u'Aucun résultat', moviechoice, xbmcgui.NOTIFICATION_INFO, 5000)
                
            exit_requested=False
            if dp.iscanceled():exit_requested=True 
            dp.close()
            if len(trailers) > 0 and not exit_requested:
                playTrailers()
            del bs
                    
        else:
            xbmc.log('Random Trailers: ' + 'Exiting Random Trailers Screen Saver Something is playing!!!!!!')
