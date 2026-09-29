import re
import textwrap
import html

import pandas as pd
import streamlit as st

from agent.agent import analyze_return


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="ReturnSense",
    page_icon="↩️",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# HTML HELPER
# ============================================================

def render_html(content):
    st.html(textwrap.dedent(content))


# ============================================================
# AI TEXT CLEANING
# ============================================================

def clean_ai_text(text):

    if not text:
        return ""

    text = str(text)

    text = text.replace("**", "")
    text = text.replace("__", "")
    text = text.replace("`", "")

    text = re.sub(
        r"^\s*#+\s*",
        "",
        text,
        flags=re.MULTILINE
    )

    text = re.sub(
        r"\n\s*\n+",
        "\n",
        text
    )

    return text.strip()


def extract_section(text, section_name, all_sections):

    text = clean_ai_text(text)

    target_pattern = rf"{re.escape(section_name)}\s*:"

    target_match = re.search(
        target_pattern,
        text,
        re.IGNORECASE
    )

    if not target_match:
        return "No clear information found."

    start = target_match.end()

    next_positions = []

    for section in all_sections:

        if section.lower() == section_name.lower():
            continue

        pattern = rf"{re.escape(section)}\s*:"

        match = re.search(
            pattern,
            text[start:],
            re.IGNORECASE
        )

        if match:
            next_positions.append(
                start + match.start()
            )

    if next_positions:
        end = min(next_positions)
    else:
        end = len(text)

    value = text[start:end].strip()

    value = re.sub(
        r"^[\s:\-–—]+",
        "",
        value
    ).strip()

    return value if value else "No clear information found."


def shorten_text(text, max_length=300):

    text = clean_ai_text(text)

    if len(text) <= max_length:
        return text

    shortened = text[:max_length].rsplit(" ", 1)[0]

    return shortened + "..."


def format_evidence(text):

    text = clean_ai_text(text)

    text = re.sub(
        r"\s+(\d+\.)\s+",
        r"\n\n\1 ",
        text
    )

    text = re.sub(
        r"\s+(Return Memory\s+\d+)",
        r"\n\1",
        text,
        flags=re.IGNORECASE
    )

    return text.strip()


# ============================================================
# FLASH CARD TEXT
# ============================================================

def make_customer_card(text):

    text = clean_ai_text(text)

    lower = text.lower()

    if (
        "no clear pattern" in lower
        or "no previous" in lower
        or "only this" in lower
    ):
        return (
            "No repeated return pattern was found "
            "for this customer."
        )

    text = re.sub(
        r"has made two distinct return orders",
        "has returned products before",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"has made (\d+) distinct return orders",
        r"has returned products \1 times",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"distinct return orders",
        "previous returns",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"return orders",
        "returns",
        text,
        flags=re.IGNORECASE
    )

    return shorten_text(text, 210)


def make_product_card(text):

    text = clean_ai_text(text)

    lower = text.lower()

    if (
        "no clear pattern" in lower
        or "no previous" in lower
    ):
        return (
            "No repeated return pattern was found "
            "for this product."
        )

    text = re.sub(
        r"has been returned in at least two separate orders",
        "has been returned more than once",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"has been returned in two separate orders",
        "has been returned more than once",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"has been returned in (\d+) separate orders",
        r"has been returned \1 times",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"distinct return orders",
        "previous returns",
        text,
        flags=re.IGNORECASE
    )

    return shorten_text(text, 220)


def make_category_card(text):

    text = clean_ai_text(text)

    lower = text.lower()

    if (
        "no clear pattern" in lower
        or "no category" in lower
    ):
        return (
            "No strong category-wide return pattern "
            "was found."
        )

    text = re.sub(
        r"category-wide",
        "across this category",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"recurring",
        "repeated",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"SKUs",
        "products",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"sku",
        "product",
        text,
        flags=re.IGNORECASE
    )

    return shorten_text(text, 220)


# ============================================================
# CSS
# ============================================================

render_html(
    """
    <style>

    .stApp {
        background-color: #0D0B14;
        color: #FFFFFF;
    }

    .block-container {
        max-width: 1450px;
        padding-top: 1rem;
        padding-bottom: 1rem;
    }

    h1, h2, h3, h4, h5, h6 {
        color: #FFFFFF !important;
    }

    p {
        color: #AFA6BC;
    }


    /* ========================================================
       HEADER
    ======================================================== */

    .top-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-bottom: 12px;
        margin-bottom: 12px;
        border-bottom: 1px solid #292333;
    }

    .brand {
        display: flex;
        align-items: center;
        gap: 11px;
    }

    .brand-icon {
        width: 42px;
        height: 42px;
        border-radius: 11px;
        background: #8B5CF6;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #FFFFFF;
        font-size: 22px;
        font-weight: 700;
    }

    .brand-name {
        color: #FFFFFF;
        font-size: 1.5rem;
        font-weight: 800;
        line-height: 1;
    }

    .brand-name span {
        color: #8B5CF6;
    }

    .brand-subtitle {
        color: #81778F;
        font-size: 0.67rem;
        margin-top: 5px;
        letter-spacing: 0.45px;
    }

    .memory-status {
        background: #15121D;
        border: 1px solid #292333;
        border-radius: 10px;
        padding: 8px 13px;
        color: #C4B5FD;
        font-size: 0.75rem;
        display: flex;
        align-items: center;
        gap: 7px;
    }

    .status-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #8B5CF6;
    }


    /* ========================================================
       METRICS
    ======================================================== */

    .metric-card {
        background: #15121D;
        border: 1px solid #292333;
        border-radius: 11px;
        padding: 9px;
        text-align: center;
    }

    .metric-value {
        color: #FFFFFF;
        font-size: 1.15rem;
        font-weight: 800;
    }

    .metric-label {
        color: #81778F;
        font-size: 0.62rem;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        margin-top: 2px;
    }


    /* ========================================================
       MAIN CARDS
    ======================================================== */

    .card {
        background: #15121D;
        border: 1px solid #292333;
        border-radius: 14px;
        padding: 13px;
    }

    .card-title {
        color: #81778F;
        font-size: 0.67rem;
        font-weight: 700;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 4px;
    }

    .card-heading {
        color: #FFFFFF;
        font-size: 1.05rem;
        font-weight: 700;
    }


    /* ========================================================
       RETURN DETAILS
    ======================================================== */

    .return-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 7px 0;
        border-bottom: 1px solid #24202D;
    }

    .return-row:last-child {
        border-bottom: none;
    }

    .return-label {
        color: #81778F;
        font-size: 0.74rem;
    }

    .return-value {
        color: #FFFFFF;
        font-size: 0.79rem;
        font-weight: 600;
    }

    .reason-badge {
        background: #241B35;
        border: 1px solid #49356A;
        color: #C4B5FD;
        padding: 4px 8px;
        border-radius: 6px;
        font-size: 0.7rem;
        font-weight: 600;
    }


    /* ========================================================
       HINDSIGHT
    ======================================================== */

    .memory-number {
        color: #FFFFFF;
        font-size: 1.8rem;
        font-weight: 800;
    }

    .memory-text {
        color: #81778F;
        font-size: 0.7rem;
        margin-bottom: 8px;
    }

    .memory-line {
        padding: 7px 0;
        border-bottom: 1px solid #24202D;
    }

    .memory-line:last-child {
        border-bottom: none;
    }

    .memory-label {
        color: #81778F;
        font-size: 0.65rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .memory-value {
        color: #DCD6E5;
        font-size: 0.75rem;
        margin-top: 2px;
    }


    /* ========================================================
       ANALYSIS
    ======================================================== */

    .analysis-header {
        color: #A78BFA;
        font-size: 0.68rem;
        font-weight: 800;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-top: 14px;
    }

    .analysis-title {
        color: #FFFFFF;
        font-size: 1.35rem;
        font-weight: 800;
        margin-top: 3px;
        margin-bottom: 10px;
    }

    .section-caption {
        color: #81778F;
        font-size: 0.67rem;
        font-weight: 700;
        letter-spacing: 0.8px;
        text-transform: uppercase;
        margin-bottom: 8px;
    }


    /* ========================================================
       MAIN PATTERN
    ======================================================== */

    .main-pattern {
        background: #15121D;
        border: 1px solid #342B46;
        border-left: 4px solid #8B5CF6;
        border-radius: 13px;
        padding: 16px 18px;
    }

    .main-pattern-label {
        color: #81778F;
        font-size: 0.65rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.9px;
    }

    .main-pattern-text {
        color: #FFFFFF;
        font-size: 1rem;
        font-weight: 600;
        line-height: 1.5;
        margin-top: 7px;
    }


    /* ========================================================
       FLASH CARDS
    ======================================================== */

    .flash-card {
        background: linear-gradient(
            145deg,
            #181420,
            #121019
        );

        border: 1px solid #30283D;

        border-radius: 17px;

        padding: 18px;

        min-height: 190px;

        position: relative;

        overflow: hidden;

        box-shadow:
            0 8px 22px rgba(0, 0, 0, 0.18);
    }

    .flash-card::after {
        content: "";

        position: absolute;

        width: 90px;
        height: 90px;

        border-radius: 50%;

        background: #8B5CF6;

        opacity: 0.055;

        right: -28px;
        bottom: -30px;
    }

    .flash-card-top {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 15px;
    }

    .flash-icon {
        width: 38px;
        height: 38px;

        border-radius: 11px;

        background: #211936;

        border: 1px solid #4B3970;

        display: flex;
        align-items: center;
        justify-content: center;

        font-size: 18px;
    }

    .flash-label {
        color: #A78BFA;

        font-size: 0.67rem;

        font-weight: 800;

        letter-spacing: 1px;

        text-transform: uppercase;
    }

    .flash-headline {
        color: #FFFFFF;

        font-size: 1rem;

        font-weight: 750;

        line-height: 1.35;

        margin-bottom: 9px;
    }

    .flash-description {
        color: #BDB5C8;

        font-size: 0.78rem;

        line-height: 1.5;
    }


    /* ========================================================
       RECOMMENDATION
    ======================================================== */

    .recommendation-box {
        background: linear-gradient(
            135deg,
            #211936,
            #181326
        );

        border: 1px solid #4B3970;

        border-radius: 14px;

        padding: 17px 19px;

        min-height: 105px;

        box-shadow:
            0 8px 24px rgba(0, 0, 0, 0.16);
    }

    .recommendation-top {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 8px;
    }

    .recommendation-label {
        color: #C4B5FD;

        font-size: 0.67rem;

        font-weight: 800;

        letter-spacing: 0.9px;

        text-transform: uppercase;
    }

    .recommendation-text {
        color: #FFFFFF;

        font-size: 0.88rem;

        font-weight: 600;

        line-height: 1.5;
    }


    /* ========================================================
       CONFIDENCE
    ======================================================== */

    .confidence-box {
        background: #15121D;

        border: 1px solid #30283D;

        border-radius: 14px;

        padding: 17px;

        min-height: 105px;
    }

    .confidence-label {
        color: #81778F;

        font-size: 0.65rem;

        font-weight: 800;

        text-transform: uppercase;

        letter-spacing: 0.8px;
    }

    .confidence-value {
        color: #C4B5FD;

        font-size: 0.84rem;

        font-weight: 700;

        margin-top: 9px;

        line-height: 1.4;
    }


    /* ========================================================
       BUTTON
    ======================================================== */

    .stButton > button {
        width: 100%;

        height: 43px;

        background-color: #8B5CF6;

        color: #FFFFFF;

        border: none;

        border-radius: 9px;

        font-weight: 700;

        font-size: 0.84rem;
    }

    .stButton > button:hover {
        background-color: #7C4FE0;

        color: #FFFFFF;
    }


    /* ========================================================
       SELECTBOX
    ======================================================== */

    div[data-baseweb="select"] > div {
        background-color: #15121D;

        border: 1px solid #30283D;

        border-radius: 8px;
    }

    div[data-baseweb="select"] span {
        color: #FFFFFF !important;
    }


    /* ========================================================
       EXPANDERS
    ======================================================== */

    div[data-testid="stExpander"] {
        background-color: #15121D;

        border: 1px solid #292333;

        border-radius: 10px;
    }


    /* ========================================================
       HIDE STREAMLIT DEFAULTS
    ======================================================== */

    #MainMenu {
        visibility: hidden;
    }

    header {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    </style>
    """
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    return pd.read_csv(
        "data/returns_sustainability_dataset.csv"
    )


df = load_data()

returned_df = df[
    df["Return_Status"] == "Returned"
].copy()


# ============================================================
# HEADER
# ============================================================

render_html(
    """
    <div class="top-header">

        <div class="brand">

            <div class="brand-icon">
                ↩
            </div>

            <div>

                <div class="brand-name">
                    Return<span>Sense</span>
                </div>

                <div class="brand-subtitle">
                    AI THAT LEARNS WHY PRODUCTS COME BACK
                </div>

            </div>

        </div>


        <div class="memory-status">

            <span class="status-dot"></span>

            Hindsight Memory Connected

        </div>

    </div>
    """
)


# ============================================================
# METRICS
# ============================================================

total_orders = len(df)

returned_orders = len(
    returned_df
)

unique_customers = df[
    "User_ID"
].nunique()

return_rate = (
    returned_orders /
    total_orders
) * 100


m1, m2, m3, m4 = st.columns(4)


with m1:

    render_html(
        f"""
        <div class="metric-card">

            <div class="metric-value">
                {total_orders:,}
            </div>

            <div class="metric-label">
                Total Orders
            </div>

        </div>
        """
    )


with m2:

    render_html(
        f"""
        <div class="metric-card">

            <div class="metric-value">
                {returned_orders:,}
            </div>

            <div class="metric-label">
                Returned Orders
            </div>

        </div>
        """
    )


with m3:

    render_html(
        f"""
        <div class="metric-card">

            <div class="metric-value">
                {unique_customers:,}
            </div>

            <div class="metric-label">
                Customers
            </div>

        </div>
        """
    )


with m4:

    render_html(
        f"""
        <div class="metric-card">

            <div class="metric-value">
                {return_rate:.1f}%
            </div>

            <div class="metric-label">
                Return Rate
            </div>

        </div>
        """
    )


st.markdown(
    "<div style='height:10px'></div>",
    unsafe_allow_html=True
)


# ============================================================
# RETURN ANALYSIS + HINDSIGHT
# ============================================================

left, right = st.columns(
    [1.05, 0.95],
    gap="medium"
)


# ============================================================
# RETURN SELECTION
# ============================================================

with left:

    render_html(
        """
        <div class="card">

            <div class="card-title">
                Return Analysis
            </div>

            <div class="card-heading">
                Select a return to investigate
            </div>

        </div>
        """
    )


    # --------------------------------------------------------
    # CREATE USER-FRIENDLY SELECTOR
    # --------------------------------------------------------

    order_ids = returned_df[
        "Order_ID"
    ].tolist()


    def format_return(order_id):

        selected_row = returned_df[
            returned_df["Order_ID"] == order_id
        ].iloc[0]

        order_id_text = str(
            selected_row["Order_ID"]
        )

        reason_text = str(
            selected_row["Return_Reason"]
        )

        category_text = str(
            selected_row["Product_Category"]
        )

        return (
            f"{order_id_text}  •  "
            f"{reason_text}  •  "
            f"{category_text}"
        )


    selected_order = st.selectbox(
        "Select a return",
        order_ids,
        format_func=format_return,
        label_visibility="collapsed"
    )


    row = returned_df[
        returned_df["Order_ID"] ==
        selected_order
    ].iloc[0]


    # --------------------------------------------------------
    # SELECTED RETURN DETAILS
    # --------------------------------------------------------

    render_html(
        f"""
        <div class="card">

            <div class="return-row">

                <span class="return-label">
                    Return ID
                </span>

                <span class="return-value">
                    {html.escape(str(row["Order_ID"]))}
                </span>

            </div>


            <div class="return-row">

                <span class="return-label">
                    Customer
                </span>

                <span class="return-value">
                    {html.escape(str(row["User_ID"]))}
                </span>

            </div>


            <div class="return-row">

                <span class="return-label">
                    Product
                </span>

                <span class="return-value">
                    {html.escape(str(row["Product_ID"]))}
                </span>

            </div>


            <div class="return-row">

                <span class="return-label">
                    Category
                </span>

                <span class="return-value">
                    {html.escape(str(row["Product_Category"]))}
                </span>

            </div>


            <div class="return-row">

                <span class="return-label">
                    Return Reason
                </span>

                <span class="reason-badge">
                    {html.escape(str(row["Return_Reason"]))}
                </span>

            </div>


            <div class="return-row">

                <span class="return-label">
                    Order Value
                </span>

                <span class="return-value">
                    ₹{row["Order_Value"]:,.2f}
                </span>

            </div>

        </div>
        """
    )


    st.markdown(
        "<div style='height:7px'></div>",
        unsafe_allow_html=True
    )


    analyze_clicked = st.button(
        "✨  ANALYZE THIS RETURN",
        use_container_width=True
    )


# ============================================================
# HINDSIGHT MEMORY
# ============================================================

with right:

    render_html(
        """
        <div class="card">

            <div class="card-title">
                Long-Term Memory
            </div>

            <div class="card-heading">
                🧠 Hindsight
            </div>

            <div style="height:7px"></div>

            <div class="memory-number">
                5,889
            </div>

            <div class="memory-text">
                Memory units currently stored
            </div>


            <div class="memory-line">

                <div class="memory-label">
                    Customer Memory
                </div>

                <div class="memory-value">
                    Previous experiences from the same customer
                </div>

            </div>


            <div class="memory-line">

                <div class="memory-label">
                    Product Memory
                </div>

                <div class="memory-value">
                    Previous returns associated with the product
                </div>

            </div>


            <div class="memory-line">

                <div class="memory-label">
                    Outcome Memory
                </div>

                <div class="memory-value">
                    Previous recommendations and actions
                </div>

            </div>

        </div>
        """
    )


# ============================================================
# AI ANALYSIS
# ============================================================

if analyze_clicked:

    return_data = {

        "order_id":
            row["Order_ID"],

        "customer_id":
            row["User_ID"],

        "product_id":
            row["Product_ID"],

        "category":
            row["Product_Category"],

        "order_date":
            row["Order_Date"],

        "return_reason":
            row["Return_Reason"],

        "days_to_return":
            row["Days_to_Return"],

        "order_value":
            row["Order_Value"],

        "return_cost":
            row["Return_Cost"],

        "profit_loss":
            row["Profit_Loss"],

        "co2_emissions":
            row["CO2_Emissions"],

        "packaging_waste":
            row["Packaging_Waste"],
    }


    with st.spinner(
        "🧠 Recalling Hindsight memories and analyzing..."
    ):

        try:

            # =================================================
            # RUN AGENT
            # =================================================

            result = analyze_return(
                return_data
            )


            # =================================================
            # SECTION NAMES
            # =================================================

            sections = [

                "Pattern Detected",

                "Customer Pattern",

                "Product Pattern",

                "Category Pattern",

                "Evidence",

                "Recommendation",

                "Reason",

                "Confidence",
            ]


            # =================================================
            # EXTRACT AI SECTIONS
            # =================================================

            pattern_detected = extract_section(
                result,
                "Pattern Detected",
                sections
            )

            customer_pattern = extract_section(
                result,
                "Customer Pattern",
                sections
            )

            product_pattern = extract_section(
                result,
                "Product Pattern",
                sections
            )

            category_pattern = extract_section(
                result,
                "Category Pattern",
                sections
            )

            evidence = extract_section(
                result,
                "Evidence",
                sections
            )

            recommendation = extract_section(
                result,
                "Recommendation",
                sections
            )

            reason = extract_section(
                result,
                "Reason",
                sections
            )

            confidence = extract_section(
                result,
                "Confidence",
                sections
            )


            # =================================================
            # CLEAN
            # =================================================

            pattern_detected = clean_ai_text(
                pattern_detected
            )

            customer_pattern = clean_ai_text(
                customer_pattern
            )

            product_pattern = clean_ai_text(
                product_pattern
            )

            category_pattern = clean_ai_text(
                category_pattern
            )

            recommendation = clean_ai_text(
                recommendation
            )

            confidence = clean_ai_text(
                confidence
            )


            # =================================================
            # CREATE HUMAN-FRIENDLY TEXT
            # =================================================

            customer_display = make_customer_card(
                customer_pattern
            )

            product_display = make_product_card(
                product_pattern
            )

            category_display = make_category_card(
                category_pattern
            )


            pattern_display = shorten_text(
                pattern_detected,
                300
            )


            recommendation_display = shorten_text(
                recommendation,
                340
            )


            confidence_display = shorten_text(
                confidence,
                110
            )


            # =================================================
            # ESCAPE HTML
            # =================================================

            pattern_display = html.escape(
                pattern_display
            )

            customer_display = html.escape(
                customer_display
            )

            product_display = html.escape(
                product_display
            )

            category_display = html.escape(
                category_display
            )

            recommendation_display = html.escape(
                recommendation_display
            )

            confidence_display = html.escape(
                confidence_display
            )


            # =================================================
            # ANALYSIS HEADER
            # =================================================

            render_html(
                """
                <div class="analysis-header">
                    ✦ AI MEMORY ANALYSIS
                </div>

                <div class="analysis-title">
                    What ReturnSense learned
                </div>
                """
            )


            # =================================================
            # MAIN PATTERN
            # =================================================

            render_html(
                f"""
                <div class="main-pattern">

                    <div class="main-pattern-label">
                        The big picture
                    </div>

                    <div class="main-pattern-text">
                        {pattern_display}
                    </div>

                </div>
                """
            )


            st.markdown(
                "<div style='height:13px'></div>",
                unsafe_allow_html=True
            )


            # =================================================
            # FLASH CARD TITLE
            # =================================================

            render_html(
                """
                <div class="section-caption">
                    What we learned from past returns
                </div>
                """
            )


            # =================================================
            # FLASH CARDS
            # =================================================

            c1, c2, c3 = st.columns(
                3,
                gap="medium"
            )


            # -------------------------------------------------
            # CUSTOMER
            # -------------------------------------------------

            with c1:

                render_html(
                    f"""
                    <div class="flash-card">

                        <div class="flash-card-top">

                            <div class="flash-icon">
                                👤
                            </div>

                            <div class="flash-label">
                                Customer
                            </div>

                        </div>


                        <div class="flash-headline">
                            Customer history
                        </div>


                        <div class="flash-description">
                            {customer_display}
                        </div>

                    </div>
                    """
                )


            # -------------------------------------------------
            # PRODUCT
            # -------------------------------------------------

            with c2:

                render_html(
                    f"""
                    <div class="flash-card">

                        <div class="flash-card-top">

                            <div class="flash-icon">
                                📦
                            </div>

                            <div class="flash-label">
                                Product
                            </div>

                        </div>


                        <div class="flash-headline">
                            What happened to this product?
                        </div>


                        <div class="flash-description">
                            {product_display}
                        </div>

                    </div>
                    """
                )


            # -------------------------------------------------
            # CATEGORY
            # -------------------------------------------------

            with c3:

                render_html(
                    f"""
                    <div class="flash-card">

                        <div class="flash-card-top">

                            <div class="flash-icon">
                                🏷️
                            </div>

                            <div class="flash-label">
                                Category
                            </div>

                        </div>


                        <div class="flash-headline">
                            Is this happening elsewhere?
                        </div>


                        <div class="flash-description">
                            {category_display}
                        </div>

                    </div>
                    """
                )


            st.markdown(
                "<div style='height:13px'></div>",
                unsafe_allow_html=True
            )


            # =================================================
            # RECOMMENDATION
            # =================================================

            r1, r2 = st.columns(
                [1.5, 0.5],
                gap="medium"
            )


            with r1:

                render_html(
                    f"""
                    <div class="recommendation-box">

                        <div class="recommendation-top">

                            <span style="
                                font-size:1rem;
                            ">
                                💡
                            </span>

                            <div class="recommendation-label">
                                What the business can do
                            </div>

                        </div>


                        <div class="recommendation-text">
                            {recommendation_display}
                        </div>

                    </div>
                    """
                )


            with r2:

                render_html(
                    f"""
                    <div class="confidence-box">

                        <div class="confidence-label">
                            Confidence
                        </div>

                        <div class="confidence-value">
                            {confidence_display}
                        </div>

                    </div>
                    """
                )


            st.markdown(
                "<div style='height:10px'></div>",
                unsafe_allow_html=True
            )


            # =================================================
            # EVIDENCE
            # =================================================

            with st.expander(
                "🔎  View evidence used by the agent"
            ):

                formatted_evidence = format_evidence(
                    evidence
                )

                st.markdown(
                    formatted_evidence
                )

                st.caption(
                    "Evidence is based on the selected return "
                    "and memories retrieved from Hindsight."
                )


            # =================================================
            # WHY
            # =================================================

            with st.expander(
                "💡  Why did ReturnSense recommend this?"
            ):

                st.write(
                    clean_ai_text(reason)
                )


        except Exception as error:

            st.error(
                f"Analysis failed: {error}"
            )


# ============================================================
# FOOTER
# ============================================================

render_html(
    """
    <div style="
        text-align:center;
        color:#5F5868;
        font-size:0.63rem;
        padding-top:10px;
    ">
        ReturnSense
        &nbsp;•&nbsp;
        Hindsight-powered AI memory
        &nbsp;•&nbsp;
        Every return teaches the next decision.
    </div>
    """
)