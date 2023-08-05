## Page Object Elements

Dist: [pypi.org](https://pypi.org/project/page-object-elements/)

### Installation

`pip install page-object-elements`

### Aspect Logger

To customize behaviour of **poe** logger, `poe.ini` should be in the root of project (or in some child dirs). If not
present or some of the values aren't set in `poe.ini` (**e.g** `logs_absolute_path`) default values will be applied.

```
poe.ini

[LOGGER]
level = DEBUG
log_name = log
stdout = True
logs_absolute_path = C:\Users\<username>\workspace\<project>
```

## Example of use

locators.py

```python
@aspect.log
class LetsCodeItLocators(object):
    # 1st section
    FIRST_SECTION = (By.XPATH, '//*[@id="page"]/div[2]/div[2]/div/div/div/div/div[1]')
    CAR_SELECT = (By.ID, 'carselect')
    BMV_CB = (By.ID, 'bmwcheck')

    # 2nd section
    SECOND_SECTION = (By.XPATH, '//*[@id="page"]/div[2]/div[2]/div/div/div/div/div[2]')
    SWITCH_TAB_EXAMPLE_LBL = (By.XPATH, '//legend[contains(text(), "Switch Tab Example")]')
    OPEN_TAB_BTN = (By.ID, 'opentab')
    ENTER_YOUR_NAME_INPUT = (By.CSS_SELECTOR, '[placeholder="Enter Your Name"]')

    # 3rd section
    THIRD_SECTION = (By.XPATH, '//*[@id="table-example-div"]')
    WEB_TABLE = (By.XPATH, '//tbody//tr')
```

page.py

```python
@aspect.log
class FirstSection(SectionElement):
    car_select = SelectElement(LetsCodeItLocators.CAR_SELECT, True)
    bmw_cb = CheckBoxElement(locator=LetsCodeItLocators.BMV_CB, enabled_check=True)


@aspect.log
class SecondSection(SectionElement):
    open_tab_btn = ScreenElement()
    switch_tab_example_lbl = LabelElement(locator=LetsCodeItLocators.SWITCH_TAB_EXAMPLE_LBL)
    enter_your_name_input = InputElement(locator=LetsCodeItLocators.ENTER_YOUR_NAME_INPUT)


@aspect.log
class ThirdSection(SectionElement):
    class RowModel(TableElement.TableRowModel):

        def __init__(self, container):
            super().__init__(container)

        @property
        def author(self):
            return self.column_cell(1).text

        @property
        def course(self):
            return self.column_cell(2).text

        @property
        def price(self):
            return self.column_cell(3).text

    web_table = TableElement(LetsCodeItLocators.WEB_TABLE, RowModel)


@aspect.log
class LetsCodeIt(BasePage):
    first_section = FirstSection(locator=LetsCodeItLocators.FIRST_SECTION)
    second_section = SecondSection(locator=LetsCodeItLocators.SECOND_SECTION)
    third_section = ThirdSection(locator=LetsCodeItLocators.THIRD_SECTION)

    def visit(self):
        self.driver.get('https://courses.letskodeit.com/practice')
```

test_letscodeid.py

```python
def test_letscodeit(chrome):
    page = LetsCodeIt(chrome)
    page.visit()

    '''LABEL'''
    label_text = page.second_section.switch_tab_example_lbl
    print(label_text)

    '''INPUT'''
    page.second_section.enter_your_name_input = 'LetsCodeIt'

    '''SELECT'''
    page.first_section.car_select = 'Benz'
    print(page.first_section.car_select.text)
    print(page.first_section.car_select.enabled)
    print(page.first_section.car_select())

    '''CHECKBOX'''
    page.first_section.bmw_cb = True
    print(page.first_section.bmw_cb.checked)
    print(page.first_section.bmw_cb.enabled)
    print(page.first_section.bmw_cb())

    '''TABLE'''
    web_table = page.third_section.web_table
    for row in web_table['all_rows']:
        print(row.author, '\t|', row.course, '\t|', row.price)
    print(30 * '=')
    for row in web_table['headers']:
        print(row.author, '\t|', row.course, '\t|', row.price)
    print(30 * '=')
    for row in web_table['rows']:
        print(row.author, '\t|', row.course, '\t|', row.price)

    '''BUTTON'''
    page.second_section.open_tab_btn.set_locator(LetsCodeItLocators.OPEN_TAB_BTN)
    page.second_section.open_tab_btn.click()
```