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
    summary_prompt = (
    "Utilize the provided History of presenting illness (HPI) and accompanying AI-generated analysis "
    "to create a structured summary. This summary should strictly adhere to DSM-5 criteria and patient-reported symptoms. "
    "Organize the content into two distinct sections with bold headings: **Analysis** and **Recommendations**. "
    "Under **Analysis**, succinctly synthesize the HPI information, highlighting key symptoms and their correlation "
    "with DSM-5 diagnostic criteria. Under **Recommendations**, provide clear and actionable steps for psychiatric care, "
    "including the consideration of consulting psychiatry or not, with specific reasons from DSM-5 criteria to support "
    "the recommendation. The summary should be precise and encapsulate all critical insights from the HPI, "
    "formatted to be immediately applicable in a clinical context. Maintain brevity while ensuring the summary "
    "remains comprehensive and clinically relevant. 300 words maximum in total."f"\n\n{combined_responses}")

    summary_response = openai.Completion.create(model='gpt-3.5-turbo-instruct',
                                                prompt=summary_prompt,
                                                max_tokens=1500)

    summary = summary_response.choices[0].text.strip()

    return render_template('results.html', summary=summary)

  except Exception as e:
    # Handle unexpected exceptions
    return render_template('error.html', error_message=str(e))


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000, debug=True)
