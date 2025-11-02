import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from pages.practice_form_page import PracticeFormPage
from utils.helpers import resource_path
import os
import time

@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-infobars")
    # options.add_argument("--headless=new")  # descomente para rodar headless
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    yield driver
    driver.quit()

def test_submit_practice_form(driver):
    page = PracticeFormPage(driver)
    page.open_page()

    page.fill_name("João", "da Silva")
    page.fill_email("joao@email.com")
    page.choose_gender("Male")
    page.fill_mobile("9999999999")
    page.set_date_of_birth(day=10, month="October", year=1990)
    page.add_subject("Maths")
    page.choose_hobby("Sports")
    img_path = resource_path("C:/Users/Diego Holanda/Documents/projetos/desafio-DH/resources/ntt-img.png")
    page.upload_picture(img_path)
    page.fill_address("Rua dos Testes, 123")
    page.select_state("NCR")
    page.select_city("Delhi")

    page.submit()

    # 2. Validar submissão e tabela do modal
    modal_data = page.get_modal_table()

    assert modal_data.get("Student Name") == "João da Silva"
    assert modal_data.get("Student Email") == "joao@email.com"
    assert modal_data.get("Gender") == "Male"
    assert modal_data.get("Mobile") == "9999999999"
    assert modal_data.get("Date of Birth") == "10 October,1990" or modal_data.get("Date of Birth").startswith("10 Oct")
    assert "Maths" in modal_data.get("Subjects", "")
    assert "Sports" in modal_data.get("Hobbies", "")
    assert modal_data.get("Address") == "Rua dos Testes, 123"
    assert modal_data.get("State and City") == "NCR Delhi"

    # pausar para visualização manual
    time.sleep(3)

    page.close_modal()
