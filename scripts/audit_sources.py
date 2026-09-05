"""Read the tour's advertised public resources; never execute downloaded scripts."""
from pathlib import Path
import concurrent.futures, json, re, requests

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'reference/source'
page = (SOURCE / 'page.html').read_text(encoding='utf-8-sig')
urls = re.findall(r'<script[^>]+src="([^"]+)"', page)
urls = [u for u in urls if 'panoPageV2.' in u or 'krp_player_' in u]

def read(url):
    try:
        r = requests.get(url, timeout=25)
        result = dict(url=url, status=r.status_code, content_type=r.headers.get('Content-Type'), bytes=len(r.content))
        if r.status_code == 200 and 'html' not in r.headers.get('Content-Type','').lower():
            dest = SOURCE / url.rsplit('/',1)[-1]
            dest.write_bytes(r.content)
            result['saved'] = str(dest.relative_to(ROOT))
            result['matches'] = re.findall(r'.{0,90}(?:cdnDomain|cdnConfig|720static\.com).{0,180}', r.text)[:35]
        return result
    except requests.RequestException as e:
        return dict(url=url, error=str(e))

if __name__ == '__main__':
    results = list(concurrent.futures.ThreadPoolExecutor(max_workers=2).map(read, urls))
    (ROOT / 'reference/reports/resource_probe.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf8')
    print(json.dumps(results,ensure_ascii=False,indent=2))
