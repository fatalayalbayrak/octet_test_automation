import pytest
from utils.driver_factory import DriverFactory

@pytest.fixture(scope="function")
def driver():
    factory = DriverFactory()
    drv = factory.get_driver()
    yield drv
    drv.quit()

@pytest.fixture(autouse=True)
def attach_driver(request, driver):
    if hasattr(request, "instance"):
        request.instance.driver = driver