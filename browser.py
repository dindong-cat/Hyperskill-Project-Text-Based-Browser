import sys
import os
import requests
from bs4 import BeautifulSoup
from colorama import Fore


def print_and_save_result(url, r):
    soup = BeautifulSoup(r.text, 'html.parser')
    for i in soup.find_all("a"):
        i.string = "".join([Fore.BLUE, i.get_text(), Fore.RESET])
    result = soup.get_text()
    print(result)
    file_name = url.split(".")[0].replace("https://", "")
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(result)


def main():
    args = sys.argv
    dir = args[1]
    if not os.access(dir, os.F_OK):
        os.makedirs(dir)
    os.chdir(dir)
    browse_history = []
    headers = {'User-Agent': 'Mozilla/5.0'}

    while True:
        url = input()
        if url == "exit":
            break
        elif url == "back":
            browse_history.pop()
            url = browse_history.pop()
            r = requests.get(url, headers=headers)
            print_and_save_result(url, r)
        else:
            if "https://" not in url:
                url = "https://" + url
                try:
                    r = requests.get(url, headers=headers)
                    if r:
                        browse_history.append(url)
                        print_and_save_result(url, r)
                    else:
                        print("Error: Incorrect URL")
                except requests.exceptions.ConnectionError:
                    print("Incorrect URL")


if __name__ == "__main__":
    main()
