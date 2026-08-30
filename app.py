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
from EDA import descr, num_vizual, num_rela, cat_vizual


# ============================================================
# CONFIG
# ============================================================

st.set_page_config(
    page_title="Insight Analyzer",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# STYLE
# ============================================================

st.html("""
<style>

/* ============================================================
   DESIGN TOKENS
   ============================================================ */

:root {
    --bg: #0A101E;
    --bg-deep: #080D18;

    --surface: rgba(16, 26, 44, 0.82);
    --surface-solid: #101A2C;
    --surface-2: #16223A;
    --surface-3: #1B2943;

    --border: rgba(148, 163, 184, 0.13);
    --border-soft: rgba(148, 163, 184, 0.08);

    --text: #EDF2F9;
    --soft: #B8C2D4;
    --muted: #7C8AA2;

    --green: #14B87E;
    --green-dark: #08704D;
    --green-soft: rgba(20, 184, 126, 0.10);

    --gold: #C9A84C;
    --red: #E26D68;
}


/* ============================================================
   APP BACKGROUND
   ============================================================ */

.stApp {
    background:
        radial-gradient(
            circle at 8% 0%,
            rgba(20, 184, 126, 0.07),
            transparent 28%
        ),
        radial-gradient(
            circle at 92% 8%,
            rgba(36, 78, 130, 0.10),
            transparent 30%
        ),
        linear-gradient(
            135deg,
            #080D18 0%,
            #0A101E 42%,
            #0C1423 100%
        );

    color: var(--text);
}


/* subtle depth behind main content */

.main {
    background:
        radial-gradient(
            circle at 50% 0%,
            rgba(255,255,255,0.015),
            transparent 35%
        );
}


/* ============================================================
   MAIN CONTAINER
   ============================================================ */

.main .block-container {
    max-width: 1400px;
    padding-top: 2.2rem;
    padding-bottom: 4rem;
}


/* ============================================================
   TYPOGRAPHY
   ============================================================ */

h1,
h2,
h3,
h4 {
    color: var(--text) !important;
    letter-spacing: -0.025em;
}

p,
label {
    color: var(--soft);
}

.page-title {
    color: var(--text);
    font-size: 2rem;
    font-weight: 800;
    letter-spacing: -1px;
    margin-bottom: 6px;
}

.page-description {
    color: var(--soft);
    font-size: .85rem;
    line-height: 1.7;
    max-width: 700px;
    margin-bottom: 28px;
}


/* ============================================================
   SIDEBAR
   ============================================================ */

section[data-testid="stSidebar"] {
    background:
        radial-gradient(
            circle at 0% 0%,
            rgba(20, 184, 126, 0.045),
            transparent 30%
        ),
        linear-gradient(
            180deg,
            #0D1524 0%,
            #0A111E 100%
        );

    border-right: 1px solid var(--border);
}

section[data-testid="stSidebar"] > div {
    padding: 1.2rem 1rem;
}


/* ============================================================
   SIDEBAR BRAND
   ============================================================ */

.sidebar-logo {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 8px 4px 26px;
}

.sidebar-logo-icon {
    width: 35px;
    height: 35px;

    display: flex;
    align-items: center;
    justify-content: center;

    border-radius: 10px;

    background:
        linear-gradient(
            135deg,
            var(--green),
            var(--green-dark)
        );

    color: white;
    font-size: .7rem;
    font-weight: 800;

    border: 1px solid rgba(201,168,76,.25);

    box-shadow:
        0 6px 18px rgba(0,0,0,.22),
        0 0 20px rgba(20,184,126,.07);
}

.sidebar-logo-text {
    color: var(--text);
    font-size: .9rem;
    font-weight: 800;
    letter-spacing: .02em;
}

.sidebar-logo-sub {
    color: var(--muted);
    font-size: .58rem;
    margin-top: 3px;
    letter-spacing: .08em;
}


/* ============================================================
   SIDEBAR WORKFLOW
   ============================================================ */

.sidebar-heading {
    color: var(--muted);
    font-size: .58rem;
    font-weight: 700;
    letter-spacing: 1.4px;
    text-transform: uppercase;
    margin: 8px 4px 13px;
}

.sidebar-step {
    display: flex;
    align-items: center;
    gap: 10px;

    padding: 8px 7px;
    margin: 4px 0;

    border-radius: 10px;

    transition:
        background .2s ease,
        border .2s ease;
}

.sidebar-step-current {
    background:
        linear-gradient(
            90deg,
            rgba(20,184,126,.10),
            rgba(20,184,126,.035)
        );

    border: 1px solid rgba(20,184,126,.16);

    box-shadow:
        inset 0 1px 0 rgba(255,255,255,.015);
}

.sidebar-step-icon {
    width: 26px;
    height: 26px;

    display: flex;
    align-items: center;
    justify-content: center;

    border-radius: 8px;

    font-size: .62rem;
    font-weight: 700;

    flex-shrink: 0;
}

.sidebar-current {
    background:
        linear-gradient(
            135deg,
            var(--green),
            var(--green-dark)
        );

    color: white;

    border: 1px solid rgba(201,168,76,.25);

    box-shadow:
        0 4px 12px rgba(20,184,126,.16);
}

.sidebar-complete {
    background: rgba(201,168,76,.09);
    border: 1px solid rgba(201,168,76,.13);
    color: var(--gold);
}

.sidebar-pending {
    background: rgba(255,255,255,.012);
    border: 1px solid var(--border);
    color: var(--muted);
}

.sidebar-step-text {
    color: var(--muted);
    font-size: .72rem;
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
    justify-content: space-between;
    align-items: center;

    padding-bottom: 22px;
    margin-bottom: 34px;

    border-bottom: 1px solid var(--border);
}

.brand {
    display: flex;
    align-items: center;
    gap: 13px;
}

.brand-icon {
    width: 43px;
    height: 43px;

    display: flex;
    align-items: center;
    justify-content: center;

    border-radius: 12px;

    background:
        linear-gradient(
            135deg,
            var(--green),
            var(--green-dark)
        );

    color: white;
    font-size: 1rem;
    font-weight: 800;

    border: 1px solid rgba(201,168,76,.28);

    box-shadow:
        0 8px 24px rgba(0,0,0,.24),
        0 0 24px rgba(20,184,126,.06);
}

.brand-name {
    color: var(--text);
    font-size: .92rem;
    font-weight: 800;
    letter-spacing: .02em;
}

.brand-description {
    color: var(--muted);
    font-size: .68rem;
    margin-top: 3px;
}

.status {
    padding: 7px 12px;

    border: 1px solid rgba(148,163,184,.13);
    border-radius: 999px;

    background:
        rgba(16,26,44,.65);

    color: var(--soft);
    font-size: .68rem;

    box-shadow:
        inset 0 1px 0 rgba(255,255,255,.025);
}


/* ============================================================
   SECTION HEADINGS
   ============================================================ */

.section {
    margin: 28px 0 15px;
}

.section-title {
    color: var(--text);
    font-size: 1.15rem;
    font-weight: 700;
}

.section-description {
    color: var(--muted);
    font-size: .72rem;
    margin-top: 4px;
}


/* ============================================================
   METRIC CARDS
   ============================================================ */

.metric-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;

    margin: 16px 0 28px;
}

.metric-card {
    position: relative;

    padding: 18px 18px 17px;

    background:
        linear-gradient(
            145deg,
            rgba(22,34,58,.92),
            rgba(13,23,39,.92)
        );

    border: 1px solid var(--border);

    border-radius: 14px;

    box-shadow:
        0 10px 28px rgba(0,0,0,.16),
        inset 0 1px 0 rgba(255,255,255,.025);

    overflow: hidden;
}


/* tiny accent line */

.metric-card::before {
    content: "";

    position: absolute;

    top: 0;
    left: 18px;
    right: 18px;

    height: 1px;

    background:
        linear-gradient(
            90deg,
            rgba(20,184,126,.35),
            transparent
        );
}

.metric-label {
    color: var(--muted);
    font-size: .58rem;

    text-transform: uppercase;
    letter-spacing: 1px;
}

.metric-value {
    color: var(--text);
    font-size: 1.5rem;
    font-weight: 700;

    margin-top: 7px;
}

.metric-detail {
    color: var(--muted);
    font-size: .61rem;
    margin-top: 3px;
}


/* ============================================================
   INFO / WARNING
   ============================================================ */

.info,
.warning {
    padding: 13px 16px;

    border-radius: 11px;

    margin: 13px 0;

    font-size: .73rem;
    line-height: 1.6;

    box-shadow:
        inset 0 1px 0 rgba(255,255,255,.018);
}

.info {
    background:
        linear-gradient(
            90deg,
            rgba(20,184,126,.085),
            rgba(20,184,126,.035)
        );

    border: 1px solid rgba(20,184,126,.18);

    color: var(--soft);
}

.warning {
    background:
        linear-gradient(
            90deg,
            rgba(226,109,104,.09),
            rgba(226,109,104,.035)
        );

    border: 1px solid rgba(226,109,104,.20);

    color: #F09A96;
}


/* ============================================================
   REVIEW CARDS
   ============================================================ */

.review-item {
    padding: 14px 16px;

    background:
        linear-gradient(
            145deg,
            rgba(22,34,58,.80),
            rgba(13,23,39,.72)
        );

    border: 1px solid var(--border);

    border-radius: 11px;

    margin-bottom: 8px;

    box-shadow:
        0 6px 18px rgba(0,0,0,.10);
}

.review-column {
    color: var(--text);
    font-size: .76rem;
    font-weight: 600;
}

.review-reason {
    color: var(--muted);
    font-size: .64rem;
    margin-top: 4px;
}


/* ============================================================
   DATAFRAME
   ============================================================ */

div[data-testid="stDataFrame"] {
    border: 1px solid var(--border);
    border-radius: 13px;
    overflow: hidden;

    box-shadow:
        0 10px 30px rgba(0,0,0,.13);
}


/* ============================================================
   FILE UPLOADER
   ============================================================ */

section[data-testid="stFileUploaderDropzone"] {
    background:
        linear-gradient(
            145deg,
            rgba(22,34,58,.72),
            rgba(12,21,36,.72)
        );

    border: 1px dashed rgba(148,163,184,.22);

    border-radius: 14px;

    min-height: 150px;

    box-shadow:
        0 12px 30px rgba(0,0,0,.14),
        inset 0 1px 0 rgba(255,255,255,.02);
}

section[data-testid="stFileUploaderDropzone"]:hover {
    border-color: rgba(20,184,126,.38);

    background:
        linear-gradient(
            145deg,
            rgba(22,40,59,.78),
            rgba(12,25,39,.76)
        );
}


/* ============================================================
   BUTTONS
   ============================================================ */

.stButton > button,
.stDownloadButton > button,
.stFormSubmitButton > button {

    min-height: 42px;

    padding: 0 17px;

    border-radius: 10px !important;

    font-size: .75rem !important;
    font-weight: 600 !important;

    border: 1px solid var(--border) !important;

    background:
        linear-gradient(
            145deg,
            rgba(22,34,58,.95),
            rgba(14,24,40,.95)
        ) !important;

    color: var(--soft) !important;

    box-shadow:
        0 5px 15px rgba(0,0,0,.12),
        inset 0 1px 0 rgba(255,255,255,.025);

    transition:
        transform .15s ease,
        border .15s ease,
        box-shadow .15s ease;
}

.stButton > button:hover,
.stDownloadButton > button:hover,
.stFormSubmitButton > button:hover {

    border-color: rgba(20,184,126,.30) !important;

    color: var(--text) !important;

    transform: translateY(-1px);

    box-shadow:
        0 8px 20px rgba(0,0,0,.18);
}


/* primary */

.stButton > button[kind="primary"],
.stFormSubmitButton > button[kind="primary"] {

    background:
        linear-gradient(
            135deg,
            #14B87E 0%,
            #08704D 100%
        ) !important;

    color: white !important;

    border:
        1px solid rgba(201,168,76,.28) !important;

    box-shadow:
        0 7px 20px rgba(20,184,126,.13),
        inset 0 1px 0 rgba(255,255,255,.10);
}

.stButton > button[kind="primary"]:hover,
.stFormSubmitButton > button[kind="primary"]:hover {

    box-shadow:
        0 10px 26px rgba(20,184,126,.18),
        inset 0 1px 0 rgba(255,255,255,.12);

    transform: translateY(-1px);
}


/* ============================================================
   INPUTS
   ============================================================ */

div[data-baseweb="select"] > div,
input,
textarea {

    background:
        rgba(22,34,58,.86) !important;

    color: var(--text) !important;

    border-color: var(--border) !important;

    border-radius: 9px !important;
}

div[data-baseweb="select"] > div:focus-within,
input:focus,
textarea:focus {

    border-color: rgba(20,184,126,.35) !important;

    box-shadow:
        0 0 0 1px rgba(20,184,126,.12) !important;
}


/* ============================================================
   RADIO / CHECKBOX
   ============================================================ */

/*
   Convert radio buttons into compact button-like choices.
   This removes the visible circular radio controls.
*/

div[data-testid="stRadio"] > div {
    gap: 8px !important;
}

div[data-testid="stRadio"] div[role="radiogroup"] {
    gap: 8px !important;
    flex-wrap: wrap;
}

div[data-testid="stRadio"] label {
    color: var(--soft) !important;

    background:
        linear-gradient(
            145deg,
            rgba(22,34,58,.95),
            rgba(14,24,40,.95)
        ) !important;

    border: 1px solid var(--border) !important;

    border-radius: 10px !important;

    padding: 8px 15px !important;

    min-height: 38px;

    cursor: pointer;

    transition:
        background .15s ease,
        border .15s ease,
        color .15s ease,
        transform .15s ease;

    box-shadow:
        0 5px 15px rgba(0,0,0,.10);
}

/* hide the circular radio */

div[data-testid="stRadio"] label > div:first-child {
    display: none !important;
}

/* selected radio option */

div[data-testid="stRadio"] label:has(input:checked) {
    background:
        linear-gradient(
            135deg,
            rgba(20,184,126,.22),
            rgba(8,112,77,.32)
        ) !important;

    border-color:
        rgba(20,184,126,.45) !important;

    color:
        var(--text) !important;

    box-shadow:
        0 5px 16px rgba(20,184,126,.10);
}

/* hover */

div[data-testid="stRadio"] label:hover {
    border-color:
        rgba(20,184,126,.30) !important;

    transform: translateY(-1px);
}


/* ============================================================
   DIVIDERS
   ============================================================ */

hr {
    border-color: var(--border) !important;
}


/* ============================================================
   DOWNLOAD BUTTON
   ============================================================ */

.stDownloadButton > button {
    background:
        linear-gradient(
            145deg,
            rgba(20,184,126,.10),
            rgba(10,25,39,.90)
        ) !important;

    border-color:
        rgba(20,184,126,.20) !important;

    color: var(--soft) !important;
}


/* ============================================================
   CAPTION
   ============================================================ */

.stCaption,
[data-testid="stCaptionContainer"] {
    color: var(--muted) !important;
}


/* ============================================================
   SCROLLBAR
   ============================================================ */

::-webkit-scrollbar {
    width: 7px;
    height: 7px;
}

::-webkit-scrollbar-track {
    background: #0A101E;
}

::-webkit-scrollbar-thumb {
    background: #26344B;
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: #33445F;
}


/* ============================================================
   RESPONSIVE
   ============================================================ */

@media (max-width: 900px) {

    .metric-grid {
        grid-template-columns: repeat(2, 1fr);
    }

    .top-header {
        gap: 15px;
        align-items: flex-start;
    }

    .status {
        font-size: .62rem;
    }
}

@media (max-width: 600px) {

    .metric-grid {
        grid-template-columns: 1fr;
    }

    .top-header {
        flex-direction: column;
    }

    .main .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }
}

</style>
""")


# ============================================================
# STATE
# ============================================================

DEFAULT_STATE = {
    "stage": "upload",
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

            temp_file.write(uploaded_file.getbuffer())
            temp_path = temp_file.name

        return load_file(temp_path)

    except Exception as error:
        st.error(f"Unable to load dataset: {error}")
        return None

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.html("""
    <div class="sidebar-logo">
        <div class="sidebar-logo-icon">IA</div>

        <div>
            <div class="sidebar-logo-text">INSIGHT ANALYZER</div>
            <div class="sidebar-logo-sub">DATA INTELLIGENCE</div>
        </div>
    </div>
    """)

    st.html('<div class="sidebar-heading">Analysis Workflow</div>')

    current_stage = st.session_state.stage
    current_index = STAGES.index(current_stage)

    for index, stage in enumerate(STAGES):

        if index < current_index:
            icon = "✓"
            icon_class = "sidebar-complete"
            step_class = ""

        elif index == current_index:
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

    st.html("""
    <div style="
        height:1px;
        background:rgba(148,163,184,.15);
        margin:22px 4px;
    "></div>

    <div class="sidebar-heading">Platform</div>

    <div style="
        color:#7C8AA2;
        font-size:.67rem;
        line-height:1.6;
    ">
        Dataset assessment, data-quality evaluation,
        preparation decisions, and exploratory analysis.
    </div>
    """)

    if st.session_state.df is not None:
        st.divider()

        if st.button("Start New Analysis", use_container_width=True):
            restart()


# ============================================================
# HEADER
# ============================================================

if st.session_state.df is None:
    status = "●  Ready for dataset"
else:
    status = "●  Dataset loaded"

st.html(
    f"""
    <div class="top-header">
        <div class="brand">
            <div class="brand-icon">◈</div>

            <div>
                <div class="brand-name">INSIGHT ANALYZER</div>
                <div class="brand-description">
                    Dataset Assessment & Exploratory Analytics
                </div>
            </div>
        </div>

        <div class="status">{status}</div>
    </div>
    """
)


# ============================================================
# UPLOAD
# ============================================================

if current_stage == "upload":

    st.markdown("## Analyze your dataset")

    st.markdown(
        """
        Upload a dataset to assess its structure, identify
        data-quality issues, prepare the data, and explore it.
        """
    )

    uploaded_file = st.file_uploader(
        "Upload CSV, XLSX, or JSON",
        type=["csv", "xlsx", "json"],
    )

    if uploaded_file:

        df = load_uploaded_file(uploaded_file)

        if df is not None:

            if st.session_state.filename != uploaded_file.name:

                st.session_state.df = df
                st.session_state.filename = uploaded_file.name
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
                    <strong>{uploaded_file.name}</strong>
                    loaded successfully —
                    {len(df):,} rows × {len(df.columns):,} columns.
                </div>
                """
            )

            st.html(
                f"""
                <div class="metric-grid">

                    <div class="metric-card">
                        <div class="metric-label">Rows</div>
                        <div class="metric-value">{len(df):,}</div>
                        <div class="metric-detail">Observations</div>
                    </div>

                    <div class="metric-card">
                        <div class="metric-label">Columns</div>
                        <div class="metric-value">{len(df.columns):,}</div>
                        <div class="metric-detail">Variables</div>
                    </div>

                    <div class="metric-card">
                        <div class="metric-label">Missing</div>
                        <div class="metric-value">
                            {int(df.isna().sum().sum()):,}
                        </div>
                        <div class="metric-detail">Missing cells</div>
                    </div>

                    <div class="metric-card">
                        <div class="metric-label">Duplicates</div>
                        <div class="metric-value">
                            {int(df.duplicated().sum()):,}
                        </div>
                        <div class="metric-detail">Repeated records</div>
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

    st.markdown("## Dataset Overview")

    st.markdown(
        "Inspect the structure and initial quality of the dataset."
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
            "Interpret exploratory patterns cautiously."
        )

    st.html(
        f"""
        <div class="metric-grid">

            <div class="metric-card">
                <div class="metric-label">Rows</div>
                <div class="metric-value">
                    {data_size["Rows"]:,}
                </div>
            </div>

            <div class="metric-card">
                <div class="metric-label">Columns</div>
                <div class="metric-value">
                    {data_size["Columns"]:,}
                </div>
            </div>

            <div class="metric-card">
                <div class="metric-label">Duplicates</div>
                <div class="metric-value">
                    {duplicates["Duplicates num"]:,}
                </div>
            </div>

            <div class="metric-card">
                <div class="metric-label">Missing</div>
                <div class="metric-value">
                    {int(df.isna().sum().sum()):,}
                </div>
            </div>

        </div>
        """
    )

    st.markdown("### Data Preview")
    st.dataframe(df.head(20), width="stretch", height=320)

    st.markdown("### Column Information")
    st.dataframe(columns_info, width="stretch")

    if not missing_values.empty:
        st.markdown("### Missing Value Summary")
        st.dataframe(missing_values, width="stretch")

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
        st.session_state.numeric_columns = numeric_columns
        st.session_state.categorical_columns = categorical_columns
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

    st.markdown("## Schema Review")

    st.markdown(
        "Review columns where automatic schema detection is uncertain."
    )

    if not review:

        st.success("No ambiguous columns were detected.")

        if st.button(
            "Continue to Data Quality →",
            type="primary",
        ):
            go_to("duplicates")

    else:

        st.info(f"{len(review)} column(s) require review.")

        with st.form("schema_review_form"):

            decisions = {}

            for index, item in enumerate(review):

                column = item["column"]
                reason = item["reason"]

                st.html(
                    f"""
                    <div class="review-item">
                        <div class="review-column">{column}</div>
                        <div class="review-reason">{reason}</div>
                    </div>
                    """
                )

                if reason == (
                    "Numeric column with few unique values - may be categorical"
                ):

                    decisions[column] = st.radio(
                        f"Is '{column}' categorical?",
                        ["Yes", "No"],
                        key=f"schema_{index}",
                        horizontal=True,
                    )

                elif reason == "Might be date":

                    decisions[column] = st.radio(
                        f"Is '{column}' a date variable?",
                        ["Yes", "No"],
                        key=f"schema_{index}",
                        horizontal=True,
                    )

                elif reason == (
                    "High unique ratio - possible identifier"
                ):

                    decisions[column] = st.radio(
                        f"Is '{column}' an identifier?",
                        ["Yes", "No"],
                        key=f"schema_{index}",
                        horizontal=True,
                    )

                elif reason == "Not fully numeric":

                    st.warning(
                        f"{column} contains values that cannot all "
                        "be interpreted as numeric. Invalid values "
                        "will become missing values."
                    )

                st.divider()

            submitted = st.form_submit_button(
                "Apply Decisions & Continue",
                type="primary",
            )

        if submitted:

            # Convert Yes/No UI values back to the values expected
            # by the existing cleaning functions.
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
            st.session_state.numeric_columns = numeric_columns
            st.session_state.categorical_columns = categorical_columns
            st.session_state.id_columns = id_columns

            go_to("duplicates")


# ============================================================
# DUPLICATES
# ============================================================

elif current_stage == "duplicates":

    df = st.session_state.df
    count = int(df.duplicated().sum())

    st.markdown("## Duplicate Records")

    if count == 0:

        st.success("No duplicate records were detected.")

        if st.button(
            "Continue to Missing Values →",
            type="primary",
        ):
            go_to("nulls")

    else:

        st.warning(f"{count:,} duplicate record(s) detected.")

        st.dataframe(
            df[df.duplicated(keep=False)].head(20),
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
    missing_values = st.session_state.missing_values

    st.markdown("## Missing Values")

    if missing_values is None or missing_values.empty:

        st.success("No missing values were detected.")

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

            st.success("No missing values were detected.")

            if st.button(
                "Continue to Outlier Analysis →",
                type="primary",
            ):
                go_to("outliers")

        else:

            with st.form("missing_values_form"):

                decisions = {}

                for column in columns.index:

                    percentage = columns.loc[
                        column,
                        "null perc",
                    ]

                    st.html(
                        f"""
                        <div class="review-item">
                            <div class="review-column">{column}</div>
                            <div class="review-reason">
                                {percentage:.1f}% missing
                            </div>
                        </div>
                        """
                    )

                    if percentage >= 50:
                        st.warning(
                            f"{column} has {percentage:.1f}% missing values."
                        )

                    decisions[column] = st.radio(
                        f"Treatment — {column}",
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
                st.session_state.columns_to_treat = deal_cols

                if deal_cols:
                    go_to("null_fill")
                else:
                    go_to("outliers")


# ============================================================
# MISSING VALUE TREATMENT
# ============================================================

elif current_stage == "null_fill":

    df = st.session_state.df
    columns = st.session_state.columns_to_treat
    missing_values = st.session_state.missing_values

    st.markdown("## Missing Value Treatment")

    with st.form("missing_treatment_form"):

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
                    <div class="review-column">{column}</div>
                    <div class="review-reason">
                        {percentage:.1f}% missing
                    </div>
                </div>
                """
            )

            if pd.api.types.is_numeric_dtype(series):

                skewness = series.skew()
                recommended = (
                    "mean"
                    if abs(skewness) < 0.5
                    else "median"
                )

                st.info(
                    f"Skewness: {skewness:.2f} · "
                    f"Recommended: {recommended.title()}"
                )

                treatment_choices[column] = st.radio(
                    f"Treatment — {column}",
                    [recommended, "mean", "median", "keep"],
                    key=f"fill_{column}",
                    horizontal=True,
                )

            else:

                mode = series.mode()

                if mode.empty:

                    treatment_choices[column] = "keep"

                else:

                    st.info(
                        f"Most frequent category: {mode.iloc[0]}"
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

    st.markdown("## Outlier Analysis")

    st.markdown(
        "Statistically unusual observations are identified using "
        "the IQR rule. Unusual does not necessarily mean incorrect."
    )

    # First call only calculates information because no decisions
    # are supplied yet.
    _, outlier_info = outliers(df, {})

    if not outlier_info:

        st.success("No statistical outliers were detected.")

        if st.button(
            "Continue to Exploratory Analysis →",
            type="primary",
        ):
            go_to("eda")

    else:

        with st.form("outlier_form"):

            decisions = {}

            for column, info in outlier_info.items():

                st.markdown(f"### {column}")

                # ------------------------------------------------
                # IQR INFORMATION
                # ------------------------------------------------

                q1 = info.get("q1")
                q3 = info.get("q3")
                iqr = info.get("iqr")

                # If the cleaning function already returns Q1/Q3/IQR,
                # use them. Otherwise calculate them here from the
                # current dataframe.
                if q1 is None or q3 is None or iqr is None:

                    series = pd.to_numeric(
                        df[column],
                        errors="coerce",
                    ).dropna()

                    if not series.empty:

                        q1 = series.quantile(0.25)
                        q3 = series.quantile(0.75)
                        iqr = q3 - q1

                if (
                    q1 is not None
                    and q3 is not None
                    and iqr is not None
                ):

                    st.html(
                        f"""
                        <div class="info">
                            <strong>How is an outlier determined?</strong><br>
                            The IQR (Interquartile Range) measures the
                            spread of the middle 50% of the data.
                            <br><br>

                            <strong>Q1:</strong> {q1:.2f}
                            &nbsp;&nbsp;·&nbsp;&nbsp;
                            <strong>Q3:</strong> {q3:.2f}
                            &nbsp;&nbsp;·&nbsp;&nbsp;
                            <strong>IQR:</strong> {iqr:.2f}
                            <br><br>

                            Values outside the displayed ranges are
                            considered statistically unusual according
                            to the corresponding IQR rule.
                        </div>
                        """
                    )

                    st.html(
                        f"""
                        <div class="metric-grid">

                            <div class="metric-card">
                                <div class="metric-label">
                                    Q1 — 25th Percentile
                                </div>
                                <div class="metric-value"
                                     style="font-size:1.15rem;">
                                    {q1:.2f}
                                </div>
                                <div class="metric-detail">
                                    Lower quartile
                                </div>
                            </div>

                            <div class="metric-card">
                                <div class="metric-label">
                                    Q3 — 75th Percentile
                                </div>
                                <div class="metric-value"
                                     style="font-size:1.15rem;">
                                    {q3:.2f}
                                </div>
                                <div class="metric-detail">
                                    Upper quartile
                                </div>
                            </div>

                            <div class="metric-card">
                                <div class="metric-label">
                                    IQR
                                </div>
                                <div class="metric-value"
                                     style="font-size:1.15rem;">
                                    {iqr:.2f}
                                </div>
                                <div class="metric-detail">
                                    Q3 − Q1
                                </div>
                            </div>

                            <div class="metric-card">
                                <div class="metric-label">
                                    Middle 50%
                                </div>
                                <div class="metric-value"
                                     style="font-size:1.15rem;">
                                    {q1:.2f} → {q3:.2f}
                                </div>
                                <div class="metric-detail">
                                    Central data range
                                </div>
                            </div>

                        </div>
                        """
                    )

                # ------------------------------------------------
                # OUTLIER RANGES
                # ------------------------------------------------

                st.html(
                    f"""
                    <div class="metric-grid">

                        <div class="metric-card">
                            <div class="metric-label">
                                Mild Outlier Range
                            </div>
                            <div class="metric-value"
                                 style="font-size:1rem;">
                                {info["mild_range"][0]:.2f}
                                →
                                {info["mild_range"][1]:.2f}
                            </div>
                            <div class="metric-detail">
                                Values beyond 1.5 × IQR
                            </div>
                        </div>

                        <div class="metric-card">
                            <div class="metric-label">
                                Mild Outliers
                            </div>
                            <div class="metric-value">
                                {info["mild_percent"]:.2f}%
                            </div>
                            <div class="metric-detail">
                                Statistical observations
                            </div>
                        </div>

                        <div class="metric-card">
                            <div class="metric-label">
                                Extreme Outlier Range
                            </div>
                            <div class="metric-value"
                                 style="font-size:1rem;">
                                {info["extreme_range"][0]:.2f}
                                →
                                {info["extreme_range"][1]:.2f}
                            </div>
                            <div class="metric-detail">
                                Values beyond 3 × IQR
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
                                Statistical observations
                            </div>
                        </div>

                    </div>
                    """
                )

                # ------------------------------------------------
                # DECISION
                # ------------------------------------------------

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

                # Make the choices explicit so the user knows
                # exactly what will happen.
                option_labels = {
                    "keep": "Keep all",
                    "mild": "Remove mild",
                    "extreme": "Remove extreme",
                    "all": "Remove mild + extreme",
                }

                decisions[column] = st.radio(
                    f"Action — {column}",
                    options,
                    format_func=lambda value: option_labels[value],
                    key=f"outlier_{column}",
                    horizontal=True,
                )

                st.caption(
                    "Keep all = no rows removed · "
                    "Remove mild = remove mild outliers only · "
                    "Remove extreme = remove extreme outliers only · "
                    "Remove mild + extreme = remove both."
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
    numeric_columns = st.session_state.numeric_columns
    categorical_columns = st.session_state.categorical_columns
    id_columns = st.session_state.id_columns

    st.markdown("## Exploratory Analysis")

    st.markdown(
        "Explore descriptive statistics, distributions, "
        "categorical variables, and numerical relationships."
    )

    st.html(
        f"""
        <div class="metric-grid">

            <div class="metric-card">
                <div class="metric-label">Final Rows</div>
                <div class="metric-value">{len(df):,}</div>
            </div>

            <div class="metric-card">
                <div class="metric-label">Variables</div>
                <div class="metric-value">{len(df.columns):,}</div>
            </div>

            <div class="metric-card">
                <div class="metric-label">Numerical</div>
                <div class="metric-value">{len(numeric_columns):,}</div>
            </div>

            <div class="metric-card">
                <div class="metric-label">Categorical</div>
                <div class="metric-value">
                    {len(categorical_columns):,}
                </div>
            </div>

        </div>
        """
    )

    st.download_button(
        "Download Clean Dataset",
        data=df.to_csv(index=False).encode("utf-8-sig"),
        file_name="cleaned_data.csv",
        mime="text/csv",
    )

    # --------------------------------------------------------
    # DESCRIPTIVE STATISTICS
    # --------------------------------------------------------

    st.markdown("### Descriptive Statistics")

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
    # NUMERICAL
    # --------------------------------------------------------

    valid_numeric = [
        column
        for column in numeric_columns
        if (
            column in df.columns
            and pd.api.types.is_numeric_dtype(df[column])
            and column not in id_columns
        )
    ]

    if valid_numeric:

        st.markdown("### Numerical Distributions")

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

        st.markdown("### Correlation Analysis")

        fig = num_rela(
            df,
            valid_numeric,
        )

        st.pyplot(
            fig,
            width="stretch",
        )

    # --------------------------------------------------------
    # CATEGORICAL
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

        st.markdown("### Categorical Distributions")

        fig = cat_vizual(
            df,
            valid_categorical,
        )

        st.pyplot(
            fig,
            width="stretch",
        )

    st.caption(
        "Insight Analyzer · Dataset Assessment & Exploratory Analytics"
    )

    if st.button("Start New Analysis"):
        restart()