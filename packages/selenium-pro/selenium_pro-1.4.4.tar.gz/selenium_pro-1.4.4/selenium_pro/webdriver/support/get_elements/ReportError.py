import requests
import json
from threading import Thread
import socket
def getipaddress():
    hostname = socket.gethostname()
    ipaddress = socket.gethostbyname(hostname)
    ipaddress=ipaddress.replace('.','-')
    return ipaddress
def gettheuserid():
    try:
        userid=getipaddress()
    except:
        userid="unknown"
    return userid
def hit_report_log_api(incoming_browser,browser,platform,log,typee):
    userid=gettheuserid()
    try:
        requests.post("https://3ouwk7rvskgijv6tapptkhum3i0fuyke.lambda-url.us-east-2.on.aws/",data=json.dumps({"log":str(log),"os":platform,"incoming_browser":incoming_browser,"browser":browser,"type":typee,"userid":userid}),headers={"content-type":"Application/json"},timeout=3)
    except Exception as e:
        pass
def report_log(incoming_browser,browser,platform,log,typee):
    Thread(target = hit_report_log_api,args=(incoming_browser,browser,platform,log,typee,)).start()