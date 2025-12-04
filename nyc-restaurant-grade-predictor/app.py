import streamlit as st
import pandas as pd
import pydeck as pdk

from src.data_loader import get_data
from src.predictor import predict_restaurant_grade
from src.utils import (
    get_grade_color,
    format_probabilities,
    row_to_model_input,
    normalize_text,
    display_value,
    prepare_map_dataframe,
)


# -------------------------------------------------
# Page config
# -------------------------------------------------
st.set_page_config(
    page_title="CleanKitchen NYC",
    page_icon="🍽️",
    layout="wide"
)

st.title("CleanKitchen NYC")
st.markdown(
    "Explore NYC restaurant inspections, neighborhood demographics, "
    "and **AI-powered grade predictions** based on real inspection data."
)


# -------------------------------------------------
# Load data
# -------------------------------------------------
@st.cache_data
def load_app_data():
    df = get_data()

    # Normalize some text fields for filters
    df["borough"] = df["borough"].astype(str).str.strip().str.title()
    df["cuisine_description"] = df["cuisine_description"].astype(str).str.strip().str.title()

    # Keep only the most recent inspection per restaurant (by camis ID)
    if "camis" in df.columns and "inspection_date" in df.columns:
        df["inspection_date"] = pd.to_datetime(df["inspection_date"], errors="coerce")
        df = df.sort_values("inspection_date", ascending=False)
        df = df.drop_duplicates(subset=["camis"], keep="first")

    return df


df = load_app_data()

if df.empty:
    st.error("No data loaded. Please check your CSV files in the data/ folder.")
    st.stop()


# -------------------------------------------------
# SIDEBAR FILTERS
# -------------------------------------------------
st.sidebar.header("🔎 Filter Restaurants")

# Borough filter
boroughs = ["All"] + sorted(df["borough"].dropna().unique().tolist())
borough_choice = st.sidebar.selectbox("Borough", boroughs, index=0)

# ZIP filter (depends on borough choice)
if borough_choice != "All":
    zip_candidates = df.loc[df["borough"] == borough_choice, "zipcode"].unique()
else:
    zip_candidates = df["zipcode"].unique()

zips = ["All"] + sorted([z for z in zip_candidates if pd.notna(z)])
zip_choice = st.sidebar.selectbox("ZIP code", zips, index=0)

# Cuisine filter
cuisine_list = sorted(df["cuisine_description"].dropna().unique().tolist())
cuisine_choice = st.sidebar.multiselect(
    "Cuisine type",
    options=cuisine_list,
    default=[]
)

# Apply filters
df_filtered = df.copy()

if borough_choice != "All":
    df_filtered = df_filtered[df_filtered["borough"] == borough_choice]

if zip_choice != "All":
    df_filtered = df_filtered[df_filtered["zipcode"] == zip_choice]

if cuisine_choice:
    df_filtered = df_filtered[df_filtered["cuisine_description"].isin(cuisine_choice)]

st.sidebar.markdown(f"**Results: {len(df_filtered)} restaurants**")


# -------------------------------------------------
# MAIN LAYOUT: Map (left) + Details/Prediction (right)
# -------------------------------------------------
left_col, right_col = st.columns([2, 1])

with left_col:
    st.subheader("Map of Restaurants")

    if len(df_filtered) == 0:
        st.info("No restaurants match your filters. Try changing the filters.")
    else:
        # Prepare data for PyDeck (no marker limit needed)
        map_df = prepare_map_dataframe(df_filtered)

        center_lat = map_df["latitude"].mean()
        center_lon = map_df["longitude"].mean()

        # Adaptive zoom based on data spread
        lat_range = map_df["latitude"].max() - map_df["latitude"].min()
        lon_range = map_df["longitude"].max() - map_df["longitude"].min()
        max_range = max(lat_range, lon_range)
        zoom = 15 if max_range < 0.01 else 13 if max_range < 0.05 else 12 if max_range < 0.1 else 11

        layer = pdk.Layer(
            "ScatterplotLayer",
            data=map_df,
            get_position=["longitude", "latitude"],
            get_color="color",
            get_radius=8,
            radius_min_pixels=4,
            radius_max_pixels=8,
            radius_scale=1,
            pickable=True,
            auto_highlight=True,
        )

        view_state = pdk.ViewState(
            latitude=center_lat,
            longitude=center_lon,
            zoom=zoom,
            pitch=0,
        )

        tooltip = {
            "html": "<b>{name}</b><br/>Cuisine: {cuisine_description}<br/>Borough: {borough}<br/>ZIP: {zipcode}<br/>Score: {score_display}<br/>Grade: <b>{grade_display}</b>",
            "style": {"backgroundColor": "steelblue", "color": "white", "fontSize": "14px", "padding": "10px"}
        }

        st.pydeck_chart(
            pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip=tooltip),
            height=500,
            use_container_width=True,
        )

        # Grade legend
        st.markdown("""
        <div style="display: flex; gap: 15px; font-size: 12px; margin-top: 5px;">
            <span><span style="color: #2ECC71;">●</span> A</span>
            <span><span style="color: #F1C40F;">●</span> B</span>
            <span><span style="color: #E67E22;">●</span> C</span>
            <span><span style="color: #3498DB;">●</span> Pending</span>
            <span><span style="color: #95A5A6;">●</span> N/A</span>
        </div>
        """, unsafe_allow_html=True)

        st.caption(f"Showing all {len(map_df):,} restaurants on map.")

    st.subheader("Restaurant List")
    st.caption("Filtered view based on your selections in the sidebar.")

    # Show a simpler table
    cols_to_show = [
        c for c in ["DBA", "dba", "borough", "zipcode",
                    "cuisine_description", "score", "grade", "inspection_date"]
        if c in df_filtered.columns
    ]
    if cols_to_show:
        st.dataframe(
            df_filtered[cols_to_show].head(300),
            use_container_width=True
        )
    else:
        st.dataframe(df_filtered.head(300), use_container_width=True)


with right_col:
    st.subheader(" Inspect & Predict")

    if len(df_filtered) == 0:
        st.info("Use the filters to select at least one restaurant.")
    else:
        # Let user pick a restaurant from a dropdown
        # Use name + zip as label
        if "dba" in df_filtered.columns:
            name_col = "dba"
        elif "DBA" in df_filtered.columns:
            name_col = "DBA"
        else:
            name_col = df_filtered.columns[0]  # fallback

        df_filtered = df_filtered.reset_index(drop=True)
        options = df_filtered.index.tolist()
        labels = [
            f"{df_filtered.loc[i, name_col]} ({df_filtered.loc[i, 'borough']}, {df_filtered.loc[i, 'zipcode']})"
            for i in options
        ]

        selected_idx = st.selectbox(
            "Choose a restaurant to analyze:",
            options=options,
            format_func=lambda i: labels[i]
        )

        selected_row = df_filtered.loc[selected_idx]

        st.markdown("###  Selected Restaurant")
        st.markdown(f"**Name:** {selected_row.get(name_col, 'N/A')}")
        st.markdown(f"**Borough:** {selected_row.get('borough', 'N/A')}")
        st.markdown(f"**ZIP:** {selected_row.get('zipcode', 'N/A')}")
        st.markdown(f"**Cuisine:** {selected_row.get('cuisine_description', 'N/A')}")

        # Show existing inspection info (if present)
        st.markdown("###  Latest Inspection Info")
        st.markdown(f"- **Score:** {display_value(selected_row.get('score'), 'N/A')}")
        st.markdown(f"- **Official Grade:** {display_value(selected_row.get('grade'), 'Unavailable')}")
        if "inspection_date" in selected_row:
            st.markdown(f"- **Inspection Date:** {selected_row.get('inspection_date')}")

        st.markdown("---")
        st.markdown("###  Model Prediction")

        if st.button("Predict Inspection Grade"):
            try:
                # Build model input
                model_input = row_to_model_input(selected_row)
                result = predict_restaurant_grade(model_input)

                predicted_grade = result["grade"]
                probabilities = result["probabilities"]
                formatted_probs = format_probabilities(probabilities)

                color = get_grade_color(predicted_grade)

                st.markdown(
                    f"**Predicted Grade:** "
                    f"<span style='color:{color}; font-size: 24px; font-weight: bold;'>{predicted_grade}</span>",
                    unsafe_allow_html=True
                )

                st.markdown("#### Confidence by Grade")
                for g, p in formatted_probs:
                    bar = "█" * int(p // 4)  # simple text bar
                    st.write(f"{g}: {p:.1f}% {bar}")

            except Exception as e:
                st.error(f"Error making prediction: {e}")
