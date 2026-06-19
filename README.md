# AI Voice Interviewer

AI Voice Interviewer is a Gradio-based voice interview application that conducts a mock interview using a candidate's resume and job description.

The app reads two PDF files:

1. Candidate Resume
2. Job Description

Once both documents are uploaded, the AI interviewer starts automatically, asks a fixed number of questions, listens to the candidate's spoken answers, and gives final interview feedback at the end.

## Interview Flow
<div style="text-align: center;">
  <img width="550" height="250" alt="interview-flow"
       src="https://github.com/user-attachments/assets/913b2748-bb99-4909-b775-88f95748572b" />
</div>

## How to run

#### 1. Open the project folder

```bash
cd ai-interview-agent
```

#### 2. Create and activate virtual environment

```bash
python -m venv venv
```

```bash
source venv/bin/activate
```

#### 3. Install dependencies

```bash
pip install -r requirements.txt
```

#### 4. Environment variables

Create a `.env` file in the root folder.

```env
OPENAI_API_KEY=your_openai_api_key_here
```

#### 5. To run the app

```bash
python app.py
```

The app will start locally, usually at:

```text
http://127.0.0.1:7860
```

## How It Works

#### Step 1: Upload Documents

Upload both files:

* Resume PDF
* Job Description PDF

Once both files are uploaded, the interview starts automatically.

#### Step 2: Chatbot Asks Questions

The AI interviewer asks one question at a time.

Questions are based mainly on the job description and supported by the candidate's resume.

#### Step 3: Candidate Answers by Voice

The candidate records their answer using the microphone.

The answer is converted into text using Whisper.

#### Step 4: Chatbot Continues Interview

Chatbot asks the next question until the fixed number of questions is completed.

#### Step 5: Final Feedback

After all questions are answered, the Chatbot provides final interview feedback.


## Final Feedback Format

At the end of the interview, the application generates a structured final interview feedback report. This report highlights the candidate’s key strengths, identifies the main areas where the candidate can improve, and provides a suggested practice plan to help them prepare better for future interviews. The feedback is designed to be concise, actionable, and easy to understand, so the candidate can clearly see what went well and what needs more work.


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

## Tech Stack
* Gradio
* OpenAI API
* Whisper
* gTTS
