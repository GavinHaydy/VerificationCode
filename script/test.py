import json
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


caps = DesiredCapabilities.CHROME
caps['loggingPrefs'] = {
    'browser': 'ALL',
    'performance': 'ALL'
}
caps['perfLoggingPrefs'] = {
    'enableNetwork' : True,
    'enablePage' : False,
    'enableTimeline' : False
    }

option = webdriver.ChromeOptions()
option.add_argument('--no-sandbox')     # 彻底停用沙箱
# option.add_argument('--headless')     # 无界面模式
# option.add_argument("--disable-extensions")    # 禁用拓展
# option.add_argument("--allow-running-insecure-content")  # 放行javascript/css/plug-ins等内容
# option.add_argument("--ignore-certificate-errors")  # 忽略与证书相关的错误
# option.add_argument("--disable-single-click-autofill")  # kEnableSingleClickAutofill的“禁用”标志
# option.add_argument("--disable-autofill-keyboard-accessory-view[8]")
# option.add_argument("--disable-full-form-autofill-ios")
# option.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:55.0) Gecko/20100101 Firefox/55.0')
option.add_experimental_option('w3c', False)
option.add_experimental_option('perfLoggingPrefs',{
    'enableNetwork': True,
    'enablePage': False,
})
pattern = re.compile(r'getGraphicCode')     # 正则匹配接口
driver = webdriver.Chrome(options=option, desired_capabilities=caps)
driver.get('url')
driver.maximize_window()
for typelog in driver.log_types:
    perfs = driver.get_log(typelog)
    for row in perfs:
        log_data = row['message']  # str ['params']
        l = pattern.search(log_data)
        if l is not None:
            log = json.loads(log_data)
            requestId = log['message']['params']['requestId']
            try:
                response_body = driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': requestId})
                x = json.loads(response_body['body'])
                verifyCode = x['result']['verifyCode']
            except:
                pass
driver.find_element_by_xpath('/html/body/div/div[1]/div[1]/div/div[2]/div/form/div[1]/div/div[2]/input').send_keys('xxxxxxxxxxxx')
driver.find_element(By.XPATH, '/html/body/div/div[1]/div[1]/div/div[2]/div/form/div[2]/div/div[2]/input').send_keys('xxxxxxx')
driver.find_element(By.XPATH, '/html/body/div/div[1]/div[1]/div/div[2]/div/form/div[3]/div/div[2]/input').send_keys(verifyCode)
driver.find_element(By.XPATH, '/html/body/div/div[1]/div[1]/div/div[2]/div/form/div[5]/div/button').click()
