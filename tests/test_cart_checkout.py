"""
test_cart_checkout.py
Автотесты для корзины и оформления заказа в Swag Labs
"""

import re
import pytest  # ← ВАЖНО!
import random
import string
from playwright.sync_api import Page, expect
from datetime import datetime


class TestCartAndCheckout:
    """Тесты для проверки корзины и оформления заказа"""
    
    BASE_URL = "https://www.saucedemo.com/"
    VALID_USERNAME = "standard_user"
    VALID_PASSWORD = "secret_sauce"
    
    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """Предусловия: авторизация"""
        page.goto(self.BASE_URL)
        page.locator("#user-name").fill(self.VALID_USERNAME)
        page.locator("#password").fill(self.VALID_PASSWORD)
        page.locator("#login-button").click()
        
        expect(page).to_have_url(re.compile(r".*inventory\.html"))
        expect(page.locator("span.title")).to_have_text("Products")
        
        print(f"\n✅ Авторизация: {self.VALID_USERNAME}")
        yield
    
    def test_add_and_remove_product_from_cart(self, page: Page):
        """TC-CART-001: Добавление и удаление товара из корзины"""
        print("\n🧪 Тест 1: Добавление и удаление товара из корзины")
        
        # Шаг 1: Добавляем товар
        products = page.locator(".inventory_item").all()
        assert len(products) > 0
        
        first_product = products[0]
        product_name = first_product.locator(".inventory_item_name").text_content().strip()
        
        add_button = first_product.locator("button:has-text('Add to cart')")
        add_button.click()
        print(f"✅ Добавили товар: {product_name}")
        
        # Шаг 2: Проверяем счетчик
        cart_badge = page.locator(".shopping_cart_badge")
        expect(cart_badge).to_be_visible()
        expect(cart_badge).to_have_text("1")
        print("✅ Счетчик корзины: 1")
        
        # Шаг 3: Переходим в корзину
        cart_link = page.locator(".shopping_cart_link")
        cart_link.click()
        expect(page).to_have_url(re.compile(r".*cart\.html"))
        print("✅ Перешли в корзину")
        
        # Шаг 4: Проверяем товар в корзине
        cart_items = page.locator(".cart_item").all()
        assert len(cart_items) == 1
        print("✅ Товар в корзине")
        
        # Шаг 5: Удаляем товар
        remove_button = cart_items[0].locator("button:has-text('Remove')")
        remove_button.click()
        
        expect(page.locator(".cart_item")).not_to_be_visible()
        expect(cart_badge).not_to_be_visible()
        print("✅ Товар удален")
        
        # Шаг 6: Возвращаемся
        continue_btn = page.locator("#continue-shopping")
        continue_btn.click()
        expect(page).to_have_url(re.compile(r".*inventory\.html"))
        print("✅ Вернулись на страницу товаров")
        
        print("🎉 Тест 1 пройден!")
    
    def test_add_products_and_checkout(self, page: Page):
        """TC-CHECKOUT-001: Добавление товаров и оформление заказа"""
        print("\n🧪 Тест 2: Оформление заказа")
        
        # Шаг 1: Добавляем 2 товара
        products = page.locator(".inventory_item").all()
        assert len(products) >= 2
        
        for i in range(2):
            product = products[i]
            name = product.locator(".inventory_item_name").text_content().strip()
            product.locator("button:has-text('Add to cart')").click()
            print(f"✅ Добавили товар {i+1}: {name}")
        
        # Шаг 2: Проверяем счетчик
        cart_badge = page.locator(".shopping_cart_badge")
        expect(cart_badge).to_have_text("2")
        print("✅ В корзине 2 товара")
        
        # Шаг 3: Переходим в корзину
        page.locator(".shopping_cart_link").click()
        expect(page).to_have_url(re.compile(r".*cart\.html"))
        print("✅ Перешли в корзину")
        
        # Шаг 4: Начинаем оформление
        page.locator("#checkout").click()
        expect(page).to_have_url(re.compile(r".*checkout-step-one\.html"))
        print("✅ Перешли к оформлению")
        
        # Шаг 5: Заполняем форму
        first_name = "Иван" + str(random.randint(1, 100))
        last_name = "Иванов" + str(random.randint(1, 100))
        zip_code = ''.join(random.choices(string.digits, k=6))
        
        page.locator("#first-name").fill(first_name)
        page.locator("#last-name").fill(last_name)
        page.locator("#postal-code").fill(zip_code)
        
        print(f"📝 Данные: {first_name} {last_name}, индекс: {zip_code}")
        
        # Шаг 6: Продолжаем
        page.locator("#continue").click()
        expect(page).to_have_url(re.compile(r".*checkout-step-two\.html"))
        print("✅ Перешли к обзору заказа")
        
        # Шаг 7: Завершаем заказ
        page.locator("#finish").click()
        expect(page).to_have_url(re.compile(r".*checkout-complete\.html"))
        print("✅ Заказ оформлен")
        
        # Шаг 8: Проверяем подтверждение
        expect(page.locator(".complete-header")).to_have_text("Thank you for your order!")
        print("✅ Подтверждение получено")
        
        # Шаг 9: Возвращаемся
        page.locator("#back-to-products").click()
        expect(page).to_have_url(re.compile(r".*inventory\.html"))
        print("✅ Вернулись на главную")
        
        print("🎉 Тест 2 пройден!")