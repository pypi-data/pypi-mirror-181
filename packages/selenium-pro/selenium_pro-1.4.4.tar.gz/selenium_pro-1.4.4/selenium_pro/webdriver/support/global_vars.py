global global_driver
global_driver=""
global_browser=""
def set_global_driver(dr):
    global global_driver
    global_driver=dr
def get_global_driver():
    global global_driver
    return global_driver
def set_browser_name(br):
    global global_browser
    global_browser=br
def get_browser_name():
    global global_browser
    return global_browser