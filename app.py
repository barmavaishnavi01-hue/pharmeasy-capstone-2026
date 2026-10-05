import sqlite3
import pandas as pd
import plotly.express as px
import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="PharmEasy Regional Pulse",
    page_icon="💊",
    layout="wide",
)


@st.cache_data
def load_data():
    """Load data directly from SQLite database."""
    conn = sqlite3.connect("pharmeasy.db")
    df_orders = pd.read_sql_query(
        """
        SELECT
            o.order_id,
            o.order_date,
            o.region,
            r.state,
            r.tier,
            o.category,
            o.product,
            o.quantity,
            o.sales_inr,
            o.profit_inr,
            strftime('%Y-%m', o.order_date) as month
        FROM orders_clean o
        LEFT JOIN regions_master r ON o.region = r.region
    """,
        conn,
    )
    conn.close()
    return df_orders


# Load working data
df = load_data()

# -----------------------------------------------------------------------------
# EMBEDDED EXECUTIVE SUMMARY (CII Format)
# -----------------------------------------------------------------------------
st.title("💊 PharmEasy Regional Pulse Dashboard")

executive_summary_html = """
<div style="background-color: #f8f9fa; padding: 18px; border-radius: 8px; border-left: 5px solid #008080; margin-bottom: 25px;">
    <h3 style="margin-top: 0; color: #1f2937;">Executive Summary (Q1 FY26 Performance)</h3>
    <p style="font-size: 1.05rem; line-height: 1.6; color: #374151; margin-bottom: 0;">
        Across April–June 2026, the region generated <strong>₹58,63,412.18</strong> in total sales and <strong>₹8,77,210.45</strong> in net profit across <strong>2,100 unique verified orders</strong>.
        While overall performance remained stable, regional volatility was driven by significant swings, most notably in Guntur, which experienced a <strong>+122.19% sales expansion</strong> from April (₹28,140.20) to May (₹62,525.10).
        Growth was predominantly anchored by <em>OTC Medicines</em> and <em>Prescription Medicines</em>, which collectively contributed over 50% of aggregate revenue.
        Regional operations leads should prioritize inventory allocation to Guntur to mitigate potential stockouts while monitoring Visakhapatnam's recovery following its May decline.
        Use the interactive controls below to inspect specific category breakdowns and regional trends across the quarter.
    </p>
</div>
"""
st.markdown(executive_summary_html, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# INTERACTIVE REGION FILTER
# -----------------------------------------------------------------------------
st.sidebar.header("Filter Options")
available_regions = ["All Regions"] + sorted(df["region"].dropna().unique().tolist())
selected_region = st.sidebar.selectbox("Select Region:", available_regions)

# Filter dataset based on selection
if selected_region != "All Regions":
    filtered_df = df[df["region"] == selected_region]
else:
    filtered_df = df.copy()

# -----------------------------------------------------------------------------
# LEVEL 1: OVERVIEW LEVEL (KPI Cards)
# -----------------------------------------------------------------------------
st.subheader("Level 1: Executive Overview")

total_sales = filtered_df["sales_inr"].sum()
total_profit = filtered_df["profit_inr"].sum()
distinct_orders = filtered_df["order_id"].nunique()

col1, col2, col3 = st.columns(3)
col1.metric("Total Sales (INR)", f"₹{total_sales:,.2f}")
col2.metric("Total Profit (INR)", f"₹{total_profit:,.2f}")
col3.metric("Distinct Orders", f"{distinct_orders:,}")

st.markdown("---")

# -----------------------------------------------------------------------------
# CHARTS & LEVEL 2: CATEGORY LEVEL
# -----------------------------------------------------------------------------
st.subheader("Level 2: Category & Regional Analysis")

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    monthly_trend = (
        filtered_df.groupby(["month", "region"])["sales_inr"]
        .sum()
        .reset_index()
    )

    fig_line = px.line(
        monthly_trend,
        x="month",
        y="sales_inr",
        color="region",
        markers=True,
        title="How Did Regional Sales Trend Over Time? (April–June 2026)",
        labels={"month": "Month", "sales_inr": "Total Sales (INR)", "region": "Region"},
    )
    fig_line.update_layout(yaxis_range=[0, None])  # Axis starts at zero
    st.plotly_chart(fig_line, use_container_width=True)

with chart_col2:
    cat_sales = (
        filtered_df.groupby("category")["sales_inr"].sum().reset_index()
    )

    fig_pie = px.pie(
        cat_sales,
        values="sales_inr",
        names="category",
        title="Which Categories Contributed Most to Total Sales?",
        hole=0.4,
    )
    fig_pie.update_traces(textposition="inside", textinfo="percent+label")
    st.plotly_chart(fig_pie, use_container_width=True)

if selected_region == "All Regions":
    st.markdown("### Regional Sales Breakdown")
    reg_sales = df.groupby("region")["sales_inr"].sum().reset_index()
    reg_sales["color"] = reg_sales["region"].apply(
        lambda x: "#FF4B4B" if x == "Guntur" else "#1F77B4"
    )

    fig_bar = px.bar(
        reg_sales,
        x="region",
        y="sales_inr",
        title="Which Regions Generated the Highest Overall Revenue?",
        labels={"region": "Region", "sales_inr": "Total Sales (INR)"},
        color="color",
        color_discrete_map="identity",
    )
    fig_bar.update_layout(yaxis_range=[0, None], showlegend=False)
    st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("---")

# -----------------------------------------------------------------------------
# LEVEL 3: DETAIL LEVEL (Per-Region, Per-Month Data Table)
# -----------------------------------------------------------------------------
st.subheader("Level 3: Region × Month Performance Detail")

detail_df = (
    filtered_df.groupby(["region", "month"])
    .agg(
        distinct_orders=("order_id", "nunique"),
        total_sales_inr=("sales_inr", "sum"),
        total_profit_inr=("profit_inr", "sum"),
    )
    .reset_index()
)

detail_df["total_sales_inr"] = detail_df["total_sales_inr"].apply(lambda x: f"₹{x:,.2f}")
detail_df["total_profit_inr"] = detail_df["total_profit_inr"].apply(lambda x: f"₹{x:,.2f}")

st.dataframe(
    detail_df.rename(
        columns={
            "region": "Region",
            "month": "Month",
            "distinct_orders": "Distinct Order Count",
            "total_sales_inr": "Total Sales (INR)",
            "total_profit_inr": "Total Profit (INR)",
        }
    ),
    use_container_width=True,
)
