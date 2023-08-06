from ..chrome.webdriver import WebDriver as Chrome  # noqa
from ..firefox.webdriver import WebDriver as Firefox  # noqa
from ..edge.webdriver import WebDriver as Edge  # noqa
from ..safari.webdriver import WebDriver as Safari  # noqa
from .DownloadChromeDriver import *
from .DownloadGeckoDriver import *
from .DownloadEdgeDriver import *
from selenium_pro.webdriver.support.global_vars import *
from selenium_pro.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium_pro.webdriver.firefox.options import Options as firefox_optionss
from selenium_pro.webdriver.chrome.options import Options as chrome_optionss
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.core.utils import ChromeType
from selenium_pro.webdriver.support.get_elements.ReportError import *
import subprocess
import requests
import json
import platform
import urllib.request
from pathlib import Path
import plistlib
try:
    from winreg import *
except:
    pass
def get_chrome_version():
    process = subprocess.Popen(
        ['reg', 'query', 'HKEY_CURRENT_USER\\Software\\Google\\Chrome\\BLBeacon', '/v', 'version'],
        stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL
    )
    version = process.communicate()[0].decode('UTF-8').strip().split()[-1]
    version=version.split(".")[0]
    return version

def get_mac_default_browser():
    browser=""
    try:
        PREFERENCES = (
        Path.home(),"Library","Preferences","com.apple.LaunchServices/com.apple.launchservices.secure.plist")
        NAMES = {
            "com.apple.safari": "Safari",
            "com.google.chrome": "Chrome",
            "org.mozilla.firefox": "Firefox",
        }
        with PREFERENCES.open("rb") as fp:
            data = plistlib.load(fp)
        for handler in data["LSHandlers"]:
            if handler.get("LSHandlerURLScheme") == "http":
                role = handler["LSHandlerRoleAll"]
                browser = NAMES[role]
                return browser
    except:
        pass
    return "Safari"
def get_default_browser(platform):
    browser=""
    if(platform=="win"):
        with OpenKey(HKEY_CURRENT_USER, r"Software\\Microsoft\\Windows\\Shell\\Associations\\UrlAssociations\\http\\UserChoice") as key:
            browser = QueryValueEx(key, 'Progid')[0]
        if("chrome" in browser.lower()):
            browser="Chrome"
        elif("firefox" in browser.lower()):
            browser="Firefox"
        elif("msedge" in browser.lower()):
            browser="Edge"
        elif("safari" in browser.lower()):
            browser="Safari"
    elif(platform=="linux"):
        try:
            chrome_ver=get_chrome_version(platform, "")
        except:
            chrome_ver=""
        if(chrome_ver!=""):
            browser="Chrome"
        else:
            browser="Chrome"
    elif(platform=="mac"):
        browser=get_mac_default_browser()
    return browser
def check_if_ui_installed(chrome_options,firefox_options,options,browser):
    if(options==None and browser=="Chrome"):
        options=chrome_optionss()
    if(options==None and browser=="Firefox"):
        options=firefox_optionss()
    if(chrome_options==None and browser=="Chrome"):
        chrome_options=chrome_optionss()
    if(firefox_options==None and browser=="Firefox"):
        firefox_options=firefox_optionss()
    ui_installed=True
    output=os.popen('ls /usr/bin/*session').read()
    if(output.strip() in ['/usr/bin/byobu-select-session',  '/usr/bin/dbus-run-session']):
        ui_installed=False
    if(ui_installed==False):
        if(browser=="Chrome"):
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
        elif(browser=="Firefox"):
            firefox_options.headless=True
            options.headless=True
    return chrome_options,firefox_options,options
def get_the_things(browser,desired_capabilities,chrome_options,firefox_options,options):
    platform, architecture=get_platform_architecture()
    incoming_browser=browser
    if(browser==None):
        browser=get_default_browser(platform)
        if(browser==""):
            browser="Chrome"
        else:
            pass
    report_log(incoming_browser,browser,platform,"Start Driver Called","Log")
    file_extension=""
    if(platform=="win"):
        file_extension=".exe"
    if(desired_capabilities==None and browser=="Safari"):
        desired_capabilities=DesiredCapabilities.SAFARI
    if(platform=='linux'):
        chrome_options,firefox_options,options=check_if_ui_installed(chrome_options,firefox_options,options,browser)
    return platform,architecture,incoming_browser,browser,file_extension,chrome_options,firefox_options,options
def get_firefox_options(options,firefox_binary,platform,incoming_browser,browser):
    try:
        binary_location=options.binary_location
    except:
        binary_location=None
    if(firefox_binary==None and binary_location==None and platform=="win"):
        binary_location='C:/Program Files/Mozilla Firefox/firefox.exe'
        if(os.path.exists(binary_location)==False):
            binary_location='C:/Program Files (x86)/Mozilla Firefox/firefox.exe'
            if(os.path.exists(binary_location)==False):
                report_log(incoming_browser,browser,platform,"Could not found Firefox Binary Location please pass it in Options, e.g \noptions.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'","Error")
                raise RuntimeError("Could not found Firefox Binary Location please pass it in Options, e.g \noptions.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'")
        if(options==None):
            options=firefox_optionss()
        options.binary_location=binary_location
    return options
def open_chrome_browser(port,options,service_args,desired_capabilities,service_log_path,chrome_options,keep_alive,file_extension,incoming_browser,browser,platform):
    if(options==None):
        options=chrome_optionss()
    options.add_argument("--start-maximized")
    if(chrome_options==None):
        chrome_options=chrome_optionss()
    chrome_options.add_argument("--start-maximized")
    try:
        driver=Chrome(executable_path=ChromeDriverManager().install(), port=port,
             options=options, service_args=service_args,
             desired_capabilities=desired_capabilities, service_log_path=service_log_path,
             chrome_options=chrome_options, keep_alive=keep_alive)
    except Exception as e:
        report_log(incoming_browser,browser,platform,"Error in Simple Chrome:-"+str(e),"Error")
        if("chromedriver unexpectedly exited" in str(e)):
            try:
                driver=Chrome(executable_path="chromedriver"+file_extension, port=port,
             options=options, service_args=service_args,
             desired_capabilities=desired_capabilities, service_log_path=service_log_path,
             chrome_options=chrome_options, keep_alive=keep_alive)
            except Exception as e:
                report_log(incoming_browser,browser,platform,"Error in relative chrome:-"+str(e),"Error")
                try:
                    driver=Chrome(executable_path=ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install(), port=port,
                 options=options, service_args=service_args,
                 desired_capabilities=desired_capabilities, service_log_path=service_log_path,
                 chrome_options=chrome_options, keep_alive=keep_alive)
                except Exception as e:
                    report_log(incoming_browser,browser,platform,"Error in chromium chrome:-"+str(e),"Error")
                    raise RuntimeError(str(e))
        else:
            raise RuntimeError(str(e))
    return driver
def open_firefox_browser(firefox_profile, firefox_binary,timeout, capabilities, proxy, options,service_log_path, firefox_options,service_args, desired_capabilities, log_path,keep_alive,platform,incoming_browser,browser):
    try:
        options=get_firefox_options(options,firefox_binary,platform,incoming_browser,browser)
        driver=Firefox(firefox_profile=firefox_profile, firefox_binary=firefox_binary,
                 timeout=timeout, capabilities=capabilities, proxy=proxy,
                 executable_path=GeckoDriverManager().install(), options=options,
                 service_log_path=service_log_path, firefox_options=firefox_options,
                 service_args=service_args, desired_capabilities=desired_capabilities, log_path=log_path,
                 keep_alive=keep_alive)
    except Exception as e:
        raise RuntimeError(str(e))
    return driver
def open_edge_browser(browser,port,options, service_args,desired_capabilities, service_log_path,chrome_options, keep_alive,firefox_profile, firefox_binary,timeout, capabilities, proxy,firefox_options,log_path,verbose,reuse_service,quiet,platform, architecture,incoming_browser,file_extension):
    try:
        driver=Edge(executable_path=EdgeChromiumDriverManager().install(),capabilities=capabilities, port=port, verbose=verbose, service_log_path=service_log_path,log_path=log_path, keep_alive=keep_alive)
    except Exception as e:
        if("matching capabilities found" in str(e) and platform=="mac"):
            capabilities={}
            try:
                driver=Edge(executable_path=EdgeChromiumDriverManager().install(),capabilities=capabilities, port=port, verbose=verbose, service_log_path=service_log_path,log_path=log_path, keep_alive=keep_alive)
            except Exception as e:
                report_log(incoming_browser,browser,platform,"Error in trying Edge with caps:-"+str(e),"Error")
                raise RuntimeError(str(e))
        else:
            report_log(incoming_browser,browser,platform,"Error in trying Edge:-"+str(e),"Error")
            raise RuntimeError(str(e))
    return driver
def open_safari_browser(browser,port,options, service_args,desired_capabilities, service_log_path,chrome_options, keep_alive,firefox_profile, firefox_binary,timeout, capabilities, proxy,firefox_options,log_path,verbose,reuse_service,quiet,platform, architecture,incoming_browser,file_extension):
    try:
        driver=Safari(port=port, executable_path="/usr/bin/safaridriver"+file_extension, reuse_service=reuse_service,desired_capabilities=desired_capabilities, quiet=quiet,keep_alive=keep_alive, service_args=service_args)
    except Exception as e:
        report_log(incoming_browser,browser,platform,"Error in trying Safari:-"+str(e),"Error")
        raise RuntimeError(str(e))
    return driver
def try_all_browsers(browser,port,options, service_args,desired_capabilities, service_log_path,chrome_options, keep_alive,firefox_profile, firefox_binary,timeout, capabilities, proxy,firefox_options,log_path,verbose,reuse_service,quiet,platform, architecture,incoming_browser,file_extension):
    try:
        print("Opening Chrome...")
        driver=open_chrome_browser(port,options,service_args,desired_capabilities,service_log_path,chrome_options,keep_alive,file_extension,incoming_browser,browser,platform)
    except Exception as e:
        print("Trying Firefox...")
        report_log(incoming_browser,browser,platform,"Error in trying  Chrome first:-"+str(e),"Error")
        try:
            driver=open_firefox_browser(firefox_profile, firefox_binary,timeout, capabilities, proxy, options,service_log_path, firefox_options,service_args, desired_capabilities, log_path,keep_alive,platform,incoming_browser,browser)
        except Exception as e:
            print("Trying Edge...")
            report_log(incoming_browser,browser,platform,"Error in trying  Firefox second:-"+str(e),"Error")
            try:
                driver=open_edge_browser(browser,port,options, service_args,desired_capabilities, service_log_path,chrome_options, keep_alive,firefox_profile, firefox_binary,timeout, capabilities, proxy,firefox_options,log_path,verbose,reuse_service,quiet,platform, architecture,incoming_browser,file_extension)
            except Exception as e:
                print("Trying Safari...")
                report_log(incoming_browser,browser,platform,"Error in trying  Edge third:-"+str(e),"Error")
                try:
                    driver=open_safari_browser(browser,port,options, service_args,desired_capabilities, service_log_path,chrome_options, keep_alive,firefox_profile, firefox_binary,timeout, capabilities, proxy,firefox_options,log_path,verbose,reuse_service,quiet,platform, architecture,incoming_browser,file_extension)
                except Exception as e:
                    report_log(incoming_browser,browser,platform,"Error in trying  Safari fourth:-"+str(e),"Error")
                    raise RuntimeError("No Browser Found")
    try:
        driver.maximize_window()
    except:
        pass
    set_global_driver(driver)
    set_browser_name(browser)
    report_log(incoming_browser,browser,platform,"Browser Opened Successfully In Start","Log")
    return driver
def start_driver(browser=None,port=0,options=None, service_args=None,desired_capabilities=None, service_log_path="driver.log",chrome_options=None, keep_alive=True,
    firefox_profile=None, firefox_binary=None,timeout=30, capabilities=None, proxy=None,firefox_options=None,log_path=None,verbose=None,
    reuse_service=False,quiet=False):
    platform, architecture,incoming_browser,browser,file_extension,chrome_options,firefox_options,options=get_the_things(browser,desired_capabilities,chrome_options,firefox_options,options)
    if(incoming_browser==None):
        driver=try_all_browsers(browser,port,options, service_args,desired_capabilities, service_log_path,chrome_options, keep_alive,firefox_profile, firefox_binary,timeout, capabilities, proxy,firefox_options,log_path,verbose,reuse_service,quiet,platform, architecture,incoming_browser,file_extension)
        return driver
    if(browser=="Chrome"):
        driver=open_chrome_browser(port,options,service_args,desired_capabilities,service_log_path,chrome_options,keep_alive,file_extension,incoming_browser,browser,platform)
    elif(browser=="Firefox"):
        driver=open_firefox_browser(firefox_profile, firefox_binary,timeout, capabilities, proxy, options,service_log_path, firefox_options,service_args, desired_capabilities, log_path,keep_alive,platform,incoming_browser,browser)
    elif(browser=="Edge"):
        driver=open_edge_browser(browser,port,options, service_args,desired_capabilities, service_log_path,chrome_options, keep_alive,firefox_profile, firefox_binary,timeout, capabilities, proxy,firefox_options,log_path,verbose,reuse_service,quiet,platform, architecture,incoming_browser,file_extension)
    elif(browser=="Safari"):
        open_safari_browser(browser,port,options, service_args,desired_capabilities, service_log_path,chrome_options, keep_alive,firefox_profile, firefox_binary,timeout, capabilities, proxy,firefox_options,log_path,verbose,reuse_service,quiet,platform, architecture,incoming_browser,file_extension)
    if(browser not in ["Chrome","Firefox","Edge","Safari"]):
        report_log(incoming_browser,browser,platform,"This function only supports Firefox, Chrome, Edge and Safari","Error")
        raise RuntimeError("This function only supports Firefox, Chrome, Edge and Safari")
    try:
        driver.maximize_window()
    except:
        pass
    set_global_driver(driver)
    set_browser_name(browser)
    report_log(incoming_browser,browser,platform,"Browser Opened Successfully","Log")
    return driver