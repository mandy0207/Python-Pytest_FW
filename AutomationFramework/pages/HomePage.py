import time

from selenium.webdriver.common.by import By

from pages.BasePage import BasePage
from pages.CheckoutPage import CheckoutPage


class HomePage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    search = (By.XPATH, "//*[@placeholder='Search for Vegetables and Fruits']")
    addtoCart = (By.XPATH, "//*[@class='product']/div[3]/button")
    imgBag = (By.XPATH, "//*[@class='cart-icon']/img")
    proceddtocheckout = (By.XPATH, "//*[contains(text(),'PROCEED TO CHECKOUT')]")

    def SearchItems(self):
        self.SetTextBox(self.search, "ber")


    def AddToCart(self):
        return self.driver.find_elements(*HomePage.addtoCart)

    def ImgBag(self):
        self.ClickElement(self.imgBag)
        # return self.driver.find_element(*HomePage.imgBag)

    # def ProceedToCheckout(self):
    #     return self.driver.find_element(*HomePage.proceddtocheckout)

    def CreateOrder(self):
        self.SearchItems()
        time.sleep(2)
        results = self.AddToCart()
        count = len(results)
        assert count > 0
        for result in results:
            result.click()
        self.ImgBag()
        self.ClickElement(self.proceddtocheckout)
        self.driver.implicitly_wait(5)
        return CheckoutPage(self.driver)
