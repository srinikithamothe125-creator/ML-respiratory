import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages


# ============================================================
# SKILL 01 - TITANIC EXPLORATORY DATA ANALYSIS
# ============================================================

print("=" * 60)
print("TITANIC DATASET - EXPLORATORY DATA ANALYSIS")
print("=" * 60)


# ============================================================
# STEP 1: DEFINE THE PROBLEM
# ============================================================

print("\nSTEP 1: DEFINE THE PROBLEM")

print("""
Problem:
Analyze the Titanic dataset and understand the factors
that affected passenger survival.

Target variable:
survived

0 = Did not survive
1 = Survived
""")


# ============================================================
# STEP 2: LOAD THE TITANIC DATASET
# ============================================================

print("\nSTEP 2: LOAD THE TITANIC DATASET")

df = sns.load_dataset("titanic")

print("\nFirst 5 rows:")
print(df.head())


# ============================================================
# UNDERSTAND THE DATA
# ============================================================

print("\nDataset Shape:")
print(df.shape)

print("\nDataset Information:")
df.info()

print("\nStatistical Description:")
print(df.describe())


# ============================================================
# STEP 3: CLEAN THE DATA
# ============================================================

print("\nSTEP 3: CLEAN THE DATA")

print("\nMissing values before cleaning:")
print(df.isnull().sum())


# Remove duplicate rows
df = df.drop_duplicates()


# Fill missing numerical values
df["age"] = df["age"].fillna(df["age"].median())
df["fare"] = df["fare"].fillna(df["fare"].median())


# Fill missing categorical values
df["embarked"] = df["embarked"].fillna(
    df["embarked"].mode()[0]
)

df["embark_town"] = df["embark_town"].fillna(
    df["embark_town"].mode()[0]
)


print("\nMissing values after cleaning:")
print(df.isnull().sum())


# ============================================================
# LIFECYCLE MAPPING DICTIONARY
# ============================================================

print("\nLIFECYCLE MAPPING")

lifecycle_mapping = {
    "Child": "0-12",
    "Teenager": "13-19",
    "Young Adult": "20-35",
    "Middle Adult": "36-55",
    "Senior": "56+"
}

print("\nLifecycle Mapping Dictionary:")
print(lifecycle_mapping)


def get_lifecycle(age):

    if pd.isna(age):
        return "Unknown"

    elif age <= 12:
        return "Child"

    elif age <= 19:
        return "Teenager"

    elif age <= 35:
        return "Young Adult"

    elif age <= 55:
        return "Middle Adult"

    else:
        return "Senior"


df["lifecycle"] = df["age"].apply(get_lifecycle)


print("\nLifecycle counts:")
print(df["lifecycle"].value_counts())


# ============================================================
# STEP 4: EXPLORATORY DATA ANALYSIS
# ============================================================

print("\nSTEP 4: EXPLORATORY DATA ANALYSIS")


# ============================================================
# SURVIVAL BY SEX
# ============================================================

print("\nSurvival rate by sex:")

survival_by_sex = df.groupby("sex")["survived"].mean()

print(survival_by_sex)


# ============================================================
# SURVIVAL BY CLASS
# ============================================================

print("\nSurvival rate by class:")

survival_by_class = (
    df.groupby("class", observed=True)["survived"].mean()
)

print(survival_by_class)


# ============================================================
# SURVIVAL BY AGE
# ============================================================

print("\nAverage age by survival:")

survival_by_age = df.groupby("survived")["age"].mean()

print(survival_by_age)


# ============================================================
# SURVIVAL BY LIFECYCLE
# ============================================================

print("\nSurvival rate by lifecycle:")

survival_by_lifecycle = (
    df.groupby("lifecycle", observed=True)["survived"].mean()
)

print(survival_by_lifecycle)


# ============================================================
# CORRELATION ANALYSIS
# ============================================================

numerical_columns = [
    "survived",
    "pclass",
    "age",
    "sibsp",
    "parch",
    "fare"
]

correlation = df[numerical_columns].corr()

print("\nCorrelation Matrix:")
print(correlation)


# ============================================================
# CREATE 4-PAGE PDF
# ============================================================

print("\nCreating 4-page PDF...")

pdf_file = "titanic_eda_report.pdf"


with PdfPages(pdf_file) as pdf:

    # ========================================================
    # PAGE 1
    # DATASET OVERVIEW + MISSING VALUE HEATMAP
    # ========================================================

    fig = plt.figure(figsize=(11, 8.5))

    fig.suptitle(
        "TITANIC EDA REPORT - PAGE 1",
        fontsize=18,
        fontweight="bold"
    )

    ax1 = plt.subplot(2, 1, 1)
    ax1.axis("off")

    overview = f"""
DATASET OVERVIEW

Dataset: Titanic

Rows: {df.shape[0]}
Columns: {df.shape[1]}

Target Variable: survived

0 = Did not survive
1 = Survived

EDA Analysis:
• Missing values
• Survival by sex
• Survival by class
• Survival by age
• Lifecycle mapping
• Correlation analysis
"""

    ax1.text(
        0.05,
        0.9,
        overview,
        fontsize=12,
        verticalalignment="top"
    )


    ax2 = plt.subplot(2, 1, 2)

    sns.heatmap(
        df.isnull(),
        cbar=False,
        yticklabels=False,
        ax=ax2
    )

    ax2.set_title("Missing-Value Heatmap")

    plt.tight_layout()

    pdf.savefig(fig)

    plt.close(fig)


    # ========================================================
    # PAGE 2
    # SURVIVAL ANALYSIS
    # ========================================================

    fig, axes = plt.subplots(
        1,
        3,
        figsize=(15, 5)
    )

    fig.suptitle(
        "TITANIC EDA REPORT - PAGE 2: SURVIVAL ANALYSIS",
        fontsize=16,
        fontweight="bold"
    )


    sns.barplot(
        data=df,
        x="sex",
        y="survived",
        ax=axes[0]
    )

    axes[0].set_title("Survival Rate by Sex")
    axes[0].set_ylabel("Survival Rate")


    sns.barplot(
        data=df,
        x="class",
        y="survived",
        ax=axes[1]
    )

    axes[1].set_title("Survival Rate by Class")
    axes[1].set_ylabel("Survival Rate")


    sns.histplot(
        data=df,
        x="age",
        hue="survived",
        bins=20,
        kde=True,
        ax=axes[2]
    )

    axes[2].set_title("Age Distribution by Survival")
    axes[2].set_xlabel("Age")


    plt.tight_layout()

    pdf.savefig(fig)

    plt.close(fig)


    # ========================================================
    # PAGE 3
    # LIFECYCLE ANALYSIS
    # ========================================================

    fig, axes = plt.subplots(
        1,
        2,
        figsize=(13, 6)
    )

    fig.suptitle(
        "TITANIC EDA REPORT - PAGE 3: LIFECYCLE ANALYSIS",
        fontsize=16,
        fontweight="bold"
    )


    lifecycle_order = [
        "Child",
        "Teenager",
        "Young Adult",
        "Middle Adult",
        "Senior"
    ]


    sns.countplot(
        data=df,
        x="lifecycle",
        order=lifecycle_order,
        ax=axes[0]
    )

    axes[0].set_title(
        "Passenger Count by Lifecycle"
    )

    axes[0].set_xlabel(
        "Lifecycle Stage"
    )

    axes[0].set_ylabel(
        "Passenger Count"
    )

    axes[0].tick_params(
        axis="x",
        rotation=45
    )


    sns.barplot(
        data=df,
        x="lifecycle",
        y="survived",
        order=lifecycle_order,
        ax=axes[1]
    )

    axes[1].set_title(
        "Survival Rate by Lifecycle"
    )

    axes[1].set_xlabel(
        "Lifecycle Stage"
    )

    axes[1].set_ylabel(
        "Survival Rate"
    )

    axes[1].tick_params(
        axis="x",
        rotation=45
    )


    plt.tight_layout()

    pdf.savefig(fig)

    plt.close(fig)


    # ========================================================
    # PAGE 4
    # CORRELATION HEATMAP + CONCLUSIONS
    # ========================================================

    fig, axes = plt.subplots(
        1,
        2,
        figsize=(15, 6)
    )

    fig.suptitle(
        "TITANIC EDA REPORT - PAGE 4",
        fontsize=16,
        fontweight="bold"
    )


    sns.heatmap(
        correlation,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        ax=axes[0]
    )

    axes[0].set_title(
        "Correlation Heatmap"
    )


    axes[1].axis("off")

    conclusions = """
EDA CONCLUSIONS

1. Female passengers had a higher
   survival rate than male passengers.

2. First-class passengers generally
   had a higher survival rate.

3. Age showed a relationship with
   passenger survival.

4. Fare and passenger class showed
   relationships with survival.

5. Lifecycle mapping helps compare
   survival across age groups.

6. Missing values were identified
   and cleaned before analysis.

7. Correlation analysis helps identify
   relationships between numerical
   variables.
"""

    axes[1].text(
        0.05,
        0.9,
        conclusions,
        fontsize=11,
        verticalalignment="top"
    )


    plt.tight_layout()

    pdf.savefig(fig)

    plt.close(fig)


# ============================================================
# COMPLETION
# ============================================================

print("\n" + "=" * 60)
print("EDA COMPLETED SUCCESSFULLY!")
print("=" * 60)

print("\nPDF created:")
print("titanic_eda_report.pdf")

print("\nGenerated files:")
print("1. titanic_eda.py")
print("2. titanic_eda_report.pdf")
