#!/usr/bin/env python3
import json
import re
import urllib.request
import urllib.parse
import sys
import os
try:
    import yaml
except ImportError:
    print("Module 'yaml' not found.")

def main(env):
    global failed_video_count, overons_url, isTrailerThumbCached, instagram_media_urls

    if env == 'dev':
        print("Launching in devolpment environment...")

        # Laad omgevingsvariabelen
        with open('env_vars.yaml', 'r') as f:
            ENV_VARS = yaml.safe_load(f)
    else:
        print("Launching in auto-update mode...")

        # Laad omgevingsvariabelen
        ENV_VARS = {
            'google_api_key': os.environ.get('google_api_key'),
            'youtube_channel_id': os.environ.get('youtube_channel_id'),
            'instagram_access_token': os.environ.get('instagram_access_token'),
            'site_base_url': os.environ.get('site_base_url')
        }
    
    # --- Initialisatie variabelen -------------------------------------------------------
    channel_data = dict()
    instagram_data = dict()
    video_paths = dict()

    failed_video_count = 0
    isTrailerThumbCached = False

    CHANNEL_URL = f"https://youtube.com/channel/{ENV_VARS['youtube_channel_id']}"
    REQUEST_HEADER = {
      'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) ' 
      'AppleWebKit/537.11 (KHTML, like Gecko) '
      'Chrome/23.0.1271.64 Safari/537.11',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
      'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
      'Accept-Encoding': 'none',
      'Accept-Language': 'en-US,en;q=0.8',
      'Connection': 'keep-alive'
    }
    seen_publish_school_years = []
    overons_url = ''
    instagram_media_urls = dict()

    # --- Algemene data van het kanaal -------------------------------------------------------
    # Divers
    print('Fetching generic channel info...')
    general_channel_data_request = urllib.request.urlopen(f"https://www.googleapis.com/youtube/v3/channels?key={ENV_VARS['google_api_key']}&id={ENV_VARS['youtube_channel_id']}&part=snippet,brandingSettings,statistics,contentDetails")
    general_channel_data = json.loads(general_channel_data_request.read())['items'][0]
    channel_data['title'] = general_channel_data['snippet']['title']
    channel_data['description'] = general_channel_data['snippet']['description'].replace('\r', '')
    channel_data['logo'] = general_channel_data['snippet']['thumbnails']['medium']['url']
    channel_data['banner'] = general_channel_data['brandingSettings']['image']['bannerExternalUrl'].replace('lh3.googleusercontent.com', 'yt3.ggpht.com')  + "=w1707"
    channel_data['trailer'] = general_channel_data['brandingSettings']['channel']['unsubscribedTrailer']
    channel_data['statistics'] = general_channel_data['statistics']
    channel_data['uploadsPlaylistId'] = general_channel_data['contentDetails']['relatedPlaylists']['uploads']

    # --- (Sociale media)links op het kanaal -------------------------------------------------------
    print(f"Fetching links from channel at {CHANNEL_URL}")

    # Neem data op
    html = urllib.request.urlopen(CHANNEL_URL).read().decode('utf-8')
    header_links = json.loads('{' + re.findall(r"\"headerLinks(?:(?!,\"subscribeButton\").)*", html)[0] + '}')['headerLinks']['channelHeaderLinksRenderer']
    print("  Data found")

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
        print(f"  Added link '{link['title']['simpleText']}' with location '{name}' ('{url}')")

    # Voeg link naar kanaal toe
    channel_link = {
        'url': CHANNEL_URL,
        'name': 'youtube',
        'title': 'YouTube',
        'iconAvailable': True
    }
    if social_links[0]['name'] == 'olva':
        social_links.append(channel_link)
    else:
        social_links.insert(0, channel_link)
    print(f"  Added channel link 'YouTube' with location 'youtube' ('{CHANNEL_URL}')")

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
        global failed_video_count, overons_url, isTrailerThumbCached

        videodata = urllib.request.urlopen(f"https://www.googleapis.com/youtube/v3/videos?key={ENV_VARS['google_api_key']}&id={video_id}&part=snippet,contentDetails,statistics")
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

            # Sla link van trailer thumbnail op
            if channel_data['trailer'] == video_id and not isTrailerThumbCached:
                overons_url = thumb_maxres_url

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

            print(f"  Analysed video '{video_title}' (id: '{video_id}', path: '{video_path}', thumbmaxres_type: {thumbmaxres_type})")
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
        playlist_page_request = urllib.request.urlopen(f"https://www.googleapis.com/youtube/v3/playlistItems?key={ENV_VARS['google_api_key']}&playlistId={playlist_id}&part=contentDetails&maxResults=50")
        while True:
            playlist_page = json.loads(playlist_page_request.read())
            for playlist_item in playlist_page['items']:
                playlist_video_ids.append(playlist_item['contentDetails']['videoId'])
            if 'nextPageToken' in playlist_page:
                playlist_page_request = urllib.request.urlopen(f"https://www.googleapis.com/youtube/v3/playlistItems?key={ENV_VARS['google_api_key']}&playlistId={playlist_id}&part=contentDetails&maxResults=50&pageToken={playlist_page['nextPageToken']}")
            else:
                break
        return playlist_video_ids

    # Vind alle afspeellijsten
    print("Fetching playlists...")
    playlists = list()
    playlists_page_request = urllib.request.urlopen(f"https://www.googleapis.com/youtube/v3/playlists?key={ENV_VARS['google_api_key']}&channelId={ENV_VARS['youtube_channel_id']}&part=snippet&maxResults=50")
    playlists_page = json.loads(playlists_page_request.read())
    while True:
        for playlist in playlists_page['items']:
            playlists.append({
                'id': playlist['id'],
                'title': playlist['snippet']['title'],
                'description': playlist['snippet']['description']
            })
            print(f"  Found playlist '{playlist['snippet']['title']}' (id: '{playlist['id']}')")
        if 'nextPageToken' in playlists_page:
            playlists_page = urllib.request.urlopen(f"https://www.googleapis.com/youtube/v3/playlists?key={ENV_VARS['google_api_key']}&channelId={ENV_VARS['youtube_channel_id']}&part=snippet&maxResults=50&pageToken={playlists_page['nextPageToken']}")
        else:
            break
    
    channel_data['playlists'] = list()
    for playlist in playlists:
        # Vind video ids van playlist
        playlist['videoIds'] = find_playlist_video_ids(playlist['id'])
        # Sla playlist op
        channel_data['playlists'].append(playlist)

    # --- Opname van videos: uploads -------------------------------------------------------
    print("Fetching uploads...")
    uploads_video_ids = find_playlist_video_ids(channel_data['uploadsPlaylistId'])
    print(f"Found {len(uploads_video_ids)} videos...")
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
    if overons_url == '':
        print("[!!] Warning: channel trailer was not found and thus overons.jpg couldn't be generated!")

    # --- Registratie van jaren waarin er is geüpload -------------------------------------------------------
    channel_data['publishSchoolYears'] = sorted(seen_publish_school_years, reverse=True)

    # --- Opname Instagram data: algemene functies -------------------------------------------------------
    # Functie om de ids te vinden van elke post
    def find_instagram_media_ids():
        media_ids = list()
        media_request = urllib.request.urlopen(f"https://graph.instagram.com/me/media?access_token={ENV_VARS['instagram_access_token']}")
        while True:
            media_page = json.loads(media_request.read())
            for media_item in media_page['data']:
                media_ids.append(media_item['id'])
            if 'paging' in media_page and 'next' in media_page['paging']:
                media_request = urllib.request.urlopen(media_page['paging']['next'])
            else:
                break
        return media_ids

    # Functie voor het verwerken van Instagram post data
    def get_instagram_post_data(media_id):
        # Request
        media_request = urllib.request.Request(f"https://graph.instagram.com/{media_id}/?access_token={ENV_VARS['instagram_access_token']}&fields=caption,media_type,media_url,thumbnail_url,permalink,timestamp", None, REQUEST_HEADER)
        media_data = json.loads(urllib.request.urlopen(media_request).read())

        # Sla afbeelding(en) op
        if media_data['media_type'] == 'VIDEO':
            instagram_media_urls[str(media_id)] = media_data['thumbnail_url']
        else:
            instagram_media_urls[str(media_id)] = media_data['media_url']
        
        # Bekijk als de post een caption heeft
        if 'caption' in media_data:
            caption = media_data['caption']
        else:
            caption = ''

        # Return
        return {
            'id': media_id,
            'media_type': media_data['media_type'],
            'caption': caption,
            'thumb': media_data['media_url'],
            'permalink': media_data['permalink'],
            'timestamp': media_data['timestamp']
        }

    # --- Opname Instagram data: algemene data -------------------------------------------------------
    instagram_data_request = urllib.request.urlopen(f"https://graph.instagram.com/me?access_token={ENV_VARS['instagram_access_token']}&fields=media_count,username")
    instagram_data = json.loads(instagram_data_request.read())
    print(f"Fetched general Instagram data, found {instagram_data['media_count']} posts")

    # --- Opname Instagram data: posts -------------------------------------------------------
    instagram_data['posts'] = list()
    instagram_media_ids = find_instagram_media_ids()
    print("Fetched Instagram media ids list")
    print("Fetching post data...")
    for media_id in instagram_media_ids:
        media_data = get_instagram_post_data(media_id)
        print(f"  Analysing post {media_id} with caption \"{media_data['caption'][:20]}...\" (type: {media_data['media_type']})")
        instagram_data['posts'].append(media_data)

    # --- Genereer info over OINC voor gebruikers zonder JavaScript -------------------------------------------------------
    links_html = f"<!DOCTYPE html>\n<html>\n<head>\n<title>Korte info over oinc</title>\n</head>\n<body>\n<li>Ons kanaal: <a href=\"https://youtube.com/channel/{ENV_VARS['youtube_channel_id']}\" target=\"_blank\" aria-label=\"Ons kanaal\">klik</a></li>\n"
    for link in social_links:
        links_html += f"<li>{link['name']}: <a href=\"{link['url']}\" target=\"_blank\" aria-label=\"{link['name']}\">klik</a></li>\n"
    links_html += f"<br>\n<p style=\"white-space: pre-wrap;\">\n{channel_data['description']}\n</p>\n<style>\nbody{{background: black; color: lightgray;}}\na{{color: lightblue; border: 2px solid transparent;}}\n:focus,:target{{border: 2px dotted white;}}\np{{color: rgb(191, 250, 114);}}\n</style>\n</body>\n</html>"
    print("Generated links.html")

    # --- Genereer sitemap -------------------------------------------------------
    print("Generating sitemap...")
    # Functie om URL van site om te vormen naar bruikbare URL
    def encodeSiteURL(url):
        if url == '/':
            newUrl = ENV_VARS['site_base_url']
        else:
            newUrl = ENV_VARS['site_base_url'] + '/?' + url
        print(f"  Added {newUrl}")
        return newUrl 

    # Sitemap
    sitemap_links = [
        encodeSiteURL('/'),
        encodeSiteURL('/over-ons'),
        encodeSiteURL('/videos')
    ]
    for school_year in uploaded_videos:
        for video in uploaded_videos[school_year]:
            sitemap_links.append(encodeSiteURL('/videos/' + video['id'] + '/' + video['videoPath']))

    # --- Opslaan van data -------------------------------------------------------
    def createDirIfNotExists(dirRel):
        dirAbs = os.path.abspath(dirRel)
        if not os.path.exists(dirAbs):
            os.makedirs(dirAbs)
            print(f"  Created new directory: {dirAbs}")

    def saveLocalJSON(pathRel, data):
        pathAbs = os.path.abspath(pathRel)
        f = open(pathAbs, "w+")
        json.dump(data, f, indent = 4)
        f.close()
        logSave(pathRel.split('/')[-1], pathAbs)

    def saveLocalText(pathRel, text):
        pathAbs = os.path.abspath(pathRel)
        f = open(pathAbs, "w+")
        f.write(text)
        f.close()
        logSave(pathRel.split('/')[-1], pathAbs)

    def saveRemoteJpg(url, pathRel):
        pathAbs = os.path.abspath(pathRel)
        urllib.request.urlretrieve(url, pathAbs)
        logSave(pathRel.split('/')[-1], pathAbs)

    def logSave(title, path):
        print(f"  Saved {title} to {path}")

    print("Saving general data...")
    if env == 'dev':
        print("  - Saving to 'public' folder -")

        # Maak bestandstructuur als deze nog niet bestaat
        createDirIfNotExists('../public')
        createDirIfNotExists('../public/generated')
        createDirIfNotExists('../public/generated/data')
        createDirIfNotExists('../public/generated/img')
        createDirIfNotExists('../public/generated/img/web')
        createDirIfNotExists('../public/generated/img/instagram')

        # Sla alles op
        saveLocalJSON("../public/generated/data/channeldata.json", channel_data)
        saveLocalJSON("../public/generated/data/videopaths.json", video_paths)
        saveLocalText("../public/generated/links.html", links_html)
        saveLocalText("../public/generated/sitemap.txt", '\n'.join(sitemap_links))

        saveRemoteJpg(channel_data['logo'], "../public/generated/img/web/logo_youtube.jpg")
        saveRemoteJpg(channel_data['banner'], "../public/generated/img/web/banner_youtube.jpg")
        if overons_url != '': saveRemoteJpg(overons_url, "../public/generated/img/web/overons.jpg")

        if os.path.isdir(os.path.abspath('../dist')):
            print("  - Saving to 'dist' folder -")

            # Maak bestandstructuur als deze nog niet bestaat
            createDirIfNotExists('../dist')
            createDirIfNotExists('../dist/generated')
            createDirIfNotExists('../dist/generated/data')
            createDirIfNotExists('../dist/generated/img')
            createDirIfNotExists('../dist/generated/img/web')
            createDirIfNotExists('../dist/generated/img/instagram')

            # Sla alles op
            saveLocalJSON("../dist/generated/data/channeldata.json", channel_data)
            saveLocalJSON("../dist/generated/data/videopaths.json", video_paths)
            saveLocalText("../dist/generated/links.html", links_html)
            saveLocalText("../dist/generated/sitemap.txt", '\n'.join(sitemap_links))

            saveRemoteJpg(channel_data['logo'], "../dist/generated/img/web/logo_youtube.jpg")
            saveRemoteJpg(channel_data['banner'], "../dist/generated/img/web/banner_youtube.jpg")
            if overons_url != '': saveRemoteJpg(overons_url, "../dist/generated/img/web/overons.jpg")

        print("Saving Instagram media...")
        for media_id, url in instagram_media_urls.items():
            saveRemoteJpg(url, f"../public/generated/img/instagram/{media_id}.jpg")
            if os.path.isdir(os.path.abspath('../dist')):
                saveRemoteJpg(url, f"../dist/generated/img/instagram/{media_id}.jpg")

    else:
        print("  - Saving to root folder -")

        # Maak bestandstructuur als deze nog niet bestaat
        createDirIfNotExists('generated')
        createDirIfNotExists('generated/data')
        createDirIfNotExists('generated/img')
        createDirIfNotExists('generated/img/web')
        createDirIfNotExists('generated/img/instagram')

        # Sla alles op
        saveLocalJSON("generated/data/channeldata.json", channel_data)
        saveLocalJSON("generated/data/videopaths.json", video_paths)
        saveLocalText("generated/links.html", links_html)
        saveLocalText("generated/sitemap.txt", '\n'.join(sitemap_links))

        saveRemoteJpg(channel_data['logo'], "generated/img/web/logo_youtube.jpg")
        saveRemoteJpg(channel_data['banner'], "generated/img/web/banner_youtube.jpg")
        if overons_url != '': saveRemoteJpg(overons_url, "generated/img/web/overons.jpg")
        
        print("Saving Instagram media...")
        for media_id, url in instagram_media_urls.items():
            saveRemoteJpg(url, f"generated/img/instagram/{media_id}.jpg")

    print("Done!")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Invalid amount of parameters given. Expected one argument ("dev" or "auto").')
    else:
        env = sys.argv[1]
        if env == 'dev':
            if 'yaml' in sys.modules:
                main('dev')
            else:
                print("Because the module 'yaml' could not be found, this script is unable to proceed. Please make sure to have this module installed.")
        elif env == 'auto':
            main('auto')
        else:
            print('Please provide an argument with either "dev" or "auto"')