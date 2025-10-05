# AI Travel & Airline Daily Briefing Prototype
# Author: TheGoodTim
# Free Streamlit version (no paid APIs)

import streamlit as st
import feedparser
import pandas as pd
from datetime import datetime
import plotly.express as px

# -----------------------------
# APP TITLE
# -----------------------------
st.set_page_config(page_title="AI Travel Brief", layout="wide")
st.title("✈️ AI Travel & Airline Daily Briefing")
st.caption("Your daily industry intel dashboard — powered by open data & AI summaries")

# -----------------------------
# SIDEBAR CONTROLS
# -----------------------------
st.sidebar.header("Settings")
competitors = st.sidebar.multiselect(
    "Competitors to Track:",
    ["Delta", "Emirates", "JetBlue", "United", "Southwest", "Lufthansa"],
    default=["Delta", "Emirates", "JetBlue"]
)
num_headlines = st.sidebar.slider("Number of headlines to show", 3, 15, 7)
tone = st.sidebar.selectbox("Summary tone", ["Concise", "Professional", "Confident"])

st.sidebar.markdown("---")
st.sidebar.info("Free prototype using public RSS feeds. Data refreshes live from the web.")

# -----------------------------
# FETCH NEWS HEADLINES
# -----------------------------
st.subheader("📰 Latest Airline & Travel Headlines")

feeds = [
    "https://www.travelweekly.com/rss.xml",
    "https://simpleflying.com/feed/",
    "https://www.businesstravelnews.com/rss",
]

news_items = []
for url in feeds:
    feed = feedparser.parse(url)
    for entry in feed.entries[:num_headlines]:
        news_items.append({
            "title": entry.title,
            "source": feed.feed.get("title", "Unknown Source"),
            "link": entry.link,
            "published": entry.get("published", ""),
        })

df = pd.DataFrame(news_items)
if df.empty:
    st.warning("No headlines could be fetched. Try again later.")
else:
    for _, row in df.iterrows():
        st.markdown(f"**[{row['title']}]({row['link']})**  \n*{row['source']}* – {row['published']}")

# -----------------------------
# COMPETITOR WATCHLIST
# -----------------------------
st.subheader("👀 Competitor Mentions Tracker")

mention_data = []
for comp in competitors:
    matches = df[df['title'].str.contains(comp, case=False, na=False)]
    mention_data.append({"Competitor": comp, "Mentions": len(matches)})

mention_df = pd.DataFrame(mention_data)
chart = px.bar(
    mention_df,
    x="Competitor",
    y="Mentions",
    title="News Mentions by Competitor",
    text="Mentions",
)
chart.update_traces(textposition="outside")
st.plotly_chart(chart, use_container_width=True)

# -----------------------------
# SOCIAL / SENTIMENT PLACEHOLDER
# -----------------------------
st.subheader("💬 Social Sentiment (Coming Soon)")
st.info("This free version doesn’t connect to Twitter/X yet. "
        "You’ll be able to add that later with an API key.")

# -----------------------------
# REGIONAL NEWS DISTRIBUTION (SIMULATED)
# -----------------------------
st.subheader("🌍 News by Region (Simulated Example)")

regions = ["North America", "Europe", "Middle East", "Asia-Pacific", "Latin America"]
region_counts = [12, 8, 5, 9, 3]
region_df = pd.DataFrame({"Region": regions, "Stories": region_counts})
region_chart = px.pie(region_df, names="Region", values="Stories", title="Regional Focus")
st.plotly_chart(region_chart, use_container_width=True)

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.caption(
    "Built by TheGoodTim · Free AI Dashboard Prototype · Powered by Streamlit, Plotly & Feedparser"
)
