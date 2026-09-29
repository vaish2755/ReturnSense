import html

def get_header_html():
    return """
    <div class="top-header">
        <div class="brand">
            <div class="brand-icon">↩</div>
            <div>
                <div class="brand-name">Return<span>Sense</span></div>
                <div class="brand-subtitle">Autonomous Return Intelligence & Prevention</div>
            </div>
        </div>
        <div class="memory-status">
            <span class="status-dot"></span>
            Hindsight Memory Connected
        </div>
    </div>
    """

def get_home_hero_html():
    return """
    <!-- HERO SECTION -->
    <div style="padding: 20px 10px 30px; text-align: left; border-bottom: 1px solid #27272a; margin-bottom: 35px;">
        <div style="display: inline-block; padding: 4px 12px; background: #27272a; border-radius: 6px; color: #60a5fa; font-size: 0.78rem; font-weight: 700; letter-spacing: 0.6px; margin-bottom: 14px;">
            AI MEMORY FOR E-COMMERCE RETURNS
        </div>
        <h1 style="font-size: 2.7rem; font-weight: 900; line-height: 1.15; margin-bottom: 16px; color: #ffffff;">
            Stop Treating Every Return <br>Like It's the First Time.
        </h1>
        <p style="font-size: 1.05rem; line-height: 1.65; color: #d4d4d8; max-width: 820px; margin-bottom: 25px;">
            In traditional e-commerce, returns are processed as disconnected transactions. When a customer sends an item back, standard refund systems don't remember if that specific customer regularly returns items after weekend events, if that shoe SKU consistently runs a half-size too small, or if a supplier batch has defect complaints.
        </p>
        <p style="font-size: 1.05rem; line-height: 1.65; color: #d4d4d8; max-width: 820px;">
            <strong>ReturnSense connects the dots.</strong> By pairing an autonomous reasoning agent with persistent long-term memory, ReturnSense evaluates past behaviors across customers, products, and categories to make informed decisions that protect your profit margins and reduce unnecessary shipping waste.
        </p>
    </div>

    <!-- HOW IT WORKS (3-STEP PIPELINE) -->
    <div style="margin-bottom: 40px;">
        <div style="color: #60a5fa; font-size: 0.75rem; font-weight: 800; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 6px;">
            SYSTEM WORKFLOW
        </div>
        <h2 style="font-size: 1.6rem; font-weight: 800; margin-bottom: 22px; color: #ffffff;">
            How ReturnSense Analyzes a Claim
        </h2>

        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px;">
            <div class="card" style="padding: 24px;">
                <div style="font-size: 1.7rem; margin-bottom: 12px; font-weight: 800; color: #60a5fa;">01</div>
                <div class="card-heading" style="margin-bottom: 10px;">Return Request Ingested</div>
                <p style="font-size: 0.88rem; line-height: 1.6; color: #a1a1aa;">
                    When a return request is submitted, ReturnSense pulls order attributes including the return reason, order value, processing costs, and logistics transit window.
                </p>
            </div>

            <div class="card" style="padding: 24px;">
                <div style="font-size: 1.7rem; margin-bottom: 12px; font-weight: 800; color: #60a5fa;">02</div>
                <div class="card-heading" style="margin-bottom: 10px;">Memory Recall via Hindsight</div>
                <p style="font-size: 0.88rem; line-height: 1.6; color: #a1a1aa;">
                    The system queries Hindsight's vector memory bank to recall past interactions: Has this customer filed similar claims before? Has this product batch been returned by others for the same issue?
                </p>
            </div>

            <div class="card" style="padding: 24px;">
                <div style="font-size: 1.7rem; margin-bottom: 12px; font-weight: 800; color: #60a5fa;">03</div>
                <div class="card-heading" style="margin-bottom: 10px;">Actionable Recommendation</div>
                <p style="font-size: 0.88rem; line-height: 1.6; color: #a1a1aa;">
                    The AI agent weighs financial impact, return legitimacy, and environmental footprint to deliver an immediate recommendation (e.g., instant replacement, inspection flag, or sizing guide update).
                </p>
            </div>
        </div>
    </div>

    <!-- CORE BUSINESS IMPACTS -->
    <div style="margin-bottom: 40px;">
        <div style="color: #60a5fa; font-size: 0.75rem; font-weight: 800; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 6px;">
            THE VALUE
        </div>
        <h2 style="font-size: 1.6rem; font-weight: 800; margin-bottom: 22px; color: #ffffff;">
            Why E-Commerce Teams Use It
        </h2>

        <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px;">
            <div class="card" style="padding: 22px;">
                <div style="font-size: 1.3rem; margin-bottom: 8px;">🛡️</div>
                <div class="card-heading" style="font-size: 1.05rem; margin-bottom: 6px;">Detect Serial Abusers & Fraud</div>
                <p style="font-size: 0.86rem; line-height: 1.6; color: #a1a1aa;">
                    Identify patterns like "wardrobing" (buying clothes to wear once and return) or fraudulent damage claims without putting genuine first-time customers through painful refund friction.
                </p>
            </div>

            <div class="card" style="padding: 22px;">
                <div style="font-size: 1.3rem; margin-bottom: 8px;">🌱</div>
                <div class="card-heading" style="font-size: 1.05rem; margin-bottom: 6px;">Quantify Environmental Waste</div>
                <p style="font-size: 0.86rem; line-height: 1.6; color: #a1a1aa;">
                    Every return has an ecological cost. ReturnSense measures carbon emissions and packaging waste generated per return, empowering brands to offer sustainable keep-and-refund incentives where shipping costs exceed product value.
                </p>
            </div>
        </div>
    </div>
    """

def get_metric_html(value, label):
    return f"""
    <div class="metric-card">
        <div class="metric-value">{value}</div>
        <div class="metric-label">{label}</div>
    </div>
    """

def get_return_card_header():
    return """
    <div class="card">
        <div class="card-title">Return Analysis</div>
        <div class="card-heading">Select a return to investigate</div>
    </div>
    """

def get_return_details_html(row):
    return f"""
    <div class="card">
        <div class="return-row">
            <span class="return-label">Return ID</span>
            <span class="return-value">{html.escape(str(row["Order_ID"]))}</span>
        </div>
        <div class="return-row">
            <span class="return-label">Customer</span>
            <span class="return-value">{html.escape(str(row["User_ID"]))}</span>
        </div>
        <div class="return-row">
            <span class="return-label">Product</span>
            <span class="return-value">{html.escape(str(row["Product_ID"]))}</span>
        </div>
        <div class="return-row">
            <span class="return-label">Category</span>
            <span class="return-value">{html.escape(str(row["Product_Category"]))}</span>
        </div>
        <div class="return-row">
            <span class="return-label">Return Reason</span>
            <span class="reason-badge">{html.escape(str(row["Return_Reason"]))}</span>
        </div>
        <div class="return-row">
            <span class="return-label">Order Value</span>
            <span class="return-value">₹{row["Order_Value"]:,.2f}</span>
        </div>
    </div>
    """

def get_memory_card_html():
    return """
    <div class="card">
        <div class="card-title">Long-Term Memory</div>
        <div class="card-heading">🧠 Hindsight Engine</div>
        <div style="height:7px"></div>
        <div class="memory-number">5,889</div>
        <div class="memory-text">Total contextual memories stored</div>
        <div class="memory-line">
            <div class="memory-label">Customer Memory</div>
            <div class="memory-value">Historical purchase and return trends per user</div>
        </div>
        <div class="memory-line">
            <div class="memory-label">Product Memory</div>
            <div class="memory-value">Recurring defects, sizing issues, or batch failures</div>
        </div>
        <div class="memory-line">
            <div class="memory-label">Outcome Memory</div>
            <div class="memory-value">Prior agent recommendations and resolution effectiveness</div>
        </div>
    </div>
    """

def get_flash_card_html(icon, label, headline, desc):
    return f"""
    <div class="flash-card">
        <div class="flash-card-top">
            <div class="flash-icon">{icon}</div>
            <div class="flash-label">{label}</div>
        </div>
        <div class="flash-headline">{headline}</div>
        <div class="flash-description">{desc}</div>
    </div>
    """

def get_footer_html():
    return """
    <div style="text-align:center; color:#71717a; font-size:0.75rem; padding-top:25px; border-top:1px solid #27272a; margin-top:30px;">
        ReturnSense • Powered by Hindsight AI Memory • Every return teaches the next decision.
    </div>
    """