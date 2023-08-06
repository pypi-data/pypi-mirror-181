"""
InstagramProfilePhotosDownloader
Copyright (C) 2022  Massimo Pavoni

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from argparse import ArgumentParser
from importlib import metadata
from os import mkdir as os_mkdir
from os.path import exists as os_path_exists
from os.path import join as os_path_join
from random import sample as random_sample
from time import sleep as time_sleep

from requests import get as requests_get
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Define command line tool parser
parser = ArgumentParser(
    prog=metadata.metadata('InstagramProfilePhotosDownloader')['name'],
    description=metadata.metadata('InstagramProfilePhotosDownloader')['summary'])
# Global positional args
parser.add_argument(
    'urls_file',
    help="location for the text file containing the photos' urls")
# Global optional args
parser.add_argument(
    '-V',
    '--version',
    action='version',
    version=f"%(prog)s {metadata.version('InstagramProfilePhotosDownloader')}")
# Commands
subparsers = parser.add_subparsers(dest='command')
# Scrape command
scrape = subparsers.add_parser('scrape', help="scrape selected profile")
# Positional args
scrape.add_argument('profile', help="instagram profile handle")
scrape.add_argument('csrftoken', help="csrftoken for secure session")
scrape.add_argument('username', help="instagram username")
scrape.add_argument('password', help="instagram password")
# Optional args
scrape.add_argument(
    '-lp',
    '--limit-posts',
    help="number of posts to gather if not all",
    dest='limit_posts')
scrape.add_argument(
    '-pw',
    '--page-wait',
    default=4,
    help="seconds to wait for pages loading",
    dest='page_wait')
scrape.add_argument(
    '-sw',
    '--scroll-wait',
    default=0.5,
    help="seconds to wait between scrolls",
    dest='scroll_wait')
scrape.add_argument(
    '-sh',
    '--scroll-height',
    default=500,
    help="pixels to scroll",
    dest='scroll_height')
# Download command
download = subparsers.add_parser(
    'download', help="download from saved text file")
# Positional args
download.add_argument(
    'photos_dir',
    help="location for the text file containing the photos' urls")
# Optional args
download.add_argument(
    '-rs',
    '--random-sample',
    help="randomly sample the amount of photos to download",
    dest='random_sample')


def scrape(args):
    # Create selenium driver
    driver = webdriver.Firefox()
    # Get Instagram login page
    driver.get('https://www.instagram.com/accounts/login/')
    # Let the page load
    time_sleep(args.page_wait)
    # Add csrftoken for secure session
    driver.add_cookie({'name': 'csrftoken',
                       'domain': 'instagram.com',
                       'value': args.csrftoken})
    # Get past cookies popup
    driver.find_element(
        By.XPATH,
        "//button[contains(.,'Only allow essential cookies')]").click()
    # Insert username
    driver.find_element(By.XPATH,
                        "//input[@name='username']").send_keys(args.username)
    # Get password element and login
    password_element = driver.find_element(
        By.XPATH, "//input[@name='password']")
    password_element.send_keys(args.password)
    password_element.send_keys(Keys.ENTER)
    # Let the page load
    time_sleep(args.page_wait)
    # Get specified Instagram profile page
    driver.get(f'https://www.instagram.com/{args.profile}/')
    # Let the page load
    time_sleep(args.page_wait)
    # Decide number of posts
    if args.limit_posts:
        posts_number = int(args.limit_posts)
    else:
        posts_number = int(
            driver.find_element(
                By.XPATH,
                "//li/div[contains(.,'posts')]/span/span").text.replace(
                ',',
                '').replace(
                '.',
                ''))
    if posts_number < 1:
        posts_number = 1
    # Gather posts
    urls = []
    while len(urls) < posts_number:
        # Find posts
        for e in driver.find_elements(
                By.XPATH, '//article/div/div/div/div//img'):
            url = e.get_attribute('src') + '\n'
            # Add url if it is not a duplicate
            if url not in urls:
                urls.append(url)
            # Break if gathered all the posts wanted
            if len(urls) == posts_number:
                break
        # Scroll down
        driver.execute_script(f"window.scrollBy(0, {args.scroll_height});")
        # Let the elements load
        time_sleep(args.scroll_wait)
    # Close selenium driver
    driver.close()
    # Save urls in text file
    with open(args.urls_file, 'w', encoding='utf-8') as f:
        f.writelines(urls)


def download(args):
    # Check if random sample is requested
    sample_amount = int(args.random_sample) if args.random_sample else 0
    if sample_amount < 1:
        sample_amount = 1
    # Get urls from text file
    with open(args.urls_file, 'r', encoding='utf-8') as f:
        urls = f.readlines()
    # Check if output directory exists
    if not os_path_exists(args.photos_dir):
        os_mkdir(args.photos_dir)
    # Download photos with requests and save them
    for i, url in enumerate(
            random_sample(
                urls, k=sample_amount) if args.random_sample else urls):
        response = requests_get(url)
        with open(os_path_join(args.photos_dir, f'{i}.png'), 'wb') as f:
            f.write(response.content)


def main():
    args = parser.parse_args()
    match args.command:
        # Scrape command
        case 'scrape':
            scrape(args)
        # Download command
        case 'download':
            download(args)


if __name__ == '__main__':
    main()
