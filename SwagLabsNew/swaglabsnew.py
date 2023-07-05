from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.select import Select
from Common_file import logger
from Common_file import CommonForAll

import random
class SwagLabsNew:

    def __init__(self):
        self.c = CommonForAll()
        self.config = self.c.get_config()
        if self.config:
            swag_log_file = self.config.get("log_file")
            self.c.setup_logging(swag_log_file)
            logger.info("Configuration loaded successfully")

            self.login = self.config.get("Login")
            self.logout = self.config.get("Logout",)
            self.sorting = self.config.get("productSorting")
            self.productSelection = self.config.get("productSelection")
            self.addtocart = self.config.get("AddToCart")
            self.addproduct = self.config.get("ProductAddtocart")
            self.checkout = self.config.get("CheckOut")
            self.addresses = self.config.get("addresses")
            logger.info("Initialization completed")

    def create_instance(self):
        try:
            service = Service(executable_path='chromedriver.exe')
            driver = webdriver.Chrome(service=service)
            driver.implicitly_wait(20)
            logger.info("WebDriver instance created successfully.")
        except Exception as e:
            logger.error(f"Error creating WebDriver instance: {str(e)}")
            return None
        else:
            return driver

    def perform_login(self, driver, username_key, password):
        # Method: perform_login
        if self.login:
            try:
                # Find username textbox, password textbox, and login button
                usr_text = self.c.wait_for_element(driver, 10, self.login, "userName_textbox")
                pass_word = self.c.wait_for_element(driver, 10, self.login, "passWord_textbox")
                login_button = self.c.wait_for_element(driver, 10, self.login, "loginButton", wait_for_clickable=True)

                # Retrieve username, password from the config file
                if usr_text and pass_word:
                    usr_text.clear()
                    usr_text.send_keys(username_key)

                    pass_word.clear()
                    pass_word.send_keys(password)

                if login_button:
                    driver.execute_script('arguments[0].click()', login_button)

                    # success_element = self.c.wait_for_element(driver, 5, self.login, "validate_homepage")
                    if self.c.wait_for_element(driver, 5, self.login, "validate_homepage"):
                        logger.info("%s: Login successful!", username_key)
                        return True
                    else:
                        logger.warning("Not navigated to Home page")
                        error_message_element = self.c.wait_for_element(driver, 5, self.login, "error_message")
                        if error_message_element:
                            error_message = error_message_element.text
                            logger.warning("%s: Login failed - %s", username_key, error_message)
                            logger.warning("Please login with a valid username and password.")
                            return False
                else:
                    logger.warning("Login button is not clickable")
            except Exception as e:
                logger.error(f"An error occurred: {str(e)}")

        else:
            logger.warning("Login key missing in config file")


    def extract_usernames(self, driver):
        if self.login:
            # Find the element containing the usernames and password
            user_names_element = self.c.wait_for_element(driver, 10, self.login, "userName")
            password_ele = self.c.wait_for_element(driver, 10, self.login, "password")

            # Extract the usernames and password from the element's text, excluding the first line
            if user_names_element is not None and password_ele is not None:
                user_names = user_names_element.text.split("\n")[1:]  # Exclude the first line
                password = password_ele.text.split("\n")[1:]  # Exclude the first line
                if user_names and len(user_names) > 0 and password:
                    # Using logger to display the extracted usernames and passwords
                    logger.info("Extracted Usernames: %s", user_names)
                    logger.info("Extracted Passwords: %s", password)
                    return user_names, password
        else:
            logger.warning("Login key missing in config file")

    def perform_logout(self, driver):
        if self.logout:
            # try:
                side_button = self.c.wait_for_element(driver, 20, self.logout, "sideButton", wait_for_clickable=True)
                if side_button:
                    driver.execute_script('arguments[0].click()', side_button)

                    logout_button = self.c.wait_for_element(driver, 20, self.logout, "logoutButton",
                                                            wait_for_clickable=True)
                    if logout_button:
                        driver.execute_script('arguments[0].click()', logout_button)

                        validate_logout = self.c.wait_for_element(driver, 20, self.logout, "ValidateLogout")

                        if validate_logout:
                            logger.info("User logged out successfully.")
                        else:
                            logger.warning("After logout not navigated to Login page")
                    else:
                        logger.warning("Logout button is not clickable")
                else:
                    logger.warning("Side button is not clickable")
            # except Exception as e:
            #     logger.error(f"An error occurred during logout: {str(e)}")
        else:
            logger.warning("Logout key missing in config file")


    def perform_testcase_1(self, driver):
        # Test Case 1: Login, Sorting, Logout
        usernames, password = self.extract_usernames(driver)

        for username in usernames:
            if self.perform_login(driver, username, password):
                # logger.info(f"Logged in as {username}")
                self.select_dropdown(driver)
                self.perform_logout(driver)
            logger.info("==========================================")


    def get_product_names(self, driver):
        # Retrieves the names of the products displayed on the page.
        product_names = self.c.wait_for_element(driver, 20, self.sorting, "productNames", extract_all=True)
        if product_names and len(product_names) > 0:
            return [product.text for product in product_names]
        else:
            logger.warning("No product names found.")
            return []

    def select_dropdown(self, driver):
        # Selects different options from the dropdown and validates the product names and prices for each option.
        if self.sorting:
            try:
                # Retrieve the default sorting option
                select_dropdown = self.c.wait_for_element(driver, 20, self.sorting, "selectDropdown")
                if select_dropdown:
                    default_option = self.c.wait_for_element(driver, 20, self.sorting, "defaultOption")
                    if default_option:
                        logger.info("Default sorting option: %s", default_option.text)
                    else:
                        logger.warning("No default sorting option was selected.")

                    # Retrieve the list of dropdown options
                    options_list = self.c.wait_for_element(driver, 20, self.sorting, "optionsList", extract_all=True)

                    if options_list and len(options_list) > 0:
                        for i in range(len(options_list)):
                            names_list_before = self.get_product_names(driver)
                            prices_list_before = self.get_product_prices(driver)
                            # Retrieve the dropdown element and select the option by index
                            dropdown = self.c.wait_for_element(driver, 40, self.sorting, "selectDropdown")
                            sl = Select(dropdown)
                            sl.select_by_index(i)

                            # Refresh the options_list
                            options_list = self.c.wait_for_element(driver, 40, self.sorting, "optionsList",
                                                                   extract_all=True)

                            option_text = options_list[i].text
                            if option_text:
                                names_list_after = self.get_product_names(driver)
                                prices_list_after = self.get_product_prices(driver)
                                # Determine if an option was selected
                                dropdown = self.c.wait_for_element(driver, 40, self.sorting, "selectDropdown")
                                sl = Select(dropdown)
                                selected_option = sl.first_selected_option
                                if selected_option:
                                    logger.info("Selected option: %s", selected_option.text)
                                    if option_text == "Name (A to Z)" or option_text == "Name (Z to A)":
                                        self.validate_product_names_change(names_list_before, names_list_after,
                                                                           option_text)
                                    elif option_text == "Price (low to high)" or option_text == "Price (high to low)":
                                        self.validate_product_prices_change(prices_list_before, prices_list_after,
                                                                            option_text)
                                    else:
                                        logger.warning("Unknown sorting option: %s", option_text)
                                else:
                                    logger.warning("No option was selected from the dropdown.")
                            else:
                                logger.warning("Test: FAIL: Option text not found: %s", option_text)

                    else:
                        logger.warning("No dropdown options found.")
                else:
                    logger.warning("No dropdown is found.")

            except Exception as e:
                logger.error("An error occurred: %s", str(e))
        else:
            logger.error("The product sorting key is missing in the config file.")

    def validate_product_names_change(self, names_before, names_after, option_text):
        # Validates if the product names have changed for the selected option.
        sorted_names = sorted(names_before)
        if option_text == "Name (Z to A)":
            sorted_names = sorted(names_before, reverse=True)

        if names_after == sorted_names:
            logger.info("Test: PASS - Product names are sorted correctly for option: %s", option_text)
        else:
            logger.info("Test: FAIL - Product names are not sorted correctly for option: %s", option_text)

    def validate_product_prices_change(self, prices_before, prices_after, option_text):
        # Validates if the product prices have changed for the selected option.
        if isinstance(prices_before, list) and isinstance(prices_after, list):
            if prices_before == sorted(prices_before) or prices_after == sorted(prices_after):
                logger.info("Test: PASS - Product prices are sorted correctly for option: %s", option_text)
            else:
                logger.info("Test: FAIL - Product prices are not sorted correctly for option: %s", option_text)
        else:
            logger.info("Test: FAIL - Invalid prices data for option: %s", option_text)

    def get_product_prices(self, driver):
        # Retrieves the prices of the products displayed on the page.
        product_prices = self.c.wait_for_element(driver, 20, self.sorting, "productPrices", extract_all=True)
        if product_prices and len(product_prices) > 0:
            return [float(price.text.replace("$", "")) for price in product_prices]
        else:
            logger.warning("No product prices found.")
            return []

    def back_to_products_btn(self, driver):
        # Clicks the "Back to products" button and waits for the desired page to load.
        try:
            back_to_products_btn = self.c.wait_for_element(driver, 20, self.productSelection,"backToProductsButton", wait_for_clickable=True)
            if back_to_products_btn:
                back_to_products_btn.click()
                logger.info("Clicked 'Back to products' button.")
                title_element = self.c.wait_for_element(driver, 20, self.productSelection, "validateHomepage")
                if not title_element:logger.warning("Failed to navigate to the home page.")
            else:logger.warning("Back to products button is not clickable.")

        except Exception as e:logger.error(str(e))
    def perform_testcase_2(self,driver):
        # Test Case 2: Login, Add item to cart based on add to cart buttons, Logout
        usernames,password= self.extract_usernames(driver)

        for username in usernames:
            if self.perform_login(driver, username, password):
                logger.info("Logged in successfully as %s.", username)

                self.add_all_items(driver)
                self.perform_logout(driver)

            logger.info("==========================================")

    def add_all_items(self, driver):
        if self.addtocart:
            initial_cart_count = self.get_cart_count(driver)

            # Find all "Add to Cart" buttons
            add_to_cart_buttons = self.c.wait_for_element(driver, 40, self.addtocart, "AddtocartButtons",
                                                          extract_all=True, wait_for_clickable=True)

            if add_to_cart_buttons and len(add_to_cart_buttons) > 0:
                for button in add_to_cart_buttons:
                    button.click()

                    # Update the initial cart count
                    initial_cart_count += 1

                # Wait for the cart count to update
                updated_cart_count = self.get_cart_count(driver)
                if initial_cart_count == updated_cart_count:
                    logger.info("All products have been successfully added to the cart")
                    logger.info("Test: PASS")
                else:
                    logger.info("Test: FAIL")

            else:
                logger.info("No 'Add to Cart' buttons found")
                updated_cart_count = self.get_cart_count(driver)
                if initial_cart_count != updated_cart_count:
                    logger.info("Some products may have been added to the cart")
                    logger.info("Test: PASS")
                else:
                    logger.info("No products added to the cart")
                    logger.info("Test: FAIL")

        else:
            logger.error("AddToCart key is missing in the configuration file")

    def get_cart_count(self, driver):
        cart_count_element = self.c.wait_for_element(driver, 20, self.addtocart, "CartStatus")
        if cart_count_element is not None:
            try:
                cart_count = int(cart_count_element.text)
                return cart_count
            except ValueError:
                logger.warning("Unable to parse the cart count as an integer.")
                return 0
        else:
            logger.warning("The cart count element was not found.")
            return 0

    def perform_testcase_3(self,driver):
        # Test Case 3: Login, Add all products to cart and perform checkout, Logout
        usernames,password= self.extract_usernames(driver)

        for username in usernames:
            if self.perform_login(driver, username, password):
                self.perform_check_out(driver)
                self.perform_logout(driver)

            logger.info("===============================================")

    def select_product(self, driver):
        # Step 1: Check if product list is displayed
        product_list = self.c.wait_for_element(driver, 20, self.productSelection, "beforeSelection", extract_all=True)
        if product_list and len(product_list) > 0:
            logger.info("List of products is displayed.")

        # Step 2: Select a product from the list
        if product_list and len(product_list) > 0:
            before_product_details = []
            for i in range(len(product_list)):
                product_list = self.c.wait_for_element(driver, 20, self.productSelection, "beforeSelection",
                                                       extract_all=True)
                product = product_list[i]

                product_name_ele = self.c.wait_for_element(product, 20, self.productSelection, "Bproduct_name")
                product_price = self.c.wait_for_element(product, 20, self.productSelection, "BproductPrice")
                product_desc = self.c.wait_for_element(product, 20, self.productSelection, "BproductDesc")

                if product_name_ele and product_price and product_desc:
                    before_details = {
                        'name': product_name_ele.text,
                        'price': product_price.text,
                        'description': product_desc.text
                    }
                    before_product_details.append(before_details)

                if product_name_ele:
                    product_name_ele.click()
                    logger.info(f"Clicked on product: {before_details['name']}")

                    # Step 3: Verify that the product details page is displayed
                    if self.c.wait_for_element(driver, 10, self.productSelection, "backToProductsButton"):
                        # Get the details of product after clicking
                        product_list_after = self.c.wait_for_element(driver, 20, self.productSelection, "AfterSelection", extract_all=True)

                        if product_list_after and len(product_list_after) > 0:
                            for j in range(len(product_list_after)):
                                displayed_product = product_list_after[j]

                                displayed_product_name = self.c.wait_for_element(displayed_product, 20, self.productSelection, "AproductName").text
                                displayed_product_price = self.c.wait_for_element(displayed_product, 20, self.productSelection, "AproductPrice").text
                                displayed_product_desc = self.c.wait_for_element(displayed_product, 20,self.productSelection, "AproductDesc").text
                                after_product_details = {
                                    'name': displayed_product_name,
                                    'price': displayed_product_price,
                                    'description': displayed_product_desc
                                }
                                # Step 4: Compare the product details and verify the correctness of displayed product details
                                if (before_details["name"] == after_product_details["name"] and
                                        before_details["price"] == after_product_details["price"] and
                                        before_details["description"] == after_product_details["description"]):
                                    add_to_cart_button = self.c.wait_for_element(driver, 20, self.addproduct,"AddtocartButton", wait_for_clickable=True)
                                    if add_to_cart_button:
                                        add_to_cart_button.click()
                                        logger.info(
                                            f"Clicked 'Add to Cart' button")
                                    else:
                                        logger.error("AddTo cart button is not clickable")
                            self.back_to_products_btn(driver)
                            logger.info("Returned to the product list page.")
            return before_product_details

    def perform_check_out(self, driver):
        # Step 1-4: Select a product and verify details
        before_product_details = self.select_product(driver)

        self.navigate_to_cart(driver)

        # Validate the details of added products to the cart
        after_list = self.cart_item_details(driver)

        if after_list:
            match_found = all(
                any(
                    added_product['name'] == before_product['name']
                    and added_product['price'] == before_product['price']
                    and added_product['description'] == before_product['description']
                    for added_product in after_list
                )
                for before_product in before_product_details
            )

            if match_found:
                logger.info("Product name, price, and description are MATCHED")

                check_out_btn = self.c.wait_for_element(driver, 20, self.checkout, "checkout_btn",
                                                        wait_for_clickable=True)
                if check_out_btn:
                    check_out_btn.click()
                    logger.info("Clicked on 'Checkout' button")

                    checkout_page = self.c.wait_for_element(driver, 20, self.checkout, "checkoutpage")
                    if checkout_page:

                        if self.checkout_address(driver):
                            logger.info("Checkout address validated")

                            continue_button = self.c.wait_for_element(driver, 20, self.checkout, "continue_btn",
                                                                      wait_for_clickable=True)
                            if continue_button:
                                continue_button.click()
                                logger.info("Clicked on 'Continue' button")

                                order_details_page = self.c.wait_for_element(driver, 20, self.checkout, "checkoutpage")
                                if order_details_page:

                                    prices = [item['price'] for item in after_list]
                                    each_item_price = 0
                                    for price in prices:
                                        each_item_price += float(price.split("$")[1])

                                    item_total_string = self.c.wait_for_element(driver, 20, self.checkout, "itemTotal")
                                    price_with_tax = self.c.wait_for_element(driver, 20, self.checkout, "taxPrice")
                                    total_string = self.c.wait_for_element(driver, 20, self.checkout, "TotalPrice")

                                    if item_total_string and price_with_tax and total_string:
                                        item_total_price = float(item_total_string.text.split("$")[1])
                                        tax = float(price_with_tax.text.split("$")[1])
                                        total = float(total_string.text.split("$")[1])

                                        if round(each_item_price) == round(item_total_price):
                                            logger.info("Sum of all product prices matched with item total price.")
                                            total_price = item_total_price + tax
                                            if round(total_price) == round(total):
                                                logger.info("Sum of tax price and item price matched with total price")

                                                finish_btn = self.c.wait_for_element(driver, 20, self.checkout,
                                                                                     "finish_button",
                                                                                     wait_for_clickable=True)

                                                if finish_btn:
                                                    finish_btn.click()
                                                    logger.info("Clicked on 'Finish' button")

                                                    complete_mesg = self.c.wait_for_element(driver, 20, self.checkout,
                                                                                            "complete_msg")
                                                    if complete_mesg:
                                                        logger.info(f"Order-Confirmation-Message: {complete_mesg.text}")
                                                        logger.info("Test: Pass")
                                                        back_to_home = self.c.wait_for_element(driver, 20,
                                                                                               self.checkout,
                                                                                               "backToHome",
                                                                                               wait_for_clickable=True)
                                                        if back_to_home:
                                                            back_to_home.click()
                                                            validate_homepage = self.c.wait_for_element(driver, 20,
                                                                                                        self.checkout,
                                                                                                        "validate_home_page")
                                                            if not validate_homepage:
                                                                logger.info("User not navigated to Homepage")
                                                        else:
                                                            logger.info("Test: FAIL")
                                                    else:
                                                        logger.info("Test: FAIL")
                                                else:
                                                    logger.error("Finish button is not clickable")
                                        else:
                                            logger.error("Sum of all product prices does not match item total price")
                                    else:
                                        logger.error("Not navigated to Order details page")
                                else:
                                    logger.error("Not navigated to checkout page")
                            else:
                                logger.error("Continue button is not clickable")
                        else:
                            logger.error("Test: Fail")
                    else:
                        logger.error("Not navigated to checkout page")
                else:
                    logger.error("Checkout button is not clickable")
            else:
                logger.error("Products details are not matched")
        else:
            logger.error("No products found in cart")
            logger.error("Test: FAIL")

    def checkout_address(self, driver):
        try:
            # Retrieve the text box elements
            first_name = self.c.wait_for_element(driver, 20, self.checkout, "firstName")
            last_name = self.c.wait_for_element(driver, 20, self.checkout, "lastName")
            postal_code = self.c.wait_for_element(driver, 20, self.checkout, "PostalCode")

            if first_name and last_name and postal_code:
                # Select a random address from the list
                random_address = random.choice(self.addresses)
                # Get the individual fields from the random address
                first_name_value = random_address['first_name']
                last_name_value = random_address['last_name']
                postal_code_value = random_address['postal_code']
                if first_name_value and last_name_value and postal_code_value:
                    # Clear the text boxes and enter values
                    first_name.clear()
                    first_name.send_keys(first_name_value)

                    last_name.clear()
                    last_name.send_keys(last_name_value)

                    postal_code.clear()
                    postal_code.send_keys(postal_code_value)
                    return True
                else:
                    logger.error("One or more fields are missing in the address.")
                    return False
        except Exception as e:
            logger.error("An exception occurred:", e)

    def cart_item_details(self, driver):
        logger.info("Retrieving product list from cart.")

        # Retrieve the product list elements from cart
        product_list_after = self.c.wait_for_element(driver, 20, self.addproduct, "cartItems", extract_all=True)
        added_product_details = []

        # Iterate over each product in the list
        if product_list_after and len(product_list_after) > 0:
            for j in range(len(product_list_after)):
                product = product_list_after[j]

                # logger.debug(f"Processing product {j + 1}/{len(product_list_after)}")

                # Retrieve the product details
                added_product_name = self.c.wait_for_element(product, 20, self.addproduct, "cartitemName")
                added_product_price = self.c.wait_for_element(product, 20, self.addproduct, "cartitemPrice")
                added_product_desc = self.c.wait_for_element(product, 20, self.addproduct, "cartitemDesc")

                if added_product_name and added_product_price and added_product_desc:
                    logger.debug("Retrieving product details.")

                    # Append the product details to the list
                    added_product_details.append({
                        'name': added_product_name.text,
                        'price': added_product_price.text,
                        'description': added_product_desc.text
                    })

                    logger.debug("Product details added to the list.")

            return added_product_details

    def navigate_to_cart(self, driver):
        # try:
            logger.info("Navigating to cart page.")

            # Wait for the cart icon to be clickable
            cart_icon = self.c.wait_for_element(driver, 10, self.addproduct, "cartIcon", wait_for_clickable=True)
            if cart_icon:
                cart_icon.click()

                logger.debug("Cart icon clicked.")

                cart_page_title = self.c.wait_for_element(driver, 20, self.addproduct, "validatecartpage")
                if cart_page_title:
                    logger.info("Successfully navigated to cart page.")
                else:
                    logger.warning("Failed to navigate to cart page.")
            else:
                logger.warning("Cart icon is not clickable.")
        # except Exception as e:
        #     logger.error("An exception occurred while navigating to cart page:", exc_info=True)

    def invoke_url(self):
        driver = self.create_instance()
        if driver:
            try:
                url = self.config.get("url")
                if url:
                    driver.get(url)
                    logger.info(f"Opened URL: {url}")
                    logger.debug(f"Page title: {driver.title}")
                    driver.maximize_window()

                    logger.info("Running Testcase-1")
                    self.perform_testcase_1(driver)

                    logger.info("Running Testcase-2")
                    self.perform_testcase_2(driver)

                    logger.info("Running Testcase-3")
                    self.perform_testcase_3(driver)

                else:
                    logger.warning("URL is missing.")
            except Exception as e:
                logger.error(f"An error occurred: {e}", exc_info=True)
            finally:
                driver.quit()


s = SwagLabsNew()
s.invoke_url()