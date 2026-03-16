#!/usr/bin/env python3
"""
Financial quotes. Supports A-shares, HK stocks, and anything on Yahoo Finance.

Usage:
  python3 scripts/quote.py sh600489 hk00700 GC=F AAPL ^TNX

Symbol formats:
  sh######  - A-share Shanghai (Tencent Finance)
  sz######  - A-share Shenzhen (Tencent Finance)
  hk#####   - Hong Kong stock (Tencent Finance)
  anything else - Yahoo Finance (US stocks, futures, indices, FX)
"""
import sys, json, urllib.request, urllib.parse

UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'

def fetch_tencent(symbols):
    """Fetch quotes for sh/sz/hk symbols from Tencent Finance."""
    q = ','.join(symbols)
    url = f'https://qt.gtimg.cn/q={q}'
    req = urllib.request.Request(url, headers={'User-Agent': UA, 'Referer': 'https://finance.qq.com'})
    with urllib.request.urlopen(req, timeout=10) as r:
        raw = r.read().decode('gbk')

    results = []
    for line in raw.strip().splitlines():
        if '="' not in line:
            continue
        val = line.split('"')[1]
        f = val.split('~')
        if len(f) < 35:
            continue
        name   = f[1]
        code   = f[2]
        price  = f[3]
        change = f[31]
        pct    = f[32]
        high   = f[33]
        low    = f[34]
        try:
            c = float(change)
            sign = '+' if c >= 0 else ''
            currency = 'HK$' if code.startswith('0') and len(code) == 5 else '¥'
            results.append(f'{name} ({code})  {currency}{price}  {sign}{change} ({sign}{pct}%)')
        except:
            results.append(f'{name} ({code})  {price}')
    return results

def fetch_yahoo(symbol):
    """Fetch quote for a single symbol from Yahoo Finance."""
    url = f'https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(symbol)}?interval=1d&range=1d'
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    with urllib.request.urlopen(req, timeout=10) as r:
        d = json.load(r)
    meta = d['chart']['result'][0]['meta']
    name  = meta.get('shortName') or meta.get('symbol') or symbol
    price = meta.get('regularMarketPrice') or meta.get('previousClose')
    prev  = meta.get('chartPreviousClose') or meta.get('previousClose') or price
    currency = meta.get('currency', '')
    try:
        change = price - prev
        pct = change / prev * 100
        sign = '+' if change >= 0 else ''
        return f'{name} ({symbol})  {currency} {price:,.2f}  {sign}{change:.2f} ({sign}{pct:.2f}%)'
    except:
        return f'{symbol}  {price}'

if len(sys.argv) < 2:
    print('Usage: quote.py <symbol> [symbol ...]')
    print('  A/HK: sh600489 sz000858 hk00700')
    print('  Others: GC=F AAPL ^TNX')
    sys.exit(1)

symbols = sys.argv[1:]

# Split by source
tencent = [s for s in symbols if s[:2].lower() in ('sh', 'sz', 'hk')]
yahoo   = [s for s in symbols if s not in tencent]

if tencent:
    try:
        for line in fetch_tencent(tencent):
            print(line)
    except Exception as e:
        print(f'[Tencent] error: {e}')

for sym in yahoo:
    try:
        print(fetch_yahoo(sym))
    except Exception as e:
        print(f'{sym}  error: {e}')
