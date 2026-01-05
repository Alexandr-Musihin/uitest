<div align="center">

# 🧪 Swag Labs Автотесты

[![Playwright](https://img.shields.io/badge/Playwright-2EAD33?style=for-the-badge&logo=playwright&logoColor=white)](https://playwright.dev)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![pytest](https://img.shields.io/badge/pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)](https://pytest.org)
[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)](https://github.com/features/actions)

**Профессиональные автотесты для проверки авторизации на Swag Labs**

[Демо](#-демо) • [Установка](#-установка) • [Использование](#-использование) • [Документация](#-документация)

</div>

---

## 📋 Оглавление

- [✨ Особенности](#-особенности)
- [🚀 Быстрый старт](#-быстрый-старт)
- [🛠️ Установка](#️-установка)
- [🧪 Запуск тестов](#-запуск-тестов)
- [📁 Структура проекта](#-структура-проекта)
- [🔧 Конфигурация](#-конфигурация)
- [📊 Отчеты](#-отчеты)
- [🤝 Вклад в проект](#-вклад-в-проект)
- [📄 Лицензия](#-лицензия)

---

## ✨ Особенности

<div align="center">

| Функциональность | Описание |
|-----------------|----------|
| 🎯 **Полное покрытие тест-кейса** | Автоматизация TC-AUTH-001 |
| 🔄 **Авторизация/деавторизация** | Проверка полного цикла входа-выхода |
| 🎨 **Поддержка нескольких браузеров** | Chrome, Firefox, Edge, WebKit |
| 📈 **Детальная отчетность** | HTML, XML, JSON отчеты |
| 🚀 **CI/CD готовность** | Интеграция с GitHub Actions |
| 🐛 **Умная отладка** | Скриншоты, трассировка, логирование |
| 📱 **Адаптивный дизайн** | Поддержка разных разрешений |

</div>

## 🚀 Быстрый старт

### Требования

- Python 3.8+
- pip
- Git

### Установка за 3 шага:

```bash
# 1. Клонировать репозиторий
git clone https://github.com/yourusername/swag-labs-tests.git
cd swag-labs-tests

# 2. Установить зависимости
pip install -r requirements.txt

# 3. Установить браузеры
playwright install chromium
```

## 🛠️ Установка

### Полная установка с виртуальным окружением:

```bash
# Создание виртуального окружения
python -m venv venv

# Активация (Windows)
venv\Scripts\activate

# Активация (Mac/Linux)
source venv/bin/activate

# Установка всех зависимостей
pip install playwright pytest pytest-playwright

# Установка браузеров
playwright install --with-deps chromium firefox
```

### Файл `requirements.txt`:

```txt
playwright==1.40.0
pytest==7.4.3
pytest-playwright==0.4.3
pytest-html==4.0.2
pytest-xdist==3.5.0
```

## 🧪 Запуск тестов

### Основные команды

<div align="center">

| Команда | Описание | 
|---------|----------|
| `pytest tests/` | Запуск всех тестов |
| `pytest tests/ --headed` | С отображением браузера |
| `pytest tests/ --browser chromium` | В Chromium |
| `pytest tests/ --browser firefox` | В Firefox |
| `pytest tests/ -v` | Подробный вывод |
| `pytest tests/ --html=report.html` | С HTML отчетом |

</div>

### Примеры запуска:

```bash
# Базовый запуск
pytest tests/test_auth_flow.py

# С визуальным интерфейсом
pytest tests/ --headed --slowmo 500

# Параллельный запуск
pytest tests/ -n auto

# Запуск с кастомными параметрами
pytest tests/ \
  --browser chromium \
  --headless \
  --html=reports/report.html \
  --self-contained-html
```

## 🔧 Конфигурация

### Настройка окружения

Создайте файл `.env` для переменных окружения:

```env
# .env
BASE_URL=https://www.saucedemo.com
USERNAME=standard_user
PASSWORD=secret_sauce
BROWSER=chromium
HEADLESS=true
SLOWMO=0
TIMEOUT=30000
```

### Конфигурация pytest в `pyproject.toml`:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = [
    "--strict-markers",
    "--strict-config",
    "--tb=short",
    "--color=yes"
]
markers = [
    "smoke: smoke tests",
    "regression: regression tests",
    "auth: authentication tests"
]
```

### Фикстуры в `conftest.py`:

```python
import pytest
from playwright.sync_api import Page, BrowserContext
import os
from dotenv import load_dotenv

load_dotenv()

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, playwright):
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
        "ignore_https_errors": True,
        "record_video_dir": "videos/" if os.getenv("RECORD_VIDEO") else None,
        "locale": "en-US",
    }

@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Page:
    page = context.new_page()
    yield page
    page.close()
```

## 📊 Отчеты

### Генерация отчетов

```bash
# HTML отчет с графиками
pytest tests/ --html=reports/report.html --css=styles.css

# JUnit для CI систем
pytest tests/ --junitxml=reports/junit.xml

# JSON для обработки
pytest tests/ --json=reports/report.json

# Все форматы сразу
pytest tests/ \
  --html=reports/report.html \
  --junitxml=reports/junit.xml \
  --json=reports/report.json
```


```bash
# Запись видео тестов
PLAYWRIGHT_VIDEO=1 pytest tests/ --headed

# Скриншоты при падении
PLAYWRIGHT_SCREENSHOT=on pytest tests/
```

### Пример выполнения:

```
test_auth_flow.py::TestAuthFlow::test_successful_login_logout 
✓ Шаг 1: Логин успешно введен
✓ Шаг 2: Пароль успешно введен (символы скрыты)
✓ Шаг 3: Авторизация успешна
✓ Шаг 4: Меню пользователя открыто
✓ Шаг 5: Деавторизация успешна
✅ Тест пройден успешно!
```

## 🏗️ CI/CD

### GitHub Actions Workflow:

```yaml
name: Playwright Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        browser: [chromium, firefox, webkit]
    steps:
    - uses: actions/checkout@v3
    - uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        playwright install --with-deps ${{ matrix.browser }}
    - name: Run tests
      run: |
        pytest tests/ \
          --browser ${{ matrix.browser }} \
          --headless \
          --html=report-${{ matrix.browser }}.html \
          --junitxml=junit-${{ matrix.browser }}.xml
    - name: Upload reports
      uses: actions/upload-artifact@v3
      with:
        name: test-reports
        path: |
          report-*.html
          junit-*.xml
          test-results/
```

## 🤝 Вклад в проект

Мы приветствуем вклад в проект! Вот как вы можете помочь:

1. **Сообщить об ошибке** — создайте Issue с подробным описанием
2. **Предложить улучшение** — опишите вашу идею
3. **Создать Pull Request** — следуйте нашему гайду

### Процесс внесения изменений:

```bash
# 1. Форкните репозиторий
# 2. Клонируйте ваш форк
git clone https://github.com/your-username/swag-labs-tests.git

# 3. Создайте ветку для фичи
git checkout -b feature/amazing-feature

# 4. Внесите изменения и протестируйте
pytest tests/

# 5. Зафиксируйте изменения
git add .
git commit -m "Add amazing feature"

# 6. Запушьте в ваш форк
git push origin feature/amazing-feature

# 7. Создайте Pull Request
```

## 📄 Лицензия

Этот проект лицензирован под MIT License — подробности см. в файле [LICENSE](LICENSE).

---

<div align="center">

### ⭐ Если проект был полезен, поставьте звездочку на GitHub!

**Создано с ❤️ для сообщества QA-инженеров**

[Документация Playwright](https://playwright.dev/python/docs/intro) •
[Примеры тестов](https://github.com/microsoft/playwright-python/tree/main/examples) •
[Сообщить об ошибке](https://github.com/yourusername/swag-labs-tests/issues)

</div>

## 🆘 Поддержка

### Частые проблемы и решения:

<details>
<summary><b>🔧 Проблемы с установкой Playwright</b></summary>

```bash
# Очистка и переустановка
pip uninstall playwright -y
pip cache purge
pip install playwright
playwright install
```

</details>

<details>
<summary><b>🌐 Проблемы с сетью/прокси</b></summary>

```bash
# Настройка прокси
export HTTP_PROXY=http://proxy.server:port
export HTTPS_PROXY=http://proxy.server:port

# Или в коде
context = browser.new_context(
    proxy={"server": "http://proxy:port"}
)
```

</details>

<details>
<summary><b>🐛 Тесты падают нестабильно</b></summary>

```python
# Добавьте явные ожидания
page.wait_for_selector("#element", state="visible", timeout=10000)

# Используйте retry логику
@pytest.mark.flaky(reruns=3, reruns_delay=1)
def test_unstable():
    ...
```

</details>

### Полезные команды для отладки:

```bash
# Проверка версий
python --version
playwright --version

# Тест соединения
playwright open https://www.saucedemo.com

# Генерация нового теста
playwright codegen https://www.saucedemo.com
```

---

<div align="center">

**📞 Нужна помощь?** [Создайте Issue](https://github.com/yourusername/swag-labs-tests/issues)

**🔄 Последнее обновление:** Август 2024


</div>
