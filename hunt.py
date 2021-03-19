#! /bin/python

import webpages
import filters
import formatting
import webbrowser
from display import print_info, print_input, print_error, print_job, clear
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-p', help='Max number of pages to fetch from each website', type=int)
args = parser.parse_args()


def get_terms():
    while True:
        clear()
        print_info('Please input the job you want to look for (e.g. Warehouse Operative)')
        terms = print_input('Job: ')
        if terms.replace(' ', '') == '':
            print_error('Please input a job to look for!!!')
            continue
        return terms


def get_postcode():
    while True:
        clear()
        print_info('Please input your postcode (e.g. ME91TP)')
        postcode = print_input('PostCode: ').strip().replace(' ', '')
        if postcode == '':
            print_error('Please enter a postcode!!!')
            continue
        return postcode


def get_proximity():
    prox_list = ['5', '10', '15', '20', '30', '50']
    while True:
        clear()
        print_info(f'Please input the proximity from your address ({str(prox_list).replace("[", "")})')
        proximity = print_input('Proximity: ').strip().replace(' ', '')
        if proximity not in prox_list:
            print_error(f'Please enter a valid proximity of {str(prox_list).replace("[", "")}')
            continue
        return proximity


def get_fulltime():
    while True:
        clear()
        print_info('Do you want to filter by Full Time jobs? (Default is \'no(n)\')')
        fulltime = print_input('y/n: ')
        formatted = fulltime.lower().replace(' ', '')
        if formatted == '' or formatted == 'n':
            return False
        elif formatted == 'y':
            return True
        else:
            print_error('Incorrect option given!!!\nPlease choose either \'y\' or \'n\'')
            continue


def get_parttime():
    while True:
        clear()
        print_info('Do you want to filter by Part Time jobs? (Default is \'no(n)\')')
        parttime = print_input('y/n: ')
        formatted = parttime.lower().replace(' ', '')
        if formatted == '' or formatted == 'n':
            return False
        elif formatted == 'y':
            return True
        else:
            print_error('Incorrect option given!!!\nPlease choose either \'y\' or \'n\'')
            continue


def get_contract():
    while True:
        clear()
        print_info('Do you want to filter by Contract jobs? (Default is \'no(n)\')')
        contract = print_input('y/n: ')
        formatted = contract.lower().replace(' ', '')
        if formatted == '' or formatted == 'n':
            return False
        elif formatted == 'y':
            return True
        else:
            print_error('Incorrect option given!!!\nPlease choose either \'y\' or \'n\'')
            continue


def get_temp():
    while True:
        clear()
        print_info('Do you want to filter by Temporary jobs? (Default is \'no(n)\')')
        temp = print_input('y/n: ')
        formatted = temp.lower().replace(' ', '')
        if formatted == '' or formatted == 'n':
            return False
        elif formatted == 'y':
            return True
        else:
            print_error('Incorrect option given!!!\nPlease choose either \'y\' or \'n\'')
            continue


def get_perm():
    while True:
        clear()
        print_info('Do you want to filter by Permanent jobs? (Default is \'no(n)\')')
        perm = print_input('y/n: ')
        formatted = perm.lower().replace(' ', '')
        if formatted == '' or formatted == 'n':
            return False
        elif formatted == 'y':
            return True
        else:
            print_error('Incorrect option given!!!\nPlease choose either \'y\' or \'n\'')
            continue


def get_search_info():
    # Get the search terms
    terms = get_terms()

    # Get the postcode
    postcode = get_postcode()

    # Get the proximity
    proximity = get_proximity()

    # Get Full Time
    fulltime = get_fulltime()

    # Get Part Time
    parttime = get_parttime()

    # Get Contract
    contract = get_contract()

    # Get Temp
    temp = get_temp()

    # Get perm
    perm = get_perm()

    # Return the parameters
    return terms, postcode, proximity, perm, temp, parttime, fulltime, contract


def display_jobs():
    jobs_list = list() # Store all jobs in a list
    reed_jobs = list() # Store all the reed jobs in list
    done = False # Variable to check if the user want's to exit the program

    with open('job_links.txt', 'r') as f:
        reed_jobs = f.readlines()

    for job in reed_jobs:
        jobs_list.append(job)

    for i, job in enumerate(jobs_list):
        job_split = job.split('||||')
        title = job_split[0] + f' {i+1}/{len(jobs_list)}'
        url = job_split[1]
        apply_for_job = False

        while True:
            clear()
            print_job(title, url)
            print_info('Would you like to apply to this job?')
            apply = print_input('[y/n]: ')
            apply = apply.lower().replace(' ', '')

            if apply == 'y':
                apply_for_job = True
                break
            elif apply == 'n':
                apply_for_job = False
                break
            else:
                print_error('Please select either \'y(yes)\' or \'n(no)\'')
                continue

        if apply_for_job:
            webbrowser.open(url)

            while True:
                clear()
                print_job(title, url)
                print('\n')
                print_info('Have you applied to the job? (y(yes)/n(no)/d(done)')
                applied = print_input('y/n/d: ')
                applied = applied.lower().replace(' ', '')

                if applied == 'y' or applied == 'n':
                    break
                elif applied == 'd':
                    done = True
                    break
                else:
                    print_error('Please input either \'y\' or \'n\' or \'d\'')
                    continue
        
        if done:
            break


def main():
    if args.p is None:
        max_pages = 6
    else:
        max_pages = args.p + 1

    try:
        search_terms, postcode, proximity, perm, temp, part_time, full_time, contract = get_search_info()
        postcode = postcode.lower().replace(' ', '')
        clear()

        # Make sure the '<website>_raw_links.txt' document for all the websites are created
        with open('reed_raw_links.txt', 'w+') as f:
            f.write('')

        with open('indeed_raw_links.txt', 'w+') as f:
            f.write('')

        with open('cv_library_raw_links.txt', 'w+') as f:
            f.write('')

        with open('job_links.txt', 'w+') as f:
            f.write('')

        # Get reed links
        for page_no in range(1, max_pages):
            if webpages.get_reed_webpage(search_terms, postcode, proximity, page_no, perm, temp, full_time, part_time, contract):
                print_info(f'Filtering Reed Jobs Page {page_no}')
                filters.filter_reed_raw_links()
            else:
                break

        # Get indeed links
        for page_no in range(1, max_pages):
            try:
                with open('response.html', 'r') as f:
                    prev_page = f.read()
            except FileNotFoundError:
                prev_page = ''

            if webpages.get_indeed_webpage(prev_page, search_terms, postcode, proximity, page_no, perm, full_time, part_time, contract):
                print_info(f'Filtering Indeed Jobs Page {page_no}')
                filters.filter_indeed_raw_links()
            else:
                break

        # Get CV Library links
        for page_no in range(1, max_pages):
            if webpages.get_cv_library_webpage(search_terms, postcode, proximity, page_no, perm, temp, part_time, contract):
                print_info(f'Filtering CV Library Jobs Page {page_no}')
                filters.filter_cv_library_links()
                page_no += 1
            else:
                break

        formatting.format_reed_raw_links(search_terms)
        formatting.format_indeed_raw_links(search_terms)
        formatting.format_cv_library_raw_links(search_terms)
        display_jobs()
    except KeyboardInterrupt:
        print_error('\'Keyboard Interrupt\' Intercepted!!!\nQuitting...', True)
        exit()


if __name__ == '__main__':
    main()
