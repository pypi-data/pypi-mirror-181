import hashlib, json, io, glob, requests, os
import vytools.utils as utils
import vytools.printer
import vytools.uploads as uploads
from vytools.config import ITEMS
import cerberus
from pathlib import Path

SCHEMA = utils.BASE_SCHEMA.copy()
SCHEMA.update({
  'thingtype':{'type':'string', 'allowed':['bundle']},
  'publish':{'type':'boolean','required':False},
  'bundles':{
    'type':'list',
    'schema': {
      'type': 'dict',
      'schema': {
        'name': {'type': 'string', 'maxlength': 128},
        'serch': {'type': 'string', 'maxlength': 128},
        'rplce': {'type': 'string', 'maxlength': 128}
      }
    }
  },
  'philes':{
    'type':'list',
    'schema': {
      'type': 'dict',
      'schema': {
        'path': {'type': 'string', 'maxlength': 1024},
        'name': {'type': 'string', 'maxlength': 128},
        'hash': {'type': 'string', 'maxlength': 32}
      }
    }
  }
})

VALIDATE = cerberus.Validator(SCHEMA)

def fhash(pth):
  md5 = hashlib.md5()
  BUF_SIZE = 65536  # lets read stuff in 64kb chunks!
  try:
    with open(pth, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            md5.update(data)
  except Exception as exc:
    vytools.printer.print_fail('Failed to get hash for {}: {}'.format(pth,exc))
  return md5.hexdigest()

def parse(name, pth, items):
  item = {
    'name':name,
    'thingtype':'bundle',
    'philes':[],
    'bundles':[],
    'depends_on':[],
    'path':pth,
    'loaded':True
  }
  try:
    content = json.load(io.open(pth, 'r', encoding='utf-8-sig'))
    item['bundles'] = content.get('bundles',[])
    item['publish'] = content.get('publish',False)
    for phile in content.get('philes',[]):
      path = phile.get('path',None)
      prefix = phile.get('prefix',None)
      rplce = phile.get('rplce',None)
      serch = phile.get('serch',None)
      if path is not None:
        thisdir = os.getcwd()
        try:
          dirpath = os.path.dirname(pth)
          os.chdir(dirpath)
          file_list = glob.glob(path,recursive=True)
          for file in file_list:
            filepath = os.path.join(dirpath,file)
            if not os.path.isfile(filepath) or any([file.endswith(ext) for ext in ['.nodule.json','.bundle.json','.vydir']]):
              continue
            newname = file if not prefix else prefix+file
            if serch is not None and rplce is not None:
              newname = newname.replace(serch,rplce)
            item['philes'].append({
              'name':newname,
              'hash':fhash(filepath),
              'path':filepath
            })
            # print(item['philes'][-1])
        except Exception as exc:
          vytools.printer.print_fail('Failed to parse bundle "{n}" at "{p}": {e}'.format(n=name, p=pth, e=exc))
          return False
        os.chdir(thisdir)
  except Exception as exc:
    vytools.printer.print_fail('Failed to parse bundle "{n}" at "{p}": {e}'.format(n=name, p=pth, e=exc))
    return False

  return utils._add_item(item, items, VALIDATE)

def find_all(items, contextpaths=None):
  success = utils.search_all(r'(.+)\.bundle\.json', parse, items, contextpaths=contextpaths)
  for (type_name, item) in items.items():
    if type_name.startswith('bundle:'):
      (typ, name) = type_name.split(':',1)
      item['depends_on'] = []
      successi = True
      for e in item['bundles']:
        if e['name'] in items:
          item['depends_on'].append(e['name'])
        else:
          successi = False
          vytools.printer.print_fail('bundle "{n}" has a reference to a bundle {t}'.format(n=name, t=e['name']))
      success &= successi
      item['loaded'] &= successi
      utils._check_self_dependency(type_name, item)
  return success

def onsuccess(item, url, headers, result):
  refresh = result.get('refresh')
  success = True
  for phile in item['philes']:
    if phile['name'] in refresh:
      res = requests.post(url+'/update_phile', json={'_id':refresh[phile['name']],
        'hash':phile['hash'],
        'content':Path(phile['path']).read_text()},headers=headers)
      if not res.json().get('processed',False):
        success = False
        vytools.printer.print_fail('  - Failed to update phile "{}": {}'.format(phile['name'],res.json()))
      else:
        vytools.printer.print_success('  - Uploaded updated phile "{}"'.format(phile['name']))
  res = requests.post(url+'/clean_philes', json={}, headers=headers)
  return success
  
def upload(lst, url, uname, token, check_first, update_list, items=None):
  if items is None: items = ITEMS
  return uploads.upload('bundle', lst, url, uname, token, check_first, update_list, onsuccess, items=items)

def extract_philes(bundle_name, items=None, visited_bundles=[]):
  if items is None: items = ITEMS
  if not bundle_name or not bundle_name.startswith('bundle:') or bundle_name not in items: return []
  bundle = items[bundle_name]
  philes = {}
  for ph in bundle.get('philes',[]):
    philes[ph['name']] = ph['path']
  for bu in bundle.get('bundles',[]):
    if bu['name'] in visited_bundles: return
    visited_bundles.append(bu['name'])
    philes__ = extract_philes(bu['name'], items, visited_bundles)
    for name,pth in philes__.items():
      if bu.get('serch','|||') != '|||':
          rplce = '' if (bu.get('rplce','|||') == '|||') else bu['rplce']
          name = name.replace(bu['serch'], rplce,1)
      philes[name] = pth
  return philes

def mimetype(pth):
  extensions_map = {
      '': {'fmt':'binary','mime':'application/octet-stream'},
      '.manifest': {'fmt':'text','mime':'text/cache-manifest'},
      '.html': {'fmt':'text','mime':'text/html'},
      '.png': {'fmt':'binary','mime':'image/png'},
      '.ico': {'fmt':'binary','mime':'image/ico'},
      '.jpg': {'fmt':'binary','mime':'image/jpg'},
      '.svg': {'fmt':'text','mime':'image/svg+xml'},
      '.css': {'fmt':'text','mime':'text/css'},
      '.js': {'fmt':'text','mime':'application/x-javascript'},
      '.wasm': {'fmt':'text','mime':'application/wasm'},
      '.json': {'fmt':'text','mime':'application/json'},
      '.xml': {'fmt':'text','mime':'application/xml'},
  }
  return extensions_map.get('.'+pth.rsplit('.',1)[-1],{})

def rspnse__(self,pth):
    val = mimetype(pth)
    content = bytes(Path(pth).read_text(), "utf8") if val.get('fmt','text')=='text' else Path(pth).read_bytes()
    self.send_response(200)
    self.send_header("Content-type", val.get('mime','text/html'))
    self.end_headers()
    self.wfile.write(content)


def server(bundle_name, items=None, ip='localhost', port=8080):
  if items is None: items = ITEMS
  if vytools.utils.exists([bundle_name], items):
    import http.server # Our http server handler for http requests
    import socketserver # Establish the TCP Socket connections

    print('The following files will be served insecurely at http://{}:{}'.format(ip,port))
    philes = extract_philes(bundle_name,items)
    for name,pth in philes.items():
      print('  - {} at http://{}:{}/{}'.format(pth,ip,port,name))
    input('Press any key to continue')

    class BundleHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
      def do_GET(self):
        if self.path[1:] in philes:
          rspnse__(self,philes[self.path[1:]])
        else:
          print(' -- Cant find',self.path)
    Handler = BundleHttpRequestHandler
    with socketserver.TCPServer(("", port), Handler) as httpd:
      httpd.serve_forever()