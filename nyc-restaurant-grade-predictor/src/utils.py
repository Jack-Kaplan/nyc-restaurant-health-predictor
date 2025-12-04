import pandas as pd

# -------------------------------------------------
# 1. Grade → Color mapping (UI styling)
# -------------------------------------------------

GRADE_COLORS = {
    "A": "#2ECC71",   # green
    "B": "#F1C40F",   # yellow
    "C": "#E67E22",   # orange
    "P": "#3498DB",   # blue (Pending)
    "Z": "#95A5A6"    # gray (Grade Pending / Not Yet Graded)
}

def get_grade_color(grade: str):
    """Return the hex color associated with a grade letter."""
    return GRADE_COLORS.get(grade, "#95A5A6")


# -------------------------------------------------
# 2. Format model prediction probabilities
# -------------------------------------------------

def format_probabilities(prob_dict: dict):
    """
    Convert the { 'A': 0.87, 'B': 0.09, ... } dictionary
    into a sorted, clean list for UI display.
    """
    formatted = []
    for grade, prob in prob_dict.items():
        formatted.append((grade, round(prob * 100, 2)))  # convert to %
    return sorted(formatted, key=lambda x: x[1], reverse=True)


# -------------------------------------------------
# 3. Convert a restaurant row into model input dictionary
# -------------------------------------------------

def row_to_model_input(row: pd.Series):
    """
    Take a row from the restaurant dataset and extract
    the 5 features expected by the model.

    Features: borough, zipcode, cuisine_description, critical_flag_bin, score
    """

    required_fields = [
        "borough",
        "zipcode",
        "cuisine_description",
        "critical_flag_bin",
        "score",
    ]

    data = {}

    for field in required_fields:
        if field not in row:
            raise KeyError(f"Missing required field: {field}. Available: {list(row.index)}")
        data[field] = row[field]

    return data


# -------------------------------------------------
# 4. Quick helper: clean filter inputs (ZIP, Cuisine, etc.)
# -------------------------------------------------

def clean_zip(zip_value):
    """Ensure ZIP codes become integers or None."""
    try:
        return int(zip_value)
    except (ValueError, TypeError):
        return None


def normalize_text(text):
    """Simple helper for cleaning cuisine/borough search inputs."""
    if pd.isna(text):
        return ""
    return str(text).strip().title()


def display_value(value, fallback="Unavailable"):
    """Return fallback string if value is NaN, None, or empty."""
    if pd.isna(value) or value == "" or value is None:
        return fallback
    return value


# -------------------------------------------------
# 5. Map marker helper functions (for Streamlit-Folium or PyDeck)
# -------------------------------------------------

def restaurant_popup_html(row):
    """
    Builds the HTML used in popups on the map
    for folium / leaflet display.
    """
    name = row.get("dba") or row.get("DBA") or "Unknown Restaurant"
    cuisine = row.get("cuisine_description", "Unknown")
    borough = row.get("borough", "Unknown")
    zipcode = row.get("zipcode", "")
    score = display_value(row.get("score"), "N/A")
    grade = display_value(row.get("grade"), "N/A")

    color = get_grade_color(grade)

    html = f"""
    <div style="font-size:14px;">
        <b>{name}</b><br>
        <span>Cuisine: {cuisine}</span><br>
        <span>Borough: {borough}</span><br>
        <span>ZIP: {zipcode}</span><br>
        <span>Score: {score}</span><br>
        <span>Grade: <b style='color:{color};'>{grade}</b></span>
    </div>
    """
    return html

