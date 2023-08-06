from selenium_pro.webdriver.common.keys import Keys
import time
from .GetKeyCodes import get_key_code,keys_code_dic
from selenium_pro.webdriver.support.global_vars import get_global_driver
def get_list_keys(key):
    if(type(key)==type([])):
        return key
    keys_code=[]
    lst_kys=key.split("+")
    lent=len(lst_kys)
    iterator=1
    for item in lst_kys:
        code=get_key_code(item)
        if(code==None):
            code=item
            if(iterator<lent):
                code=item+"+"
        keys_code.append(code)
        iterator=iterator+1
    return keys_code
def find_element_for_key(ele):
    new_ele=ele
    ele.send_keys("PUBLICACEG123")
    all_eles=ele.find_elements_by_tag_name("*")
    all_eles.append(ele)
    for el in all_eles:
        if(el.get_attribute("innerHTML")=="PUBLICACEG123"):
            new_ele=el
            break
    return new_ele
def keypress(key,ele,driver):
    keys_code=get_list_keys(key)
    code=""
    if(type(key)!=type([])):
        item=key.upper()
        code=get_key_code(item)
    try:
        if(len(keys_code)==1):
            if("\n" in str(keys_code[0])):
                keys_code=keys_code[0]
                keys_code=keys_code.replace("\n","\ue008\ue007\ue008")
        ele.send_keys(keys_code)
    except Exception as e:
        if("not interactable" in str(e) and len(keys_code)==1 and code==None):
            query="arguments[0].value='key';"
            query=query.replace("key",str(keys_code[0]))
            driver.execute_script(query, ele);
        elif("only supports characters in the BMP" in str(e)):
            if(ele.tag_name!="input"):
                ele=find_element_for_key(ele)
                driver.execute_script("arguments[0].innerHTML = arguments[1]",ele,key)
                time.sleep(1)
                ele.send_keys(' ')
                ele.send_keys(Keys.BACKSPACE)
            else:
                driver.execute_script("arguments[0].value = arguments[1]",ele,key)
            code=""
    if(len(keys_code)>1 and type(key)!=type([])):
        code=key
    return code
def type_by_pro(element,key):
    key_done=False
    i=0
    driver=get_global_driver()
    while(i<5):
        #element=driver.switch_to.active_element
        value_before=element.get_attribute("value")
        text_before=element.text
        code=keypress(key,element,driver)
        try:
            value_after=element.get_attribute("value")
            text_after=element.text
        except:
            value_after=""
            text_after=""
        if(code==None):
            if(text_before!=text_after):
                key_done=True
            elif(value_before!=value_after):
                key_done=True
            if(key_done==True):
                break
        else:
            break
        time.sleep(1)
        i=i+1