import re
import pytest
from playwright.sync_api import Page, expect

class TestAuthFlow:
    """Тест-кейс TC-AUTH-001: Проверка успешной авторизации и деавторизации"""
    
    # Константы с данными для теста
    BASE_URL = "https://www.saucedemo.com/"
    VALID_USERNAME = "standard_user"
    VALID_PASSWORD = "secret_sauce"
    
    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """Предусловия: Открытие страницы авторизации"""
        # Шаг 0: Переход на страницу авторизации
        page.goto(self.BASE_URL)
        
        # Проверка, что мы на правильной странице
        expect(page).to_have_title("Swag Labs")
        expect(page.locator("div.login_logo")).to_be_visible()
        
        yield
        
        # Постусловие: Закрытие браузера выполняется автоматически через фикстуру pytest-playwright
    
    def test_successful_login_logout(self, page: Page):
        """TC-AUTH-001: Проверка успешной авторизации и деавторизации"""
        
        # ===== ШАГ 1: Ввод логина =====
        # Находим поле ввода логина по ID и вводим валидный логин
        username_field = page.locator("#user-name")
        username_field.fill(self.VALID_USERNAME)
        
        # Проверяем, что логин отображается в поле ввода
        expect(username_field).to_have_value(self.VALID_USERNAME)
        print("✓ Шаг 1: Логин успешно введен")
        
        # ===== ШАГ 2: Ввод пароля =====
        # Находим поле ввода пароля по ID и вводим валидный пароль
        password_field = page.locator("#password")
        password_field.fill(self.VALID_PASSWORD)
        
        # Проверяем, что пароль скрыт (тип input должен быть "password")
        expect(password_field).to_have_attribute("type", "password")
        print("✓ Шаг 2: Пароль успешно введен (символы скрыты)")
        
        # ===== ШАГ 3: Нажатие кнопки Login =====
        # Находим кнопку входа по ID и кликаем
        login_button = page.locator("#login-button")
        login_button.click()
        
        # Ожидаем обработки запроса и переадресации
        page.wait_for_load_state("networkidle")
        
        # Проверка 3.1: URL изменился (ушли со страницы логина)
        expect(page).not_to_have_url(self.BASE_URL)
        
        # Проверка 3.2: Находимся на главной странице после входа
        expect(page).to_have_url(re.compile(r".*inventory\.html"))
        
        # Проверка 3.3: Отображается приветствие/уникальный элемент
        # На сайте Swag Labs после входа отображается заголовок "Products"
        products_title = page.locator("span.title")
        expect(products_title).to_be_visible()
        expect(products_title).to_have_text("Products")
        
        # Проверка 3.4: Форма входа не отображается
        expect(page.locator("#login-button")).not_to_be_visible()
        
        # Дополнительная проверка: отображается меню пользователя (бургер-меню)
        menu_button = page.locator("#react-burger-menu-btn")
        expect(menu_button).to_be_visible()
        
        print("✓ Шаг 3: Авторизация успешна - пользователь на главной странице")
        
        # ===== ШАГ 4: Открытие меню пользователя =====
        # Кликаем на бургер-меню (элемент профиля пользователя)
        menu_button.click()
        
        # Ожидаем появления выпадающего меню
        menu_container = page.locator(".bm-menu-wrap")
        expect(menu_container).to_be_visible()
        
        # Проверяем, что меню содержит нужные пункты
        # В Swag Labs меню содержит пункт "Logout"
        logout_menu_item = page.locator("#logout_sidebar_link")
        expect(logout_menu_item).to_be_visible()
        expect(logout_menu_item).to_have_text("Logout")
        
        # Также проверяем наличие других пунктов меню
        expect(page.locator("#inventory_sidebar_link")).to_be_visible()  # All Items
        expect(page.locator("#about_sidebar_link")).to_be_visible()      # About
        
        print("✓ Шаг 4: Меню пользователя успешно открыто")
        
        # ===== ШАГ 5: Выход из системы =====
        # Кликаем на пункт "Logout"
        logout_menu_item.click()
        
        # Ожидаем переадресации на страницу авторизации
        page.wait_for_load_state("networkidle")
        
        # Проверка 5.1: Произошла переадресация на страницу авторизации
        expect(page).to_have_url(self.BASE_URL)
        
        # Проверка 5.2: Форма авторизации снова отображается
        expect(page.locator("#login-button")).to_be_visible()
        expect(page.locator("#user-name")).to_be_visible()
        expect(page.locator("#password")).to_be_visible()
        
        # Проверка 5.3: Элементы личного кабинета не отображаются
        expect(page.locator("#react-burger-menu-btn")).not_to_be_visible()
        expect(products_title).not_to_be_visible()
        
        print("✓ Шаг 5: Деавторизация успешна - пользователь на странице входа")
        
        print("\n✅ Тест TC-AUTH-001 пройден успешно!")
        print("   Авторизация и деавторизация работают корректно.")

    # Дополнительный тест для проверки граничных случаев
    def test_login_with_invalid_credentials(self, page: Page):
        """Дополнительный тест: Проверка авторизации с невалидными данными"""
        # Ввод неверных данных
        page.locator("#user-name").fill("invalid_user")
        page.locator("#password").fill("wrong_password")
        page.locator("#login-button").click()
        
        # Проверяем сообщение об ошибке
        error_message = page.locator("h3[data-test='error']")
        expect(error_message).to_be_visible()
        expect(error_message).to_contain_text("Username and password do not match")
        
        print("✓ Дополнительный тест: Неверные данные корректно отклоняются")

# Для запуска теста из командной строки
if __name__ == "__main__":
    # Установите pytest и playwright перед запуском:
    # pip install pytest playwright pytest-playwright
    # playwright install
    
    # Запуск через pytest (рекомендуется):
    # pytest test_auth_flow.py --browser chromium --headed
    
    print("Для запуска тестов используйте команду:")
    print("pytest test_auth_flow.py --browser chromium --headed")
    
    # Или альтернативный запуск без pytest:
    from playwright.sync_api import sync_playwright
    
    def manual_test():
        with sync_playwright() as p:
            # Запускаем браузер Microsoft Edge
            browser = p.chromium.launch(
                channel="msedge",  # Используем Microsoft Edge
                headless=False  # Для визуальной проверки
            )
            
            # Создаем контекст с настройками
            context = browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            )
            
            page = context.new_page()
            
            # Создаем экземпляр теста и выполняем
            test = TestAuthFlow()
            test.setup(page)
            test.test_successful_login_logout(page)
            
            browser.close()
    
    # Раскомментируйте для ручного запуска:
    # manual_test()