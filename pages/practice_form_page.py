from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pages.base_page import BasePage
import os
import time

class PracticeFormPage(BasePage):
    URL = "https://demoqa.com/automation-practice-form"

    # locators
    FIRST_NAME = (By.ID, "firstName")
    LAST_NAME = (By.ID, "lastName")
    EMAIL = (By.ID, "userEmail")
    GENDER_LABEL = "//label[text()='{gender}']" 
    MOBILE = (By.ID, "userNumber")
    DOB_INPUT = (By.ID, "dateOfBirthInput")
    SUBJECTS_INPUT = (By.ID, "subjectsInput")
    HOBBIES_LABEL = "//label[text()='{hobby}']"
    UPLOAD_INPUT = (By.ID, "uploadPicture")
    ADDRESS = (By.ID, "currentAddress")
    STATE_INPUT = (By.ID, "state")      
    CITY_INPUT = (By.ID, "city")  
    DROPDOWN_OPTIONS = (By.CSS_SELECTOR, "div[id^='react-select'] div.css-11unzgr")  # options of react-select
    SUBMIT_BUTTON = (By.ID, "submit")
    MODAL_DIALOG = (By.CLASS_NAME, "modal-content")
    MODAL_TABLE_ROWS = (By.CSS_SELECTOR, "table tbody tr")
    DOB_INPUT = (By.ID, "dateOfBirthInput")
    YEAR_SELECT = (By.CLASS_NAME, "react-datepicker__year-select")
    MONTH_SELECT = (By.CLASS_NAME, "react-datepicker__month-select")
    DAY_CELL = (By.CLASS_NAME, "react-datepicker__day")


    def open_page(self):
        self.open(self.URL)


    def fill_name(self, first, last):
        self.send_keys(self.FIRST_NAME, first)
        self.send_keys(self.LAST_NAME, last)

    def fill_email(self, email):
        self.send_keys(self.EMAIL, email)

    def choose_gender(self, gender_text):
        locator = (By.XPATH, self.GENDER_LABEL.format(gender=gender_text))
        self.click(locator)

    def fill_mobile(self, mobile):
        self.send_keys(self.MOBILE, mobile)

    def set_date_of_birth(self, day: int, month: int, year: int):

        self.click(self.DOB_INPUT)
        time.sleep(0.3)

        year_elem = self.wait.until(EC.presence_of_element_located(self.YEAR_SELECT))
        Select(year_elem).select_by_value(str(year))
        time.sleep(0.3)
        # foi necessário criar a lista de meses para que seja selecionado o indice, uma vez que é esperado o indice do mes
        months = [
            "January","February","March","April","May","June",
            "July","August","September","October","November","December"
        ]
        month = months.index(month)
        month_elem = self.wait.until(EC.presence_of_element_located(self.MONTH_SELECT))
        Select(month_elem).select_by_value(str(month))
        try:
            day_elements = self.wait.until(EC.presence_of_all_elements_located(self.DAY_CELL))
        except TimeoutException:
            raise RuntimeError("Não foi possível localizar os dias no datepicker.")

        for d in day_elements:
            if "outside-month" not in d.get_attribute("class") and d.text.strip() == str(day):
                d.click()
                break

    def add_subject(self, subject_text):
        # campo autocomplete: enviar texto e pressionar ENTER
        el = self.find(self.SUBJECTS_INPUT)
        el.send_keys(subject_text)
        el.send_keys(Keys.ENTER)

    def choose_hobby(self, hobby_text: str):
        # localiza todos os labels de hobbies
        hobby_labels = self.driver.find_elements(By.CSS_SELECTOR, "label[for^='hobbies-checkbox']")
        
        # percorre e clica no que corresponde ao texto desejado
        for label in hobby_labels:
            if label.text.strip().lower() == hobby_text.strip().lower():
                #scroll até o elemento antes de clicar
                self.driver.execute_script("arguments[0].scrollIntoView(true);", label)
                label.click()
                return

    def upload_picture(self, file_path):
        # garante caminho absoluto
        full_path = os.path.abspath(file_path)
        self.find(self.UPLOAD_INPUT).send_keys(full_path)

    def fill_address(self, address_text):
        self.send_keys(self.ADDRESS, address_text)

    def select_state(self, state_name: str):
        self.select_from_dropdown(
            self.STATE_INPUT,
            (By.CSS_SELECTOR, "div[id*='react-select'][class*='option']"), state_name
        )

    def select_city(self, city_name: str):
        self.select_from_dropdown(
            self.CITY_INPUT,
            (By.CSS_SELECTOR, "div[id*='react-select'][class*='option']"), city_name
        )

    def submit(self):
        btn = self.find(self.SUBMIT_BUTTON)
        self.execute_script("arguments[0].scrollIntoView(true);", btn)
        btn.click()

    def get_modal_table(self):
        self.find(self.MODAL_DIALOG)
        rows = self.driver.find_elements(*self.MODAL_TABLE_ROWS)
        data = {}
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) >= 2:
                key = cols[0].text.strip()
                value = cols[1].text.strip()
                data[key] = value
        return data

    def close_modal(self):
        close_btn = (By.ID, "closeLargeModal")
        self.click(close_btn)
