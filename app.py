import os
import json
import streamlit as st
from dotenv import load_dotenv
from google import genai


load_dotenv()

# First try .env for local development
API_KEY = os.getenv("GEMINI_API_KEY")

# If running on Streamlit Cloud, use Streamlit Secrets
if not API_KEY:
    try:
        API_KEY = st.secrets["GEMINI_API_KEY"]
    except Exception:
        API_KEY = None


st.set_page_config(
    page_title="AI Meeting Notes Generator",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown(
    """
    <style>

    /* Main page */
    .main {
        padding-top: 1rem;
    }

    /* Header */
    .main-title {
        text-align: center;
        font-size: 44px;
        font-weight: 700;
        margin-bottom: 8px;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #666666;
        margin-bottom: 35px;
    }

    /* Section headings */
    .section-heading {
        font-size: 25px;
        font-weight: 650;
        margin-top: 25px;
        margin-bottom: 15px;
    }

    /* Summary card */
    .summary-card {
        padding: 22px;
        border-radius: 14px;
        background-color: #eef6ff;
        border-left: 5px solid #4c8bf5;
        margin-bottom: 20px;
        line-height: 1.7;
    }

    /* Action cards */
    .action-card {
        padding: 18px;
        border-radius: 12px;
        border: 1px solid #dddddd;
        background-color: #fafafa;
        margin-bottom: 12px;
    }

    /* Decision cards */
    .decision-card {
        padding: 14px 18px;
        border-radius: 10px;
        background-color: #f5f8ff;
        border-left: 4px solid #5277d9;
        margin-bottom: 10px;
    }

    /* Deadline cards */
    .deadline-card {
        padding: 14px 18px;
        border-radius: 10px;
        background-color: #fff9ed;
        border-left: 4px solid #f0a500;
        margin-bottom: 10px;
    }

    /* Small info text */
    .helper-text {
        color: #777777;
        font-size: 14px;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #888888;
        margin-top: 45px;
        padding: 20px;
        font-size: 14px;
    }

    </style>
    """,
    unsafe_allow_html=True
)




if not API_KEY:

    st.error(
        "Gemini API key was not found. "
        "Please configure GEMINI_API_KEY in your .env file "
        "or Streamlit Secrets."
    )

    st.stop()

try:

    client = genai.Client(api_key=API_KEY)

except Exception as e:

    st.error(f"Unable to initialize Gemini: {e}")

    st.stop()

st.markdown(
    '<div class="main-title">📝 AI Meeting Notes Generator</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="subtitle">
    Transform lengthy meeting notes into clear, structured and actionable insights.
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-heading">📄 Meeting Notes</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="helper-text">Upload a text file or paste your meeting notes below.</div>',
    unsafe_allow_html=True
)

# File upload
uploaded_file = st.file_uploader(
    "Upload meeting notes",
    type=["txt"],
    label_visibility="collapsed"
)

# Read uploaded file
uploaded_notes = ""

if uploaded_file:

    try:

        uploaded_notes = uploaded_file.read().decode("utf-8")

        st.success(
            f"Loaded meeting notes from: {uploaded_file.name}"
        )

    except Exception:

        st.error(
            "Unable to read the uploaded file. "
            "Please upload a valid UTF-8 text file."
        )


# Text input
notes = st.text_area(
    "Paste meeting notes",
    height=280,
    placeholder="""
Example:

The product team met to discuss the Q4 launch.

Rahul will prepare the product demo by September 5.
Priya will finalize the marketing campaign by September 8.

The team decided to launch the product on September 15.

The approved marketing budget is ₹50,000.

The next project review meeting will be held on September 10.
""",
    label_visibility="collapsed"
)


if uploaded_notes.strip():
    final_notes = uploaded_notes
else:
    final_notes = notes



col1, col2 = st.columns(2)

with col1:

    generate_button = st.button(
        "✨ Generate Meeting Summary",
        use_container_width=True
    )

with col2:

    clear_button = st.button(
        "🗑️ Clear",
        use_container_width=True
    )


if clear_button:

    st.rerun()




if generate_button:

    # Validate input
    if not final_notes.strip():

        st.warning(
            "Please paste meeting notes or upload a .txt file first."
        )

        st.stop()


    prompt = f"""
You are an expert AI meeting assistant.

Your task is to analyze the meeting notes provided below and
convert them into a concise, structured and actionable meeting summary.

MEETING NOTES
-------------
{final_notes}

Return ONLY valid JSON.

Use exactly this structure:

{{
    "summary": "A concise summary of the meeting.",

    "key_discussion_points": [
        "Important discussion point 1",
        "Important discussion point 2",
        "Important discussion point 3"
    ],

    "action_items": [
        {{
            "task": "Specific action or task",
            "owner": "Person responsible or Unknown",
            "deadline": "Deadline or Not specified"
        }}
    ],

    "important_decisions": [
        "Important decision 1",
        "Important decision 2"
    ],

    "deadlines": [
        {{
            "task": "Task, event or milestone",
            "date": "Date or Not specified"
        }}
    ]
}}

IMPORTANT RULES:

1. Do not invent information.
2. Only extract information that is present in the meeting notes.
3. If an owner is not mentioned, use "Unknown".
4. If a deadline is not mentioned, use "Not specified".
5. Identify meaningful decisions separately from discussion points.
6. Identify all explicit deadlines and important dates.
7. Keep the summary concise and readable.
8. Do not add markdown formatting.
9. Return valid JSON only.
"""


    with st.spinner("🤖 Gemini is analyzing the meeting notes..."):

        try:

            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )

            result_text = response.text.strip()


            # Gemini may sometimes return JSON inside
            # markdown code fences.

            if result_text.startswith("```json"):

                result_text = result_text[
                    len("```json"):
                ].strip()

            elif result_text.startswith("```"):

                result_text = result_text[
                    len("```"):
                ].strip()


            if result_text.endswith("```"):

                result_text = result_text[
                    :-len("```")
                ].strip()

            result = json.loads(result_text)

            st.success(
                "Meeting notes successfully analyzed!"
            )



            st.markdown(
                '<div class="section-heading">📌 Meeting Summary</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                f"""
                <div class="summary-card">
                {result.get("summary", "No summary available.")}
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                '<div class="section-heading">💬 Key Discussion Points</div>',
                unsafe_allow_html=True
            )

            discussion_points = result.get(
                "key_discussion_points",
                []
            )

            if discussion_points:

                for point in discussion_points:

                    st.markdown(
                        f"• {point}"
                    )

            else:

                st.info(
                    "No major discussion points identified."
                )


            st.markdown(
                '<div class="section-heading">✅ Action Items</div>',
                unsafe_allow_html=True
            )

            action_items = result.get(
                "action_items",
                []
            )

            if action_items:

                # Table header
                header_col1, header_col2, header_col3 = st.columns(
                    [2.5, 1, 1]
                )

                with header_col1:
                    st.markdown("**📋 Task**")

                with header_col2:
                    st.markdown("**👤 Owner**")

                with header_col3:
                    st.markdown("**📅 Deadline**")


                st.divider()


                # Action rows
                for item in action_items:

                    col1, col2, col3 = st.columns(
                        [2.5, 1, 1]
                    )

                    with col1:
                        st.write(
                            item.get(
                                "task",
                                "Not specified"
                            )
                        )

                    with col2:
                        st.write(
                            item.get(
                                "owner",
                                "Unknown"
                            )
                        )

                    with col3:
                        st.write(
                            item.get(
                                "deadline",
                                "Not specified"
                            )
                        )

                    st.divider()

            else:

                st.info(
                    "No action items identified."
                )


            st.markdown(
                '<div class="section-heading">🔵 Important Decisions</div>',
                unsafe_allow_html=True
            )

            decisions = result.get(
                "important_decisions",
                []
            )

            if decisions:

                for decision in decisions:

                    st.markdown(
                        f"""
                        <div class="decision-card">
                        • {decision}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            else:

                st.info(
                    "No important decisions identified."
                )


            st.markdown(
                '<div class="section-heading">⏰ Deadlines</div>',
                unsafe_allow_html=True
            )

            deadlines = result.get(
                "deadlines",
                []
            )

            if deadlines:

                for deadline in deadlines:

                    date = deadline.get(
                        "date",
                        "Not specified"
                    )

                    task = deadline.get(
                        "task",
                        "Not specified"
                    )

                    st.markdown(
                        f"""
                        <div class="deadline-card">
                        <strong>📅 {date}</strong>
                        &nbsp; — &nbsp;
                        {task}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            else:

                st.info(
                    "No deadlines identified."
                )

            summary_text = f"""
AI MEETING SUMMARY
==================

MEETING SUMMARY
---------------
{result.get("summary", "No summary available.")}


KEY DISCUSSION POINTS
---------------------

"""

            for point in discussion_points:

                summary_text += f"- {point}\n"


            summary_text += """

ACTION ITEMS
------------

"""


            for item in action_items:

                summary_text += (
                    f"Task: {item.get('task', 'Not specified')}\n"
                    f"Owner: {item.get('owner', 'Unknown')}\n"
                    f"Deadline: {item.get('deadline', 'Not specified')}\n\n"
                )


            summary_text += """

IMPORTANT DECISIONS
-------------------

"""


            for decision in decisions:

                summary_text += f"- {decision}\n"


            summary_text += """

DEADLINES
---------

"""


            for deadline in deadlines:

                summary_text += (
                    f"{deadline.get('date', 'Not specified')} "
                    f"— {deadline.get('task', 'Not specified')}\n"
                )


            st.markdown(
                '<div class="section-heading">📥 Download Summary</div>',
                unsafe_allow_html=True
            )

            download_col1, download_col2 = st.columns(2)

            with download_col1:

                st.download_button(
                    label="📄 Download Readable TXT",
                    data=summary_text,
                    file_name="meeting_summary.txt",
                    mime="text/plain",
                    use_container_width=True
                )


            with download_col2:

                st.download_button(
                    label="📦 Download Structured JSON",
                    data=json.dumps(
                        result,
                        indent=4,
                        ensure_ascii=False
                    ),
                    file_name="meeting_summary.json",
                    mime="application/json",
                    use_container_width=True
                )
        except json.JSONDecodeError:

            st.error(
                "Gemini returned an unexpected response format. "
                "Please try generating the summary again."
            )


        except Exception as e:

            error_message = str(e)

            st.error(
                f"Something went wrong: {error_message}"
            )


st.markdown(
    """
    <div class="footer">
        📝 AI Meeting Notes Generator &nbsp;•&nbsp;
        Powered by Google Gemini & Streamlit
    </div>
    """,
    unsafe_allow_html=True
)