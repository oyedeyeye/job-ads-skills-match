# Job Ads Retriever & Skills Matching Application

## Overview
This application provides an ATS (Application Tracking System) that evaluates candidates' profiles against job descriptions using Google's Gemini AI. It integrates with the Adzuna API to retrieve job advertisements and assesses candidates’ fit asynchronously.

---

## Key Features
- **Job Ads Retrieval**: Fetches job advertisements from the Adzuna API.
- **Profile Evaluation**: Uses Google Gemini AI to evaluate candidates' profiles against job descriptions.
- **Asynchronous Processing**: Employs `aiohttp` and `asyncio` for concurrent API requests and job matching.

---

## Prerequisites
1. **Environment Variables**:
   - `APP_ID`: Adzuna API ID
   - `APP_KEY`: Adzuna API Key
   - `GOOGLE_API_KEY`: API key for Google Generative AI (Gemini)
2. **Dependencies**: Install using `pip install -r requirements.txt`
    ```requirements.txt
    Flask
    flask[async]
    python-dotenv
    google.generativeai
    aiohttp
    asyncio
    ```

---

## API Endpoints

### 1. **Root**
   - **URL**: `/`
   - **Method**: GET
   - **Description**: A basic health check endpoint.
   - **Response**:
     ```html
     <p>Hello, World!</p>
     ```

### 2. **Retrieve Job Ads**
   - **URL**: `/retrieve-job-ads`
   - **Method**: POST
   - **Description**: Fetches job ads and evaluates candidate profiles asynchronously.
   - **Request Payload**:
     ```json
     {
       "job_role": "Software Engineer",
       "location": "us",
       "candidate_profile": "Experienced Python developer with 3 years of..."
     }
     ```
   - **Response**: List of job advertisements with evaluation results.
     ```json
     [
       {
         "title": "Junior Python Developer",
         "description": "...",
         "location": "...",
         "gemini_match": "{\"JD Match\": \"85%\", \"MissingKeywords\": [\"Django\", \"REST APIs\"]}"
       },
       ...
     ]
     ```
   - **Error Responses**:
     - `400`: Invalid job role or profile supplied.
     - `500`: Internal server error or third-party API issues.

---

## Code Walkthrough

### Environment Configuration
- `.env` file for storing sensitive keys:
  ```env
  APP_ID=your_adzuna_app_id
  APP_KEY=your_adzuna_app_key
  GOOGLE_API_KEY=your_google_api_key
  ```

### Asynchronous Functions
- `get_job_ads(session, job_role, location)`: Fetches job ads from Adzuna API.
- `get_gemini_response(job_description, candidate_profile)`: Sends prompts to Gemini AI for profile evaluation.

### Routes
- **`/retrieve-job-ads`**:
  - Validates inputs.
  - Retrieves job ads using `aiohttp`.
  - Sends job descriptions and candidate profiles to Gemini for evaluation.
- **`/`**: Basic health check endpoint.

### AI Prompt
The application uses a custom prompt to guide Gemini in evaluating profiles. This ensures consistent and structured AI responses.

---

## Running the Application
1. Install dependencies:  
   ```bash
   pip install flask python-dotenv aiohttp google-generativeai
   ```
2. Add environment variables in a `.env` file.
3. Start the application:
   ```bash
   python app.py
   ```
4. Access the application at `http://localhost:8080`.

---

## Future Improvements
- Enhance error handling for API timeouts and invalid responses.
- Add unit tests for API endpoints and async functions.
- Extend support for other job search APIs.

---

Let me know if you'd like to refine this further!