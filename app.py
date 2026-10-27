import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Nassau Candy Route Intelligence",
    page_icon="🍬",
    layout="wide"
)

@st.cache_data
def load_data():
    return pd.read_csv("Nassau Candy Distributor.csv")

df = load_data()
df["Order Date"] = pd.to_datetime(
    df["Order Date"],
    dayfirst=True,
    errors="coerce"
)

df["Ship Date"] = pd.to_datetime(
    df["Ship Date"],
    dayfirst=True,
    errors="coerce"
)
# Factory mapping
factory_mapping = {
    "Wonka Bar - Nutty Crunch Surprise": "Lot's O' Nuts",
    "Wonka Bar - Fudge Mallows": "Lot's O' Nuts",
    "Wonka Bar -Scrumdiddlyumptious": "Lot's O' Nuts",
    "Wonka Bar - Milk Chocolate": "Wicked Choccy's",
    "Wonka Bar - Triple Dazzle Caramel": "Wicked Choccy's",
    "Laffy Taffy": "Sugar Shack",
    "SweeTARTS": "Sugar Shack",
    "Nerds": "Sugar Shack",
    "Fun Dip": "Sugar Shack",
    "Fizzy Lifting Drinks": "Sugar Shack",
    "Everlasting Gobstopper": "Secret Factory",
    "Lickable Wallpaper": "Secret Factory",
    "Wonka Gum": "Secret Factory",
    "Hair Toffee": "The Other Factory",
    "Kazookles": "The Other Factory"
}

df["Factory"] = df["Product Name"].map(factory_mapping)
st.title("🍬 Nassau Candy Route Intelligence")
st.markdown(
    """
    <style>
    /* Warm candy-factory background */
    .stApp {
        background:
            radial-gradient(ellipse at 0% 0%, #ffd6df 0%, transparent 28%),
            radial-gradient(ellipse at 100% 0%, #f6d4bd 0%, transparent 25%),
            radial-gradient(ellipse at 0% 100%, #ffe5b5 0%, transparent 25%),
            linear-gradient(135deg, #fff9ed, #fff0e8 55%, #fff7e9);
        color: #492719;
    }

    /* Candy decorations in the corners */
    .stApp::before {
        content: "🍭  🍬  🍫";
        position: fixed;
        top: 12px;
        left: 12px;
        font-size: 30px;
        opacity: 0.55;
        pointer-events: none;
        z-index: 0;
    }

    .stApp::after {
        content: "🍫  🍬  🍭";
        position: fixed;
        bottom: 12px;
        right: 12px;
        font-size: 30px;
        opacity: 0.55;
        pointer-events: none;
        z-index: 0;
    }

    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1450px;
    }

    h1 {
        color: #71351f !important;
        font-size: 2.5rem !important;
        font-weight: 800 !important;
    }

    h2, h3 {
