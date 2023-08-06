from robot.api import logger
from robot.utils import asserts
from robot.libraries.BuiltIn import BuiltIn
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.opera import OperaDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class BrowserSetup:
    @staticmethod
    def get_library_driver_instance(library_name):
        library_instance = BuiltIn().get_library_instance(library_name)
        library_browser_instance = library_instance.driver
        return library_browser_instance

    @staticmethod
    def get_latest_browser_path(browser_type):
        browsers = {
            "chrome": ChromeDriverManager().install(),
            "firefox": GeckoDriverManager().install(),
            "brave": ChromeDriverManager(chrome_type=ChromeType.BRAVE).install(),
            "edge": EdgeChromiumDriverManager().install(),
            "opera": OperaDriverManager().install()
        }
        downloaded_webdriver_path = browsers.get(browser_type, None)
        if downloaded_webdriver_path != None:
            return downloaded_webdriver_path

    @staticmethod
    def manipulate_page_loading_behavior(browser_type: str, behavior: str) -> object:
        browsers = {
            "chrome": DesiredCapabilities().CHROME,
            "firefox": DesiredCapabilities().FIREFOX,
            "edge": DesiredCapabilities().EDGE,
            "safari": DesiredCapabilities().SAFARI}
        behaviors = {
            "fully": "normal",
            "partially": "eager"
        }
        desired_capability_instance = browsers.get(browser_type)
        desired_capability_instance['pageLoadStrategy'] = behaviors.get(
            behavior)
        return desired_capability_instance

    @staticmethod
    def change_page_load_timeout_value(browser_library_name, new_time):
        browser = BrowserSetup.get_library_driver_instance(
            browser_library_name)
        browser.set_page_load_timeout(new_time)
