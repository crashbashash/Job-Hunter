def filter_reed_raw_links():
    raw_link_list = list()  # Create list for raw unformatted links found in the 'response.html' file

    # Read the lines from the 'response.html' file
    with open(f'response.html', 'r') as file:
        file_lines = file.readlines()

    # Get raw job links
    for line in file_lines:
        line = line.strip() + '\n'
        if '<a href="/jobs/' in line:
            if 'sponsored_job_click' in line:
                raw_link_list.append(line)
            elif 'job_click' in line:
                raw_link_list.append(line)

    with open(f'reed_raw_links.txt', 'a') as f:
        f.writelines(raw_link_list)


def filter_indeed_raw_links():
    raw_link_list = list()  # Create a list for raw unformatted links found in the 'response.html' file

    # Read the lines from the 'response.html' file
    with open('response.html', 'r') as file:
        file_lines = file.readlines()

    # Get raw job links
    for i, line in enumerate(file_lines):
        line = line.replace('\n', '')
        if line == '<a' and file_lines[i+1].replace('\n', '') == 'target="_blank"' and file_lines[i+8].replace('\n', '') == 'class="jobtitle turnstileLink "':
            raw_link = ''
            for text in file_lines[i:i+8]:
                if 'href="' in text or 'title="' in text:
                    raw_link += text.replace('\n', '') + '||||'
            raw_link_list.append(raw_link + '\n')

    with open(f'indeed_raw_links.txt', 'a') as f:
        f.writelines(raw_link_list)
