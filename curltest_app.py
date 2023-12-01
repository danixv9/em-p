CURL /__replauthuser
X-Replit-User-Id
X-Replit-User-Name
X-Replit-User-Teams
X-Replit-User-Roles
CURL /__replauthuser
CURL /__replauthuser
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Retrieve OpenAI API key from the environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
HEADERS = {
  'Authorization': f'Bearer {OPENAI_API_KEY}',
  'Content-Type': 'application/json'
}


class TestCurlApp:

  def send_request(self, url, data):
    try:
      response = requests.post(url, json=data, headers=HEADERS)
      response.raise_for_status()
      return response.json()
    except requests.exceptions.HTTPError as http_err:
      print(
        f"HTTP error occurred: {http_err} - Status Code: {http_err.response.status_code}"
      )
    except requests.exceptions.ConnectionError as conn_err:
      print(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
      print(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
      print(f"An unknown error occurred: {req_err}")
    return None

  def test_api_gpt35(self):
    print("Testing GPT-3.5 API...")
    data = {
      'model': 'gpt-3.5-turbo',
      'prompt': 'This is a test prompt for GPT-3.5.',
      'max_tokens': 5
    }
    result = self.send_request(
      'https://api.openai.com/v1/engines/gpt-3.5-turbo/completions', data)
    if result:
      print("GPT-3.5 Model Response: ", result)

  def test_api_gpt4(self):
    print("Testing GPT-4.0 API...")
    data = {
      'model': 'gpt-4',
      'prompt': 'This is a test prompt for GPT-4.0.',
      'max_tokens': 5
    }
    result = self.send_request(
      'https://api.openai.com/v1/engines/gpt-4/completions', data)
    if result:
      print("GPT-4.0 Model Response: ", result)

  def test_api_gpt4_32k(self):
    print("Testing GPT-4 32K Model API...")
    data = {
      'model': 'gpt-4-32k',
      'prompt': 'This is a test prompt for GPT-4 32K token model.',
      'max_tokens': 5
    }
    result = self.send_request(
      'https://api.openai.com/v1/engines/gpt-4-32k/completions', data)
    if result:
      print("GPT-4 32K Model Response: ", result)

  def test_api_assistant(self):
    print("Testing Assistant API...")
    assistant_id = "asst_RZN0R97tu6PDxSimiO7CL6qv"  # Replace with your actual assistant ID
    data = {'model': 'gpt-3.5-turbo', 'inputs': 'Tell me a joke.'}
    result = self.send_request(
      f'https://api.openai.com/v1/assistants/{assistant_id}/messages', data)
    if result:
      print("Assistant Model Response: ", result)


# Execute the tests
if __name__ == '__main__':
  test_api = TestCurlApp()
  test_api.test_api_gpt35()
  test_api.test_api_gpt4()
  test_api.test_api_gpt4_32k()
  test_api.test_api_assistant()
