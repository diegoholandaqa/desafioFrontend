from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class BasePage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def open(self, url):
        self.driver.get(url)

    def find(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_clickable(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator))

    def click(self, locator):
        el = self.find_clickable(locator)
        el.click()

    def send_keys(self, locator, text, clear_first=True):
        el = self.find(locator)
        if clear_first:
            el.clear()
        el.send_keys(text)

    def execute_script(self, script, *args):
        return self.driver.execute_script(script, *args)

    def wait_for_element_invisible(self, locator):
        try:
            return self.wait.until(EC.invisibility_of_element_located(locator))
        except TimeoutException:
            return False

    def select_from_dropdown(self, field_locator, options_locator, option_text: str):
        # Clica em um campo dropdown e seleciona a opção pelo texto.
        
        self.click(field_locator)
        
        # Aguarda e percorre todas as opções disponíveis
        options = self.driver.find_elements(*options_locator)
        for opt in options:
            if opt.text.strip().lower() == option_text.strip().lower():
                opt.click()
                return