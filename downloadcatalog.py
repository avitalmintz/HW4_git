import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep

BASE_URL = "http://collegecatalog.uchicago.edu/"

def fetch_page(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch page: {url}")
    sleep(3)
    return BeautifulSoup(response.text, 'html.parser')

programs_of_study_url = BASE_URL + 'thecollege/programsofstudy/'
programs_of_study_page = fetch_page(programs_of_study_url)
all_links = programs_of_study_page.find_all('a')
department_links = [a for a in all_links if '/thecollege/' in a['href']]
final_department_links = department_links[1:-13] 
all_major_links = [BASE_URL + a['href'].lstrip('/') for a in final_department_links]

course_data = []

for major_url in all_major_links:
    major_page = fetch_page(major_url)
    courses_in_major = major_page.find_all('div', class_='courseblock main')
    for course in courses_in_major:
        title_info = course.find('p', class_='courseblocktitle').get_text(strip=True).split('.')
        class_number = title_info[0].strip() if title_info else 'N/A'
        class_name = title_info[1].strip() if len(title_info) > 1 else 'N/A'
        units = title_info[2].strip() if len(title_info) > 2 else 'N/A'
        description = course.find('p', class_='courseblockdesc').get_text(strip=True)

        detail_element = course.find('p', class_='courseblockdetail')
        if detail_element:
            details_text = detail_element.get_text(strip=True).replace('\xa0', ' ')
            instructor_part = details_text.split('Instructor(s): ')[1] if 'Instructor(s):' in details_text else 'N/A'
            instructor = instructor_part.split('Terms Offered:')[0].strip() if 'Terms Offered:' in instructor_part else 'N/A'
            terms_offered = details_text.split('Terms Offered: ')[1].split('Prerequisite(s):')[0].strip() if 'Terms Offered:' in details_text else 'N/A'
            prerequisites_parts = details_text.split('Prerequisite(s): ')
            prerequisites = prerequisites_parts[1].split('Equivalent Course(s):')[0].strip() if len(prerequisites_parts) > 1 else 'N/A'
            equivalent_courses_parts = details_text.split('Equivalent Course(s): ')
            equivalent_courses = equivalent_courses_parts[1].strip() if len(equivalent_courses_parts) > 1 else 'N/A'
        else:
            instructor = terms_offered = prerequisites = equivalent_courses = 'N/A'

        course_data.append({
            'Class Number': class_number,
            'Class Name': class_name,
            'Units': units,
            'Description': description,
            'Instructor': instructor,
            'Terms Offered': terms_offered,
            'Prerequisites': prerequisites,
            'Equivalent Courses': equivalent_courses
        })

df_courses = pd.DataFrame(course_data)
df_courses.drop_duplicates(subset=['Class Name']).to_csv('catalog.csv', index=False)
print('Catalog data saved to catalog.csv')
department_data = [{'Department URL': url, 'Department Name': a.text.strip()} for a, url in zip(final_department_links, all_major_links)]
df_departments = pd.DataFrame(department_data)
df_departments.to_csv('department.csv', index=False)
print('Department data saved to department.csv')
