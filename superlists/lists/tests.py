from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.views import home_page

class HomePageTest(TestCase):
  def test_root_url_resolves_to_homepage_view(self):
    found = resolve('/')
    self.assertEqual(found.func, home_page)

  def test_homepage_returns_html(self):
    request = HttpRequest()
    request.method = 'POST'
    request.POST['item_text'] = 'A new list item'

    response = home_page(request)
    self.assertIn('A new list item', response.content.decode())
    expected_html = render_to_string(
      'home.html',
      {'new_item_text': 'A new list item'}
    )
    self.assertEqual(response.content.decode(), expected_html)