import re
import shutil
from collections import deque
import argparse
import os
import requests
from bs4 import BeautifulSoup
import validators
from colorama import Fore


def saves_page(dir_name, url, soup):
    file = open(f'{dir_name}/{url[7:url.find(".")]}', "w")
    file.write(soup.text)
    file.close()


def check_url(url):
    has_https = bool(re.search("^https://", url))
    if not has_https:
        url = ''.join("https://" + url)
    return url


# Function to remove tags
def remove_tags(html):
    # parse html content
    soup = BeautifulSoup(html, "html.parser")

    for data in soup(['style', 'script']):
        # Remove tags
        data.decompose()

    # return data by retrieving the tag content
    return '\n'.join(soup.stripped_strings)


exist = os.access('tb_tabs', os.F_OK)
if exist:
    shutil.rmtree('tb_tabs')

# terminal arguments
parser = argparse.ArgumentParser()
parser.add_argument("directory", type=str)
args = parser.parse_args()

# gets directory name and checks if it exists
dir_name = args.directory
exist = os.access(str(dir_name), os.F_OK)

# makes directory and other variables
os.mkdir(dir_name)
current_page = ""
previous = deque()
text = ""

while True:

    url = input()

    if url == "exit":
        break
    elif url == "back":
        # checks if there is a previous page
        # and prints if so
        if previous:
            print(previous[-1])
            previous.pop()

    else:

        # checks if url has https
        url = check_url(url)

        # saves and prints site if url is valid
        if validators.url(url):

            # if there is already a current page
            # that current page is saved as a
            # previous page
            if current_page:
                previous.append(current_page)

            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')

            # changes color of all links
            for i in soup.find_all("a"):
                i.string = "".join([Fore.BLUE, i.get_text(), Fore.RESET])

            # stores page in file
            saves_page(dir_name, url, soup)

            # saves page as current
            current = page.text

            # prints page without blank lines
            text = soup.text
            text = re.sub(r"\s*\n", "\n", text)
            print(text)

        else:
            print("Invalid URL")
