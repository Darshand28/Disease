import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="Testing Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------
st.markdown("""
<style>
.main {
    background-color: #0E1117;
    color: white;
}

h1, h2, h3 {
    color: #4FC3F7;
}

.stMetric {
    background-color: #1E1E1E;
    padding: 15px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------
st.title("📊 Testing Analytics Dashboard")

st.markdown("""
Interactive analytics dashboard with charts, KPIs,
deep insights, and modern Streamlit UI.
""")

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------
df = pd.read_csv("data/Testing.csv")

# ---------------------------------------------------
# SHOW DATA
# ---------------------------------------------------
st.subheader("📋 Dataset Preview")
st.dataframe(df.head(), use_container_width=True)

# ---------------------------------------------------
# COLUMN SELECTION
# ---------------------------------------------------
numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns

if len(numeric_cols) < 1:
    st.error("No numeric columns found in dataset.")
    st.stop()

selected_col = st.selectbox(
    "Select Numeric Column for Analysis",
    numeric_cols
)

# ---------------------------------------------------
# KPI SECTION
# ---------------------------------------------------
total = df[selected_col].sum()
average = df[selected_col].mean()
maximum = df[selected_col].max()
minimum = df[selected_col].min()

c1, c2, c3, c4 = st.columns(4)

c1.metric("📈 Total", f"{total:,.2f}")
c2.metric("📊 Average", f"{average:,.2f}")
c3.metric("⬆️ Maximum", f"{maximum:,.2f}")
c4.metric("⬇️ Minimum", f"{minimum:,.2f}")

st.divider()

# ---------------------------------------------------
# LINE CHART
# ---------------------------------------------------
fig1 = px.line(
    df,
    y=selected_col,
    title=f"{selected_col} Trend Analysis"
)

st.plotly_chart(fig1, use_container_width=True)

# ---------------------------------------------------
# BAR CHART
# ---------------------------------------------------
fig2 = px.bar(
    df,
    y=selected_col,
    title=f"{selected_col} Distribution"
)

st.plotly_chart(fig2, use_container_width=True)

# ---------------------------------------------------
# HISTOGRAM
# ---------------------------------------------------
fig3 = px.histogram(
    df,
    x=selected_col,
    nbins=20,
    title=f"{selected_col} Histogram"
)

st.plotly_chart(fig3, use_container_width=True)

# ---------------------------------------------------
# PIE CHART
# ---------------------------------------------------
if len(df.columns) > 1:

    category_cols = df.select_dtypes(include=['object']).columns

    if len(category_cols) > 0:

        cat_col = category_cols[0]

        pie_data = df.groupby(cat_col)[selected_col].sum().reset_index()

        fig4 = px.pie(
            pie_data,
            names=cat_col,
            values=selected_col,
            title=f"{selected_col} by {cat_col}"
        )

        st.plotly_chart(fig4, use_container_width=True)

# ---------------------------------------------------
# INSIGHTS
# ---------------------------------------------------
st.subheader("🧠 AI Insights")

st.success(
    f"The average value of {selected_col} is {average:,.2f}."
)

if average > (maximum * 0.6):
    st.info(
        "The dataset shows consistently high values."
    )
else:
    st.warning(
        "The dataset contains high variation in values."
    )

# ---------------------------------------------------
# CORRELATION HEATMAP
# ---------------------------------------------------
if len(numeric_cols) > 1:

    st.subheader("🔥 Correlation Heatmap")

    corr = df[numeric_cols].corr()

    fig5 = px.imshow(
        corr,
        text_auto=True,
        aspect="auto",
        title="Correlation Matrix"
    )

    st.plotly_chart(fig5, use_container_width=True)

# ---------------------------------------------------
# DOWNLOAD DATA
# ---------------------------------------------------
csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇️ Download Dataset",
    data=csv,
    file_name="Testing.csv",
    mime="text/csv"
)

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------
st.markdown("---")
st.markdown("Built using Streamlit, Plotly, Pandas")
