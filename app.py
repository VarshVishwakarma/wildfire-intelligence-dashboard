import pandas as pd
import numpy as np
import panel as pn
import hvplot.pandas
import holoviews as hv
import glob
import os

# =========================
# INITIALIZATION
# =========================
# Use Fast design system and include Tabulator
pn.extension('tabulator', sizing_mode="stretch_width", design='fast')

# Premium Theme Colors
ACCENT_COLOR = "#FF4500" # Fire Orange
BG_COLOR = "#ffffff"

# =========================
# LOAD OR MOCK DATA 
# =========================
try:
    # Attempt to load and concatenate all CSVs in the data folder
    csv_files = glob.glob("data/*.csv")
    
    # Prevents the "ValueError: No objects to concatenate" by explicitly checking
    if not csv_files:
        raise ValueError("No CSV files found in 'data/' directory to concatenate.")
        
    df_list = [pd.read_csv(f) for f in csv_files]
    df = pd.concat(df_list, ignore_index=True)
    df['acq_date'] = pd.to_datetime(df['acq_date'])
    
except (FileNotFoundError, ValueError) as e:
    # Safely fallback to dummy data if directory is empty or files are missing
    print(f"⚠️ Data Load Notice: {e}")
    print("Generating sample premium data for immediate testing...")
    
    dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
    np.random.seed(42)
    df = pd.DataFrame({
        'acq_date': np.random.choice(dates, 5000),
        'country': np.random.choice(['USA', 'Canada', 'Brazil', 'Australia', 'Spain', 'Indonesia', 'India'], 5000),
        'latitude': np.random.uniform(-50, 60, 5000),
        'longitude': np.random.uniform(-120, 150, 5000),
        'brightness': np.random.uniform(300, 500, 5000),
        'frp': np.random.uniform(10, 150, 5000)
    })

# =========================
# WIDGETS (SIDEBAR)
# =========================
date_slider = pn.widgets.DateRangeSlider(
    name='📅 Observation Period',
    start=df['acq_date'].min(),
    end=df['acq_date'].max(),
    value=(df['acq_date'].min(), df['acq_date'].max()),
    bar_color=ACCENT_COLOR
)

country_select = pn.widgets.MultiChoice(
    name='🌍 Region Filter',
    options=sorted(df['country'].unique()),
    value=list(df['country'].unique())[:4],
    solid=True
)

query_box = pn.widgets.TextInput(
    name="🤖 AI Quick Query",
    placeholder="Try: 'fires today' or 'total fires'",
)

query_output = pn.pane.Markdown("*Awaiting query...*", styles={'color': '#666666', 'font-style': 'italic'})

# =========================
# DATA FILTERING
# =========================
def filter_data(date_range, countries):
    return df[
        (df['acq_date'] >= date_range[0]) &
        (df['acq_date'] <= date_range[1]) &
        (df['country'].isin(countries))
    ]

# =========================
# PREMIUM METRIC CARDS
# =========================
def create_card(title, value, icon):
    """Generates a premium HTML/CSS metric card (Light Theme)"""
    html = f"""
    <div style="
        background: linear-gradient(135deg, #ffffff 0%, #f4f6f8 100%);
        border-left: 4px solid {ACCENT_COLOR};
        border-radius: 8px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        text-align: left;
        height: 100%;
    ">
        <div style="color: #6c757d; font-size: 0.85em; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 5px;">
            {title}
        </div>
        <div style="color: #212529; font-size: 2.2em; font-weight: 700;">
            <span style="font-size: 0.8em; margin-right: 5px;">{icon}</span>{value}
        </div>
    </div>
    """
    return pn.pane.HTML(html, sizing_mode="stretch_width", height=120)

def metrics(date_range, countries):
    filtered = filter_data(date_range, countries)
    
    total_fires = f"{len(filtered):,}"
    
    # Safely handle missing 'brightness' column
    if 'brightness' in filtered.columns and not filtered.empty:
        max_intensity = f"{int(filtered['brightness'].max())}K"
    else:
        max_intensity = "N/A"
        
    # Safely handle missing 'frp' column
    if 'frp' in filtered.columns and not filtered.empty:
        avg_frp = f"{round(filtered['frp'].mean(), 1)} MW"
    else:
        avg_frp = "N/A"

    return pn.Row(
        create_card("Total Detections", total_fires, "🔥"),
        create_card("Peak Intensity", max_intensity, "⚡"),
        create_card("Avg Fire Radiative Power", avg_frp, "📊"),
        sizing_mode="stretch_width"
    )

metrics_panel = pn.bind(metrics, date_slider, country_select)

# =========================
# VISUALIZATIONS
# =========================
def wildfire_map(date_range, countries):
    filtered = filter_data(date_range, countries)
    if filtered.empty:
        return pn.pane.Markdown("### No data available for this selection.", align="center")

    # Wrap the custom URL in an hv.Tiles object to satisfy hvplot requirements
    localized_google_tiles = hv.Tiles('https://mt0.google.com/vt/lyrs=m&hl=en&gl=IN&x={X}&y={Y}&z={Z}')

    # NASA-Level UI Upgrade: Hybrid Approach
    if len(filtered) > 100000:
        # Fallback to datashader for extreme scale performance
        point_plot = filtered.hvplot.points(
            x='longitude', y='latitude',
            tiles=localized_google_tiles, 
            datashade=True, 
            cmap='fire',
            height=750,
            responsive=True,
            xaxis=None, yaxis=None
        )
    else:
        # Premium NASA-Level Rendering for < 100k points
        # Scale dot size dynamically by brightness if available, else static size
        if 'brightness' in filtered.columns:
            point_size = hv.dim('brightness') * 0.02
            hover_columns = ['brightness', 'frp'] if 'frp' in filtered.columns else ['brightness']
        else:
            point_size = 8
            hover_columns = []
            
        point_plot = filtered.hvplot.points(
            x='longitude', y='latitude',
            tiles=localized_google_tiles,
            color='#FF1100',      # Crisp, vivid thermal red
            size=point_size,      # Dynamic sizing based on intensity
            alpha=0.6,            # Semi-transparent to show overlaps
            hover_cols=hover_columns, # Include hover data
            height=750,
            responsive=True,
            xaxis=None, yaxis=None,
            line_color='black',   # Adds subtle contrast to separate overlapping dots
            line_width=0.3
        )

    return point_plot.opts(
        toolbar='above', 
        default_tools=['pan', 'wheel_zoom']
    )

map_plot = pn.bind(wildfire_map, date_slider, country_select)

def trend_chart(date_range, countries):
    filtered = filter_data(date_range, countries)
    if filtered.empty:
        return pn.pane.Markdown("### No data.", align="center")

    trend = filtered.groupby('acq_date').size().reset_index(name='count')
    
    return trend.hvplot.line(
        x='acq_date', y='count',
        height=300, responsive=True,
        color=ACCENT_COLOR, line_width=3,
        grid=True, ylabel="Fire Detections", xlabel=""
    ).opts(
        toolbar=None, 
        bgcolor="white",
        show_grid=True, gridstyle={'grid_line_color': '#e0e0e0'}
    )

trend_plot = pn.bind(trend_chart, date_slider, country_select)

def hotspot_table(date_range, countries):
    filtered = filter_data(date_range, countries)
    if filtered.empty:
        return pn.pane.Markdown("No data")

    hotspots = (
        filtered.groupby(['latitude', 'longitude'])
        .size()
        .reset_index(name='Intensity Score')
        .sort_values(by='Intensity Score', ascending=False)
        .head(10)
    )
    # Round coordinates for cleaner display
    hotspots['latitude'] = hotspots['latitude'].round(3)
    hotspots['longitude'] = hotspots['longitude'].round(3)

    return pn.widgets.Tabulator(
        hotspots, 
        height=300, 
        theme='default', # Switch to default light theme
        show_index=False,
        layout='fit_columns'
    )

hotspots_panel = pn.bind(hotspot_table, date_slider, country_select)

# =========================
# AI INSIGHTS (SIDEBAR)
# =========================
def insights(date_range, countries):
    filtered = filter_data(date_range, countries)
    if filtered.empty:
        return pn.pane.Markdown("No data for insights.")

    midpoint = filtered['acq_date'].max() - pd.Timedelta(days=7)
    last_week = filtered[filtered['acq_date'] >= midpoint]
    prev_week = filtered[filtered['acq_date'] < midpoint]

    change = 0
    if len(prev_week) > 0:
        change = ((len(last_week) - len(prev_week)) / len(prev_week)) * 100

    trend_icon = "📈" if change > 0 else "📉"
    trend_color = "#ff4500" if change > 0 else "#00cc66"

    return pn.pane.Markdown(f"""
    <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 3px solid #dee2e6;">
        <h4 style="margin-top: 0; color: #343a40;">Automated Briefing</h4>
        <p style="color: #495057; font-size: 0.95em;">
            Analyzing <b>{len(filtered):,}</b> thermal anomalies. Activity has shifted by 
            <span style="color: {trend_color}; font-weight: bold;">{change:+.1f}%</span> 
            {trend_icon} compared to the previous period.
        </p>
    </div>
    """, sizing_mode="stretch_width")

insights_panel = pn.bind(insights, date_slider, country_select)

# =========================
# QUERY LOGIC
# =========================
def update_query(event):
    query = query_box.value.lower()
    
    if "today" in query or "latest" in query:
        today = df['acq_date'].max()
        count = len(df[df['acq_date'] == today])
        query_output.object = f"**Result:** 🔥 {count} fires detected on {today.strftime('%b %d')}."
    elif "total" in query:
        query_output.object = f"**Result:** 🌍 {len(df):,} total historical fires logged."
    elif query.strip() == "":
        query_output.object = "*Awaiting query...*"
    else:
        query_output.object = "*Unrecognized command. Try 'fires today'.*"

query_box.param.watch(update_query, 'value')

# =========================
# DASHBOARD LAYOUT (FAST TEMPLATE)
# =========================
# We use FastListTemplate for a built-in modern, responsive shell
template = pn.template.FastListTemplate(
    title="Global Wildfire Intelligence Command",
    logo="https://cdn-icons-png.flaticon.com/512/785/785116.png", # Fire icon
    header_background="#FFFFFF",
    header_color="#000000", # Changed to black text so it is visible on white background
    accent_base_color=ACCENT_COLOR,
    theme="default", # Switched to light theme
    theme_toggle=False,
    
    # --- SIDEBAR ---
    sidebar=[
        pn.pane.Markdown("### ⚙️ Parameters"),
        date_slider,
        pn.Spacer(height=10),
        country_select,
        pn.layout.Divider(),
        pn.pane.Markdown("### 🧠 Insights"),
        insights_panel,
        pn.layout.Divider(),
        pn.pane.Markdown("### 🔎 Copilot Query"),
        query_box,
        query_output
    ],
    
    # --- MAIN CANVAS ---
    main=[
        pn.Column(
            metrics_panel,
            pn.Spacer(height=10),
            pn.Card(map_plot, title="Satellite Thermal Anomalies", hide_header=True, sizing_mode="stretch_width"),
            pn.Spacer(height=10),
            pn.Row(
                pn.Card(trend_plot, title="Temporal Activity", hide_header=True, sizing_mode="stretch_width"),
                pn.Card(hotspots_panel, title="📍 Critical Hotspots (Coordinates)", hide_header=False, sizing_mode="stretch_width"),
                sizing_mode="stretch_width"
            ),
            sizing_mode="stretch_both"
        )
    ]
)

template.servable()
