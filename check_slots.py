from selenium import webdriver
import time
import datetime
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options
import twilio
from twilio.rest import Client


def send_message(to_num, from_num, message, twilio_account_sid, twilio_auth_token):
    try:
        client = Client(twilio_account_sid, twilio_auth_token)
        client.messages.create(to=to_num, from_=from_num, body=message)
    except Exception as e:
        print("Some problem occured in sending message: {}".format(e))


def call(twiml_url, from_num, to_num, twilio_account_sid, twilio_auth_token):
    client = Client(twilio_account_sid, twilio_auth_token)
    call = client.calls.create(from_=from_num, to=to_num, url=twiml_url)


def send_email(gmail_id, gmail_pass, message, to_email_id):
    try:
        import smtplib

        s = smtplib.SMTP("smtp.gmail.com", 587)  # creates SMTP session
        s.starttls()  # start TLS for security
        s.login(gmail_id, gmail_pass)  # Authentication
        s.sendmail(gmail_id, to_email_id, message)  # sending the mail
        s.quit()  # terminating the session
    except Exception as e:
        print("Some error occured in sending email: {}".format(e))


if __name__ == "__main__":

    # define all the variables here
    # VFS login credentials
    vfs_email_address = "your-vfs-account-email-address"
    vfs_account_password = "your-vfs-account-password"
    # Twilio credentials
    twilio_sid = "your-twilio-sid"
    twilio_token = "your-twilio-token"
    from_num = "twilio-number-to-receive-text-and-call-from"
    to_num = "number-on-which-to-receive-text-and-call"
    twiml_url = "your-twilio-url"
    # interval between consecutive checking
    interval = 120


    ##############################################################
    while True:
        try:
            # check for Blue card slot
            print("Checking for Bluecard category")

            firefox_options = Options()
            # open in headless mode to run in background
            firefox_options.headless = True
            # firefox_options.add_argument("start-maximized")
            # following options reduce the RAM usage
            firefox_options.add_argument("disable-infobars")
            firefox_options.add_argument("--disable-extensions")
            firefox_options.add_argument("--no-sandbox")
            firefox_options.add_argument("--disable-application-cache")
            firefox_options.add_argument("--disable-gpu")
            firefox_options.add_argument("--disable-dev-shm-usage")
            driver = webdriver.Firefox(options=firefox_options)

            # make sure that the browser is full screen, else some buttons will not be visible to selenium
            driver.maximize_window()

            # open the webpage
            driver.get("https://visa.vfsglobal.com/ind/en/deu/login")

            # logging in
            time.sleep(
                10
            )  # sleep provides sufficient time for all the elements to get visible
            uname = driver.find_element_by_xpath("//input[@id='mat-input-0']")
            uname.send_keys(vfs_email_address)
            pwd = driver.find_element_by_xpath("//input[@id='mat-input-1']")
            pwd.send_keys(vfs_account_password)
            sign_in_button = driver.find_element_by_xpath("//button/span")
            sign_in_button.click()
            time.sleep(10)

            # select from drop down
            new_booking_button = driver.find_element_by_xpath(
                "//section/div/div[2]/button/span"
            )
            new_booking_button.click()
            time.sleep(5)
            drop_down_button = driver.find_element_by_xpath(
                "//mat-form-field/div/div/div[3]"
            )
            drop_down_button.click()
            time.sleep(2)
            delhi_option = driver.find_element_by_xpath(
                "//mat-option[@id='mat-option-10']/span"
            )
            delhi_option.click()
            time.sleep(5)
            appointment_category_dropdown_button = driver.find_element_by_xpath(
                "//div[@id='mat-select-value-3']"
            )
            appointment_category_dropdown_button.click()
            time.sleep(5)
            bluecard_category = driver.find_element_by_xpath(
                "//mat-option[@id='mat-option-18']/span"
            )
            bluecard_category.click()
            time.sleep(5)
            subcategory_dropdown = driver.find_element_by_xpath(
                "//div[@id='mat-select-value-5']"
            )
            # subcategory_dropdown.click()
            driver.execute_script("arguments[0].click();", subcategory_dropdown)
            time.sleep(5)
            try:
                try:
                    bluecard_subcategory = driver.find_element_by_xpath(
                        "//mat-option[@id='mat-option-27']/span"
                    )
                except Exception:
                    bluecard_subcategory = driver.find_element_by_xpath(
                        "//mat-option[@id='mat-option-28']/span"
                    )
                # bluecard_subcategory.click()
                driver.execute_script("arguments[0].click();", bluecard_subcategory)
            except Exception as e:
                print("some error in bluecard subcategory: ", e)
                pass
            time.sleep(5)

            # read contents of the text box
            message_box = driver.find_element_by_xpath("//div[4]/div")
            if message_box.text != "No appointment slots are currently available":
                print("Message: ", message_box.text)
                # Earliest Available Slot : 30/11/2021
                print("Sending message and calling")
                ts = time.time()
                st = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
                message = "{} at {}".format(message_box.text, st)
                send_message(to_num, from_num, message, twilio_sid, twilio_token)
                print("message sent")
                # call
                call(twiml_url, from_num, to_num, twilio_sid, twilio_token)
                print("called")

            # Close the browser
            driver.close()
            driver.quit()
            print("sleeping for 2 mins")
            time.sleep(interval)
        except Exception as e:
            print("some error ", e)
            print("sleeping for a minute")
            time.sleep(60)
            pass
