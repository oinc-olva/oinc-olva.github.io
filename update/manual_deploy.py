#!/usr/bin/env python3
import yaml
import os

def main():
    # Zet locatie
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # Laad omgevingsvariabelen
    with open('env_vars.yaml', 'r') as f:
        ENV_VARS = yaml.safe_load(f)

    # Maak commando's
    commands = f"""
        cd ..
        npm run compile
        cd dist

        git init
        git add -A
        git config user.email "{ENV_VARS['email']}"
        git config user.name "{ENV_VARS['username']}"
        git commit -m \"🔧 Handmatige website update\"
        git remote add origin https://{ENV_VARS['access_token']}@github.com/{ENV_VARS['username']}/{ENV_VARS['username']}.github.io.git
        git push -f https://{ENV_VARS['access_token']}@github.com/{ENV_VARS['username']}/{ENV_VARS['username']}.github.io.git master:gh-pages
    """

    commands = commands.split('\n')
    for i in range(len(commands)):
        commands[i] = commands[i].lstrip()
    commands = '\n'.join(commands)

    f = open("manual_deploy.sh", "w", encoding="utf-8")
    f.write(commands)
    f.close()

    os.system("bash manual_deploy.sh")
    os.remove("manual_deploy.sh")

if __name__ == "__main__":
    main()