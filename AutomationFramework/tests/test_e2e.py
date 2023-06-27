import pytest
from TestData.HomepageData import HomepageData
from Utilities.BaseClass import BaseClass
from pages.CheckoutPage import CheckoutPage
from pages.HomePage import HomePage


class TestOne(BaseClass):
    @pytest.mark.usefixtures("dataLoad")
    def test_e2e(self, dataLoad):
        homePage = HomePage(self.driver)
        checkoutPage = homePage.CreateOrder()
        checkoutPage.PromoOperations(dataLoad[0])
        checkoutPage.AmountValidation()

    @pytest.fixture()
    def dataLoad(self):
        print("User profile data is being created")
        return HomepageData.test_homepage_data
