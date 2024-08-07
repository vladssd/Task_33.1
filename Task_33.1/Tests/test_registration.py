import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from faker import Faker
import random
import string
import re
import time
from faker.providers import internet

fake = Faker('ru_RU')

@pytest.fixture
def browser():
    from selenium import webdriver
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

@pytest.mark.negative
def test_registration_negative_latin_letters(browser, generate_password):
    fake = Faker()
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = fake.email()
    password = generate_password(12)

    browser.get(
        "https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth?client_id=lk_b2c&redirect_uri=https%3A%2F%2Flk-api.rt.ru%2Fsso-auth%2F%3Fredirect%3Dhttps%253A%252F%252Fstart.rt.ru%252F&response_type=code&scope=openid")

    next_button = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "standard_auth_btn"))
    )
    next_button.click()

    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "kc-register"))
    )

    phone_tab_button = browser.find_element(By.ID, "kc-register")
    phone_tab_button.click()

    first_name_input = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located(
            (By.XPATH,
             '//input[@class="rt-input__input rt-input__input--rounded rt-input__input--orange" and @name="firstName"]'))
    )
    first_name_input.send_keys(first_name)

    last_name_input = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located(
            (By.XPATH,
             '//input[@class="rt-input__input rt-input__input--rounded rt-input__input--orange" and @type="text" and @name="lastName"]')
        )
    )
    last_name_input.send_keys(last_name)

    region_input = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located(
            (By.XPATH,
             "//div[@class='rt-input rt-input--rounded rt-input--orange rt-input--actions']//input[@class='rt-input__input rt-select__input rt-input__input--rounded rt-input__input--orange' and @type='text']"))
    )
    region_input.send_keys("Москва г")

    address_input = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "address"))
    )
    address_input.send_keys(email)

    password_input = browser.find_element(By.NAME, "password")
    password_input.send_keys(password)

    confirm_password_input = browser.find_element(By.NAME, "password-confirm")
    confirm_password_input.send_keys(password)

    try:
        register_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                                        "button.rt-btn.rt-btn--orange.rt-btn--medium.rt-btn--rounded.register-form__reg-btn[name='register']"))
        )
        register_button.click()
    except TimeoutException:
        print("Кнопка 'Зарегистрироваться' не была найдена или не была кликабельна.")
        assert False, "Кнопка 'Зарегистрироваться' не была найдена или не была кликабельна."

    # Добавляем проверку на успешность регистрации
    success_message = WebDriverWait(browser, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "success-message-class"))
        # замените на реальный класс или идентификатор сообщения об успехе
    )
    assert success_message is not None, "Регистрация не удалась"

    expected_url = "https://b2c.passport.rt.ru/auth/realms/b2c/login-actions/authenticate?client_id=lk_b2c&tab_id=ka7pfwvoauI"
    WebDriverWait(browser, 20).until(
        EC.url_to_be(expected_url)
    )
    assert browser.current_url == expected_url, f"Expected URL: {expected_url}, but got {browser.current_url}"

    response_status = browser.execute_script("return window.performance.getEntries()[0].responseStart;")
    assert response_status == 200, f"Expected status code 200, but got {response_status}"

@pytest.mark.email
def test_registration_by_email(browser, generate_cyrillic_name ,generate_password):
    fake = Faker()
    first_name = generate_cyrillic_name()
    last_name = generate_cyrillic_name()
    email = fake.email()
    password = generate_password(12)

    browser.get(
        "https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth?client_id=lk_b2c&redirect_uri=https%3A%2F%2Flk-api.rt.ru%2Fsso-auth%2F%3Fredirect%3Dhttps%253A%252F%252Fstart.rt.ru%252F&response_type=code&scope=openid")

    next_button = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "standard_auth_btn"))
    )
    next_button.click()

    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "kc-register"))
    )

    phone_tab_button = browser.find_element(By.ID, "kc-register")
    phone_tab_button.click()

    first_name_input = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located(
            (By.XPATH,
             '//input[@class="rt-input__input rt-input__input--rounded rt-input__input--orange" and @name="firstName"]'))
    )
    first_name_input.send_keys(first_name)

    last_name_input = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located(
            (By.XPATH,
             '//input[@class="rt-input__input rt-input__input--rounded rt-input__input--orange" and @type="text" and @name="lastName"]')
        )
    )
    last_name_input.send_keys(last_name)

    region_input = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located(
            (By.XPATH,
             "//div[@class='rt-input rt-input--rounded rt-input--orange rt-input--actions']//input[@class='rt-input__input rt-select__input rt-input__input--rounded rt-input__input--orange' and @type='text']"))
    )
    region_input.send_keys("Москва г")

    address_input = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "address"))
    )
    address_input.send_keys(email)

    password_input = browser.find_element(By.NAME, "password")
    password_input.send_keys(password)

    confirm_password_input = browser.find_element(By.NAME, "password-confirm")
    confirm_password_input.send_keys(password)

    try:
        register_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                                        "button.rt-btn.rt-btn--orange.rt-btn--medium.rt-btn--rounded.register-form__reg-btn[name='register']"))
        )
        register_button.click()
    except TimeoutException:
        print("Кнопка 'Зарегистрироваться' не была найдена или не была кликабельна.")
        assert False, "Кнопка 'Зарегистрироваться' не была найдена или не была кликабельна."

        # Ожидание изменения URL в браузере
    WebDriverWait(browser, 5).until(
        EC.url_changes(
            "https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth?client_id=lk_b2c&redirect_uri=https%3A%2F%2Flk-api.rt.ru%2Fsso-auth%2F%3Fredirect%3Dhttps%253A%252F%252Fstart.rt.ru%252F&response_type=code&scope=openid")
    )

    current_url = browser.current_url
    assert current_url != "https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth?client_id=lk_b2c&redirect_uri=https%3A%2F%2Flk-api.rt.ru%2Fsso-auth%2F%3Fredirect%3Dhttps%253A%252F%252Fstart.rt.ru%252F&response_type=code&scope=openid", "URL не изменился после регистрации"

    print(f"Текущий URL после регистрации: {current_url}")

@pytest.mark.email
def test_registration_by_email_boundary_1(browser, generate_cyrillic_name, generate_cyrillic_name_boundary_1 ,generate_password): #  минимальная граница ФИО
    fake = Faker()
    first_name = generate_cyrillic_name_boundary_1()
    last_name = generate_cyrillic_name()
    email = fake.email()
    password = generate_password(12)

    browser.get(
        "https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth?client_id=lk_b2c&redirect_uri=https%3A%2F%2Flk-api.rt.ru%2Fsso-auth%2F%3Fredirect%3Dhttps%253A%252F%252Fstart.rt.ru%252F&response_type=code&scope=openid")

    next_button = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "standard_auth_btn"))
    )
    next_button.click()

    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "kc-register"))
    )

    phone_tab_button = browser.find_element(By.ID, "kc-register")
    phone_tab_button.click()

    first_name_input = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located(
            (By.XPATH,
             '//input[@class="rt-input__input rt-input__input--rounded rt-input__input--orange" and @name="firstName"]'))
    )
    first_name_input.send_keys(first_name)

    last_name_input = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located(
            (By.XPATH,
             '//input[@class="rt-input__input rt-input__input--rounded rt-input__input--orange" and @type="text" and @name="lastName"]')
        )
    )
    last_name_input.send_keys(last_name)

    region_input = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located(
            (By.XPATH,
             "//div[@class='rt-input rt-input--rounded rt-input--orange rt-input--actions']//input[@class='rt-input__input rt-select__input rt-input__input--rounded rt-input__input--orange' and @type='text']"))
    )
    region_input.send_keys("Москва г")

    address_input = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "address"))
    )
    address_input.send_keys(email)

    password_input = browser.find_element(By.NAME, "password")
    password_input.send_keys(password)

    confirm_password_input = browser.find_element(By.NAME, "password-confirm")
    confirm_password_input.send_keys(password)

    try:
        register_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                                        "button.rt-btn.rt-btn--orange.rt-btn--medium.rt-btn--rounded.register-form__reg-btn[name='register']"))
        )
        register_button.click()
    except TimeoutException:
        print("Кнопка 'Зарегистрироваться' не была найдена или не была кликабельна.")
        assert False, "Кнопка 'Зарегистрироваться' не была найдена или не была кликабельна."

        # Ожидание изменения URL в браузере
    WebDriverWait(browser, 5).until(
        EC.url_changes(
            "https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth?client_id=lk_b2c&redirect_uri=https%3A%2F%2Flk-api.rt.ru%2Fsso-auth%2F%3Fredirect%3Dhttps%253A%252F%252Fstart.rt.ru%252F&response_type=code&scope=openid")
    )

    current_url = browser.current_url
    assert current_url != "https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth?client_id=lk_b2c&redirect_uri=https%3A%2F%2Flk-api.rt.ru%2Fsso-auth%2F%3Fredirect%3Dhttps%253A%252F%252Fstart.rt.ru%252F&response_type=code&scope=openid", "URL не изменился после регистрации"

    print(f"Текущий URL после регистрации: {current_url}")

@pytest.mark.email
def test_registration_by_email_boundary_2(browser, generate_cyrillic_name, generate_cyrillic_name_boundary_2,
                                              generate_password):  # максимальная граница ФИО
        fake = Faker()
        first_name = generate_cyrillic_name()
        last_name = generate_cyrillic_name_boundary_2()
        email = fake.email()
        password = generate_password(12)

        browser.get(
            "https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth?client_id=lk_b2c&redirect_uri=https%3A%2F%2Flk-api.rt.ru%2Fsso-auth%2F%3Fredirect%3Dhttps%253A%252F%252Fstart.rt.ru%252F&response_type=code&scope=openid")

        next_button = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, "standard_auth_btn"))
        )
        next_button.click()

        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, "kc-register"))
        )

        phone_tab_button = browser.find_element(By.ID, "kc-register")
        phone_tab_button.click()

        first_name_input = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located(
                (By.XPATH,
                 '//input[@class="rt-input__input rt-input__input--rounded rt-input__input--orange" and @name="firstName"]'))
        )
        first_name_input.send_keys(first_name)

        last_name_input = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located(
                (By.XPATH,
                 '//input[@class="rt-input__input rt-input__input--rounded rt-input__input--orange" and @type="text" and @name="lastName"]')
            )
        )
        last_name_input.send_keys(last_name)

        region_input = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located(
                (By.XPATH,
                 "//div[@class='rt-input rt-input--rounded rt-input--orange rt-input--actions']//input[@class='rt-input__input rt-select__input rt-input__input--rounded rt-input__input--orange' and @type='text']"))
        )
        region_input.send_keys("Москва г")

        address_input = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, "address"))
        )
        address_input.send_keys(email)

        password_input = browser.find_element(By.NAME, "password")
        password_input.send_keys(password)

        confirm_password_input = browser.find_element(By.NAME, "password-confirm")
        confirm_password_input.send_keys(password)

        try:
            register_button = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR,
                                            "button.rt-btn.rt-btn--orange.rt-btn--medium.rt-btn--rounded.register-form__reg-btn[name='register']"))
            )
            register_button.click()
        except TimeoutException:
            print("Кнопка 'Зарегистрироваться' не была найдена или не была кликабельна.")
            assert False, "Кнопка 'Зарегистрироваться' не была найдена или не была кликабельна."

            # Ожидание изменения URL в браузере
        WebDriverWait(browser, 5).until(
            EC.url_changes(
                "https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth?client_id=lk_b2c&redirect_uri=https%3A%2F%2Flk-api.rt.ru%2Fsso-auth%2F%3Fredirect%3Dhttps%253A%252F%252Fstart.rt.ru%252F&response_type=code&scope=openid")
        )

        current_url = browser.current_url
        assert current_url != "https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth?client_id=lk_b2c&redirect_uri=https%3A%2F%2Flk-api.rt.ru%2Fsso-auth%2F%3Fredirect%3Dhttps%253A%252F%252Fstart.rt.ru%252F&response_type=code&scope=openid", "URL не изменился после регистрации"

        print(f"Текущий URL после регистрации: {current_url}")

@pytest.mark.email
def test_registration_by_fake_email(browser, generate_cyrillic_name, generate_cyrillic_email, generate_password):
    fake = Faker('ru_RU')  # Используем русский локальный провайдер
    fake.add_provider(internet)

    first_name = generate_cyrillic_name()
    last_name = generate_cyrillic_name()

    # Генерируем кириллический адрес электронной почты
    email = generate_cyrillic_email()
    password = generate_password(12)

    browser.get(
        "https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth?client_id=lk_b2c&redirect_uri=https%3A%2F%2Flk-api.rt.ru%2Fsso-auth%2F%3Fredirect%3Dhttps%253A%252F%252Fstart.rt.ru%252F&response_type=code&scope=openid")

    next_button = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "standard_auth_btn"))
    )
    next_button.click()

    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "kc-register"))
    )

    phone_tab_button = browser.find_element(By.ID, "kc-register")
    phone_tab_button.click()

    first_name_input = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located(
            (By.XPATH,
             '//input[@class="rt-input__input rt-input__input--rounded rt-input__input--orange" and @name="firstName"]'))
    )
    first_name_input.send_keys(first_name)

    last_name_input = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located(
            (By.XPATH,
             '//input[@class="rt-input__input rt-input__input--rounded rt-input__input--orange" and @type="text" and @name="lastName"]')
        )
    )
    last_name_input.send_keys(last_name)

    region_input = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located(
            (By.XPATH,
             "//div[@class='rt-input rt-input--rounded rt-input--orange rt-input--actions']//input[@class='rt-input__input rt-select__input rt-input__input--rounded rt-input__input--orange' and @type='text']"))
    )
    region_input.send_keys("Москва г")

    address_input = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "address"))
    )
    address_input.send_keys(email)
    # Добавление задержки 10 секунд
    time.sleep(10)

    password_input = browser.find_element(By.NAME, "password")
    password_input.send_keys(password)

    confirm_password_input = browser.find_element(By.NAME, "password-confirm")
    confirm_password_input.send_keys(password)

    try:
        register_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                                        "button.rt-btn.rt-btn--orange.rt-btn--medium.rt-btn--rounded.register-form__reg-btn[name='register']"))
        )
        register_button.click()
    except TimeoutException:
        print("Кнопка 'Зарегистрироваться' не была найдена или не была кликабельна.")
        assert False, "Кнопка 'Зарегистрироваться' не была найдена или не была кликабельна."

    WebDriverWait(browser, 5).until(
        EC.url_changes(
            "https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth?client_id=lk_b2c&redirect_uri=https%3A%2F%2Flk-api.rt.ru%2Fsso-auth%2F%3Fredirect%3Dhttps%253A%252F%252Fstart.rt.ru%252F&response_type=code&scope=openid")
    )

    current_url = browser.current_url
    assert current_url != "https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth?client_id=lk_b2c&redirect_uri=https%3A%2F%2Flk-api.rt.ru%2Fsso-auth%2F%3Fredirect%3Dhttps%253A%252F%252Fstart.rt.ru%252F&response_type=code&scope=openid", "URL не изменился после регистрации"

    print(f"Текущий URL после регистрации: {current_url}")

@pytest.mark.email
def test_registration_by_fake_domen_email(browser, generate_cyrillic_name, generate_email_with_special_domain, generate_password):
    fake = Faker('ru_RU')  # Используем русский локальный провайдер

    first_name = generate_cyrillic_name()
    last_name = generate_cyrillic_name()
    email = generate_email_with_special_domain()
    password = generate_password(12)

    browser.get(
        "https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth?client_id=lk_b2c&redirect_uri=https%3A%2F%2Flk-api.rt.ru%2Fsso-auth%2F%3Fredirect%3Dhttps%253A%252F%252Fstart.rt.ru%252F&response_type=code&scope=openid")

    next_button = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "standard_auth_btn"))
    )
    next_button.click()

    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "kc-register"))
    )

    phone_tab_button = browser.find_element(By.ID, "kc-register")
    phone_tab_button.click()

    first_name_input = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located(
            (By.XPATH,
             '//input[@class="rt-input__input rt-input__input--rounded rt-input__input--orange" and @name="firstName"]'))
    )
    first_name_input.send_keys(first_name)

    last_name_input = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located(
            (By.XPATH,
             '//input[@class="rt-input__input rt-input__input--rounded rt-input__input--orange" and @type="text" and @name="lastName"]')
        )
    )
    last_name_input.send_keys(last_name)

    region_input = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located(
            (By.XPATH,
             "//div[@class='rt-input rt-input--rounded rt-input--orange rt-input--actions']//input[@class='rt-input__input rt-select__input rt-input__input--rounded rt-input__input--orange' and @type='text']"))
    )
    region_input.send_keys("Москва г")

    address_input = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "address"))
    )
    address_input.send_keys(email)
    # Добавление задержки 5 секунд
    time.sleep(5)

    password_input = browser.find_element(By.NAME, "password")
    password_input.send_keys(password)

    confirm_password_input = browser.find_element(By.NAME, "password-confirm")
    confirm_password_input.send_keys(password)

    try:
        register_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                                        "button.rt-btn.rt-btn--orange.rt-btn--medium.rt-btn--rounded.register-form__reg-btn[name='register']"))
        )
        register_button.click()
    except TimeoutException:
        print("Кнопка 'Зарегистрироваться' не была найдена или не была кликабельна.")
        assert False, "Кнопка 'Зарегистрироваться' не была найдена или не была кликабельна."

    try:
        # Ожидаем, что URL изменится после успешной регистрации
        WebDriverWait(browser, 10).until(
            EC.url_changes(
                "https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth?client_id=lk_b2c&redirect_uri=https%3A%2F%2Flk-api.rt.ru%2Fsso-auth%2F%3Fredirect%3Dhttps%253A%252F%252Fstart.rt.ru%252F&response_type=code&scope=openid")
        )
    except TimeoutException:
        assert False, "URL не изменился после попытки регистрации, возможно регистрация не прошла."

    current_url = browser.current_url
    print(f"Текущий URL после регистрации: {current_url}")

    assert current_url != "https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth?client_id=lk_b2c&redirect_uri=https%3A%2F%2Flk-api.rt.ru%2Fsso-auth%2F%3Fredirect%3Dhttps%253A%252F%252Fstart.rt.ru%252F&response_type=code&scope=openid", "URL не изменился после регистрации"

    try:
        error_message = WebDriverWait(browser, 5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".error-message"))
        )
        assert "неверный формат email" in error_message.text.lower(), "Ожидается ошибка валидации некорректного email"
        print("Получена ошибка валидации: ", error_message.text)
    except TimeoutException:
        assert False, "Ожидаемая ошибка валидации не была показана. Возможно, регистрация прошла успешно с некорректным email."

@pytest.mark.phone
def test_registration_by_fake_phone(browser, generate_cyrillic_name, generate_password):
    fake = Faker()
    first_name = generate_cyrillic_name()
    last_name = generate_cyrillic_name()
    phone = fake.phone_number()
    password = generate_password(12)

    browser.get(
        "https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth?client_id=lk_b2c&redirect_uri=https%3A%2F%2Flk-api.rt.ru%2Fsso-auth%2F%3Fredirect%3Dhttps%253A%252F%252Fstart.rt.ru%252F&response_type=code&scope=openid")

    next_button = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "standard_auth_btn"))
    )
    next_button.click()

    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "kc-register"))
    )

    phone_tab_button = browser.find_element(By.ID, "kc-register")
    phone_tab_button.click()

    first_name_input = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located(
            (By.XPATH,
             '//input[@class="rt-input__input rt-input__input--rounded rt-input__input--orange" and @name="firstName"]'))
    )
    first_name_input.send_keys(first_name)

    last_name_input = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located(
            (By.XPATH,
             '//input[@class="rt-input__input rt-input__input--rounded rt-input__input--orange" and @type="text" and @name="lastName"]')
        )
    )
    last_name_input.send_keys(last_name)

    region_input = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located(
            (By.XPATH,
             "//div[@class='rt-input rt-input--rounded rt-input--orange rt-input--actions']//input[@class='rt-input__input rt-select__input rt-input__input--rounded rt-input__input--orange' and @type='text']"))
    )
    region_input.send_keys("Москва г")

    address_input = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "address"))
    )
    address_input.send_keys(phone)
    # Добавление задержки 10 секунд
    time.sleep(10)

    password_input = browser.find_element(By.NAME, "password")
    password_input.send_keys(password)

    confirm_password_input = browser.find_element(By.NAME, "password-confirm")
    confirm_password_input.send_keys(password)

    try:
        register_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                                        "button.rt-btn.rt-btn--orange.rt-btn--medium.rt-btn--rounded.register-form__reg-btn[name='register']"))
        )
        register_button.click()
    except TimeoutException:
        print("Кнопка 'Зарегистрироваться' не была найдена или не была кликабельна.")
        assert False, "Кнопка 'Зарегистрироваться' не была найдена или не была кликабельна."

        # Ожидание изменения URL в браузере
    WebDriverWait(browser, 15).until(
        EC.url_changes(
            "https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth?client_id=lk_b2c&redirect_uri=https%3A%2F%2Flk-api.rt.ru%2Fsso-auth%2F%3Fredirect%3Dhttps%253A%252F%252Fstart.rt.ru%252F&response_type=code&scope=openid")
    )

    current_url = browser.current_url
    assert current_url != "https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth?client_id=lk_b2c&redirect_uri=https%3A%2F%2Flk-api.rt.ru%2Fsso-auth%2F%3Fredirect%3Dhttps%253A%252F%252Fstart.rt.ru%252F&response_type=code&scope=openid", "URL не изменился после регистрации"

    print(f"Текущий URL после регистрации: {current_url}")

@pytest.mark.phone
def test_registration_by_phone(browser, generate_cyrillic_name, generate_phone_number_1, generate_password):
    fake = Faker()

    first_name = generate_cyrillic_name()
    last_name = generate_cyrillic_name()
    phone = generate_phone_number_1()
    password = generate_password(12)

    browser.get(
        "https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth?client_id=lk_b2c&redirect_uri=https%3A%2F%2Flk-api.rt.ru%2Fsso-auth%2F%3Fredirect%3Dhttps%253A%252F%252Fstart.rt.ru%252F&response_type=code&scope=openid"
    )

    next_button = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "standard_auth_btn"))
    )
    next_button.click()

    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "kc-register"))
    )

    phone_tab_button = browser.find_element(By.ID, "kc-register")
    phone_tab_button.click()

    first_name_input = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located(
            (By.XPATH,
             '//input[@class="rt-input__input rt-input__input--rounded rt-input__input--orange" and @name="firstName"]')
        )
    )
    first_name_input.send_keys(first_name)

    last_name_input = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located(
            (By.XPATH,
             '//input[@class="rt-input__input rt-input__input--rounded rt-input__input--orange" and @type="text" and @name="lastName"]')
        )
    )
    last_name_input.send_keys(last_name)

    region_input = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located(
            (By.XPATH,
             "//div[@class='rt-input rt-input--rounded rt-input--orange rt-input--actions']//input[@class='rt-input__input rt-select__input rt-input__input--rounded rt-input__input--orange' and @type='text']")
        )
    )
    region_input.send_keys("Москва г")

    address_input = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "address"))
    )
    address_input.send_keys(phone)

    # Добавление задержки 10 секунд
    time.sleep(10)

    password_input = browser.find_element(By.NAME, "password")
    password_input.send_keys(password)

    confirm_password_input = browser.find_element(By.NAME, "password-confirm")
    confirm_password_input.send_keys(password)

    try:
        register_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                                        "button.rt-btn.rt-btn--orange.rt-btn--medium.rt-btn--rounded.register-form__reg-btn[name='register']"))
        )
        register_button.click()
    except TimeoutException:
        print("Кнопка 'Зарегистрироваться' не была найдена или не была кликабельна.")
        assert False, "Кнопка 'Зарегистрироваться' не была найдена или не была кликабельна."

    WebDriverWait(browser, 15).until(
        EC.url_changes(
            "https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth?client_id=lk_b2c&redirect_uri=https%3A%2F%2Flk-api.rt.ru%2Fsso-auth%2F%3Fredirect%3Dhttps%253A%252F%252Fstart.rt.ru%252F&response_type=code&scope=openid")
    )

    current_url = browser.current_url
    assert current_url != "https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth?client_id=lk_b2c&redirect_uri=https%3A%2F%2Flk-api.rt.ru%2Fsso-auth%2F%3Fredirect%3Dhttps%253A%252F%252Fstart.rt.ru%252F&response_type=code&scope=openid", "URL не изменился после регистрации"

    print(f"Текущий URL после регистрации: {current_url}")
