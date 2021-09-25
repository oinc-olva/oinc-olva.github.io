#!/usr/bin/env python3
import yaml
import json
import re
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
    # Initialiseer API en channel_data variabelen
    api = Api(api_key=ENV_VARS['api_key'])
    channel_data = dict()

    # Neem algemene data van het kanaal op
    general_channel_data = api.get_channel_info(channel_id=ENV_VARS['channel_id']).items[0].to_dict()
    channel_data['title'] = general_channel_data['brandingSettings']['channel']['title']
    channel_data['description'] = general_channel_data['brandingSettings']['channel']['description']
    channel_data['trailer'] = general_channel_data['brandingSettings']['channel']['unsubscribedTrailer']
    channel_data['keywords'] = general_channel_data['brandingSettings']['channel']['keywords']
    channel_data['statistics'] = general_channel_data['statistics']

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
            playlist_data['content'].append(video.snippet.resourceId.videoId)

        channel_data['playlists'].append(playlist_data)

    # Neem uploads op
    uploads_list_id = general_channel_data['contentDetails']['relatedPlaylists']['uploads']
    uploads_data = {
        'listid': uploads_list_id,
        'content': []
    }
    uploads_item_data = api.get_playlist_items(playlist_id=uploads_list_id, count=None)
    for video in uploads_item_data.items:
        uploads_data['content'].append(video.snippet.resourceId.videoId)
    channel_data['uploads'] = uploads_data

    # Sla data op
    f = open(cd + "/../dist/data.json", "w")
    json.dump(channel_data, f, indent = 4)
    f.close()

    # Commit naar Github
    commit_msg = '🚀 Automatische vernieuwing van website (' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ')'
    runcmd("npm run build")
    runcmd(f"git remote set-url origin https://{ENV_VARS['access_token']}@github.com/{ENV_VARS['username']}/{ENV_VARS['username']}.github.io.git/")
    runcmd(f"git config user.email {ENV_VARS['email']}")
    runcmd(f"git config user.name {ENV_VARS['username']}")
    runcmd("cd dist")
    runcmd("git init")
    runcmd("git add data.json")
    runcmd(f"git commit -m \"{commit_msg}\"")
    runcmd(f"git push -f git@github.com:{ENV_VARS['username']}/{ENV_VARS['username']}.github.io.git main:gh-pages")

if __name__ == "__main__":
    main()