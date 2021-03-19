from colorama import Fore, Back, Style
from display import clear, print_info


def format_reed_raw_links(terms: str):
    with open('reed_raw_links.txt', 'r') as f:
        lines = f.readlines()

    jobs_links = list()

    for i, line in enumerate(lines):
        clear()

        if line.replace(' ', '') == '':
            continue

        url = 'https://www.reed.co.uk' # Set the base reed ur
        job_title = '' # Create variable to store the job title

        url_start_found = False
        url_end_found = False
        title_found = False
        title_start_found = False
        title_end_found = False
        for j, c in enumerate(line):
            if not url_start_found or not url_end_found:
                if c == '"' and not url_start_found:
                    url_start_found = True
                elif c == '"' and url_start_found and not url_end_found:
                    url_end_found = True
                elif url_start_found and not url_end_found:
                    url += c
            elif not title_found or not title_start_found or not title_end_found:
                if line[j:j+5] == 'title':
                    title_found = True
                elif title_found and not title_start_found and c == '"':
                    title_start_found = True
                elif title_start_found and not title_end_found and c == '"':
                    title_end_found = True
                elif title_start_found and not title_end_found:
                    job_title += c

        for term in terms.split(' '):
            if term.lower() in job_title.lower() and len(term) > 3:
                jobs_links.append(f'{job_title}||||{url}\n')
                break

    with open('job_links.txt', 'a') as f:
        f.writelines(jobs_links)


def format_indeed_raw_links(terms: str):
    with open('indeed_raw_links.txt', 'r') as f:
        lines = f.readlines()

    jobs_links = list()

    for line in lines:
        line_split = line.split('||||')
        link = ''
        title = ''
        for info in line_split:
            if info.strip() != '':
                if 'href="' in info:
                    link = 'https://uk.indeed.com' + info.replace('href=', '').replace('"', '').strip()
                elif 'title="' in info:
                    title = info.replace('title="', '').replace('"', '').strip()

        for term in terms.split(' '):
            if term.lower() in title.lower() and len(term) > 3:
                jobs_links.append(f'{title}||||{link}\n')
                break

    with open('job_links.txt', 'a') as f:
        f.writelines(jobs_links)


def format_cv_library_raw_links(terms: str):
    with open('cv_library_raw_links.txt', 'r') as f:
        lines = f.readlines()

    job_links = list()

    for line in lines:
        link = 'https://www.cv-library.co.uk'
        title = ''
        href_pos = line.find('href="')
        title_pos = line.find('title="')

        link_start = False
        title_start = False
        for i in range(href_pos,len(line)):
            c = line[i]
            if c == '"' and not link_start:
                link_start = True
            elif link_start:
                if c != '"':
                    link += c
                else:
                    break

        for i in range(title_pos, len(line)):
            c = line[i]
            if c == '"' and not title_start:
                title_start = True
            elif title_start:
                if c != '"':
                    title += c
                else:
                    break

        terms_split = terms.split(' ')
        for term in terms_split:
            if term.lower() in title.lower() and len(term) > 3:
                job_links.append(f'{title}||||{link}')
                break

        with open('job_links.txt', 'a') as f:
            f.writelines(job_links)
