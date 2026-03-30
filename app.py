import pandas as pd
import panel as pn
import hvplot.pandas
import glob

pn.extension(sizing_mode="stretch_width")

# =========================
# LOAD DATA (MEMORY SAFE 🚀)
# =========================
files = glob.glob("viirs-jpss1/2024/*.csv")

df_list = []

for f in files:
    temp = pd.read_csv(
        f,
        usecols=['latitude', 'longitude', 'bright_ti4', 'acq_date', 'frp'],
        nrows=50000   # 🔥 LIMIT PER FILE (CRITICAL FIX)
    )
    
    temp['country'] = f.split("_")[-1].replace(".csv", "")
    df_list.append(temp)

df = pd.concat(df_list, ignore_index=True)

df = df.rename(columns={'bright_ti4': 'brightness'})
df['acq_date'] = pd.to_datetime(df['acq_date'])

# =========================
# WIDGETS
# =========================
date_slider = pn.widgets.DateRangeSlider(
    name='📅 Date Range',
    start=df['acq_date'].min(),
    end=df['acq_date'].max(),
    value=(df['acq_date'].min(), df['acq_date'].max())
)

country_select = pn.widgets.MultiChoice(
    name='🌍 Country',
    options=sorted(df['country'].unique()),
    value=['India']
)

query_box = pn.widgets.TextInput(
    name="🔎 Quick Query",
    placeholder="e.g. fires today"
)

query_output = pn.pane.Markdown("")

# =========================
# FILTER
# =========================
def filter_data(date_range, countries):
    return df[
        (df['acq_date'] >= date_range[0]) &
        (df['acq_date'] <= date_range[1]) &
        (df['country'].isin(countries))
    ]

# =========================
# 🔥 MAP (DATASHADER SAFE)
# =========================
def wildfire_map(date_range, countries):
    filtered = filter_data(date_range, countries)

    return filtered.hvplot.points(
        x='longitude',
        y='latitude',
        tiles='OSM',
        datashade=True,   # 🚀 NO LAG
        height=500
    )

map_plot = pn.bind(wildfire_map, date_slider, country_select)

# =========================
# METRICS
# =========================
def metric_card(title, value):
    return pn.pane.Markdown(f"""
### {title}
## **{value}**
""", styles={
        'background': '#111',
        'padding': '15px',
        'border-radius': '10px',
        'color': 'white',
        'text-align': 'center'
    })

def metrics(date_range, countries):
    filtered = filter_data(date_range, countries)

    return pn.Row(
        metric_card("🔥 Total Fires", len(filtered)),
        metric_card("⚡ Max Intensity", int(filtered['brightness'].max()) if not filtered.empty else 0),
        metric_card("📊 Avg FRP", round(filtered['frp'].mean(), 2) if not filtered.empty else 0),
    )

metrics_panel = pn.bind(metrics, date_slider, country_select)

# =========================
# TREND
# =========================
def trend_chart(date_range, countries):
    filtered = filter_data(date_range, countries)

    trend = filtered.groupby('acq_date').size().reset_index(name='count')

    return trend.hvplot.line(
        x='acq_date',
        y='count',
        height=300,
        line_width=2
    )

trend_plot = pn.bind(trend_chart, date_slider, country_select)

# =========================
# HOTSPOTS
# =========================
def hotspot_table(date_range, countries):
    filtered = filter_data(date_range, countries)

    hotspots = (
        filtered.groupby(['latitude', 'longitude'])
        .size()
        .reset_index(name='fire_count')
        .sort_values(by='fire_count', ascending=False)
        .head(5)
    )

    return pn.widgets.Tabulator(hotspots, height=200)

hotspots_panel = pn.bind(hotspot_table, date_slider, country_select)

# =========================
# INSIGHTS
# =========================
def insights(date_range, countries):
    filtered = filter_data(date_range, countries)

    if filtered.empty:
        return pn.pane.Markdown("No data")

    last_week = filtered[filtered['acq_date'] >= (filtered['acq_date'].max() - pd.Timedelta(days=7))]
    prev_week = filtered[
        (filtered['acq_date'] < (filtered['acq_date'].max() - pd.Timedelta(days=7))) &
        (filtered['acq_date'] >= (filtered['acq_date'].max() - pd.Timedelta(days=14)))
    ]

    change = ((len(last_week) - len(prev_week)) / max(len(prev_week), 1)) * 100

    return pn.pane.Markdown(f"""
## 🧠 Insights

- 🌍 Total fires: **{len(filtered)}**
- 📈 Weekly change: **{round(change,2)}%**

👉 Wildfire activity trend detected.
""")

insights_panel = pn.bind(insights, date_slider, country_select)

# =========================
# 🔎 QUERY FIXED
# =========================
def update_query(event):
    query = query_box.value.lower()

    if "today" in query:
        today = df['acq_date'].max()
        count = len(df[df['acq_date'] == today])
        query_output.object = f"🔥 Fires today: **{count}**"

    elif "total" in query:
        query_output.object = f"🌍 Total fires: **{len(df)}**"

    else:
        query_output.object = "Try: 'fires today' or 'total fires'"

query_box.param.watch(update_query, 'value')

# =========================
# LAYOUT
# =========================
header = pn.pane.Markdown("""
# 🌍 Wildfire Intelligence Dashboard
### Advanced geospatial wildfire analytics
""", styles={'text-align': 'center'})

controls = pn.Row(date_slider, country_select, query_box)

tabs = pn.Tabs(
    ("🌍 Map", map_plot),
    ("📈 Trends", trend_plot),
    ("🔥 Hotspots", hotspots_panel),
    ("🧠 Insights", insights_panel)
)

dashboard = pn.Column(
    header,
    pn.Spacer(height=10),
    controls,
    pn.Spacer(height=10),
    query_output,
    pn.Spacer(height=10),
    metrics_panel,
    pn.Spacer(height=15),
    tabs
)

dashboard.servable()