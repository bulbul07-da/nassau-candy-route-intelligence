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
    .main {
        padding-top: 1rem;
    }

    h1 {
        font-size: 2.5rem;
        font-weight: 700;
    }

    h2, h3 {
        font-weight: 600;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown(
    "### Data-driven analysis of shipment routes, geography and shipping modes"
)
st.markdown(
    """
    <style>
    [data-testid="stMetric"] {
        background-color: #f8f9fa;
        border: 1px solid #e5e7eb;
        padding: 18px;
        border-radius: 12px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.divider()
total_shipments = len(df)
total_states = df["State/Province"].nunique()
total_ship_modes = df["Ship Mode"].nunique()
total_products = df["Product Name"].nunique()


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Shipments", f"{total_shipments:,}")

with col2:
    st.metric("Destination Locations", f"{total_states:,}")

with col3:
    st.metric("Ship Modes", f"{total_ship_modes:,}")

with col4:
    st.metric("Products", f"{total_products:,}")

st.divider()
# Interactive Filters
st.subheader("🎛️ Filters")
filter_date = st.date_input(
    "Order Date Range",
    value=(df["Order Date"].min().date(), df["Order Date"].max().date())
)
filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(4)

with filter_col1:
    selected_region = st.selectbox(
        "Region",
        ["All"] + sorted(df["Region"].dropna().unique().tolist())
    )

with filter_col2:
    selected_state = st.selectbox(
        "State/Province",
        ["All"] + sorted(df["State/Province"].dropna().unique().tolist())
    )

with filter_col3:
    selected_ship_mode = st.selectbox(
        "Ship Mode",
        ["All"] + sorted(df["Ship Mode"].dropna().unique().tolist())
    )

with filter_col4:
    selected_factory = st.selectbox(
        "Factory",
        ["All"] + sorted(df["Factory"].dropna().unique().tolist())
    )

filtered_df = df.copy()
if len(filter_date) == 2:
    start_date, end_date = filter_date

    filtered_df = filtered_df[
        (filtered_df["Order Date"].dt.date >= start_date)
        & (filtered_df["Order Date"].dt.date <= end_date)
    ]
if selected_region != "All":
    filtered_df = filtered_df[
        filtered_df["Region"] == selected_region
    ]

if selected_state != "All":
    filtered_df = filtered_df[
        filtered_df["State/Province"] == selected_state
    ]

if selected_ship_mode != "All":
    filtered_df = filtered_df[
        filtered_df["Ship Mode"] == selected_ship_mode
    ]

if selected_factory != "All":
    filtered_df = filtered_df[
        filtered_df["Factory"] == selected_factory
    ]

st.info(
    f"Showing {len(filtered_df):,} shipments after applying filters."
)
st.subheader("Dataset Overview")

st.write(
    f"The filtered dataset contains **{len(filtered_df):,} shipments** "
    f"covering **{filtered_df['State/Province'].nunique():,} destination locations**."
)

st.dataframe(
    filtered_df.head(10),
    width="stretch"
)
# Route Efficiency Overview
st.divider()

st.subheader("📊 Route Volume Overview")

route_summary = (
    filtered_df.groupby(["Factory", "State/Province"])
    .size()
    .reset_index(name="Shipment Volume")
)

route_summary["Route"] = (
    route_summary["Factory"]
    + " → "
    + route_summary["State/Province"]
)

route_summary = route_summary.sort_values(
    "Shipment Volume",
    ascending=False
)

st.write("Top routes by shipment volume:")

st.dataframe(
    route_summary[
        ["Route", "Shipment Volume"]
    ].head(10),
    width="stretch"
)
# Ship Mode Comparison
st.divider()

st.subheader("🚚 Ship Mode Comparison")

ship_mode_summary = (
    filtered_df["Ship Mode"]
    .value_counts()
    .reset_index()
)

ship_mode_summary.columns = ["Ship Mode", "Shipment Volume"]

col1, col2 = st.columns(2)

with col1:
    st.bar_chart(
        ship_mode_summary.set_index("Ship Mode")
    )

with col2:
    st.dataframe(
        ship_mode_summary,
        width="stretch"
    )
# Geographic Shipping Analysis
st.divider()
st.subheader("🌎 Geographic Shipping Analysis")

state_summary = (
    filtered_df["State/Province"]
    .value_counts()
    .reset_index()
)

state_summary.columns = ["State/Province", "Shipment Volume"]

col1, col2 = st.columns(2)

with col1:
    st.bar_chart(
        state_summary.head(15).set_index("State/Province")
    )

with col2:
    st.dataframe(
        state_summary.head(15),
        width="stretch"
    )
# Geographic Shipping Map
st.divider()

st.subheader("🗺️ Geographic Shipping Map")

state_codes = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ",
    "Arkansas": "AR", "California": "CA", "Colorado": "CO",
    "Connecticut": "CT", "Delaware": "DE", "Florida": "FL",
    "Georgia": "GA", "Hawaii": "HI", "Idaho": "ID",
    "Illinois": "IL", "Indiana": "IN", "Iowa": "IA",
    "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA",
    "Maine": "ME", "Maryland": "MD", "Massachusetts": "MA",
    "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS",
    "Missouri": "MO", "Montana": "MT", "Nebraska": "NE",
    "Nevada": "NV", "New Hampshire": "NH", "New Jersey": "NJ",
    "New Mexico": "NM", "New York": "NY", "North Carolina": "NC",
    "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK",
    "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI",
    "South Carolina": "SC", "South Dakota": "SD", "Tennessee": "TN",
    "Texas": "TX", "Utah": "UT", "Vermont": "VT",
    "Virginia": "VA", "Washington": "WA", "West Virginia": "WV",
    "Wisconsin": "WI", "Wyoming": "WY",
    "District of Columbia": "DC"
}

state_map = (
    filtered_df[
        filtered_df["State/Province"].isin(state_codes.keys())
    ]
    .groupby("State/Province")
    .size()
    .reset_index(name="Shipment Volume")
)

state_map["State Code"] = state_map["State/Province"].map(state_codes)

fig = px.choropleth(
    state_map,
    locations="State Code",
    locationmode="USA-states",
    color="Shipment Volume",
    scope="usa",
    hover_name="State/Province",
    hover_data={"State Code": False, "Shipment Volume": True},
    title="Shipment Volume by U.S. State"
)

st.plotly_chart(fig, width="stretch")

st.caption(
    "The map shows shipment concentration across U.S. destination states. "
    "Higher shipment volume indicates greater geographic concentration."
)
# Route Drill-Down
st.divider()

st.subheader("🔍 Route Drill-Down")

route_summary = (
    filtered_df
    .groupby(["Factory", "State/Province"])
    .agg(
        Shipment_Volume=("Order ID", "count"),
        Total_Sales=("Sales", "sum"),
        Total_Units=("Units", "sum"),
        Avg_Gross_Profit=("Gross Profit", "mean")
    )
    .reset_index()
)

route_summary["Route"] = (
    route_summary["Factory"]
    + " → "
    + route_summary["State/Province"]
)

route_summary = route_summary.sort_values(
    "Shipment_Volume",
    ascending=False
)
route_summary["Total_Sales"] = route_summary["Total_Sales"].round(2)
route_summary["Avg_Gross_Profit"] = route_summary["Avg_Gross_Profit"].round(2)
st.dataframe(
    route_summary[
        [
            "Route",
            "Shipment_Volume",
            "Total_Sales",
            "Total_Units",
            "Avg_Gross_Profit"
        ]
    ],
    width="stretch"
)
# Factory Shipment Analysis
st.divider()

st.subheader("🏭 Factory Shipment Analysis")

factory_summary = (
    filtered_df["Factory"]
    .value_counts()
    .reset_index()
)

factory_summary.columns = ["Factory", "Shipment Volume"]
factory_summary["Shipment Volume"] = factory_summary["Shipment Volume"].astype(int)
col1, col2 = st.columns(2)

with col1:
    st.bar_chart(
        factory_summary.set_index("Factory")
    )

with col2:
    st.dataframe(
        factory_summary,
        width="stretch"
    )
# Data Quality Note
st.divider()

st.subheader("⚠️ Data Quality Note")

st.warning(
    "The source dataset contains shipment dates that occur substantially "
    "after the corresponding order dates. Calculated shipping lead times "
    "range from 904 to 1,642 days for all records. Because the source "
    "dates are not validated for logistics timing, raw shipping lead time "
    "is excluded from route-performance benchmarking."
)

st.caption(
    "Raw Order Date and Ship Date are retained for auditability; "
    "they should not be interpreted as actual transit times without "
    "a validated correction to the source data."
)