import sys
import os
import subprocess
import urllib.request
import zipfile
import xml.etree.ElementTree as elemTree
from io import BytesIO
import plistlib
import requests
from bs4 import BeautifulSoup
import tarfile
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
        raise RuntimeError('Could not determine geckodriver download URL for this platform.')
    return platform, architecture
def edit_cdc_string(geckodriver_filename):
    with open(geckodriver_filename,"rb") as d:
        file_data=d.read()
    file_data=file_data.replace(b"cdc_",b"tch_")
    with open(geckodriver_filename,"wb") as d:
        d.write(file_data)
def get_geckodriver_filename():
    if sys.platform.startswith('win'):
        return 'geckodriver.exe'
    return 'geckodriver'
def get_geckodriver_url(platform, architecture):
    result = requests.get("https://github.com/mozilla/geckodriver/releases")
    if not result.ok:
        raise RuntimeError('Could not determine geckodriver version')
    soup = BeautifulSoup(result.content, 'html.parser')
    for a in soup.find_all("a"):
        if("/mozilla/geckodriver/releases/download" in a["href"]):
            if(a["href"].strip().endswith("win32.zip") and platform=="win"):
                url=a["href"]
                break
            elif(a["href"].strip().endswith("linux64.tar.gz") and platform=="linux"):
                url=a["href"]
                break
            elif(a["href"].strip().endswith("macos.tar.gz") and platform=="mac"):
                url=a["href"]
                break
    return "https://github.com"+url

def download_geckodriver():
    print("Downloading Geckodriver...")
    platform, architecture=get_platform_architecture()
    url=get_geckodriver_url(platform, architecture)
    geckodriver_filename = get_geckodriver_filename()
    response = urllib.request.urlopen(url)
    archive = BytesIO(response.read())
    if(url.endswith(".zip")):
        with zipfile.ZipFile(archive) as zip_file:
            zip_file.extract(geckodriver_filename, "")
    else:
        tar = tarfile.open(fileobj=archive, mode='r:gz')
        tar.extract(geckodriver_filename)
        tar.close()
    try:
        os.chmod(geckodriver_filename, 0o775)
    except Exception as e:
        pass