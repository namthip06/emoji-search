import streamlit as st
import sys
import os

# Ensure we can import from utils and src
sys.path.append(os.path.join(os.path.dirname(__file__)))

from utils.emoji_searcher import EmojiSearcher
from src.components import render_emoji_grid

# Page Configuration
st.set_page_config(
    page_title="Emoji Search",
    page_icon="🔍",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom Styling
st.markdown("""
    <style>
    .main {
        padding-top: 2rem;
    }
    .main {
        padding-top: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.title("✨ Semantic Emoji Search")
st.markdown("Type a phrase (in English or Thai) to find the most relevant emojis powered by AI.")

# Initialize Searcher (Cached)
@st.cache_resource
def get_searcher():
    try:
        return EmojiSearcher()
    except Exception as e:
        return None

searcher = get_searcher()

if not searcher:
    st.error("Failed to initialize the search engine. Please check if the ChromaDB is correctly set up.")
    st.stop()

# Search Interface
# Search Interface
query = st.text_input("Search", placeholder="Search for something...", key="search_input", label_visibility="collapsed")

if query:
    n_results = 6
    with st.spinner("Finding the best emojis..."):
        results = searcher.search(query, n_results=n_results)
    
    if results:
        st.markdown(f"### Results for *'{query}'*")
        
        # Display the results using the interactive component
        render_emoji_grid(results)
    else:
        st.info("No matching emojis found. Try a different query!")