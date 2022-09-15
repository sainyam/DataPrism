import json
import gzip

def parse(path):
  g = gzip.open(path, 'r')
  for l in g:
    jobj=(eval(l))
    try:
      txt=jobj['title']
      txt.replace(',','')
      print(jobj['asin']+","+txt)
    except:
      continue

parse('./metadata.json.gz')

