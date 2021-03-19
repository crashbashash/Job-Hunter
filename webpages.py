import requests
from random import randint


def random_user_agent():
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15']
    
    return user_agents[randint(0,len(user_agents)-1)]


def get_reed_webpage(search_terms: str, postcode: str, proximity: str, page=1, perm=False, temp=False, full_time=False, part_time=False, contract=False):
    url = 'https://www.reed.co.uk/jobs/' # Set the url to the base of the reed jobs url

    # Attach our search terms seperated by '-' to the url
    for term in search_terms.split(' '):
        if term != ' ' or term != '':
            url += term.lower() + '-'

    url += 'jobs-in-' + postcode.lower() # Attach our location in lowercase to the url

    # Create headers for the request
    headers = {
    'authority': 'www.reed.co.uk',
    'cache-control': 'max-age=0',
    'dnt': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': random_user_agent(),
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'accept-language': 'en-GB,en;q=0.9'
    }

    params = (
        ('pageno', str(page)),
        ('perm', perm),
        ('temp', temp),
        ('fulltime', full_time),
        ('parttime', part_time),
        ('contract', contract),
        ('proximity', proximity)
    )

    response = requests.get(url, headers=headers, params=params) # Send a request to the url specified
    get_body = response.text  # Get the raw text of the servers response

    error_filter = f'resulted in no matches'
    if error_filter in get_body:
        return False

    with open(f'response.html', 'w+') as f:
        f.write(get_body)
    
    return True


def get_indeed_webpage(last_page, search_terms: str, postcode: str, proximity: str, page=1, perm=False, full_time=False, part_time=False, contract=False):
    headers = {
        'authority': 'uk.indeed.com',
        'upgrade-insecure-requests': '1',
        'dnt': '1',
        'user-agent': random_user_agent(),
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

    if full_time:
        job_type = 'fulltime'
    elif part_time:
        job_type = 'parttime'
    elif perm:
        job_type = 'permanent'
    elif contract:
        job_type = 'contract'
    else:
        job_type = ''

    if proximity == '20' or proximity == '30':
        proximity = '25'

    if page == 1:
        page = ''
    else:
        page = f'{page-1}0'

    params = (
        ('q', search_terms),
        ('l', postcode),
        ('radius', proximity),
        ('jt', job_type),
        ('start', page)
    )

    response = requests.get('https://uk.indeed.com/jobs', headers=headers, params=params)

    if response.text == last_page:
        return False

    with open(f'response.html', 'w+') as f:
        f.write(response.text)

    return True


def get_cv_library_webpage(search_terms: str, postcode: str, proximity: str, page=1, perm=False, temp=False, part_time=False, contract=False):
    headers = {
        'authority': 'www.cv-library.co.uk',
        'upgrade-insecure-requests': '1',
        'dnt': '1',
        'user-agent': random_user_agent(),
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

    if proximity == '30':
        proximity = '35'

    params = (
        ('q', search_terms),
        ('distance', proximity),
        ('page', str(page)),
        ('contract', contract),
        ('temporary', temp),
        ('permanent', perm),
        ('part-time', part_time),
    )

    response = requests.get(f'https://www.cv-library.co.uk/jobs-in-{postcode.lower()}', headers=headers, params=params)

    if '0 jobs found.' in response.text:
        return False

    with open('response.html', 'w') as f:
        f.write(response.text)
    return True
