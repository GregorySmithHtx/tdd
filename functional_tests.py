from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewVisitorTest(unittest.TestCase):
  def setUp(self):
      self.browser = webdriver.Firefox()
      self.browser.implicitly_wait(3)

  def tearDown(self):
    self.browser.quit()

  def check_for_row_in_list_table(self, row_text):
    table = self.browser.find_element_by_id('id_list_table')
    rows = table.find_elements_by_tag_name('tr')
    self.assertIn(row_text, [row.text for row in rows])

  def test_can_start_a_list_and_retrieve_it_later(self):
    #Open a browser to our homepage
    self.browser.get('http://localhost:3333')

    #Check out how the title mentions to-do lists
    self.assertIn('To-Do', self.browser.title)
    header_text = self.browser.find_element_by_tag_name('h1').text
    self.assertIn('To-Do', header_text)

    # Enter a to-do
    inputbox =  self.browser.find_element_by_id('id_new_item')
    self.assertEqual(
      inputbox.get_attribute('placeholder'),
      'Enter a to-do item'
    )
    # Type "Buy Peacock Feathers"
    inputbox.send_keys("Buy Peacock Feathers")

    # On enter, the page updates and lists 
    # "1: Buy Peacock Feathers" as a new to-do list item
    inputbox.send_keys(Keys.ENTER)
    self.check_for_row_in_list_table('1: Buy Peacock Feathers')

    # There is still a text box inviting her to add another item. She
    # enters "Use peacock feathers to make a fly" (Edith is very
    # methodical)
    inputbox = self.browser.find_element_by_id('id_new_item')
    inputbox.send_keys('Use peacock feathers to make a fly')
    inputbox.send_keys(Keys.ENTER)
    self.check_for_row_in_list_table('1: Buy Peacock Feathers')
    self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')

    self.fail('Finish the test!')
    # The page updates and shows both items

    # The should be a unique url to revisit to-do list

    # Visit that url see to-do list


if __name__ == '__main__':
  unittest.main(warnings='ignore')