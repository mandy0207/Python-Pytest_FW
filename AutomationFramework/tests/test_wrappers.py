from Utilities.BaseClass import BaseClass
from pages.CheckWrappersPage import CheckWrapperPage


class TestWrappers(BaseClass):

    def test_AllWrappers(self):
        self.driver.get("https://rahulshettyacademy.com/AutomationPractice/")
        chkObj = CheckWrapperPage(self.driver)
        chkObj.AllOperations()



