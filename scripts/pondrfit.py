from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import queue

def pondrfit(sequence, queue):
    start_url = 'http://original.disprot.org/pondr-fit.php'
    def save_results(results):
        results = results.splitlines() # split by lines into list
        results = results[1:] # remove extra things we don't want

        # remove extra spaces
        for i in range(len(results)):
            results[i] = results[i].replace('  ', '')
            results[i] = results[i].replace('   ', ' ')
            results[i] = results[i].strip()
            results[i] = results[i]

        for ind,aa in enumerate(results):
            results[ind] = aa.split(' ')[2] # split string and only take wanted value

        return results

    def submit_sequence(sequence, start_url):
        chrome_options = Options()
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--headless")  # run headless chrome
        browser = webdriver.Chrome(options=chrome_options)
        browser.get(start_url) # navigate to page
        Sequence = browser.find_element_by_name('native_sequence')  # fill in form

        Sequence.send_keys(sequence)
        browser.find_element_by_xpath('/html/body/table[3]/tbody/tr[3]/td/input[1]').click() # submit form
        browser.find_element_by_xpath('/html/body/center[1]/a[4]').click() # click link with disorder data
        html = browser.find_element_by_xpath('/html/body/pre').text # parse new page
        browser.close()
        return html

    results = submit_sequence(sequence, start_url)

    predictions = save_results(results)

    queue.put(predictions)
    return predictions