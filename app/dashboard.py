import streamlit as st
import pandas as pd
import os
import gspread
from gspread_dataframe import get_as_dataframe
from analysis import convert_followers # Keep using this from analysis.py

# --- Page Configuration ---
st.set_page_config(layout="wide", page_title="AI Influencer Dashboard")

# --- Configuration ---
GOOGLE_SHEET_NAME = "AI Influencer Tracker sheet" 
WORKSHEET_NAME = "Sheet1"
CREDENTIALS_FILE = os.path.join("google_credentials.json")

# --- Load and Cache Data ---
@st.cache_data(ttl=600)  # Cache data for 10 minutes (600 seconds)
def load_data():
    try:
        gc = gspread.service_account(filename=CREDENTIALS_FILE)
        sh = gc.open(GOOGLE_SHEET_NAME)
        worksheet = sh.worksheet(WORKSHEET_NAME)
        df = get_as_dataframe(worksheet)
        df = df.dropna(how='all')
        
        if 'Followers' in df.columns:
            df['Followers'] = df['Followers'].apply(convert_followers)
            df = df.dropna(subset=['Followers'])
        else:
            st.error("Column 'Followers' not found in Google Sheet.")
            return pd.DataFrame()
            
        return df
        
    except gspread.exceptions.SpreadsheetNotFound:
        st.error(f"Google Sheet '{GOOGLE_SHEET_NAME}' not found.")
        st.error("Make sure the name is correct and you shared it with the service account email.")
        return pd.DataFrame()
    except gspread.exceptions.WorksheetNotFound:
        st.error(f"Worksheet tab '{WORKSHEET_NAME}' not found in your Google Sheet.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"An error occurred while loading data: {e}")
        return pd.DataFrame()

df = load_data()

if not df.empty:
    # --- Dashboard Title ---
    st.title("🤖 AI Influencer Tracker Dashboard")
    st.markdown("This dashboard is connected live to your Google Sheet.")

    # --- Top-Level Metrics ---
    st.header("Key Metrics")
    total_influencers = len(df)
    total_followers = df['Followers'].sum()
    avg_followers = df['Followers'].mean()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Influencers", f"{total_influencers}")
    col2.metric("Total Followers (All Platforms)", f"{total_followers:,.0f}")
    col3.metric("Average Followers", f"{avg_followers:,.0f}")

    # --- [NEW DYNAMIC INSIGHT CALCULATIONS] ---
    # Platform calculations
    top_platform_1_name = "N/A"
    top_platform_2_name = "N/A"
    top_2_platform_percent = 0

    # Niche calculations
    top_niche_1 = "N/A"
    top_niche_2 = "N/A"

    if 'Platform' in df.columns and total_influencers > 0:
        platform_counts = df['Platform'].value_counts()
        
        if len(platform_counts) > 0:
            # Get Top Platform 1
            top_platform_1_name = platform_counts.index[0]
            count_platform_1 = platform_counts.iloc[0]
            
            if len(platform_counts) > 1:
                # Get Top Platform 2
                top_platform_2_name = platform_counts.index[1]
                count_platform_2 = platform_counts.iloc[1]
                
                # Calculate combined percentage
                total_top_2_count = count_platform_1 + count_platform_2
                top_2_platform_percent = (total_top_2_count / total_influencers) * 100
            else:
                # Handle edge case where there is only 1 platform
                top_2_platform_percent = (count_platform_1 / total_influencers) * 100
                top_platform_2_name = "any other"

    if 'Niche' in df.columns:
        niche_counts = df['Niche'].value_counts()
        if len(niche_counts) > 0:
            top_niche_1 = niche_counts.index[0]
        if len(niche_counts) > 1:
            top_niche_2 = niche_counts.index[1]
    # --- End of New Calculations ---

    st.markdown("---")

    # --- Main Dashboard Layout ---
    st.header("Influencer Analysis")
    col1, col2 = st.columns(2)

    with col1:
        # --- 1. Platform Distribution ---
        st.subheader("Influencers by Platform")
        if 'Platform' in df.columns:
            platform_counts = df['Platform'].value_counts()
            st.bar_chart(platform_counts)
        else:
            st.warning("Column 'Platform' not found.")

    with col2:
        # --- 2. Follower Distribution ---
        st.subheader("Total Followers by Platform")
        if 'Platform' in df.columns:
            platform_followers = df.groupby('Platform')['Followers'].sum().sort_values(ascending=False)
            st.bar_chart(platform_followers)
        else:
            st.warning("Column 'Platform' not found.")

    # --- 3. Top Influencers Table ---
    st.header("Top 10 Influencers by Followers")
    top_influencers = df.sort_values(by='Followers', ascending=False).head(10)
    
    st.dataframe(top_influencers.style.format({
        'Followers': '{:,.0f}'
    }), use_container_width=True)

    # --- 4. Raw Data Explorer ---
    with st.expander("Explore All Influencer Data"):
        st.dataframe(df.style.format({
            'Followers': '{:,.0f}'
        }), use_container_width=True)

    st.markdown("---")

    # --- [MODIFIED] Quick Insights (MOVED TO THE END) ---
    st.header("Quick Insights")
    
    # Use f-strings to display the new dynamic variables
    insight_text = (
        f"💡 **{top_2_platform_percent:.0f}%** of all influencers are on the top two platforms: **{top_platform_1_name}** and **{top_platform_2_name}**. "
        f"The most popular niches are **{top_niche_1}** and **{top_niche_2}**."
    )
    st.info(insight_text)

else:
    st.warning("Could not load data to display the dashboard. Check the error messages above.")