"""Page Objects for the task creation page and the task list page.

Filled in for Lab 5 Web UI Automation.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class NewTaskPage:
    TITLE_INPUT = (By.ID, "title")
    PRIORITY_INPUT = (By.ID, "priority")
    DUE_DATE_INPUT = (By.ID, "due_date")
    HOURS_INPUT = (By.ID, "hours")
    CREATE_BUTTON = (By.ID, "create-button")
    SUCCESS_BANNER = (By.ID, "success-banner")

    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url

    def open(self):
        self.driver.get(self.base_url + "/")
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.TITLE_INPUT)
        )

    def create_task(self, title, priority, due_date, hours):
        title_el = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.TITLE_INPUT)
        )
        title_el.clear()
        title_el.send_keys(title)

        priority_el = self.driver.find_element(*self.PRIORITY_INPUT)
        priority_el.clear()
        priority_el.send_keys(str(priority))

        due_date_el = self.driver.find_element(*self.DUE_DATE_INPUT)
        due_date_el.clear()
        due_date_el.send_keys(str(due_date))

        hours_el = self.driver.find_element(*self.HOURS_INPUT)
        hours_el.clear()
        hours_el.send_keys(str(hours))

        create_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.CREATE_BUTTON)
        )
        create_btn.click()

    def wait_for_success(self):
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.SUCCESS_BANNER)
        )


class TaskListPage:
    TASK_TABLE = (By.ID, "task-table")
    # Generic locators for the first task in the list
    ANY_COMPLETE_BUTTON = (By.XPATH, "//button[contains(text(), 'Complete') or contains(@class, 'complete') or @data-task-id]")
    FIRST_STATUS_CELL = (By.XPATH, "//td[contains(@id, 'status-')]")

    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url

    @staticmethod
    def complete_button(task_id):
        return (By.CSS_SELECTOR, f'button[data-task-id="{task_id}"]')

    @staticmethod
    def status_cell(task_id):
        return (By.ID, f"status-{task_id}")

    def open(self):
        self.driver.get(self.base_url + "/tasks")
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.TASK_TABLE)
        )

    def mark_complete(self, task_id=None):
        """Clicks the complete button. If task_id is given, uses specific button; otherwise finds the first complete button."""
        if task_id is not None:
            locator = (By.XPATH, f"//button[@data-task-id='{task_id}' or contains(@onclick, '{task_id}')]")
        else:
            locator = self.ANY_COMPLETE_BUTTON

        complete_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(locator)
        )
        complete_btn.click()

    def wait_until_completed(self, task_id=None):
        """Waits until status cell contains 'Completed'."""
        if task_id is not None:
            locator = self.status_cell(task_id)
        else:
            locator = self.FIRST_STATUS_CELL

        return WebDriverWait(self.driver, 10).until(
            EC.text_to_be_present_in_element(locator, "Completed")
        )
