import requests
from bs4 import BeautifulSoup
from db import session_scope
from bootstrap import bootstrap
from models import Server


def server_search(to_visit_sites, start_point):

    with session_scope() as session:
        while len(to_visit_sites):
            helper = to_visit_sites.pop(0)
            response = requests.get(helper)
            soup = BeautifulSoup(response.content, 'html.parser')

            r = requests.head(helper)
            server_info = r.headers.get("server")
            if server_info is None:
                server_info = "NO SERVER FOUND"
            ser = Server(name=helper, server=server_info)
            session.add(ser)
            session.commit()

            for link in soup.find_all('a'):
                to_be_added = link.get('href')
                if to_be_added is not None and to_be_added not in to_visit_sites:
                    if to_be_added.startswith('http') and ".bg" in to_be_added:
                        to_visit_sites.append(to_be_added)
                        print(to_be_added)

                    elif to_be_added.startswith("link"):
                        to_be_added = start_point + to_be_added
                        to_visit_sites.append(to_be_added)
                        print(to_be_added)

    yield to_visit_sites


def run_server_search():
    start_point = "http://register.start.bg/"
    to_visit_sites = []
    to_visit_sites.append(start_point)
    to_visit_sites = list(server_search(to_visit_sites, start_point))


def main():
    bootstrap()
    run_server_search()


if __name__ == '__main__':
    main()
