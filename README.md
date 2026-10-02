
# CareerLens

### AI-Powered Tech Career Market Explorer

CareerLens is an interactive dashboard for exploring the Indian tech job market through data analytics and GenAI.

It combines job-market analysis with an AI-powered question-answering layer so users can explore hiring demand, experience requirements, skills, work modes, and disclosed salary patterns directly from the dataset.

---
## 🚀 Live Demo

**https://careerlens-in.streamlit.app/**

Explore the interactive dashboard and ask questions about the Indian tech job market using the AI-powered **Ask CareerLens** feature.
---
## What CareerLens Does

CareerLens provides:

- Job demand analysis across technology roles
- Hiring concentration across Indian cities
- Work-mode analysis (On-site, Hybrid, Remote)
- Experience-level distribution
- Skill-domain demand
- Most frequently mentioned skills
- Fresher-friendly job analysis
- Salary analysis for jobs with disclosed salaries
- AI-generated market insights
- Interactive AI-powered Q&A through Ask CareerLens

---

## Key Features

### Interactive Dashboard

Users can filter the dataset by:

- Role Category
- Work Mode
- Experience Level

All KPIs and visualizations update according to the selected filters.

### AI Market Insights

CareerLens uses GenAI to convert dashboard statistics into concise business-oriented insights.

Each insight focuses on:

**What the data shows → Why it matters → Practical takeaway**

### Ask CareerLens

Users can ask questions about the data directly from the dashboard.

Examples:

- Which role has the highest demand?
- Which roles have more fresher-friendly opportunities?
- Which role has the highest average disclosed salary?
- Which city has the highest number of job postings?
- How does salary vary across experience levels?

The AI is restricted to the structured analysis generated from the CareerLens dataset rather than acting as a general-purpose chatbot.

---

## Dataset

The project uses an Indian technology job-market dataset containing **23,201 job postings** across multiple technology roles and locations.

The dataset includes information such as:

- Job role
- Company
- Location
- Experience
- Salary
- Required skills
- Work mode
- Company size
- Skill domain
- Posting recency

Salary analysis is based only on job postings where salary information is disclosed.

---

## Tech Stack

**Python**

- Pandas
- Plotly
- Streamlit
- python-dotenv
- Google GenAI

---

## Running the Project Locally

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd AI-Dashboard-Explainer
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your Gemini API key

Create a `.env` file:

```text
GEMINI_API_KEY=your_api_key_here
```

### 5. Run the application

```bash
streamlit run app.py
```

---

## Project Goal

The goal of CareerLens is to combine traditional data analytics with GenAI in a practical dashboard that helps users explore patterns in the technology job market and ask data-driven questions interactively.

---

## Future Improvements

Possible future additions include:

* More advanced job-market filters
* Time-based hiring trend analysis
* Skill combinations and co-occurrence analysis
* Additional geographic insights
* Improved AI explanations and visual summaries

```

