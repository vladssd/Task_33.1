import os

import pytest
import requests
from PIL import Image
import pytesseract
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver


# Установка переменной окружения TESSDATA_PREFIX
os.environ['TESSDATA_PREFIX'] = r'C:\Users\SONY\Desktop\Study\TESTER\ДИПЛОМ\tesseract'

def recognize_text_from_image(image_path):
    # Задаем путь к исполняемому файлу Tesseract (пример для Windows)
    pytesseract.pytesseract.tesseract_cmd = r'C:\Users\SONY\Desktop\Study\TESTER\ДИПЛОМ\tesseract'

    # Открываем изображение с CAPTCHA
    img = Image.open(image_path)

    # Распознаем текст с помощью pytesseract
    text = pytesseract.image_to_string(img)

    return text

@pytest.mark.password_recovery
def test_password_recovery_by_email(browser, open_password_recovery_page):
    # Открытие страницы восстановления пароля
    open_password_recovery_page()

    assert browser.current_url == (
        'https://b2c.passport.rt.ru/auth/realms/b2c/login-actions/reset-credentials?client_id=lk_b2c&tab_id=LyCXSrIiNEE')

    # Явное ожидание появления элемента
    wait = WebDriverWait(browser, 15)

    # Выбираем восстановление по e-mail:
    email_tab = wait.until(EC.presence_of_element_located((By.ID, "t-btn-tab-mail")))
    email_tab.click()

    # Ввод email
    email_input = wait.until(EC.presence_of_element_located((By.ID, "username")))
    email_input.send_keys("tests.for.test2024@gmail.com")

    # Получаем URL картинки CAPTCHA
    captcha_image = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "rt-captcha__image")))
    captcha_image_url = captcha_image.get_attribute("src")

    # Скачать изображение CAPTCHA
    response = requests.get(captcha_image_url)
    if response.status_code == 200:
        with open('captcha.png', 'wb') as f:
            f.write(response.content)
    else:
        raise Exception("Failed to download CAPTCHA image")

    # Распознаем текст с CAPTCHA
    captcha_text = recognize_text_from_image('captcha.png')
    print(f'Recognized CAPTCHA text: {captcha_text}')

    # Вводим распознанный текст CAPTCHA
    captcha_input = wait.until(EC.presence_of_element_located((By.ID, "captcha")))
    captcha_input.send_keys(captcha_text)

    # Ожидание 10 секунд
    browser.implicitly_wait(10)

    # Нажимаем кнопку "Продолжить"
    continue_button = wait.until(EC.element_to_be_clickable((By.ID, "reset")))
    continue_button.click()

    # Добавляем задержку для ожидания загрузки страницы
    browser.implicitly_wait(5)

    # Проверка успешной авторизации
    assert (
        "required-action?execution=UPDATE_PASSWORD" in browser.current_url
    ) or (
        "login-actions/authenticate" in browser.current_url
    )

