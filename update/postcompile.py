#!/usr/bin/env python3
import os
import glob

def main():
    # Kopieer gegenereerde head tags
    with open(os.path.abspath('dist/index.html'), 'r') as f:
        html_head_tags = f.read()[6:-7]
    
    # Sla op in ander bestand
    f = open(os.path.abspath('dist/htmlHeadTags.html'), "w+")
    f.write(html_head_tags)
    f.close()
    print('Found and saved HTML head tags')

    # Kopieer index.html van /public naar /dist
    with open(os.path.abspath('public/index.html'), 'r') as src:
        dest = open(os.path.abspath('dist/index.html'), "w+")
        dest.write(src.read().replace('$headTags', html_head_tags))
        dest.close()
    print('Copied public/index.html --> dist/index.html and (possibly) injected head tags')
    
    # Update (bijna) alle html-bestanden in /dist
    html_files = glob.glob('dist/[!generated]*/**/*.html', recursive=True)
    for file_ in html_files:
        html_file_abs = os.path.abspath(file_)

        f = open(html_file_abs, 'r')
        src = f.read().replace('$headTags', html_head_tags)
        f.close()

        f = open(html_file_abs, 'w+')
        f.write(src.replace('$headTags', html_head_tags))
        f.close()
    print(f"Injected HTML head tags in (at most) {len(html_files)} files")

    # Verwijder public/htmlHeadTags.html
    os.remove(os.path.abspath('public/htmlHeadTags.html'))
            

if __name__ == "__main__":
    main()