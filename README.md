# Lamah

### Dataset Assessment & Exploratory Analysis

Lamah is a Python-based application for the initial assessment and exploration of tabular datasets.

It provides a structured workflow for examining dataset structure, reviewing ambiguous column types, identifying common data-quality issues, and exploring statistical patterns. Users can make their own data-treatment decisions throughout the workflow, apply those decisions, and export the resulting dataset for further analysis.

The goal is simple: **give you a clear first look at your data, help you decide what needs attention, and give you a direction for where to start next.**

> **Understand the data first. Then decide where to take the analysis.**

---

## Why I Built It

A large part of data analysis begins with the same fundamental questions:

* What does this dataset look like?
* What do the variables represent?
* Are there quality issues that need attention?
* Which columns need further interpretation?
* What patterns are already visible?

I wanted to turn these initial steps into a coherent workflow rather than keep them as disconnected operations inside a notebook.

Lamah brings together Python, Pandas, statistical reasoning, and exploratory analysis into a practical application that takes a dataset from **initial assessment to a processed, exploratory view**.

The application is designed to support the analyst's decisions, not make those decisions on their behalf.

---

## Workflow

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

The workflow is sequential by design. Each stage helps establish context for the next rather than treating data preparation and exploration as isolated operations.

---

## What It Covers

### 1. Dataset Overview

Lamah starts by profiling the dataset through:

* Dimensions
* Column structure and data types
* Unique and non-null values
* Missing values
* Duplicate records
* Memory usage

This provides an initial understanding of what the dataset contains before any treatment is applied.

### 2. Schema Detection & Review

Column roles are assessed using characteristics of the underlying values. The workflow can flag cases such as:

* Date-like columns
* Numeric columns with low cardinality that may represent categories
* Columns containing non-numeric values
* High-uniqueness columns that may represent identifiers

When the interpretation is ambiguous, the user is asked to review the column rather than having the application silently assume its meaning.

### 3. Data Quality & Treatment

Lamah surfaces duplicate records and missing values and allows the user to decide how they should be handled.

These decisions are then applied to the dataset.

The resulting processed dataset can be **exported and saved for use outside the application**.

### 4. Outlier Assessment

Potential outliers are evaluated using the IQR rule, with separate boundaries for observations beyond `1.5 × IQR` and `3 × IQR`.

An outlier is not automatically treated as an error. The purpose of this stage is to make unusual observations visible so they can be considered in context.

### 5. Exploratory Analysis

The final stage provides descriptive statistics and visual analysis of:

* Numerical distributions
* Categorical frequencies
* Relationships between numerical variables
* Correlations
* Summary observations from the available analysis

The result is not intended to be the end of the analysis. Instead, it helps the user understand **what the data is showing and where deeper analysis may be worth starting**.

---

## Design Approach

A key design choice in Lamah is the balance between **rule-based automation and human judgment**.

Some properties can be reasonably inferred from the data itself. Others depend on the meaning of a variable and cannot be reliably determined from values alone.

Lamah therefore uses rules to surface potential interpretations and issues, while leaving ambiguous decisions to the user.

This also applies to data treatment. The application does not assume that every missing value, duplicate, or unusual observation should be handled in the same way.

The user makes the treatment decisions, Lamah applies them through the workflow, and the resulting dataset can then be taken forward for further analysis.

---

## From Dataset to Direction

Lamah is intended to answer the questions that usually come **before** deeper analysis.

By the end of the workflow, the user should have:

* A clearer understanding of the dataset structure
* Identified areas that require attention
* Applied the data-treatment decisions they selected
* A processed dataset that can be exported
* An initial view of distributions and relationships
* A better idea of **where to begin the next stage of analysis**

This is the role of Lamah: not to decide what the analysis should be, but to make the starting point clearer.

---

## Implementation

The application separates the analytical logic from the Streamlit interface:

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

* **`app.py`** — Application flow, interface, state management, and user decisions.
* **`file_loader.py`** — Dataset loading.
* **`data_overview.py`** — Initial dataset profiling.
* **`schema_detection.py`** — Schema and column-role detection.
* **`cleaning_data.py`** — Data conversion, duplicate handling, missing-value treatment, and outlier processing.
* **`EDA.py`** — Descriptive analysis, visualizations, and generated observations.

The analytical behavior is implemented through explicit Python rules, Pandas operations, and statistical methods.

---

## Limitations

Lamah currently relies on explicit rules and heuristics. Its results therefore depend on how a dataset represents its values and on the assumptions encoded in those rules.

Some datasets may require manual interpretation or produce classifications and recommendations that are not appropriate for their context.

This is particularly relevant to schema detection, missing-value treatment, and outlier assessment.

Lamah should therefore be viewed as a **structured starting point for analysis**, rather than a system that guarantees a correct interpretation of every dataset.

---

## Tech Stack

* Python
* Pandas
* Matplotlib
* Seaborn
* Streamlit

---

## Author

**Areena Almeshaly**
Statistics & AI Student

[Email](mailto:areena1020@gmail.com) · [LinkedIn](https://www.linkedin.com/in/areena-almeshaly)

---

### Disclaimer

Lamah is an analytical support tool. Its results should be interpreted in the context of the underlying data, domain knowledge, and the purpose of the analysis.
