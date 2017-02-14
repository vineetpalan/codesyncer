import re
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait


class Hackerrank(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = webdriver.PhantomJS('phantomjs/bin/phantomjs')

    completed_challenges = dict()

    def wait_untill_completion(self, type_of_idenifier, value):
        element_present = expected_conditions.presence_of_element_located((type_of_idenifier, value))
        WebDriverWait(self.driver, 10).until(element_present)
        return

    def login(self):
        self.driver.get("https://www.hackerrank.com/auth/login/master")
        self.driver.find_element_by_name("login").send_keys(self.username)
        self.driver.find_element_by_id("legacy-login").find_element_by_name('password').send_keys(self.password)
        time.sleep(1)
        self.driver.find_element_by_id("legacy-login").find_element_by_name('commit').click()

    def get_submissions(self):
        self.wait_untill_completion(By.CLASS_NAME, 'span8')
        self.driver.get("https://www.hackerrank.com/submissions/all")
        self.wait_untill_completion(By.CLASS_NAME, 'chronological-submissions-list-view')
        elements = self.driver.find_elements_by_class_name("chronological-submissions-list-view")
        return elements

    def get_challenges_url(self):
        challenges = []
        elements = self.get_submissions()
        for val in elements:
            submission_time = val.find_elements_by_class_name('span2')[1].get_attribute('innerHTML')
            result = val.find_element_by_class_name('span3').get_attribute('innerHTML')
            if 'Accepted' in result and 'day' not in submission_time:
                challenges.append(
                    val.find_element_by_class_name('btn-wrap').find_element_by_css_selector('a').get_attribute('href'))
        return challenges

    def get_challenge_name(self, challenge):
        r = re.compile('challenges/(.*?)/submissions')
        return r.search(challenge).group(1).replace('-', '_').capitalize()

    def save_to_file(self, challenge, submission_code):
        challenge_name = self.get_challenge_name(challenge).title()
        f = open(challenge_name + '.java', "w")
        f.write(submission_code.text)
        challenge_name = challenge_name.replace('_',' ')
        self.completed_challenges[challenge_name]=os.path.abspath(f.name)
        f.close()

    def get_challenges(self):
        for challenge in self.get_challenges_url():
            self.driver.get(challenge)
            self.wait_untill_completion(By.ID, 'submission-code')
            self.wait_untill_completion(By.CLASS_NAME,'testcase-card-wrap')
            gutter_elements = self.driver.find_elements_by_class_name('CodeMirror-gutter-wrapper')
            for gutter_element in gutter_elements:
                self.driver.execute_script('arguments[0].innerHTML=""', gutter_element)

            submission_code = self.driver.find_element_by_id('submission-code')
            self.save_to_file(challenge, submission_code)

    def start_sync(self):
        self.login()
        self.get_challenges()
        return self.completed_challenges