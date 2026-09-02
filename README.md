# Lameh

### Dataset Assessment & Exploratory Analysis

🚀 **[Live Demo — Try Lameh](https://areenaalmeshaly-analyzer-proj-app-o1idh6.streamlit.app)**

Lameh is a Python-based application for assessing and exploring tabular datasets.

It brings together dataset profiling, schema detection, data treatment, and exploratory analysis into a guided workflow. The application helps users examine their dataset, review potentially ambiguous columns, handle common data issues, and explore basic statistical patterns before continuing with further analysis.

> **Understand the data first. Then decide where to take the analysis.**

---

## Workflow

```text
Upload
  ↓
Dataset Overview
  ↓
Schema Detection & Review
  ↓
Duplicates
  ↓
Missing Values
  ↓
Outliers
  ↓
Exploratory Analysis
  ↓
Processed Dataset
```

## Features

### Dataset Overview

Lameh provides an initial profile of the dataset, including:

* Number of rows and columns
* Memory usage
* Data types
* Unique and non-null values
* Duplicate records
* Missing values and percentages
* A warning for datasets with fewer than 50 rows

### Schema Detection

The application examines column values to identify potentially ambiguous cases, including:

* Numeric columns
* Date-like columns
* Numeric columns with few unique values that may represent categories
* Columns that are not fully numeric
* High-uniqueness columns that may represent identifiers

Ambiguous cases are presented for user review rather than automatically assigning a single interpretation.

### Data Treatment

Users can decide how identified issues should be handled.

The application supports:

* Converting values to numeric
* Converting columns to categorical or date types
* Identifying possible identifier columns
* Removing duplicate records
* Handling missing values using deletion, mean, median, mode, or keeping them
* Assessing and removing selected outliers

### Outlier Detection

Numerical columns are assessed using the IQR method.

Lameh distinguishes between:

* **Mild outliers:** between `1.5 × IQR` and `3 × IQR`
* **Extreme outliers:** beyond `3 × IQR`

Users can choose whether to remove mild outliers, extreme outliers, or both.

### Exploratory Analysis

The EDA stage provides:

* Descriptive statistics
* Histograms for numerical variables
* Frequency bar charts for categorical variables
* Correlation heatmap for numerical variables
* Automatically generated observations based on the available data

The generated observations currently focus on strong numerical relationships, strong skewness, and highly concentrated categorical variables.

## Design Approach

Lameh uses explicit rules and user decisions throughout the workflow.

Column characteristics can provide useful signals, but they do not always determine the meaning of a variable. For example, a numeric column with a small number of unique values could represent either a numerical variable or a categorical code.

For these cases, Lameh surfaces the case for review instead of forcing an interpretation.

The same approach is used for data treatment: the application identifies issues and provides treatment options, while the user decides what should be applied.

## Project Structure

```text
Analyzer-proj/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── src/
    ├── file_loader.py
    ├── data_overview.py
    ├── schema_detection.py
    ├── cleaning_data.py
    └── EDA.py
```

### Core Modules

**`app.py`**

Streamlit application interface and workflow.

**`src/file_loader.py`**

Loads CSV, XLSX, and JSON datasets.

**`src/data_overview.py`**

Generates dataset dimensions, column information, duplicates, missing-value information, memory usage, and the small-dataset warning.

**`src/schema_detection.py`**

Contains numeric detection, date detection, and column classification logic.

**`src/cleaning_data.py`**

Handles column conversion, identifier selection, duplicate removal, missing-value treatment, and outlier processing.

**`src/EDA.py`**

Contains descriptive statistics, numerical and categorical visualizations, correlation analysis, and generated observations.

## Installation & Local Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Analyzer-proj
```

### 2. Create a Virtual Environment

Creating a virtual environment keeps the project's dependencies isolated from other Python projects.

```bash
python3 -m venv .venv
```

Activate it on macOS/Linux:

```bash
source .venv/bin/activate
```

### 3. Install Dependencies

Install the libraries required by Lameh:

```bash
pip install -r requirements.txt
```

The dependencies include:

* Streamlit
* Pandas
* Matplotlib
* Seaborn
* OpenPyXL

### 4. Run the Application

Start Lameh locally with:

```bash
streamlit run app.py
```

The application will open in your browser through the local Streamlit server.

## Live Demo

Lameh is deployed with Streamlit and can be used directly without local installation.

🚀 **[Open Lameh](https://areenaalmeshaly-analyzer-proj-app-o1idh6.streamlit.app)**

## Limitations

Lameh currently relies on explicit rules and thresholds. The interpretation of a column can depend on the context and meaning of the underlying data, so detected classifications should be reviewed by the user.

Similarly, outliers and missing values are not automatically treated as errors. Their appropriate treatment depends on the dataset and analysis context.

The generated observations are based on a limited set of statistical conditions and are intended as an initial summary rather than a complete interpretation of the dataset.

## Tech Stack

**Python · Pandas · Matplotlib · Seaborn · Streamlit**

## Scope

Lameh focuses on the **initial assessment and exploration of tabular data**.

It is intended to help users move from receiving a dataset to understanding its basic structure, addressing selected data issues, and identifying initial statistical patterns that can guide further analysis.

## Author

**Areena Almeshaly**

Statistics & AI Student

---

**Disclaimer:** Lameh is an analytical support tool. Its results depend on the input data and the rules implemented in the current version and should be interpreted in the context of the data and the purpose of the analysis.
