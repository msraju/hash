import re
import feedparser
import pprint
import csv

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


# Output each feed for the c2s into a CSV file, which contains its own key-value pairs
with open('processed_c2s.csv', 'w', newline='') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    for posts in results:
         wr.writerow(results[posts]['c2s'])

# Pprint the c2s,urls, links and sha256s into a specific file
with open('processed_c2s.txt', 'wt') as out:
    for posts in results:
         pprint.pprint(results[posts]['c2s'], stream=out)

with open('processed_urls.txt', 'wt') as out:
    for posts in results:
         pprint.pprint(results[posts]['urls'], stream=out)

with open('processed_links.txt', 'wt') as out:
    for posts in results:
         pprint.pprint(results[posts]['links'], stream=out)

with open('processed_sha256s.txt', 'wt') as out:
    for posts in results:
         pprint.pprint(results[posts]['sha256s'], stream=out)

# pprint all the above into a single file
with open('processed_all.txt', 'wt') as out:
    pprint.pprint(results, stream=out)

# Dump the porcessed files
with open('processed.txt','w') as F:
    F.write('\n'.join(proc))
