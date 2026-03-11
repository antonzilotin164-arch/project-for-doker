from locators.locators import LocatorsImagePage
from base.globalVariables import base_url_image_page, add_url_image_page, request
from base.initializationDriver import *
from pathlib import Path
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import logging
import requests

logger = logging.getLogger(__name__)
logging.basicConfig(filename='myapp.log', level=logging.INFO)


class ImagePage():
    def __init__(self, driver):
        self.driver = driver

    def check_current_url(self):
        result = check_current_url(self.driver, base_url_image_page, add_url_image_page)
        if result:
            logger.info("Мы успешно попали на ресурс генерации изображений")
            return result
        else:
            logger.info("Сбой, что-то пошло не так")
            return result

    def check_current_model_generate(self):
        model_generate = wait_element(self.driver, LocatorsImagePage.model_generate, timeout=10)
        css_style_color = model_generate.value_of_css_property("color")
        if css_style_color in ["rgb(255, 255, 255)", "rgba(255, 255, 255, 1)", "#fff", "#ffffff"]:
            logger.info("Выбрана модель по умолчанию")
            return True
        else:
            logger.info("Ошибка выбора модели генерации")
            return False

    def select_model_generate(self):
        selected_model_generate = wait_element(self.driver, LocatorsImagePage.selected_model_generate, timeout=10)
        selected_model_generate.click()

    def check_selected_model(self):
        check_model = wait_element(self.driver, LocatorsImagePage.selected_model_generate, timeout=10)
        font_weight = check_model.value_of_css_property("font-weight")
        if font_weight in ["bold", "700", "600"]:
            logger.info("Модель выбрана верно")
            return True
        else:
            logger.info(f"Модель выбрана неверно")
            return False

    def click_descriptions_field(self):
        descriptions_field = wait_element(self.driver, LocatorsImagePage.descriptions_field, timeout=10)
        descriptions_field.click()

    def check_input_field_is_active(self):
        input_field_is_active = wait_element(self.driver, LocatorsImagePage.descriptions_field, timeout=10)

        # Ждем нужный цвет границы
        WebDriverWait(self.driver, 3).until(
            lambda d: input_field_is_active.value_of_css_property("border-color") in ["#e253dd", "rgb(226, 83, 221)",
                                                                                      "rgba(226, 83, 221, 1)"]
        )

        css_style_border_color = input_field_is_active.value_of_css_property("border-color")
        logger.info(f"Фактический цвет границы: '{css_style_border_color}'")
        logger.info("Поле ввода активно")
        return True

    def input_descriptions_query(self):
        input_descriptions_field = wait_element(self.driver, LocatorsImagePage.descriptions_field, timeout=10)
        input_descriptions_field.send_keys(request)

    def check_value(self, search_value, locator):
        field_value = wait_element(self.driver, locator, timeout=5)
        actual_value = field_value.get_attribute("value")

        if actual_value == search_value:
            logger.info(f"В поле корректное значение: '{actual_value}'")
            return True
        else:
            logger.info(f"Ошибка!: '{actual_value}', ожидалось: '{search_value}'")
            return False

    def click_button_generate_image(self, locator):
        """Клик по кнопке генерации через JavaScript (чтобы избежать перекрытия)"""
        button_generate_image = wait_element(self.driver, locator, timeout=10)

        # Ждем что кнопка кликабельна
        WebDriverWait(self.driver, 3).until(
            EC.element_to_be_clickable(locator)
        )

        self.driver.execute_script("arguments[0].click();", button_generate_image)
        logger.info("Клик по кнопке генерации выполнен через JavaScript")

    def check_click_button_generate_image(self):
        generate_button = wait_element(self.driver, LocatorsImagePage.button_generate_image, timeout=10)
        is_disabled = generate_button.get_attribute("disabled") is not None
        if is_disabled:
            logger.info("Кнопка 'Сгенерировать изображение' заблокирована")
        else:
            logger.info("Кнопка 'Сгенерировать изображение' активна")
        return is_disabled

    def check_start_generation(self):
        loading_indicator = wait_element(self.driver, LocatorsImagePage.loading_indicator, timeout=10)
        display_value = loading_indicator.value_of_css_property("display")

        if display_value == "block":
            logger.info("Генерация изображения начата успешно")
            return True
        elif display_value == "none":
            logger.info("Генерация изображения провалилась")
            return False

    def download_image_via_http(self, save_dir=None):
        """Скачиваем изображение напрямую через HTTP, используя ссылку из тега img"""

        # Ждем появления изображения
        WebDriverWait(self.driver, 3000).until(
            EC.presence_of_element_located((By.ID, "resultImage"))
        )

        # Получаем URL изображения из src
        img_element = self.driver.find_element(By.ID, "resultImage")
        img_url = img_element.get_attribute('src')

        # Логируем URL для отладки
        logger.info(f"URL для скачивания: {img_url}")

        if not img_url:
            raise Exception("Не удалось получить ссылку на изображение")

        # Определяем директорию для сохранения
        if save_dir is None:
            save_dir = Path(__file__).parent.parent / "downloads"
        save_dir = Path(save_dir)

        # Папка должна существовать (создается в initialization)
        if not save_dir.exists():
            save_dir.mkdir(parents=True, exist_ok=True)

        # Формируем имя файла
        file_name = f"image_{int(time.time())}.jpg"
        file_path = save_dir / file_name

        # Скачиваем файл
        response = requests.get(img_url, timeout=300)
        response.raise_for_status()

        # Сохраняем
        with open(file_path, 'wb') as f:
            f.write(response.content)

        # Проверяем что файл скачался и не ноль
        if not file_path.exists():
            raise Exception(f"Файл не был создан: {file_path}")

        file_size = file_path.stat().st_size
        if file_size == 0:
            raise Exception(f"Файл скачался пустой (0 байт): {file_path}")

        logger.info(f"Изображение сохранено: {file_path}, размер: {file_size} байт")
        return file_path

