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
    
    # --- Beheer API data -------------------------------------------------------
    # Initialiseer APIs en channel_data variabelen
    api = Api(api_key=ENV_VARS['api_key'])
    channel_data = dict()
    global failed_video_count
    failed_video_count = 0

    # Neem algemene data van het kanaal op
    general_channel_data = api.get_channel_info(channel_id=ENV_VARS['channel_id']).items[0].to_dict()
    channel_data['title'] = general_channel_data['brandingSettings']['channel']['title']
    channel_data['description'] = general_channel_data['brandingSettings']['channel']['description']
    channel_data['trailer'] = general_channel_data['brandingSettings']['channel']['unsubscribedTrailer']
    channel_data['keywords'] = general_channel_data['brandingSettings']['channel']['keywords']
    channel_data['statistics'] = general_channel_data['statistics']

    # Functie voor het verwerken van videodata
    def get_video_data(video_id):
        global failed_video_count

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

            video_duration_iso = videodata['contentDetails']['duration'][2:]
            video_duration = ""
            i = 0
            while i < len(video_duration_iso) - 1:
                if video_duration_iso[i].isdigit():
                    if i+1 < len(video_duration_iso) and video_duration_iso[i+1].isdigit():
                        video_duration += video_duration_iso[i] + video_duration_iso[i+1]
                        i += 1
                    else:
                        video_duration += "0" + video_duration_iso[i]
                else:
                    video_duration += ":"
                i += 1

            return {
                'id': video_id,
                'title': videodata['snippet']['title'],
                'description': videodata['snippet']['description'],
                'duration': video_duration,
                'views': videodata['statistics']['viewCount'],
                'thumb': videodata['snippet']['thumbnails']['medium']['url'],
                'thumbmaxres': thumb_maxres_url,
                'thumbmaxres_type': thumbmaxres_type
            }

    # Neem afspeellijsten op
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

    # Neem uploads op
    uploads_list_id = general_channel_data['contentDetails']['relatedPlaylists']['uploads']
    uploads_data = {
        'listid': uploads_list_id,
        'content': []
    }
    uploads_item_data = api.get_playlist_items(playlist_id=uploads_list_id, count=None)
    for video in uploads_item_data.items:
        videodata = get_video_data(video.snippet.resourceId.videoId)
        if videodata != None:
            uploads_data['content'].append(videodata)
        
    channel_data['uploads'] = uploads_data
    print("Failed video count: " + str(failed_video_count))

    # Sla data op
    f = open(cd + "/../dist/channeldata.json", "w")
    json.dump(channel_data, f, indent = 4)
    f.close()
    f = open(cd + "/../public/channeldata.json", "w")
    json.dump(channel_data, f, indent = 4)
    f.close()

    # Commit naar Github
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