"""Verify the current source archives and repository file manifest."""
from pathlib import Path
import csv
import hashlib
import json
import zipfile

ROOT = Path(__file__).resolve().parent

def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    version = json.loads((ROOT / 'VERSION.json').read_text(encoding='utf-8'))
    for component in version['components']:
        path = ROOT / component['name']
        if sha256(path) != component['sha256']:
            raise ValueError('Archive hash mismatch: ' + path.name)
        with zipfile.ZipFile(path) as archive:
            if archive.testzip() is not None:
                raise ValueError('Archive CRC failure: ' + path.name)
            if len(archive.infolist()) != component['files']:
                raise ValueError('Archive member count mismatch: ' + path.name)
    with (ROOT / 'FILE_MANIFEST_SHA256.csv').open(encoding='utf-8', newline='') as stream:
        rows = list(csv.DictReader(stream))
    for row in rows:
        path = (ROOT / row['path']).resolve()
        if ROOT not in path.parents or not path.is_file() or sha256(path) != row['sha256']:
            raise ValueError('File manifest mismatch: ' + row['path'])
    print(json.dumps({'status': 'PASS', 'release': version['release_id'],
                      'components': len(version['components']), 'files': len(rows)}, indent=2))

if __name__ == '__main__':
    main()
