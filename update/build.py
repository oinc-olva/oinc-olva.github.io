#!/usr/bin/env python3
import yaml
import json
import re
import urllib.request
import urllib.parse
from os import path as ospath
from os import system as runcmd
from time import gmtime, strftime

def main():
    # Vind de locatie van dit script
    cd = ospath.dirname(__file__)

    # Laad omgevingsvariabelen
    with open('env_vars.yaml', 'r') as f:
        ENV_VARS = yaml.safe_load(f)
    
    # --- Initialisatie variabelen -------------------------------------------------------
    channel_data = dict()
    video_paths = dict()

    global failed_video_count
    failed_video_count = 0
    global isTrailerThumbCached
    isTrailerThumbCached = False

    seen_publish_school_years = []

    # --- Algemene data van het kanaal -------------------------------------------------------
    # Divers
    general_channel_data_request = urllib.request.urlopen(f"https://www.googleapis.com/youtube/v3/channels?key={ENV_VARS['api_key']}&id={ENV_VARS['channel_id']}&part=snippet,brandingSettings,statistics,contentDetails")
    general_channel_data = json.loads(general_channel_data_request.read())['items'][0]
    channel_data['title'] = general_channel_data['snippet']['title']
    channel_data['description'] = general_channel_data['snippet']['description'].replace('\r', '')
    channel_data['logo'] = general_channel_data['snippet']['thumbnails']['medium']['url']
    channel_data['banner'] = general_channel_data['brandingSettings']['image']['bannerExternalUrl'].replace('lh3.googleusercontent.com', 'yt3.ggpht.com')  + "=w1707"
    channel_data['trailer'] = general_channel_data['brandingSettings']['channel']['unsubscribedTrailer']
    channel_data['statistics'] = general_channel_data['statistics']
    channel_data['uploadsPlaylistId'] = general_channel_data['contentDetails']['relatedPlaylists']['uploads']

    # Sla logo en banner op
    if ospath.isdir(cd + '/../dist'):
        urllib.request.urlretrieve(channel_data['logo'], cd + '/../dist/logo.jpg')
        urllib.request.urlretrieve(channel_data['banner'], cd + '/../dist/banner.jpg')
    urllib.request.urlretrieve(channel_data['logo'], cd + '/../public/logo.jpg')
    urllib.request.urlretrieve(channel_data['banner'], cd + '/../public/banner.jpg')

    # --- (Sociale media)links op het kanaal -------------------------------------------------------
    # Neem data op
    html = urllib.request.urlopen(f"https://youtube.com/channel/{ENV_VARS['channel_id']}").read().decode('utf-8')
    header_links = json.loads('{' + re.findall(r"\"headerLinks(?:(?!,\"subscribeButton\").)*", html)[0] + '}')['headerLinks']['channelHeaderLinksRenderer']

    # Maak lijst van sociale media
    AVAILABLE_SOCIAL_ICONS = ['discord', 'facebook-messenger', 'whatsapp', 'facebook', 'instagram', 'youtube', 'snapchat', 'tiktok', 'twitch', 'twitter', 'wix', 'wordpress', 'squarespace', 'github', 'google']
    social_links = []
    for link in [*header_links['primaryLinks'], *header_links['secondaryLinks']]:
        # Vind URL van sociale media
        url = urllib.parse.unquote(link['navigationEndpoint']['urlEndpoint']['url'].partition('&q=')[2])
        if not url.endswith('/'):
            url += '/'

        # Laat link weg als het wijst naar de website zelf
        if 'oinc-olva.github.io' in url or 'oinc.olva.be' in url:
            continue

        # Vind naam van sociale media
        parts = url.split('.')
        if parts[0] == 'https://www' or parts[0] == 'http://www':
            parts = parts[1:]
        elif parts[0].startswith('https://'):
            parts[0] = parts[0][8:]
        elif parts[0].startswith('http://'):
            parts[0] = parts[0][7:]
        
        subdomainsNum = -1
        for part in parts:
            if '/' in part:
                break
            subdomainsNum += 1

        name = parts[subdomainsNum]
        if name == 'messenger':
            name = 'facebook-messenger'
        
        # Sla URL en naam op
        social_links.append({
            'url': url,
            'name': name,
            'title': link['title']['simpleText'],
            'iconAvailable': name in AVAILABLE_SOCIAL_ICONS
        })

    # Voeg link naar kanaal toe
    channel_link = {
        'url': f"https://youtube.com/channel/{ENV_VARS['channel_id']}",
        'name': 'youtube',
        'title': 'YouTube',
        'iconAvailable': True
    }
    if social_links[0]['name'] == 'olva':
        social_links.append(channel_link)
    else:
        social_links.insert(0, channel_link)

    # Registreer data
    channel_data['socialLinks'] = social_links

    # --- Opname van videos: algemene functies -------------------------------------------------------
    # Functie om een datum van een video te vervormen naar het gewenst formaat (YYYY-MM-DD => DD [maand in het Nederlands] YYYY)
    def translate_date(date):
        MAANDEN = ['januari', 'februari', 'maart', 'april', 'mei', 'juni', 'juli', 'augustus', 'september', 'oktober', 'november', 'december']
        
        year = date[:4]
        month  = int(date[5:7])
        day = date[8:10]
        
        return day + ' ' + MAANDEN[month - 1] + ' ' + year

    # Functie om een schooljaar te berekenen waarin een datum valt
    def get_school_year(date):
        year = int(date[:4])
        month  = int(date[5:7])

        if month < 9: year -= 1
        school_year = str(year) + ' - ' + str(year + 1)

        if school_year not in seen_publish_school_years:
            seen_publish_school_years.append(school_year)
        return school_year

    # Functie voor het verwerken van videodata
    def get_video_data(video_id):
        global failed_video_count
        global isTrailerThumbCached

        videodata = urllib.request.urlopen(f"https://www.googleapis.com/youtube/v3/videos?key={ENV_VARS['api_key']}&id={video_id}&part=snippet,contentDetails,statistics")
        videodata = json.loads(videodata.read())['items']
        if len(videodata) == 0:
            failed_video_count += 1
            return None
        else:
            videodata = videodata[0]

            # Vind thumbnail
            thumbnails = videodata['snippet']['thumbnails']
            if 'maxres' in thumbnails:
                thumbmaxres_type = 3
                thumb_maxres_url = thumbnails['maxres']['url']
            elif 'high' in thumbnails:
                thumbmaxres_type = 2
                thumb_maxres_url = thumbnails['high']['url']
            elif 'medium' in thumbnails:
                thumbmaxres_type = 1
                thumb_maxres_url = thumbnails['medium']['url']
            else:
                thumbmaxres_type = 0
                thumb_maxres_url = '/thumbdefault.jpg'

            # Vind titel
            video_title = videodata['snippet']['title']

            # Bereken tijd van video
            video_duration_iso = videodata['contentDetails']['duration'][2:]
            video_duration_partsStr = list(filter(lambda part: part != '', re.split('[HMS]', video_duration_iso)))
            for i, partDur in enumerate(video_duration_partsStr[1:]):
                if len(partDur) == 1: video_duration_partsStr[i + 1] = '0' + partDur

            if video_duration_iso[-1] == 'H': video_duration_partsStr.extend(('00', '00'))
            if video_duration_iso[-1] == 'M': video_duration_partsStr.append('00')
            if len(video_duration_partsStr) == 1: video_duration_partsStr.insert(0, '0')

            video_duration_partsInt = [int(x) for x in video_duration_partsStr]
            video_duration_sec = 0
            for i, partDur in enumerate(video_duration_partsInt):
                video_duration_sec += partDur * pow(60, len(video_duration_partsInt) - 1 - i)

            if len(video_duration_partsInt) == 2: video_duration_partsInt.insert(0, 0)
            TR = ['uur', 'uren', 'minuut', 'minuten', 'seconde', 'seconden']
            video_duration_translated_parts = []
            for i, partDur in enumerate(video_duration_partsInt):
                if partDur == 0:
                    continue
                elif partDur == 1:
                    video_duration_translated_parts.append('1 ' + TR[i*2])
                else:
                    video_duration_translated_parts.append(str(partDur) + ' ' + TR[i*2+1])

            # Sla trailer thumbnail op
            if channel_data['trailer'] == video_id and not isTrailerThumbCached:
                if ospath.isdir(cd + '/../dist'):
                    urllib.request.urlretrieve(thumb_maxres_url, cd + '/../dist/overons.jpg')
                urllib.request.urlretrieve(thumb_maxres_url, cd + '/../public/overons.jpg')

            # Bereken publicatiedatum
            publish_date = videodata['snippet']['publishedAt'][:10]

            # Registreer omleidingslink
            video_path = video_title.lower().replace(' ', '-').replace('+', 'plus').replace('@', 'at').replace('&', 'en').replace('€', 'euro').replace('$', 'dollar')
            video_path = re.sub(r'[^\x00-\x7f]',r'', video_path)
            video_path = re.sub(r'[\.\,\!\?\:\;\"\'\`\\\/\%\|\#\>\<]',r'', video_path)
            video_path = re.sub(r'(-)\1+',r'\1', video_path)
            video_paths[video_id] = dict()
            video_paths[video_id]["title"] = video_title
            video_paths[video_id]["path"] = video_path

            return {
                'id': video_id,
                'title': video_title,
                'description': videodata['snippet']['description'],
                'durationSec': video_duration_sec,
                'durationFormatted': ':'.join(video_duration_partsStr),
                'durationFormattedParts': len(video_duration_partsStr),
                'durationTranslated': ' '.join(video_duration_translated_parts),
                'publishDate': translate_date(publish_date),
                'publishSchoolYear': get_school_year(publish_date),
                'publishYear': publish_date[:4],
                'views': videodata['statistics']['viewCount'],
                'thumb': videodata['snippet']['thumbnails']['medium']['url'],
                'thumbmaxres': thumb_maxres_url,
                'thumbmaxres_type': thumbmaxres_type,
                'videoPath': video_path
            }

    # --- Opname van videos: afspeellijsten -------------------------------------------------------
    # Functie voor het vinden van video ids in een afspeellijst
    def find_playlist_video_ids(playlist_id):
        playlist_video_ids = list()
        playlist_page_request = urllib.request.urlopen(f"https://www.googleapis.com/youtube/v3/playlistItems?key={ENV_VARS['api_key']}&playlistId={playlist_id}&part=contentDetails&maxResults=50")
        while True:
            playlist_page = json.loads(playlist_page_request.read())
            for playlist_item in playlist_page['items']:
                playlist_video_ids.append(playlist_item['contentDetails']['videoId'])
            if 'nextPageToken' in playlist_page:
                playlist_page_request = urllib.request.urlopen(f"https://www.googleapis.com/youtube/v3/playlistItems?key={ENV_VARS['api_key']}&playlistId={playlist_id}&part=contentDetails&maxResults=50&pageToken={playlist_page['nextPageToken']}")
            else:
                break
        return playlist_video_ids

    # Vind alle afspeellijsten
    playlists = list()
    playlists_page_request = urllib.request.urlopen(f"https://www.googleapis.com/youtube/v3/playlists?key={ENV_VARS['api_key']}&channelId={ENV_VARS['channel_id']}&part=snippet&maxResults=50")
    playlists_page = json.loads(playlists_page_request.read())
    while True:
        for playlist in playlists_page['items']:
            playlists.append({
                'id': playlist['id'],
                'title': playlist['snippet']['title'],
                'description': playlist['snippet']['description']
            })
        if 'nextPageToken' in playlists_page:
            playlists_page = urllib.request.urlopen(f"https://www.googleapis.com/youtube/v3/playlists?key={ENV_VARS['api_key']}&channelId={ENV_VARS['channel_id']}&part=snippet&maxResults=50&pageToken={playlists_page['nextPageToken']}")
        else:
            break
    
    channel_data['playlists'] = list()
    for playlist in playlists:
        # Vind video ids van playlist
        playlist['videoIds'] = find_playlist_video_ids(playlist['id'])
        # Sla playlist op
        channel_data['playlists'].append(playlist)

    # --- Opname van videos: uploads -------------------------------------------------------
    uploads_video_ids = find_playlist_video_ids(channel_data['uploadsPlaylistId'])
    uploaded_videos = dict()
    for video_id in uploads_video_ids:
        # Vind videodata op basis van video id
        video_data = get_video_data(video_id)
        if video_data == None: continue

        # Sla de videodata op onder het juiste schooljaar
        school_year = video_data['publishSchoolYear']
        if school_year not in uploaded_videos:
            uploaded_videos[school_year] = list()
        uploaded_videos[school_year].append(video_data)
        
    channel_data['uploadedVideos'] = uploaded_videos
    print("Failed video count: " + str(failed_video_count))

    # --- Registratie van jaren waarin er is geüpload -------------------------------------------------------
    channel_data['publishSchoolYears'] = sorted(seen_publish_school_years, reverse=True)

    # --- Genereer info over OINC voor gebruikers zonder JavaScript -------------------------------------------------------
    links_html = f"<!DOCTYPE html>\n<html>\n<head>\n<title>Korte info over oinc</title>\n</head>\n<body>\n<li>Ons kanaal: <a href=\"https://youtube.com/channel/{ENV_VARS['channel_id']}\" target=\"_blank\" aria-label=\"Ons kanaal\">klik</a></li>\n"
    for link in social_links:
        links_html += f"<li>{link['name']}: <a href=\"{link['url']}\" target=\"_blank\" aria-label=\"{link['name']}\">klik</a></li>\n"
    links_html += f"<br>\n<p style=\"white-space: pre-wrap;\">\n{channel_data['description']}\n</p>\n<style>\nbody{{background: black; color: lightgray;}}\na{{color: lightblue; border: 2px solid transparent;}}\n:focus,:target{{border: 2px dotted white;}}\np{{color: rgb(191, 250, 114);}}\n</style>\n</body>\n</html>"

    # --- Opslaan van data -------------------------------------------------------
    if ospath.isdir(cd + '/../dist'):
        f = open(cd + "/../dist/channeldata.json", "w+")
        json.dump(channel_data, f, indent = 4)
        f.close()
        f = open(cd + "/../dist/videopaths.json", "w+")
        json.dump(video_paths, f, indent = 4)
        f.close()

        f = open(cd + "/../dist/links.html", "w+")
        f.write(links_html)
        f.close()
        
    f = open(cd + "/../public/channeldata.json", "w+")
    json.dump(channel_data, f, indent = 4)
    f.close()
    f = open(cd + "/../public/videopaths.json", "w+")
    json.dump(video_paths, f, indent = 4)
    f.close()

    f = open(cd + "/../public/links.html", "w+")
    f.write(links_html)
    f.close()


    # --- Commit naar Github -------------------------------------------------------
    # commit_msg = '🚀 Automatische vernieuwing van website (' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ')'
    # runcmd("npm run build")
    # runcmd(f"git remote set-url origin https://{ENV_VARS['access_token']}@github.com/{ENV_VARS['username']}/{ENV_VARS['username']}.github.io.git/")
    # runcmd(f"git config user.email {ENV_VARS['email']}")
    # runcmd(f"git config user.name {ENV_VARS['username']}")
    # runcmd("cd dist")
    # runcmd("git init")
    # runcmd("git add data.json")
    # runcmd(f"git commit -m \"{commit_msg}\"")
    # runcmd(f"git push -f git@github.com:{ENV_VARS['username']}/{ENV_VARS['username']}.github.io.git main:gh-pages")

if __name__ == "__main__":
    main()