{\rtf1\ansi\ansicpg1252\cocoartf2709
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 # ai_travel_brief.py\
# Streamlit prototype for "AI Daily Travel Briefing"\
# Features (mock data):\
# - Top Headlines (summarized in a concise, confident tone)\
# - Competitor Watchlist (Delta, Emirates, JetBlue)\
# - Social Sentiment Scan (mocked tweets + VADER-like scores)\
# - Visualizations: news volume by region, competitor mention counts, sentiment breakdown\
# - Optional Add-Ons (implemented in prototype): Text-to-Speech (gTTS), Regional Heatmap, One-line AI Insight generator (mocked)\
#\
# How to run:\
# 1. Install dependencies: pip install streamlit pandas plotly gtts\
# 2. Run: streamlit run ai_travel_brief.py\
#\
# Notes:\
# - This is a mock prototype using generated/sample data to demonstrate the UI and flows.\
# - Swap the `fetch_mock_data()` function with real fetchers (Newsdata.io, snscrape, OpenAI/HuggingFace summarizers) when ready.\
# - There are inline comments showing where to plug real APIs.\
\
import streamlit as st\
import pandas as pd\
import plotly.express as px\
import plotly.graph_objects as go\
import datetime\
import random\
import io\
from gtts import gTTS\
\
st.set_page_config(page_title="AI Travel Brief \'97 Prototype", layout="wide")\
\
# -------------------------- Mock Data Generator --------------------------\
def fetch_mock_data(date=None, n_headlines=8):\
    """Return a dict with mock headlines, competitor mentions, tweets, and region data.\
    Replace this function with live fetchers from News APIs, RSS, and snscrape for tweets.\
    """\
    if date is None:\
        date = datetime.date.today()\
\
    sample_titles = [\
        "Delta expands European routes for 2026, adding Rome and Madrid",\
        "IATA reports 8% YoY growth in passenger demand; Asia-Pacific leads recovery",\
        "Jet fuel prices spike 3.2% amid refinery maintenance",\
        "Emirates announces carbon offsetting program for long-haul flights",\
        "JetBlue opens new lounge at JFK ahead of summer travel season",\
        "Low-cost carriers push new fares in Southeast Asia",\
        "Airport congestion prompts operational changes at major hubs",\
        "Airlines test AI-driven dynamic pricing systems"\
    ]\
\
    headlines = []\
    for i in range(n_headlines):\
        t = random.choice(sample_titles)\
        headlines.append(\{\
            "id": i+1,\
            "title": t,\
            "source": random.choice(["Reuters", "Skift", "Travel Weekly", "IATA", "Bloomberg"]),\
            "region": random.choices(["North America", "Europe", "Asia-Pacific"], weights=[0.45,0.35,0.20])[0],\
            "published_at": (datetime.datetime.combine(date, datetime.time(hour=random.randint(0,23), minute=random.randint(0,59))))\
        \})\
\
    # Mock competitor mentions\
    competitors = ["Delta", "Emirates", "JetBlue"]\
    competitor_mentions = []\
    for c in competitors:\
        competitor_mentions.append(\{\
            "airline": c,\
            "mentions": random.randint(10,80),\
            "top_story": random.choice(sample_titles)\
        \})\
\
    # Mock tweets (for sentiment)\
    tweet_texts = [\
        "Loving the new routes Delta announced! Great move.",\
        "Terrible service on my last JetBlue flight, disappointed.",\
        "Emirates sustainability initiative is the future of travel.",\
        "Airport security lines were a mess today.",\
        "AI pricing is getting out of hand, saw a wild fare change.",\
        "Flights on time and crew were amazing. Thumbs up!",\
        "Bleisure travel is here to stay, combining work and leisure."\
    ]\
    tweets = []\
    for i in range(80):\
        t = random.choice(tweet_texts)\
        tweets.append(\{\
            "id": i+1,\
            "text": t,\
            # crude sentiment scoring: positive/neutral/negative\
            "sentiment_score": random.uniform(-1,1),\
            "created_at": (datetime.datetime.combine(date, datetime.time(hour=random.randint(0,23), minute=random.randint(0,59))))\
        \})\
\
    # Region counts\
    region_counts = pd.Series([h["region"] for h in headlines]).value_counts().to_dict()\
\
    return \{\
        "date": date,\
        "headlines": pd.DataFrame(headlines),\
        "competitor_mentions": pd.DataFrame(competitor_mentions),\
        "tweets": pd.DataFrame(tweets),\
        "region_counts": region_counts\
    \}\
\
# -------------------------- Simple Summarizer (Mock) --------------------------\
def summarize_text_to_tone(text, tone="concise_confident_professional"):\
    """Mock summarizer that returns a short rephrasing. Replace with OpenAI/HuggingFace call.\
    Keep it concise (1-2 sentences) and confident.\
    """\
    # Very naive mock transformation for prototype purpose\
    if "IATA" in text:\
        return "IATA reports strong passenger demand growth; Asia-Pacific is leading the recovery."\
    if "fuel" in text or "jet fuel" in text:\
        return "Jet fuel costs rose sharply, pressuring short-term margins."\
    if "Delta" in text and "European" in text:\
        return "Delta is expanding direct Europe routes for 2026, targeting business and leisure travel."\
    if "Emirates" in text and "carbon" in text:\
        return "Emirates rolled out a new carbon offsetting push for long-haul flights."\
    if "JetBlue" in text and "JFK" in text:\
        return "JetBlue opened a new JFK lounge to improve premium experience."\
    if "AI-driven" in text:\
        return "Carriers are trialing AI-driven dynamic pricing to optimize yield."\
    # fallback: trim + confident close\
    sentence = text.split('.')[0]\
    if len(sentence) > 140:\
        sentence = sentence[:140].rsplit(' ',1)[0] + '...'\
    return sentence\
\
# -------------------------- Sentiment Bucketizer --------------------------\
def bucket_sentiment(score):\
    if score >= 0.3:\
        return 'Positive'\
    elif score <= -0.3:\
        return 'Negative'\
    else:\
        return 'Neutral'\
\
# -------------------------- One-line AI Insight (Mock) --------------------------\
def generate_one_line_insight(headlines_df, competitor_df, tweets_df):\
    # Mocked simple logic to compose a one-liner insight\
    top_region = headlines_df['region'].mode().iloc[0]\
    top_comp = competitor_df.sort_values('mentions', ascending=False).iloc[0]['airline']\
    insight = f"\{top_region\} is driving the day's coverage; \{top_comp\} is the most-talked-about carrier \'97 watch capacity and pricing moves."\
    return insight\
\
# -------------------------- Streamlit UI --------------------------\
st.title("\uc0\u9992 \u65039  AI Daily Travel Brief \'97 Prototype")\
st.markdown("A mock prototype dashboard demonstrating the Daily Briefing experience (mock data). Replace mock data with live APIs to go production.")\
\
# Controls\
col_control_1, col_control_2, col_control_3 = st.columns([1,1,2])\
with col_control_1:\
    selected_date = st.date_input("Brief Date", value=datetime.date.today())\
with col_control_2:\
    refresh_button = st.button("Refresh Mock Data")\
with col_control_3:\
    tone_choice = st.selectbox("Summary Tone", options=["concise_confident_professional","more_conversational","analytical"], index=0)\
\
# Fetch data\
if refresh_button:\
    data = fetch_mock_data(selected_date)\
else:\
    data = fetch_mock_data(selected_date)\
\
headlines_df = data['headlines']\
competitor_df = data['competitor_mentions']\
tweets_df = data['tweets']\
region_counts = data['region_counts']\
\
# Top Headlines Panel\
st.header("Top Headlines")\
cols = st.columns([3,1])\
with cols[0]:\
    for idx, row in headlines_df.sort_values('published_at', ascending=False).iterrows():\
        st.subheader(f"\{row['title']\}")\
        summarized = summarize_text_to_tone(row['title'], tone=tone_choice)\
        st.write(summarized)\
        st.caption(f"Source: \{row['source']\} \'97 \{row['published_at'].strftime('%Y-%m-%d %H:%M')\}")\
        st.markdown('---')\
\
# Competitor Watchlist\
st.header("Competitor Watchlist")\
c1, c2 = st.columns([1,2])\
with c1:\
    st.subheader("Mentions This Week")\
    st.table(competitor_df.set_index('airline'))\
with c2:\
    st.subheader("Top Competitor Headlines (Summaries)")\
    for idx, row in competitor_df.iterrows():\
        s = summarize_text_to_tone(row['top_story'], tone=tone_choice)\
        st.write(f"**\{row['airline']\}** \'97 \{s\}")\
\
# Visualizations\
st.header("Visualizations & Trends")\
vis_col1, vis_col2 = st.columns(2)\
with vis_col1:\
    st.subheader("News Volume by Region")\
    region_df = pd.DataFrame(list(region_counts.items()), columns=['region','count'])\
    fig_region = px.pie(region_df, names='region', values='count', title='News Distribution by Region')\
    st.plotly_chart(fig_region, use_container_width=True)\
\
with vis_col2:\
    st.subheader("Competitor Mentions")\
    fig_comp = px.bar(competitor_df, x='airline', y='mentions', title='Mentions by Competitor')\
    st.plotly_chart(fig_comp, use_container_width=True)\
\
# Sentiment Scan\
st.header("Social Sentiment Scan")\
# Bucketize\
tweets_df['bucket'] = tweets_df['sentiment_score'].apply(bucket_sentiment)\
sentiment_counts = tweets_df['bucket'].value_counts().reindex(['Positive','Neutral','Negative']).fillna(0)\
\
s1, s2 = st.columns([1,2])\
with s1:\
    st.subheader("Sentiment Breakdown")\
    fig_sent = px.pie(values=sentiment_counts.values, names=sentiment_counts.index, title='Tweet Sentiment')\
    st.plotly_chart(fig_sent, use_container_width=True)\
\
with s2:\
    st.subheader("Recent Sample Tweets")\
    sample_tweets = tweets_df.sample(min(6, len(tweets_df)))[['text','sentiment_score']]\
    for idx, r in sample_tweets.iterrows():\
        st.write(r['text'])\
        st.caption(f"Sentiment score: \{r['sentiment_score']:.2f\}")\
\
# One-line AI Insight\
st.header("One-line Insight")\
insight = generate_one_line_insight(headlines_df, competitor_df, tweets_df)\
st.info(insight)\
\
# -------------------------- Optional Add-Ons (Implemented) --------------------------\
st.header("Optional Add-Ons (Prototype)")\
\
# 1) Text-to-Speech: convert the one-line insight to audio using gTTS\
st.subheader("Play the Insight (Text-to-Speech)")\
if st.button("Play Insight as Audio"):\
    tts = gTTS(text=insight, lang='en')\
    mp3_fp = io.BytesIO()\
    tts.write_to_fp(mp3_fp)\
    mp3_fp.seek(0)\
    st.audio(mp3_fp.read(), format='audio/mp3')\
\
# 2) Regional Heatmap: simple mock using choropleth with sample lat/lon and counts\
st.subheader("Regional Heatmap (Mock)")\
heatmap_data = pd.DataFrame(\{\
    'region': ['North America','Europe','Asia-Pacific'],\
    'lat':[40.0,54.0,22.0],\
    'lon':[-100.0,10.0,100.0],\
    'count':[region_counts.get('North America',0), region_counts.get('Europe',0), region_counts.get('Asia-Pacific',0)]\
\})\
fig_map = px.scatter_geo(heatmap_data, lat='lat', lon='lon', size='count', hover_name='region', projection='natural earth', title='News Volume by Region (mock)')\
st.plotly_chart(fig_map, use_container_width=True)\
\
# 3) Export brief to Google Sheet (instructions)\
st.subheader("Export / Persistence")\
st.markdown("This prototype suggests exporting summaries to Google Sheets or Firebase for persistence. In production, wire the fetch & summarizer to write to your storage of choice.")\
\
# 4) Download Brief (as text file)\
st.subheader("Download Today's Brief")\
if st.button("Download Brief as TXT"):\
    out_lines = []\
    out_lines.append(f"AI Travel Brief - \{data['date'].isoformat()\}\\n")\
    out_lines.append("Top Headlines:\\n")\
    for idx,row in headlines_df.iterrows():\
        out_lines.append(f"- \{row['title']\} -- \{summarize_text_to_tone(row['title'], tone=tone_choice)\}\\n")\
    out_lines.append('\\nCompetitor Mentions:\\n')\
    for idx,row in competitor_df.iterrows():\
        out_lines.append(f"- \{row['airline']\}: \{row['mentions']\} mentions\\n")\
    out_lines.append('\\nOne-line Insight:\\n')\
    out_lines.append(insight + '\\n')\
    txt_bytes = '\\n'.join(out_lines).encode('utf-8')\
    st.download_button("Download Brief", data=txt_bytes, file_name=f"travel_brief_\{data['date'].isoformat()\}.txt")\
\
# -------------------------- Footer / Developer Hints --------------------------\
st.markdown('---')\
st.markdown("### Developer Hints & Next Steps")\
st.markdown("- Swap `fetch_mock_data()` with a real fetcher: Newsdata.io, Mediastack, or RSS parsing (feedparser).\\n- Use `snscrape` to pull tweets during the desired time window, then run an NLP sentiment model for better accuracy (VADER, spaCy, or Hugging Face sentiment models).\\n- For summarization and tone, connect to OpenAI or a Hugging Face summarization model. Provide a prompt template that instructs the model to use a concise, confident, professional tone.\\n- Persist results to Google Sheets or Firebase so the dashboard can query historical data.\\n- Set up a GitHub Action or cron to run the collection + summarization daily.\\n")\
\
st.caption("Prototype generated for Tim \'97 replace mock connectors with production APIs to go live.")\
}