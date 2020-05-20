import requests
from bs4 import BeautifulSoup
from db import session_scope
from bootstrap import bootstrap
from models import Server

to_visit_sites = []

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
            info = session.query(Server).filter(Server.name == helper).one_or_none()
            if info is None:
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


def run_server_search():
    if len(to_visit_sites) == 0:
        start_point = input("Please, enter link for the start point: ")
        to_visit_sites.append(start_point)
    else:
        start_point = to_visit_sites[0]
    server_search(to_visit_sites, start_point)


def main():
    bootstrap()
    run_server_search()


if __name__ == '__main__':
    main()
