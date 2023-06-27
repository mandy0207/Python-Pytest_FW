from selenium.webdriver.common.by import By

from pages.BasePage import BasePage


class CheckoutPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    promocode = (By.CSS_SELECTOR, ".promoCode")
    promobtn = (By.CSS_SELECTOR, ".promoBtn")

    discount_locator = By.CSS_SELECTOR, ".promoInfo"
    amount_locator = By.XPATH, "//table/tbody/tr/td[5]"
    total_amount= By.XPATH, "//*[@class='totAmt']"

    def AddPromoCode(self):
        return self.driver.find_element(*CheckoutPage.promocode)

    def PromoBtn(self):
        return self.driver.find_element(*CheckoutPage.promobtn)

    def GetAmount(self):
        return self.driver.find_elements(*CheckoutPage.amount_locator)

    def GetTotalAmount(self):
        return self.driver.find_element(*CheckoutPage.total_amount)

    def PromoOperations(self, couponCode):
        self.SetTextBox(self.promocode, couponCode)
        self.ClickElement(self.promobtn)
        self.WaitUntilVisible(self.discount_locator)
        print(self.GetElementText(self.discount_locator))

    def AmountValidation(self):
        list_amount = self.GetAmount()
        sumVal = 0
        for amount in list_amount:
            sumVal = sumVal + int(amount.text)
        print(sumVal)
        amount_total= self.GetElementText(self.total_amount)
        amount_total= int(amount_total)
        assert sumVal == amount_total



