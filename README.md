# 📝 AI Meeting Notes Generator

An AI-powered application that transforms lengthy meeting notes 
into clear, structured, and actionable summaries using the 
Google Gemini API.

The application extracts important information such as key 
discussion points, action items, responsible team members, 
important decisions, and deadlines, making meeting outcomes 
easier to understand and follow.

---

## 🚀 Live Demo

🔗 **Try the MOM:** 
https://minutesofmeetings.streamlit.app/

---

## 📌 Problem Statement

Meetings often generate lengthy notes that can be difficult 
to read and organize. Important decisions, assigned tasks, 
and deadlines may get lost in large blocks of text.

This project solves that problem by using Artificial 
Intelligence to convert unstructured meeting notes into 
well-organized and readable summaries.

---

## 💡 Project Overview

The AI Meeting Notes Generator allows users to:

- Paste meeting notes directly into the application.
- Upload meeting notes through a text file.
- Analyze lengthy and unstructured meeting content.
- Generate an AI-powered structured summary.
- Identify important discussion points.
- Extract action items and their owners.
- Identify important decisions.
- Extract deadlines and upcoming events.
- Download the generated summary as a TXT file.
- Download structured meeting data as a JSON file.

The goal is to help users save time and focus on the most 
important outcomes of their meetings.

---

## ✨ Key Features

### 1. Meeting Notes Input
Users can either paste their meeting notes into the 
text area or upload a `.txt` file.

### 2. AI-Powered Summarization
The Google Gemini API analyzes the meeting content and 
generates a concise and meaningful summary.

### 3. Key Discussion Points
The application identifies the main topics and issues 
discussed during the meeting.

### 4. Action Items
Tasks are extracted along with:

- Task description
- Responsible person
- Deadline, if available

### 5. Important Decisions
The application highlights decisions made during 
the meeting.

### 6. Deadline Extraction
Important dates, upcoming meetings, and task deadlines 
are presented in an organized format.

### 7. Downloadable Reports
Users can download the generated results in:

- Readable TXT format
- Structured JSON format

### 8. User-Friendly Interface
The application provides a clean and simple interface 
designed for students, teams, and professionals.

---

## 🛠️ Technology Stack

| Technology | Purpose |
|------------|---------|
| Python | Application development |
| Streamlit | User interface |
| Google Gemini API | AI-powered analysis |
| python-dotenv | Environment variable management |
| JSON | Structured output |
| TXT | Readable meeting summary |
| Git & GitHub | Version control |

---

## 🏗️ Application Workflow

1. The user enters or uploads meeting notes.
2. The application validates the input.
3. The notes are sent to the Google Gemini API.
4. Gemini analyzes the meeting content.
5. Important information is extracted.
6. The results are organized into structured sections.
7. The summary is displayed on the application.
8. The user can download the results as TXT or JSON.

### Workflow Diagram

### 📌 How it will look

                 👤 User Input
                       │
                       ▼
             📝 Meeting Notes / TXT File
                       │
                       ▼
             ⚙️ Streamlit Application
                       │
                       ▼
                🤖 Google Gemini API
                       │
                       ▼
                🧠 AI-Powered Analysis
                       │
                       ▼
             📋 Structured Meeting Summary
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼            ▼
     💬 Discussion   ✅ Action    🔵 Decisions  ⏰ Deadlines
       Points        Items
          │            │            │            │
          └────────────┴────────────┴────────────┘
                       │
                       ▼
                📥 TXT / JSON Files

---

## 📂 Project Structure

```text
AI-Meeting-Notes-Generator/
│
├── app.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
