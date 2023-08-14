from selenium import webdriver
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from colorama import Fore, init
import random, time, cloudscraper, requests

ua = UserAgent()
init(autoreset=True) 

def get_random_user_agent():
    return ua.random

def random_sleep():
    time.sleep(random.uniform(1, 2))

def get_proxies(max_proxies):
    proxies = []
    urls = [
        'https://raw.githubusercontent.com/UptimerBot/proxy-list/main/proxies/http.txt',
        'https://raw.githubusercontent.com/saschazesiger/Free-Proxies/master/proxies/http.txt',
        'https://raw.githubusercontent.com/ALIILAPRO/Proxy/main/http.txt',
        'https://raw.githubusercontent.com/prxchk/proxy-list/main/http.txt',
        'https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/http.txt',
        'https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/http.txt',
        'https://sunny9577.github.io/proxy-scraper/proxies.txt',
        'https://raw.githubusercontent.com/zevtyardt/proxy-list/main/http.txt',
        'https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies_anonymous/http.txt'
    ]
    
    for url in urls:
        if len(proxies) >= max_proxies:
            break
        
        try:
            response = requests.get(url)
            if response.status_code == 200:
                new_proxies = [line.strip() for line in response.text.splitlines() if line.strip()]
                
                if len(proxies) + len(new_proxies) > max_proxies:
                    needed_proxies = max_proxies - len(proxies)
                    proxies += new_proxies[:needed_proxies]
                else:
                    proxies += new_proxies
                    
        except Exception as e:
            print(f"{Fore.RED}Error fetching proxies from {url}: {e}")

    return proxies

def is_proxy_working(proxy, test_url="http://www.google.com/", timeout=4):
    scraper = cloudscraper.create_scraper()
    scraper.proxies = {"http": proxy, "https": proxy}
    
    try:
        response = scraper.get(test_url, timeout=timeout)
        return 200 <= response.status_code < 300
    except (cloudscraper.exceptions.CloudflareChallengeError, requests.exceptions.ConnectTimeout):
        return False
    except Exception as e:
        return False

def filter_working_proxies(proxies, test_url, max_workers=100):
    working_proxies = []

    print(f"{Fore.CYAN}Checking proxies against {test_url} ...")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(tqdm(executor.map(lambda proxy: is_proxy_working(proxy, test_url), proxies), total=len(proxies), bar_format=Fore.GREEN + '{l_bar}{bar}{r_bar}'))
        
        for proxy, working in zip(proxies, results):
            if working:
                working_proxies.append(proxy)

    print(f"{Fore.GREEN}Working proxies: {Fore.CYAN}{len(working_proxies)}/{len(proxies)}")

    return working_proxies

def get_chrome_driver(proxy=None, headless=True, no_proxy=False):
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--log-level=3")
    
    if proxy:
        options.add_argument(f"--proxy-server={proxy}")
    
    if headless:
        options.add_argument('--headless')
        
    if no_proxy:
        options.add_argument('--no-proxy-server')
    
    options.add_argument(f"--user-agent={get_random_user_agent()}")
    options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
    prefs = {"profile.default_content_setting_values.notifications": 2, "images": 2, "javascript": 1}
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=options)
    
    return driver

def check_single_link_with_selenium(href, proxy):
    driver = get_chrome_driver(proxy=proxy, headless=True, no_proxy=False)
    
    try:
        driver.get(href)
        if driver.current_url != href:
            driver.quit()
            return href
    except Exception as e:
        driver.quit()
        return href
    
    driver.quit()
    return None

def check_single_link(args):
    href, proxy = args
    broken_link = None

    random_sleep()
    
    scraper = cloudscraper.create_scraper(
        browser={
            'browser': 'chrome',
            'platform': 'windows',
            'mobile': False
        }
    )
    scraper.proxies = {"http": proxy, "https": proxy}
    headers = {
        "Referer": "https://www.google.com/" 
    }
    scraper.headers.update(headers)

    try:
        response = scraper.get(href, timeout=10)
        if not(200 <= response.status_code < 300):
            if response.status_code == 403:
                broken_link = check_single_link_with_selenium(href, proxy)
            else:
                broken_link = href
                print(f"Broken link: {href} -> Status code: {response.status_code}")
    except cloudscraper.exceptions.CloudflareChallengeError:
        pass
    except Exception as e:
        pass
    
    return broken_link

def check_links(url):
    driver = get_chrome_driver(headless=True, no_proxy=True)
    driver.get(url)
    links = [link.get_attribute('href') for link in driver.find_elements(By.TAG_NAME, 'a') if link.get_attribute('href')]
    driver.quit()

    link_proxy_pairs = [(link, random.choice(proxies)) for link in links]

    broken_links = []
    with ThreadPoolExecutor(max_workers=50) as executor:
        for broken_link in executor.map(check_single_link, link_proxy_pairs):
            if broken_link:
                broken_links.append(broken_link)

    return broken_links

if __name__ == "__main__":
    target_url = input(f"{Fore.GREEN}Enter your website: {Fore.CYAN}")
    max_proxies = int(input(f"{Fore.GREEN}Number of proxies you want to get: {Fore.CYAN}"))
    proxies = filter_working_proxies(get_proxies(max_proxies), target_url)
    if not proxies:
        print(f"{Fore.RED}No working proxies found. Exiting...")
        exit()

    broken_links_list = check_links(target_url)

    if not broken_links_list:
        print(f"{Fore.GREEN}No broken links found!")
    else:
        print(f"{Fore.GREEN}Total broken links found: {Fore.RED}{len(broken_links_list)}")