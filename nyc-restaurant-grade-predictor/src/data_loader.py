import pandas as pd
import os
import streamlit as st

# -------------------------------------------------
# BASE PATHS
# -------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
# Use cleaned data from the root data directory
RESTAURANT_DATA_PATH = os.path.join(BASE_DIR, "..", "data", "cleaned_restaurant_inspections.csv")


# -------------------------------------------------
# Load restaurant data with Streamlit caching
# -------------------------------------------------

@st.cache_data
def load_restaurant_data():
    """
    Loads the cleaned restaurant inspection dataset.
    Includes: borough, zipcode, cuisine_description, score,
    critical_flag, and coordinates for mapping.
    """
    # Read CSV with zipcode as string to preserve format
    df = pd.read_csv(RESTAURANT_DATA_PATH, low_memory=False, dtype={'zipcode': str})

    # Rename 'boro' to 'borough' for consistency
    if 'boro' in df.columns and 'borough' not in df.columns:
        df = df.rename(columns={'boro': 'borough'})

    # Clean/standardize core fields
    df['borough'] = df['borough'].astype(str).str.strip().str.title()
    df['cuisine_description'] = df['cuisine_description'].astype(str).str.strip().str.title()

    # Clean zipcode - empty strings become None
    df['zipcode'] = df['zipcode'].str.strip().replace('', None)

    # Create critical_flag_bin from critical_flag if not present
    if 'critical_flag_bin' not in df.columns and 'critical_flag' in df.columns:
        df['critical_flag_bin'] = (df['critical_flag'].str.lower() == 'critical').astype(int)

    return df


# -------------------------------------------------
# Public function app will import
# -------------------------------------------------

def get_data():
    """Returns the cleaned restaurant inspection data."""
    return load_restaurant_data()
