import concurrent.futures, json, pathlib, re, subprocess, sys, time
root=pathlib.Path(__file__).resolve().parent
urls=json.loads((root/'targets.json').read_text())
out=pathlib.Path(sys.argv[1]); out.mkdir(parents=True,exist_ok=True)
ua='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.0.0 Safari/537.36'
modern='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36'
variants=[('head-proof',['-I','-A',ua]),('get-proof',['-A',ua]),('get-compressed',['-A',ua,'--compressed']),('get-accept',['-A',ua,'-H','Accept: text/html']),('get-modern',['-A',modern,'-H','Accept: text/html','--compressed'])]
def probe(item):
 i,url=item; results=[]
 for label,opts in variants:
  dest=out/f'{i}-{label}'; headers=str(dest)+'.headers'; body=str(dest)+'.body'
  cmd=['curl','-sS','-L','--connect-timeout','15','--max-time','60','--max-filesize','2097152','-D',headers,'-o',body,'-w','%{json}',*opts,url]
  p=subprocess.run(cmd,text=True,capture_output=True,timeout=70)
  try: info=json.loads(p.stdout)
  except ValueError: info={'raw':p.stdout}
  h=pathlib.Path(headers).read_text(errors='replace') if pathlib.Path(headers).exists() else ''
  b=pathlib.Path(body).read_text(errors='replace') if pathlib.Path(body).exists() else ''
  title=re.search(r'<title[^>]*>(.*?)</title>',b,re.S|re.I)
  row={'url':url,'variant':label,'exit':p.returncode,'status':info.get('http_code'),'seconds':info.get('time_total'),'effective':info.get('url_effective'),'bytes':info.get('size_download'),'error':p.stderr.strip(),'title':title.group(1).strip() if title else None,'headers':[v for v in h.splitlines() if re.match(r'(?i)^(HTTP/|server:|retry-after:|cf-mitigated:|content-type:|location:|content-encoding:|content-length:|transfer-encoding:|connection:)',v)],'challenge':'cf-chl-' in b or 'Just a moment' in b}
  results.append(row); print(json.dumps(row,ensure_ascii=False),flush=True)
  pathlib.Path(body).unlink(missing_ok=True)
  pathlib.Path(headers).unlink(missing_ok=True)
  time.sleep(2)
 return results
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
 rows=[row for group in pool.map(probe,enumerate(urls)) for row in group]
(out/'results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
