import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
import openai

load_dotenv()

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Assistant ID for the assistant you've already created
assistant_id = "asst_RZN0R97tu6PDxSimiO7CL6qv"  # Replace with your actual assistant ID


@app.route('/')
def index():
  return render_template('index.html')


@app.route('/analyze_hpi', methods=['POST'])
def analyze_hpi():
  try:
    hpi = request.form['hpi']

    # Call to GPT-4.0
    gpt4_response = openai.Completion.create(
      model='gpt-4',
      prompt=
      f"Analyze the HPI in the context of the Diagnostic and Statistical Manual of Mental Disorders, 5th Edition (DSM-5): {hpi}",
      max_tokens=100,
      n=1,
      stop=None,
      temperature=0.7)

    # Call to GPT-3.5-turbo
    gpt35_response = openai.Completion.create(
      model='gpt-3.5-turbo',
      prompt=
      f"Analyze the HPI in the context of the Diagnostic and Statistical Manual of Mental Disorders, 5th Edition (DSM-5): {hpi}",
      max_tokens=100,
      n=1,
      stop=None,
      temperature=0.7)

    # Create a new thread for the assistant
    thread = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                          messages=[{
                                            "role":
                                            "system",
                                            "content":
                                            "You are a helpful assistant."
                                          }, {
                                            "role": "user",
                                            "content": hpi
                                          }])

    assistant_response = thread.choices[0].message.content

    # Combine responses and summarize
    combined_responses = f"ANALYSIS:\n{gpt4_response.choices[0].text}\n\n{gpt35_response.choices[0].text}\n\n{assistant_response}"

    summary_prompt = combined_responses + "\n\nRECOMMENDATION:\nBased on the analysis, the following recommendations are suggested:\n\n- Consider a psychiatric consultation to assess the need for medication management and specialized treatment.\n- Explore outpatient therapy options such as cognitive-behavioral therapy (CBT) or dialectical behavior therapy (DBT) for targeted interventions.\n- Collaborate with a multidisciplinary team, including psychologists and social workers, to provide comprehensive support.\n- Discuss the potential benefits of group therapy or support groups to enhance social connections and shared experiences.\n\nThese recommendations are provided based on the analysis, but it is essential to consider the individual's specific needs and preferences when deciding on the appropriate management approach."

    summary_response = openai.Completion.create(model='gpt-3.5-turbo',
                                                prompt=summary_prompt,
                                                max_tokens=300,
                                                n=1,
                                                stop=None,
                                                temperature=0.7)

    summary = summary_response.choices[0].text.strip()

    return render_template('results.html', summary=summary)

  except Exception as e:
    error_message = f"An error occurred: {str(e)}"
    return render_template('error.html', error_message=error_message)


if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
