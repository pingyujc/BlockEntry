# this script should scrape the data from the job website store the information
# can store into firebase and maybe csv file too.


# website we are scraping from: https://www.dejob.top/job

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import csv
from bs4 import BeautifulSoup
import time

driver = webdriver.Chrome()


def scrape_jobs(job_names, companies, salaries, job_links):

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    # this one is the wrapper of all listings
    # listing1 = soup.find_all("div", class_="job_list-wrap__BGVhM")
    # print(listing1)

    # listings = soup.find_all("div", class_="job-item_job-item__hEOl6")

    # print(len(listings))

    # Find all the <a> tags that wrap the job listings
    job_links_elements = soup.find_all("a", href=True)

    # Iterate through each <a> tag and extract information
    for job_link_element in job_links_elements:
        # Extract the link from the <a> tag
        job_link = "https://www.dejob.top" + job_link_element["href"]

        # Find the job listing details within the <a> tag
        job_name = job_link_element.find("div", class_="job-item_company__PVLBK")
        company = job_link_element.find("div", class_="job-item_info__hVBPv")
        salary = job_link_element.find("div", class_="job-item_salary__yTSDI")

        if (
            job_name and company and salary
        ):  # Ensure elements are found before extracting text
            # Append the information to the lists
            job_names.append(job_name.text)
            companies.append(company.text)
            salaries.append(salary.text)
            job_links.append(job_link)

    # Print the lists
    # print("Job Names:", job_names)
    # print("Companies:", companies)
    # print("Salaries:", salaries)
    # print("Links:", job_links)


def navigate_to_next_page():
    try:
        # Find the 'Next' button and click it
        next_button_xpath = "//button[contains(@class, 'ant-pagination-item-link')][.//span[contains(@class, 'anticon') and contains(@class, 'anticon-right')]]"
        next_button = driver.find_element(By.XPATH, next_button_xpath)

        # Check if the 'Next' button is disabled
        # This can be done by checking for the 'disabled' attribute or a specific class that indicates it is disabled
        if next_button.get_attribute(
            "disabled"
        ) == "true" or "disabled-class" in next_button.get_attribute("class"):
            # If the button is disabled, we've reached the last page
            return False

        # print(next_button)
        next_button.click()
        time.sleep(1)  # Wait for the next page to load
        return True
    except NoSuchElementException:
        # If 'Next' button is not found, we've reached the end of the listings
        return False


# store data into csv file
def save_to_csv(job_names, companies, salaries, job_links, filename="dejob.csv"):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        # Write the header
        writer.writerow(["Job Name", "Company", "Salary", "Link"])
        # Write the job information
        for i in range(len(job_names)):
            writer.writerow([job_names[i], companies[i], salaries[i], job_links[i]])

    print(f"Data saved to {filename}")


def main():
    driver.get("https://www.dejob.top/job")
    # Lists to store the scraped info
    job_names = []
    companies = []
    salaries = []
    job_links = []
    time.sleep(2)  # wait for the page to load
    # i want to scrape 3 pages
    # for i in range(3):
    #     scrape_jobs(job_names, companies, salaries, job_links)
    #     print("scraping")
    #     if not navigate_to_next_page():
    #         break
    while True:
        scrape_jobs(job_names, companies, salaries, job_links)
        print("scraping")
        if not navigate_to_next_page():
            break

    save_to_csv(job_names, companies, salaries, job_links)
    # Close the driver
    driver.quit()


if __name__ == "__main__":
    main()
