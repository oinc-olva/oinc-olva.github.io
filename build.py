#!/usr/bin/env python3
import yaml
import json
import re
from os import getcwd as cd
from os import system as runcmd
from time import gmtime, strftime
from pyyoutube import Api

def main():
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

    # Sla data op voor te kunnen debuggen als er iets foutloopt
    f = open("./debug.json", "w")
    json.dump(channel_data, f, indent = 4)
    f.close()

    # --- Bouw index.html uit template ------------------------------------------
    # Lees index_template.html
    f = open("index_template.html", "r")
    index_template = f.read()
    f.close()

    # Vervang variabelen (N.B.: als variabele verwijst naar sleutelwoorden, maak dan klaar voor gebruik in meta van website)
    def handle_var(var):
        tokens = var.group()[1:-1].split('.')
        data = channel_data.copy()
        isKeywords = False
        while len(tokens) > 0:
            try:
                data = data[tokens[0]]
            except KeyError as e:
                print(f"KeyError: unknown variable {e}. Build unsuccessful.")
                quit()
            else:
                if tokens[0] == 'keywords':
                    isKeywords = True
                del tokens[0]
        
        if isKeywords:
            keywords = data.split('"')
            for i, keyword in enumerate(keywords):
                keywords[i] = keyword.strip()
                if keywords[i] == '':
                    del keywords[i]
                else:
                    keywords[i] = keywords[i].replace(',', '&#44;')
            data = ', '.join(keywords)
        else:
            data = data.replace('"', '&quot;')

        return data
    
    indexHTML = re.sub(r"\{([^\}]+)\}", handle_var, index_template)

    # Sla op als index.html
    with open('index.html', 'w') as f:
        f.write(indexHTML)

    # Commit naar Github
    commit_msg = 'Update website (' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ')'
    runcmd(f"git remote set-url origin https://{ENV_VARS['access_token']}@github.com/{ENV_VARS['username']}/{ENV_VARS['username']}.github.io.git/")
    runcmd(f"git config user.email {ENV_VARS['email']}")
    runcmd(f"git config user.name {ENV_VARS['username']}")
    runcmd(f"git commit -m \"{commit_msg}\" -- index.html")
    runcmd("git push")

if __name__ == "__main__":
    main()