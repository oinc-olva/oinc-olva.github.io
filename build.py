#!/usr/bin/env python3
import yaml
import json
from os import getcwd as cd
from os import system as runcmd
from time import gmtime, strftime
from pyyoutube import Api

def main():
    # Get environmental variables
    with open('env_vars.yaml', 'r') as f:
        ENV_VARS = yaml.safe_load(f)
    
    # Grab data from youtube api
    api = Api(api_key=ENV_VARS['api_key'])
    channel_data = api.get_channel_info(channel_id='UC6hYUzHTEx2sCO23hQtVZ6w').items[0].to_dict()

    # Dump json
    f = open("./channeldata.json", "w")
    json.dump(channel_data['brandingSettings'], f, indent = 4)
    f.close()

    # Commit to Github
    commit_msg = 'Update website (' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ')'
    print(f"git remote set-url origin https://{ENV_VARS['access_token']}@github.com/{ENV_VARS['username']}/oinc-olva.github.io.git/")
    runcmd(f"git remote set-url origin https://{ENV_VARS['access_token']}@github.com/{ENV_VARS['username']}/oinc-olva.github.io.git/")
    runcmd(f"git config user.email {ENV_VARS['email']}")
    runcmd(f"git config user.name {ENV_VARS['username']}")
    runcmd(f"git commit -m \"{commit_msg}\" -- channeldata.json")
    runcmd("git push")

if __name__ == "__main__":
    main()