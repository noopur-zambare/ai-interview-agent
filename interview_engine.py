from openai import OpenAI
from dotenv import load_dotenv
import os


load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class InterviewAgent:
    def __init__(self, resume_text, jd_text, max_questions=5):
        self.max_questions = max_questions
        self.questions_asked = 0
        self.finished = False

        self.messages = [
            {
                "role": "system",
                "content": f"""
You are a FAANG-level AI interviewer.

You are conducting a realistic mock interview.

Rules:
- Ask ONE question at a time.
- Ask exactly {max_questions} questions in total.
- Base questions mainly on the JOB DESCRIPTION.
- Use the RESUME for relevant follow-up and deep-dive questions.
- Mix:
  1. Technical questions
  2. Resume-based questions
  3. Behavioral questions
- Do NOT give feedback after every answer.
- After each answer, simply ask the next question.
- Once all {max_questions} questions are answered, give final feedback only.
- Do not ask any more questions after the final feedback.

Final feedback format must be exactly:

Final Interview Feedback:

Strengths:
- <strength 1>
- <strength 2>
- <strength 3>

Areas to Improve:
- <area 1>
- <area 2>
- <area 3>

Suggested Practice Plan:
- <practice point 1>
- <practice point 2>
- <practice point 3>

RESUME:
{resume_text}

JOB DESCRIPTION:
{jd_text}
"""
            }
        ]

    def ask(self, user_answer=None):
        if self.finished:
            return "The interview is already complete. Please upload new documents or restart the app to begin again."

        # First question
        if user_answer is None:
            self.questions_asked += 1

            prompt = f"""
Start the interview.

Ask question {self.questions_asked} of {self.max_questions}.

Ask only one strong opening question based on the job description.
Do not give feedback.
"""

            self.messages.append(
                {
                    "role": "user",
                    "content": prompt
                }
            )

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=self.messages,
                temperature=0.7
            )

            reply = response.choices[0].message.content

            self.messages.append(
                {
                    "role": "assistant",
                    "content": reply
                }
            )

            return reply

        # Save candidate answer
        self.messages.append(
            {
                "role": "user",
                "content": user_answer
            }
        )

        # If all questions are answered, generate final feedback
        if self.questions_asked >= self.max_questions:
            final_prompt = f"""
The candidate has now answered all {self.max_questions} questions.

The interview is complete.

Do not ask another question.

Give final feedback only in this exact format:

Final Interview Feedback:

Strengths:
- <strength 1>
- <strength 2>
- <strength 3>

Areas to Improve:
- <area 1>
- <area 2>
- <area 3>

Suggested Practice Plan:
- <practice point 1>
- <practice point 2>
- <practice point 3>
"""

            self.messages.append(
                {
                    "role": "user",
                    "content": final_prompt
                }
            )

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=self.messages,
                temperature=0.7
            )

            reply = response.choices[0].message.content

            self.messages.append(
                {
                    "role": "assistant",
                    "content": reply
                }
            )

            self.finished = True
            return reply

        # Ask next question
        self.questions_asked += 1

        prompt = f"""
Ask question {self.questions_asked} of {self.max_questions}.

Ask only one question.
Do not give feedback yet.
Make the question relevant to the job description and resume.
"""

        self.messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=self.messages,
            temperature=0.7
        )

        reply = response.choices[0].message.content

        self.messages.append(
            {
                "role": "assistant",
                "content": reply
            }
        )

        return reply

    def is_finished(self):
        return self.finished