import gradio as gr
from pypdf import PdfReader
from pathlib import Path

from stt import transcribe
from tts import speak
from interview_engine import InterviewAgent


CSS_PATH = Path(__file__).with_name("styles.css")

if CSS_PATH.exists():
    custom_css = CSS_PATH.read_text(encoding="utf-8")
else:
    custom_css = ""


agent = None


def get_file_path(file):
    if file is None:
        return None

    if isinstance(file, str):
        return file

    if hasattr(file, "name"):
        return file.name

    return None


def read_file(file_path):
    reader = PdfReader(file_path)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text.strip()


def handle_resume_upload(file):
    if file is None:
        return None, "No resume uploaded"

    file_path = get_file_path(file)
    filename = Path(file_path).name

    return file, f"Resume uploaded: {filename}"


def handle_jd_upload(file):
    if file is None:
        return None, "No job description uploaded"

    file_path = get_file_path(file)
    filename = Path(file_path).name

    return file, f"Job description uploaded: {filename}"


def start(resume_file, jd_file):
    global agent

    resume_path = get_file_path(resume_file)
    jd_path = get_file_path(jd_file)

    if resume_path is None or jd_path is None:
        history = [
            {
                "role": "assistant",
                "content": "Please upload both the resume and job description first."
            }
        ]
        return history, None

    try:
        resume_text = read_file(resume_path)
        jd_text = read_file(jd_path)

        if not resume_text:
            history = [
                {
                    "role": "assistant",
                    "content": "I could not read text from the resume PDF. Please upload a text-based PDF."
                }
            ]
            return history, None

        if not jd_text:
            history = [
                {
                    "role": "assistant",
                    "content": "I could not read text from the job description PDF. Please upload a text-based PDF."
                }
            ]
            return history, None

        agent = InterviewAgent(
            resume_text,
            jd_text,
            max_questions=5
        )

        question = agent.ask()
        audio_file = speak(question)

        history = [
            {
                "role": "assistant",
                "content": question
            }
        ]

        return history, audio_file

    except Exception as e:
        history = [
            {
                "role": "assistant",
                "content": f"Error while starting interview: {str(e)}"
            }
        ]
        return history, None


def try_auto_start(resume_file, jd_file):
    resume_path = get_file_path(resume_file)
    jd_path = get_file_path(jd_file)

    if resume_path is None or jd_path is None:
        return [], None

    return start(resume_file, jd_file)


def interview(audio, history):
    global agent

    if history is None:
        history = []

    if audio is None:
        return history, None, None

    if agent is None:
        history.append(
            {
                "role": "assistant",
                "content": "Please upload both PDFs first. The interview will start automatically."
            }
        )
        return history, None, None

    try:
        user_text = transcribe(audio)

        if not user_text:
            history.append(
                {
                    "role": "assistant",
                    "content": "I could not hear your answer clearly. Please try again."
                }
            )
            return history, None, None

        reply = agent.ask(user_text)

        if agent.is_finished():
            reply = reply + "\n\nInterview complete."

        audio_file = speak(reply)

        history.append(
            {
                "role": "user",
                "content": user_text
            }
        )

        history.append(
            {
                "role": "assistant",
                "content": reply
            }
        )

        return history, audio_file, None

    except Exception as e:
        history.append(
            {
                "role": "assistant",
                "content": f"Error during interview: {str(e)}"
            }
        )
        return history, None, None


with gr.Blocks(
    theme=gr.themes.Monochrome(),
    css=custom_css
) as demo:

    resume_state = gr.State(None)
    jd_state = gr.State(None)

    with gr.Column(elem_id="main-container"):

        gr.Markdown(
            """
            # AI Voice Interviewer

            Upload a resume and job description. The interview starts automatically once both files are uploaded.
            """,
            elem_classes="app-header"
        )

        with gr.Row(elem_classes="upload-row"):

            with gr.Column(scale=1):
                gr.Markdown("### Resume", elem_classes="section-label")

                resume_button = gr.UploadButton(
                    "Upload Resume PDF",
                    file_types=[".pdf"],
                    file_count="single",
                    elem_classes="upload-button"
                )

                resume_drop = gr.File(
                    label="Drag and drop resume PDF",
                    file_types=[".pdf"],
                    elem_classes="drop-zone"
                )

                resume_status = gr.Markdown(
                    "No resume uploaded",
                    elem_classes="upload-status"
                )

            with gr.Column(scale=1):
                gr.Markdown("### Job Description", elem_classes="section-label")

                jd_button = gr.UploadButton(
                    "Upload Job Description PDF",
                    file_types=[".pdf"],
                    file_count="single",
                    elem_classes="upload-button"
                )

                jd_drop = gr.File(
                    label="Drag and drop job description PDF",
                    file_types=[".pdf"],
                    elem_classes="drop-zone"
                )

                jd_status = gr.Markdown(
                    "No job description uploaded",
                    elem_classes="upload-status"
                )

        chatbot = gr.Chatbot(
            label="Interview Conversation",
            elem_id="chatbot"
        )

        with gr.Row(elem_classes="audio-row"):

            audio_input = gr.Audio(
                sources=["microphone"],
                type="filepath",
                label="Your Answer"
            )

            audio_output = gr.Audio(
                label="Interviewer Voice",
                autoplay=True,
                interactive=False
            )

        gr.Markdown(
            "The interviewer will speak automatically after both files are uploaded.",
            elem_classes="footer-note"
        )

        resume_button.upload(
            fn=handle_resume_upload,
            inputs=resume_button,
            outputs=[resume_state, resume_status]
        ).then(
            fn=try_auto_start,
            inputs=[resume_state, jd_state],
            outputs=[chatbot, audio_output]
        )

        resume_drop.change(
            fn=handle_resume_upload,
            inputs=resume_drop,
            outputs=[resume_state, resume_status]
        ).then(
            fn=try_auto_start,
            inputs=[resume_state, jd_state],
            outputs=[chatbot, audio_output]
        )

        jd_button.upload(
            fn=handle_jd_upload,
            inputs=jd_button,
            outputs=[jd_state, jd_status]
        ).then(
            fn=try_auto_start,
            inputs=[resume_state, jd_state],
            outputs=[chatbot, audio_output]
        )

        jd_drop.change(
            fn=handle_jd_upload,
            inputs=jd_drop,
            outputs=[jd_state, jd_status]
        ).then(
            fn=try_auto_start,
            inputs=[resume_state, jd_state],
            outputs=[chatbot, audio_output]
        )

        audio_input.stop_recording(
            fn=interview,
            inputs=[audio_input, chatbot],
            outputs=[chatbot, audio_output, audio_input]
        )


demo.launch()