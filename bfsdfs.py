import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def get_links(url):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return []
        soup = BeautifulSoup(response.text, 'html.parser')
        links = []
        for tag in soup.find_all('a', href=True):
            link = urljoin(url, tag['href'])
            # Only visit links with http or https schemes
            if urlparse(link).scheme in ('http', 'https'):
                links.append(link)
        return links
    except requests.RequestException:
        return []

def bfs_web_crawler(start_url, max_visits=30):
    visited = set()
    queue = [start_url]
    order_visited = []

    while queue and len(visited) < max_visits:
        current_url = queue.pop(0)  
        if current_url not in visited:
            visited.add(current_url)
            order_visited.append(current_url)
            links = get_links(current_url)
            for link in links:
                if link not in visited:
                    queue.append(link)
    return order_visited

def dfs_web_crawler(start_url, max_visits=30):
    visited = set()
    stack = [start_url]
    order_visited = []

    while stack and len(visited) < max_visits:
        current_url = stack.pop()  
        if current_url not in visited:
            visited.add(current_url)
            order_visited.append(current_url)
            links = get_links(current_url)
            for link in links:
                if link not in visited:
                    stack.append(link)
    return order_visited

if __name__ == "__main__":
    start = 'https://google.com'  

    print("BFS crawl order:")
    bfs_order = bfs_web_crawler(start)
    for url in bfs_order:
        print(url)

    print("\nDFS crawl order:")
    dfs_order = dfs_web_crawler(start)
    for url in dfs_order:
        print(url)
