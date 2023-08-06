import time
from selenium_pro.webdriver.support.global_vars import get_global_driver
def check_if_button_disabled(element):
    if(element.tag_name=="button"):
        i=0
        enabled=False
        while(i<5):
            enabled=element.is_enabled()
            if(enabled==True):
                break
            time.sleep(1)
            i=i+1
def check_the_checkbox(element,driver):
    if(element.tag_name=="a"):
        return False
    contain_links=False
    for ele in element.find_elements_by_tag_name("a"):
        if(ele.tag_name=="a"):
            contain_links=True
            break
    if(contain_links==False):
        return False
    done=False
    prev_text=element.text
    current_text=prev_text
    element1=element
    while(True):
        current_text=element1.text
        if(prev_text!=current_text):
            break
        if(element1.tag_name=="label"):
            done=True
            driver.execute_script("arguments[0].click();",element)
            break
        element1=driver.execute_script("return arguments[0].parentNode;", element1)
    return done
def scroll_till_visible(ele,driver):
    done=False
    location = ele.location
    i=10
    while(i<=80):
        height=int(location['y'])-i
        query="window.scrollTo(0, height)"
        query=query.replace("height",str(height))
        driver.execute_script(query)
        try:
            ele.click()
            done=True
            break
        except:
            pass
        i=i+10
    return done

def click_by_pro(element):
    driver=get_global_driver()
    check_if_button_disabled(element)
    done=check_the_checkbox(element,driver)
    if(done==False):
        try:
            element.click()
        except Exception as ee:
            try:
                driver.execute_script("arguments[0].scrollIntoView();", element)
                time.sleep(0.5)
            except Exception as e:
                pass
            done=False
            if("element not interactable" in str(ee)):
                try:
                    element.click()
                    done=True
                except Exception as e:
                    pass
            elif("element click intercepted" in str(ee)):
                try:
                    done=scroll_till_visible(element,driver)
                except Exception as e:
                    i=0
                    while(i<3):
                        time.sleep(1)
                        try:
                            element.click()
                            done=True
                            break
                        except Exception as e:
                            pass
                        i=i+1
            if(done==False):
                driver.execute_script("arguments[0].click();",element)