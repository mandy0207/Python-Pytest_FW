import time

import softest
from selenium.common import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from Utilities.LoggerUtil import LoggerUtil


class BasePage(softest.TestCase):
    waiter = None

    def __init__(self, driver):

        ignored_exceptions = (NoSuchElementException, TimeoutException)
        self.driver = driver
        self.waiter = WebDriverWait(self.driver, 7, poll_frequency=2, ignored_exceptions=ignored_exceptions)

    # Use the ActionChain class to click
    def ActionsClickElement(self, locator):
        LoggerUtil.getLogger(self).info("{} {}".format("Actions Click Element ", locator))
        element = self.driver.find_element(*locator)
        self.WaitUntilClickable(locator)
        act = ActionChains(self.driver)
        act.move_to_element(element).click().perform()

    # Clear a text box using backspace
    def ClearTextboxWithBackspace(self, locator):
        element = self.driver.find_element(*locator)
        self.WaitUntilClickable(locator)
        field_Value = element.get_attribute("value")
        try:
            for i in range(len(field_Value)):
                element.send_keys(Keys.BACKSPACE)
        except Exception as e:
            self.DoSoftAssertFailure("Failed adding characters to field")

    # Click a Checkbox
    def ClickCheckbox(self, locator):
        self.WaitUntilClickable(locator).click()
        try:
            self.waiter.until(EC.text_to_be_present_in_element_attribute(locator, "aria-checked", "true"))
        except Exception as e:
            self.DoSoftAssertFailure("Failed waiting for checkbox to be checked")

    # Click Element
    def ClickElement(self, locator):
        LoggerUtil.getLogger(self).info("{} {}".format("Click Element ", locator))
        self.SteadyWait(locator)
        self.retryingFindClick(locator)

    # Wait for document ready state to be complete
    def DomWait(self):
        LoggerUtil.getLogger(self).info("Waiting for dom load to complete")
        try:
            self.waiter.until(lambda driver: self.driver.execute_script('return document.readyState') == 'complete')
        except Exception as e:
            self.DoSoftAssertFailure("Failed Waiting for dom load to complete")

    # Double-click the element
    def DoubleClickElement(self, locator):
        LoggerUtil.getLogger(self).info("{} {}".format("Double Click Element", locator))
        element = self.driver.find_element(*locator)
        self.WaitUntilClickable(locator)
        try:
            act = ActionChains(self.driver)
            act.move_to_element(element).double_click(element).perform()
        except Exception as e:
            self.DoSoftAssertFailure("Failed to double click element")

    # Check If Element exists or not
    def Exists(self, locator):
        try:
            self.WaitUntilVisible(locator)
            return True
        except Exception as e:
            return False

    # Get Element Text
    def GetElementText(self, locator):
        try:
            elementText = self.WaitUntilVisible(locator).text
            return elementText
        except Exception as e:
            self.DoSoftAssertFailure("Failed to get text from element")
            return ""

    # Get the value attribute of an element
    def GetElementValue(self, locator):
        element = self.driver.find_element(*locator)
        try:
            elementValue = element.get_attribute("value")
            return elementValue
        except Exception as e:
            self.DoSoftAssertFailure("Failed to get value from element")
            return ""

    # Use  JavaScript executor  to click an element
    def JavaScriptClickElement(self, locator):
        LoggerUtil.getLogger(self).info("{} {}".format("JavaScript Executor Click Element", locator))
        element = self.driver.find_element(*locator)
        self.WaitUntilClickable(locator)
        self.driver.execute_script("arguments[0].click();", element)

    # Use JavaScriptExecutor to set Textbox
    def JavaScriptSetTextBox(self, locator, Value):
        LoggerUtil.getLogger(self).info("{} {} {}".format("JavaScript Fill text box", locator, Value))
        element = self.driver.find_element(*locator)
        self.WaitUntilVisible(locator)
        try:
            self.driver.execute_script("arguments[0].value='" + Value + "';", element)
        except Exception as e:
            self.DoSoftAssertFailure("Could not set element text to " + Value)

    # Use JavascriptExecutor to set a text box and then press ENTER
    def JavaScriptSetTextBoxAndReturn(self, locator, Value):
        element = self.driver.find_element(*locator)
        self.JavaScriptSetTextBox(locator, Value)
        try:
            element.send_keys(Keys.RETURN)
        except Exception as e:
            self.DoSoftAssertFailure("Could not press RETURN on element")

    # Use JavascriptExecutor to set a text box and then press TAB
    def JavaScriptSetTextBoxAndTab(self, locator, Value):
        element = self.driver.find_element(*locator)
        self.JavaScriptSetTextBox(locator, Value)
        try:
            element.send_keys(Keys.TAB)
        except Exception as e:
            self.DoSoftAssertFailure("Could not press TAB on element")

    # Move Focus to an Element or Hover an Element
    def MoveToElement(self, locator):
        element = self.driver.find_element(*locator)
        try:
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
        except Exception as e:
            self.DoSoftAssertFailure("Failed to move to element")
        return element

    def retryingFindClick(self, locator):
        # element = self.driver.find_element(*locator)
        maxRetries = 100
        attempts = 0
        while attempts < maxRetries:
            try:
                self.WaitUntilEnabled(locator).click()
                break
            except StaleElementReferenceException as e:
                print(e)
            attempts = attempts + 1

    # Use JavaScriptExecutor to scroll view to an element
    def ScrollToView(self, locator):
        element = self.driver.find_element(*locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

    # Scroll Up
    def ScrollUp(self, ):
        self.driver.execute_script("window.scrollBy(0,-250)")

    # Scroll till bottom of page
    def ScrollTillBottom(self):
        self.driver.execute_script("window.scroll(0,document.body.scrollHeight)")

    # Select an Item from Dropdown by visible text
    def SelectFromDropdownByText(self, dropdownLocator, Value):
        LoggerUtil.getLogger(self).info("{} {} {} {}".format("select ", Value, "from dropdown", dropdownLocator))
        dropdownelement = self.driver.find_element(*dropdownLocator)
        self.WaitUntilVisible(dropdownLocator)
        self.WaitUntilClickable(dropdownLocator)
        self.MoveToElement(dropdownLocator)
        try:
            dd = Select(dropdownelement)
            dd.select_by_visible_text(Value)
            dropdownelement.send_keys(Keys.RETURN, Keys.TAB)
        except Exception as e:
            self.DoSoftAssertFailure("{} {}".format("could not select from dropdown", Value))

    # Set Value of date picker field
    def SetDateField(self, locator, Value):
        LoggerUtil.getLogger(self).info("{} {} {} {}".format("Set", locator, "date picker to", Value))
        self.MoveToElement(locator)
        self.SetTextBoxByCharacter(locator, Value)

    # Set Value of Text box by characters sequence
    def SetTextBoxByCharacter(self, locator, Value):
        LoggerUtil.getLogger(self).info("{} {} {} {}".format("Fill text Box", locator, ": ", Value))
        datePicker = self.driver.find_element(*locator)
        self.WaitUntilVisible(locator)
        try:
            to_array = list(Value)
            for i in to_array:
                time.sleep(0.2)
                datePicker.send_keys(i)
            time.sleep(2)
            datePicker.send_keys(Keys.TAB)
        except Exception as e:
            self.DoSoftAssertFailure("Failed to send characters to element")

    # Set the value of TextBox
    def SetTextBox(self, locator, textToAdd):
        LoggerUtil.getLogger(self).info("{} {} {} {}".format("Fill text Box", locator, ": ", textToAdd))
        element = self.driver.find_element(*locator)
        self.WaitUntilVisible(locator)
        self.MoveToElement(locator).clear()
        try:
            element.click()
            self.ClearTextboxWithBackspace(locator)
            element.send_keys(textToAdd)
        except Exception as e:
            self.DoSoftAssertFailure("{} {}".format("could not set element to ", textToAdd))

    # Set the value of text box followed by a return
    def SetTextBoxAndReturn(self, locator, textToAdd):
        self.SetTextBox(locator, textToAdd)
        element = self.driver.find_element(*locator)
        try:
            element.send_keys(Keys.RETURN)
        except Exception as e:
            self.DoSoftAssertFailure("Could not press RETURN on element")

    # Set the value of text box followed by a return and TAB key press
    def SetTextBoxAndReturnAndTab(self, locator, textToAdd):
        self.SetTextBox(locator, textToAdd)
        element = self.driver.find_element(*locator)
        try:
            element.send_keys(Keys.RETURN, Keys.TAB)
        except Exception as e:
            self.DoSoftAssertFailure("Could not RETURN and TAB on field")

    # Set the value of text box followed by a TAB key press
    def SetTextBoxAndTab(self, locator, textToAdd):
        self.SetTextBox(locator, textToAdd)
        element = self.driver.find_element(*locator)
        try:
            element.send_keys(Keys.TAB)
        except Exception as e:
            self.DoSoftAssertFailure("Failed to press TAB from field")

    # Set value of text box by individual key press
    def SetTextBoxByCharacter(self, locator, Value):
        element = self.driver.find_element(*locator)
        self.WaitUntilVisible(locator)
        try:
            to_array = list(Value)
            for i in to_array:
                time.sleep(0.2)
                element.send_keys(i)
            time.sleep(2)
            element.send_keys(Keys.TAB)
        except Exception as e:
            self.DoSoftAssertFailure("Failed to send characters to element")

    # Set the value attribute of an element
    def SetValueAttribute(self, locator, Value):
        element = self.driver.find_element(*locator)
        self.WaitUntilVisible(locator)
        try:
            self.driver.execute_script("arguments[0].value='arguments[1]';", element, Value)
        except Exception as e:
            self.DoSoftAssertFailure("Could not set value attribute to " + Value)

    # Helper to wait for an element to be fully available, preventing stale element exceptions
    def SteadyWait(self, locator):
        LoggerUtil.getLogger(self).info("{} {}".format("Actions Click Element ", locator))
        domWait = "N"
        steadyWait = "y"
        if domWait.__eq__('y'):
            self.DomWait()
        if steadyWait.__eq__('y'):
            print(locator)
            return self.OverrideExpectedCondition(locator)
        else:
            return True

    def OverrideExpectedCondition(self, locator):
        element = self.driver.find_element(*locator)
        try:
            self.waiter.until(lambda d: element.is_displayed)
            return True
        except StaleElementReferenceException as e:
            self.DoSoftAssertFailure("Failed waiting for element to be ready")
            return False

    # Verify an elements text value
    def VerifyElementText(self, locator, expectedText):
        actualElementText = self.WaitUntilVisible(locator).text
        try:
            assert actualElementText.__eq__(expectedText)
        except Exception as e:
            self.DoSoftAssertFailure("Element text did not match")
            print(e)

    # Verify if two strings are equal
    def VerifyEqual(self, actual, expected, message):
        if actual.__eq__(expected):
            assert actual.__eq__(expected)
        else:
            print("Add code for Reporting")

    # wait until the title attribute is value
    def WaitUntilTitleAttributeIs(self, locator, Value):
        # element = self.driver.find_element(*locator)
        self.WaitUntilVisible(locator)
        try:
            self.waiter.until(EC.text_to_be_present_in_element_attribute(locator, "title", Value))
        except Exception as e:
            self.DoSoftAssertFailure("WaitUntilTitleAttributeIs -> Title attribute did not become" + Value)

    # To check element is not displayed
    def WaitUntilNotDisplayed(self, locator):
        element = self.driver.find_element(*locator)
        retries = 1000
        while retries > 0:
            try:
                time.sleep(0.2)
                if not element.is_displayed():
                    break
            except Exception as e:
                retries = 0
            retries = retries - 1

    # wait until element is clickable
    def WaitUntilClickable(self, locator):
        LoggerUtil.getLogger(self).info("{} {}".format("Wait until element is Clickable ", locator))
        element = self.driver.find_element(*locator)
        self.WaitUntilEnabled(locator);
        try:
            self.waiter.until(EC.element_to_be_clickable(locator))
        except Exception as e:
            self.DoSoftAssertFailure("WaitUntilClickable -> Element did not become clickable")
        return element

    # wait until element is enabled
    def WaitUntilEnabled(self, locator):
        LoggerUtil.getLogger(self).info("{} {}".format("Wait Until element is Enabled", locator))
        element = self.driver.find_element(*locator)
        self.SteadyWait(locator)
        try:
            self.waiter.until(lambda d: element.is_enabled() and element.is_displayed())
        except Exception as e:
            self.DoSoftAssertFailure("WaitUntilPresent -> Element was not enabled")
        return element

    # wait Until element is visible
    def WaitUntilVisible(self, locator):
        LoggerUtil.getLogger(self).info("{} {}".format("Wait until element is Visible ", locator))
        element = self.driver.find_element(*locator)
        self.SteadyWait(locator)
        try:
            self.waiter.until(EC.visibility_of(element))
        except Exception as e:
            self.DoSoftAssertFailure("WaitUntilVisible -> Element did not become visible")
        return element

    def DoSoftAssertFailure(self, message):
        self.soft_assert(self.assertTrue, False, message)
