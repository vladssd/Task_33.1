import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.mark.phone
def test_auth_by_phone(browser):
    browser.get(
        "https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth?client_id=lk_b2c&redirect_uri=https%3A%2F%2Flk-api.rt.ru%2Fsso-auth%2F%3Fredirect%3Dhttps%253A%252F%252Fstart.rt.ru%252F&response_type=code&scope=openid")

    # 1. Нажимаем на кнопку для перехода на другую страницу
    next_button = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "standard_auth_btn"))
    )
    next_button.click()
    # 2. Ожидаем загрузки новой страницы
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "t-btn-tab-phone"))
    )
    # 3. Нажимаем на кнопку с ID "t-btn-tab-phone"
    phone_tab_button = browser.find_element(By.ID, "t-btn-tab-phone")
    phone_tab_button.click()
    # 4. Вводим номер телефона в поле с ID "username"
    phone_input = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "username"))
    )
    phone_input.send_keys("+79266338788")
    # 5. Вводим пароль в поле с ID "password"
    password_input = browser.find_element(By.ID, "password")
    password_input.send_keys("8tw-PVL/T%6eY-/")
    # 6. Нажимаем кнопку с ID "kc-login"
    login_button = browser.find_element(By.ID, "kc-login")
    login_button.click()
    # Добавляем задержку для ожидания загрузки страницы
    browser.implicitly_wait(5)
    # Проверка успешной авторизации
    assert "start.rt.ru" in browser.current_url

@pytest.mark.phone
def test_auth_by_default_phone_message(browser):
    try:
        browser.get(
            "https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth?client_id=lk_b2c&redirect_uri=https%3A%2F%2Flk-api.rt.ru%2Fsso-auth%2F%3Fredirect%3Dhttps%253A%252F%252Fstart.rt.ru%252F&response_type=code&scope=openid")

        # Вводим несуществующий номер телефона
        phone_input = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, "address")))
        phone_input.send_keys("+7000000000")

        # Нажимаем кнопку "Получить код"
        login_button = browser.find_element(By.ID, "otp_get_code")
        login_button.click()

        # Добавляем задержку для ожидания загрузки страницы
        browser.implicitly_wait(5)

        # Проверка URL для определения успешного или неуспешного теста
        current_url = browser.current_url
        error_message = "Неверный номер телефона" in browser.page_source

        if "login-actions/authenticate" in current_url:
            raise AssertionError("Тест неудачный: Заведите баг репорт")
        elif error_message:
            print("Тест успешный: Сообщение об ошибке 'Неверный номер телефона' отображается")
        else:
            raise AssertionError("Тест неудачный: Не удалось обнаружить ожидаемое поведение")
    finally:
        # Закрываем браузер
        browser.quit()


@pytest.mark.phone
def test_auth_by_empty_phone(browser):
    browser.get(
        "https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth?client_id=lk_b2c&redirect_uri=https%3A%2F%2Flk-api.rt.ru%2Fsso-auth%2F%3Fredirect%3Dhttps%253A%252F%252Fstart.rt.ru%252F&response_type=code&scope=openid")

    # 1. Нажимаем на кнопку для перехода на другую страницу
    next_button = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "standard_auth_btn"))
    )
    next_button.click()
    # 2. Ожидаем загрузки новой страницы
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "t-btn-tab-phone"))
    )
    # 3. Нажимаем на кнопку с ID "t-btn-tab-phone"
    phone_tab_button = browser.find_element(By.ID, "t-btn-tab-phone")
    phone_tab_button.click()
    # 4. Вводим номер телефона в поле с ID "username"
    phone_input = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "username"))
    )
    phone_input.send_keys("")
    # 5. Вводим пароль в поле с ID "password"
    password_input = browser.find_element(By.ID, "password")
    password_input.send_keys("8tw-PVL/T%6eY-/")
    # 6. Нажимаем кнопку с ID "kc-login"
    login_button = browser.find_element(By.ID, "kc-login")
    login_button.click()
    # Добавляем задержку для ожидания загрузки страницы
    browser.implicitly_wait(5)
    # Проверка успешной авторизации
    assert "start.rt.ru" in browser.current_url


@pytest.mark.phone
def test_auth_invalid_phone(browser):
    browser.get(
        "https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth?client_id=lk_b2c&redirect_uri=https%3A%2F%2Flk-api.rt.ru%2Fsso-auth%2F%3Fredirect%3Dhttps%253A%252F%252Fstart.rt.ru%252F&response_type=code&scope=openid")

    # 1. Нажимаем на кнопку для перехода на другую страницу
    next_button = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "standard_auth_btn"))
    )
    next_button.click()
    # 2. Ожидаем загрузки новой страницы
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "t-btn-tab-phone"))
    )
    # 3. Нажимаем на кнопку с ID "t-btn-tab-phone"
    phone_tab_button = browser.find_element(By.ID, "t-btn-tab-phone")
    phone_tab_button.click()
    # 4. Вводим номер телефона в поле с ID "username"
    phone_input = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "username"))
    )
    phone_input.send_keys("+7111111111L")
    # 5. Вводим пароль в поле с ID "password"
    password_input = browser.find_element(By.ID, "password")
    password_input.send_keys("8tw-PVL/T%6eY-/")
    # 6. Нажимаем кнопку с ID "kc-login"
    login_button = browser.find_element(By.ID, "kc-login")
    login_button.click()
    # Добавляем задержку для ожидания загрузки страницы
    browser.implicitly_wait(5)
    # Проверка успешной авторизации
    error_message = browser.find_element(By.ID, "error_message").text
    assert error_message == "Неверный логин или пароль"

@pytest.mark.phone
def test_auth_by_invalid_password_by_phone(browser):
    browser.get(
        "https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth?client_id=lk_b2c&redirect_uri=https%3A%2F%2Flk-api.rt.ru%2Fsso-auth%2F%3Fredirect%3Dhttps%253A%252F%252Fstart.rt.ru%252F&response_type=code&scope=openid")

    # 1. Нажимаем на кнопку для перехода на другую страницу
    next_button = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "standard_auth_btn"))
    )
    next_button.click()
    # 2. Ожидаем загрузки новой страницы
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "t-btn-tab-phone"))
    )
    # 3. Нажимаем на кнопку с ID "t-btn-tab-phone"
    phone_tab_button = browser.find_element(By.ID, "t-btn-tab-phone")
    phone_tab_button.click()
    # 4. Вводим номер телефона в поле с ID "username"
    phone_input = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "username"))
    )
    phone_input.send_keys("+79266338788")
    # 5. Вводим пароль в поле с ID "password"
    password_input = browser.find_element(By.ID, "password")
    password_input.send_keys("8tw-PVLasdj/T%6eY-/")
    # 6. Нажимаем кнопку с ID "kc-login"
    login_button = browser.find_element(By.ID, "kc-login")
    login_button.click()
    # Добавляем задержку для ожидания загрузки страницы
    browser.implicitly_wait(5)
    # Проверка успешной авторизации
    assert "start.rt.ru" in browser.current_url

@pytest.mark.phone
def test_auth_by_empty_password_by_phone(browser):
    browser.get(
        "https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth?client_id=lk_b2c&redirect_uri=https%3A%2F%2Flk-api.rt.ru%2Fsso-auth%2F%3Fredirect%3Dhttps%253A%252F%252Fstart.rt.ru%252F&response_type=code&scope=openid")

    # 1. Нажимаем на кнопку для перехода на другую страницу
    next_button = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "standard_auth_btn"))
    )
    next_button.click()
    # 2. Ожидаем загрузки новой страницы
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "t-btn-tab-phone"))
    )
    # 3. Нажимаем на кнопку с ID "t-btn-tab-phone"
    phone_tab_button = browser.find_element(By.ID, "t-btn-tab-phone")
    phone_tab_button.click()
    # 4. Вводим номер телефона в поле с ID "username"
    phone_input = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "username"))
    )
    phone_input.send_keys("+79266338788")
    # 5. Вводим пароль в поле с ID "password"
    password_input = browser.find_element(By.ID, "password")
    password_input.send_keys("")
    # 6. Нажимаем кнопку с ID "kc-login"
    login_button = browser.find_element(By.ID, "kc-login")
    login_button.click()
    # Добавляем задержку для ожидания загрузки страницы
    browser.implicitly_wait(5)
    # Проверка успешной авторизации
    assert "start.rt.ru" in browser.current_url

@pytest.mark.email
def test_auth_by_email(browser):
    browser.get(
        "https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth?client_id=lk_b2c&redirect_uri=https%3A%2F%2Flk-api.rt.ru%2Fsso-auth%2F%3Fredirect%3Dhttps%253A%252F%252Fstart.rt.ru%252F&response_type=code&scope=openid")

    # 1. Нажимаем на кнопку для перехода на форму входа по email
    next_button = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "standard_auth_btn"))
    )
    next_button.click()

    # 2. Ожидаем загрузки новой страницы
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "t-btn-tab-mail"))
    )

    # 3. Нажимаем на кнопку с ID "t-btn-tab-mail"
    email_tab_button = browser.find_element(By.ID, "t-btn-tab-mail")
    email_tab_button.click()

    # 4. Вводим email в поле с ID "username"
    email_input = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "username"))
    )
    email_input.send_keys("tests.for.test2024@gmail.com")

    # 5. Вводим пароль в поле с ID "password"
    password_input = browser.find_element(By.ID, "password")
    password_input.send_keys("8tw-PVL/T%6eY-/")

    # 6. Нажимаем кнопку с ID "kc-login"
    login_button = browser.find_element(By.ID, "kc-login")
    login_button.click()

    # Добавляем задержку для ожидания загрузки страницы
    browser.implicitly_wait(5)

    # Проверка успешной авторизации
    assert "start.rt.ru" in browser.current_url

@pytest.mark.email
def test_auth_invalid_email(browser):
    browser.get(
        "https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth?client_id=lk_b2c&redirect_uri=https%3A%2F%2Flk-api.rt.ru%2Fsso-auth%2F%3Fredirect%3Dhttps%253A%252F%252Fstart.rt.ru%252F&response_type=code&scope=openid")

    # 1. Нажимаем на кнопку для перехода на форму входа по email
    next_button = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "standard_auth_btn"))
    )
    next_button.click()

    # 2. Ожидаем загрузки новой страницы
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "t-btn-tab-mail"))
    )

    # 3. Нажимаем на кнопку с ID "t-btn-tab-mail"
    email_tab_button = browser.find_element(By.ID, "t-btn-tab-mail")
    email_tab_button.click()

    # 4. Вводим неверный email в поле с ID "username"
    email_input = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "username"))
    )
    email_input.send_keys("invalid_email@example.com")

    # 5. Вводим пароль в поле с ID "password"
    password_input = browser.find_element(By.ID, "password")
    password_input.send_keys("8tw-PVL/T%6eY-/")

    # 6. Нажимаем кнопку с ID "kc-login"
    login_button = browser.find_element(By.ID, "kc-login")
    login_button.click()

    # Ожидаем появления сообщения об ошибке
    error_message = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "form-error-message"))
    ).text

    # Проверка сообщения об ошибке
    assert error_message == "Неверный логин или пароль"

@pytest.mark.email
def test_auth_invalid_email_password(browser):
    browser.get(
        "https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth?client_id=lk_b2c&redirect_uri=https%3A%2F%2Flk-api.rt.ru%2Fsso-auth%2F%3Fredirect%3Dhttps%253A%252F%252Fstart.rt.ru%252F&response_type=code&scope=openid")

    # 1. Нажимаем на кнопку для перехода на форму входа по email
    next_button = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "standard_auth_btn"))
    )
    next_button.click()

    # 2. Ожидаем загрузки новой страницы
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "t-btn-tab-mail"))
    )

    # 3. Нажимаем на кнопку с ID "t-btn-tab-mail"
    email_tab_button = browser.find_element(By.ID, "t-btn-tab-mail")
    email_tab_button.click()

    # 4. Вводим неверный email в поле с ID "username"
    email_input = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "username"))
    )
    email_input.send_keys("tests.for.test2024@gmail.com")

    # 5. Вводим пароль в поле с ID "password"
    password_input = browser.find_element(By.ID, "password")
    password_input.send_keys("wqewqw-PVL/T%6eY-/")

    # 6. Нажимаем кнопку с ID "kc-login"
    login_button = browser.find_element(By.ID, "kc-login")
    login_button.click()

    # Ожидаем появления сообщения об ошибке
    error_message = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "form-error-message"))
    ).text

    # Проверка сообщения об ошибке
    assert error_message == "Неверный логин или пароль"

@pytest.mark.email
def test_auth_email_empty_password(browser):
    browser.get(
        "https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth?client_id=lk_b2c&redirect_uri=https%3A%2F%2Flk-api.rt.ru%2Fsso-auth%2F%3Fredirect%3Dhttps%253A%252F%252Fstart.rt.ru%252F&response_type=code&scope=openid")

    # 1. Нажимаем на кнопку для перехода на форму входа по email
    next_button = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "standard_auth_btn"))
    )
    next_button.click()

    # 2. Ожидаем загрузки новой страницы
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "t-btn-tab-mail"))
    )

    # 3. Нажимаем на кнопку с ID "t-btn-tab-mail"
    email_tab_button = browser.find_element(By.ID, "t-btn-tab-mail")
    email_tab_button.click()

    # 4. Вводим неверный email в поле с ID "username"
    email_input = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "username"))
    )
    email_input.send_keys("tests.for.test2024@gmail.com")

    # 5. Вводим пароль в поле с ID "password"
    password_input = browser.find_element(By.ID, "password")
    password_input.send_keys("")

    # 6. Нажимаем кнопку с ID "kc-login"
    login_button = browser.find_element(By.ID, "kc-login")
    login_button.click()

    # Ожидаем появления сообщения об ошибке
    error_message = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "form-error-message"))
    ).text

    # Проверка сообщения об ошибке
    assert error_message == "Неверный логин или пароль"

@pytest.mark.login
def test_auth_login(browser):
    browser.get(
        "https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth?client_id=lk_b2c&redirect_uri=https%3A%2F%2Flk-api.rt.ru%2Fsso-auth%2F%3Fredirect%3Dhttps%253A%252F%252Fstart.rt.ru%252F&response_type=code&scope=openid")
    # 1. Нажимаем на кнопку для перехода на форму входа по email
    next_button = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "standard_auth_btn"))
    )
    next_button.click()
    # 2. Ожидаем загрузки новой страницы
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "t-btn-tab-login"))
    )
    # 3. Нажимаем на кнопку с ID "t-btn-tab-mail"
    login_tab_button = browser.find_element(By.ID, "t-btn-tab-login")
    login_tab_button.click()
    # 4. Вводим верный логин в поле с ID "username"
    login_input = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "username"))
    )
    login_input.send_keys("rtkid_1722531873554")
    # 5. Вводим пароль в поле с ID "password"
    password_input = browser.find_element(By.ID, "password")
    password_input.send_keys("8tw-PVL/T%6eY-/")
    # 6. Нажимаем кнопку с ID "kc-login"
    login_button = browser.find_element(By.ID, "kc-login")
    login_button.click()
    # Добавляем задержку для ожидания загрузки страницы
    browser.implicitly_wait(5)
    # Проверка успешной авторизации
    assert "start.rt.ru" in browser.current_url

@pytest.mark.login
def test_auth_login_empty_password(browser):
    browser.get(
        "https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth?client_id=lk_b2c&redirect_uri=https%3A%2F%2Flk-api.rt.ru%2Fsso-auth%2F%3Fredirect%3Dhttps%253A%252F%252Fstart.rt.ru%252F&response_type=code&scope=openid")
    # 1. Нажимаем на кнопку для перехода на форму входа по email
    next_button = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "standard_auth_btn"))
    )
    next_button.click()
    # 2. Ожидаем загрузки новой страницы
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "t-btn-tab-login"))
    )
    # 3. Нажимаем на кнопку с ID "t-btn-tab-mail"
    login_tab_button = browser.find_element(By.ID, "t-btn-tab-login")
    login_tab_button.click()
    # 4. Вводим верный логин в поле с ID "username"
    login_input = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "username"))
    )
    login_input.send_keys("rtkid_1722531873554")
    # 5. Вводим  пустой пароль в поле с ID "password"
    password_input = browser.find_element(By.ID, "password")
    password_input.send_keys("")
    # 6. Нажимаем кнопку с ID "kc-login"
    login_button = browser.find_element(By.ID, "kc-login")
    login_button.click()
    # Ожидаем появления сообщения об ошибке
    error_message = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "form-error-message"))
    ).text
    # Проверка сообщения об ошибке
    assert error_message == "Неверный логин или пароль"

@pytest.mark.login
def test_auth_login_invalid_login(browser):
    browser.get(
        "https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth?client_id=lk_b2c&redirect_uri=https%3A%2F%2Flk-api.rt.ru%2Fsso-auth%2F%3Fredirect%3Dhttps%253A%252F%252Fstart.rt.ru%252F&response_type=code&scope=openid")
    # 1. Нажимаем на кнопку для перехода на форму входа по email
    next_button = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "standard_auth_btn"))
    )
    next_button.click()
    # 2. Ожидаем загрузки новой страницы
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "t-btn-tab-login"))
    )
    # 3. Нажимаем на кнопку с ID "t-btn-tab-mail"
    login_tab_button = browser.find_element(By.ID, "t-btn-tab-login")
    login_tab_button.click()
    # 4. Вводим верный логин в поле с ID "username"
    login_input = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "username"))
    )
    login_input.send_keys("123")
    # 5. Вводим  пароль в поле с ID "password"
    password_input = browser.find_element(By.ID, "password")
    password_input.send_keys("8tw-PVL/T%6eY-/")
    # 6. Нажимаем кнопку с ID "kc-login"
    login_button = browser.find_element(By.ID, "kc-login")
    login_button.click()
    # Ожидаем появления сообщения об ошибке
    error_message = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "form-error-message"))
    ).text
    # Проверка сообщения об ошибке
    assert error_message == "Неверный логин или пароль"

@pytest.mark.login
def test_auth_login_invalid_password(browser):
    browser.get(
        "https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth?client_id=lk_b2c&redirect_uri=https%3A%2F%2Flk-api.rt.ru%2Fsso-auth%2F%3Fredirect%3Dhttps%253A%252F%252Fstart.rt.ru%252F&response_type=code&scope=openid")
    # 1. Нажимаем на кнопку для перехода на форму входа по email
    next_button = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "standard_auth_btn"))
    )
    next_button.click()
    # 2. Ожидаем загрузки новой страницы
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "t-btn-tab-login"))
    )
    # 3. Нажимаем на кнопку с ID "t-btn-tab-mail"
    login_tab_button = browser.find_element(By.ID, "t-btn-tab-login")
    login_tab_button.click()
    # 4. Вводим верный логин в поле с ID "username"
    login_input = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "username"))
    )
    login_input.send_keys("rtkid_1722531873554")
    # 5. Вводим  не верный пароль в поле с ID "password"
    password_input = browser.find_element(By.ID, "password")
    password_input.send_keys("123456789")
    # 6. Нажимаем кнопку с ID "kc-login"
    login_button = browser.find_element(By.ID, "kc-login")
    login_button.click()
    # Ожидаем появления сообщения об ошибке
    error_message = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "form-error-message"))
    ).text
    # Проверка сообщения об ошибке
    assert error_message == "Неверный логин или пароль"
