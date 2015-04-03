from lxml import html
import os
import random
import requests
import string

unsplash = requests.get("https://unsplash.com/")
html_tree = html.fromstring(unsplash.text)

# Collects picture source as URL
weekly_ten_pictures = html_tree.xpath('/html/body/div/div/div/div/div/a/img/@src')

# Collects the names of the photographers 
picture_credits = html_tree.xpath('/html/body/div/div/div/div/div/h2/a[2]/text()')

credits_and_pictures = zip(picture_credits, weekly_ten_pictures)

desktop_unsplash_dir = os.path.expanduser('~/Desktop/unsplash')

# Creates an "unsplash" directory in Desktop if the directory doesn't already exist
if not os.path.exists(desktop_unsplash_dir):
    os.makedirs(desktop_unsplash_dir)

for credit, picture in credits_and_pictures:

    picture_data = requests.get(picture)

    if picture_data.status_code == 200:

        picture_html_tree = html.fromstring(picture_data.text)
        picture_name = ''.join(random.choice(string.hexdigits) for i in range(16))

        file_path = os.path.expanduser('~/Desktop/unsplash/{}-{}.jpeg'.format(credit, picture_name))

        print("Downloading {}-{}.jpeg".format(credit, picture_name))
        with open(file_path, 'wb') as f:
            f.write(picture_data.content)
        print("Finished.\n")
