#CmDownloader YT-DL Version
#import os
from os import path

from os import remove
from os import rename
from os import mkdir

from os import system

from colorama import init

from youtube_dl import YoutubeDL #vielleicht lieber ganz youtube_dl aber das hier ist schneller ma sehen
import subprocess

import eyed3 #am besten nicht alles von eyed3 importen das zieht 2 milisekunden
import json
#from eyed3 import id3

import encodings.idna #??

dirname = path.dirname(__file__)

if path.exists("mp3") == False:
    print("Erstelle Ordner:\"mp3\"")
    mkdir("mp3")
if path.exists("mp4") == False:
    mkdir("mp4")
    print("Erstelle Ordner:\"mp4\"")

mp3dir = path.join(dirname, "mp3")
mp4dir = path.join(dirname, "mp4")

#videofile = mp4dir+"\\"+"videofile.mp4" die können glaub ich weg
#audiofile = mp4dir+"\\"+"audiofile.mp3"
#mp3audiofile = mp3dir+"\\"+"mp3audiofile.mp3"

sonderbuchstaben = ["\\","/",":","*","?","\"","<",">","|"]

debugmode = False

globalmsg = None

barsize = 100

progress = 0
def hook(d):
    global progress
    global filename
    global barsize
    if d["status"] == "downloading":
        try:
            total = int(d["total_bytes"])
        except:
            total = int(d["total_bytes_estimate"])
        #current = round((int(d["downloaded_bytes"])/int(d["total_bytes"]))*barsize)
        current = round((int(d["downloaded_bytes"])/total)*barsize)
        if current == 0:
            progress = 0
        elif current != progress:
            while progress < current:
                progress = progress+1
                print("█", end="", flush=True)#░▒▓█─__▔‾_
    elif d["status"] == "finished":
        progress = 0
        filename = d["filename"]
        #print(d["elapsed"])
    elif d["status"] == "error":
        print("Fehler")
def hookfinish(d):
    global filename
    if d["status"] == "finished":
        filename = d["filename"]

def debughook(d): #debughook
    print("xD")
    print(d)

def elapsedhook(d):
    if d["status"] == "finished":
        print(d["elapsed"])

def get_opts(opt, path, h): #out
    if opt == "bestmp4":
        ytdl_opts_bestmp4 = {
            "format": "bestvideo/best",
            "quiet": True,
            "outtmpl": path+".%(ext)s", #mp4dir + "/%(title)s.%(ext)s", %(playlist_title)s/ 
            "progress_hooks": [h],
            "logger": logger,
            }
        return ytdl_opts_bestmp4

    if opt == "bestmp3":
        ytdl_opts_bestmp3 = {
            "format": "bestaudio/best",
            "quiet": True,
            "outtmpl": path+".%(ext)s",
            "progress_hooks": [h],
            "logger": logger,
            }
        return ytdl_opts_bestmp3

    if opt == "quiet":
        ytdl_opts_quiet = {
            "quiet": True,
            "progress_hooks": [h],
            "ignoreerrors": True,
            "logger": logger,
            }
        return ytdl_opts_quiet

    if opt == "title":
        ytdl_opts_title = {
            "quiet": True,
            "progress_hooks": [h],
            "ignoreerrors": True,
            "extract_flat" : True,
            "logger": logger,
            }
        return ytdl_opts_title

def gettitle_old(video):
    return YoutubeDL(get_opts("quiet", None, None)).extract_info(video, download=False).get("title", None)

def gettitle_old2(video):
    return YoutubeDL(get_opts("title", None, None)).extract_info(video, download=False).get("title", None)
def gettitle(video):
    try:
        return YoutubeDL(get_opts("title", None, None)).extract_info(video, download=False)["title"]#.get("title", None)
    except:
        return None
def cleanstring(string):
    matches = [x for x in sonderbuchstaben if x in string]
    for s in matches:
        string = string.replace(s,"")
    return string

class logger:
    def debug(msg):
        if debugmode == True:
            print("Debug: "+msg)
        else:
            pass
    def warning(msg):
        if debugmode == True:
            print("Warnung: "+msg)
        else:
            pass
    def error(msg):
        global globalmsg
        globalmsg = msg
        if debugmode == True:
            print("Fehler: "+msg)
            #if "is not a valid URL" in msg:
                #print("\n[X] Kein gültiger Link oder Befehl.")
                #print("msg"+msg)
            #elif "Sign in to confirm your age" in msg:
                #print("\n[X] Video ist altersbeschränkt.")
            #else:
                #print("Fehler: "+msg)

class mono: # für ein video
    def customname(directory, mpformat):
        while True:
            print("\n┌ Benutzerdefinierten Videonamen angeben. Leer lassen für normalen YouTube Titel.\n|")
            customname = input("└ ")
            customname = cleanstring(customname)
            if not customname:
                outputname = videotitle
            else:
                outputname = customname
            outputfile = directory+"\\"+outputname+mpformat
            if path.exists(outputfile) == True:
                print("\n\033[31m[X]\033[0m Datei existiert bereits. Bitte anderen Namen wählen.")
                continue
            else:
                print("\n\033[32m[√]\033[0m Dateiname:", outputname)
                return outputfile
                break
    class mp4:
        def run():
            outputfile = mono.customname(mp4dir, ".mp4")#print(outputfile+"/%(title)s.%(ext)s")
            files = mono.mp4.download()
            mono.mp4.combine(files[0], files[1], outputfile)
            print("\n\033[32m[√]\033[0m Download Abgeschlossen.")
        def download():
            global barsize
            barsize = 50
            print("\n┌ Downloade Video und Audio:\n├────────────────────────────────────────────────────────────────────────────────────────────────────┐\n|", end="")#├┌┐└┘
            YoutubeDL(get_opts("bestmp4", mp4dir+"\\"+"videofile", hook)).download([video_url])
            videofile = filename
            YoutubeDL(get_opts("bestmp3", mp4dir+"\\"+"audiofile", hook)).download([video_url])
            audiofile = filename
            print("|\n├────────────────────────────────────────────────────────────────────────────────────────────────────┘")
            files = [videofile, audiofile]
            return files
        def combine(vf, af, out):
            print("└ Kombiniere beide Dateien...")
            command = str("ffmpeg.exe -hide_banner -loglevel error -i \""+vf+"\" -i \""+af+"\" -y -c:v copy -c:a aac \""+out+"\"")
            subprocess.run(command)#, shell=False)
            remove(vf)
            remove(af)

    class mp3:
        def run():
            outputfile = mono.customname(mp3dir, ".mp3")
            mono.mp3.download()
            mono.mp3.convert(filename, outputfile)
            print("\n\033[32m[√]\033[0m Download abgeschlossen und Video konvertiert.")
        def download():
            global barsize
            barsize = 100
            print("\n┌ Downloade und konvertiere Video:\n├────────────────────────────────────────────────────────────────────────────────────────────────────┐\n|", end="")
            YoutubeDL(get_opts("bestmp3", mp3dir+"\\"+"mp3audiofile", hook)).download([video_url])
            print("|\n└────────────────────────────────────────────────────────────────────────────────────────────────────┘")
        def convert(af, out):
            command = str("ffmpeg.exe -hide_banner -loglevel error -i \""+af+"\" \""+out+"\"")
            subprocess.run(command, shell=False)
            remove(af)

class poly: #für playlists format = mp3 mp4
    playlistqueue = 0
    def getplaylistlinks(playlist):
        links = []
        result = YoutubeDL(get_opts("title", None, None)).extract_info(playlist, download=False)
        videos = result["entries"]
        for i, item in enumerate(videos):
            try:
                videos = result["entries"][i]['url']#['webpage_url']
                links.append(videos)
            except Exception as e:
                print(e)
                continue
        return links #return len(YoutubeDL(get_opts("quiet")).extract_info(playlist, download=False)["entries"])
    def anfang(num, end):
        if num == 1:
            anfang = "├ "
        elif num == end:
            anfang = "└ "
        else:
            anfang = "| "
        return anfang
    class mp4:
        def run():
            #global links
            playlistdir = mp4dir+"\\"+cleanstring(playlisttitle)
            links = poly.getplaylistlinks(video_url)
            linkslen = len(links)
            print("\n┌ Videos in Playlist: "+str(linkslen)+"\n|\n├ Downloade Videos:\n|")
            for video in links:
                poly.playlistqueue = poly.playlistqueue+1
                videotitle = gettitle(video)
                if not videotitle:
                    print("├", end="")
                    linkslen = linkslen-1
                    poly.playlistqueue = poly.playlistqueue-1
                    poly.mp4.fehlermeldungen()
                    continue
                outputfile = playlistdir+"\\"+cleanstring(videotitle)+".mp4"
                print(poly.anfang(poly.playlistqueue, linkslen)+str(poly.playlistqueue)+". "+videotitle, end="")
                if path.exists(outputfile) == True:
                    print(" \033[31m[X]\033[0m Datei existiert bereits.")
                    continue
                files = poly.mp4.download(video, playlistdir)
                poly.mp4.combine(files[0], files[1], outputfile)
                print(" \033[32m[√]\033[0m")
            print("\n\033[32m[√]\033[0m Downloads Abgeschlossen.")
        def download(link, playlistdir):
            YoutubeDL(get_opts("bestmp4", playlistdir+"\\"+"videofile", hookfinish)).download([link])
            videofile = filename
            YoutubeDL(get_opts("bestmp3", playlistdir+"\\"+"audiofile", hookfinish)).download([link])
            audiofile = filename
            files = [videofile, audiofile]
            return files
        def combine(vf, af, out):
            command = str("ffmpeg.exe -hide_banner -loglevel error -i \""+vf+"\" -i \""+af+"\" -y -c:v copy -c:a aac \""+out+"\"")
            subprocess.run(command)
            remove(vf)
            remove(af)
        def fehlermeldungen():
            if "Sign in to confirm your age" in globalmsg:
                print("\033[31m[X]\033[0m Video ist altersbeschränkt.")
            elif "Video unavailable" in globalmsg:
                print("\033[31m[X]\033[0m Video ist nicht verfügbar.")
            elif "Private video" in globalmsg:
                print("\033[31m[X]\033[0m Video ist Privat.")
            else:
                print("\033[31m[X]\033[0m Video nicht gefunden. Fehler:", globalmsg)
    class cleanmp3:
        #archive = []
        #archivelinks = []
        def run():
            playlistdir = poly.cleanmp3.getplaylistdir()
            if not path.exists(playlistdir):
                mkdir(playlistdir)
            fullarchive = poly.cleanmp3.logik(playlistdir)
            print("\n┌ Videos in Playlist:",len(fullarchive["archive"]),"\n|\n├ Downloade und konvertiere Videos:\n|")
            for i, video in enumerate(fullarchive["archive"]):
                videotitle = fullarchive["titles"][i]
                print(poly.anfang(i+1 , len(fullarchive["archive"]))+str(i+1)+". "+videotitle, end="")
                outputfile = playlistdir+"\\"+cleanstring(videotitle)+".mp3"
                if path.exists(outputfile) == True:
                    if not gettitle(video):
                        print(" \033[31m[X]\033[0m Datei existiert noch, ist aber nicht mehr in der Playlist.")
                    else:
                        print(" \033[31m[X]\033[0m Datei existiert bereits.")
                    poly.cleanmp3.metadata(i+1, outputfile)
                    continue
                poly.cleanmp3.download(video, playlistdir)
                poly.cleanmp3.convert(filename, outputfile)
                poly.cleanmp3.metadata(i+1, outputfile)
                print(" \033[32m[√]\033[0m")
            print("\n\033[32m[√]\033[0m Downloads Abgeschlossen.")
            if globalmsg:
                print(" |\n\033[33m[!]\033[0m Manche Videos waren altersbeschränkt, privat oder nicht verfügbar.")
        def download(link, playlistdir):
            YoutubeDL(get_opts("bestmp3", playlistdir+"\\"+"mp3audiofile", hookfinish)).download([link])
        def convert(af, out):
            command = str("ffmpeg.exe -hide_banner -loglevel error -i \""+af+"\" \""+out+"\"")
            subprocess.run(command, shell=False)
            remove(af)
        def metadata(num, file):
            eye = eyed3.load(file)
            eye.tag.track_num = num
            eye.tag.album = playlisttitle
            eye.tag.save()
        def logik(playlistdir):
            archivelinks = []
            titles = []
            links = poly.getplaylistlinks(video_url)
            archivepath = playlistdir+"\\"+cleanstring(playlisttitle)+".txt"
            fullarchive = poly.cleanmp3.getarchive(archivepath)
            if fullarchive:
                archive = fullarchive["archive"]
            else:
                fullarchive = {}
                archive = []
                titles = []
            for video in links:
                poly.playlistqueue = poly.playlistqueue+1

                videotitle = gettitle(video)
                if not videotitle:
                    poly.playlistqueue = poly.playlistqueue-1
                    continue
                if fullarchive:
                    if links.index(video) <= len(archive)-1:
                        #print(archive[links.index(video)])
                        if not archive[links.index(video)] in links:
                            title = gettitle(archive[links.index(video)])
                            if not title: #wenns succeded dann wurds extra deleted und sollte daher auch ausm index entfernt werden
                                title = fullarchive["titles"][links.index(video)] #[archive.index(item)]
                                file = playlistdir+"\\"+cleanstring(title)+".mp3"
                                if path.exists(file) == True:
                                    archivelinks.insert(poly.playlistqueue-1, archive[links.index(video)]) #der hier
                                    titles.insert(poly.playlistqueue-1, title)
                                    poly.playlistqueue = poly.playlistqueue+1
                                else:
                                    pass
                            else:
                                file = playlistdir+"\\"+cleanstring(title)+".mp3"
                                if path.exists(file) == True:
                                    remove(file)
                        else:
                            pass
                    else:
                        pass
                else:
                    pass
                archivelinks.insert(poly.playlistqueue-1, video)
                titles.insert(poly.playlistqueue-1, videotitle)
            if fullarchive:
                for item in archive:
                    if not item in archivelinks:
                        title = gettitle(item)
                        if not title:
                            title = fullarchive["titles"][archive.index(item)]
                            file = playlistdir+"\\"+cleanstring(title)+".mp3"
                            if path.exists(file) == True:
                                poly.playlistqueue = poly.playlistqueue+1
                                archivelinks.insert(poly.playlistqueue-1, item)#archive[archive.index(item)]
                                titles.insert(poly.playlistqueue-1, title)
                        else:
                            file = playlistdir+"\\"+cleanstring(title)+".mp3"
                            if path.exists(file) == True:
                                remove(file)

            #print("links:        ", links, "\narchive:      ", archive, "\narchivelinks: ", archivelinks, "\ntitles:       ", titles)
            archive = archivelinks
            fullarchive["archive"] = archive
            fullarchive["titles"] = titles
            poly.cleanmp3.savearchive(fullarchive, archivepath)
            return fullarchive#, linkslen#ich glaube linkslen wird gar nicht mehr benötigt weil man einfach len(archivelinks) machen kann
        def getarchive(archivepath):
            if path.exists(archivepath) == True:
                with open(archivepath, "r") as file:
                    return json.load(file)
            else:
                #open(archivepath, "w")
                return None #[]
        def savearchive(archive, archivepath):
            with open(archivepath, "w") as file:
                json.dump(archive, file)
        def getplaylistdir():
            return mp3dir+"\\"+cleanstring(playlisttitle)
#interface start
info = """
┌ Der YouTube-Downloader gemacht von einem Entwickler bei \"420NussbaumProductions\"
│
├ \033[31mChangelog:\033[0m
| \033[91mVersion 1.6.0\033[0m
│ -Neues Startlogo,
│ -Playlists werden in ordner gespeichert
│ -Archive Feature (mehr dazu im Handbuch)
│ -Support für mehr Platformen
│ -Programm wurde komplett umgeschrieben für das Modul "youtube-dl"
│
| \033[91mVersion 1.6.1\033[0m
│ -Bug fixes
├ \033[31mHandbuch:\033[0m
│ Gebe im Hauptmenü einen Video- oder Playlistlink an. Unterstützt sind:
│ -Youtube Videos und Playlists
│ -Soundcloud (nur einzelne Songs)
│ -Reddit Videos
│
| Und noch vieles mehr das Modul unterstützt vieles aber diese 3 wurden von mir getestet.
│ Zur Not einfach ausprobieren und mich anschreiben, dass ich den Support dafür einbaue.
│
| All diese kann man entweder in Mp4 oder Mp3 downloaden mit der höchsten Qualität als Standard,
│ was sich in späteren Versionen noch einstellbar machen lässt. Die Videos werden entweder in
│ den Ordner "Mp3" oder "Mp4" abgespeichert, mit einen wählbaren Namen, der aber
│ sonst der YouTube Titel ist.
│
| Playlists werden in einen eigenen Ordner im jeweiligen Formatordner abgespeichert, der nach der
│ Playlist benannt wird. Videos werden hineingedownloaded und in einer Txt-Datei vermerkt.
│ Falls ein Video aus der Playlist nun also gelöscht wird, existiert es doch immer noch im Ordner
│ und damit in der nochmals gedownloadeten Playlists, wenn man sie "updatet".
│ Wird ein Video manuell gelöscht wird es auch als File aus dem Ordner gelöscht.
│
| Jedes gedownloadete YouTube-Video aus der jeweiligen Playlist wird mit einer Track Number
│ nummeriert damit die Playlist einfach in der richtigen Reihenfolge abgespielt werden kann.
│ Falls ein Video aus der Playlist deleted ist, aber noch im Ordner mit ist, weicht die Track
│ Number von der Playlist-Nummerierung in Youtube ab.
│
| Unavailable und Altersbeschränkte Videos sind nicht downloadbar und werden im Playlistdownload
│ geskipt, mit einer Warnung am Ende, dass manche Videos fehlen.
│
├ \033[31mKontakt:\033[0m
| Bei Bugs anderen Fehlern oder Verbresserungsvorschlägen kontaktiere mich, falls kein anderer Weg
└ möglich ist, unter \033[94m420NussbaumProductions@gmail.com\033[0m."""
#print("420NBP CM-DL")
init(autoreset=True)
system("mode 180, 45")
print("""\033[90m-   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -
    \033[31m****************************************  \033[32m    _ _ ___ __  _  _            _                     ___             _         _   _                \033[31m
  ***(#***************************************  \033[32m | | |_  )  \| \| |_  _ _____| |__  __ _ _  _ _ __ | _ \_ _ ___  __| |_  _ __| |_(_)___ _ _  ___ ® \033[31m
 ****#\033[37m@@@@\033[31m************************************* \033[32m |_  _/ / () | .` | || (_-<_-< '_ \/ _` | || | '  \|  _/ '_/ _ \/ _` | || / _|  _| / _ \ ' \(_-<   \033[31m
 ****#\033[37m@@@@@@@@&&\033[31m******************************* \033[32m   |_/___\__/|_|\_|\_,_/__/__/_.__/\__,_|\_,_|_|_|_|_| |_| \___/\__,_|\_,_\__|\__|_\___/_||_/__/   \033[31m
 ****#\033[37m@@&@@@@@@@@@@@@\033[31m************************** \033[32m ───────────────────────────────────────────────────────────────────────────────────────────────── \033[31m
 ****#\033[37m@@(          *@@@@@\033[31m**********************
 ****#\033[37m@@(  *&&&)     *#@@@@@@\033[31m******************\033[37m   $$$$$$\                \033[31m$$$$$$$\                                    $$\                           $$\                    
 ****#\033[37m@@(  *@@@@@&)   *@@@@@@@@@\033[31m***************\033[37m  $$  __$$\               \033[31m$$  __$$\                                   $$ |                          $$ |
 ****#\033[37m@@(  *@@@@@@@)  *@@@@@@@@@@@@@@\033[31m**********\033[37m  $$ /  \__|$$$$$$\$$$$\  \033[31m$$ |  $$ | $$$$$$\  $$\  $$\  $$\ $$$$$$$\  $$ | $$$$$$\   $$$$$$\   $$$$$$$ | $$$$$$\   $$$$$$\        
 ****#\033[37m@@(  *@@@@@@@)  *@@@@@@@@@@@@@@@@@&\033[31m******\033[37m  $$ |      $$  _$$  _$$\ \033[31m$$ |  $$ |$$  __$$\ $$ | $$ | $$ |$$  __$$\ $$ |$$  __$$\  \____$$\ $$  __$$ |$$  __$$\ $$  __$$\ 
 ****#\033[37m@@(  *@@@@@@@)  *@@@@@@@@@@@@@*     \033[31m.****\033[37m  $$ |      $$ / $$ / $$ |\033[31m$$ |  $$ |$$ /  $$ |$$ | $$ | $$ |$$ |  $$ |$$ |$$ /  $$ | $$$$$$$ |$$ /  $$ |$$$$$$$$ |$$ |  \__| 
 ****#\033[37m@@(  *@@@@@&)   *@@@@@@@@@****   \033[31m.*******\033[37m  $$ |  $$\ $$ | $$ | $$ |\033[31m$$ |  $$ |$$ |  $$ |$$ | $$ | $$ |$$ |  $$ |$$ |$$ |  $$ |$$  __$$ |$$ |  $$ |$$   ____|$$ |  
 ****#\033[37m@@(  *&&&)    .#@@@@@@@*     \033[31m,***********\033[37m  \$$$$$$  |$$ | $$ | $$ |\033[31m$$$$$$$  |\$$$$$$  |\$$$$$\$$$$  |$$ |  $$ |$$ |\$$$$$$  |\$$$$$$$ |\$$$$$$$ |\$$$$$$$\ $$ |  
 ****#\033[37m@@(         .@@@@@***   \033[31m.,***************\033[37m   \______/ \__| \__| \__|\033[31m\_______/  \______/  \_____\____/ \__|  \__|\__| \______/  \_______| \_______| \_______|\__|
 ****#\033[37m@@@@@@@@@@@@@*   \033[31m...*********************
 ****#\033[37m@@@@@@@*     \033[31m...************************* \033[90m  _   __            _              __   ____    __\033[31m
 ****#\033[37m@€***  \033[31m.../###########################(** \033[90m | | / /__ _______ (_)__  ___     / /  / __/   / / \033[31m
 ****.    ,***/&\033[37m@@@@@@@@@@@@@@@@@@@@@@@@@@@\033[31m(*** \033[90m | |/ / -_) __(_-</ / _ \/ _ \   / /  / _ \   / /\033[31m
  \033[31m***,,*********                            ** \033[90m  |___/\__/_/ /___/_/\___/_//_/  /_/()/____/()/_/\033[31m
    \033[31m*****************************************
\033[90m-   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -\033[0m""")
while True:
    print("\n┌ \033[31mMenü\033[0m - Gebe einen der folgenden Befehle ein:\n|\n| - \033[91mVideo- oder Playlistlink\033[0m\n|\n| - \"info\"\n|\n| - \033[90m\"conf\"\033[0m\n|")
    #"\n┌ Gebe einen YouTube Video- oder Playlist-Link an, oder schreibe \"conf\" um die Einstellungen zu öffnen.\n|"
    video_url = input("└ > ")
    if video_url == "conf":
        print("\n\033[33m[!]\033[0m Einstellungen sind noch in Bearbeitung.")
        input("\n» Drücke \"Enter\", um die Einstellungen zu verlassen.")
        continue
    elif video_url == "info":
        print(info)
        #print("\nDer YouTube-Downloader gemacht von einem Entwickler bei \"420NussbaumProductions\"\nHandbuch:\n\n[!] In Bearbeitung")
        input("\n» Drücke \"Enter\", um das Handbuch zu verlassen.")
        continue
    elif video_url == "debug":
        debugmode = True
        print("Debug Modus aktiviert")
        continue
    elif video_url == "exit":
        break
    elif "playlist?list" in video_url:
        playlisttitle = gettitle(video_url)
        if not playlisttitle:
            print("\n\033[31m[X]\033[0m Playlist nicht gefunden. Fehler:", globalmsg)
            continue
        print("\n\033[32m[√]\033[0m Playlist gefunden:", playlisttitle)
            #if globalmsg:
                #print(" |\n[!] Manche Videos sind altersbeschränkt, privat oder nicht verfügbar.")
        print("\n┌ Gebe das gewünschte Dateiformat in die Konsole ein: \"mp3\" oder \"mp4\".\n|")
        menuinput = input("└ ")
        if menuinput == "mp4":
            print("\n\033[32m[√]\033[0m Dateiformat: mp4")
            poly.mp4.run()
            break
        elif menuinput == "mp3":
            print("\n\033[32m[√]\033[0m Dateiformat: mp3")
            poly.cleanmp3.run()
            break
        else:
            print("\n\033[31m[X]\033[0m Befehl nicht erkannt: Schreibe \"mp3\" oder \"mp4\"")
            continue
    else:
        videotitle = gettitle(video_url)
        if not videotitle:
            if "is not a valid URL" in globalmsg:
                print("\n\033[31m[X]\033[0m Kein gültiger Link oder Befehl.")
            elif "Sign in to confirm your age" in globalmsg:
                print("\n\033[31m[X]\033[0m Video ist altersbeschränkt.")
            elif "Video unavailable" in globalmsg:
                print("\n\033[31m[X]\033[0m Video ist nicht verfügbar.")
            elif "Private video" in globalmsg:
                print("\n\033[31m[X]\033[0m Video ist Privat.")
            else:
                print("\n\033[31m[X]\033[0m Video nicht gefunden. Fehler:", globalmsg)
            continue
        else:
            print("\n\033[32m[√]\033[0m Video gefunden:", videotitle)
        videotitle = cleanstring(videotitle)
        print("\n┌ Gebe das gewünschte Dateiformat in die Konsole ein: \"mp3\" oder \"mp4\".\n|")
        menuinput = input("└ ")
        if menuinput == "mp4":
            print("\n\033[32m[√]\033[0m Dateiformat: mp4")
            mono.mp4.run()
            break
        elif menuinput == "mp3":
            print("\n\033[32m[√]\033[0m Dateiformat: mp3")
            mono.mp3.run()
            break
        else:
            print("\n\033[31m[X]\033[0m Befehl nicht erkannt: Schreibe \"mp3\" oder \"mp4\"")
            continue

input("\n» Drücke \"Enter\", um das Programm zu schließen.")
