from urllib.parse import urlparse
from urllib import robotparser
import os
from urllib.request import urlopen
from bs4 import BeautifulSoup

# AGENT_NAME = '*'
# URL_BASE = 'https://news.uci.edu'
# parser = robotparser.RobotFileParser()
# parser.set_url(parse.urljoin(URL_BASE, 'robots.txt'))
# parser.read()
# print(parser.site_maps())
# print(parser.entries[0].rulelines[0].path)
# print(parser.entries[0].rulelines[0].allowance)
# for entry in parser.entries:
#     print(entry.useragents)

# https://github.com/python/cpython/blob/3.10/Lib/urllib/robotparser.py
class MyRobotParser2:
    def __init__(self, url_base) -> None:
        self.AGENT_NAME = '*'
        self.URL_BASE = url_base
        self.parser = robotparser.RobotFileParser()
        self.parser.set_url(parse.urljoin(self.URL_BASE, 'robots.txt'))
        self.parser.read()

    def get_sitmaps(self) -> list:
        return self.parser.site_maps()

    def get_allowed_paths(self) -> list:
        allowed_paths = []
        allowed_rulelines = []
        print(self.parser.entries)
        for entry in self.parser.entries:
            print(entry)
            if self.AGENT_NAME in entry.useragents:
                print(entry.rulelines)
                allowed_rulelines.extend(entry.rulelines)

        for ruleline in allowed_rulelines:
            if ruleline.allowance:
                allowed_paths.append(ruleline.path)
        return allowed_paths

    def check_can_fetch(self, url):
        '''checks if the url you want to visit is allowed by robots.txt'''        
        return self.parser.can_fetch(self.AGENT_NAME, url)

# myrobotparser = MyRobotParser('https://informatics.uci.edu')
# # print(myrobotparser.get_allowed_paths())
# print(myrobotparser.check_can_fetch('https://informatics.uci.edu/research/gifts-grants/'))



class MyRobotParser:
    def __init__(self, url_base) -> None:
        self.AGENT_NAME = '*'
        self.URL_BASE = url_base
        self.robot_txt_url = os.path.join(self.URL_BASE, 'robots.txt')
        self.robot_txt_text = self.extract_text()
        self.robot_txt_info = {'sitemaps': [], 'allow': [], 'disallow': [], 'crawl_delay': 0, 'request_rate': 0}

    def extract_text(self):
        html_page = urlopen(self.robot_txt_url)
        soup = BeautifulSoup(html_page)
        return soup.findAll(text=True)[0]

    def get_robot_text_info(self) -> list:
        correct_user_agent = False
        for line in self.robot_txt_text.rstrip().split('\n'):
            if line == '' or line[0] == '#':
                pass
            elif line.startswith('User-agent'):
                if self.AGENT_NAME in line:
                    correct_user_agent = True
                else:
                    correct_user_agent = False
            elif correct_user_agent and line.startswith('Allow:'):
                self.robot_txt_info['allow'].append(line.split()[-1])
            elif correct_user_agent and line.startswith('Disallow'):
                self.robot_txt_info['disallow'].append(line.split()[-1])
            elif line.startswith('Crawl-delay'):
                self.robot_txt_info['crawl_delay'] = int(line.split()[-1])
            elif line.startswith('Request-rate'):
                self.robot_txt_info['request_rate'] = int(line.split()[-1])
            elif line.startswith('Sitemap:'):
                self.robot_txt_info['sitemaps'].append(line.split()[-1])



    def check_can_fetch(self, url) -> bool:
        '''checks if the url you want to visit is allowed by robots.txt'''
        parsed_url = urlparse(url)
        in_disallow = False
        for allow_path in self.robot_txt_info['allow']:
            if parsed_url.path.startswith(allow_path):
                return True
        for disallow_path in self.robot_txt_info['disallow']:
            if parsed_url.path.startswith(disallow_path):
                in_disallow = True     
        return not in_disallow 


    

# myrobotparser = MyRobotParser('https://news.uci.edu')
# myrobotparser.get_robot_text_info()
# print(myrobotparser.robot_txt_info)

# data = urlopen('https://news.uci.edu/wp-sitemap.xml')
# print(data)
# Passing the data of the xml
# file to the xml parser of
# beautifulsoup
# bs_data = BeautifulSoup(data, 'xml')
# print(bs_data)
# for points in bs_data.find_all("sitemap"):
#     point = str(points.text)
#     print(point)
import re
# a = re.findall(r'(https?://[^\s"]+)', bs_data)
# print(a)

def read_xml(url):
    xml = urlopen(url)
    xml_data = BeautifulSoup(xml, 'xml')
    print(xml_data)
    for tag in xml_data.find_all("sitemap"):
        url = str(tag.text)
        print(url)
# read_xml('https://news.uci.edu/wp-sitemap-posts-post-1.xml')

def read_xml_tree(url):
    f = urlopen(url)
    res = f.readlines()
    for d in res:
        print(type(d))
        data = re.findall(r'(https?://[^\s"]+)',d)
        for i in data:
            print(i)
# read_xml_tree('https://news.uci.edu/wp-sitemap.xml')

read_xml_tree('https://news.uci.edu/wp-sitemap-posts-post-1.xml')



# import urllib.robotparser as urobot
# import urllib.request
# from bs4 import BeautifulSoup


# url = "https://uci.edu"
# rp = urobot.RobotFileParser()
# rp.set_url(url + "/robots.txt")
# rp.read()
# if rp.can_fetch("*", url):
#     site = urllib.request.urlopen(url)
#     sauce = site.read()
#     soup = BeautifulSoup(sauce, "html.parser")
#     actual_url = site.geturl()[:site.geturl().rfind('/')]

#     my_list = soup.find_all("a", href=True)
#     for i in my_list:
#         # rather than != "#" you can control your list before loop over it
#         if i != "#":
#             newurl = str(actual_url)+"/"+str(i)
#             try:
#                 if rp.can_fetch("*", newurl):
#                     print(newurl)
#                     site = urllib.request.urlopen(newurl)
#                     # do what you want on each authorized webpage
#             except:
#                 pass
# else:
#     print("cannot scrap")