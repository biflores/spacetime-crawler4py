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
    #return empty list if urlopen gives status other than 200
    try:
        html_page = urlopen(url)
    #Make more specific
    except:
        return new_urls
    soup = BeautifulSoup(html_page)
    for link in soup.findAll('a'):
        new_urls.append(link.get('href'))
    return new_urls

# TODO: move to another file 
# this function is to get started on the code for the deliverables
def extract_text(url):
    html_page = urlopen(url)
    soup = BeautifulSoup(html_page)
    return soup.findAll(text=True)



def is_valid(url):
    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        # make sure that fragment is empty
        if parsed.fragment:
            return False
        #check that links are in appropriate domains
        #missing today.uci.edu/department/information_computer_sciences/*
        if re.match(
            r"[:\/.a-zA-Z]*.ics.uci.edu[a-zA-Z1-9\/]*"
            + r"|[:\/.a-zA-Z]*.cs.uci.edu[a-zA-Z1-9\/]*"
            + r"|[:\/.a-zA-Z]*.informatics.uci.edu[a-zA-Z1-9\/]*"
            + r"|[:\/.a-zA-Z]*.stat.uci.edu[a-zA-Z1-9\/]*", parsed.netloc.lower()):
            pass
        else:
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