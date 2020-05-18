import requests
from bs4 import BeautifulSoup

from bootstrap import bootstrap


def run_server_search():
    start_site = input("Please, insert html link here:")
    to_visit_sites = []
    to_visit_sites.append(start_site)

    while len(to_visit_sites) > 0:
        helper = to_visit_sites[0]
        to_visit_sites.pop(0)
        response = requests.get(helper)
        soup = BeautifulSoup(response.content, 'html.parser')
        r = requests.head("http://register.start.bg/")
        server_info = r.headers["server"]
        ##TODO
        for link in soup.find_all('a'):
            to_be_added = link.get('href')
            if to_be_added is not None and to_be_added not in to_visit_sites:
                if "link" in to_be_added or ".bg" in to_be_added:
                    to_visit_sites.append(to_be_added)


def main():
    bootstrap()
