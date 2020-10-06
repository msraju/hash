import re
import feedparser
import pprint

SHA256 = '[a-f0-9]{64}'
URL = 'https?://[^\s]+'
IP = '\d+\.\d+\.\d+\.\d+'
NAME = '\<h4 id="([^\"]+)"\>'
SECTION = '\<h4 id="[^\"]+"\>[\s\S]*?\<\/pre\>\<\/div\>\<\/div\>'


rss_url = 'https://paste.cryptolaemus.com/feed.xml'

feed = feedparser.parse(rss_url)
results = {}

try:
    with open('processed.txt') as F:
        proc = F.read().split('\n')
except:
    proc = []

for post in feed.entries:
    if post.id in proc:
        continue

    result = {'sha256s': [], 'urls': [], 'links': [], 'c2s': []}

    data = post.content[0].get('value')
    sections = re.findall(SECTION, data)

    for section in sections:
        names = re.match(NAME, section)
        name = 'no-section-name'
        if names:
            name = names.groups()[0]

        links = []
        urls = re.findall(URL, section)
        sha256s = re.findall(SHA256, section)
        c2s = re.findall(IP, section)

        for srch_trm in ['daily-log', 'credits', 'what-is', 'community-lists', 'sandbox', 'report', 'news']:
            if srch_trm in name:
                links = re.findall(URL, section)
                urls = []
                break

        result['sha256s'] += [[x,name] for x in sha256s]
        result['urls'] += [[x,name] for x in urls]
        result['links'] += [[x,name] for x in links]
        result['c2s'] += [[x,name] for x in c2s]
    results[post.id] = result
    proc.append(post.id)

with open('processed.txt','w') as F:
    F.write('\n'.join(proc))


pprint.pprint(results)