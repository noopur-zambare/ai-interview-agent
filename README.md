# AI Voice Interviewer

AI Voice Interviewer is a Gradio-based voice interview application that conducts a mock interview using a candidate's resume and job description.

The app reads two PDF files:

1. Candidate Resume
2. Job Description

Once both documents are uploaded, the AI interviewer starts automatically, asks a fixed number of questions, listens to the candidate's spoken answers, and gives final interview feedback at the end.

---

## Final Feedback Format

At the end of the interview, the application generates a structured final interview feedback report. This report highlights the candidate’s key strengths, identifies the main areas where the candidate can improve, and provides a suggested practice plan to help them prepare better for future interviews. The feedback is designed to be concise, actionable, and easy to understand, so the candidate can clearly see what went well and what needs more work.

---

## Project Structure

```text
ai-interview-agent/
│
├── app.py
├── styles.css
├── interview_engine.py
├── stt.py
├── tts.py
├── .env
├── requirements.txt
└── README.md
```

---

## Tech Stack
* Gradio
* OpenAI API
* Whisper
* gTTS

---

## Installation

### 1. Open the project folder

```bash
cd ai-interview-agent
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the root folder.

```env
OPENAI_API_KEY=your_openai_api_key_here
```

---

## How to Run

Run the app using:

```bash
python app.py
```

The app will start locally, usually at:

```text
http://127.0.0.1:7860
```

Open this URL in your browser.

---

## How It Works

### Step 1: Upload Documents

Upload both files:

* Resume PDF
* Job Description PDF

Once both files are uploaded, the interview starts automatically.

### Step 2: AI Asks Questions

The AI interviewer asks one question at a time.

Questions are based mainly on the job description and supported by the candidate's resume.

### Step 3: Candidate Answers by Voice

The candidate records their answer using the microphone.

The answer is converted into text using Whisper.

### Step 4: AI Continues Interview

The AI asks the next question until the fixed number of questions is completed.

### Step 5: Final Feedback

After all questions are answered, the AI provides final interview feedback.

---

## Number of Questions

The number of interview questions is fixed inside `app.py`.

Example:

```python
agent = InterviewAgent(resume_text, jd_text, max_questions=5)
```

To change the number of questions, update `max_questions`.

Examples:

```python
max_questions=3
max_questions=7
max_questions=10
```

---

## Interview Flow

```text
Upload Resume + Job Description
        ↓
AI asks Question 1
        ↓
Candidate answers by voice
        ↓
AI asks Question 2
        ↓
Candidate answers by voice
        ↓
AI continues until fixed question limit
        ↓
Final Interview Feedback
```



