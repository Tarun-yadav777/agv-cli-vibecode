# FIFA World Cup 2026™ Match Tracker & Standings

A premium, modern dark-themed web application to track the official match results, upcoming fixtures, and live group standings for the **FIFA World Cup 2026™** (hosted across USA, Canada, and Mexico from June 11 to July 19, 2026). 

---

## 🚀 Features

*   **Official Finished Match Results**: Shows correct, real-world match outcomes from the opening match on June 11 up to June 17, including detail timelines (goals, yellow/red cards).
*   **Upcoming Scheduled Fixtures**: Displays scheduled upcoming matches for June 18 with exact local times, stadiums, and team matchups.
*   **Clean Flag Logos**: Utilizes a mapping to fetch sharp flag images from `flagcdn.com` styled as uniform, elegant rounded rectangular logos.
*   **Tabbed Group Standings**: Dynamically calculates and renders standings (Played, Won, Drawn, Lost, GD, Points) for all 11 active groups (Group A through Group K) using a space-saving horizontal tab navigation bar.
*   **Real-time Sync**: Features a sync button that makes an API call to fetch live match updates, with a graceful local cache fallback.

---

## 🛠️ Tech Stack

*   **Backend**: Python, Flask (for server routing, JSON state loading, and standings sorting)
*   **Frontend Structure & Styles**: HTML5, Vanilla CSS3 (custom dark Midnight-blue theme, glassmorphism, responsive grid layout)
*   **Frontend Logic**: Vanilla JavaScript (ES6 fetch API for async updates and DOM manipulation)

---

## 🏗️ How it was Created

1.  **Project Initialization**: Set up a lightweight Flask application and installed the dependencies.
2.  **Core Data Modeling**: Modeled a JSON-based database structure (`state.json`) loaded with correct matches played during the initial week of the World Cup and upcoming fixtures.
3.  **Standings Processor**: Wrote a Python calculator that accumulates match statistics (Wins, Draws, Losses, Goals For/Against, Goal Difference, Points) for each group and sorts them according to official FIFA criteria.
4.  **UI Design**: 
    *   Designed a premium, immersive sport-dashboard dashboard layout with glowing indicators and glassmorphism.
    *   Replaced gradient badges with circular/rounded national flags using ISO-2 letter country mapping.
    *   Engineered a horizontal tab navigation for group standings to make the sidebar compact and clean.
5.  **Git Integration**: Created a `.gitignore` file, initialized Git, committed the code, and pushed the repository to GitHub.

---

## ⚙️ Getting Started

### Prerequisites
*   Python 3.10 or higher
*   pip (Python package manager)

### Installation & Run
1. Clone this repository (or copy the project directory):
   ```bash
   git clone https://github.com/Tarun-yadav777/agv-cli-vibecode.git
   cd agv-cli-vibecode
   ```
2. Install Flask:
   ```bash
   pip install flask
   ```
3. Run the development server:
   ```bash
   python app.py
   ```
4. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```
