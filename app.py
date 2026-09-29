import os
import re
import html
import pandas as pd
import streamlit as st

from agent.agent import analyze_return
import templates

# ============================================================
# PAGE CONFIG & ROUTING
# ============================================================
st.set_page_config(
    page_title="ReturnSense",
    page_icon="↩️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Initialize page state
if "page" not in st.session_state:
    st.session_state.page = "home"

def set_page(page_name):
    st.session_state.page = page_name
    st.rerun()

# Load external CSS file
def load_css(file_path="styles.css"):
    if os.path.exists(file_path):
        with open(file_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# ============================================================
# AI TEXT CLEANING & EXTRACTION
# ============================================================
def clean_ai_text(text):
    if not text:
        return ""
    text = str(text)
    text = text.replace("**", "").replace("__", "").replace("`", "")
    text = re.sub(r"^\s*#+\s*", "", text, flags=re.MULTILINE)
    text = re.sub(r"\n\s*\n+", "\n", text)
    return text.strip()

def extract_section(text, section_name, all_sections):
    text = clean_ai_text(text)
    target_match = re.search(rf"{re.escape(section_name)}\s*:", text, re.IGNORECASE)
    if not target_match:
        return "No clear information found."
    
    start = target_match.end()
    next_positions = []
    
    for section in all_sections:
        if section.lower() == section_name.lower():
            continue
        match = re.search(rf"{re.escape(section)}\s*:", text[start:], re.IGNORECASE)
        if match:
            next_positions.append(start + match.start())
            
    end = min(next_positions) if next_positions else len(text)
    value = re.sub(r"^[\s:\-–—]+", "", text[start:end].strip()).strip()
    return value if value else "No clear information found."

def shorten_text(text, max_length=300):
    text = clean_ai_text(text)
    if len(text) <= max_length:
        return text
    return text[:max_length].rsplit(" ", 1)[0] + "..."

def format_evidence(text):
    text = clean_ai_text(text)
    text = re.sub(r"\s+(\d+\.)\s+", r"\n\n\1 ", text)
    text = re.sub(r"\s+(Return Memory\s+\d+)", r"\n\1", text, flags=re.IGNORECASE)
    return text.strip()

def make_customer_card(text):
    text = clean_ai_text(text)
    lower = text.lower()
    if "no clear pattern" in lower or "no previous" in lower or "only this" in lower:
        return "No repeated return pattern was found for this customer."
    text = re.sub(r"has made two distinct return orders", "has returned products before", text, flags=re.IGNORECASE)
    text = re.sub(r"has made (\d+) distinct return orders", r"has returned products \1 times", text, flags=re.IGNORECASE)
    text = re.sub(r"distinct return orders", "previous returns", text, flags=re.IGNORECASE)
    text = re.sub(r"return orders", "returns", text, flags=re.IGNORECASE)
    return shorten_text(text, 210)

def make_product_card(text):
    text = clean_ai_text(text)
    lower = text.lower()
    if "no clear pattern" in lower or "no previous" in lower:
        return "No repeated return pattern was found for this product."
    text = re.sub(r"has been returned in at least two separate orders", "has been returned more than once", text, flags=re.IGNORECASE)
    text = re.sub(r"has been returned in two separate orders", "has been returned more than once", text, flags=re.IGNORECASE)
    text = re.sub(r"has been returned in (\d+) separate orders", r"has been returned \1 times", text, flags=re.IGNORECASE)
    text = re.sub(r"distinct return orders", "previous returns", text, flags=re.IGNORECASE)
    return shorten_text(text, 220)

def make_category_card(text):
    text = clean_ai_text(text)
    lower = text.lower()
    if "no clear pattern" in lower or "no category" in lower:
        return "No strong category-wide return pattern was found."
    text = re.sub(r"category-wide", "across this category", text, flags=re.IGNORECASE)
    text = re.sub(r"recurring", "repeated", text, flags=re.IGNORECASE)
    text = re.sub(r"SKUs", "products", text, flags=re.IGNORECASE)
    text = re.sub(r"sku", "product", text, flags=re.IGNORECASE)
    return shorten_text(text, 220)

# ============================================================
# LOAD DATA
# ============================================================
@st.cache_data
def load_data():
    return pd.read_csv("data/returns_sustainability_dataset.csv")

df = load_data()
returned_df = df[df["Return_Status"] == "Returned"].copy()

# ============================================================
# HEADER & TOP NAVIGATION
# ============================================================
st.html(templates.get_header_html())

nav_left, nav_right = st.columns([7.5, 2.5])
with nav_right:
    if st.session_state.page == "home":
        if st.button("🚀 Enter Console", use_container_width=True):
            set_page("process")
    else:
        if st.button("← Back to Overview", use_container_width=True):
            set_page("home")

# ============================================================
# PAGE 1: HOME / OVERVIEW
# ============================================================
if st.session_state.page == "home":
    st.html(templates.get_home_hero_html())

    cta_col1, cta_col2, cta_col3 = st.columns([1, 2, 1])
    with cta_col2:
        if st.button("✨ Launch Return Analysis Console", use_container_width=True):
            set_page("process")

# ============================================================
# PAGE 2: PROCESS / INVESTIGATION CONSOLE
# ============================================================
elif st.session_state.page == "process":
    # 1. Summary Metrics
    total_orders = len(df)
    returned_orders = len(returned_df)
    unique_customers = df["User_ID"].nunique()
    return_rate = (returned_orders / total_orders) * 100

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.html(templates.get_metric_html(f"{total_orders:,}", "Total Orders"))
    with m2:
        st.html(templates.get_metric_html(f"{returned_orders:,}", "Returned Orders"))
    with m3:
        st.html(templates.get_metric_html(f"{unique_customers:,}", "Customers"))
    with m4:
        st.html(templates.get_metric_html(f"{return_rate:.1f}%", "Return Rate"))

    st.write("")

    # 2. Main Two-Column Layout (Selection & Memory)
    left, right = st.columns([1.05, 0.95], gap="medium")

    with left:
        st.html(templates.get_return_card_header())
        
        order_ids = returned_df["Order_ID"].tolist()

        def format_return(order_id):
            selected_row = returned_df[returned_df["Order_ID"] == order_id].iloc[0]
            return f"{selected_row['Order_ID']}  •  {selected_row['Return_Reason']}  •  {selected_row['Product_Category']}"

        selected_order = st.selectbox(
            "Select a return",
            order_ids,
            format_func=format_return,
            label_visibility="collapsed"
        )

        row = returned_df[returned_df["Order_ID"] == selected_order].iloc[0]

        st.html(templates.get_return_details_html(row))
        
        st.write("")
        analyze_clicked = st.button("✨  ANALYZE THIS RETURN", use_container_width=True)

    with right:
        st.html(templates.get_memory_card_html())

    # 3. AI Analysis Results
    if analyze_clicked:
        return_data = {
            "order_id": row["Order_ID"],
            "customer_id": row["User_ID"],
            "product_id": row["Product_ID"],
            "category": row["Product_Category"],
            "order_date": row["Order_Date"],
            "return_reason": row["Return_Reason"],
            "days_to_return": row["Days_to_Return"],
            "order_value": row["Order_Value"],
            "return_cost": row["Return_Cost"],
            "profit_loss": row["Profit_Loss"],
            "co2_emissions": row["CO2_Emissions"],
            "packaging_waste": row["Packaging_Waste"],
        }

        with st.spinner("🧠 Recalling Hindsight memories and analyzing..."):
            try:
                result = analyze_return(return_data)

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

                pattern_detected = extract_section(result, "Pattern Detected", sections)
                customer_pattern = extract_section(result, "Customer Pattern", sections)
                product_pattern = extract_section(result, "Product Pattern", sections)
                category_pattern = extract_section(result, "Category Pattern", sections)
                evidence = extract_section(result, "Evidence", sections)
                recommendation = extract_section(result, "Recommendation", sections)
                reason = extract_section(result, "Reason", sections)
                confidence = extract_section(result, "Confidence", sections)

                customer_display = make_customer_card(customer_pattern)
                product_display = make_product_card(product_pattern)
                category_display = make_category_card(category_pattern)

                pattern_display = shorten_text(pattern_detected, 300)
                recommendation_display = shorten_text(recommendation, 340)
                confidence_display = shorten_text(confidence, 110)

                st.html("""
                    <div class="analysis-header">✦ AI MEMORY ANALYSIS</div>
                    <div class="analysis-title">What ReturnSense learned</div>
                """)

                st.html(f"""
                    <div class="main-pattern">
                        <div class="main-pattern-label">The big picture</div>
                        <div class="main-pattern-text">{html.escape(pattern_display)}</div>
                    </div>
                """)

                st.write("")
                c1, c2, c3 = st.columns(3, gap="medium")
                with c1:
                    st.html(templates.get_flash_card_html("👤", "Customer", "Customer History", html.escape(customer_display)))
                with c2:
                    st.html(templates.get_flash_card_html("📦", "Product", "Product Recurrence", html.escape(product_display)))
                with c3:
                    st.html(templates.get_flash_card_html("🏷️", "Category", "Category Patterns", html.escape(category_display)))

                st.write("")
                r1, r2 = st.columns([1.5, 0.5], gap="medium")
                with r1:
                    st.html(f"""
                        <div class="recommendation-box">
                            <div class="recommendation-top">
                                <span style="font-size:1.1rem;">💡</span>
                                <div class="recommendation-label">What the business can do</div>
                            </div>
                            <div class="recommendation-text">{html.escape(recommendation_display)}</div>
                        </div>
                    """)
                with r2:
                    st.html(f"""
                        <div class="confidence-box">
                            <div class="confidence-label">Confidence</div>
                            <div class="confidence-value">{html.escape(confidence_display)}</div>
                        </div>
                    """)

                st.write("")
                with st.expander("🔎  View evidence used by the agent"):
                    st.markdown(format_evidence(evidence))
                    st.caption("Evidence is based on the selected return and memories retrieved from Hindsight.")

                with st.expander("💡  Why did ReturnSense recommend this?"):
                    st.write(clean_ai_text(reason))

            except Exception as error:
                st.error(f"Analysis failed: {error}")

# ============================================================
# FOOTER
# ============================================================
st.html(templates.get_footer_html())