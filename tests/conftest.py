import random
from pathlib import Path
import pytest
from base.initializationDriver import initialization, stop_driver
from base.globalVariables import password, base_url_image_page, base_url
from page.imagePage import ImagePage


@pytest.fixture()
def setup(request):
    request.cls.driver = initialization
    #request.cls.screenshot(request.cls)
    yield
    stop_driver(request.cls.driver)




@pytest.fixture(scope="function")
def browser_session():
    """Фикстура для перехода на страницу"""
    driver = initialization(base_url_image_page)
    generate_image_page = ImagePage(driver)

    yield driver, generate_image_page

    # Пост-условие - закрытие браузера
    driver.quit()


@pytest.fixture(scope="function")
def browser_session_with_download():
    """Фикстура для тестов со скачиванием"""
    download_dir = Path(__file__).parent.parent / "downloads"
    driver, actual_download_dir = initialization(base_url_image_page, download_dir, return_tuple=True)  # ← с return_tuple
    generate_image_page = ImagePage(driver)

    yield driver, generate_image_page, actual_download_dir
    driver.quit()