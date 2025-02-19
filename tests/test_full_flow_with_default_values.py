import unittest

from pages.home_page import HomePage
from pages.login_page import LoginPage
from tests.base_test import BaseTest
from utils.logger import logger


class TestFullFlowWithDefaultValues(BaseTest, unittest.TestCase):
    provider_infos = ["isyeriinfo1", "isyeriinfo2", "isyeriinfo3", "isyeriinfo4", "isyeriinfo5"]
    installment_options_for_personal = ["3", "5", "7", "9", "11", "13", "15", "17"]
    installment_options_for_commercial = ["2", "4", "6", "8", "10", "12", "14", "16", "18"]


    def test_full_flow_with_default_values(self):
        """
        Full Flow Test Steps:
        1. Login with default credentials and perform SMS verification.
        2. Create Pos for this test case
        3. Search and find the POS and add Commisions to the POS
        4. Enter the test step and clicks the 'Satış (3D)' button
        5. Next Steps....
        """

        self.logger = logger
        self.logger.info("1. Login with default credentials and perform SMS verification.")
        self.login_page = LoginPage(self.driver)
        self.sms_page = self.login_page.login()
        self.home_page = self.sms_page.sms_login()
        self.logger.info("Successfully logged in")
        self.logger.info("1. Login with default credentials and perform SMS verification - Completed.")

        self.logger.info("2. Create Pos for this test case")
        self.pos_setup_page = self.home_page.hover_and_click_pos_define()
        self.add_new_pos_page = self.pos_setup_page.click_add_button()
        self.add_new_pos_page.click_dropdowns_with_placeholder_text("Ödeme Sistemi")
        self.add_new_pos_page.select_option_from_dropdown(option_text="QNB FinansBank")
        self.add_new_pos_page.enter_pos_name("Octet Test Otomasyon Pos test5")
        self.add_new_pos_page.clickx_dropdowns_with_placeholder_text("Durum")
        self.add_new_pos_page.select_option_from_dropdown("Aktif")
        self.add_new_pos_page.click_dropdowns_with_placeholder_text("Mod")
        self.add_new_pos_page.select_option_from_dropdown("Test ortam")
        self.add_new_pos_page.enter_values_into_merchant_info(self.provider_infos)
        self.add_new_pos_page.click_dropdowns_with_placeholder_text("POS Tipi")
        self.add_new_pos_page.select_option_from_dropdown("Standart")
        self.add_new_pos_page.click_dropdowns_with_placeholder_text("Kart Türleri")
        self.add_new_pos_page.select_option_from_dropdown("Tümü")
        self.add_new_pos_page.click_dropdowns_with_placeholder_text("3D Seçimi")
        self.add_new_pos_page.select_option_from_dropdown("Her zaman 3D Kullan")
        self.add_new_pos_page.select_installment_options(self.installment_options_for_personal, "Personal")
        self.add_new_pos_page.select_installment_options(self.installment_options_for_commercial, "Commercial")
        self.pos_setup_page = self.add_new_pos_page.click_save_button()
        self.logger.info("2. POS created successfully")

        self.logger.info("3. Search and find the POS and add Commisions to the POS")
        self.pos_setup_page.search_pos_from_list("Octet Test Otomasyon Pos test1")
        self.pos_detail_page = self.pos_setup_page.click_pos_detail_button()
        self.pos_detail_page.click_tab("Komisyonlar")
        self.pos_detail_page.click_add_button()
        self.pos_detail_page.click_commission_toggle()
        self.pos_detail_page.enter_commission_name("Komisyon1")
        self.pos_detail_page.enter_start_date()
        self.pos_detail_page.enter_computed_values_for_specific_indexes(1,5,1.5,2,0)
        self.pos_detail_page.enter_computed_values_for_specific_indexes(2,5,1.5,3,1)
        self.pos_detail_page.enter_computed_values_for_specific_indexes(3,5,1.5,4,0)
        self.pos_detail_page.click_save_button()
        self.pos_detail_page.click_close_icon()
        self.logger.info("3. Search and find the POS and add Commisions to the POS - completed")

        self.logger.info("4. Enter the test step and clicks the 'Satış (3D)' button")
        self.home_page = HomePage(self.driver)
        self.transaction_page = self.home_page.hover_and_click_test_transactions()
        self.transaction_page.click_add_button()
        self.transaction_page.enter_amount("10")
        self.transaction_page.click_dropdowns_with_placeholder_text("Banka")
        self.transaction_page.select_option_from_dropdown("QNB FinansBank")
        self.transaction_page.click_dropdowns_with_placeholder_text("POS")
        self.transaction_page.select_option_from_dropdown("Cagatay")
        self.transaction_page.enter_card_number("5456165456165454")
        self.transaction_page.enter_card_holder_name("Octet test kart")
        self.transaction_page.enter_card_expire("1230")
        self.transaction_page.enter_card_cvv2("000")
        self.transaction_page.enter_reference_number("000")
        self.transaction_page.click_s3d_button()
        self.logger.info("4. Enter the test step and clicks the 'Satış (3D)' button - completed")

        self.logger.info("5. Next Steps....")

    def tearDown(self):
        """
        Teardown: Quit the driver after the test completes.
        """
        self.logger.info("Tearing down the test environment.")
        self.driver.quit()
        self.logger.info("WebDriver has been quit successfully.")