from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class NewVisitorTest(FunctionalTest):
  def test_can_start_a_list_and_retrieve_it_later(self):
    #Open a browser to our homepage
    self.browser.get(self.server_url)

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

    # When she hits enter, she is taken to a new URL,
    # and now the page lists "1: Buy peacock feathers" as an item in a
    # to-do list table
    inputbox.send_keys(Keys.ENTER)
    edith_list_url = self.browser.current_url
    self.assertRegex(edith_list_url, '/lists/.+') #1
    self.check_for_row_in_list_table('1: Buy Peacock Feathers')

    # There is still a text box inviting her to add another item. She
    # enters "Use peacock feathers to make a fly" (Edith is very
    # methodical)
    inputbox = self.browser.find_element_by_id('id_new_item')
    inputbox.send_keys('Use peacock feathers to make a fly')
    inputbox.send_keys(Keys.ENTER)
    self.check_for_row_in_list_table('1: Buy Peacock Feathers')
    self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')

    # Now a new user, Francis, comes along to the site.

    ## We use a new browser session to make sure that no information
    ## of Edith's is coming through from cookies etc #1
    self.browser.quit()
    self.browser = webdriver.Firefox()

    # Francis visits the home page.  There is no sign of Edith's
    # list
    self.browser.get(self.server_url)
    page_text = self.browser.find_element_by_tag_name('body').text
    self.assertNotIn('Buy Peacock Feathers', page_text)
    self.assertNotIn('make a fly', page_text)

    # Francis starts a new list by entering a new item. He
    # is less interesting than Edith...
    inputbox = self.browser.find_element_by_id('id_new_item')
    inputbox.send_keys('Buy milk')
    inputbox.send_keys(Keys.ENTER)

    # Francis gets his own unique URL
    francis_list_url = self.browser.current_url
    self.assertRegex(francis_list_url, '/lists/.+')
    self.assertNotEqual(francis_list_url, edith_list_url)

    # Again, there is no trace of Edith's list
    page_text = self.browser.find_element_by_tag_name('body').text
    self.assertNotIn('Buy Peacock Feathers', page_text)
    self.assertIn('Buy milk', page_text)
    # The page updates and shows both items

    # The should be a unique url to revisit to-do list

    # Visit that url see to-do list