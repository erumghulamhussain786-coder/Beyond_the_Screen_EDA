
import streamlit as st
import pandas as pd
import plotly.express as px

# Dashboard title
st.title("Beyond the Screen")

# Dashboard description
st.write(
    "An analysis of late-night phone habits, "
    "sleep quality and daily fatigue."
)

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("data/bedtime_screentime_sleep_debt.csv")
    return df

# Store dataset

# Load original dataset
data = load_data()

# Dashboard Filters
st.sidebar.title("Dashboard Filters")

# Filter 1: Occupation Type
selected_occupation = st.sidebar.multiselect(
    "Select Occupation Type",
    options=sorted(data["occupation_type"].unique()),
    default=sorted(data["occupation_type"].unique())
)

# Filter 2: Sleep Debt Category
selected_sleep_debt = st.sidebar.multiselect(
    "Select Sleep Debt Category",
    options=sorted(data["sleep_debt_category"].unique()),
    default=sorted(data["sleep_debt_category"].unique())
)

# Apply filters
df = data[
    (data["occupation_type"].isin(selected_occupation)) &
    (data["sleep_debt_category"].isin(selected_sleep_debt))
]


# Display dataset information
st.subheader("Dataset Overview")

st.write("Total Records:", df.shape[0])
st.write("Total Columns:", df.shape[1])

# Display first five rows
st.write("Preview of Dataset")
st.dataframe(df.head())

# KPI Section
st.subheader("Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Records", df.shape[0])

with col2:
    st.metric(
        "Avg. Phone Usage",
        f"{df['bedtime_phone_minutes'].mean():.2f} min"
    )

with col3:
    st.metric(
        "Avg. Sleep Duration",
        f"{df['total_sleep_hours'].mean():.2f} hrs"
    )

with col4:
    st.metric(
        "Avg. Fatigue Score",
        f"{df['next_day_fatigue_score'].mean():.2f}"
    )


# Graph 1: Professional Bedtime Phone Usage Distribution

st.subheader("1. Bedtime Phone Usage Distribution")

# Calculate median phone usage
median_usage = df["bedtime_phone_minutes"].median()

# Create histogram
fig1 = px.histogram(
    df,
    x="bedtime_phone_minutes",
    nbins=25,
    title="How Much Time Do Users Spend on Their Phones Before Bed?",
    labels={
        "bedtime_phone_minutes": "Bedtime Phone Usage (Minutes)",
        "count": "Number of Users"
    },
    color_discrete_sequence=["#3977D5"],
    opacity=0.85
)

# Add median reference line
fig1.add_vline(
    x=median_usage,
    line_dash="dash",
    line_color="#E67E22",
    annotation_text=f"Median: {median_usage:.0f} min",
    annotation_position="top"
)

# Improve graph layout
fig1.update_layout(
    template="plotly_white",
    height=480,
    title_font_size=19,
    title_x=0.02,
    font=dict(
        family="Arial",
        size=13,
        color="#263445"
    ),
    margin=dict(l=45, r=30, t=85, b=55),
    bargap=0.08,
    showlegend=False
)

# Improve axes
fig1.update_xaxes(
    showgrid=False,
    zeroline=False
)

fig1.update_yaxes(
    showgrid=True,
    gridcolor="#EAECEF",
    zeroline=False
)

# Display graph
st.plotly_chart(fig1, use_container_width=True)

# Graph 2: Most Commonly Used Bedtime Apps

st.subheader("2. Most Commonly Used Bedtime Apps")

# Count the records for each app
app_counts = (
    df["primary_bedtime_app"]
    .value_counts()
    .sort_values(ascending=True)
    .reset_index()
)

app_counts.columns = ["App", "Number of Users"]

# Create horizontal bar chart
fig2 = px.bar(
    app_counts,
    x="Number of Users",
    y="App",
    orientation="h",
    title="Which Apps Are Most Popular Before Bedtime?",
    text="Number of Users",
    color_discrete_sequence=["#3977D5"]
)

# Improve graph appearance
fig2.update_layout(
    template="plotly_white",
    height=430,
    title_font_size=19,
    title_x=0.02,
    font=dict(
        family="Arial",
        size=13,
        color="#263445"
    ),
    margin=dict(l=30, r=40, t=80, b=45),
    showlegend=False
)

# Format bars and labels
fig2.update_traces(
    textposition="outside",
    marker_line_width=0
)

fig2.update_xaxes(
    title="Number of Users",
    showgrid=True,
    gridcolor="#EAECEF"
)

fig2.update_yaxes(
    title="Bedtime App Category",
    showgrid=False
)

# Display graph
st.plotly_chart(fig2, use_container_width=True)

# Graph 3: Phone Usage vs Sleep Duration

st.subheader("3. Phone Usage vs. Sleep Duration")

fig3 = px.scatter(
    df,
    x="bedtime_phone_minutes",
    y="total_sleep_hours",
    title="Relationship Between Bedtime Phone Usage and Sleep Duration",
    labels={
        "bedtime_phone_minutes": "Bedtime Phone Usage (Minutes)",
        "total_sleep_hours": "Total Sleep Duration (Hours)"
    },
    color_discrete_sequence=["#3977D5"],
    opacity=0.55
)

fig3.update_layout(
    template="plotly_white",
    height=480,
    title_font_size=19,
    title_x=0.02,
    font=dict(
        family="Arial",
        size=13,
        color="#263445"
    ),
    margin=dict(l=45, r=30, t=85, b=55)
)

fig3.update_traces(
    marker=dict(size=7)
)

fig3.update_xaxes(
    showgrid=False,
    zeroline=False
)

fig3.update_yaxes(
    showgrid=True,
    gridcolor="#EAECEF",
    zeroline=False
)

st.plotly_chart(fig3, use_container_width=True)

# Graph 4: Phone Usage vs Next-Day Fatigue

st.subheader("4. Phone Usage vs. Next-Day Fatigue")

fig4 = px.scatter(
    df,
    x="bedtime_phone_minutes",
    y="next_day_fatigue_score",
    title="Relationship Between Phone Usage and Next-Day Fatigue",
    labels={
        "bedtime_phone_minutes": "Bedtime Phone Usage (Minutes)",
        "next_day_fatigue_score": "Next-Day Fatigue Score"
    },
    color_discrete_sequence=["#E67E22"],
    opacity=0.55
)

fig4.update_layout(
    template="plotly_white",
    height=480,
    title_font_size=19,
    title_x=0.02,
    font=dict(
        family="Arial",
        size=13,
        color="#263445"
    ),
    margin=dict(l=45, r=30, t=85, b=55)
)

fig4.update_traces(
    marker=dict(size=7)
)

fig4.update_xaxes(
    showgrid=False,
    zeroline=False
)

fig4.update_yaxes(
    showgrid=True,
    gridcolor="#EAECEF",
    zeroline=False
)

st.plotly_chart(fig4, use_container_width=True)

# Graph 5: Average Fatigue by Occupation

st.subheader("5. Average Fatigue by Occupation")

# Calculate average fatigue for each occupation
occupation_fatigue = (
    df.groupby("occupation_type")["next_day_fatigue_score"]
    .mean()
    .reset_index()
    .sort_values("next_day_fatigue_score", ascending=True)
)

# Create horizontal bar chart
fig5 = px.bar(
    occupation_fatigue,
    x="next_day_fatigue_score",
    y="occupation_type",
    orientation="h",
    title="Average Next-Day Fatigue Across Occupation Types",
    labels={
        "occupation_type": "Occupation Type",
        "next_day_fatigue_score": "Average Fatigue Score"
    },
    text_auto=".2f",
    color_discrete_sequence=["#3977D5"]
)

# Improve appearance
fig5.update_layout(
    template="plotly_white",
    height=430,
    title_font_size=19,
    title_x=0.02,
    font=dict(
        family="Arial",
        size=13,
        color="#263445"
    ),
    margin=dict(l=30, r=40, t=80, b=45),
    showlegend=False
)

fig5.update_traces(
    textposition="outside"
)

fig5.update_xaxes(
    showgrid=True,
    gridcolor="#EAECEF",
    range=[0, 7]
)

fig5.update_yaxes(
    title="Occupation Type",
    showgrid=False
)

st.plotly_chart(fig5, use_container_width=True)

# Graph 6: Average Sleep Duration by Sleep Debt Category

st.subheader("6. Average Sleep Duration by Sleep Debt Category")

# Calculate average sleep duration
sleep_category = (
    df.groupby("sleep_debt_category")["total_sleep_hours"]
    .mean()
    .reset_index()
    .sort_values("total_sleep_hours", ascending=True)
)

# Create horizontal bar chart
fig6 = px.bar(
    sleep_category,
    x="total_sleep_hours",
    y="sleep_debt_category",
    orientation="h",
    title="Average Sleep Duration Across Sleep Debt Categories",
    labels={
        "sleep_debt_category": "Sleep Debt Category",
        "total_sleep_hours": "Average Sleep Duration (Hours)"
    },
    text_auto=".2f",
    color_discrete_sequence=["#16A085"]
)

# Improve appearance
fig6.update_layout(
    template="plotly_white",
    height=430,
    title_font_size=19,
    title_x=0.02,
    font=dict(
        family="Arial",
        size=13,
        color="#263445"
    ),
    margin=dict(l=30, r=40, t=80, b=45),
    showlegend=False
)

fig6.update_traces(
    textposition="outside"
)

fig6.update_xaxes(
    showgrid=True,
    gridcolor="#EAECEF"
)

fig6.update_yaxes(
    title="Sleep Debt Category",
    showgrid=False
)

st.plotly_chart(fig6, use_container_width=True)


# Raw Data Viewer

st.subheader("Explore Raw Dataset")

show_data = st.checkbox("Show Raw Dataset")

if show_data:
    st.dataframe(df, use_container_width=True)

# Key Findings

st.subheader("Key Findings")

st.markdown("""
- **Average bedtime phone usage:** 59.25 minutes.
- **Most popular bedtime app:** TikTok / Reels.
- **Phone usage and sleep duration:** Moderate negative correlation (-0.554).
- **Phone usage and fatigue:** Strong positive correlation (+0.711).
- **Highest fatigue by occupation:** Healthcare / Shift Workers (5.54).
- **Highest average sleep duration:** Optimal Recovery category (8.35 hours).
""")
