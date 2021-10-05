import os
import platform
import time
import requests
import zipfile
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


macM1 = False
email = ''
password = ''
url = ''

# PROGRAM DON'T TOUCH PLEASE
links = []


def download_chromedriver():
    if macM1:
        url = 'https://chromedriver.storage.googleapis.com/93.0.4577.63/chromedriver_mac64_m1.zip'
    else:
        url = 'https://chromedriver.storage.googleapis.com/93.0.4577.63/chromedriver_mac64.zip'

    if platform.system() == 'Windows':
        url = 'https://chromedriver.storage.googleapis.com/93.0.4577.63/chromedriver_win32.zip'

    r = requests.get(url, allow_redirects=True)
    open('chromedriver.zip', 'wb').write(r.content)

    with zipfile.ZipFile("chromedriver.zip", "r") as zip_ref:
        zip_ref.extractall("chromedriver")

    os.remove("chromedriver.zip")


def download_ffmpeg():
    url = 'https://evermeet.cx/ffmpeg/ffmpeg-103927-g68815d6791.zip'
    if platform.system() == 'Windows':
        url = 'https://github.com/GyanD/codexffmpeg/releases/download/2021-10-03-git-2761a7403b/ffmpeg-2021-10-03-git-2761a7403b-essentials_build.zip'

    r = requests.get(url, allow_redirects=True)
    open('ffmpeg.zip', 'wb').write(r.content)

    with zipfile.ZipFile("ffmpeg.zip", "r") as zip_ref:
        zip_ref.extractall("ffmpeg")

    os.remove("ffmpeg.zip")


def download_style():
    r = requests.get('https://drive.google.com/uc?export=download&id=1Yr3Hjv9XgPJfdMefFMXrAL2bSLw5epQd',
                     allow_redirects=True)
    open('style.css', 'wb').write(r.content)


def get_links(drvr):
    weeks = []
    for week in drvr.find_elements_by_css_selector('nav[role="navigation"] a'):
        weeks.append(week.get_attribute('href'))

    i = 1
    for week in weeks:
        print('Loading ' + str(i) + ' week...')
        drvr.get(week)

        while len(drvr.find_elements_by_class_name('m-composite-link')) == 0:
            time.sleep(1)

        for link in drvr.find_elements_by_css_selector('a.m-composite-link'):
            if "Quiz" not in link.get_attribute('data-ahoy-event-properties'):
                links.append(link.get_attribute('href'))
        i = i + 1


def find_browser():

    pathBraveMac = '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser'
    pathChromeMac = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'

    pathChromeWindows = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'

    if platform.system() == 'Windows':
        if os.path.isfile(pathChromeWindows):
            browser = pathChromeWindows
        else:
            browser = raw_input("Please, insert the path of your browser's EXE file (Only Chrome or Brave):")
    else:
        if os.path.isfile(pathBraveMac):
            browser = pathBraveMac
        elif os.path.isfile(pathChromeMac):
            browser = pathChromeMac
        else:
            browser = raw_input("Please, insert the path of your browser's app file (Only Chrome or Brave):")

    return browser


if __name__ == '__main__':

    print("You have installed this program successfully, now follow this steps:\n")

    browser = find_browser()

    if platform.system() == 'Darwin':
        print("Does your Mac have a M1 Processor? (True or False):")
        x = raw_input()
        if x == 'True':
            macM1 = x
        print("Saved: " + str(macM1) + "\n")

    if email == '':
        print("Enter the email of FutureLearn's account:")
        email = str(raw_input())

    if password == '':
        print("Enter your password:")
        password = str(raw_input())

    if url == '':
        print("Enter the link of your course:")
        url = str(raw_input())

    print('\nSystem: ' + platform.system())

    # DOWNLOADING FILES
    if not os.path.exists('style.css'):
        print("Downloading style...")
        download_style()

    if not os.path.exists('ffmpeg'):
        print("Downloading ffmpeg...")
        download_ffmpeg()
        os.chmod('ffmpeg/ffmpeg', 0775)

    if not os.path.exists('chromedriver'):
        print("Downloading chromedriver...")
        download_chromedriver()
        os.chmod('chromedriver/chromedriver', 0775)

    # CONSTRUCTOR
    options = Options()
    options.binary_location = browser
    drvr = webdriver.Chrome(options=options, executable_path='chromedriver/chromedriver')

    # LOGIN PAGE
    drvr.get('https://www.futurelearn.com/sign-in')

    while len(drvr.find_elements_by_id('onetrust-accept-btn-handler')) == 0:
        time.sleep(1)
    drvr.find_element_by_id('onetrust-accept-btn-handler').click()
    print('Login in...')
    drvr.find_element_by_css_selector('input[name="email"]').send_keys(email)
    drvr.find_element_by_css_selector('input[name="password"]').send_keys(password)
    drvr.find_element_by_css_selector('button[name="submit"]').click()

    # LOAD CONTENT
    while len(drvr.find_elements_by_id('main-content')) == 0:
        time.sleep(1)
    drvr.get(url)

    # GET LINKS
    get_links(drvr)

    # GET STEPS
    title = drvr.find_elements_by_class_name('mainHeader-runLink_ljhVP')[0].text

    print('Starting with ' + title)

    # CREATE DIRECTORIES
    if not os.path.exists(title.replace(' ', '_')):
        os.makedirs(title.replace(' ', '_'))
        os.makedirs(title.replace(' ', '_') + '/courses')
        os.makedirs(title.replace(' ', '_') + '/videos')

    # DOWNLOAD CONTENT
    i = 0
    for link in links:
        if i == 0:
            i = i + 1
            continue

        print('\nStarting with ' + link)
        drvr.get(link)

        if len(drvr.find_elements_by_id('main-content')) == 0:
            time.sleep(1)

        # DOWNLOAD VIDEO
        has_video = False
        if len(drvr.find_elements_by_css_selector('.video-js[tabindex="-1"]')) != 0:
            has_video = True
            loop = True

            while loop:
                drvr.find_elements_by_css_selector('.video-js[tabindex="-1"]')[0].click()
                time.sleep(2)
                resources = drvr.execute_script("return window.performance.getEntries();")
                for resource in resources:
                    if ".m3u8?ts=" in resource['name']:
                        print('Downloading video...')
                        os.system(os.getcwd() + '/ffmpeg/ffmpeg' + ' -i "' + resource[
                            'name'] + '" -bsf:a aac_adtstoasc -c copy ' + os.getcwd() + '/' + title.replace(' ',
                                                                                                            '_') + '/videos/' +
                                  link.split('steps/')[1] + '.mp4 -loglevel quiet')
                        loop = False
                        break

        # CHANGE VIDEO
        if has_video:
            elmnt = drvr.find_elements_by_css_selector(".video-module_wrapper__N3CvP")[0]
            drvr.execute_script(
                "arguments[0].innerHTML = '<video controls src=../videos/" + link.split('steps/')[1] + ".mp4>'", elmnt)

        # CHANGE NEXT AND PREVIOUS
        elmnt = drvr.find_elements_by_css_selector('a[aria-label="next step"]')[0]
        drvr.execute_script(
            "arguments[0].setAttribute('href', '" + elmnt.get_attribute('href').split('/')[7] + ".html')", elmnt)

        elmnt = drvr.find_elements_by_css_selector('a[aria-label="previous step"]')[0]
        drvr.execute_script(
            "arguments[0].setAttribute('href', '" + elmnt.get_attribute('href').split('/')[7] + ".html')", elmnt)

        # GET TEXT
        text = '<html><head><link rel="stylesheet" href="../../style.css"></head><body>' + \
               drvr.find_element_by_id('main-content').get_attribute('outerHTML').encode('utf-8').strip() + \
               '</body></html>'

        text = text.replace('/links/', 'https://www.futurelearn.com/links/')

        # CREATE FILE HTML
        print('Creating html file...')
        f = open(title.replace(' ', '_') + '/courses/' + link.split('steps/')[1] + '.html', "a")
        f.write(text)
        f.close()

        i = i + 1
