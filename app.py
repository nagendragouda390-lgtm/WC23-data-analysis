import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Cricket Analytics Dashboard",
                   page_icon="🏏",
                   layout="wide")

# Load Data
matches = pd.read_csv("matches.csv")
deliveries = pd.read_csv("deliveries.csv")

st.title("🏏 Cricket Analytics Dashboard")

# Sidebar
season = st.sidebar.selectbox(
    "Select Season",
    ["All"] + list(matches["season"].unique())
)

if season != "All":
    matches = matches[matches["season"] == season]
    deliveries = deliveries[deliveries["season"] == season]

# KPIs
total_matches = matches.shape[0]
total_runs = deliveries["runs_off_bat"].sum()
total_wickets = deliveries["player_dismissed"].notna().sum()
teams = len(set(matches["team1"]).union(set(matches["team2"])))

col1, col2, col3, col4 = st.columns(4)

col1.metric("Matches", total_matches)
col2.metric("Runs", total_runs)
col3.metric("Wickets", total_wickets)
col4.metric("Teams", teams)

st.divider()

# Team Wins
st.subheader("🏆 Team Wins")

wins = matches["winner"].value_counts().reset_index()
wins.columns = ["Team", "Wins"]

fig = px.bar(
    wins,
    x="Team",
    y="Wins",
    color="Wins"
)

st.plotly_chart(fig, use_container_width=True)

# Top Run Scorers
st.subheader("👑 Top Run Scorers")

runs = deliveries.groupby("striker")["runs_off_bat"].sum() \
                 .sort_values(ascending=False) \
                 .head(10)

fig2 = px.bar(
    x=runs.index,
    y=runs.values,
    labels={"x":"Player","y":"Runs"}
)

st.plotly_chart(fig2, use_container_width=True)

# Top Wicket Takers
st.subheader("🎯 Top Wicket Takers")

wkts = deliveries.dropna(subset=["player_dismissed"]) \
                 .groupby("bowler")["player_dismissed"] \
                 .count() \
                 .sort_values(ascending=False) \
                 .head(10)

fig3 = px.bar(
    x=wkts.index,
    y=wkts.values,
    labels={"x":"Bowler","y":"Wickets"}
)

st.plotly_chart(fig3, use_container_width=True)

# Venue Analysis
st.subheader("🏟 Matches by Venue")

venue = matches["venue"].value_counts().reset_index()
venue.columns = ["Venue","Matches"]

fig4 = px.pie(
    venue,
    names="Venue",
    values="Matches"
)

st.plotly_chart(fig4, use_container_width=True)
