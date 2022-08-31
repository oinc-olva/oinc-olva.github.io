#!/usr/bin/env python3
import json
import re
import urllib.request
import urllib.parse
import urllib.error
import sys
import os
import io
from PIL import Image
try:
    import yaml
except ImportError:
    print("Module 'yaml' not found.")

def main(env):
    global failed_video_count, overons_url, isTrailerThumbCached, instagram_image_urls, instagram_video_urls, instagram_requests_left

    if env == 'dev':
        print("Launching in devolpment environment...")

        # Zet locatie
        os.chdir(os.path.dirname(os.path.abspath(__file__)))

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
    overons_url = ''
    instagram_image_urls = dict()
    instagram_video_urls = dict()
    instagram_flagged_for_deletion = list()
    instagram_requests_left = 240

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
    def translate_video_date(date):
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

            # Vind thumbnails
            thumbnails = videodata['snippet']['thumbnails']

            # Kijk als het webp-formaat ondersteund is voor de thumbnail van de video
            isWebpSupported = False
            try:
                req = urllib.request.urlopen(f"https://i.ytimg.com/vi_webp/{video_id}/mqdefault.webp")
            except urllib.error.HTTPError as e:
                pass
            except urllib.error.URLError as e:
                print(f"[Error] A URLError occured while fetching URL https://i.ytimg.com/vi_webp/{video_id}/mqdefault.webp: {e.reason}")
            else:
                isWebpSupported = True

            # Vind de meest kwalitatieve thumbnail
            if 'maxres' in thumbnails:
                thumbmaxres_type = 4
                thumb_maxres_url = f"https://i.ytimg.com/vi_webp/{video_id}/maxresdefault.webp" if isWebpSupported else thumbnails['maxres']['url']
            elif 'standard' in thumbnails:
                thumbmaxres_type = 3
                thumb_maxres_url = f"https://i.ytimg.com/vi_webp/{video_id}/sddefault.webp" if isWebpSupported else thumbnails['standard']['url']
            elif 'high' in thumbnails:
                thumbmaxres_type = 2
                thumb_maxres_url = f"https://i.ytimg.com/vi_webp/{video_id}/hqdefault.webp" if isWebpSupported else thumbnails['high']['url']
            elif 'medium' in thumbnails:
                thumbmaxres_type = 1
                thumb_maxres_url = f"https://i.ytimg.com/vi_webp/{video_id}/mqdefault.webp" if isWebpSupported else thumbnails['medium']['url']
            else:
                thumbmaxres_type = 0
                thumb_maxres_url = f"https://i.ytimg.com/vi_webp/{video_id}/default.webp" if isWebpSupported else thumbnails['default']['url']

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

            print(f"  Analysed video '{video_title}' (id: '{video_id}', path: '{video_path}', thumbmaxres_type: {thumbmaxres_type}, isWebpSupported: {isWebpSupported})")
            return {
                'id': video_id,
                'title': video_title,
                'description': videodata['snippet']['description'],
                'durationSec': video_duration_sec,
                'durationFormatted': ':'.join(video_duration_partsStr),
                'durationFormattedParts': len(video_duration_partsStr),
                'durationTranslated': ' '.join(video_duration_translated_parts),
                'publishDate': translate_video_date(publish_date),
                'publishSchoolYear': get_school_year(publish_date),
                'publishYear': publish_date[:4],
                'views': videodata['statistics']['viewCount'],
                'thumb': f"https://i.ytimg.com/vi_webp/{video_id}/mqdefault.webp" if isWebpSupported else thumbnails['medium']['url'],
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
                'description': playlist['snippet']['description'],
                'videoIds': find_playlist_video_ids(playlist['id'])
            })
            print(f"  Found playlist '{playlist['snippet']['title']}' (id: '{playlist['id']}')")
        if 'nextPageToken' in playlists_page:
            playlists_page = urllib.request.urlopen(f"https://www.googleapis.com/youtube/v3/playlists?key={ENV_VARS['google_api_key']}&channelId={ENV_VARS['youtube_channel_id']}&part=snippet&maxResults=50&pageToken={playlists_page['nextPageToken']}")
        else:
            break
    channel_data['playlists'] = playlists

    # --- Opname van videos: uploads -------------------------------------------------------
    print("Fetching uploads...")
    uploads_video_ids = find_playlist_video_ids(channel_data['uploadsPlaylistId'])
    print(f"Found {len(uploads_video_ids)} videos...")

    videos = {
        'order': list(),
        'values': dict()
    }
    school_years = {
        'order': list(),
        'values': dict()
    }
    for video_id in uploads_video_ids:
        # Vind videodata op basis van video id
        video_data = get_video_data(video_id)
        if video_data == None: continue

        # Sla video op
        videos['order'].append(video_id)
        videos['values'][video_id] = video_data

        # Plaats video onder het juiste schooljaar
        school_year = video_data['publishSchoolYear']
        if school_year not in school_years['order']:
            school_years['values'][school_year] = list()
            school_years['order'].append(school_year)
        school_years['values'][school_year].append(video_id)

    channel_data['schoolYears'] = school_years
    channel_data['videos'] = videos
    print("Failed video count: " + str(failed_video_count))
    if overons_url == '':
        print("[!!] Warning: channel trailer was not found and thus overons.jpg couldn't be generated!")

    # --- Hernieuw Instagram gebruikerstoken -------------------------------------------------------
    print("Reloading Instagram user token...")
    try:
        instagram_token_renew_request = urllib.request.urlopen(f"https://graph.instagram.com/refresh_access_token?grant_type=ig_refresh_token&access_token={ENV_VARS['instagram_access_token']}")
        instagram_requests_left -= 1
    except:
        print('  Failed!')
    else:
        print('  Success!')

    # --- Opname Instagram data: algemene functies -------------------------------------------------------
    # Functie om de datum te vinden van een post
    def translate_instagram_date(timestamp):
        MAANDEN = ['januari', 'februari', 'maart', 'april', 'mei', 'juni', 'juli', 'augustus', 'september', 'oktober', 'november', 'december']
        
        year = timestamp[:4]
        month  = int(timestamp[5:7])
        day = int(timestamp[8:10])
        
        return str(day) + ' ' + MAANDEN[month - 1] + ' ' + year

    # Functie om de nieuwe ids te vinden van elke post
    def find_new_instagram_media_ids(first_page):
        global instagram_requests_left
        media_ids = list()
        if first_page == None:
            media_request = urllib.request.urlopen(f"https://graph.instagram.com/me/media?access_token={ENV_VARS['instagram_access_token']}")
            instagram_requests_left -= 1
            media_page = json.loads(media_request.read())
        else:
            media_page = first_page

        while True:
            for media_item in media_page['data']:
                media_ids.append(media_item['id'])
            if 'paging' in media_page and 'next' in media_page['paging']:
                media_request = urllib.request.urlopen(media_page['paging']['next'])
                media_page = json.loads(media_request.read())
            else:
                break
        return media_ids

    # Functie om de oude ids te vinden van elke post
    def find_old_instagram_media_ids():
        old_ids = list()
        for media in instagram_data['posts']:
            old_ids.append(media['id'])
        return old_ids

    # Functie voor het verwerken van Instagram post data
    def get_new_instagram_post_data(media_id):
        global instagram_requests_left
        # Error als geen requests over
        if instagram_requests_left < 10: return False

        # Request
        media_request = urllib.request.Request(f"https://graph.instagram.com/{media_id}/?access_token={ENV_VARS['instagram_access_token']}&fields=caption,media_type,media_url,thumbnail_url,permalink,timestamp", None, REQUEST_HEADER)
        instagram_requests_left -= 1
        media_data = json.loads(urllib.request.urlopen(media_request).read())

        # Sla afbeelding(en) op
        media_children = None
        media_url = None
        media_thumb = None

        if media_data['media_type'] == 'VIDEO': # Video
            instagram_image_urls[f"{str(media_id)}.webp"] = media_data['thumbnail_url']
            instagram_video_urls[f"{str(media_id)}.mp4"] = media_data['media_url']
            media_url = f"/generated/img/instagram/{media_id}.mp4"
            media_thumb = f"/generated/img/instagram/{media_id}.webp"

        elif media_data['media_type'] == 'IMAGE': # Afbeelding
            instagram_image_urls[f"{str(media_id)}.webp"] = media_data['media_url']
            media_url = f"/generated/img/instagram/{media_id}.webp"
            media_thumb = f"/generated/img/instagram/{media_id}.webp"
            
        else: # Album
            media_children_request = urllib.request.Request(f"https://graph.instagram.com/{media_id}/children/?access_token={ENV_VARS['instagram_access_token']}&fields=media_url,media_type,thumbnail_url", None, REQUEST_HEADER)
            instagram_requests_left -= 1
            media_children_data = json.loads(urllib.request.urlopen(media_children_request).read())['data']

            media_children = list()
            for child in media_children_data:
                if child['media_type'] == 'VIDEO':
                    instagram_video_urls[f"{child['id']}.mp4"] = child['media_url']
                    instagram_image_urls[f"{child['id']}.webp"] = child['thumbnail_url'] # Elke .jpg thumbnail wordt later gedownload en omgezet naar .webp

                    media_children.append({
                        'id': child['id'],
                        'media_url': f"/generated/img/instagram/{child['id']}.mp4",
                        'thumb': f"/generated/img/instagram/{child['id']}.webp",
                        'media_type': 'VIDEO'
                    })
                else:
                    instagram_image_urls[f"{child['id']}.webp"] = child['media_url'] # Elke .jpg afbeelding wordt later gedownload en omgezet naar .webp

                    media_children.append({
                        'id': child['id'],
                        'media_url': f"/generated/img/instagram/{child['id']}.webp",
                        'media_type': 'IMAGE'
                    })

            # Zet thumbnail voor album
            if media_children[0]['media_type'] == 'VIDEO':
                media_thumb = media_children[0]['thumb']
            else:
                media_thumb = media_children[0]['media_url']

        # Return
        return {
            'id': media_id,
            'media_type': media_data['media_type'],
            'caption': media_data.get('caption', ''),
            'thumb': media_thumb,
            'media_url': media_url,
            'permalink': media_data['permalink'],
            'timestamp': media_data['timestamp'],
            'date': translate_instagram_date(media_data['timestamp']),
            'children': media_children
        }

    # Functie voor het updaten van instagram data
    def set_instagram_changes(old_media_ids, new_media_ids):
        # Bereken verwijderingen en toevoegingen
        old_media_ids_set = set(old_media_ids)
        new_media_ids_set = set(new_media_ids)
        deletions = list(old_media_ids_set - new_media_ids_set)
        additions = list(new_media_ids_set - old_media_ids_set)
        print("Changes in Instagram data found:")

        # Verwijder afbeeldingen van oudere posts
        for deletion in deletions:
            # Vind index in instagram_data
            deletion_index = -1
            for post in instagram_data['posts']:
                if post['id'] == deletion:
                    deletion_index = instagram_data['posts'].index(post)
                    break

            # Vind type van post
            deletion_type = instagram_data['posts'][deletion_index]['media_type']

            # Markeer om te verwijderen
            print(f"  Flagged post {deletion} ({deletion_type}) for deletion")
            if deletion_type == 'VIDEO':
                instagram_flagged_for_deletion.append(deletion + '.mp4')
                instagram_flagged_for_deletion.append(deletion + '.webp')
            elif deletion_type == 'IMAGE':
                instagram_flagged_for_deletion.append(deletion + '.webp')
            else:
                for child in instagram_data['posts'][deletion_index]['children']:
                    instagram_flagged_for_deletion.append(child['media_url'][25:])
                    if child['media_type'] == 'VIDEO': instagram_flagged_for_deletion.append(child['thumb'][25:])
                    print(f"    Flagged child id {child['id']} for deletion")

        # Verwijder data van oudere posts
        i = 0
        while i < len(instagram_data['posts']):
            if instagram_data['posts'][i]['id'] in deletions:
                del instagram_data['posts'][i]
                print(f"  Deleted data of post {post['id']} ({post['media_type']})")
            else:
                i += 1
        
        # Voeg nieuwe posts toe
        new_media_ids.reverse()
        for media_id in new_media_ids:
            # Sla over als post niet nieuw is
            if media_id not in additions: continue
            # Vraag data van post op
            instagram_new_post_data = get_new_instagram_post_data(media_id)
            if instagram_new_post_data == None: # Eindig loop als geen requests meer over
                print(f"  Tried to add new post {media_id}, but there are no requests left to use... Aborting addition script!")
                break
            # Voeg post toe aan data
            instagram_data['posts'].insert(0, instagram_new_post_data)
            print(f"  Added new post {media_id} ({instagram_new_post_data['media_type']}) with caption \"{instagram_new_post_data['caption'][:20]}...\"")

    # --- Opname Instagram data: algemene data -------------------------------------------------------
    # Vraag algemene data op van instagram.com
    instagram_general_data_request = urllib.request.urlopen(f"https://graph.instagram.com/me?access_token={ENV_VARS['instagram_access_token']}&fields=media_count,username")
    instagram_requests_left -= 1
    instagram_general_data = json.loads(instagram_general_data_request.read())

    # Laad vorige instagram data
    instagram_data_request = urllib.request.urlopen("https://raw.githubusercontent.com/oinc-olva/oinc-olva.github.io/gh-pages/generated/data/instagram.json")
    instagram_data = json.loads(instagram_data_request.read())

    # Log
    print(f"Fetched general new and old Instagram data, found {instagram_general_data['media_count']} posts (previously {instagram_data['media_count']})")

    # --- Opname Instagram data: posts ------------------------------------------------------
    if instagram_general_data['media_count'] == instagram_data['media_count']:
        # - Als geen verschil in hoeveelheid posts, kijk als de eerste post dezelfde is -
        # Vind id van eerste post
        media_page_request = urllib.request.urlopen(f"https://graph.instagram.com/me/media?access_token={ENV_VARS['instagram_access_token']}")
        instagram_requests_left -= 1
        media_page = json.loads(media_page_request.read())

        # Vergelijk
        if len(media_page['data']) == 0:
            # Als nieuwe data leeg is, dan is er geen enkele post meer op het account --> Alle post data verwijderen
            instagram_old_media_ids = find_old_instagram_media_ids()
            set_instagram_changes(instagram_old_media_ids, list())
        elif len(instagram_data['posts']) == 0 or media_page['data'][0]['id'] != instagram_data['posts'][0]['id']:
            # Als niet gelijk, dan is er minstens één post verwijderd en één toegevoegd --> Volledige scan nodig!
            instagram_old_media_ids = find_old_instagram_media_ids()
            instagram_new_media_ids = find_new_instagram_media_ids(media_page)
            set_instagram_changes(instagram_old_media_ids, instagram_new_media_ids)
        else:
            print('Instagram data is already up-to-date!')
    
    else:
        # - Als verschil in hoeveelheid posts, dan zijn er posts toegevoegd/verwijderd -
        # Een volledige scan is nodig!
        instagram_old_media_ids = find_old_instagram_media_ids()
        instagram_new_media_ids = find_new_instagram_media_ids(None)
        set_instagram_changes(instagram_old_media_ids, instagram_new_media_ids)

    # Pas enkele waarden aan
    instagram_data['username'] = instagram_general_data['username']
    instagram_data['id'] = instagram_general_data['id']
    instagram_data['media_count'] = instagram_general_data['media_count']

    # --- Genereer info over OINC voor gebruikers zonder JavaScript -------------------------------------------------------
    links_html = f"<!DOCTYPE html>\n<html>\n<head>\n<title>Korte info over oinc</title>\n</head>\n<body>\n<li>Ons kanaal: <a href=\"https://youtube.com/channel/{ENV_VARS['youtube_channel_id']}\" target=\"_blank\" aria-label=\"Ons kanaal\">klik</a></li>\n"
    for link in social_links:
        links_html += f"<li>{link['name']}: <a href=\"{link['url']}\" target=\"_blank\" aria-label=\"{link['name']}\">klik</a></li>\n"
    links_html += f"<br>\n<p style=\"white-space: pre-wrap;\">\n{channel_data['description']}\n</p>\n<style>\nbody{{background: black; color: lightgray;}}\na{{color: lightblue; border: 2px solid transparent;}}\n:focus,:target{{outline: 2px solid #55c7e4;}}\np{{color: rgb(191, 250, 114);}}\n</style>\n</body>\n</html>"
    print("Generated links.html")

    # --- Genereer statische pagina's voor SEO: ALGEMEEN (SETUP) -------------------------------------------------------
    static_html_pages_params = dict()
    if env == 'dev':
        with open('static_page_preset.html', 'r') as f:
            static_html_page_preset = f.read()
    else:
        static_html_page_preset_request = urllib.request.urlopen('https://raw.githubusercontent.com/oinc-olva/oinc-olva.github.io/main/update/static_page_preset.html')
        static_html_page_preset = static_html_page_preset_request.read().decode("UTF-8")

    if env == 'dev':
        with open(os.path.abspath('../dist/htmlHeadTags.html'), 'r') as f:
            html_head_tags = f.read()
    else:
        with open('htmlHeadTags.html', 'r') as f:
            html_head_tags = f.read()

    # Genereer content header
    html_header = "<h2>Pagina's:</h2><ul>"
    pages = [
        {
            'title': 'Home',
            'path': '/'
        },
        {
            'title': 'Video\'s',
            'path': '/videos'
        },
        {
            'title': 'Over ons',
            'path': '/over-ons'
        }
    ]
    for page in pages:
        html_header += f"<li><a href=\"{page['path']}\">{page['title']}</a></li>"

    html_header += "</ul><h2>Uitgaande links:</h2><ul>"
    for social_link in channel_data['socialLinks']:
        html_header += f"<li><a href=\"{social_link['url']}\">{social_link['title']}</a></li>"
    html_header += "</ul>"

    # --- Genereer statische pagina's voor SEO: /over-ons -------------------------------------------------------
    static_html_pages_params['/over-ons'] = {
        'title': 'Over ons',
        'description': "Kom meer te weten over OINC!",
        'url': f"{ENV_VARS['site_base_url']}/over-ons",
        'image': f"{ENV_VARS['site_base_url']}/generated/img/web/overons.webp",
        'contentHTML': f"<h2>Over ons</h2><p id=\"preview-description\" style=\"margin-left:50px;\">{channel_data['description']}</p>"
    }
    # --- Genereer statische pagina's voor SEO: /videos -------------------------------------------------------
    # - Genereer HTML voor afspeellijsten -
    videos_playlists_html = ""
    for playlist in channel_data['playlists']:
        videos_playlists_html += f"<li><a href=\"/videos/{playlist['videoIds'][0]}/{video_paths[playlist['videoIds'][0]]['path']}?lijst={playlist['id']}\"><h3>{playlist['title']}</h3></a><p class=\"preview-playlists-description\">{playlist['description']}</p></li>"

    # - Genereer HTML voor video's -
    videos_videos_html = ""
    for school_year in channel_data['schoolYears']['order']:
        videos_videos_html += f"<li><h3>{school_year}</h3><ul>"
        for video_id in channel_data['schoolYears']['values'][school_year]:
            videos_videos_html += f"<li><a href=\"/videos/{video_id}/{video_paths[video_id]['path']}\"><h4>{channel_data['videos']['values'][video_id]['title']}</h4></a></li>"
        videos_videos_html += "</ul></li>"

    # - Sla variabelen op -
    static_html_pages_params['/videos'] = {
        'title': 'Video\'s',
        'description': "Bekijk onze gallerij aan video's!",
        'url': f"{ENV_VARS['site_base_url']}/videos",
        'image': f"{ENV_VARS['site_base_url']}/generated/img/web/banner_youtube.webp",
        'contentHTML': f"<h2>Afspeellijsten</h2><ul id=\"preview-playlists\">{videos_playlists_html}</ul><h2>Video's</h2><ul id=\"preview-videos\">{videos_videos_html}</ul>"
    }
    # --- Genereer statische pagina's voor SEO: /videos/:videoid/:videoPath, /v/:videoId -------------------------------------------------------
    for video_id, video_data in channel_data['videos']['values'].items():
        video_static_html_page_param = {
            'title': video_data['title'].replace('\\', '\\\\'),
            'description': video_data['description'].replace('\\', '\\\\').replace('\n', ' '),
            'url': f"{ENV_VARS['site_base_url']}/videos/{video_id}/{video_data['videoPath']}",
            'image': video_data['thumbmaxres'],
            'contentHTML': f"<h2>Videoinformatie:</h2><div id=\"preview-videoInfo\" style=\"margin-left:50px;\"><p id=\"preview-description\">{video_data['description']}</p><p id=\"preview-info\">{video_data['views']} weergaven | {video_data['publishDate']}</p><p id=\"preview-videoLink\">Link naar video: <a href=\"https://youtube.com/watch?v={video_id}\">https://youtube.com/watch?v={video_id}</a></p><p id=\"preview-shortVideoLink\">Korte link naar deze video: <a href=\"/v/{video_id}\">{ENV_VARS['site_base_url']}/v/{video_id}</a></p><a href=\"/videos\" id=\"preview-videos-link\">Bekijk onze videogallerij!</a></div>"
        }
        static_html_pages_params[f"/videos/{video_id}/{video_data['videoPath']}"] = video_static_html_page_param
        static_html_pages_params[f"/v/{video_id}"] = video_static_html_page_param

    # --- Genereer sitemap -------------------------------------------------------
    print("Generating sitemap...")
    # Functie om URL van site om te vormen naar bruikbare URL
    def encodeSiteURL(url):
        if url == '/':
            newUrl = ENV_VARS['site_base_url']
        else:
            newUrl = ENV_VARS['site_base_url'] + url + '/'
        print(f"  Added {newUrl}")
        return newUrl 

    # Sitemap
    sitemap_links = [
        encodeSiteURL('/'),
        encodeSiteURL('/over-ons'),
        encodeSiteURL('/videos')
    ]
    for video_id, video in videos['values'].items():
        sitemap_links.append(encodeSiteURL(f"/videos/{video_id}/{video['videoPath']}"))
        sitemap_links.append(encodeSiteURL(f"/v/{video_id}"))

    # --- Opslaan en verwijderen van data -------------------------------------------------------
    def delLocal(pathRel):
        pathAbs = os.path.abspath(pathRel)
        if os.path.exists(pathAbs):
            os.remove(pathAbs)
            logDel(pathRel.split('/')[-1], pathAbs)
        else:
            logDelFail(pathRel.split('/')[-1], pathAbs)

    def logDel(title, path):
        print(f"  Deleted file {title} at {path}")

    def logDelFail(title, path):
        print(f"  Tried to delete inexisting file {title} at {path}")

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

    def saveRemoteMedia(url, pathRel):
        pathAbs = os.path.abspath(pathRel)
        urllib.request.urlretrieve(url, pathAbs)
        logSave(pathRel.split('/')[-1], pathAbs)

    def convertJPGAndSaveAsWEBP(url, pathRel):
        pathAbs = os.path.abspath(pathRel)
        imagePath = io.BytesIO(urllib.request.urlopen(url).read())
        image = Image.open(imagePath)
        image.save(pathAbs, 'webp', optimize = True, quality = 80)
        logSave(pathRel.split('/')[-1], pathAbs + ' (conversion: JPG -> webp)')

    def logSave(title, path):
        print(f"  Saved {title} to {path}")

    # Sla alle gegenereerde HTML-pagina's op
    def saveGeneratedHTMLPages(pathRel, isSubstituteHeadTags):
        for page_rel_url, page_params in static_html_pages_params.items():
            # Genereer bestandstructuur
            rel_dir = ""
            for sub_dir in page_rel_url.split('/')[1:]:
                rel_dir = os.path.join(rel_dir, sub_dir).replace('\\', '/')
                createDirIfNotExists(os.path.join(pathRel, rel_dir))

            # Maak HTML
            html = static_html_page_preset.replace('$title', f"{page_params['title']} - OINC").replace('$description', page_params['description']).replace('$url', page_params['url']).replace('$image', page_params['image']).replace('$headerHTML', html_header).replace('$contentHTML', page_params['contentHTML'])
            if 'styling' in page_params:
                html = html.replace('$styling', f"<style>{page_params['styling']}</style>")
            else:
                html = html.replace('$styling', '')

            if isSubstituteHeadTags:
                html = html.replace('$headTags', html_head_tags)

            # Sla bestand op
            saveLocalText(os.path.join(pathRel, rel_dir, f"index{'.html.template' if pathRel == '../public' else '.html'}"), html)

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
        saveLocalJSON("../public/generated/data/instagram.json", instagram_data)
        saveLocalText("../public/generated/links.html", links_html)
        saveLocalText("../public/generated/sitemap.txt", '\n'.join(sitemap_links))

        convertJPGAndSaveAsWEBP(channel_data['logo'], "../public/generated/img/web/logo_youtube.webp")
        convertJPGAndSaveAsWEBP(channel_data['banner'], "../public/generated/img/web/banner_youtube.webp")
        if overons_url != '': convertJPGAndSaveAsWEBP(overons_url, "../public/generated/img/web/overons.webp")

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
            saveLocalJSON("../dist/generated/data/instagram.json", instagram_data)
            saveLocalText("../dist/generated/links.html", links_html)
            saveLocalText("../dist/generated/sitemap.txt", '\n'.join(sitemap_links))

            convertJPGAndSaveAsWEBP(channel_data['logo'], "../dist/generated/img/web/logo_youtube.webp")
            convertJPGAndSaveAsWEBP(channel_data['banner'], "../dist/generated/img/web/banner_youtube.webp")
            if overons_url != '': convertJPGAndSaveAsWEBP(overons_url, "../dist/generated/img/web/overons.webp")

        # Verwijder instagram post bestanden
        print("Deleting old Instagram media...")
        for instagram_media_file in instagram_flagged_for_deletion:
            delLocal(f"../public/generated/img/instagram/{instagram_media_file}")
            if os.path.isdir(os.path.abspath('../dist')):
                delLocal(f"../dist/generated/img/instagram/{instagram_media_file}")
        if len(instagram_flagged_for_deletion) == 0:
            print("  No media to remove!")
            
        # Sla nieuwe instagram post bestanden op
        print("Saving new Instagram media...")

        print("  - Saving video files -")
        if len(instagram_video_urls) == 0:
            print("  No video files to save!")
        else:
            for media_file, url in instagram_video_urls.items():
                saveRemoteMedia(url, f"../public/generated/img/instagram/{media_file}")
                if os.path.isdir(os.path.abspath('../dist')):
                    saveRemoteMedia(url, f"../dist/generated/img/instagram/{media_file}")

        print("  - Saving image files -")
        if len(instagram_image_urls) == 0:
            print("  No image files to save!")
        else:
            for media_file, url in instagram_image_urls.items():
                convertJPGAndSaveAsWEBP(url, f"../public/generated/img/instagram/{media_file}")
                if os.path.isdir(os.path.abspath('../dist')):
                    convertJPGAndSaveAsWEBP(url, f"../dist/generated/img/instagram/{media_file}")
        
        # Sla gegenereerde HTML-bestanden op
        print("Saving generated HTML pages...")
        saveGeneratedHTMLPages('../public', False)
        if os.path.isdir(os.path.abspath('../dist')):
            saveGeneratedHTMLPages('../dist', True)

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
        saveLocalJSON("generated/data/instagram.json", instagram_data)
        saveLocalText("generated/links.html", links_html)
        saveLocalText("generated/sitemap.txt", '\n'.join(sitemap_links))

        convertJPGAndSaveAsWEBP(channel_data['logo'], "generated/img/web/logo_youtube.webp")
        convertJPGAndSaveAsWEBP(channel_data['banner'], "generated/img/web/banner_youtube.webp")
        if overons_url != '': convertJPGAndSaveAsWEBP(overons_url, "generated/img/web/overons.webp")
        
        # Verwijder instagram post bestanden
        print("Deleting old Instagram media...")
        for instagram_media_file in instagram_flagged_for_deletion:
            delLocal(f"generated/img/instagram/{instagram_media_file}")
        if len(instagram_flagged_for_deletion) == 0:
            print("  No media to remove!")
            
        # Sla nieuwe instagram post bestanden op
        print("Saving new Instagram media...")

        print("  - Saving video files -")
        if len(instagram_video_urls) == 0:
            print("  No video files to save!")
        else:
            for media_file, url in instagram_video_urls.items():
                saveRemoteMedia(url, f"generated/img/instagram/{media_file}")

        print("  - Saving image files -")
        if len(instagram_image_urls) == 0:
            print("  No image files to save!")
        else:
            for media_file, url in instagram_image_urls.items():
                convertJPGAndSaveAsWEBP(url, f"generated/img/instagram/{media_file}")

        # Sla gegenereerde HTML-bestanden op
        print("Saving generated HTML pages...")
        saveGeneratedHTMLPages('', True)

    print(f"Done! ({instagram_requests_left} instagram requests left)")

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