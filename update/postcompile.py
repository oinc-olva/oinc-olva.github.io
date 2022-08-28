#!/usr/bin/env python3
import os
import re
import glob

def main():
    # Kopieer gegenereerde head tags
    with open(os.path.abspath('dist/index.html'), 'r') as f:
        html_head_tags = re.findall(r"\.ico\"\>(.*?)\<\/head\>", f.read())[0]
    
    # Sla op in ander bestand
    f = open(os.path.abspath('dist/htmlHeadTags.html'), "w+")
    f.write(html_head_tags)
    f.close()
    print('Found and saved HTML head tags')
    
    # Update (bijna) alle html-bestanden in /dist
    html_files = glob.glob('dist/[!generated]*/**/*.html.template', recursive=True)
    for file_ in html_files:
        html_file_abs = os.path.abspath(file_)

        f = open(html_file_abs, 'r')
        src = f.read().replace('$headTags', html_head_tags)
        f.close()
        os.remove(html_file_abs)

        f = open(html_file_abs[:-9], 'w+')
        f.write(src.replace('$headTags', html_head_tags))
        f.close()
    print(f"Injected HTML head tags in (at most) {len(html_files)} files")
            

if __name__ == "__main__":
    main()