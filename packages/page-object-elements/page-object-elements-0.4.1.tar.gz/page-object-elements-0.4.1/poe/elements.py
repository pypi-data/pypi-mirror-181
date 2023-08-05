# ---------------------------------------------------------------------------------
# Name:        elements.py

# Author:      Milan Ranisavljevic
# ---------------------------------------------------------------------------------
import traceback

from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.event_firing_webdriver import EventFiringWebElement
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait

from poe import aspect
from poe.logger import logger
from poe.utility import get_methods_and_properties


@aspect.log
class ScreenElement(object):
    """
    BaseScreenElement class that is initialized on every screen object class.
       :param locator: WebElement locator
       :param container: webdriver or WebElement that contains other WebElements
       :param wait: period of time that method will wait for element to fulfill specified condition
       :param poll_frequency: sleep interval between calls
       :param ignored_exceptions: iterable structure of exception classes ignored during calls
       :param until_not: if true, method will be waiting for element not to be what is specified with condition
       :param method: expected condition that method waits (from expected_conditions or custom_conditions modules)
       :param fail_message: fail message which will be shown when specified condition is not met
       :param scroll_to_element: if True driver will scroll to element location on page

       Ways to set locators if not via constructor:
       -self.screen_element.set_locator("id", "someID")
    """

    @aspect.log
    def __init__(self,
                 locator=None,
                 wait=10,
                 poll_frequency=0.5,
                 method=ec.visibility_of_element_located,
                 ignored_exceptions=(NoSuchElementException, StaleElementReferenceException,),
                 until_not=False,
                 fail_message=None,
                 scroll_to_element=False,
                 container=None):
        if self.__class__.__name__ != 'ScreenElement' and locator == None:
            raise AttributeError(
                f'"locator" can\'t be None for <{self.__class__.__name__}> instance.'
                f' Must be set through the constructor...except for <ScreenElement>.')
        self.driver: WebElement | list[WebElement] = container
        self._locator: tuple[str, str] = locator
        self._wait: int = wait
        self._poll_frequency: float = poll_frequency
        self._verify_method = method
        self._ignored_exceptions: list[Exception] = ignored_exceptions
        self._until_not: bool = until_not
        self._fail_message: str = fail_message
        self._scroll_to_element: bool = scroll_to_element
        self._coordinates: dict = {}

    @aspect.log
    def _resolve_fail_message(self):
        locator = self._locator if self._locator else 'out'
        appearance = "disappear" if self._until_not else "show up"
        if self._fail_message is not None:
            self._fail_message = f'{self._fail_message} :: Waited for {self._wait} seconds!'
        else:
            self._fail_message = f'Element with{locator} locator did not {appearance} in {self._wait} seconds!'

    @aspect.log
    def _refresh(self, obj):  # the most important method
        """
       Refreshes the container of the WebElement in the DOM each time it is referenced,
       waits for element to fulfil conditions based on objects' properties.

       :param obj: instance of class that owns the property
       :raises: :exc:`selenium.common.exceptions.TimeoutException` if timeout occurs
       """
        if self._locator_is_none(obj):
            return self
        else:
            if isinstance(self.driver, EventFiringWebElement):
                self.driver = self.driver.wrapped_element
            self._resolve_fail_message()
            wdw = WebDriverWait(obj.driver, self._wait, self._poll_frequency, self._ignored_exceptions)
            if self._until_not:
                self.driver = wdw.until_not(self._verify_method(self._locator), self._fail_message)
            else:
                self.driver = wdw.until(self._verify_method(self._locator), self._fail_message)
            if self._scroll_to_element:
                self._coordinates = self.driver.location_once_scrolled_into_view
            logger.info(f'Getting <{self.driver.__class__.__name__}> instance :: {self._locator}')
            return self.driver

    @aspect.log
    def _locator_is_none(self, obj):
        """
        The method is intended to solve cases when the locator is not set during the construction of the element itself
        """
        if self._locator is None:
            logger.warning(
                f' <locator> is not set for <{self.__class__.__name__}>'
                f' instance on <{obj.__class__.__name__}> page.'
                f' This will raise Attribute Error if called as <WebElement> object.'
            )
            logger.info(f'Getting <{self.__class__.__name__}> instance...')
            return True
        return False

    @aspect.log
    def set_locator(self, locator: tuple[str, str]):
        """If not set in constructor, setting locator enables use of object as a WebDriver"""
        try:
            assert locator is not None
            assert len(locator) == 2
            assert type(locator[0]) == type(locator[1]) == str
            isinstance(locator, tuple)
            self._locator = locator
        except Exception as e:
            logger.error('Locator should be <tuple[str, str]> with 2 string elements e.g ("id", "someID")')
            logger.error('\n'.join([str(e), traceback.format_exc()]))
            raise e
        logger.info(f'Setting locator {self._locator} on <{self.__class__.__name__}> instance')

    @aspect.log
    def __get__(self, obj, owner):
        """
        Gets the ScreenElement or WebElement based on condition if locator property is set.
        """
        return self._refresh(obj)

    @aspect.log
    def __getattr__(self, attr):
        class_instance = self.__class__.__name__
        screen_element_methods_and_props = get_methods_and_properties(ScreenElement, dont=True, starts_with='_')
        web_element_methods_and_props = get_methods_and_properties(WebElement, dont=True, starts_with='_')
        if attr in web_element_methods_and_props:
            errmsg = f'<{class_instance}> object has no attribute "{attr}". To be referenced as a <WebElement> {class_instance}.locator property must me set!'
            infomsg = f'<{class_instance}> available methods and properties for setting locator: {screen_element_methods_and_props}. Or through the constructor.'
            logger.error(errmsg)
            logger.info(infomsg)
            raise AttributeError(errmsg)
        raise AttributeError(f'<{class_instance}> object has no attribute "{attr}"')


@aspect.log
class SectionElement(ScreenElement):
    """Section element class that is initialized as a container of other elements"""

    def __get__(self, obj, owner):
        """Gets the section with WebElements"""
        super(SectionElement, self).__get__(obj, owner)
        return self


@aspect.log
class LabelElement(ScreenElement):
    """LabelElement class that is initialized on label screen object class."""

    def __get__(self, obj, owner):
        """Gets the text of the specified object"""
        super(LabelElement, self).__get__(obj, owner)
        return self.driver.text


@aspect.log
class InputElement(ScreenElement):
    """InputElement class that is initialized on input screen object class."""

    def __set__(self, obj, value):
        """Sets the text to the value supplied"""
        self._refresh(obj)
        self.driver.clear()
        self.driver.send_keys(value)

    def __get__(self, obj, owner):
        """Gets the text of the specified object"""
        super(InputElement, self).__get__(obj, owner)
        return self.driver.get_attribute("value")


@aspect.log
class SelectElement(ScreenElement):
    """SelectElement class that is initialized on select screen object class."""

    def __init__(self, locator, enabled_check=False):
        super(SelectElement, self).__init__(locator)
        self.enabled_check = enabled_check
        self.text = None
        self.enabled = None

    def __set__(self, obj, value):
        """Selects the text in dropwdown menu to the value supplied"""
        self._refresh(obj)
        Select(self.driver).select_by_visible_text(value)

    def __get__(self, obj, owner):
        """Gets the text of the selected object in dropdown"""
        super(SelectElement, self).__get__(obj, owner)
        selected_option = Select(self.driver).first_selected_option
        self.text = selected_option.text.strip()
        if self.enabled_check:
            self.enabled = selected_option.is_enabled()
        return self

    def __call__(self, *args, **kwargs):
        if self.enabled_check:
            return {'value': self.text, 'enabled': self.enabled}
        return self.text


@aspect.log
class CheckBoxElement(ScreenElement):
    """CheckBoxElement class that is initialized on CheckBoxElement screen object class."""

    def __init__(self, locator, enabled_check):
        super(CheckBoxElement, self).__init__(locator=locator)
        self.enabled_check = enabled_check
        self._checked = None
        self._enabled = None

    @property
    def checked(self) -> bool:
        return self._checked

    @property
    def enabled(self) -> bool:
        return self._enabled

    def __set__(self, obj, value):
        """Sets the checkbox state to the value supplied"""
        self._refresh(obj)
        self._checked = self.driver.is_selected()
        if not isinstance(value, bool):
            raise TypeError('Value for checkbox selection must be "True" of "False"!')
        if value:
            self.driver.click() if not self._checked else None
        else:
            self.driver.click() if self._checked else None

    def __get__(self, obj, owner):
        """Gets the element, state and the enabled from the checkbox element"""
        super(CheckBoxElement, self).__get__(obj, owner)
        if self._locator is not None and not isinstance(self.driver, bool):
            self._refresh(obj)
            self._checked = self.driver.is_selected()
            self._enabled = self.driver.is_enabled()
            return self
        return self

    def __call__(self, *args, **kwargs):
        if self.enabled_check:
            return {'value': self._checked, 'enabled': self._enabled}
        return self._checked


@aspect.log
class TableElement(ScreenElement):

    class TableRowModel(object):
        """
        class RowModel(TableElement.TableRowModel):

        def __init__(self, container):
            super().__init__(container)
            self._author = f'{self.tag}:nth-child(1)'
            self._course = f'{self.tag}:nth-child(2)'
            self._price = f'{self.tag}:nth-child(3)'

        @property
        def author(self):
            return self.driver.find_element_by_css_selector(self._author).text

        @property
        def course(self):
            return self.driver.find_element_by_css_selector(self._course).text

        @property
        def price(self):
            return self.driver.find_element_by_css_selector(self._price).text

        """

        def __init__(self, container):
            self.driver = container
            self.tag = 'th' if self.driver.find_elements('xpath', './th') else 'td'

        def column_cell(self, index):
            return self.driver.find_element_by_css_selector(f'{self.tag}:nth-child({index})')

    def __init__(self, table_rows_locator, table_row_model_cls):
        # noinspection PyTypeChecker
        super(TableElement, self).__init__(locator=table_rows_locator, method=ec.presence_of_all_elements_located)
        self._table_entry_cls = table_row_model_cls
        self._table_headers = None
        self._table_rows = None

    @property
    def headers(self):
        return self._table_headers

    @property
    def rows(self):
        return self._table_rows

    def __get__(self, obj, owner):
        """
            Gets list of table rows, type of provided model class (table_entry_cls). e.g. SoftphoneTableRow!
            locator=(By.CSS_SELECTOR, 'tr'),
            condition=ec.presence_of_all_elements_located)]
        """
        self._refresh(obj)
        all_table_rows = [self._table_entry_cls(table_row) for table_row in self.driver]
        self._table_headers = list(filter(lambda row: (row.driver.find_elements('xpath', './th')), all_table_rows))
        self._table_rows = list(filter(lambda row: (row.driver.find_elements('xpath', './td')), all_table_rows))
        return self

    def filter_rows_by(self, column, value):
        return list(filter(lambda row: getattr(row, column).text == str(value), self._table_rows))
