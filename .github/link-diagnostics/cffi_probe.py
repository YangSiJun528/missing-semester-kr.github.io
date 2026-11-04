from pathlib import Path
from urllib.parse import urlparse, unquote
from html.parser import HTMLParser
from curl_cffi import requests
import curl_cffi, json, re, time
class Anchors(HTMLParser):
 def __init__(self):super().__init__();self.values=set()
 def handle_starttag(self,tag,attrs):
  self.values.update(v for k,v in attrs if k in ('id','name') and v)
print('CURL_CFFI_VERSION '+curl_cffi.__version__,flush=True)
for url in json.loads((Path(__file__).parent/'targets.json').read_text()):
 start=time.monotonic()
 try:
  response=requests.get(url,impersonate='chrome',timeout=30)
  title=re.search(r'<title[^>]*>(.*?)</title>',response.text,re.S|re.I)
  parsed=Anchors();parsed.feed(response.text);fragment=unquote(urlparse(url).fragment)
  row={'url':url,'status':response.status_code,'effective':response.url,'title':title.group(1).strip() if title else None,'bytes':len(response.content),'cf_mitigated':response.headers.get('cf-mitigated'),'fragment':fragment,'fragment_exists':fragment in parsed.values if fragment else None,'parking_redirect':'window.location.href="/lander"' in response.text,'seconds':round(time.monotonic()-start,2)}
 except Exception as error:row={'url':url,'error':str(error),'seconds':round(time.monotonic()-start,2)}
 print('CURL_CFFI_RESULT '+json.dumps(row,ensure_ascii=False),flush=True)
 time.sleep(2)
