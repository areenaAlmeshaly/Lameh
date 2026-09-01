# Lamah

### Dataset Assessment & Exploratory Analysis

Lamah is a Python-based application for the initial assessment and exploration of tabular datasets.

It provides a structured workflow for examining dataset structure, reviewing ambiguous column types, identifying common data-quality issues, applying user-selected treatments, and exploring statistical patterns.

The result is a processed dataset that can be exported for further analysis, together with a clearer understanding of the dataset and where further analysis may begin.

> **Understand the data first. Then decide where to take the analysis.**

---

## Why I Built It

A large part of data analysis begins with the same questions:

* What does this dataset look like?
* What do the variables represent?
* Are there quality issues that need attention?
* Which columns require further interpretation?
* What patterns are already visible?

I wanted to turn these initial steps into a coherent workflow rather than keep them as disconnected operations inside a notebook.

Lamah brings together Python, Pandas, statistical reasoning, and exploratory analysis into a practical application that takes a dataset from **initial assessment to a processed and explored state**.

The purpose is not to remove analytical judgment, but to make the first stage of working with a dataset more structured and deliberate.

---

## How It Works

Lamah follows a sequential workflow in which each stage builds on the decisions and information established earlier.

```text
Upload
  ↓
Dataset Overview
  ↓
Schema Detection
  ↓
Schema Review
  ↓
Duplicate Assessment
  ↓
Missing Value Assessment & Treatment
  ↓
Outlier Assessment
  ↓
Exploratory Analysis
  ↓
Processed Dataset
```

---

## How to Use

1. **Upload a dataset** through the application.
2. **Review the dataset overview**, including its dimensions, columns, data types, missing values, and duplicates.
3. **Review detected schema cases** where a column may have an ambiguous type or role.
4. **Confirm or change the classification** of columns that require user interpretation.
5. **Review duplicate records** and decide whether they should be removed.
6. **Review missing values** and select how they should be treated.
7. **Review potential outliers** identified through the IQR method.
8. **Continue to exploratory analysis** to examine the resulting dataset.
9. **Export the processed dataset** and use it for further analysis outside Lamah.

The workflow is guided, but the treatment decisions remain with the user.

---

## What It Covers

### Dataset Overview

Lamah begins by profiling the dataset through:

* Dataset dimensions
* Column structure and data types
* Unique and non-null values
* Missing values
* Duplicate records
* Memory usage

This provides an initial view of the dataset before treatment decisions are made.

### Schema Detection & Review

The application uses characteristics of the underlying values to flag potentially ambiguous columns, including:

* Date-like columns
* Numeric columns with low cardinality that may represent categories
* Columns that are not fully numeric
* High-uniqueness columns that may represent identifiers

Detection is not treated as infallible. When a column requires interpretation, Lamah asks the user to review it rather than silently assuming its role.

### Data Quality & Treatment

Lamah identifies duplicate records and missing values and allows the user to decide how they should be handled.

Depending on the selected treatment, the application applies the decision to the working dataset. The resulting processed dataset can then be exported.

### Outlier Assessment

Potential outliers are assessed using the IQR rule.

The application distinguishes between observations beyond:

* `1.5 × IQR`
* `3 × IQR`

An unusual observation is not automatically considered an error. Outlier detection is used to make potentially important observations visible for further consideration.

### Exploratory Analysis

The EDA stage provides statistical and visual summaries including:

* Descriptive statistics
* Numerical distributions
* Categorical frequencies
* Relationships between numerical variables
* Correlations
* Summary observations from the available analysis

The purpose of this stage is to provide an initial view of the data and help identify where deeper analysis may be useful.

---

## Design Approach

A central design decision in Lamah is the balance between **rule-based automation and human judgment**.

Some characteristics can be reasonably inferred from the values in a dataset. Others depend on the meaning of a variable and cannot be reliably determined from its values alone.

For example, a column containing values such as `1, 2, 3, 4, 5` is technically numeric, but those values could represent measurements, ratings, codes, or categories.

Rather than forcing a single interpretation, Lamah can flag such cases for review.

The same principle is applied to data treatment: the application surfaces issues and provides treatment options, while the user decides what should happen to the data.

This makes Lamah a **guided analytical support tool**, rather than a black-box cleaning system.

---

## Implementation

The application separates the Streamlit interface and workflow from the main analytical components.

```text
Analyzer-proj/
│
├── app.py
├── file_loader.py
├── data_overview.py
├── schema_detection.py
├── cleaning_data.py
├── EDA.py
└── README.md
```

### Core Modules

**`app.py`**
Controls the Streamlit interface, workflow stages, session state, and user decisions.

**`file_loader.py`**
Handles dataset loading.

**`data_overview.py`**
Generates the initial dataset summary, including dimensions, column information, duplicates, missing values, and related checks.

**`schema_detection.py`**
Contains the logic used to detect numeric and date-like columns and classify potentially ambiguous column roles.

**`cleaning_data.py`**
Contains data-conversion logic, identifier checks, duplicate handling, missing-value handling, and outlier processing.

**`EDA.py`**
Contains descriptive analysis, visualizations, and generated observations.

The analytical behavior is implemented through explicit Python rules, Pandas operations, and statistical methods.

---

## Limitations

Lamah currently relies on explicit rules and heuristics. Its results therefore depend on how the input data is structured and represented, as well as on the assumptions encoded in those rules.

Some datasets may require manual interpretation or produce classifications and recommendations that are not appropriate for their specific context.

This is particularly relevant to:

* Schema detection
* Missing-value treatment
* Identifier detection
* Outlier assessment
* Automated summary observations

These limitations are part of the current implementation and are important to consider when interpreting the results.

Lamah is intended to provide a **structured first look and direction for further analysis**, not a definitive interpretation of every dataset.

---

## Tech Stack

* **Python**
* **Pandas**
* **Matplotlib**
* **Seaborn**
* **Streamlit**

---

## Running Locally

Clone the repository and install the required dependencies:

```bash
git clone <repository-url>
cd Analyzer-proj
pip install -r requirements.txt
```

Run the Streamlit application:

```bash
streamlit run app.py
```

The application will open in your browser.

> If the repository does not currently contain a `requirements.txt`, add one before using these installation instructions.

---

## Project Scope

Lamah focuses on the **initial stage of data analysis**:

```text
Dataset
   ↓
Understand
   ↓
Assess
   ↓
Make treatment decisions
   ↓
Process
   ↓
Explore
   ↓
Identify direction for further analysis
```

It is not intended to replace domain knowledge or determine the complete analytical approach for a dataset.

Its role is to reduce the friction between **receiving a dataset and knowing how to begin working with it**.

---

## Author

**Areena Almeshaly**
Statistics & AI Student

[Email](mailto:areena1020@gmail.com) · [LinkedIn](https://www.linkedin.com/in/areena-almeshaly)

---

### Disclaimer

Lamah is an analytical support tool. Its results depend on the input data and the rules implemented in the current version and should be interpreted in the context of the data, domain knowledge, and purpose of the analysis.
