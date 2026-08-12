import re
import urllib.request
import os

with open(r'C:\Tools\autesagent\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# find manifest url
match = re.search(r'"url":\s*"(/assets/manifest-[^"]+\.js)"', text)
if match:
    manifest_url = match.group(1)
    print('Manifest URL:', manifest_url)
    # Download the manifest
    url = f'https://metisagent.co{manifest_url}'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            content = response.read().decode('utf-8')
            # Replace metis with autes inside manifest
            content = content.replace('metis', 'autes')
            content = content.replace('METIS', 'AUTES')
            local_path = os.path.join(r'C:\Tools\autesagent', manifest_url.lstrip('/'))
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            with open(local_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print('Downloaded and patched manifest')
    except Exception as e:
        print('Failed to download manifest:', e)
else:
    print('No manifest URL found')
