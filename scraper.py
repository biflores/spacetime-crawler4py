import re
from urllib.parse import urlparse
from urllib.request import urlopen
from bs4 import BeautifulSoup

def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]

def extract_next_links(url, resp):
    # Implementation requred.
    new_urls = []
    html_page = urlopen.open(url)
    soup = BeautifulSoup.BeautifulSoup(html_page)
    for link in soup.findAll('a'):
        new_urls.append(link.get('href'))
    return new_urls

# TODO: move to another file 
# this function is to get started on the code for the deliverables
def extract_text(url):
    html_page = urlopen.open(url)
    soup = BeautifulSoup.BeautifulSoup(html_page)
    return soup.findAll(text=True)


def is_valid(url):
    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise