import csv
import json
import os.path
import traceback

import requests
from bs4 import BeautifulSoup

email = 'youremail@gmail.com'
password = 'yourpass'
infile = "./linkedin-in.csv"
outfile = "./linkedin-out.csv"

login = 'https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin'
submit = 'https://www.linkedin.com/uas/login-submit'
headers = ["company_name", "linkedin_url", "Description", "url", "keywords", "btype", "product_url"]


def main():
    os.system('color 0a')
    logo()
    print(f"Logging in using email {email}...")
    client = requests.Session()
    soup = BeautifulSoup(client.get(login).content, "html.parser")
    login_information = {
        'session_key': email,
        'session_password': password,
        'loginCsrfParam': soup.find('input', {'name': "loginCsrfParam"})['value'],
    }
    client.post(submit, data=login_information)
    with open(infile, 'r', encoding='utf8', errors='ignore') as temp:
        inlines = [line for line in csv.reader(temp)]
    if not os.path.isfile(outfile):
        with open(outfile, 'w', encoding='utf8', errors='ignore') as temp:
            csv.writer(temp).writerow(headers)
    with open(outfile, 'r', encoding='utf8', errors='ignore') as temp:
        outlines = temp.read()
    # print(outlines)
    for line in inlines[1:]:
        url = f"{line[1]}/about"
        print(url)
        if line[1] not in outlines:
            desc = "Not found"
            try:
                content = client.get(url).content
                # print(content)
                codes = BeautifulSoup(content, "lxml").findAll('code')
                # print(len(codes))
                if len(codes) > 0:
                    for code in codes:
                        if "articlePermalinkForTopCompanies" in code.text:
                            js = json.loads(codes[18].text)
                            for included in js['included']:
                                if 'description' in included.keys() and included['description'] is not None and len(
                                        included['description']) > 5:
                                    desc = included['description'].strip().replace("\n", " ").replace("\r", " ")
                                    print(desc)
                                    line[2] = desc
                                    with open(outfile, 'a', encoding='utf8', errors='ignore', newline='') as temp:
                                        csv.writer(temp).writerow(line)
                                    break
                            break
                else:
                    input("Pls login using browser and fill captcha...")
            except Exception as e:
                traceback.print_exc()
                print(e)
                with open("error.csv", 'a', encoding='utf8', errors='ignore', newline='') as temp:
                    csv.writer(temp).writerow(line)
            # input("press any key")
        else:
            print("Already scraped!")


def logo():
    print("""
    .____    .__        __              .___.___        
    |    |   |__| ____ |  | __ ____   __| _/|   | ____  
    |    |   |  |/    \|  |/ // __ \ / __ | |   |/    \ 
    |    |___|  |   |  \    <\  ___// /_/ | |   |   |  \\
    |_______ \__|___|  /__|_ \\\\___  >____ | |___|___|  /
            \/       \/     \/    \/     \/          \/ 
=====================================================================
        Scrape 'about' info from list of linkedin profiles
            Developed by: github.com/evilgenius786
=====================================================================
[+] Multithreaded
[+] Without browser
""")


if __name__ == "__main__":
    main()
