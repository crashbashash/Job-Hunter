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
            if term in job_title:
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
            if term in title:
                jobs_links.append(f'{title}||||{link}\n')
                break

    with open('job_links.txt', 'a') as f:
        f.writelines(jobs_links)
