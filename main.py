import os
import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


def read_login_items():
    t_login = os.environ['TLOGIN']
    t_password = os.environ['TPASSWORD']
    return t_login, t_password


def read_sms_text():
    file = open("smstext.txt", "r", encoding='utf8')
    return file.read()


def wait_for_element(self, *locator, timeout=None):
    timeout = timeout or 2
    return WebDriverWait(self, timeout).until(
        expected_conditions.visibility_of_element_located(locator))


def send_sms(recipient, sms_text, t_login, t_pass):
    d = webdriver.Chrome()
    d.get("http://www.t-mobile.cz")

    try:
        iframe = d.find_element_by_xpath("//iframe[@class='gdpr-iframe']")
        d.switch_to.frame(iframe)
        accept_button = wait_for_element(d, By.ID, "acceptAllQuick")
        accept_button.click()
        d.switch_to.default_content()
    except:
        pass

    try:
        login = wait_for_element(d, By.XPATH, '//span[contains(text(), "Přihlásit")]')
        login.click()

        pass_tab = wait_for_element(d, By.ID, "passwordtab")
        pass_tab.click()

        username = wait_for_element(d, By.ID, "username")
        username.click()
        username.send_keys(t_login)

        password = wait_for_element(d, By.ID, "password")
        password.click()
        password.send_keys(t_pass)
        password.send_keys(Keys.ENTER)

        time.sleep(5)

        send_sms = wait_for_element(d, By.XPATH, '//i[@class="ico-sms no-svg-ico"]')
        send_sms.click()

        recipient_number = wait_for_element(d, By.XPATH, '//input[@type="text"]')
        recipient_number.click()
        recipient_number.send_keys(recipient)
        box_content = wait_for_element(d, By.XPATH, '//div[@class="box-content"]')
        box_content.click()

        text = wait_for_element(d, By.ID, 'smsText')
        text.click()
        text.send_keys(sms_text)

        submit_btn = wait_for_element(d, By.ID, 'submitButton')
        submit_btn.click()
        d.close()

    except:
        d.close()


def main():
    tlogin, tpassword = read_login_items()
    # recipient = '777'
    recipient = sys.argv[1]
    sms_text = read_sms_text()
    send_sms(recipient, sms_text, tlogin, tpassword)

if __name__ == "__main__":
    main()

