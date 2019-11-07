'''
http://www.cnblogs.com/end-of-summer/p/9765982.html
https://www.cnblogs.com/glumer/p/8485052.html
https://www.cnblogs.com/glumer/p/8487622.html


github site:
https://github.com/search?utf8=%E2%9C%93&q=appium&type=
'''
from AppiumLibrary import AppiumLibrary
from robot.api import logger
from time import sleep
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


class MobileAppLibrary(AppiumLibrary):

    def __init__(self, timeout=5, run_on_failure='MobileAppLibrary.Capture Page Screenshot'):
        for base in AppiumLibrary.__bases__:
            base.__init__(self)
        self.set_appium_timeout(timeout)
        self.register_keyword_to_run_on_failure(run_on_failure)

    def check_element(self, locator, selected, timeout=30):
        self.wait_until_page_contains_element(locator, timeout)
        checked = self.get_element_attribute(locator, 'checked')

        selected = selected.lower()
        checked = checked.lower()

        if (selected != checked):
                AppiumLibrary.click_element(self, locator)

    def wait_until_page_contains_element(self, locator, timeout=None, error=None, auto_swipe=True):
        if (auto_swipe != True):
            return AppiumLibrary.wait_until_page_contains_element(self, locator, timeout=timeout, error=error)

        count = 5
        if timeout == None:
            timeout_per_page = None
        else:
            timeout_per_page = float(float(timeout) / count)

        exception = None

        while count > 0:
            try:
                return AppiumLibrary.wait_until_page_contains_element(self, locator, timeout=timeout_per_page,
                                                                      error=error)
            except Exception:
                count = count - 1
                if count < 3:
                    try:
                        logger.info(
                            "Failed to find the element on current page, try to scroll the screen down and find the element again.")
                        self.swipe_by_percent(50, 70, 50, 30)
                    except Exception:
                        logger.info("Failed to swipe mobile screen")
        else:
            sleep(1)

        raise exception

    def input_text(self, locator, text, timeout=30):
        """Types the given `text` into text field identified by `locator`.

        See `introduction` for details about locating elements.
        """
        self.wait_until_page_contains_element(locator, timeout)
        AppiumLibrary.clear_text(self, locator)
        AppiumLibrary.input_text(self, locator, text)
        try:
            self.hide_keyboard()
        except BaseException:
            pass

    def input_password(self, locator, text, timeout=30):
        """Types the given password into text field identified by `locator`.

        Difference between this keyword and `Input Text` is that this keyword
        does not log the given password. See `introduction` for details about
        locating elements.
        """
        self.wait_until_page_contains_element(locator, timeout)
        AppiumLibrary.clear_text(self, locator)
        AppiumLibrary.input_password(self, locator, text)
        try:
            self.hide_keyboard()
        except BaseException:
            pass

    def input_value(self, locator, text, timeout=30):
        """Sets the given value into text field identified by `locator`. This is an IOS only keyword, input value makes use of set_value

        See `introduction` for details about locating elements.
        """
        self.wait_until_page_contains_element(locator, timeout)
        AppiumLibrary.clear_text(self, locator)
        AppiumLibrary.input_value(self, locator, text)
        try:
            self.hide_keyboard()
        except BaseException:
            pass

    def click_element(self, locator, timeout=30, auto_swipe=True):
        """Click element identified by `locator`.

        Key attributes for arbitrary elements are `index` and `name`. See
        `introduction` for details about locating elements.
        """
        self.wait_until_page_contains_element(locator, timeout=timeout, auto_swipe=auto_swipe)
        AppiumLibrary.click_element(self, locator)

    def page_should_contain_element(self, locator, loglevel='INFO', timeout=30, auto_swipe=True):
        """Verifies that current page contains `locator` element.

        If this keyword fails, it automatically logs the page source
        using the log level specified with the optional `loglevel` argument.
        Giving `NONE` as level disables logging.
        """
        self.wait_until_page_contains_element(locator, timeout, auto_swipe=auto_swipe)
        AppiumLibrary.page_should_contain_element(self, locator, loglevel=loglevel)

    def page_should_contain_text(self, text, loglevel='INFO', timeout=30):
        """Verifies that current page contains `text`.

        If this keyword fails, it automatically logs the page source
        using the log level specified with the optional `loglevel` argument.
        Giving `NONE` as level disables logging.
        """
        self.wait_until_page_contains(text, timeout)
        AppiumLibrary.page_should_contain_text(self, text, loglevel=loglevel)

    def page_should_not_contain_element(self, locator, loglevel='INFO', timeout=30):
        """Verifies that current page not contains `locator` element.

        If this keyword fails, it automatically logs the page source
        using the log level specified with the optional `loglevel` argument.
        Giving `NONE` as level disables logging.
        """
        self.wait_until_page_does_not_contain_element(locator, timeout)
        AppiumLibrary.page_should_not_contain_element(self, locator, loglevel=loglevel)

    def page_should_not_contain_text(self, text, loglevel='INFO', timeout=30):
        """Verifies that current page not contains `text`.

        If this keyword fails, it automatically logs the page source
        using the log level specified with the optional `loglevel` argument.
        Giving `NONE` as level disables logging.
        """
        self.wait_until_page_does_not_contain(text, timeout)
        AppiumLibrary.page_should_not_contain_text(self, text, loglevel=loglevel)

    def open_application(self, remote_url, alias=None, **kwargs):
        res = AppiumLibrary.open_application(self, remote_url, alias=alias, **kwargs)
        sleep(5)
        try:
            driver = self._current_application()
            driver.switch_to.alert.accept()
            sleep(5)
        except BaseException:
            pass
        return res

    def launch_application(self):
        """ Launch application. Application can be launched while Appium session running.
        This keyword can be used to launch application during test case or between test cases.

        This keyword works while `Open Application` has a test running. This is good practice to `Launch Application`
        and `Quit Application` between test cases. As Suite Setup is `Open Application`, `Test Setup` can be used to `Launch Application`

        Example (syntax is just a representation, refer to RF Guide for usage of Setup/Teardown):
        | [Setup Suite] |
        |  | Open Application | http://localhost:4723/wd/hub | platformName=Android | deviceName=192.168.56.101:5555 | app=${CURDIR}/demoapp/OrangeDemoApp.apk |
        | [Test Setup] |
        |  | Launch Application |
        |  |  | <<<test execution>>> |
        |  |  | <<<test execution>>> |
        | [Test Teardown] |
        |  | Quit Application |
        | [Suite Teardown] |
        |  | Close Application |

        See `Quit Application` for quiting application but keeping Appium sesion running.

        New in AppiumLibrary 1.4.6
        """
        AppiumLibrary.launch_application(self)
        sleep(5)
        try:
            driver = self._current_application()
            driver.switch_to.alert.accept()
            sleep(5)
        except BaseException:
            pass

    def accept_alert_if_exist(self):
        try:
            sleep(5)
            driver = self._current_application()
            driver.switch_to.alert.accept()
            sleep(5)
        except BaseException:
            pass

    def get_element_attribute(self, locator, attribute):
        if isinstance(locator, WebElement):
            try:
                attr_val = locator.get_attribute(attribute)
                self._info("Element attribute '%s' value '%s' " % (attribute, attr_val))
                return attr_val
            except:
                raise AssertionError("Attribute '%s' is not valid for element" % (attribute))
        return AppiumLibrary.get_element_attribute(self, locator, attribute)

    def open_notifications(self):
        driver = self._current_application()
        driver.open_notifications()

    # def capture_page_screenshot(self, filename=None):
    #     return AppiumLibrary.capture_page_screenshot(filename)