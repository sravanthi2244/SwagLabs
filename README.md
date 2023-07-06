# **SwagLabs Web Application**
Welcome to the Swag Labs Web Application! This is a sample e-commerce web application built to showcase various features and functionality that can be implemented in an online store. 
It allows users to browse and purchase different products from the Swag Labs inventory.

This repository contains an **Automation script** for testing the Swag Labs Web Application. The script automates various scenarios to validate the functionality of the application.


The Swag Labs Web application link mentioned below. If you click on the given link it will navigate you to the Swag Labs Web application.

URL for Swag Labs Web Application -[Navigate to site](https://www.saucedemo.com/)


# **Prerequisites**
- Python 3.7 or higher installed on your machine
- Selenium WebDriver
- Chrome WebDriver (for running tests in Chrome)


# **Features**
- ## **Product Catalog :**
  -   The Product Catalog feature display of available products within the application.
  -   It provides users with comprehensive details such as the product's name, description, price, and images.
  -   Users can easily browse through the catalog and view detailed information about each product.
    
- ## **Product Sorting :**
  -  The Product Sorting feature allows users to sort the products in the catalog based on specific criteria.
  -  Users can choose to sort the products by price, name, or other relevant attributes.
  -  This functionality provides users with the ability to customize the product listing according to their preferences, making it easier to find the desired items.

- ## **Shopping Cart :**
  -   The Shopping Cart feature allows users to easily add products to their cart.
  -   Users can view the contents of their cart, review the selected items.
  -   Proceed to checkout when they are ready to complete their purchase.

- ## **Checkout Process :**
  -  During the checkout process, users  can enter their shipping details for the items in their cart.
  -  Once the shipping information is entered, they can Proceed to checkout and complete the purchase.



# **Test Scenarios**
The automation script covers the following test scenarios:

- **Login:** Validate the login functionality by entering valid and invalid credentials.

- **Product Sorting:** Test the sorting functionality by sorting products based on price, name, and other attributes.
  
- **Product Selection:** Verify the functionality of selecting a product from the product catalog and adding it to the shopping cart.

- **Shopping Cart:** Add products to the cart, verify the cart contents, and proceed to checkout.

- **Checkout Process:** Enter shipping details and complete the checkout process to verify successful purchase processing.



# Test Cases                      

 
| S.No | Test Case Name | Test Steps |
-------|----------------|-------|
|1 | User Login  | 1. Open the Swag Labs Web Application.<br/>2. Verify that the login page is displayed.<br/>3. Enter the username into the username input field.<br/>4. Enter the password into the password input field.<br/>5. Click on the login button.<br/>6. Verify that the login page is displayed.<br/>7. Repeat steps 3-5 of "User Login" for all available users.<br/>8. Validate whether all logins are successful or not.<br/>9. Verify that the appropriate error message is displayed after login failure..<br/>10. Click on the logout button.<br/>11. Verify that the user is logged out and redirected to the login page.
|2 | Product Sorting  | 1. Select the filtering dropdown and click<br/>2. Verify that the dropdown includes options for sorting the products.<br/>3. Verify that the default sorting option is displayed and selected.<br/>4. Select the sorting option.<br/>5. Validate  that the products are sorted correctly based on the selected sorting option.<br/>6. Repeat step 4-5 for all sorting options
|3 | Product Selection | 1. On the home page, verify that the list of products is displayed.<br/>2. Select a product from the list.<br/>3.  Click on a product name or image .<br/>4. Verify that the product details page is displayed.<br/>5. Check that the product name, description, and price are correctly displayed.</br>6. Perform any additional checks or validations required for the selected product.<br/>7.Repeate steps 2-6 for different products<br/>8. Click on "Back to Home" button and verify navigate user to Product/Home page
|4 | Shopping cart  | 1. Open the Swag Labs Web Application.<br/>2. Browse the product catalog and select a product to add to the cart.<br/>3. Verify that the selected product is added to the cart.<br/>4. Navigate to the shopping cart page and validate the added product.<br/>5. Ensure that the cart displays the correct quantity and total price of the selected items.                      
|5 | Checkout Process |1. Open the Swag Labs Web Application.<br/>2. Browse the product catalog and add one or more products to the cart.<br/>3. Navigate to the shopping cart page.<br/>4. Click on the "Proceed to Checkout" button.<br/>5. Enter the shipping details in the checkout section and click on "Proceed to Checkout."<br/>6. Validate that the shipping information is successfully entered and displayed correctly.<br/>7. Complete the checkout process and verify that the purchase is successfully processed.









