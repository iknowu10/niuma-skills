#!/usr/bin/env python3
import argparse, json, urllib.request, urllib.parse

parser = argparse.ArgumentParser()
parser.add_argument('--query', required=True)
parser.add_argument('--limit', type=int, default=10)
args = parser.parse_args()

params = urllib.parse.urlencode({
    'query': args.query,
    'filters': 'type:Movie',
    'hitsPerPage': args.limit,
    'attributesToRetrieve': 'title,releaseDate,rating,tags,link',
})
url = f"https://I7WSMSQJH0-dsn.algolia.net/1/indexes/prod_HOYTSAU?{params}"
req = urllib.request.Request(url, headers={
    'X-Algolia-Application-Id': 'I7WSMSQJH0',
    'X-Algolia-API-Key': 'd2154c1fa8eae2dd92d8a0f9b20eb1af',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
})
with urllib.request.urlopen(req) as r:
    data = json.load(r)

hits = data.get('hits', [])
print(f"{'Title':<45} {'Rating':<8} {'Genres':<30} {'Release'}")
print('-' * 95)
for h in hits:
    release = h.get('releaseDate', '')[:10] if h.get('releaseDate') else ''
    print(f"{h['title'][:44]:<45} {h.get('rating',''):<8} {', '.join(h.get('tags',[]))[:29]:<30} {release}")
