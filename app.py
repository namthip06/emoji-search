import streamlit as st
import sys
import os

# Ensure we can import from utils and src
sys.path.append(os.path.join(os.path.dirname(__file__)))

from utils.emoji_searcher import EmojiSearcher
from utils.subword_tokenizer import SubwordTokenizer
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

@st.cache_resource
def get_tokenizer():
    try:
        return SubwordTokenizer()
    except Exception as e:
        st.error(f"Failed to load tokenizer: {e}")
        return None

searcher = get_searcher()
tokenizer = get_tokenizer()

if not searcher:
    st.error("Failed to initialize the search engine. Please check if the ChromaDB is correctly set up.")
    st.stop()

# Search Interface
query = st.text_input("Search", placeholder="Search for something...", key="search_input", label_visibility="collapsed")

if query:
    n_results = 6
    with st.spinner("Finding the best emojis..."):
        results = searcher.search(query, n_results=n_results)
        
        if tokenizer:
            try:
                subword_splits = tokenizer.split_compound(query)
                # subword_splits is list of tuples, e.g. [('Sun', 'flower')]

                print("Subword splits:", subword_splits)
                
                # Use the first valid split if any
                if subword_splits:
                    parts = subword_splits[0] # (part1, part2)
                    
                    # Search for parts
                    sub_results_1 = searcher.search(parts[0], n_results=4)
                    sub_results_2 = searcher.search(parts[1], n_results=4)
                else:
                    parts = None
            except Exception as e:
                print(f"Subword search error: {e}")
                parts = None
        else:
            parts = None

    if results:
        st.markdown(f"### Results for *'{query}'*")
        
        # Display the results using the interactive component
        render_emoji_grid(results)
    else:
        st.info("No direct matching emojis found.")

    # Display Subword Analysis if available
    if parts:
        st.markdown("---")
        st.subheader("🧩 Compound Breakdown")
        st.markdown(f"Detected compound words: **{parts[0]}** + **{parts[1]}**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.caption(f"Results for '{parts[0]}'")
            render_emoji_grid(sub_results_1, columns=2)
            
        with col2:
            st.caption(f"Results for '{parts[1]}'")
            render_emoji_grid(sub_results_2, columns=2)