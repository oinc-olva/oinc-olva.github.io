#!/usr/bin/env python3
import yaml
import json
import re
import urllib
from os import path as ospath
from os import system as runcmd
from time import gmtime, strftime
from pyyoutube import Api

def main():
    # Vind de locatie van dit script
    cd = ospath.dirname(__file__)

    # Laad omgevingsvariabelen
    with open('env_vars.yaml', 'r') as f:
        ENV_VARS = yaml.safe_load(f)
    
    # --- Initialisatie API data -------------------------------------------------------
    # Initialiseer APIs en enkele variabelen
    api = Api(api_key=ENV_VARS['api_key'])
    channel_data = dict()
    video_paths = dict()

    global failed_video_count
    failed_video_count = 0
    global isTrailerThumbCached
    isTrailerThumbCached = False

    seenPublishSchoolYears = []

    # --- Algemene API data -------------------------------------------------------
    # Divers
    general_channel_data = urllib.request.urlopen(f"https://www.googleapis.com/youtube/v3/channels?key={ENV_VARS['api_key']}&id={ENV_VARS['channel_id']}&part=snippet,brandingSettings,statistics,contentDetails")
    general_channel_data = json.loads(general_channel_data.read())['items'][0]
    channel_data['title'] = general_channel_data['snippet']['title']
    channel_data['description'] = general_channel_data['snippet']['description'].replace('\r', '')
    channel_data['logo'] = general_channel_data['snippet']['thumbnails']['medium']['url']
    channel_data['banner'] = general_channel_data['brandingSettings']['image']['bannerExternalUrl'].replace('lh3.googleusercontent.com', 'yt3.ggpht.com')
    channel_data['trailer'] = general_channel_data['brandingSettings']['channel']['unsubscribedTrailer']
    channel_data['statistics'] = general_channel_data['statistics']

    # Sla logo en banner op
    if ospath.isdir(cd + '/../dist'):
        urllib.request.urlretrieve(channel_data['logo'], cd + '/../dist/logo.jpg')
        urllib.request.urlretrieve(channel_data['banner'] + "=w1707", cd + '/../dist/banner.jpg')
    urllib.request.urlretrieve(channel_data['logo'], cd + '/../public/logo.jpg')
    urllib.request.urlretrieve(channel_data['banner'] + "=w1707", cd + '/../public/banner.jpg')

    # --- (Sociale media)links op het kanaal -------------------------------------------------------
    # Neem data op
    html = urllib.request.urlopen(f"https://youtube.com/channel/{ENV_VARS['channel_id']}").read().decode('utf-8')
    header_links = json.loads('{' + re.findall(r"\"headerLinks(?:(?!,\"subscribeButton\").)*", html)[0] + '}')['headerLinks']['channelHeaderLinksRenderer']

    social_links = list()
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
        if name == 'google' and subdomainsNum > 0:
            name += '-' + parts[subdomainsNum - 1]
        elif name == 'messenger':
            name = 'facebook-messenger'
        
        # Sla URL en naam op
        social_links.append({
            'url': url,
            'name': name
        })

    # Bekijk als Font Awesome iconen heeft voor de sociale mediakanalen
    header= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) ' 
      'AppleWebKit/537.11 (KHTML, like Gecko) '
      'Chrome/23.0.1271.64 Safari/537.11',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
      'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
      'Accept-Encoding': 'none',
      'Accept-Language': 'en-US,en;q=0.8',
      'Connection': 'keep-alive'}
    try:
        req = urllib.request.Request(url="http://fontawesome.io/cheatsheet/", headers=header)
        html = urllib.request.urlopen(req).read().decode('utf-8')
        icondata = json.loads(re.findall(r"\[\{\"data\".*\}\]", html)[0])[1]['data']
    except:
        print('Error whilst fetching available brand icons for FontAwesome')
        for social_link in social_links:
            social_link['iconAvailable'] = False
    else:
        icons = list()

        for icon in icondata:
            if 'brands' in icon['attributes']['membership']['free']:
                icons.append(icon['id'])
        
        for social_link in social_links:
            if social_link['name'] in icons:
                social_link['iconAvailable'] = True
            else:
                social_link['iconAvailable'] = False

    # Registreer data
    channel_data['socialLinks'] = social_links

    # --- Opname van videos: algemene functies -------------------------------------------------------
    # Functie om een datum van een video te vervormen naar het gewenst formaat (YYYY-MM-DD => DD [maand in het Nederlands] YYYY)
    def translateDate(date):
        MAANDEN = ['januari', 'februari', 'maart', 'april', 'mei', 'juni', 'juli', 'augustus', 'september', 'oktober', 'november', 'december']
        
        year = int(date[:4])
        month  = int(date[5:7])
        day = int(date[8:10])
        
        return str(day) + ' ' + MAANDEN[month - 1] + ' ' + str(year)

    # Functie om een schooljaar te berekenen waarin een datum valt
    def getSchoolYear(date):
        year = int(date[:4])
        month  = int(date[5:7])

        if month < 9: year -= 1
        schoolYear = str(year) + '-' + str(year + 1)

        if schoolYear not in seenPublishSchoolYears:
            seenPublishSchoolYears.append(schoolYear)
        return schoolYear

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

            video_title = videodata['snippet']['title']

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

            if channel_data['trailer'] == video_id and not isTrailerThumbCached:
                if ospath.isdir(cd + '/../dist'):
                    urllib.request.urlretrieve(thumb_maxres_url, cd + '/../dist/overons.jpg')
                urllib.request.urlretrieve(thumb_maxres_url, cd + '/../public/overons.jpg')

            publishDate = videodata['snippet']['publishedAt'][:10]

            # Registreer omleidingslink
            video_path = video_title.lower().replace(' ', '-').replace('+', 'plus').replace('@', 'at').replace('&', 'en')
            video_path = re.sub(r'[^\x00-\x7f]',r'', video_path)
            video_path = re.sub(r'[\.\,\!\?\:\;\"\'\`\\\/\%\$\|\#\>\<]',r'', video_path)
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
                'publishDate': translateDate(publishDate),
                'publishSchoolYear': getSchoolYear(publishDate),
                'publishYear': publishDate[:4],
                'views': videodata['statistics']['viewCount'],
                'thumb': videodata['snippet']['thumbnails']['medium']['url'],
                'thumbmaxres': thumb_maxres_url,
                'thumbmaxres_type': thumbmaxres_type,
                'videoPath': video_path
            }

    # --- Opname van videos: afspeellijsten -------------------------------------------------------
    playlist_ids_data = api.get_playlists(channel_id=ENV_VARS['channel_id'], count=None).items
    channel_data['playlists'] = []
    for playlist in playlist_ids_data:
        list_id = playlist.id
        list_snippet = playlist.snippet
        
        playlist_data = {
            'name': list_snippet.title,
            'description': list_snippet.description,
            'listid': list_id,
            'content': []
        }

        playlist_item_data = api.get_playlist_items(playlist_id=list_id, count=None)
        for video in playlist_item_data.items:
            videodata = get_video_data(video.snippet.resourceId.videoId)
            if videodata != None:
                playlist_data['content'].append(videodata)

        channel_data['playlists'].append(playlist_data)

    # --- Opname van videos: uploads -------------------------------------------------------
    uploads_list_id = general_channel_data['contentDetails']['relatedPlaylists']['uploads']
    uploads_data = {
        'listid': uploads_list_id,
        'content': {}
    }
    uploads_item_data = api.get_playlist_items(playlist_id=uploads_list_id, count=None)
    for video in uploads_item_data.items:
        videodata = get_video_data(video.snippet.resourceId.videoId)
        if videodata != None:
            schoolYear = videodata['publishSchoolYear']
            if schoolYear not in uploads_data['content']:
                uploads_data['content'][schoolYear] = []
            uploads_data['content'][schoolYear].append(videodata)
        
    channel_data['uploads'] = uploads_data
    print("Failed video count: " + str(failed_video_count))

    # --- Registratie van jaren waarin er is geüpload -------------------------------------------------------
    channel_data['publishSchoolYears'] = sorted(seenPublishSchoolYears, reverse=True)

    # --- Genereer info over OINC voor gebruikers zonder JavaScript -------------------------------------------------------
    links_html = f"<!DOCTYPE html>\n<html>\n<head>\n<title>Korte info over oinc</title>\n</head>\n<body>\n<li>Ons kanaal: <a href=\"https://youtube.com/channel/{ENV_VARS['channel_id']}\" target=\"_blank\">klik</a></li>\n"
    for link in social_links:
        links_html += f"<li>{link['name']}: <a href=\"{link['url']}\" target=\"_blank\">klik</a></li>\n"
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