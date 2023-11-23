import unittest
from app import app


class FlaskAppTests(unittest.TestCase):

  def setUp(self):
    # set up the application for testing
    app.testing = True
    self.client = app.test_client()

  def test_index_page(self):
    # Test index page loads successfully
    response = self.client.get('/')
    self.assertEqual(response.status_code, 200)
    self.assertIn('Medical HPI Analysis', response.get_data(as_text=True))

  def test_analyze_hpi_valid_input(self):
    # Test HPI analysis with valid input
    hpi_test_data = {
      'hpi': 'The patient has been feeling depressed for the past two weeks.'
    }
    response = self.client.post('/analyze_hpi', data=hpi_test_data)
    self.assertEqual(response.status_code, 200)
    self.assertIn('Analysis Results', response.get_data(as_text=True))

  def test_analyze_hpi_empty_input(self):
    # Test HPI analysis with empty input
    hpi_test_data = {'hpi': ''}
    response = self.client.post('/analyze_hpi', data=hpi_test_data)
    self.assertEqual(response.status_code, 200)
    self.assertIn('Error', response.get_data(as_text=True))

  def test_invalid_endpoint(self):
    # Test for non-existent endpoint
    response = self.client.get('/wrong_endpoint')
    self.assertEqual(response.status_code, 404)

  def test_content_type(self):
    # Test content type of index page
    response = self.client.get('/')
    self.assertEqual(response.content_type, 'text/html; charset=utf-8')

  # Additional tests can go here covering more use cases as needed.


if __name__ == '__main__':
  unittest.main()
