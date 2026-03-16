#!/usr/bin/env python3
"""
Weather forecast via Open-Meteo (free, no API key).

Usage:
  python3 scripts/forecast.py                        # default: Melbourne
  python3 scripts/forecast.py --city melbourne
  python3 scripts/forecast.py --lat -33.87 --lon 151.21  # Sydney coords
  python3 scripts/forecast.py --days 3
"""
import argparse, json, urllib.request

CITIES = {
    'melbourne': (-37.8136, 144.9631, 'Melbourne'),
    'sydney':    (-33.8688, 151.2093, 'Sydney'),
    'brisbane':  (-27.4698, 153.0251, 'Brisbane'),
    'beijing':   (39.9042,  116.4074, 'Beijing'),
    'shanghai':  (31.2304,  121.4737, 'Shanghai'),
    'shenzhen':  (22.5431,  114.0579, 'Shenzhen'),
}

WEATHER_ICONS = {
    0: '☀️', 1: '🌤', 2: '🌤', 3: '☁️',
    45: '🌫', 48: '🌫',
    51: '🌦', 53: '🌦', 55: '🌧',
    61: '🌧', 63: '🌧', 65: '🌧',
    71: '🌨', 73: '🌨', 75: '🌨', 77: '🌨',
    80: '🌦', 81: '🌦', 82: '🌦',
    85: '🌨', 86: '🌨',
    95: '⛈', 96: '⛈', 99: '⛈',
}

parser = argparse.ArgumentParser()
parser.add_argument('--city', default='melbourne')
parser.add_argument('--lat', type=float)
parser.add_argument('--lon', type=float)
parser.add_argument('--days', type=int, default=1)
args = parser.parse_args()

if args.lat and args.lon:
    lat, lon, city_name = args.lat, args.lon, f'{args.lat},{args.lon}'
else:
    city_key = args.city.lower()
    if city_key not in CITIES:
        print(f'Unknown city: {args.city}. Use --lat/--lon or one of: {", ".join(CITIES)}')
        exit(1)
    lat, lon, city_name = CITIES[city_key]

url = (
    f'https://api.open-meteo.com/v1/forecast'
    f'?latitude={lat}&longitude={lon}'
    f'&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max,weathercode'
    f'&timezone=auto&forecast_days={args.days + 1}'
)

with urllib.request.urlopen(url, timeout=10) as r:
    w = json.load(r)

daily = w['daily']
dates = daily['time']
highs = daily['temperature_2m_max']
lows  = daily['temperature_2m_min']
rains = daily['precipitation_probability_max']
codes = daily['weathercode']

print(f'🌍 {city_name}')
for i in range(args.days):
    icon = WEATHER_ICONS.get(codes[i], '🌡')
    label = 'Today' if i == 0 else ('Tomorrow' if i == 1 else dates[i])
    print(f'  {label:<10} {icon}  {lows[i]:.0f}–{highs[i]:.0f}°C  rain {rains[i]}%')
