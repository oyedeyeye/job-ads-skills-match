from flask import Flask, request, jsonify
from dotenv import load_dotenv
import asyncio
import aiohttp
import os
import google.generativeai as genai


load_dotenv()
APP_ID = os.getenv('APP_ID')
APP_KEY = os.getenv('APP_KEY')

# Configure Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Flask app
app = Flask(__name__)


input_prompt = """
You are a highly experienced Application Tracking System (ATS) specializing in evaluating resumes for tech roles. Your task is to assess the provided candidate profile against the given job description.

Focus on identifying the alignment between skills, experience, and requirements. Provide a match score as a percentage (0-100%) based on relevance and list any missing keywords from the profile that are important for the job.

Candidate Profile:
"{candidate_profile}"

Job Description:
"{job_description}"

Format your response as a single JSON string with the following structure:
{{"JD Match":"%", "MissingKeywords":[]}}
"""
# Provide a match percentage  and a brief justification for the score.


async def get_job_ads(session, job_role, location):
    """Fetch job adverts asynchronously from the Adzuna API."""
    url = f'https://api.adzuna.com/v1/api/jobs/{location}/search/1?app_id={APP_ID}&app_key={APP_KEY}&results_per_page=5&what={job_role}&what_or=junior%20%20entry%20level&what_exclude=senior&max_days_old=20'

    async with session.get(url) as response:
        if response.status == 200:
            return await response.json()
        else:
            return {"error": f"HTTP {response.status} - {await response.text()}"}


async def get_gemini_response(job_description, candidate_profile):
    """Generate Gemini response asynchronously"""
    prompt = input_prompt.format(candidate_profile=candidate_profile, job_description=job_description)
    model = genai.GenerativeModel('gemini-pro')
    response = await asyncio.to_thread(model.generate_content, prompt)
    return response.text


@app.route('/retrieve-job-ads', methods=['POST'])
async def retrieve_job_adverts():
    """Route that returns job adverts from job search APIs with asynchronous job matching"""
    try:
        # JSON Payload from the request body
        data = request.json
        job_role = data.get('job_role', '')
        location = data.get('location', 'us')
        candidate_profile = data.get('candidate_profile', '')

        # print(f"Job Role: {job_role}\n\n Profile: {candidate_profile}")
        if not job_role or not candidate_profile:
            return ({"error": "Invalid job role or profile supplied"}), 400

        # create asynchronous HTTP Session
        async with aiohttp.ClientSession() as session:
            # Fetch job adverts concurrently
            job_ads = await get_job_ads(session, job_role, location)

            if 'error' in job_ads:
                return jsonify(job_ads), 500

            results = []
            # process each job description concurrently
            tasks = [
                get_gemini_response(job['description'], candidate_profile)
                for job in job_ads.get('results', [])
            ]
            ats_responses = await asyncio.gather(*tasks)

            # Combine ats responses with job ads
            for job, ats_response in zip(job_ads.get('results', []),
                                         ats_responses):
                job['gemini_match'] = ats_response
                results.append(job)

            return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/')
def hello_world():
    return '<p>Hello, World!</p>'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
