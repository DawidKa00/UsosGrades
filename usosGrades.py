import argparse

from prettytable import PrettyTable
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

parser = argparse.ArgumentParser(prog='UsosGrades',
                                 description="Skrypt do pobrania i obliczenia średniej na USOS")
parser.add_argument("username", type=str, help="Identyfikator logowania na USOS / PESEL")
parser.add_argument("password", type=str, help="Hasło logowania")
args=parser.parse_args()

# Pobiera dostępne semestry
def get_available_semesters(driver):
    driver.get("https://usosweb.us.edu.pl/kontroler.php?_action=dla_stud/studia/oceny/index")

    frame_oceny = driver.find_element(By.ID, 'oceny')

    semestry_elements = frame_oceny.find_elements(By.XPATH, './/usos-frame-section[@section-title]')

    # Wyciągnij nazwy semestrów
    semestry = [sem.get_attribute("section-title") for sem in semestry_elements]

    return semestry

# Funkcja do wyboru semestru przez użytkownika
def choose_semester(driver):
    semesters = get_available_semesters(driver)
    semesters.append('Wszystkie semestry')
    print("Dostępne semestry:")
    for i, semestr in enumerate(semesters, start=1):
        print(f"{i}. {semestr}")

    choice = int(input("Wybierz numer semestru: ")) - 1
    if 0 <= choice < len(semesters) - 1:
        return semesters[choice], choice
    elif choice == len(semesters) - 1:
        return semesters[choice], choice
    else:
        print("\nBłędny wybór. Spróbuj ponownie.")
        return choose_semester(driver)

# Rozwiń tabelę semestrów
def expand_sections(driver, semester_num):
    wait = WebDriverWait(driver, 10)
    if semester_num >= 2:
        try:
            # Rozwiń sekcję
            expand_button = wait.until(EC.element_to_be_clickable((By.XPATH, f"/html/body/usos-layout/div[2]/main-panel/main/div/div/usos-frame/usos-frame-section[{semester_num}]")))
            expand_button.click()
        except Exception as e:
            print(f"Błąd podczas rozwijania sekcji: {e}")

# Funkcja do pobrania ocen z wybranego semestru
def get_grades(driver, semester_num):
    wait = WebDriverWait(driver, 10)
    semester_num += 1
    try:

        expand_sections(driver, semester_num)

        table_xpath = f"/html/body/usos-layout/div[2]/main-panel/main/div/div/usos-frame/usos-frame-section[{semester_num}]/table/tbody"

        table = wait.until(EC.presence_of_element_located((By.XPATH, table_xpath)))

        rows = table.find_elements(By.XPATH, ".//tr")

        grades = []
        for index, row in enumerate(rows, start=1):
            try:
                subject_name = row.find_element(By.XPATH, ".//a").text.strip()
                try:
                    subject_grade = row.find_element(By.XPATH, ".//td[3]/div[1]/span").text.strip()
                except NoSuchElementException:
                    subject_grade = row.find_element(By.XPATH, ".//td[3]/span").text.strip()
                grades.append((subject_name, subject_grade))

            except Exception as e:
                print(e)

        return grades
    except Exception as e:
        print(f"Błąd podczas pobierania tabeli lub wierszy: {e}")
        return []

# Funkcja do wyświetlania wyników
def display_results(grades):
    table = PrettyTable()
    table.field_names = ["Przedmiot", "Ocena"]
    sum = 0
    count = 0
    mean = 0

    for subject, grade in grades:
        table.add_row([subject, grade])
        if grade == "(brak ocen)" or grade == 'Zal': continue
        grade = grade.replace(',', '.')
        sum += float(grade)
        count += 1
    print(table)
    if count > 0:
        mean = sum / count
        mean = round(mean, 2)
    print(f"Łączna liczba liczonych przedmiotów: {count}")
    print("Średnia: ", mean)

# Funkcja do logowania do USOS
def login_usos(username, password, driver):
    # Przejdź do strony logowania
    driver.get(
        "https://logowanie.us.edu.pl/cas/login?service=https%3A%2F%2Fusosweb.us.edu.pl%2Fkontroler.php%3F_action%3Dlogowaniecas%2Findex&locale=pl")

    wait = WebDriverWait(driver, 20)
    # Znajdź pola loginu i hasła
    username_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
    password_field = driver.find_element(By.ID, "password")

    # Wprowadź dane logowania
    username_field.send_keys(username)

    password_field.send_keys(password)

    # Znajdź i kliknij przycisk "ZALOGUJ"
    login_button = driver.find_element(By.NAME, "submit")
    login_button.click()

    print("Logged in!")

def main():
    username = args.username
    password = args.password

    # Konfiguracja opcji Chrome dla trybu headless
    chrome_options = Options()
    # chrome_options.headless = True

    chrome_options.add_argument("disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-in-process-stack-traces")
    chrome_options.add_argument("--disable-logging")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--output=/dev/null")

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    driver.set_window_position(-10000, 0)
    try:
        # Logowanie
        login_usos(username, password, driver)

        selected_semester, semester_num = choose_semester(driver)
        if selected_semester == "Wszystkie semestry":
            for i in range(0, semester_num):
                grades = get_grades(driver, i)
                display_results(grades)
                print('-' * 80)
        else:
            print(f"Wybrany semestr: {selected_semester}")
            grades = get_grades(driver, semester_num)
            display_results(grades)

    except ValueError as e:
        print(f"Wystąpił błąd: {e}")
    finally:
        driver.quit()


if __name__ == "__main__":
    print('\n' * 40)
    main()
