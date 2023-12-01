import os
from flask import Flask, render_template, request
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Set the API key for OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route('/')
def index():
  # Make sure 'index.html' is present in the 'templates' directory
  return render_template('index.html')


@app.route('/analyze_hpi', methods=['POST'])
def analyze_hpi():
  try:
    # Extract HPI from the form
    hpi = request.form['hpi']
    system_message = f"Analyze the HPI in the context of DSM-5: {hpi}"

    # Call the chat completion endpoint using gpt-4 for analyzing HPI
    response = openai.ChatCompletion.create(model="gpt-4",
                                            messages=[{
                                              "role": "system",
                                              "content": system_message
                                            }, {
                                              "role": "user",
                                              "content": hpi
                                            }])

    combined_responses = response.choices[0].message['content']

    # Create a summary using gpt-3.5-turbo-instruct through the legacy completions endpoint
    summary_prompt = f"""The provided prompt requests a structured summary based on the History of Presenting Illness (HPI) and an AI-generated analysis, aligning with DSM-5 criteria and patient-reported symptoms. The summary should be organized under two bold headings: Analysis and Recommendations.

        Analysis: This section should succinctly synthesize the HPI, focusing on key symptoms and their alignment with DSM-5 diagnostic criteria. It should be concise yet thorough in highlighting the core aspects of the patient's presentation, ensuring a clear understanding of the clinical picture.

        Recommendations: This part should offer clear, actionable steps for psychiatric care. It should discuss whether consulting with psychiatry is advisable, backed by specific DSM-5 criteria justifying the recommendation. The guidance provided should be direct and applicable, aiding in clinical decision-making.

        The summary's objective is to encapsulate essential insights from the HPI in a format conducive to immediate clinical application. It should maintain brevity while being comprehensive and clinically pertinent, within a word limit of 300 words. Now use the prompt above to work on:

        {combined_responses}. PLEASE FORMAT THE FINAL RESPONSE TO BE READABLE AND WELL PARAGRAPHED"""

    summary_response = openai.Completion.create(model='gpt-3.5-turbo-instruct',
                                                prompt=summary_prompt,
                                                max_tokens=1500)

    summary = summary_response.choices[0].text.strip()

    system_message_for_response = f"Organize the summary response in the context of DSM-5 under the following bolded headings: Analysis and Recommendations, both separated by two lines: {summary}"

    response_formatted = openai.ChatCompletion.create(
      model="gpt-4",
      messages=[{
        "role": "system",
        "content": system_message_for_response
      }, {
        "role": "user",
        "content": hpi
      }])

    return render_template(
      'results.html', summary=response_formatted.choices[0].message['content'])

  except Exception as e:
    # Handle unexpected exceptions
    return render_template('error.html', error_message=str(e))


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000, debug=True)
