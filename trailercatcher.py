# -*- coding: latin-1 -*-
import subprocess
import time
import datetime
import sys
import os.path
import unicodedata
import Tkinter
import shutil
import tkFileDialog
import glob
import pprint
from allocine import allocine
import urllib
import urllib2
import logging
import mechanize
import re
from bs4 import BeautifulSoup
import xbmc
import xbmcgui
api = allocine()
api.configure('100043982026','29d185d98c984a359e6e6f26a0474269')
rootDir = os.path.dirname(os.path.abspath(__file__))
try:
    _DEV_NULL = subprocess.DEVNULL
except AttributeError:
    _DEV_NULL = open(os.devnull, 'wb')
class trailercatcher(object):
    
    def logg(self,str,debug=None):
        ts=datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        print (ts+' : '+str.encode('utf-8'))
        return True
    
    def cleantitle(self,title):
        specialchars=['/','(',')',',','.',';','!','?','-',':','_','[',']','|','  ','  ','  ']
        title=unicodedata.normalize('NFKD',title).encode('ascii','ignore')
        for chars in specialchars:
            title=title.replace(chars,' ')        
        return title.lower()
        
    def libraryscan(self,path):
        self.logg('Veuillez patienter pendant la recherche des films sans bandes-annonces dans ' + path)
        fichier=[] 
        self.logg('Calcul en cours....')
        numberfiles=0
        pathori=path
        trailerfound=''
        for path, dires, fics in os.walk(path):
            for f in fics:
                numberfiles+=1
        currentnumber=0
        for root, dirs, files in os.walk(pathori):
            for i in files:
                currentnumber+=1
                trailercount=0
                if ('.mkv' in i.lower() or '.avi' in i.lower() or '.mp4' in i.lower() or '.m2ts' in i.lower() or '.mk3d' in i.lower()) and '-trailer' not in i:
                    for x in os.listdir(root):
                        if '-trailer' in x:
                            trailercount+=1
                            trailerfound=x
                    if trailercount==0:
                        fileroot=root
                        filename=i
                        filename=filename[:filename.rfind(")")].replace(' 3DBD','').replace('(','').replace(')','')
                        fichier.append([fileroot,filename,i[:-4]])
                    self.logg(str(currentnumber)+' fichiers scannes sur un total de '+str(numberfiles))   
        self.logg(str(numberfiles)+' fichiers scannes sur un total de '+str(numberfiles))
        return fichier,trailerfound
      
    def allocinesearch(self,moviename):
        series=['2','3','4','5','6','7','8']
        listallovostfr=[]
        listallovo=[]
        listallovf=[]
        self.logg('Tentative de recherche sur Allocine de ' +moviename[:-5])
        try:
            search = api.search(moviename[:-5], "movie")
            for result in search['feed']['movie']:
                countseries=0
                ficheresult=api.movie(result['code'])
                ficheresulttitle=self.cleantitle(ficheresult['movie']['title'])
                ficheresulttitleori=self.cleantitle(ficheresult['movie']['originalTitle'])
                yearresult=ficheresult['movie']['productionYear']
                test=self.cleantitle(moviename[:-5].decode('unicode-escape'))
                if not yearresult:
                    yearresult=0
                for x in series:
                    if (x in ficheresulttitle or x in ficheresulttitleori) and (not '3d' in ficheresulttitle and not '3d' in ficheresulttitleori):
                        if x not in moviename[:-5]:
                            countseries+=1                        
                if self.cleantitle(moviename[:-5].decode('unicode-escape')) in ficheresulttitle and countseries==0 and int(moviename[len(moviename)-4:])+2>yearresult and int(moviename[len(moviename)-4:])-2<yearresult:
                    goodresult=result
                    break
            
            self.logg('Recherche de la fiche du film avec le code : ' + str(goodresult['code']))
            movieallo = ficheresult
            for x in movieallo['movie']['link']:
                if x.has_key('name') and 'Bandes annonces' in x['name']:
                    pagetrailer=x['href']
                else:
                    continue
            soup = BeautifulSoup( urllib2.urlopen(pagetrailer), "html.parser" )
            rows = soup.findAll("a")
            
            for lien in rows:
                try:
                    if 'annonce' in str(lien).lower() and 'vf' in str(lien).lower():
                        lienid=lien['href'][:lien['href'].find('&')].replace('/video/player_gen_cmedia=','')
                        self.logg("Potentiel code de bande annonce [{0}] en VF".format(lienid))
                        trailerallo = api.trailer(lienid)
                        long=len(trailerallo['media']['rendition'])
                        bestba=trailerallo['media']['rendition'][long-1]
                        linkallo=trailerallo['media']['rendition'][long-1]['href']
                        heightbaallo=bestba['height']
                        longadr=len(linkallo)
                        extallo=linkallo[longadr-3:]
                        
                        listallovf.append({'link':linkallo,'ext':extallo,'height':heightbaallo})
                        if heightbaallo>=481:
                            self.logg('Bande annonce vf et HD trouve sur Allocine jarrete de chercher')
                            break
                        else:
                            self.logg('Bande annonce vf non HD trouve sur Allocine je continue de chercher')
                    elif 'annonce' in str(lien).lower() and 'vost' in str(lien).lower():
                        lienid=lien['href'][:lien['href'].find('&')].replace('/video/player_gen_cmedia=','')
                        self.logg("Potentiel code de bande annonce [{0}] en VOSTFR".format(lienid))
                        trailerallo = api.trailer(lienid)
                        long=len(trailerallo['media']['rendition'])
                        bestba=trailerallo['media']['rendition'][long-1]
                        linkallo=trailerallo['media']['rendition'][long-1]['href']
                        heightbaallo=bestba['height']
                        longadr=len(linkallo)
                        extallo=linkallo[longadr-3:]
                        
                        listallovostfr.append({'link':linkallo,'ext':extallo,'height':heightbaallo})
                        self.logg('Bande annonce vostfr trouve sur Allocine je continue de chercher')
                    elif 'annonce' in str(lien).lower() and ' VO' in str(lien):
                        lienid=lien['href'][:lien['href'].find('&')].replace('/video/player_gen_cmedia=','') 
                        trailerallo = api.trailer(lienid)
                        long=len(trailerallo['media']['rendition'])
                        bestba=trailerallo['media']['rendition'][long-1]
                        linkallo=trailerallo['media']['rendition'][long-1]['href']
                        heightbaallo=bestba['height']
                        longadr=len(linkallo)
                        extallo=linkallo[longadr-3:]
                        if hasattr(trailerallo['media'],'subtitles') and trailerallo['media']['subtitles']['$'].lower().replace('ç','c') ==u'francais':
                            self.logg("Potentiel code de bande annonce [{0}] en VOSTFR".format(lienid))
                            listallovostfr.append({'link':linkallo,'ext':extallo,'height':heightbaallo})
                            self.logg('Bande annonce vostfr trouve sur Allocine je continue de chercher')
                        else:
                            self.logg("Potentiel code de bande annonce [{0}] en VO".format(lienid))
                            listallovo.append({'link':linkallo,'ext':extallo,'height':heightbaallo})
                            self.logg('Bande annonce vo trouve sur Allocine je continue de chercher')
                    
                    else:
                        continue
                except Exception,e:
                    print e
                    continue
            self.logg(str(len(listallovf)) +" bandes annonces en VF trouvees sur allocine")
            self.logg(str(len(listallovostfr)) +" bandes annonces en VOSTFR trouvees sur allocine")
            self.logg(str(len(listallovo)) +" bandes annonces en VO trouvees sur allocine")       
            return listallovf,listallovostfr,listallovo
        except :
            self.logg(str(len(listallovf)) +" bandes annonces en VF trouvees sur allocine")
            self.logg(str(len(listallovostfr)) +" bandes annonces en VOSTFR trouvees sur allocine")
            self.logg(str(len(listallovo)) +" bandes annonces en VO trouvees sur allocine")  
            return listallovf,listallovostfr,listallovo
           
    def quacontrolallo(self,listallo,type):
        bestqualallo=0
        for linkvf in listallo:
            if bestqualallo<linkvf['height']:
                bestqualallo=linkvf['height']
        self.logg('Meilleure resolution trouvee sur Allocine en '+type+' : '+str(bestqualallo)+'p')
        return bestqualallo
    
    def videodl(self,cleanlist,trailername,moviename,trailerpath,allo=False,maxheight=0):
       if allo:
            for url in cleanlist:
                if maxheight==url['height']:
                    linkallo=url['link']
                    heightbaallo=url['height']
                    extallo=url['ext']
                    self.logg('Telechargement de la bande annonce suivante : ' + linkallo +' en '+str(heightbaallo)+'p en cours...')
                    try:
                        urllib.urlretrieve(linkallo, os.path.join(trailerpath,trailername)+'.'+extallo)
                        self.logg('Une bande annonce telechargee pour ' + moviename +' sur Allocine')
                        return trailerpath+'/'+trailername+'.'+extallo
                        break
                    except:
                        continue
            return False
            
    def trailersearch(self,moviefolder):
        dp=xbmcgui.DialogProgress()
        dp.create('Recherche','','','En cours')
        self.logg('Ceci est une beta. Certaines bandes annonces pourront etre en anglais voir ne pas correspondre au film')
        if len(moviefolder) > 0:
            self.logg("Vous avez choisi : %s" % moviefolder)
        
        path = moviefolder
        
        fichier,trailerfound = self.libraryscan(path)
        if len(fichier)>0:
            self.logg(str(len(fichier)) + ' films sans bandes annonces ont ete trouves')
            for moviewithouttrailer in fichier:
                self.logg(unicodedata.normalize('NFKD', moviewithouttrailer[1]).encode('ascii','ignore'))
        else:
            self.logg('Aucun film sans bande annonce trouve')
            xbmcgui.Dialog().notification(u'Le film possède une bande annonce', u'Je rafraichis la base de données avec', xbmcgui.NOTIFICATION_INFO, 5000)
            os.path.join(moviefolder,trailerfound)
            return os.path.join(moviefolder,trailerfound).replace('\\','/')
              
        for movie in fichier:
            trailerpath=movie[0]
            moviename = unicodedata.normalize('NFKD', movie[1]).encode('ascii','ignore')
            trailername=movie[2]+'-trailer'
            searchstring=moviename
            listvfallo,listvostfrallo,listvoallo=self.allocinesearch(moviename)
            dp.close()
            if listvfallo:
                maxqual=self.quacontrolallo(listvfallo,'vf')
                dp.create(u'Téléchargement','','','Bande annonce en VF en cours')
                path=self.videodl(listvfallo,trailername,moviename,trailerpath,True,maxqual)
                xbmcgui.Dialog().notification(u'Bande annonce téléchargée', u'Bande annonce téléchargée en VF. BDD mise à jour', xbmcgui.NOTIFICATION_INFO, 5000)
                dp.close()
                return path
            elif listvostfrallo:
                maxqual=self.quacontrolallo(listvostfrallo,'vostfr')
                dp.create(u'Téléchargement','','','Bande annonce en VOST en cours')
                path=self.videodl(cleanlistvf,trailername,moviename,trailerpath,True,maxqual)
                xbmcgui.Dialog().notification(u'Bande annonce téléchargée', u'Bande annonce téléchargée en VOST. BDD mise à jour', xbmcgui.NOTIFICATION_INFO, 5000)
                dp.close()
                return path
            elif listvoallo:
                maxqual=self.quacontrolallo(listvoallo,'vo')
                dp.create(u'Téléchargement','','','Bande annonce en VO en cours')
                path=self.videodl(listvoallo,trailername,moviename,trailerpath,True,maxqual)
                xbmcgui.Dialog().notification(u'Bande annonce téléchargée', u'Bande annonce téléchargée en VO. BDD mise à jour', xbmcgui.NOTIFICATION_INFO, 5000)
                dp.close()
                return path
            else:
                self.logg('Snifff encore un film pourri pas de bande annonce trouvee pour ' + moviename)
                xbmcgui.Dialog().notification(u'Bande annonce non trouvée', u'Essayez Bovfscraper qui a des chances de la trouver', xbmcgui.NOTIFICATION_INFO, 5000)
                return False
        