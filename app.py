import os
import tempfile

import pandas as pd
import streamlit as st

from file_loader import load_file
from data_overview import data_summary
from schema_detection import detect_numeric, detect_date, classify_columns

from cleaning_data import (
    turning_categ,
    turning_date,
    is_ID,
    not_full_num,
    duplicate_val,
    null_val,
    null_deal,
    outliers,
)

from EDA import (
    descr,
    num_vizual,
    num_rela,
    cat_vizual,
    generate_insights,
)


# ============================================================
# CONFIG
# ============================================================

st.set_page_config(
    page_title="Lameh",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# STYLE
# ============================================================

st.html(
    """
<style>

/* ============================================================
   DESIGN TOKENS
   ============================================================ */

:root {
    --bg: #0A101E;
    --surface: #101A2C;
    --surface-soft: #131F34;
    --surface-hover: #17253D;

    --border: rgba(148, 163, 184, 0.13);

    --text: #EDF2F9;
    --soft: #B8C2D4;
    --muted: #7C8AA2;

    --green: #14B87E;
    --green-dark: #08704D;
    --green-soft: rgba(20, 184, 126, 0.09);

    --red: #E26D68;
}


/* ============================================================
   GLOBAL
   ============================================================ */

@import url(
    'https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&display=swap'
);

html,
body,
[class*="css"] {
    font-family: "IBM Plex Sans", sans-serif;
}

.stApp {
    background: var(--bg);
    color: var(--text);
}

.main .block-container {
    max-width: 1320px;
    padding-top: 2.8rem;
    padding-bottom: 5rem;
}


/* ============================================================
   TYPOGRAPHY
   ============================================================ */

h1,
h2,
h3,
h4 {
    color: var(--text) !important;
    letter-spacing: -0.02em;
}

p,
label {
    color: var(--soft);
}

.main-heading {
    max-width: 760px;
}

.main-heading h1 {
    font-size: clamp(2.4rem, 5vw, 4.4rem);
    line-height: 1.02;
    font-weight: 700;
    letter-spacing: -0.045em;
    margin-bottom: 20px;
}

.main-heading p {
    max-width: 700px;
    color: var(--soft);
    font-size: 1rem;
    line-height: 1.8;
}

.section-description {
    color: var(--muted);
    font-size: .78rem;
    line-height: 1.6;
}


/* ============================================================
   SIDEBAR
   ============================================================ */

section[data-testid="stSidebar"] {
    background: #0C1423;
    border-right: 1px solid var(--border);
}

section[data-testid="stSidebar"] > div {
    padding: 1.25rem 1rem;
}

.sidebar-brand {
    padding: 8px 4px 28px;
}

.sidebar-brand-name {
    color: var(--text);
    font-size: .88rem;
    font-weight: 600;
    letter-spacing: .01em;
}

.sidebar-brand-description {
    color: var(--muted);
    font-size: .65rem;
    margin-top: 4px;
}

.sidebar-heading {
    color: var(--muted);
    font-size: .62rem;
    font-weight: 600;
    letter-spacing: .08em;
    text-transform: uppercase;
    margin: 5px 4px 12px;
}


/* ============================================================
   WORKFLOW
   ============================================================ */

.sidebar-step {
    display: flex;
    align-items: center;
    gap: 10px;

    padding: 8px 6px;
    margin: 2px 0;

    border-radius: 7px;

    transition:
        background .15s ease,
        color .15s ease;
}

.sidebar-step-current {
    background: rgba(20, 184, 126, .06);
}

.sidebar-step-icon {
    width: 20px;
    height: 20px;

    display: flex;
    align-items: center;
    justify-content: center;

    border-radius: 50%;

    font-size: .58rem;
    font-weight: 600;

    flex-shrink: 0;

    border: 1px solid rgba(148, 163, 184, .16);
}

.sidebar-current {
    background: var(--green);
    border-color: var(--green);
    color: white;
}

.sidebar-pending {
    background: transparent;
    color: var(--muted);
}

.sidebar-step-text {
    color: var(--muted);
    font-size: .70rem;
}

.sidebar-step-text-current {
    color: var(--text);
    font-weight: 600;
}


/* ============================================================
   TOP HEADER
   ============================================================ */

.top-header {
    display: flex;
    align-items: center;
    justify-content: space-between;

    padding-bottom: 20px;
    margin-bottom: 46px;

    border-bottom: 1px solid var(--border);
}

.brand {
    display: flex;
    align-items: center;
}

.brand-name {
    color: var(--text);
    font-size: .88rem;
    font-weight: 600;
}

.brand-description {
    color: var(--muted);
    font-size: .64rem;
    margin-top: 3px;
}

.status {
    color: var(--muted);
    font-size: .68rem;
}


/* ============================================================
   WELCOME / LANDING
   ============================================================ */

.welcome {
    min-height: calc(100vh - 150px);

    display: flex;
    flex-direction: column;
    justify-content: center;

    padding: 2rem 0 4rem;
}

.welcome-content {
    max-width: 900px;
}

.welcome-eyebrow {
    color: var(--green);
    font-size: .68rem;
    font-weight: 600;
    letter-spacing: .14em;
    text-transform: uppercase;

    margin-bottom: 18px;
}

.welcome-title {
    color: var(--text);
    font-size: clamp(4rem, 10vw, 7.5rem);
    line-height: .9;
    font-weight: 700;

    letter-spacing: -0.065em;

    margin: 0 0 24px;
}

.welcome-subtitle {
    color: var(--soft);

    font-size: clamp(1rem, 1.6vw, 1.2rem);

    line-height: 1.7;

    max-width: 760px;

    margin: 0;
}

.welcome-description {
    color: var(--muted);

    font-size: .78rem;

    line-height: 1.8;

    max-width: 720px;

    margin-top: 16px;
}


/* ============================================================
   WELCOME FEATURES
   ============================================================ */

.feature-grid {
    display: grid;

    grid-template-columns: repeat(4, 1fr);

    gap: 12px;

    margin-top: 54px;

    max-width: 1100px;
}

.feature-card {
    background: var(--surface);

    border: 1px solid var(--border);

    border-radius: 10px;

    padding: 19px 18px;

    min-height: 135px;

    transition:
        background .18s ease,
        border-color .18s ease,
        transform .18s ease,
        box-shadow .18s ease;
}

.feature-card:hover {
    background: var(--surface-soft);

    border-color: rgba(20, 184, 126, .22);

    transform: translateY(-2px);

    box-shadow: 0 10px 24px rgba(0, 0, 0, .16);
}

.feature-number {
    color: var(--green);

    font-size: .60rem;

    font-weight: 600;

    letter-spacing: .08em;

    margin-bottom: 15px;
}

.feature-title {
    color: var(--text);

    font-size: .78rem;

    font-weight: 600;

    margin-bottom: 7px;
}

.feature-description {
    color: var(--muted);

    font-size: .65rem;

    line-height: 1.65;
}


/* ============================================================
   WELCOME ACTION
   ============================================================ */

.welcome-action {
    margin-top: 38px;
}

.welcome-note {
    color: var(--muted);

    font-size: .64rem;

    line-height: 1.6;

    margin-top: 12px;
}


/* ============================================================
   LANDING PAGE
   ============================================================ */

.landing {
    padding: 2.5rem 0 1rem;
}

.landing-eyebrow {
    color: var(--green);
    font-size: .68rem;
    font-weight: 600;
    letter-spacing: .12em;
    text-transform: uppercase;
    margin-bottom: 16px;
}

.landing-note {
    max-width: 680px;
    color: var(--muted);
    font-size: .72rem;
    line-height: 1.7;
    margin-top: 12px;
}

.upload-section {
    margin-top: 55px;
    padding-top: 28px;
    border-top: 1px solid var(--border);
}

.upload-title {
    color: var(--text);
    font-size: 1rem;
    font-weight: 600;
    margin-bottom: 5px;
}

.upload-description {
    color: var(--muted);
    font-size: .72rem;
    margin-bottom: 18px;
}


/* ============================================================
   FILE UPLOADER
   ============================================================ */

section[data-testid="stFileUploaderDropzone"] {
    background: var(--surface);
    border: 1px dashed rgba(148, 163, 184, .25);

    border-radius: 12px;

    min-height: 145px;

    transition:
        background .2s ease,
        border-color .2s ease;
}

section[data-testid="stFileUploaderDropzone"]:hover {
    border-color: rgba(20, 184, 126, .40);

    background: var(--surface-soft);
}


/* ============================================================
   METRICS
   ============================================================ */

.metric-grid {
    display: grid;

    grid-template-columns: repeat(4, 1fr);

    gap: 12px;

    margin: 18px 0 30px;
}

.metric-card {
    padding: 17px 18px;

    background: var(--surface);

    border: 1px solid var(--border);

    border-radius: 10px;
}

.metric-label {
    color: var(--muted);

    font-size: .59rem;

    text-transform: uppercase;

    letter-spacing: .08em;
}

.metric-value {
    color: var(--text);

    font-size: 1.35rem;

    font-weight: 600;

    margin-top: 6px;
}

.metric-detail {
    color: var(--muted);

    font-size: .61rem;

    margin-top: 3px;
}


/* ============================================================
   INFORMATION
   ============================================================ */

.info,
.warning {
    padding: 12px 15px;

    border-radius: 8px;

    margin: 12px 0;

    font-size: .72rem;

    line-height: 1.65;
}

.info {
    background: rgba(20, 184, 126, .055);

    border: 1px solid rgba(20, 184, 126, .16);

    color: var(--soft);
}

.warning {
    background: rgba(226, 109, 104, .055);

    border: 1px solid rgba(226, 109, 104, .16);

    color: #F09A96;
}


/* ============================================================
   REVIEW ITEMS
   ============================================================ */

.review-item {
    padding: 13px 15px;

    background: var(--surface);

    border: 1px solid var(--border);

    border-radius: 9px;

    margin-bottom: 8px;
}

.review-column {
    color: var(--text);

    font-size: .76rem;

    font-weight: 600;
}

.review-reason {
    color: var(--muted);

    font-size: .65rem;

    margin-top: 4px;
}


/* ============================================================
   BUTTONS
   ============================================================ */

.stButton > button,
.stDownloadButton > button,
.stFormSubmitButton > button {

    min-height: 40px;

    padding: 0 16px;

    border-radius: 8px !important;

    font-family: "IBM Plex Sans", sans-serif !important;

    font-size: .73rem !important;

    font-weight: 500 !important;

    background: var(--surface) !important;

    color: var(--soft) !important;

    border: 1px solid var(--border) !important;

    box-shadow: none !important;

    transition:
        transform .18s ease,
        border-color .18s ease,
        color .18s ease,
        background .18s ease,
        box-shadow .18s ease !important;
}

.stButton > button:hover,
.stDownloadButton > button:hover,
.stFormSubmitButton > button:hover {

    border-color: rgba(20, 184, 126, .35) !important;

    color: var(--text) !important;

    transform: translateY(-2px) !important;

    box-shadow: 0 8px 20px rgba(0, 0, 0, .18) !important;
}

.stButton > button:active,
.stDownloadButton > button:active,
.stFormSubmitButton > button:active {

    transform: translateY(0) !important;

    box-shadow: none !important;
}

.stButton > button[kind="primary"],
.stFormSubmitButton > button[kind="primary"] {

    background: var(--green) !important;

    color: white !important;

    border-color: var(--green) !important;

    box-shadow: none !important;
}

.stButton > button[kind="primary"]:hover,
.stFormSubmitButton > button[kind="primary"]:hover {

    background: #12A974 !important;

    border-color: #12A974 !important;

    color: white !important;

    transform: translateY(-2px) !important;

    box-shadow: 0 8px 20px rgba(20, 184, 126, .14) !important;
}


/* ============================================================
   WELCOME BUTTON
   ============================================================ */

.welcome-action .stButton > button {

    min-height: 46px !important;

    padding: 0 24px !important;

    font-size: .78rem !important;

    border-radius: 9px !important;
}


/* ============================================================
   RADIO — NO CIRCLE
   ============================================================ */

div[data-testid="stRadio"] div[role="radiogroup"] {

    gap: 7px !important;

    flex-wrap: wrap;
}

div[data-testid="stRadio"] div[role="radiogroup"] label {

    position: relative !important;

    background: var(--surface) !important;

    border: 1px solid var(--border) !important;

    border-radius: 8px !important;

    padding: 8px 15px !important;

    min-height: 36px;

    color: var(--soft) !important;

    cursor: pointer;

    transition:
        background .15s ease,
        border-color .15s ease,
        color .15s ease,
        transform .15s ease;
}


/* Remove radio circle */

div[data-testid="stRadio"] div[role="radiogroup"] label > div:first-child {

    display: none !important;
}

div[data-testid="stRadio"] input[type="radio"] {

    display: none !important;
}


/* Selected */

div[data-testid="stRadio"] div[role="radiogroup"] label:has(
    input[type="radio"]:checked
) {

    background: rgba(20, 184, 126, .12) !important;

    border-color: rgba(20, 184, 126, .45) !important;

    color: var(--green) !important;
}


/* Hover */

div[data-testid="stRadio"] div[role="radiogroup"] label:hover {

    border-color: rgba(20, 184, 126, .30) !important;

    transform: translateY(-1px);
}


/* Keyboard focus */

div[data-testid="stRadio"] div[role="radiogroup"] label:has(
    input[type="radio"]:focus-visible
) {

    outline: 1px solid rgba(20, 184, 126, .55);

    outline-offset: 2px;
}


/* ============================================================
   INPUTS
   ============================================================ */

div[data-baseweb="select"] > div,
input,
textarea {

    background: var(--surface) !important;

    color: var(--text) !important;

    border-color: var(--border) !important;

    border-radius: 8px !important;
}


/* ============================================================
   DATAFRAME
   ============================================================ */

div[data-testid="stDataFrame"] {

    border: 1px solid var(--border);

    border-radius: 10px;

    overflow: hidden;
}


/* ============================================================
   DOWNLOAD
   ============================================================ */

.stDownloadButton > button {

    background: rgba(20, 184, 126, .06) !important;

    border-color: rgba(20, 184, 126, .18) !important;

    color: var(--soft) !important;
}


/* ============================================================
   DIVIDERS
   ============================================================ */

hr {
    border-color: var(--border) !important;
}


/* ============================================================
   FOOTER
   ============================================================ */

.footer {
    margin-top: 80px;

    padding-top: 24px;

    border-top: 1px solid var(--border);

    display: flex;

    justify-content: space-between;

    gap: 30px;
}

.footer-name {
    color: var(--text);

    font-size: .75rem;

    font-weight: 600;
}

.footer-role {
    color: var(--muted);

    font-size: .65rem;

    margin-top: 4px;
}

.footer-links {
    display: flex;

    flex-direction: column;

    gap: 4px;

    text-align: right;
}

.footer-links a {
    color: var(--muted);

    font-size: .65rem;

    text-decoration: none;

    transition:
        color .15s ease,
        transform .15s ease;
}

.footer-links a:hover {
    color: var(--green);

    transform: translateX(-2px);
}

.footer-note {
    color: var(--muted);

    font-size: .60rem;

    line-height: 1.6;

    margin-top: 18px;

    max-width: 620px;
}


/* ============================================================
   RESPONSIVE
   ============================================================ */

@media (max-width: 900px) {

    .metric-grid {
        grid-template-columns: repeat(2, 1fr);
    }

    .feature-grid {
        grid-template-columns: repeat(2, 1fr);
    }

    .top-header {
        gap: 15px;
    }

    .main .block-container {
        padding-left: 1.25rem;
        padding-right: 1.25rem;
    }
}


@media (max-width: 600px) {

    .metric-grid {
        grid-template-columns: 1fr;
    }

    .feature-grid {
        grid-template-columns: 1fr;
    }

    .top-header {
        flex-direction: column;
        align-items: flex-start;
    }

    .welcome {
        min-height: auto;
        padding-top: 2rem;
    }

    .welcome-title {
        font-size: 4rem;
    }

    .main-heading h1 {
        font-size: 2.5rem;
    }

    .footer {
        flex-direction: column;
    }

    .footer-links {
        text-align: left;
    }
}

</style>
"""
)


# ============================================================
# STATE
# ============================================================

DEFAULT_STATE = {
    "stage": "welcome",
    "df": None,
    "numeric_columns": [],
    "categorical_columns": [],
    "id_columns": [],
    "review": [],
    "missing_values": None,
    "columns_to_treat": [],
    "schema_done": False,
    "filename": None,
}

for key, value in DEFAULT_STATE.items():

    if key not in st.session_state:
        st.session_state[key] = value


STAGES = [
    "welcome",
    "upload",
    "overview",
    "review",
    "duplicates",
    "nulls",
    "null_fill",
    "outliers",
    "eda",
]

WORKFLOW_STAGES = [
    "upload",
    "overview",
    "review",
    "duplicates",
    "nulls",
    "null_fill",
    "outliers",
    "eda",
]

STAGE_LABELS = {
    "upload": "Dataset Upload",
    "overview": "Dataset Overview",
    "review": "Schema Review",
    "duplicates": "Duplicate Records",
    "nulls": "Missing Values",
    "null_fill": "Missing Value Treatment",
    "outliers": "Outlier Analysis",
    "eda": "Exploratory Analysis",
}


# ============================================================
# NAVIGATION
# ============================================================

def go_to(stage):

    st.session_state.stage = stage
    st.rerun()


def restart():

    for key, value in DEFAULT_STATE.items():
        st.session_state[key] = value

    st.rerun()


# ============================================================
# FILE LOADING
# ============================================================

def load_uploaded_file(uploaded_file):

    suffix = os.path.splitext(uploaded_file.name)[1]

    temp_path = None

    try:

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix,
        ) as temp_file:

            temp_file.write(
                uploaded_file.getbuffer()
            )

            temp_path = temp_file.name

        return load_file(temp_path)

    except Exception as error:

        st.error(
            f"Unable to load dataset: {error}"
        )

        return None

    finally:

        if temp_path and os.path.exists(temp_path):

            os.remove(temp_path)


# ============================================================
# CURRENT STAGE
# ============================================================

current_stage = st.session_state.stage


# ============================================================
# SIDEBAR
# ============================================================

if current_stage != "welcome":

    with st.sidebar:

        st.html(
            """
            <div class="sidebar-brand">

                <div class="sidebar-brand-name">
                    Lameh
                </div>

                <div class="sidebar-brand-description">
                    Dataset Assessment & Exploratory Analytics
                </div>

            </div>
            """
        )

        st.html(
            '<div class="sidebar-heading">Analysis Workflow</div>'
        )

        current_index = (
            WORKFLOW_STAGES.index(current_stage)
            if current_stage in WORKFLOW_STAGES
            else 0
        )

        for index, stage in enumerate(WORKFLOW_STAGES):

            if index == current_index:

                icon = str(index + 1)

                icon_class = "sidebar-current"

                step_class = "sidebar-step-current"

            else:

                icon = str(index + 1)

                icon_class = "sidebar-pending"

                step_class = ""

            text_class = (
                "sidebar-step-text-current"
                if index == current_index
                else ""
            )

            st.html(
                f"""
                <div class="sidebar-step {step_class}">

                    <div class="sidebar-step-icon {icon_class}">
                        {icon}
                    </div>

                    <div class="sidebar-step-text {text_class}">
                        {STAGE_LABELS[stage]}
                    </div>

                </div>
                """
            )

        st.divider()

        st.html(
            """
            <div class="sidebar-heading">
                About
            </div>

            <div style="
                color:#7C8AA2;
                font-size:.67rem;
                line-height:1.7;
            ">
                A structured workflow for assessing
                dataset structure, data quality,
                and statistical characteristics
                before exploratory analysis.
            </div>
            """
        )

        if st.session_state.df is not None:

            st.divider()

            if st.button(
                "Start New Analysis",
                use_container_width=True,
            ):

                restart()


# ============================================================
# HEADER
# ============================================================

if current_stage == "welcome":

    status = ""

elif st.session_state.df is None:

    status = "Ready"

else:

    status = "Dataset loaded"


if current_stage != "welcome":

    st.html(
        f"""
        <div class="top-header">

            <div class="brand">

                <div>

                    <div class="brand-name">
                        Lameh
                    </div>

                    <div class="brand-description">
                        Dataset Assessment & Exploratory Analytics
                    </div>

                </div>

            </div>

            <div class="status">
                {status}
            </div>

        </div>
        """
    )


# ============================================================
# WELCOME
# ============================================================

if current_stage == "welcome":

    st.html(
        """
        <div class="welcome">

            <div class="welcome-content">

                <div class="welcome-eyebrow">
                    DATASET ASSESSMENT & EXPLORATORY ANALYSIS
                </div>

                <h1 class="welcome-title">
                    Lameh
                </h1>

                <p class="welcome-subtitle">
                    A structured workflow for assessing,
                    validating, preparing, and exploring
                    tabular datasets.
                </p>

                <div class="welcome-description">
                    Lameh helps you examine how a dataset is
                    structured, identify potential data quality
                    issues, review uncertain column classifications,
                    make explicit cleaning decisions, and explore
                    the statistical characteristics of the resulting data.
                </div>

            </div>


            <div class="feature-grid">

                <div class="feature-card">

                    <div class="feature-number">
                        01
                    </div>

                    <div class="feature-title">
                        Assess Structure
                    </div>

                    <div class="feature-description">
                        Examine dataset dimensions, column types,
                        missing values, duplicates, and a preview
                        of the available records.
                    </div>

                </div>


                <div class="feature-card">

                    <div class="feature-number">
                        02
                    </div>

                    <div class="feature-title">
                        Review Schema
                    </div>

                    <div class="feature-description">
                        Detect columns that may require
                        clarification, including dates,
                        categorical variables, and identifiers.
                    </div>

                </div>


                <div class="feature-card">

                    <div class="feature-number">
                        03
                    </div>

                    <div class="feature-title">
                        Address Data Quality
                    </div>

                    <div class="feature-description">
                        Review duplicate records, missing values,
                        missing-value treatment, and statistical
                        outliers before analysis.
                    </div>

                </div>


                <div class="feature-card">

                    <div class="feature-number">
                        04
                    </div>

                    <div class="feature-title">
                        Explore the Data
                    </div>

                    <div class="feature-description">
                        Examine descriptive statistics,
                        distributions, categorical patterns,
                        and relationships between numerical variables.
                    </div>

                </div>

            </div>


            <div class="welcome-action">

                <div id="start-analysis"></div>

            </div>

        </div>
        """
    )

    start_col, _ = st.columns([1, 5])

    with start_col:

        if st.button(
            "Start Analysis →",
            type="primary",
            use_container_width=True,
        ):

            go_to("upload")


# ============================================================
# UPLOAD
# ============================================================

elif current_stage == "upload":

    st.html(
        """
        <div class="landing">

            <div class="landing-eyebrow">
                STEP 01 · DATASET UPLOAD
            </div>

            <div class="main-heading">

                <h1>
                    Start with your dataset.
                </h1>

                <p>
                    Upload a tabular dataset to begin a structured
                    assessment of its structure, quality, and
                    statistical characteristics.
                </p>

                <div class="landing-note">
                    Lameh will first inspect the dataset and identify
                    areas that may require review before continuing
                    through the data-quality and exploratory-analysis workflow.
                </div>

            </div>

            <div class="upload-section">

                <div class="upload-title">
                    Upload dataset
                </div>

                <div class="upload-description">
                    Supported formats: CSV, XLSX, and JSON.
                </div>

            </div>

        </div>
        """
    )

    uploaded_file = st.file_uploader(
        "Upload dataset",
        type=["csv", "xlsx", "json"],
        label_visibility="collapsed",
    )

    if uploaded_file:

        df = load_uploaded_file(
            uploaded_file
        )

        if df is not None:

            if (
                st.session_state.filename
                != uploaded_file.name
            ):

                st.session_state.df = df

                st.session_state.filename = (
                    uploaded_file.name
                )

                st.session_state.schema_done = False

                st.session_state.review = []

                st.session_state.numeric_columns = []

                st.session_state.categorical_columns = []

                st.session_state.id_columns = []

                st.session_state.missing_values = None

                st.session_state.columns_to_treat = []

            st.html(
                f"""
                <div class="info">

                    <strong>
                        {uploaded_file.name}
                    </strong>

                    loaded successfully —
                    {len(df):,} rows ×
                    {len(df.columns):,} columns.

                </div>
                """
            )

            st.html(
                f"""
                <div class="metric-grid">

                    <div class="metric-card">

                        <div class="metric-label">
                            Rows
                        </div>

                        <div class="metric-value">
                            {len(df):,}
                        </div>

                        <div class="metric-detail">
                            Observations
                        </div>

                    </div>


                    <div class="metric-card">

                        <div class="metric-label">
                            Columns
                        </div>

                        <div class="metric-value">
                            {len(df.columns):,}
                        </div>

                        <div class="metric-detail">
                            Variables
                        </div>

                    </div>


                    <div class="metric-card">

                        <div class="metric-label">
                            Missing
                        </div>

                        <div class="metric-value">
                            {int(df.isna().sum().sum()):,}
                        </div>

                        <div class="metric-detail">
                            Missing cells
                        </div>

                    </div>


                    <div class="metric-card">

                        <div class="metric-label">
                            Duplicates
                        </div>

                        <div class="metric-value">
                            {int(df.duplicated().sum()):,}
                        </div>

                        <div class="metric-detail">
                            Repeated records
                        </div>

                    </div>

                </div>
                """
            )

            if st.button(
                "Begin Dataset Assessment →",
                type="primary",
            ):

                go_to("overview")


# ============================================================
# OVERVIEW
# ============================================================

elif current_stage == "overview":

    df = st.session_state.df

    st.markdown(
        "## Dataset Overview"
    )

    st.markdown(
        """
        <div class="section-description">
            Inspect the dataset dimensions, column structure,
            record duplication, and missing-value profile.
        </div>
        """,
        unsafe_allow_html=True,
    )

    (
        data_size,
        columns_info,
        duplicates,
        missing_values,
        small_warning,
    ) = data_summary(df)

    st.session_state.missing_values = missing_values

    if small_warning:

        st.warning(
            "Small dataset detected (<50 observations). "
            "Exploratory patterns should be interpreted cautiously "
            "because estimates and visual patterns may be unstable."
        )

    st.html(
        f"""
        <div class="metric-grid">

            <div class="metric-card">

                <div class="metric-label">
                    Rows
                </div>

                <div class="metric-value">
                    {data_size["Rows"]:,}
                </div>

            </div>


            <div class="metric-card">

                <div class="metric-label">
                    Columns
                </div>

                <div class="metric-value">
                    {data_size["Columns"]:,}
                </div>

            </div>


            <div class="metric-card">

                <div class="metric-label">
                    Duplicates
                </div>

                <div class="metric-value">
                    {duplicates["Duplicates num"]:,}
                </div>

            </div>


            <div class="metric-card">

                <div class="metric-label">
                    Missing
                </div>

                <div class="metric-value">
                    {int(df.isna().sum().sum()):,}
                </div>

            </div>

        </div>
        """
    )

    st.markdown(
        "### Data Preview"
    )

    st.markdown(
        """
        <div class="section-description">
            A sample of the first 20 observations is shown for an
            initial inspection of values and column structure.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.dataframe(
        df.head(20),
        width="stretch",
        height=320,
    )

    st.markdown(
        "### Column Information"
    )

    st.markdown(
        """
        <div class="section-description">
            Review the detected data types and basic column-level
            characteristics before schema classification.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.dataframe(
        columns_info,
        width="stretch",
    )

    if not missing_values.empty:

        st.markdown(
            "### Missing Value Summary"
        )

        st.markdown(
            """
            <div class="section-description">
                Columns with missing observations are listed with
                their corresponding missing-value counts and percentages.
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.dataframe(
            missing_values,
            width="stretch",
        )

    if not st.session_state.schema_done:

        numeric_info = detect_numeric(df)

        date_info = detect_date(df)

        (
            df,
            review,
            numeric_columns,
            categorical_columns,
        ) = classify_columns(
            df,
            numeric_info,
            date_info,
        )

        st.session_state.df = df

        st.session_state.review = review

        st.session_state.numeric_columns = (
            numeric_columns
        )

        st.session_state.categorical_columns = (
            categorical_columns
        )

        st.session_state.schema_done = True

    if st.button(
        "Continue to Schema Review →",
        type="primary",
    ):

        go_to("review")


# ============================================================
# SCHEMA REVIEW
# ============================================================

elif current_stage == "review":

    df = st.session_state.df

    review = st.session_state.review

    st.markdown(
        "## Schema Review"
    )

    st.markdown(
        """
        <div class="section-description">
            Review columns for which automatic classification is
            uncertain. The detected suggestion is a starting point;
            the final classification remains your decision.
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not review:

        st.success(
            "No ambiguous columns were detected."
        )

        if st.button(
            "Continue to Data Quality →",
            type="primary",
        ):

            go_to("duplicates")

    else:

        st.info(
            f"{len(review)} column(s) require review before the "
            "data-quality assessment can continue."
        )

        with st.form(
            "schema_review_form"
        ):

            decisions = {}

            for index, item in enumerate(review):

                column = item["column"]

                reason = item["reason"]

                st.html(
                    f"""
                    <div class="review-item">

                        <div class="review-column">
                            {column}
                        </div>

                        <div class="review-reason">
                            {reason}
                        </div>

                    </div>
                    """
                )

                if reason == (
                    "Numeric column with few unique values - may be categorical"
                ):

                    decisions[column] = st.radio(
                        f"Should '{column}' be treated as categorical?",
                        ["Yes", "No"],
                        key=f"schema_{index}",
                        horizontal=True,
                    )

                elif reason == "Might be date":

                    decisions[column] = st.radio(
                        f"Should '{column}' be treated as a date variable?",
                        ["Yes", "No"],
                        key=f"schema_{index}",
                        horizontal=True,
                    )

                elif reason == (
                    "High unique ratio - possible identifier"
                ):

                    decisions[column] = st.radio(
                        f"Should '{column}' be treated as an identifier?",
                        ["Yes", "No"],
                        key=f"schema_{index}",
                        horizontal=True,
                    )

                elif reason == "Not fully numeric":

                    st.warning(
                        f"{column} contains values that cannot all "
                        "be interpreted as numeric. Values that cannot "
                        "be converted will be represented as missing values."
                    )

                st.divider()

            submitted = st.form_submit_button(
                "Apply Decisions & Continue",
                type="primary",
            )

        if submitted:

            normalized_decisions = {
                column: (
                    "y"
                    if value == "Yes"
                    else "n"
                )
                for column, value in decisions.items()
            }

            (
                df,
                numeric_columns,
                categorical_columns,
            ) = turning_categ(
                df,
                review,
                st.session_state.numeric_columns,
                st.session_state.categorical_columns,
                normalized_decisions,
            )

            df = turning_date(
                df,
                review,
                normalized_decisions,
            )

            id_columns = is_ID(
                review,
                normalized_decisions,
            )

            (
                df,
                numeric_columns,
            ) = not_full_num(
                df,
                review,
                numeric_columns,
            )

            st.session_state.df = df

            st.session_state.numeric_columns = (
                numeric_columns
            )

            st.session_state.categorical_columns = (
                categorical_columns
            )

            st.session_state.id_columns = (
                id_columns
            )

            go_to("duplicates")


# ============================================================
# DUPLICATES
# ============================================================

elif current_stage == "duplicates":

    df = st.session_state.df

    count = int(
        df.duplicated().sum()
    )

    st.markdown(
        "## Duplicate Records"
    )

    st.markdown(
        """
        <div class="section-description">
            Identify records that are exact duplicates of another
            row in the dataset and decide whether they should be removed.
        </div>
        """,
        unsafe_allow_html=True,
    )

    if count == 0:

        st.success(
            "No exact duplicate records were detected."
        )

        if st.button(
            "Continue to Missing Values →",
            type="primary",
        ):

            go_to("nulls")

    else:

        st.warning(
            f"{count:,} exact duplicate record(s) detected."
        )

        st.dataframe(
            df[
                df.duplicated(
                    keep=False
                )
            ].head(20),
            width="stretch",
        )

        choice = st.radio(
            "Remove duplicate records?",
            ["Yes", "No"],
            horizontal=True,
        )

        if st.button(
            "Apply Decision & Continue →",
            type="primary",
        ):

            normalized_choice = (
                "y"
                if choice == "Yes"
                else "n"
            )

            st.session_state.df = duplicate_val(
                df,
                normalized_choice,
            )

            go_to("nulls")


# ============================================================
# MISSING VALUES
# ============================================================

elif current_stage == "nulls":

    df = st.session_state.df

    missing_values = (
        st.session_state.missing_values
    )

    st.markdown(
        "## Missing Values"
    )

    st.markdown(
        """
        <div class="section-description">
            Review columns containing missing observations and
            decide whether to remove the affected values or retain
            the column for explicit treatment.
        </div>
        """,
        unsafe_allow_html=True,
    )

    if (
        missing_values is None
        or missing_values.empty
    ):

        st.success(
            "No missing values were detected."
        )

        if st.button(
            "Continue to Outlier Analysis →",
            type="primary",
        ):

            go_to("outliers")

    else:

        columns = missing_values[
            missing_values["null perc"] > 0
        ]

        if columns.empty:

            st.success(
                "No missing values were detected."
            )

            if st.button(
                "Continue to Outlier Analysis →",
                type="primary",
            ):

                go_to("outliers")

        else:

            with st.form(
                "missing_values_form"
            ):

                decisions = {}

                for column in columns.index:

                    percentage = columns.loc[
                        column,
                        "null perc",
                    ]

                    st.html(
                        f"""
                        <div class="review-item">

                            <div class="review-column">
                                {column}
                            </div>

                            <div class="review-reason">
                                {percentage:.1f}% missing
                            </div>

                        </div>
                        """
                    )

                    if percentage >= 50:

                        st.warning(
                            f"{column} has "
                            f"{percentage:.1f}% missing values. "
                            "A high proportion of missing observations "
                            "may affect interpretation and should be "
                            "considered when selecting a treatment."
                        )

                    decisions[column] = st.radio(
                        f"Treatment decision — {column}",
                        ["drop", "deal"],
                        key=f"missing_{column}",
                        horizontal=True,
                    )

                    st.divider()

                submitted = st.form_submit_button(
                    "Apply Decisions & Continue",
                    type="primary",
                )

            if submitted:

                deal_cols, df = null_val(
                    df,
                    missing_values,
                    decisions,
                )

                st.session_state.df = df

                st.session_state.columns_to_treat = (
                    deal_cols
                )

                if deal_cols:

                    go_to("null_fill")

                else:

                    go_to("outliers")


# ============================================================
# MISSING VALUE TREATMENT
# ============================================================

elif current_stage == "null_fill":

    df = st.session_state.df

    columns = (
        st.session_state.columns_to_treat
    )

    missing_values = (
        st.session_state.missing_values
    )

    st.markdown(
        "## Missing Value Treatment"
    )

    st.markdown(
        """
        <div class="section-description">
            Select a treatment for each retained column with missing
            values. For numerical variables, the suggested method is
            based on the observed skewness of the available values.
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.form(
        "missing_treatment_form"
    ):

        treatment_choices = {}

        for column in columns:

            series = df[column]

            percentage = missing_values.loc[
                column,
                "null perc",
            ]

            st.html(
                f"""
                <div class="review-item">

                    <div class="review-column">
                        {column}
                    </div>

                    <div class="review-reason">
                        {percentage:.1f}% missing
                    </div>

                </div>
                """
            )

            if pd.api.types.is_numeric_dtype(
                series
            ):

                skewness = series.skew()

                recommended = (
                    "mean"
                    if abs(skewness) < 0.5
                    else "median"
                )

                st.info(
                    f"Observed skewness: {skewness:.2f} · "
                    f"Suggested treatment: {recommended.title()}"
                )

                treatment_choices[column] = st.radio(
                    f"Treatment — {column}",
                    [
                        recommended,
                        "mean",
                        "median",
                        "keep",
                    ],
                    key=f"fill_{column}",
                    horizontal=True,
                )

            else:

                mode = series.mode()

                if mode.empty:

                    treatment_choices[column] = "keep"

                else:

                    st.info(
                        f"Most frequent observed category: "
                        f"{mode.iloc[0]}"
                    )

                    treatment_choices[column] = st.radio(
                        f"Treatment — {column}",
                        ["mode", "keep"],
                        key=f"fill_{column}",
                        horizontal=True,
                    )

            st.divider()

        submitted = st.form_submit_button(
            "Apply Treatment & Continue",
            type="primary",
        )

    if submitted:

        st.session_state.df = null_deal(
            df,
            columns,
            missing_values,
            treatment_choices,
        )

        go_to("outliers")


# ============================================================
# OUTLIERS
# ============================================================

elif current_stage == "outliers":

    df = st.session_state.df

    st.markdown(
        "## Outlier Analysis"
    )

    st.markdown(
        """
        <div class="section-description">
            Potential statistical outliers are identified using
            the interquartile range (IQR) rule. An outlier is an
            observation that falls unusually far from the central
            distribution; it is not necessarily an error and should
            be evaluated in context before removal.
        </div>
        """,
        unsafe_allow_html=True,
    )

    _, outlier_info = outliers(
        df,
        {},
    )

    if not outlier_info:

        st.success(
            "No statistical outliers were detected using the IQR rule."
        )

        if st.button(
            "Continue to Exploratory Analysis →",
            type="primary",
        ):

            go_to("eda")

    else:

        with st.form(
            "outlier_form"
        ):

            decisions = {}

            for column, info in outlier_info.items():

                st.markdown(
                    f"### {column}"
                )

                series = pd.to_numeric(
                    df[column],
                    errors="coerce",
                ).dropna()

                if not series.empty:

                    q1 = series.quantile(0.25)

                    q3 = series.quantile(0.75)

                    iqr = q3 - q1

                    lower_inner = q1 - 1.5 * iqr

                    upper_inner = q3 + 1.5 * iqr

                    lower_outer = q1 - 3 * iqr

                    upper_outer = q3 + 3 * iqr

                    st.html(
                        f"""
                        <div class="metric-grid">

                            <div class="metric-card">

                                <div class="metric-label">
                                    Q1
                                </div>

                                <div class="metric-value">
                                    {q1:.2f}
                                </div>

                                <div class="metric-detail">
                                    25th percentile
                                </div>

                            </div>


                            <div class="metric-card">

                                <div class="metric-label">
                                    Median
                                </div>

                                <div class="metric-value">
                                    {series.median():.2f}
                                </div>

                                <div class="metric-detail">
                                    50th percentile
                                </div>

                            </div>


                            <div class="metric-card">

                                <div class="metric-label">
                                    Q3
                                </div>

                                <div class="metric-value">
                                    {q3:.2f}
                                </div>

                                <div class="metric-detail">
                                    75th percentile
                                </div>

                            </div>


                            <div class="metric-card">

                                <div class="metric-label">
                                    IQR
                                </div>

                                <div class="metric-value">
                                    {iqr:.2f}
                                </div>

                                <div class="metric-detail">
                                    Q3 − Q1
                                </div>

                            </div>

                        </div>
                        """
                    )

                    st.html(
                        f"""
                        <div class="info">

                            <strong>
                                IQR interpretation
                            </strong>

                            <br><br>

                            The middle 50% of observations
                            lies between

                            <strong>
                                {q1:.2f}
                            </strong>

                            and

                            <strong>
                                {q3:.2f}
                            </strong>.

                            <br><br>

                            Values below

                            <strong>
                                {lower_inner:.2f}
                            </strong>

                            or above

                            <strong>
                                {upper_inner:.2f}
                            </strong>

                            are classified as mild outliers
                            under the 1.5 × IQR rule.

                            <br><br>

                            Values below

                            <strong>
                                {lower_outer:.2f}
                            </strong>

                            or above

                            <strong>
                                {upper_outer:.2f}
                            </strong>

                            are classified as extreme outliers
                            under the 3 × IQR rule.

                        </div>
                        """
                    )

                st.html(
                    f"""
                    <div class="metric-grid">

                        <div class="metric-card">

                            <div class="metric-label">
                                Mild Outliers
                            </div>

                            <div class="metric-value">
                                {info["mild_percent"]:.2f}%
                            </div>

                            <div class="metric-detail">
                                Beyond 1.5 × IQR
                            </div>

                        </div>


                        <div class="metric-card">

                            <div class="metric-label">
                                Extreme Outliers
                            </div>

                            <div class="metric-value">
                                {info["extreme_percent"]:.2f}%
                            </div>

                            <div class="metric-detail">
                                Beyond 3 × IQR
                            </div>

                        </div>


                        <div class="metric-card">

                            <div class="metric-label">
                                Mild Boundary
                            </div>

                            <div
                                class="metric-value"
                                style="font-size:1rem;"
                            >
                                {info["mild_range"][0]:.2f}
                                →
                                {info["mild_range"][1]:.2f}
                            </div>

                            <div class="metric-detail">
                                Lower → Upper
                            </div>

                        </div>


                        <div class="metric-card">

                            <div class="metric-label">
                                Extreme Boundary
                            </div>

                            <div
                                class="metric-value"
                                style="font-size:1rem;"
                            >
                                {info["extreme_range"][0]:.2f}
                                →
                                {info["extreme_range"][1]:.2f}
                            </div>

                            <div class="metric-detail">
                                Lower → Upper
                            </div>

                        </div>

                    </div>
                    """
                )

                options = ["keep"]

                if info["mild_percent"] > 0:

                    options.append("mild")

                if info["extreme_percent"] > 0:

                    options.append("extreme")

                if (
                    info["mild_percent"] > 0
                    and info["extreme_percent"] > 0
                ):

                    options.append("all")

                option_labels = {
                    "keep": "Keep all",
                    "mild": "Remove mild",
                    "extreme": "Remove extreme",
                    "all": "Remove mild + extreme",
                }

                decisions[column] = st.radio(
                    f"Action — {column}",
                    options,
                    format_func=lambda value:
                        option_labels[value],
                    key=f"outlier_{column}",
                    horizontal=True,
                )

                st.caption(
                    "Keep all = retain all observations · "
                    "Remove mild = remove observations beyond 1.5 × IQR · "
                    "Remove extreme = remove observations beyond 3 × IQR · "
                    "Remove mild + extreme = remove observations beyond 1.5 × IQR."
                )

                st.divider()

            submitted = st.form_submit_button(
                "Apply Decisions & Continue",
                type="primary",
            )

        if submitted:

            df, _ = outliers(
                df,
                decisions,
            )

            st.session_state.df = df

            go_to("eda")


# ============================================================
# EDA
# ============================================================

elif current_stage == "eda":

    df = st.session_state.df

    numeric_columns = (
        st.session_state.numeric_columns
    )

    categorical_columns = (
        st.session_state.categorical_columns
    )

    id_columns = (
        st.session_state.id_columns
    )

    st.markdown(
        "## Exploratory Analysis"
    )

    st.markdown(
        """
        <div class="section-description">
            Examine the cleaned dataset through descriptive statistics,
            numerical distributions, categorical distributions, and
            relationships between numerical variables.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.html(
        f"""
        <div class="metric-grid">

            <div class="metric-card">

                <div class="metric-label">
                    Final Rows
                </div>

                <div class="metric-value">
                    {len(df):,}
                </div>

                <div class="metric-detail">
                    Observations after selected treatments
                </div>

            </div>


            <div class="metric-card">

                <div class="metric-label">
                    Variables
                </div>

                <div class="metric-value">
                    {len(df.columns):,}
                </div>

                <div class="metric-detail">
                    Dataset columns
                </div>

            </div>


            <div class="metric-card">

                <div class="metric-label">
                    Numerical
                </div>

                <div class="metric-value">
                    {len(numeric_columns):,}
                </div>

                <div class="metric-detail">
                    Numerical variables
                </div>

            </div>


            <div class="metric-card">

                <div class="metric-label">
                    Categorical
                </div>

                <div class="metric-value">
                    {len(categorical_columns):,}
                </div>

                <div class="metric-detail">
                    Categorical variables
                </div>

            </div>

        </div>
        """
    )

    st.download_button(
        "Download Clean Dataset",
        data=df.to_csv(
            index=False
        ).encode("utf-8-sig"),
        file_name="cleaned_data.csv",
        mime="text/csv",
    )


    # --------------------------------------------------------
    # DESCRIPTIVE STATISTICS
    # --------------------------------------------------------

    st.markdown(
        "### Descriptive Statistics"
    )

    st.markdown(
        """
        <div class="section-description">
            Summary measures for the variables included in
            the descriptive analysis.
        </div>
        """,
        unsafe_allow_html=True,
    )

    descriptions = descr(
        df,
        id_columns,
    )

    if descriptions:

        descriptive_df = pd.DataFrame(
            descriptions
        ).T

        st.dataframe(
            descriptive_df,
            width="stretch",
        )


    # --------------------------------------------------------
    # NUMERICAL DISTRIBUTIONS
    # --------------------------------------------------------

    valid_numeric = [
        column

        for column in numeric_columns

        if (
            column in df.columns
            and pd.api.types.is_numeric_dtype(
                df[column]
            )
            and column not in id_columns
        )
    ]

    if valid_numeric:

        st.markdown(
            "### Numerical Distributions"
        )

        st.markdown(
            """
            <div class="section-description">
                Visualize the distribution of the numerical variables
                retained for exploratory analysis.
            </div>
            """,
            unsafe_allow_html=True,
        )

        fig = num_vizual(
            df,
            valid_numeric,
        )

        st.pyplot(
            fig,
            width="stretch",
        )


    # --------------------------------------------------------
    # CORRELATION
    # --------------------------------------------------------

    if len(valid_numeric) > 1:

        st.markdown(
            "### Correlation Analysis"
        )

        st.markdown(
            """
            <div class="section-description">
                Examine pairwise linear association between numerical
                variables. Correlation describes association, not causation.
            </div>
            """,
            unsafe_allow_html=True,
        )

        fig = num_rela(
            df,
            valid_numeric,
        )

        st.pyplot(
            fig,
            width="stretch",
        )


    # --------------------------------------------------------
    # CATEGORICAL DISTRIBUTIONS
    # --------------------------------------------------------

    valid_categorical = [
        column

        for column in categorical_columns

        if (
            column in df.columns
            and column not in id_columns
        )
    ]

    if valid_categorical:

        st.markdown(
            "### Categorical Distributions"
        )

        st.markdown(
            """
            <div class="section-description">
                Examine the observed frequency distribution of
                categorical variables included in the analysis.
            </div>
            """,
            unsafe_allow_html=True,
        )

        fig = cat_vizual(
            df,
            valid_categorical,
        )

        st.pyplot(
            fig,
            width="stretch",
        )


    # --------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------

    insights = generate_insights(
        df,
        valid_numeric,
        valid_categorical,
        id_columns,
    )

    if insights:

        st.markdown(
            "### Summary"
        )

        st.markdown(
            """
            <div class="section-description">
                Key observations identified from the dataset's
                descriptive characteristics and exploratory patterns.
                These observations are intended to support interpretation,
                not replace statistical or domain judgment.
            </div>
            """,
            unsafe_allow_html=True,
        )

        for insight in insights:

            st.markdown(
                f"• {insight}"
            )


    # --------------------------------------------------------
    # DISCLAIMER
    # --------------------------------------------------------

    st.html(
        """
        <div class="footer-note">

            Lameh is an analytical support tool.
            Its results are intended to help users inspect
            and assess their datasets and should not replace
            domain knowledge, statistical judgment, or
            task-specific analysis.

        </div>
        """
    )


    # --------------------------------------------------------
    # FOOTER
    # --------------------------------------------------------

    st.html(
        """
        <div class="footer">

            <div>

                <div class="footer-name">
                    Areena Almeshaly
                </div>

                <div class="footer-role">
                    Statistics & AI Student
                </div>

            </div>


            <div class="footer-links">

                <a href="mailto:areena1020@gmail.com">
                    Email
                </a>

                <a
                    href="https://www.linkedin.com/in/areena-almeshaly"
                    target="_blank"
                >
                    LinkedIn
                </a>

            </div>

        </div>
        """
    )


    if st.button(
        "Start New Analysis"
    ):

        restart()