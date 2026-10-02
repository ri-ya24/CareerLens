
import os
import pandas as pd
import plotly.express as px
import streamlit as st
from dotenv import load_dotenv
from google import genai

# Page configuration

st.set_page_config(
    page_title="CareerLens",
    page_icon="📊",
    layout="wide"
)

# Load environment variables

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)
st.markdown(
    """
    <style>

    /* Main page spacing */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }

    /* Main title */
    h1 {
        font-size: 2.8rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }

    /* Section headings */
    h2, h3 {
        font-weight: 600;
    }

    /* KPI cards */
    [data-testid="stMetric"] {
        padding: 1.1rem;
        border: 1px solid rgba(128, 128, 128, 0.2);
        border-radius: 12px;
        background: rgba(128, 128, 128, 0.03);
    }

    [data-testid="stMetricLabel"] {
        font-size: 0.9rem;
    }

    [data-testid="stMetricValue"] {
        font-size: 1.7rem;
        font-weight: 650;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        border-right: 1px solid rgba(128, 128, 128, 0.15);
    }

    /* Captions */
    .stCaption {
        font-size: 0.9rem;
    }

    /* Text input */
    div[data-baseweb="input"] {
        border-radius: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# Load data

@st.cache_data
def load_data():
    return pd.read_csv("archive/indian_tech_jobs_2026.csv")


df = load_data()


# Header

st.title("CareerLens")
st.subheader("AI-Powered Tech Career Market Explorer")

st.write(
    "Explore hiring demand, career opportunities, work modes, "
    "experience levels, and skill domains across the Indian tech job market."
)

st.divider()


# Sidebar filters

st.sidebar.header("Filters")

role_options = sorted(df["role_category"].unique())
work_mode_options = sorted(df["work_mode"].unique())
experience_options = sorted(df["experience_tier"].unique())

selected_roles = st.sidebar.multiselect(
    "Role Category",
    options=role_options,
    default=role_options
)

selected_work_modes = st.sidebar.multiselect(
    "Work Mode",
    options=work_mode_options,
    default=work_mode_options
)

selected_experience = st.sidebar.multiselect(
    "Experience Level",
    options=experience_options,
    default=experience_options
)


# Apply filters

filtered_df = df[
    df["role_category"].isin(selected_roles)
    & df["work_mode"].isin(selected_work_modes)
    & df["experience_tier"].isin(selected_experience)
].copy()

# Key metrics

total_jobs = len(filtered_df)

fresher_jobs = int(
    filtered_df["is_fresher_friendly"].sum()
)

remote_jobs = int(
    filtered_df["work_mode"].eq("Remote").sum()
)

salary_disclosed_jobs = int(
    filtered_df["salary_disclosed"].sum()
)

salary_df = filtered_df[
    filtered_df["salary_disclosed"]
    & filtered_df["salary_midpoint_lpa"].notna()
]

if not salary_df.empty:
    average_salary = salary_df["salary_midpoint_lpa"].mean()
else:
    average_salary = 0


# KPI section

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Total Jobs",
    f"{total_jobs:,}"
)

col2.metric(
    "Fresher-Friendly Jobs",
    f"{fresher_jobs:,}"
)

col3.metric(
    "Remote Jobs",
    f"{remote_jobs:,}"
)

col4.metric(
    "Salary Disclosed",
    f"{salary_disclosed_jobs:,}"
)

col5.metric(
    "Average Salary",
    f"{average_salary:.1f} LPA"
)

st.divider()

# Job demand by role

st.subheader("Job Demand by Role")

role_counts = (
    filtered_df["role_category"]
    .value_counts()
    .reset_index()
)

role_counts.columns = ["Role", "Jobs"]

role_chart = px.bar(
    role_counts,
    x="Role",
    y="Jobs",
    text="Jobs",
    title="Job Postings by Role"
)

role_chart.update_layout(
    xaxis_title="Role",
    yaxis_title="Job Postings",
    showlegend=False
)

st.plotly_chart(
    role_chart,
    use_container_width=True
)


# City and work mode

col1, col2 = st.columns(2)

with col1:

    st.subheader("Top Hiring Cities")

    city_counts = (
        filtered_df["primary_city"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    city_counts.columns = ["City", "Jobs"]

    city_chart = px.bar(
        city_counts,
        x="Jobs",
        y="City",
        orientation="h",
        text="Jobs",
        title="Top 10 Cities by Job Openings"
    )

    city_chart.update_layout(
        yaxis={"categoryorder": "total ascending"},
        xaxis_title="Job Postings",
        yaxis_title="City"
    )

    st.plotly_chart(
        city_chart,
        use_container_width=True
    )


with col2:

    st.subheader("Work Mode Distribution")

    work_mode_counts = (
        filtered_df["work_mode"]
        .value_counts()
        .reset_index()
    )

    work_mode_counts.columns = ["Work Mode", "Jobs"]

    work_mode_chart = px.pie(
        work_mode_counts,
        names="Work Mode",
        values="Jobs",
        hole=0.45,
        title="On-site, Hybrid, and Remote Jobs"
    )

    st.plotly_chart(
        work_mode_chart,
        use_container_width=True
    )


# Experience and skill domain

col1, col2 = st.columns(2)

with col1:

    st.subheader("Experience Level Distribution")

    experience_counts = (
        filtered_df["experience_tier"]
        .value_counts()
        .reset_index()
    )

    experience_counts.columns = ["Experience Level", "Jobs"]

    experience_chart = px.bar(
        experience_counts,
        x="Experience Level",
        y="Jobs",
        text="Jobs",
        title="Job Postings by Experience Level"
    )

    experience_chart.update_layout(
        xaxis_title="Experience Level",
        yaxis_title="Job Postings",
        showlegend=False
    )

    st.plotly_chart(
        experience_chart,
        use_container_width=True
    )


with col2:

    st.subheader("Skill Domain Demand")

    skill_domain_counts = (
        filtered_df["skill_domain"]
        .value_counts()
        .reset_index()
    )

    skill_domain_counts.columns = ["Skill Domain", "Jobs"]

    skill_domain_chart = px.bar(
        skill_domain_counts,
        x="Skill Domain",
        y="Jobs",
        text="Jobs",
        title="Job Demand Across Skill Domains"
    )

    skill_domain_chart.update_layout(
        xaxis_title="Skill Domain",
        yaxis_title="Job Postings",
        showlegend=False
    )

    st.plotly_chart(
        skill_domain_chart,
        use_container_width=True
    )


# Extract individual skills

skills_series = (
    filtered_df["skills_required"]
    .dropna()
    .str.split(",")
    .explode()
    .str.strip()
    .str.lower()
)

skills_series = skills_series[
    (skills_series != "") &
    (skills_series != "not available")
]

top_skills = skills_series.value_counts().head(15)


# Top skills

st.subheader("Most In-Demand Skills")

top_skills_df = top_skills.reset_index()

top_skills_df.columns = ["Skill", "Jobs"]

skills_chart = px.bar(
    top_skills_df,
    x="Jobs",
    y="Skill",
    orientation="h",
    text="Jobs",
    title="Top 15 Skills Mentioned in Job Postings"
)

skills_chart.update_layout(
    yaxis={"categoryorder": "total ascending"},
    xaxis_title="Job Postings",
    yaxis_title="Skill"
)

st.plotly_chart(
    skills_chart,
    use_container_width=True
)
# AI market insights

st.divider()
st.subheader("AI Market Insights")

top_role = filtered_df["role_category"].value_counts().idxmax()
top_city = filtered_df["primary_city"].value_counts().idxmax()
top_skill_domain = filtered_df["skill_domain"].value_counts().idxmax()
top_work_mode = filtered_df["work_mode"].value_counts().idxmax()

fresher_rate = (
    filtered_df["is_fresher_friendly"].mean() * 100
)

salary_disclosure_rate = (
    filtered_df["salary_disclosed"].mean() * 100
)

senior_rate = (
    filtered_df["is_senior"].mean() * 100
)

average_skills = (
    filtered_df["skills_count"].mean()
)

average_experience = (
    filtered_df["experience_min_yrs"].mean()
)

insight_data = f"""
You are a Business Analyst analyzing an Indian technology job-market dataset.

CareerLens dashboard statistics:

Total jobs: {len(filtered_df):,}

Most common role:
{top_role}

Top hiring city:
{top_city}

Most common skill domain:
{top_skill_domain}

Most common work mode:
{top_work_mode}

Fresher-friendly jobs:
{fresher_jobs:,}

Fresher-friendly rate:
{fresher_rate:.1f}%

Senior-job rate:
{senior_rate:.1f}%

Jobs with salary disclosed:
{salary_disclosed_jobs:,}

Salary disclosure rate:
{salary_disclosure_rate:.1f}%

Average skills mentioned per job:
{average_skills:.1f}

Average minimum experience required:
{average_experience:.1f} years

Top roles by job count:
{role_counts.head(6).to_string()}

Top cities by job count:
{city_counts.head(10).to_string()}

Skill-domain demand:
{skill_domain_counts.to_string()}

Work-mode distribution:
{work_mode_counts.to_string()}

Experience-level distribution:
{experience_counts.to_string()}
"""


insight_prompt = f"""
You are the Business Analyst for CareerLens.

CareerLens is an Indian technology job-market analytics dashboard.

Your job is to convert the provided statistics into useful,
decision-oriented market insights.

DATA:
{insight_data}

Generate exactly 3 insights.

For every insight use this format:

**Insight:** What the data shows.

**Why it matters:** What this pattern means for candidates,
recruiters, or hiring teams.

**Takeaway:** A practical consideration based only on the data.

Rules:

- Use ONLY the provided CareerLens data.
- Do not use outside knowledge.
- Do not invent statistics.
- Do not invent causes.
- Do not claim correlation is causation.
- Do not say a pattern proves why companies behave a certain way.
- Do not simply repeat a KPI.
- Prefer comparisons between roles, cities, experience levels,
  work modes, skills, and skill domains.
- Salary conclusions must acknowledge that salary disclosure
  is limited in the dataset.
- Keep each insight concise and easy to understand.
- Focus on hiring demand, candidate opportunities,
  workforce requirements, and market patterns.
- Recommendations must be framed as considerations,
  not guaranteed outcomes.
"""

try:

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=insight_prompt
    )

    st.write(response.text)

except Exception as e:

    st.error(
        f"Unable to generate AI insights: {e}"
    )

# Build analytics context

role_counts = filtered_df["role_category"].value_counts()

city_counts = (
    filtered_df["primary_city"]
    .value_counts()
    .head(10)
)

work_mode_counts = filtered_df["work_mode"].value_counts()

experience_counts = filtered_df["experience_tier"].value_counts()

skill_domain_counts = filtered_df["skill_domain"].value_counts()


# Fresher analysis

role_fresher_rate = (
    filtered_df.groupby("role_category")["is_fresher_friendly"]
    .mean()
    .mul(100)
    .sort_values(ascending=False)
)

fresher_by_role = (
    filtered_df.groupby("role_category")["is_fresher_friendly"]
    .agg(["sum", "count"])
)

fresher_by_role["rate_percent"] = (
    fresher_by_role["sum"] /
    fresher_by_role["count"] * 100
)

fresher_by_role = fresher_by_role.sort_values(
    "rate_percent",
    ascending=False
)


# Role combinations

role_work_mode = pd.crosstab(
    filtered_df["role_category"],
    filtered_df["work_mode"]
)

role_experience = pd.crosstab(
    filtered_df["role_category"],
    filtered_df["experience_tier"]
)

role_city = pd.crosstab(
    filtered_df["role_category"],
    filtered_df["primary_city"]
)

role_skill_domain = pd.crosstab(
    filtered_df["role_category"],
    filtered_df["skill_domain"]
)

city_work_mode = pd.crosstab(
    filtered_df["primary_city"],
    filtered_df["work_mode"]
)


# Company analysis

company_size_counts = (
    filtered_df["company_size_bucket"]
    .value_counts()
)

company_size_role = pd.crosstab(
    filtered_df["company_size_bucket"],
    filtered_df["role_category"]
)

senior_by_company_size = (
    filtered_df.groupby("company_size_bucket")["is_senior"]
    .agg(["sum", "count"])
)

senior_by_company_size["senior_rate_percent"] = (
    senior_by_company_size["sum"] /
    senior_by_company_size["count"] * 100
)


# Salary analysis

salary_df = filtered_df[
    filtered_df["salary_disclosed"]
    & filtered_df["salary_midpoint_lpa"].notna()
].copy()

if not salary_df.empty:

    salary_by_role = (
        salary_df.groupby("role_category")["salary_midpoint_lpa"]
        .agg(["count", "mean", "median", "min", "max"])
        .sort_values("mean", ascending=False)
    )

    salary_by_experience = (
        salary_df.groupby("experience_tier")["salary_midpoint_lpa"]
        .agg(["count", "mean", "median", "min", "max"])
        .sort_values("mean", ascending=False)
    )

    salary_tier_counts = (
        salary_df["salary_tier"]
        .value_counts()
    )

else:

    salary_by_role = pd.DataFrame()

    salary_by_experience = pd.DataFrame()

    salary_tier_counts = pd.Series(dtype="int64")


# Salary negotiability

salary_negotiable_counts = (
    filtered_df["salary_negotiable"]
    .value_counts()
)

salary_negotiable_rate = (
    filtered_df["salary_negotiable"]
    .mean() * 100
)


# Experience analysis

experience_range = (
    filtered_df[
        ["experience_min_yrs", "experience_max_yrs"]
    ].describe()
)

average_min_experience = filtered_df[
    "experience_min_yrs"
].mean()

average_max_experience = filtered_df[
    "experience_max_yrs"
].mean()


# Seniority analysis

seniority_counts = (
    filtered_df["is_senior"]
    .value_counts()
)

senior_rate = (
    filtered_df["is_senior"].mean() * 100
)


# Skill analysis

skills_series = (
    filtered_df["skills_required"]
    .dropna()
    .str.split(",")
    .explode()
    .str.strip()
    .str.lower()
)

skills_series = skills_series[
    (skills_series != "") &
    (skills_series != "not available")
]

top_skills = skills_series.value_counts().head(20)


# Skill count analysis

average_skills_per_job = filtered_df[
    "skills_count"
].mean()

median_skills_per_job = filtered_df[
    "skills_count"
].median()


# Job recency

average_days_since_posted = filtered_df[
    "days_since_posted"
].mean()

median_days_since_posted = filtered_df[
    "days_since_posted"
].median()


# Data quality

missing_values = (
    filtered_df.isna()
    .sum()
    .sort_values(ascending=False)
)

duplicate_count = filtered_df.duplicated().sum()


# Ask CareerLens

st.divider()
st.subheader("Ask CareerLens")

st.caption(
    "Ask questions about the data, charts, and patterns in this dashboard."
)

user_question = st.text_input(
    "Ask about the data shown in CareerLens",
    placeholder="e.g. Which role has the highest average salary?"
)


if user_question:

    analysis_context = f"""
CareerLens dataset analysis:

TOTAL JOB MARKET
Total jobs: {len(filtered_df):,}


JOB DEMAND BY ROLE
{role_counts.to_string()}


TOP HIRING CITIES
{city_counts.to_string()}


WORK MODE
{work_mode_counts.to_string()}


EXPERIENCE LEVEL
{experience_counts.to_string()}


SKILL DOMAIN
{skill_domain_counts.to_string()}


TOP INDIVIDUAL SKILLS
{top_skills.to_string()}


FRESHER OPPORTUNITIES
Fresher-friendly jobs: {fresher_jobs:,}
Fresher-friendly rate: {fresher_rate:.2f}%

Fresher-friendly rate by role:
{role_fresher_rate.to_string()}


ROLE × WORK MODE
{role_work_mode.to_string()}


ROLE × EXPERIENCE
{role_experience.to_string()}


ROLE × CITY
{role_city.to_string()}


ROLE × SKILL DOMAIN
{role_skill_domain.to_string()}


CITY × WORK MODE
{city_work_mode.to_string()}


COMPANY SIZE
{company_size_counts.to_string()}


COMPANY SIZE × ROLE
{company_size_role.to_string()}


SENIOR POSITIONS BY COMPANY SIZE
{senior_by_company_size.to_string()}


SENIORITY
Senior jobs: {seniority_counts.get(True, 0):,}
Non-senior jobs: {seniority_counts.get(False, 0):,}
Senior-job rate: {senior_rate:.2f}%


SALARY DISCLOSURE
Jobs with disclosed salary: {salary_disclosed_jobs:,}
Salary disclosure rate: {salary_disclosure_rate:.2f}%


SALARY BY ROLE
{salary_by_role.to_string()}


SALARY BY EXPERIENCE
{salary_by_experience.to_string()}


SALARY TIERS
{salary_tier_counts.to_string()}


SALARY NEGOTIABILITY
{salary_negotiable_counts.to_string()}
Negotiable salary rate: {salary_negotiable_rate:.2f}%


EXPERIENCE RANGE

Average minimum experience:
{average_min_experience:.2f} years

Average maximum experience:
{average_max_experience:.2f} years

Overall experience statistics:
{experience_range.to_string()}


SKILL REQUIREMENTS

Average skills mentioned per job:
{average_skills_per_job:.2f}

Median skills mentioned per job:
{median_skills_per_job:.2f}


JOB RECENCY

Average days since posting:
{average_days_since_posted:.2f}

Median days since posting:
{median_days_since_posted:.2f}


DATA QUALITY

Duplicate rows:
{duplicate_count}

Missing values:
{missing_values.to_string()}
"""


    question_prompt = f"""
You are the data analyst for CareerLens.

CareerLens is an Indian technology job-market analytics dashboard.

Answer the user's question using ONLY the structured dataset analysis
provided below.

{analysis_context}


USER QUESTION:
{user_question}


RULES:

- Use only the CareerLens dataset analysis provided above.
- Do not use outside knowledge.
- Do not invent statistics.
- Do not invent companies, roles, salaries, skills, cities, or trends.
- If the question cannot be answered from the provided data, say:

"The available CareerLens data is insufficient to answer this question."

- If the user asks for "best", "worst", or a recommendation,
  do not give a subjective judgment.
  Instead, provide the measurable comparison available in the data.

- If the user asks about salary, use only jobs where salary is disclosed
  and salary_midpoint_lpa is available.

- Clearly distinguish between:
  1. What the data shows.
  2. What the pattern may mean.

- Do not confuse correlation or frequency with causation.
- Do not claim that a pattern proves why companies behave a certain way.
- Do not claim that one factor causes another unless the dataset directly supports it.

- Keep the answer concise but useful.
- Use numbers when relevant.
- Explain calculations in simple language when needed.
- If comparing categories, clearly name the categories being compared.

You are acting as a Business Analyst, not a generic chatbot.
"""


    try:

        answer = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=question_prompt
        )

        st.write(answer.text)

    except Exception as e:

        st.error(
            f"Unable to answer the question: {e}"
        )




# Footer

st.divider()

st.caption("CareerLens | Indian Tech Job Market Analytics")

