import sys
import os
import subprocess
import urllib.request
import zipfile
import xml.etree.ElementTree as elemTree
from io import BytesIO
import plistlib
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
        raise RuntimeError('Could not determine chromedriver download URL for this platform.')
    return platform, architecture
def edit_cdc_string(chromedriver_filename):
    with open(chromedriver_filename,"rb") as d:
        file_data=d.read()
    file_data=file_data.replace(b"cdc_",b"tch_")
    with open(chromedriver_filename,"wb") as d:
        d.write(file_data)
def get_chrome_version(platform, architecture):

    if(platform=="win"):
        process = subprocess.Popen(
            ['reg', 'query', 'HKEY_CURRENT_USER\\Software\\Google\\Chrome\\BLBeacon', '/v', 'version'],
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL
        )
        version = process.communicate()[0].decode('UTF-8').strip().split()[-1]
        version=version.split(".")[0]
    elif(platform=="linux"):
        process = subprocess.Popen(["google-chrome", "-version"], stdout=subprocess.PIPE)
        version = process.communicate()[0].decode().split("Google Chrome")[1].strip()
        version=version.split(".")[0]
    elif(platform=='darwin'):
        plistloc = "/Applications/Google Chrome.app/Contents/Info.plist"
        with open(plistloc, 'rb') as f:
            pl = plistlib.load(f)
        version = pl["CFBundleShortVersionString"]
        version=version.split(".")[0]
    return version
def get_chromedriver_filename(platform):
    if(platform=='win'):
        return 'chromedriver.exe'
    return 'chromedriver'
def get_chromedriver_url(version,platform, architecture):
    base_url = 'https://chromedriver.storage.googleapis.com/'
    return base_url + version + '/chromedriver_' + platform + architecture + '.zip'
def get_major_version(version):
    return version.split('.')[0]
def get_matched_chromedriver_version(version):
    doc = urllib.request.urlopen('https://chromedriver.storage.googleapis.com').read()
    root = elemTree.fromstring(doc)
    for k in root.iter('{http://doc.s3.amazonaws.com/2006-03-01}Key'):
        if k.text.find(get_major_version(version) + '.') == 0:
            return k.text.split('/')[0]
    return
def download_chromedriver():
    print("Downloading ChromeDriver...")
    platform, architecture=get_platform_architecture()
    chrome_version=get_chrome_version(platform, architecture)
    chromedriver_version = get_matched_chromedriver_version(chrome_version)
    url = get_chromedriver_url(chromedriver_version,platform, architecture)
    chromedriver_filename = get_chromedriver_filename(platform)
    response = urllib.request.urlopen(url)
    archive = BytesIO(response.read())
    with zipfile.ZipFile(archive) as zip_file:
        zip_file.extract(chromedriver_filename, "")
    edit_cdc_string(chromedriver_filename)
    try:
        os.chmod(chromedriver_filename, 0o775)
    except Exception as e:
        pass