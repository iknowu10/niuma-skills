#!/usr/bin/env python3
import argparse, json, urllib.request

parser = argparse.ArgumentParser()
parser.add_argument('--limit', type=int, default=20)
args = parser.parse_args()

UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
req = urllib.request.Request('https://apim.hoyts.com.au/au/cinemaapi/api/movies', headers={'User-Agent': UA})
with urllib.request.urlopen(req) as r:
    movies = json.load(r)

movies = [m for m in movies if m.get('type') == 'comingSoon']
movies.sort(key=lambda m: m.get('releaseDate') or '')
movies = movies[:args.limit]

print(f"{'Title':<45} {'Rating':<8} {'Runtime':<9} {'Genres':<30} {'Release'}")
print('-' * 106)
for m in movies:
    release = m.get('releaseDate', '')[:10] if m.get('releaseDate') else 'TBA'
    print(f"{m['name'][:44]:<45} {m['rating']['id']:<8} {str(m.get('duration',''))+'min':<9} {', '.join(m.get('genres',[]))[:29]:<30} {release}")
