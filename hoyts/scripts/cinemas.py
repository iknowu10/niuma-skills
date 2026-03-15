#!/usr/bin/env python3
import argparse, json, urllib.request

parser = argparse.ArgumentParser()
parser.add_argument('--state', default='')
args = parser.parse_args()

UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
req = urllib.request.Request('https://apim.hoyts.com.au/au/cinemaapi/api/cinemas', headers={'User-Agent': UA})
with urllib.request.urlopen(req) as r:
    cinemas = json.load(r)

if args.state:
    cinemas = [c for c in cinemas if c['state'] == args.state.upper()]
cinemas.sort(key=lambda c: (c['state'], c['name']))

print(f"{'Name':<35} {'ID':<8} {'State':<6} {'Suburb':<20} {'Features'}")
print('-' * 110)
for c in cinemas:
    print(f"{c['name'][:34]:<35} {c['id']:<8} {c['state']:<6} {c['address']['suburb'][:19]:<20} {', '.join(c.get('features',[]))}")
