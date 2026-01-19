import allure
from base.globalVariables import request, correct_aspect_ratio
from locators.locators import LocatorsImagePage

@allure.feature("Image generation page")
@allure.story("Открытие ресурса генерации изображения")
@allure.tag("Smoke")
@allure.title("Открывается правильный URL")
def test_open_browser(browser_session):
    with allure.step("Открыть страницу генерации изображения"):
        driver, generate_image_page = browser_session

    with allure.step("Проверить, что открыт верный URL"):
        assert generate_image_page.check_current_url()

@allure.feature("Image generation page")
@allure.story("Проверяется модель")
@allure.tag("Smoke")
@allure.title("Проверка, что выбрана модель по умолчанию")
def test_check_model(browser_session):
    with allure.step("Открыть страницу генерации изображения"):
        driver, generate_image_page = browser_session
    with allure.step("Проверить, что выбрана модель по умолчанию"):
        assert generate_image_page.check_current_model_generate()

@allure.feature("Image generation page")
@allure.story("Выбор модели генерации")
@allure.tag("functional")
@allure.title("Проверка выбора модели FLUX.1 [pro]")
def test_select_model(browser_session):
    with allure.step("Переход на ресурс генерации изображения"):
        driver, generate_image_page = browser_session

    with allure.step("Переход на модель FLUX.1 [pro]"):
        generate_image_page.select_model_generate()

    with allure.step("Проверка, что действительно перешли на модель FLUX.1 [pro]"):
        assert generate_image_page.check_selected_model()

@allure.feature("Image generation page")
@allure.story("Проверяем, что поле ввода активно")
@allure.tag("smoke")
@allure.title("Проверка активности поля ввода")
def test_check_input_field_is_active(browser_session):
    with allure.step("Переход на ресурс генерации изображения"):
        driver, generate_image_page = browser_session

    with allure.step("Переход на модель FLUX.1 [pro]"):
        generate_image_page.select_model_generate()

    with allure.step("Клик по полю ввода"):
        generate_image_page.click_descriptions_field()

    with allure.step("Проверка, что поле ввода стало активно"):
        assert generate_image_page.check_input_field_is_active()

@allure.feature("Image generation page")
@allure.story("Ввод текста в поле генерации")
@allure.tag("smoke")
@allure.title("Проверка отображения введённого текста")
def test_input_field_accepts_and_displays_text(browser_session):
    with allure.step("Переход на ресурс генерации изображения"):
        driver, generate_image_page = browser_session

    with allure.step("Переход на модель FLUX.1 [pro]"):
        generate_image_page.select_model_generate()

    with allure.step("Клик по полю ввода"):
        generate_image_page.click_descriptions_field()

    with allure.step("Ввод запроса на генерацию изображения"):
        generate_image_page.input_descriptions_query()

    with allure.step("Проверка, что значение в поле ввода соответствует введенному запросу"):
        assert generate_image_page.check_value(request, LocatorsImagePage.descriptions_field)

@allure.feature("Image generation page")
@allure.story("Проверка соотношения сторон изображения")
@allure.tag("functional")
@allure.title("Проверка соотношения сторон")
def test_check_aspect_ratio(browser_session):
    with allure.step("Переход на ресурс генерации изображения"):
        driver, generate_image_page = browser_session

    with allure.step("Переход на модель FLUX.1 [pro]"):
        generate_image_page.select_model_generate()

    with allure.step("Клик по полю ввода"):
        generate_image_page.click_descriptions_field()

    with allure.step("Ввод запроса на генерацию изображения"):
        generate_image_page.input_descriptions_query()

    with allure.step("Проверка, что заданное разрешение изображения соответствует требованиям"):
        assert generate_image_page.check_value(correct_aspect_ratio, LocatorsImagePage.aspect_ratio)

@allure.feature("Image generation page")
@allure.story("Клик по кнопке генерации")
@allure.tag("smoke")
@allure.title("Проверка клика по кнопке генерации")
def test_check_click_button_generate_image(browser_session):
    with allure.step("Переход на ресурс генерации изображения"):
        driver, generate_image_page = browser_session

    with allure.step("Переход на модель FLUX.1 [pro]"):
        generate_image_page.select_model_generate()

    with allure.step("Клик по полю ввода"):
        generate_image_page.click_descriptions_field()

    with allure.step("Ввод запроса на генерацию изображения"):
        generate_image_page.input_descriptions_query()

    with allure.step("Клик по кнопке 'Сгенерировать изображение'"):
        generate_image_page.click_button_generate_image(LocatorsImagePage.button_generate_image)

    with allure.step("Проверка, что нажатие кнопки прошло успешно"):
        assert generate_image_page.check_click_button_generate_image()


@allure.feature("Image generation page")
@allure.story("Начало генерации изображения")
@allure.tag("smoke")
@allure.title("Проверка начала генерации изображения")
def test_start_generation(browser_session):
    with allure.step("Переход на ресурс генерации изображения"):
        driver, generate_image_page = browser_session

    with allure.step("Переход на модель FLUX.1 [pro]"):
        generate_image_page.select_model_generate()
    with allure.step("Клик по полю ввода"):
        generate_image_page.click_descriptions_field()

    with allure.step("Ввод запроса на генерацию изображения"):
        generate_image_page.input_descriptions_query()

    with allure.step("Клик по кнопке 'Сгенерировать изображение'"):
        generate_image_page.click_button_generate_image(LocatorsImagePage.button_generate_image)

    with allure.step("Проверка, что генерация изображения начата успешно"):
        assert generate_image_page.check_start_generation()

@allure.feature("Image generation page")
@allure.story("Генерация и скачивание изображения")
@allure.tag("e2e")
@allure.title("Проверка успешной генерации и скачивания изображения")
def test_check_file_download_successful(browser_session_with_download):
    with allure.step("Переход на ресурс генерации изображения, создание папки для скачивания"):
        driver, generate_image_page, download_dir = browser_session_with_download
        print(f"Папка для скачивания: {download_dir}")

    with allure.step("Переход на модель FLUX.1 [pro]"):
        generate_image_page.select_model_generate()

    with allure.step("Клик по полю ввода"):
        generate_image_page.click_descriptions_field()

    with allure.step("Ввод запроса на генерацию изображения"):
        generate_image_page.input_descriptions_query()

    with allure.step("Клик по кнопке 'Сгенерировать изображение'"):
        generate_image_page.click_button_generate_image(LocatorsImagePage.button_generate_image)

    with allure.step("Нажатие кнопки скачивания"):
        generate_image_page.click_download_button()

    with allure.step("Обработка системного диалога"):
        generate_image_page.handle_save_dialog()

    with allure.step("Ожидание завершения скачивания"):
        downloaded_file = generate_image_page.wait_for_download_complete()

    with allure.step("Проверка успешного скачивания файла"):
        assert downloaded_file

























