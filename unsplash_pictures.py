"""Simple image downloader for images from Unsplash"""
from bs4 import BeautifulSoup
from termcolor import colored
import requests
import os

class UnsplashDownloader:

    def __init__(self, download_range='weekly', download_dir='~/Desktop/unsplash/'):
        self.unsplash_url = "https://unsplash.com/"
        self.download_dir = self.setup_directory(download_dir)
        self.download_range = download_range
        self.image_count = self.find_image_count()
        self.download_images()

    def find_image_count(self):
        """Counts the number of files within a directory."""
        return len([name for name in os.listdir(self.download_dir) if os.path.isfile(name)])

    def download_images(self):
        """Download images by parsing the HTML tree from Unsplash's main page."""
        html_tree = requests.get(self.unsplash_url).text
        unsplash_soup = BeautifulSoup(html_tree, 'html.parser')
        image_divs = unsplash_soup.body.find_all('div', {"class":"photo"})
        image_info = [(self.parse_url(image), self.parse_credit(image)) for image in image_divs]

        for image in image_info:
            image_data = self.download_image(image[0])
            if image_data.status_code == 200:
                print(colored("Downloading {}.jpeg".format(image[1]), 'green'))
                file_path = os.path.expanduser(
                    '{}{}-{}.jpeg'.format(self.download_dir, image[1], self.image_count))

                with open(file_path, 'wb') as image_file:
                    image_file.write(image_data.content)

                self.image_count += 1
            else:
                print(colored("Download failed for image URL: {}.".format(image[1]), 'red'))

    @classmethod
    def download_image(cls, image_url):
        """Downloads an image based on the URL and returns the data."""
        print("Downloading from image URL: {}".format(image_url))
        return requests.get(image_url)

    @classmethod
    def parse_url(cls, image_div):
        """Returns the URL of a given image parsed from an image div."""
        image_url = image_div.find('img')['src']
        return image_url[:image_url.find('?')]

    @classmethod
    def parse_credit(cls, image_div):
        """Given Format = 'Photo By Photographer Name'. Parses the name to use as credit
        for downloaded image."""
        return image_div.find('img')['alt'].partition('By')[-1].strip()

    @classmethod
    def setup_directory(self, download_directory):
        """Creates an "unsplash" directory in Desktop if the directory doesn't already exist"""
        desktop_unsplash_dir = os.path.expanduser(download_directory)
        if not os.path.exists(desktop_unsplash_dir):
            os.makedirs(desktop_unsplash_dir)

        return desktop_unsplash_dir

if __name__ == "__main__":
    downloader = UnsplashDownloader()
    downloader.download_images()
