from selenium import webdriver
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Wait for objects to load completely
def wait_load(path):
    try:
        element_present = EC.presence_of_element_located((By.XPATH, path))
        WebDriverWait(driver, 180).until(element_present)
    except TimeoutException:
        print("Timed out waiting for page to load")


# Go to courses search page
def courses_menu():
    path = "/html/body/div/div[1]/div/div/div/div[3]/div/div/div/div/div[8]/a/span"
    wait_load(path)
    element = driver.find_element(By.XPATH, path)
    wait_load(path)
    driver.execute_script("arguments[0].scrollIntoView(true);", element)
    wait_load(path)
    element.click()
    # driver.find_element(By.XPATH, path).click()
    path = "/html/body/div/div[1]/div/div/div/div[3]/div/div/div/div/div[8]/div/div[1]/a/span"
    wait_load(path)
    driver.find_element(By.XPATH, path).click()


# Search for course by course number
def course_number_goto(num):
    radio_path = "/html/body/div/div[3]/div/div/div[2]/div/div/div/form/div[2]/table/tbody/tr[2]/td[1]/input"
    wait_load(radio_path)
    driver.find_element(By.XPATH, radio_path).click()
    path_enter_code = "/html/body/div/div[3]/div/div/div[2]/div/div/div/form/div[2]/table/tbody/tr[2]/td[3]/input"
    wait_load(path_enter_code)
    driver.find_element(By.XPATH, path_enter_code).click()
    driver.find_element(By.XPATH, path_enter_code).send_keys(num)
    path_btn = "/html/body/div/div[3]/div/div/div[2]/div/div/div/form/div[2]/table/tbody/tr[8]/td/input[2]"
    wait_load(path_btn)
    element = driver.find_element(By.XPATH, path_btn)
    driver.execute_script("arguments[0].scrollIntoView(true);", element)
    element.click()


def check_element_exists(path):
    try:
        driver.find_element(By.XPATH, path)
    except NoSuchElementException:
        print("NoSuchElementException")
        return False
    return True


def register_course(path, is_available):
    wait_load("/html/body/div/div[3]/div/div/div[2]/div/div/div/form/div/div[2]/div/div/div[2]/div[2]/button")  # Info
    course_is_full_path = "/html/body/div/div[3]/div/div/div[2]/div/div/div/form/div/div[2]/div/div/div[2]/div[" \
                          "2]/button"  # Wait list button
    exist_bool_course_is_full = check_element_exists(course_is_full_path)
    if exist_bool_course_is_full:
        driver.back()
        return not is_available
    wait_load(path)
    element = driver.find_element(By.XPATH, path)
    driver.execute_script("arguments[0].scrollIntoView(true);", element)
    element.click()
    if final_reg:
        driver.back()  # To skip the close window which can't be clicked
    return is_available


def initialize_bools():
    global course_available
    global final_reg
    global skip_the_plan_b_course
    if not course_available:
        course_available = True
    if final_reg:
        final_reg = False
    if not skip_the_plan_b_course:
        skip_the_plan_b_course = True


# Setup chromedriver
PATH = "C:\chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.maximize_window()

# Open page for student information login
driver.get("https://info.braude.ac.il/yedion/fireflyweb.aspx?prgname=LoginValidation")

# Initialize & declare booleans (check before every course)
course_available = True  # Check if course is available for registration to complete the registration (lec, prac, lab)
final_reg = False  # Check if this is final part (lec, prac, lab) of the course
skip_the_plan_b_course = True  # In some cases I'll have two+ options, skip if the former registration was successful

courses_menu()  # Advanced WEB technologies -- lecture -> practice
course_number_goto("61977")
course_available = register_course("/html/body/div/div[3]/div/div/div[2]/div/div/div/form/div/div[2]/div[1]/div/div["
                                   "2]/div[1]/button", course_available)
if course_available:
    courses_menu()
    course_number_goto("61977")
    if not final_reg:  # False
        final_reg = not final_reg  # Change to True
    course_available = register_course("/html/body/div[2]/div[3]/div/div/div[2]/div/div/div/form/div/div[2]/div["
                                       "2]/div/div[2]/div[1]/button", course_available)
else:
    skip_the_plan_b_course = not skip_the_plan_b_course  # False

if not skip_the_plan_b_course:  # Programming Languages -- lec -> prac
    initialize_bools()
    courses_menu()
    course_number_goto("61980")
    course_available = register_course("/html/body/div/div[3]/div/div/div[2]/div/div/div/form/div/div[2]/div["
                                       "1]/div/div[2]/div[1]/button", course_available)
    if course_available:
        courses_menu()
        course_number_goto("61980")
        if not final_reg:  # False
            final_reg = not final_reg  # Change to True
        course_available = register_course("/html/body/div/div[3]/div/div/div[2]/div/div/div/form/div/div[2]/div["
                                           "3]/div/div[2]/div[1]/button", course_available)
######################################################################
######################################################################
initialize_bools()  # Scientific programming -- lec
courses_menu()
course_number_goto("61991")
if not final_reg:  # False
    final_reg = not final_reg  # Change to True
course_available = register_course("/html/body/div/div[3]/div/div/div[2]/div/div/div/form/div/div[2]/div/div/div["
                                   "2]/div[1]/button", course_available)
if not course_available:
    skip_the_plan_b_course = not skip_the_plan_b_course

if not skip_the_plan_b_course:  # Information theory -- lec
    initialize_bools()
    courses_menu()
    course_number_goto("61958")
    if not final_reg:
        final_reg = not final_reg
    course_available = register_course("/html/body/div/div[3]/div/div/div[2]/div/div/div/form/div/div[2]/div/div/div["
                                       "2]/div[1]/button", course_available)
######################################################################
######################################################################
initialize_bools()  # Android Development Lab -- lec -> lab
courses_menu()
course_number_goto("61985")
course_available = register_course("/html/body/div/div[3]/div/div/div[2]/div/div/div/form/div/div[2]/div[1]/div/div["
                                   "2]/div[1]/button", course_available)
if course_available:
    courses_menu()
    course_number_goto("61985")
    if not final_reg:
        final_reg = not final_reg
    course_available = register_course("/html/body/div/div[3]/div/div/div[2]/div/div/div/form/div/div[2]/div["
                                       "2]/div/div[2]/div[1]/button", course_available)
######################################################################
######################################################################
initialize_bools()  # Seminar in Algorithms -- lec
courses_menu()
course_number_goto("61968")
if not final_reg:
    final_reg = not final_reg
course_available = register_course("/html/body/div/div[3]/div/div/div[2]/div/div/div/form/div/div[2]/div/div/div["
                                   "2]/div[1]/button", course_available)
if not course_available:
    skip_the_plan_b_course = not skip_the_plan_b_course

if not skip_the_plan_b_course:  # Seminar in Software Verification -- lec
    initialize_bools()
    courses_menu()
    course_number_goto("61969")
    if not final_reg:
        final_reg = not final_reg
    course_available = register_course("/html/body/div/div[3]/div/div/div[2]/div/div/div/form/div/div[2]/div/div/div["
                                       "2]/div[1]/button", course_available)
######################################################################
######################################################################
initialize_bools()  # Data compression -- lec -> prac
courses_menu()
course_number_goto("61975")
course_available = register_course("/html/body/div/div[3]/div/div/div[2]/div/div/div/form/div/div[2]/div[1]/div/div["
                                   "2]/div[1]/button", course_available)
if course_available:
    courses_menu()
    course_number_goto("61975")
    if not final_reg:
        final_reg = not final_reg
    course_available = register_course("/html/body/div/div[3]/div/div/div[2]/div/div/div/form/div/div[2]/div["
                                       "2]/div/div[2]/div[1]/button", course_available)
else:
    skip_the_plan_b_course = not skip_the_plan_b_course

if not skip_the_plan_b_course:  # Digital Image Processing -- lec -> lab
    initialize_bools()
    courses_menu()
    course_number_goto("61971")
    course_available = register_course("/html/body/div/div[3]/div/div/div[2]/div/div/div/form/div/div[2]/div["
                                       "1]/div/div[2]/div[1]/button", course_available)
    if course_available:
        courses_menu()
        course_number_goto("61971")
        if not final_reg:
            final_reg = not final_reg
        course_available = register_course("/html/body/div/div[3]/div/div/div[2]/div/div/div/form/div/div[2]/div["
                                           "2]/div/div[2]/div[1]/button", course_available)
######################################################################
######################################################################
initialize_bools()  # Parallel and Distributed Programming using Cloud Technology -- lec -> prac
courses_menu()
course_number_goto("61768")
course_available = register_course("/html/body/div/div[3]/div/div/div[2]/div/div/div/form/div/div[2]/div[2]/div/div["
                                   "2]/div[1]/button", course_available)
if course_available:
    courses_menu()
    course_number_goto("61768")
    if not final_reg:
        final_reg = not final_reg
    course_available = register_course("/html/body/div/div[3]/div/div/div[2]/div/div/div/form/div/div[2]/div["
                                       "3]/div/div[2]/div[1]/button", course_available)
######################################################################
######################################################################
initialize_bools()  # Capstone Project – Phase 1
courses_menu()
course_number_goto("61998")
course_available = register_course("/html/body/div/div[3]/div/div/div[2]/div/div/div/form/div/div[2]/div/div/div["
                                   "2]/div[1]/button", course_available)
