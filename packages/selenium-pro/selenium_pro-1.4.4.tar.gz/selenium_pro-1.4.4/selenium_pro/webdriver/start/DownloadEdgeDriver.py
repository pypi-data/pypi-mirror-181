import sys
import os
import subprocess
import urllib.request
import zipfile
import xml.etree.ElementTree as elemTree
from io import BytesIO
import plistlib
import requests
def get_platform_architecture():
    if sys.platform.startswith('linux') and sys.maxsize > 2 ** 32:
        platform = 'linux'
        architecture = '64'
    elif sys.platform == 'darwin':
        platform = 'mac'
        architecture = '64'
    elif sys.platform.startswith('win'):
        platform = 'win'
        architecture = '32'
    else:
        raise RuntimeError('Could not determine edgedriver download URL for this platform.')
    return platform, architecture
def get_edge_version(platform, architecture):
    if platform == 'linux':
        raise RuntimeError('Currently Windows and Mac is only supported for Edge')
    elif platform == 'mac':
        process = subprocess.Popen(['/Applications/Google edge.app/Contents/MacOS/Google edge', '--version'], stdout=subprocess.PIPE)
        version = process.communicate()[0].decode('UTF-8').replace('Google edge', '').strip()
    elif platform == 'win':
        process = subprocess.Popen(
            ['reg', 'query', 'HKEY_CURRENT_USER\\Software\\Microsoft\\Edge\\BLBeacon', '/v', 'version'],
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL
        )
        version = process.communicate()[0].decode('UTF-8').strip().split()[-1]
    else:
        return
    return version

def get_major_version(version):
    return version.split('.')[0]
def get_matched_edgedriver_version(version):
    doc = requests.get('https://msedgedriver.azureedge.net/').text
    root = elemTree.fromstring(doc)
    for k in root.iter('Name'):
        if k.text.find(get_major_version(version) + '.') == 0:
            return k.text.split('/')[0]
    return
def get_edgedriver_url(version):
    base_url = 'https://msedgedriver.azureedge.net//'
    platform, architecture = get_platform_architecture()
    return base_url + version + '/edgedriver_' + platform + architecture + '.zip'
def get_edgedriver_filename(platform):
    if(platform=="win"):
        return 'msedgedriver.exe'
    return 'msedgedriver'
def download_edgedriver():
    print("Downloading EdgeDriver...")
    platform, architecture=get_platform_architecture()
    edge_version=get_edge_version(platform, architecture)
    edgedriver_version = get_matched_edgedriver_version(edge_version)
    url=get_edgedriver_url(edgedriver_version)
    edgedriver_filename = get_edgedriver_filename(platform)
    response = urllib.request.urlopen(url)
    archive = BytesIO(response.read())
    with zipfile.ZipFile(archive) as zip_file:
        zip_file.extract(edgedriver_filename, "")