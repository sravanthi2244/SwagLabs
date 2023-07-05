
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException,InvalidSelectorException
import yaml
import logging

# Create a logger object
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class CommonForAll:
    def get_config(self): # Load the YAML configuration file and retrieve the configuration settings

        try:
            with open('swag_config_new.yaml', 'r') as file:
                config = yaml.load(file, Loader=yaml.FullLoader)
            return config

        except FileNotFoundError:
            logger.error("Config file not found. Please check that the file 'config_file.yaml' exists in the current directory.", exc_info=True)
            return None
        except yaml.YAMLError as e:
            logger.error("Error occurred while loading the config file: {}".format(str(e)), exc_info=True)
            return None
        except Exception as e:
            logger.error("An unexpected error occurred while loading the config file: {}".format(str(e)), exc_info=True)
            return None


    def setup_logging(self, swag_log_file): # Set up logging configuration

        # Create a file handler to store logs in a file
        file_handler = logging.FileHandler(swag_log_file, mode="w")
        file_handler.setLevel(logging.INFO)

        # Create a console handler to display logs on the console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # Create a formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add the handlers to the logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)


    # Waits for an element to be present on the page
    def wait_for_element(self, driver, timeout, config, element_name, extract_all=False, wait_for_clickable=False):
        wait = WebDriverWait(driver, timeout)
        try:
            if not config or element_name not in config or not config[element_name]:
                logger.warning(f"Selector value for '{element_name}' is empty or not provided in the configuration.")
                return None

            selector = config[element_name]
            if selector.startswith("//"):  # Check if XPath selector
                if extract_all:
                    elements = wait.until(EC.visibility_of_all_elements_located((By.XPATH, selector)))
                else:
                    if wait_for_clickable:
                        element = wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                    else:
                        element = wait.until(EC.visibility_of_element_located((By.XPATH, selector)))
            else:  # Assume CSS selector

                if extract_all:
                    elements = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, selector)))
                else:
                    if wait_for_clickable:
                        element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                    else:
                        element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))

            if extract_all:
                return elements
            else:
                return element

        except TimeoutException as e:
            logger.error(f"Timeout occurred while waiting for element: {element_name}", )

        except NoSuchElementException:
            logger.error(f"Element not found: {element_name}", exc_info=True)
        except InvalidSelectorException:
            logger.error(f"Invalid selector for '{element_name}': Please check the selector value in the config file.",
                         exc_info=True)
        except Exception:
            logger.error(f"An error occurred while waiting for element: {element_name}", exc_info=True)
        return None
