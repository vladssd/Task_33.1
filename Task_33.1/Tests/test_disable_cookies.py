from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest

# Опции для Chrome браузера
chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-cookies")
chrome_options.add_argument("--disable-browser-side-navigation")
chrome_options.add_argument("--disable-gpu")

@pytest.fixture
def driver():
    # Инициализация веб-драйвера с опциями
    driver = webdriver.Chrome(options=chrome_options)
    yield driver
    # Закрытие браузера после завершения теста
    driver.quit()

@pytest.mark.cookies
def test_disable_cookies(driver):
    # Переход на страницу авторизации
    driver.get(
        "https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth?client_id=lk_b2c&redirect_uri=https%3A%2F%2Flk-api.rt.ru%2Fsso-auth%2F%3Fredirect%3Dhttps%253A%252F%252Fstart.rt.ru%252F&response_type=code&scope=openid"
    )

    # Ожидание и клик на кнопку для перехода на форму входа по email
    next_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "standard_auth_btn"))
    )
    next_button.click()

    # Проверка отображения popup с информацией о необходимости включить файлы cookie
    try:
        cookies_tip = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.rt-footer-left__cookies-tip-container .rt-footer-left__item-accent#cookies-tip-open'))
        )
        cookies_tip.click()
        print("Элемент cookies найден и по нему кликнули.")
    except Exception as e:
        print("Не удалось найти или кликнуть по элементу cookies:", str(e))
        driver.save_screenshot("cookies_tip_not_found.png")

    # Проверка отображения popup с информацией о необходимости включить файлы cookie
    try:
        popup = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'span.rt-tooltip__title'))  # Заменяем на CSS-селектор
        )
        print("Popup с информацией о файлах cookie найден.")
    except Exception as e:
        print("Не удалось найти popup с информацией о файлах cookie:", str(e))
        driver.save_screenshot("popup_not_found.png")
        return  # Прерывание теста, если popup не найден

    try:
        retry_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.rt-tooltip__close'))  # Заменяем на CSS-селектор
        )
        print("Кнопка закрытия popup найдена.")
    except Exception as e:
        print("Не удалось найти кнопку закрытия popup:", str(e))
        driver.save_screenshot("retry_button_not_found.png")
        return  # Прерывание теста, если кнопка не найдена

    # Проверка наличия popup и кнопки
    try:
        assert popup.is_displayed()
        assert retry_button.is_displayed()
        print("Тест пройден: Popup и кнопка отображаются корректно.")
    except AssertionError as e:
        print("Тест не пройден: Popup или кнопка не отображаются:", str(e))
        driver.save_screenshot("popup_or_retry_button_not_displayed.png")
