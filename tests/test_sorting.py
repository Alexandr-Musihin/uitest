import re
import pytest
from playwright.sync_api import Page, expect
from typing import List, Tuple
import locale

class TestProductSorting:
    """Тесты для проверки сортировки товаров в Swag Labs"""
    
    BASE_URL = "https://www.saucedemo.com/"
    VALID_USERNAME = "standard_user"
    VALID_PASSWORD = "secret_sauce"
    
    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """Предусловие: авторизация и переход на страницу товаров"""
        # Авторизация
        page.goto(self.BASE_URL)
        page.locator("#user-name").fill(self.VALID_USERNAME)
        page.locator("#password").fill(self.VALID_PASSWORD)
        page.locator("#login-button").click()
        
        # Проверка успешной авторизации
        expect(page).to_have_url(re.compile(r".*inventory\.html"))
        expect(page.locator("span.title")).to_have_text("Products")
        
        yield
        
    def extract_product_data(self, page: Page) -> List[Tuple[str, float]]:
        """
        Извлекает данные о товарах со страницы
        Возвращает список кортежей (название, цена)
        """
        products = []
        
        # Находим все элементы товаров
        product_elements = page.locator(".inventory_item").all()
        
        for product in product_elements:
            # Извлекаем название товара
            name_element = product.locator(".inventory_item_name")
            product_name = name_element.text_content().strip()
            
            # Извлекаем цену товара
            price_element = product.locator(".inventory_item_price")
            price_text = price_element.text_content().strip()
            
            # Конвертируем цену в число (убираем $)
            try:
                price = float(price_text.replace("$", ""))
            except ValueError:
                price = 0.0
            
            products.append((product_name, price))
        
        return products
    
    def test_sort_by_name_a_to_z(self, page: Page):
        """TC-SORT-001: Проверка сортировки по имени от A до Z (по умолчанию)"""
        print("\n=== Тест сортировки A → Z ===")
        
        # 1. Получаем текущий порядок товаров (по умолчанию должен быть A-Z)
        initial_products = self.extract_product_data(page)
        print(f"Найдено товаров: {len(initial_products)}")
        
        # 2. Проверяем, что сортировка по умолчанию выбрана
        sort_dropdown = page.locator(".product_sort_container")
        expect(sort_dropdown).to_have_value("az")
        
        # 3. Проверяем, что названия отсортированы от A до Z
        product_names = [name for name, _ in initial_products]
        sorted_names = sorted(product_names, key=lambda x: x.lower())
        
        assert product_names == sorted_names, f"Ожидалась сортировка A-Z, но порядок отличается"
        
        # 4. Выводим информацию для наглядности
        print("Товары в порядке A-Z:")
        for i, (name, price) in enumerate(initial_products, 1):
            print(f"  {i:2}. {name:<30} ${price:.2f}")
        
        print("✅ Сортировка по имени от A до Z работает корректно")
    
    def test_sort_by_name_z_to_a(self, page: Page):
        """TC-SORT-002: Проверка сортировки по имени от Z до A"""
        print("\n=== Тест сортировки Z → A ===")
        
        # 1. Выбираем сортировку "Name (Z to A)"
        sort_dropdown = page.locator(".product_sort_container")
        sort_dropdown.select_option("za")
        
        # Ждем обновления страницы
        page.wait_for_load_state("networkidle")
        
        # 2. Получаем товары после сортировки
        sorted_products = self.extract_product_data(page)
        
        # 3. Проверяем, что сортировка применена в выпадающем списке
        expect(sort_dropdown).to_have_value("za")
        
        # 4. Проверяем, что названия отсортированы от Z до A
        product_names = [name for name, _ in sorted_products]
        reverse_sorted_names = sorted(product_names, key=lambda x: x.lower(), reverse=True)
        
        assert product_names == reverse_sorted_names, f"Ожидалась сортировка Z-A, но порядок отличается"
        
        # 5. Выводим информацию для наглядности
        print("Товары в порядке Z-A:")
        for i, (name, price) in enumerate(sorted_products, 1):
            print(f"  {i:2}. {name:<30} ${price:.2f}")
        
        print("✅ Сортировка по имени от Z до A работает корректно")
    
    def test_sort_by_price_low_to_high(self, page: Page):
        """TC-SORT-003: Проверка сортировки по цене от низкой к высокой"""
        print("\n=== Тест сортировки по цене (low → high) ===")
        
        # 1. Выбираем сортировку "Price (low to high)"
        sort_dropdown = page.locator(".product_sort_container")
        sort_dropdown.select_option("lohi")
        
        # Ждем обновления страницы
        page.wait_for_load_state("networkidle")
        
        # 2. Получаем товары после сортировки
        sorted_products = self.extract_product_data(page)
        
        # 3. Проверяем, что сортировка применена
        expect(sort_dropdown).to_have_value("lohi")
        
        # 4. Проверяем, что цены отсортированы по возрастанию
        product_prices = [price for _, price in sorted_products]
        
        # Проверяем, что каждая следующая цена больше или равна предыдущей
        for i in range(len(product_prices) - 1):
            assert product_prices[i] <= product_prices[i + 1], \
                f"Нарушена сортировка по возрастанию: {product_prices[i]} > {product_prices[i + 1]}"
        
        # 5. Выводим информацию для наглядности
        print("Товары по возрастанию цены:")
        for i, (name, price) in enumerate(sorted_products, 1):
            print(f"  {i:2}. ${price:6.2f} - {name}")
        
        print("✅ Сортировка по цене от низкой к высокой работает корректно")
    
    def test_sort_by_price_high_to_low(self, page: Page):
        """TC-SORT-004: Проверка сортировки по цене от высокой к низкой"""
        print("\n=== Тест сортировки по цене (high → low) ===")
        
        # 1. Выбираем сортировку "Price (high to low)"
        sort_dropdown = page.locator(".product_sort_container")
        sort_dropdown.select_option("hilo")
        
        # Ждем обновления страницы
        page.wait_for_load_state("networkidle")
        
        # 2. Получаем товары после сортировки
        sorted_products = self.extract_product_data(page)
        
        # 3. Проверяем, что сортировка применена
        expect(sort_dropdown).to_have_value("hilo")
        
        # 4. Проверяем, что цены отсортированы по убыванию
        product_prices = [price for _, price in sorted_products]
        
        # Проверяем, что каждая следующая цена меньше или равна предыдущей
        for i in range(len(product_prices) - 1):
            assert product_prices[i] >= product_prices[i + 1], \
                f"Нарушена сортировка по убыванию: {product_prices[i]} < {product_prices[i + 1]}"
        
        # 5. Выводим информацию для наглядности
        print("Товары по убыванию цены:")
        for i, (name, price) in enumerate(sorted_products, 1):
            print(f"  {i:2}. ${price:6.2f} - {name}")
        
        print("✅ Сортировка по цене от высокой к низкой работает корректно")
    
    def test_all_sorting_options(self, page: Page):
        """TC-SORT-005: Комплексная проверка всех вариантов сортировки""" # pytest test_sorting.py::TestProductSorting::test_all_sorting_options -v
        print("\n=== Комплексный тест всех вариантов сортировки ===")
        
        sort_options = [
            ("az", "Name (A to Z)", "от A до Z"),
            ("za", "Name (Z to A)", "от Z до A"),
            ("lohi", "Price (low to high)", "по возрастанию цены"),
            ("hilo", "Price (high to low)", "по убыванию цены")
        ]
        
        previous_order = None
        
        for option_value, option_text, description in sort_options:
            print(f"\nТестируем сортировку: {description}")
            
            # Выбираем опцию сортировки
            sort_dropdown = page.locator(".product_sort_container")
            sort_dropdown.select_option(option_value)
            
            # Ждем обновления
            page.wait_for_load_state("networkidle")
            
            # Проверяем, что опция выбрана
            expect(sort_dropdown).to_have_value(option_value)
            
            # Получаем текущий порядок товаров
            current_products = self.extract_product_data(page)
            
            # Проверяем, что порядок изменился (кроме первого раза)
            if previous_order is not None:
                assert current_products != previous_order, \
                    f"Порядок товаров не изменился при выборе '{description}'"
            
            previous_order = current_products
            
            # Дополнительные проверки в зависимости от типа сортировки
            if option_value in ["az", "za"]:
                # Проверка сортировки по имени
                names = [name for name, _ in current_products]
                if option_value == "az":
                    expected_names = sorted(names, key=lambda x: x.lower())
                else:  # "za"
                    expected_names = sorted(names, key=lambda x: x.lower(), reverse=True)
                
                assert names == expected_names, \
                    f"Некорректная сортировка по имени для '{description}'"
            
            elif option_value in ["lohi", "hilo"]:
                # Проверка сортировки по цене
                prices = [price for _, price in current_products]
                for i in range(len(prices) - 1):
                    if option_value == "lohi":
                        assert prices[i] <= prices[i + 1], \
                            f"Нарушена сортировка по возрастанию цены"
                    else:  # "hilo"
                        assert prices[i] >= prices[i + 1], \
                            f"Нарушена сортировка по убыванию цены"
            
            print(f"  ✅ {description} - ОК")
        
        print("\n✅ Все варианты сортировки работают корректно!")
    
    def test_sorting_persistence(self, page: Page):
        """TC-SORT-006: Проверка сохранения выбранной сортировки при перезагрузке"""
        print("\n=== Тест сохранения сортировки ===")
        
        # 1. Выбираем сортировку "Price (high to low)"
        sort_dropdown = page.locator(".product_sort_container")
        sort_dropdown.select_option("hilo")
        page.wait_for_load_state("networkidle")
        
        # 2. Запоминаем порядок товаров
        products_before_reload = self.extract_product_data(page)
        
        # 3. Обновляем страницу
        page.reload()
        page.wait_for_load_state("networkidle")
        
        # 4. Проверяем, что сортировка сохранилась
        expect(sort_dropdown).to_have_value("hilo")
        
        # 5. Получаем товары после перезагрузки
        products_after_reload = self.extract_product_data(page)
        
        # 6. Проверяем, что порядок товаров не изменился
        assert products_before_reload == products_after_reload, \
            "Порядок товаров изменился после перезагрузки страницы"
        
        print("✅ Выбранная сортировка сохраняется при перезагрузке страницы")
    
    def test_sorting_with_special_characters(self, page: Page):
        """TC-SORT-007: Проверка сортировки с товарами, содержащими спецсимволы"""
        print("\n=== Тест сортировки со спецсимволами ===")
        
        # 1. Проверяем сортировку A-Z
        sort_dropdown = page.locator(".product_sort_container")
        sort_dropdown.select_option("az")
        page.wait_for_load_state("networkidle")
        
        products = self.extract_product_data(page)
        names = [name for name, _ in products]
        
        # 2. Проверяем, что сортировка работает корректно
        # (игнорируя регистр и обрабатывая спецсимволы)
        sorted_names = sorted(names, key=lambda x: x.lower())
        
        # 3. Выводим товары для проверки
        print("Товары (включая спецсимволы):")
        for i, name in enumerate(names, 1):
            has_special = any(not c.isalnum() and c != ' ' for c in name)
            special_mark = " ✨" if has_special else ""
            print(f"  {i:2}. {name}{special_mark}")
        
        assert names == sorted_names, "Сортировка A-Z работает некорректно со спецсимволами"
        
        print("✅ Сортировка корректно обрабатывает товары со спецсимволами")

# Дополнительные утилиты для тестов
def verify_sorting_order(elements: List[Tuple[str, float]], sort_type: str) -> bool:
    """
    Проверяет правильность сортировки элементов
    sort_type: 'name_asc', 'name_desc', 'price_asc', 'price_desc'
    """
    if not elements:
        return True
    
    if sort_type == 'name_asc':
        names = [name.lower() for name, _ in elements]
        return all(names[i] <= names[i + 1] for i in range(len(names) - 1))
    
    elif sort_type == 'name_desc':
        names = [name.lower() for name, _ in elements]
        return all(names[i] >= names[i + 1] for i in range(len(names) - 1))
    
    elif sort_type == 'price_asc':
        prices = [price for _, price in elements]
        return all(prices[i] <= prices[i + 1] for i in range(len(prices) - 1))
    
    elif sort_type == 'price_desc':
        prices = [price for _, price in elements]
        return all(prices[i] >= prices[i + 1] for i in range(len(prices) - 1))
    
    return False

# Для запуска тестов напрямую
if __name__ == "__main__":
    from playwright.sync_api import sync_playwright
    
    def run_tests():
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context(viewport={'width': 1920, 'height': 1080})
            page = context.new_page()
            
            try:
                test = TestProductSorting()
                
                print("=" * 60)
                print("Запуск тестов сортировки товаров")
                print("=" * 60)
                
                # Запускаем каждый тест
                test.setup(page)
                
                tests_to_run = [
                    ("Сортировка A-Z", test.test_sort_by_name_a_to_z),
                    ("Сортировка Z-A", test.test_sort_by_name_z_to_a),
                    ("Сортировка по возрастанию цены", test.test_sort_by_price_low_to_high),
                    ("Сортировка по убыванию цены", test.test_sort_by_price_high_to_low),
                    ("Все варианты сортировки", test.test_all_sorting_options),
                    ("Сохранение сортировки", test.test_sorting_persistence),
                    ("Сортировка со спецсимволами", test.test_sorting_with_special_characters),
                ]
                
                passed = 0
                failed = 0
                
                for test_name, test_func in tests_to_run:
                    try:
                        print(f"\n{'='*60}")
                        print(f"Тест: {test_name}")
                        print(f"{'='*60}")
                        test_func(page)
                        print(f"✅ {test_name} - ПРОЙДЕН")
                        passed += 1
                    except Exception as e:
                        print(f"❌ {test_name} - ПРОВАЛЕН")
                        print(f"   Ошибка: {str(e)}")
                        failed += 1
                        # Делаем скриншот при падении теста
                        page.screenshot(path=f"error_{test_name.replace(' ', '_')}.png")
                
                print(f"\n{'='*60}")
                print(f"РЕЗУЛЬТАТЫ:")
                print(f"  Пройдено: {passed}")
                print(f"  Провалено: {failed}")
                print(f"  Всего: {passed + failed}")
                print(f"{'='*60}")
                
                if failed == 0:
                    print("🎉 Все тесты успешно пройдены!")
                else:
                    print(f"⚠️  {failed} тестов не пройдено")
                
            finally:
                browser.close()
    
    run_tests()