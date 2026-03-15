#!/usr/bin/env python3
import argparse, json, urllib.request
from datetime import datetime, timezone, timedelta

AEST = timezone(timedelta(hours=10))

parser = argparse.ArgumentParser()
parser.add_argument('--cinema', required=True)
parser.add_argument('--date', default='')
parser.add_argument('--movie', default='')
args = parser.parse_args()

target_date = args.date or datetime.now(AEST).date().isoformat()

UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    with urllib.request.urlopen(req) as r:
        return json.load(r)

cinemas = fetch('https://apim.hoyts.com.au/au/cinemaapi/api/cinemas')
cinema = next((c for c in cinemas if c['id'] == args.cinema.upper() or c['slug'] == args.cinema.lower()), None)
if not cinema:
    print(f"Cinema not found: {args.cinema}")
    print("Run: python3 scripts/cinemas.py")
    exit(1)

movies, sessions = (
    fetch('https://apim.hoyts.com.au/au/cinemaapi/api/movies'),
    fetch(f"https://apim.hoyts.com.au/au/cinemaapi/api/sessions?date={target_date}&cinemaId={cinema['id']}"),
)

movie_map = {m['vistaId']: m['name'] for m in movies}
TAG_LABELS = {'RC': 'Recliners', 'DAYBEDS': 'Daybeds', 'LOUNGE': 'Lounge',
              'XTREME': 'Xtremescreen', 'IMAX': 'IMAX', 'LUX': 'LUX',
              'DBOX': 'D-BOX', 'SCREENX': 'SCREENX', 'ATMOS': 'Atmos', '3D': '3D', 'ONYX': 'ONYX'}
SKIP_TAGS = {'AD', 'CC', 'RC_STANDARD', 'DISCOUNT'}

results = [
    s for s in sessions
    if s['cinemaId'] == cinema['id'] and s['date'].startswith(target_date)
]
if args.movie:
    results = [s for s in results if args.movie.lower() in movie_map.get(s['movieId'], '').lower()]

results.sort(key=lambda s: s['date'])

print(f"\n{cinema['name']} — {target_date}\n")
print(f"{'Time':<7} {'Movie':<45} {'Screen':<18} {'Format'}")
print('-' * 90)
for s in results:
    tags = [TAG_LABELS.get(t, t) for t in s.get('originalTags', []) if t not in SKIP_TAGS and t in TAG_LABELS]
    fmt = ', '.join(tags) or 'Standard'
    print(f"{s['date'][11:16]:<7} {movie_map.get(s['movieId'], s['movieId'])[:44]:<45} {s['screenName']:<18} {fmt}")

print(f"\n{len(results)} sessions")
