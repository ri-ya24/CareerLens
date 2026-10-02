import pandas as pd
import os

file_path = "archive/indian_tech_jobs_2026.csv"

df = pd.read_csv(file_path)

print("\n--- DATASET SHAPE ---")
print(df.shape)

print("\n--- COLUMNS ---")
print(df.columns.tolist())

print("\n--- FIRST 5 ROWS ---")
print(df.head())

print("\n--- DATA TYPES ---")
print(df.dtypes)

print("\n--- MISSING VALUES ---")
print(df.isnull().sum())

print("\n--- DUPLICATES ---")
print(df.duplicated().sum())
print("\n--- ROLE CATEGORIES ---")
print(df["role_category"].value_counts())

print("\n--- WORK MODE ---")
print(df["work_mode"].value_counts())

print("\n--- TOP CITIES ---")
print(df["primary_city"].value_counts().head(15))

print("\n--- SKILL DOMAINS ---")
print(df["skill_domain"].value_counts())

print("\n--- SALARY TIERS ---")
print(df["salary_tier"].value_counts())

print("\n--- EXPERIENCE TIERS ---")
print(df["experience_tier"].value_counts())
print("\n--- SAMPLE SKILLS ---")
print(df["skills_required"].head(10).to_string(index=False))

print("\n--- FRESHER FRIENDLY ---")
print(df["is_fresher_friendly"].value_counts())

print("\n--- SALARY DISCLOSED ---")
print(df["salary_disclosed"].value_counts())

print("\n--- COMPANY SIZE ---")
print(df["company_size_bucket"].value_counts())