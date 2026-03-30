<div align="center">

🌍 Wildfire Intelligence Command Center

Mission-Critical Geospatial Analytics & Thermal Anomaly Detection

Transforming millions of raw NASA satellite telemetry points into real-time, actionable climate intelligence without browser latency.

</div>

📸 Visual Showcase

<div align="center">
<img src="assets/hero-dashboard.jpg" alt="Global Wildfire Command Dashboard" width="800" style="border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);"/>





<em>Global View: Real-time threat mapping, automated briefings, and critical metric KPIs.</em>
</div>

📍 Localized Threat Analysis

🌍 Global Data Render

<img src="assets/india-view.jpg" alt="India View with NASA telemetry" width="400" style="border-radius: 8px;"/>

<img src="assets/global-map.jpg" alt="Global Map Render" width="400" style="border-radius: 8px;"/>

High-fidelity point rendering over localized geographic zones.

Extreme-scale rendering of global thermal anomalies.

🧠 The Problem Statement

Global thermal anomalies are escalating at an unprecedented rate. Environmental agencies, first responders, and climate scientists process millions of data points daily from NASA's VIIRS and MODIS satellites.

However, traditional web dashboards crash or severely lag when attempting to plot datasets exceeding 50,000 geospatial points. Decision-makers are forced to choose between granular data resolution and application stability.

💡 The Solution

The Wildfire Intelligence Dashboard bridges the gap between massive data scale and interactive user experience. Built entirely in Python, it acts as a high-performance web application utilizing server-side rasterization (Datashader) to render millions of data points into a single image instantly, bypassing browser DOM limitations.

Coupled with a reactive UI framework (Panel) and hybrid rendering pipelines, it provides an elite analytical environment capable of handling global-scale climate datasets seamlessly.

⚡ Core Features

🗺️ Hybrid Rendering Engine: Dynamically switches between high-fidelity dynamic vector points (for localized views < 100k points) and ultra-fast Datashader rasterization (for global scale > 100k points).

🧠 Automated Insights Generation: Algorithmically calculates period-over-period percentage shifts in fire activity, providing users with instant, readable executive briefings.

🔎 NLP-Lite Query Copilot: A text-based rapid query system allowing users to type natural language commands like "fires today" or "total fires" to extract instant metrics.

🎛️ Reactive Filtering Pipeline: Multi-dimensional cross-filtering by temporal windows and geographical regions.

📍 Critical Hotspot Detection: Automatically groups and ranks geospatial coordinates by intensity score to identify severe, concentrated fire clusters.

🛡️ Zero-Crash Fail-Safe Architecture: Built-in resilience. If external datasets fail to load or are missing, the system autonomously triggers a synthetic data generator to ensure the UI remains live and testable.

🏗️ System Architecture

The dashboard is built on a modern, reactive Python architecture designed for extreme scale:

Data Ingestion Layer (pandas):
Aggregates and cleans CSV chunks. Includes an autonomous fallback protocol that generates statistically realistic NumPy distributions if source files are missing.

Reactive State Binding (pn.bind):
A declarative dependency graph. Functions do not manually redraw the screen; instead, visualization layers automatically re-evaluate only when their dependent widgets (Date Slider, Country Select) experience state mutations.

Rendering Layer (hvPlot & Datashader):

Vector Mode: Renders coordinates with dynamic size scaling mapped to Fire Radiative Power (FRP) alongside hover telemetry.

Raster Mode: Datashader aggregates points into pixels on the server, sending a lightweight PNG to the client.

Presentation Layer (Panel FastListTemplate):
Responsive, premium dark/light mode adaptable UI shell utilizing CSS Grid and Flexbox for mobile-ready analytics.

🛠️ Installation & Execution

Prerequisites

Python 3.9 or higher

Git installed on your machine

1. Clone the Repository

Open your terminal and clone the repository. (Note: Run this command only once to avoid creating nested folders!)

git clone [https://github.com/VarshVishwakarma/wildfire-intelligence-dashboard.git](https://github.com/VarshVishwakarma/wildfire-intelligence-dashboard.git)
cd wildfire-intelligence-dashboard


2. Set Up a Virtual Environment (Recommended)

Keep your global Python environment clean by creating a dedicated virtual environment.

Windows:

python -m venv venv
venv\Scripts\activate


macOS/Linux:

python3 -m venv venv
source venv/bin/activate


3. Install Dependencies

pip install -r requirements.txt


4. Setup Data (Optional)

By default, the dashboard features a "Zero-Crash Protocol" and will generate 5,000 realistic sample data points if no NASA data is found.

To use real NASA FIRMS data:

Create a data folder in the root directory: mkdir data

Place your downloaded NASA .csv files inside the data folder.

5. Launch the Command Center

Start the Panel server. The --show flag will automatically open the dashboard in your default web browser.

python -m panel serve app.py --show


📂 Project Structure

wildfire-intelligence-dashboard/
├── data/                      # Directory for NASA FIRMS CSVs (gitignored)
├── assets/                    # Static assets (images, icons for README)
├── app.py                     # Main application logic & reactive components
├── requirements.txt           # Python dependencies
├── .gitignore                 # Excludes heavy datasets and pycache
└── README.md                  # Project documentation


🔮 Roadmap & Future Enhancements

[ ] Real-time Streaming Integration: Connect directly to the NASA FIRMS live API feed instead of relying on static CSV loads.

[ ] AI-Powered Threat Prediction: Implement an XGBoost or LSTM model to forecast high-risk fire zones based on historical weather and thermal data.

[ ] Multi-Layer Overlays: Add wind direction, atmospheric temperature, and population density map layers.

[ ] Cloud Deployment: Containerize via Docker and deploy on AWS/GCP with a dedicated scalable backend.

🤝 Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated.

Fork the Project

Create your Feature Branch (git checkout -b feature/AmazingFeature)

Commit your Changes (git commit -m 'Add some AmazingFeature')

Push to the Branch (git push origin feature/AmazingFeature)

Open a Pull Request

<div align="center">

"Turning raw satellite telemetry into actionable global intelligence."

Designed with precision for top-tier geospatial analytics.

⭐ If you find this project impressive or useful, please consider giving it a star! ⭐

</div>
