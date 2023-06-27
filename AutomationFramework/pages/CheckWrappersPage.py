import time

from selenium.webdriver.common.by import By

from pages.BasePage import BasePage


class CheckWrapperPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    checkbox1 = (By.ID, "checkBoxOption1")
    checkbox2 = (By.ID, "checkBoxOption")
    heading_text = (By.TAG_NAME, "h1")
    radio2 = (By.XPATH, "//*[@value='radio2']")
    country_textbox = (By.XPATH, "//*[@placeholder='Type to Select Countries']")
    name = (By.XPATH, "//input[@id='displayed-text']")
    hover = (By.ID, "mousehover")
    dropdown = (By.ID, "dropdown-class-example")
    alertname = (By.XPATH, "//*[@name='enter-name']")

    def AllOperations(self):
        self.ActionsClickElement(self.checkbox1)
        print(self.Exists(self.checkbox2))
        text = self.GetElementText(self.heading_text)
        assert text == "Practice Page"
        radioVal = self.GetElementValue(self.radio2)
        assert radioVal == "radio2"
        self.JavaScriptClickElement(self.radio2)
        self.JavaScriptSetTextBoxAndTab(self.country_textbox, "India")
        self.JavaScriptSetTextBoxAndReturn(self.name, "Maninder")
        self.DoubleClickElement(self.radio2)
        self.ScrollToView(self.hover)
        time.sleep(2)
        self.MoveToElement(self.hover)
        self.ScrollToView(self.radio2)
        self.SelectFromDropdownByText(self.dropdown, "Option3")
        self.SetTextBoxByCharacter(self.alertname, "DEEPAK")



