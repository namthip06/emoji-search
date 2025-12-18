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
st.markdown("Type a phrase (support 25+ languages following WordNet (OMW 1.4)) to find the most relevant emojis powered by AI.")

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
                # subword_splits is list of list of str
                print("Subword splits:", subword_splits)
                
                # Prepare results for all splits
                all_compound_results = []
                for parts in subword_splits:
                    # parts is list of strings, e.g. ['Sun', 'flower']
                    split_entry = []
                    for part in parts:
                        part_res = searcher.search(part, n_results=1)
                        split_entry.append((part, part_res))
                    all_compound_results.append(split_entry)

            except Exception as e:
                print(f"Subword search error: {e}")
                all_compound_results = []
        else:
            all_compound_results = []

    if results:
        st.markdown(f"### Results for *'{query}'*")
        
        # Display the results using the interactive component
        render_emoji_grid(results)
    else:
        st.info("No direct matching emojis found.")

    # Display Subword Analysis if available
    if all_compound_results:
        st.markdown("---")
        st.subheader("Compound Breakdowns")
        
        for idx, split_group in enumerate(all_compound_results):
            # split_group is a list of (word, results)
            words = [item[0] for item in split_group]
            breakdown_text = " + ".join([f"**{w}**" for w in words])
            
            st.markdown(f"##### Option {idx+1}: {breakdown_text}")
            
            # Display parts in a grid with 2 columns per row
            grid_cols = 2
            for i in range(0, len(split_group), grid_cols):
                chunk = split_group[i:i + grid_cols]
                cols = st.columns(grid_cols)
                
                for j, (word, sub_res) in enumerate(chunk):
                    with cols[j]:
                        st.caption(f"'{word}'")
                        if sub_res:
                            # Use more columns inside to make it more square if width allows
                            render_emoji_grid(sub_res, columns=2)
                        else:
                            st.text("-")
            
            if idx < len(all_compound_results) - 1:
                st.divider()