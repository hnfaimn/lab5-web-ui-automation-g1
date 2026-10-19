"""Lab 5: automate login, create a task, mark it complete, log out.

Filled in for Lab 5 Web UI Automation.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.login_page import LoginPage
from pages.task_page import NewTaskPage, TaskListPage

DEMO_USERNAME = "demo"
DEMO_PASSWORD = "demo1234"


def test_login_with_valid_credentials(driver, base_url):
    login_page = LoginPage(driver, base_url)
    login_page.open()
    login_page.login(DEMO_USERNAME, DEMO_PASSWORD)
    
    # Wait for the NewTaskPage title input field to prove login succeeded
    title_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(NewTaskPage.TITLE_INPUT)
    )
    assert title_input.is_displayed()


def test_login_with_invalid_credentials(driver, base_url):
    login_page = LoginPage(driver, base_url)
    login_page.open()
    login_page.login("demo", "wrong-password")
    error = login_page.wait_for_error()
    assert "Invalid username or password" in error.text


def test_create_task(driver, base_url):
    login_page = LoginPage(driver, base_url)
    login_page.open()
    login_page.login(DEMO_USERNAME, DEMO_PASSWORD)

    new_task_page = NewTaskPage(driver, base_url)
    new_task_page.create_task(
        title="Prepare slides",
        priority="2",
        due_date="2026-12-01",
        hours="3"
    )
    
    banner = new_task_page.wait_for_success()
    assert banner.is_displayed()


def test_mark_task_complete_and_logout(driver, base_url):
    login_page = LoginPage(driver, base_url)
    login_page.open()
    login_page.login(DEMO_USERNAME, DEMO_PASSWORD)

    # 1. Create a task first so there is something to complete
    new_task_page = NewTaskPage(driver, base_url)
    new_task_page.create_task(
        title="Task to complete",
        priority="1",
        due_date="2026-12-01",
        hours="1"
    )
    new_task_page.wait_for_success()

    # 2. Open task list and mark task complete
    task_list_page = TaskListPage(driver, base_url)
    task_list_page.open()
    task_list_page.mark_complete()
    
    # 3. Wait dynamically until status shows "Completed" (No time.sleep)
    assert task_list_page.wait_until_completed()

    # 4. Click logout link and confirm return to login page
    logout_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "logout-link"))
    )
    logout_link.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "username"))
    )
    assert "login" in driver.current_url.lower()