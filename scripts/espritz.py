import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


def espritz(sequence, queue, start_url='http://protein.bio.unipd.it/espritz/'):
    """
    Automation script for ESpritz protein disorder prediction webserver
    :param sequence:  str, protein sequence query
    :param queue:  list, container for return values
    :param start_url:  str, URL to webserver
    :return:  queue
    """
    # list mapping prediction options (for scraper) to what to put in the file name
    predictors_t = [['Xray', 'X-Ray'], ['Disprot', 'Disprot'], ['NMR', 'NMR']]

    def save_results(results):
        """ Parse HTML page source """
        data = []
        results = results.splitlines()
        results[0] = results[0][84:]
        results = results[:-1]
        for i in results:
            new = i[2:]
            data.append(new)

        for ind, aa in enumerate(data):
            data[ind] = aa.split(' ')  # split string and only take wanted value
        return data


    def check_if_loaded(browser):
        """
        Function to ensure the page has finished running before extracting the results.
        """
        # waits 1 hour before giving Timeout error
        # searches for notice element in the new page to know it has changed
        WebDriverWait(browser, 3600).until(EC.presence_of_element_located((By.ID, 'notice')))

    def submit_sequence(sequence, url, predictor):
        """
        create instance of chrome webdriver
        :param sequence:
        :param url:
        :param predictor:
        :return:
        """
        # need to add chromedriver to path, or specify its location here
        chrome_options = Options()
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--headless")  # run headless chrome
        browser = webdriver.Chrome(options=chrome_options)
        browser.get(url)

        # fill in form
        seq = browser.find_element_by_id('sequence')
        seq.send_keys(sequence)
        model = browser.find_element_by_name('model')
        for option in model.find_elements_by_tag_name('option'):
            if option.text == predictors_t[predictor][1]:
                option.click()

        # submit form
        browser.find_element_by_name('Submit Query').submit()

        # object to store url of new loading page
        new_url = browser.current_url
        # print(new_url)
        # print('Starting.')
        check_if_loaded(browser) # wait until page loads
        # print('Done loading.')
        window_before = browser.window_handles[0] # get window handle of results page

        # print(browser.current_url)
        links = browser.find_elements_by_tag_name('a') # get all links
        disorder = links[3]
        disorder.click()
        window_after = browser.window_handles[1] # get window handle of disorder data page
        browser.switch_to.window(window_after) # switch browser to new page
        html = browser.page_source # parse new page
        browser.quit()
        return html

    predictors = [0, 1, 2]
    espritz_total = []
    # 0 for short, 1 for long

    # run each predictor separately
    for pre in predictors:
        results = submit_sequence(sequence, start_url, pre)
        temp_results = save_results(results)
        espritz_total.append(temp_results)
        # time.sleep(60) # wait before running again

    queue.put(espritz_total)
    return espritz_total