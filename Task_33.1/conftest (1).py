import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import random
import string
import re
import time

@pytest.fixture(scope="function")
def browser():
    # отображение графического окна
    service = Service(ChromeDriverManager().install())
    browser = webdriver.Chrome(service=service)

    # Настройка параметров Chrome для headless режима
    # chrome_options = Options()
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--disable-gpu")
    # chrome_options.add_argument("--no-sandbox")
    # chrome_options.add_argument("--disable-dev-shm-usage")
    #
    # # Использование webdriver_manager для автоматического скачивания и запуска ChromeDriver
    # service = Service(ChromeDriverManager().install())
    # browser = webdriver.Chrome(service=service, options=chrome_options)

    yield browser
    browser.quit()


# Фикстура для открытия страницы авторизации
@pytest.fixture(scope="function")
def open_auth_page(browser):
    browser.get("https://start.rt.ru/")
    yield

@pytest.fixture(scope='function')
def open_password_recovery_page(browser):
    def _open():
        browser.get(
        'https://b2c.passport.rt.ru/auth/realms/b2c/login-actions/reset-credentials?client_id=lk_b2c&tab_id=LyCXSrIiNEE')
    return _open

@pytest.fixture
def generate_phone_number():
    def _generate_phone_number():
        phone_number = '+7' + ''.join([str(random.randint(0, 9)) for _ in range(10)])
        return phone_number
    return _generate_phone_number

@pytest.fixture
def generate_phone_number_1():
    def _generate_phone_number_1():
        phone_number = '+7' + ''.join(random.choice('0123456789') for _ in range(10))
        return phone_number
    return _generate_phone_number_1

@pytest.fixture
def generate_password():
    def _generate_password(length=12):
        if length < 4:
            raise ValueError("Длина пароля должна быть не менее 4 символов.")

        chars = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"
        upper = random.choice(string.ascii_uppercase)
        lower = random.choice(string.ascii_lowercase)
        digit = random.choice(string.digits)
        special = random.choice("!@#$%^&*()")
        other_characters = ''.join(random.choice(chars) for _ in range(length - 4))
        password = upper + lower + digit + special + other_characters
        password = ''.join(random.sample(password, len(password)))
        return password
    return _generate_password

@pytest.fixture
def generate_cyrillic_name():
    def _generate_cyrillic_name(min_length=5, max_length=10):
        letters = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
        return ''.join(random.choice(letters) for _ in range(random.randint(min_length, max_length)))
    return _generate_cyrillic_name

@pytest.fixture
def generate_cyrillic_name_boundary_1():
    def _generate_cyrillic_name_boundary_1(min_length=1, max_length=1):
        letters = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
        return ''.join(random.choice(letters) for _ in range(random.randint(min_length, max_length)))
    return _generate_cyrillic_name_boundary_1

@pytest.fixture
def generate_cyrillic_name_boundary_2():
    def _generate_cyrillic_name_boundary_2(min_length=31, max_length=32):
        letters = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
        return ''.join(random.choice(letters) for _ in range(random.randint(min_length, max_length)))
    return _generate_cyrillic_name_boundary_2

@pytest.fixture
def generate_cyrillic_email(generate_cyrillic_name):
    def _generate_cyrillic_email():
        local_part = generate_cyrillic_name()
        domain = 'example.рф'  # Пример кириллического домена
        return f"{local_part}@{domain}"
    return _generate_cyrillic_email

@pytest.fixture
def generate_email_with_special_domain():
    def _generate_email_with_special_domain():
        local_part = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        special_characters = ['#', '!', '%', '^', '&', '*', '+', '=', '~', ',', '.', ';', ':', '?', '/', '\\']
        special_char = random.choice(special_characters)
        special_domain = f"example{special_char}domain.com"
        return f"{local_part}@{special_domain}"
    return _generate_email_with_special_domain
