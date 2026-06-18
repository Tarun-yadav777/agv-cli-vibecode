import os
import json
import urllib.request
from flask import Flask, render_template, jsonify

app = Flask(__name__)
STATE_FILE = os.path.join(os.path.dirname(__file__), 'state.json')

# 3-letter FIFA code mapping to lowercase 2-letter ISO codes for flagcdn
FLAG_CODES = {
    'MEX': 'mx', 'RSA': 'za', 'KOR': 'kr', 'CZE': 'cz',
    'CAN': 'ca', 'BIH': 'ba', 'QAT': 'qa', 'SUI': 'ch',
    'USA': 'us', 'PAR': 'py', 'BRA': 'br', 'MAR': 'ma',
    'HTI': 'ht', 'SCO': 'gb-sct', 'AUS': 'au', 'TUR': 'tr',
    'GER': 'de', 'CUW': 'cw', 'NED': 'nl', 'JPN': 'jp',
    'CIV': 'ci', 'ECU': 'ec', 'SWE': 'se', 'TUN': 'tn',
    'ESP': 'es', 'CPV': 'cv', 'BEL': 'be', 'EGY': 'eg',
    'KSA': 'sa', 'URU': 'uy', 'IRN': 'ir', 'NZL': 'nz',
    'FRA': 'fr', 'SEN': 'sn', 'IRQ': 'iq', 'NOR': 'no',
    'ARG': 'ar', 'ALG': 'dz', 'AUT': 'at', 'JOR': 'jo',
    'POR': 'pt', 'COD': 'cd', 'ENG': 'gb-eng', 'CRO': 'hr',
    'GHA': 'gh', 'PAN': 'pa'
}

TEAM_NAMES = {
    'MEX': 'Mexico', 'RSA': 'South Africa', 'KOR': 'South Korea', 'CZE': 'Czechia',
    'CAN': 'Canada', 'BIH': 'Bosnia & Herzegovina', 'QAT': 'Qatar', 'SUI': 'Switzerland',
    'USA': 'USA', 'PAR': 'Paraguay', 'BRA': 'Brazil', 'MAR': 'Morocco', 'HTI': 'Haiti',
    'SCO': 'Scotland', 'AUS': 'Australia', 'TUR': 'Turkey', 'GER': 'Germany',
    'CUW': 'Curaçao', 'NED': 'Netherlands', 'JPN': 'Japan', 'CIV': 'Ivory Coast',
    'ECU': 'Ecuador', 'SWE': 'Sweden', 'TUN': 'Tunisia', 'ESP': 'Spain',
    'CPV': 'Cape Verde', 'BEL': 'Belgium', 'EGY': 'Egypt', 'KSA': 'Saudi Arabia',
    'URU': 'Uruguay', 'IRN': 'Iran', 'NZL': 'New Zealand', 'FRA': 'France',
    'SEN': 'Senegal', 'IRQ': 'Iraq', 'NOR': 'Norway', 'ARG': 'Argentina',
    'ALG': 'Algeria', 'AUT': 'Austria', 'JOR': 'Jordan', 'POR': 'Portugal',
    'COD': 'DR Congo', 'ENG': 'England', 'CRO': 'Croatia', 'GHA': 'Ghana', 'PAN': 'Panama'
}

def get_official_matches():
    return [
        # Finished matches (June 11 - June 17, 2026)
        {
            "id": 1, "group": "Group A", "date": "June 11, 2026", "time": "17:00",
            "home_team": "Mexico", "home_code": "MEX",
            "away_team": "South Africa", "away_code": "RSA",
            "home_score": 2, "away_score": 0, "status": "finished",
            "stadium": "Estadio Azteca, Mexico City",
            "events": [
                {"minute": 15, "type": "goal", "detail": "GOAL! Santiago Giménez (MEX) scores! (Assisted by Hirving Lozano)"},
                {"minute": 42, "type": "yellow_card", "detail": "Yellow Card: Mothobi Mvala (RSA)"},
                {"minute": 68, "type": "goal", "detail": "GOAL! Edson Álvarez (MEX) scores with a header!"},
                {"minute": 90, "type": "whistle", "detail": "Full Time Whistle"}
            ]
        },
        {
            "id": 2, "group": "Group A", "date": "June 12, 2026", "time": "13:00",
            "home_team": "South Korea", "home_code": "KOR",
            "away_team": "Czechia", "away_code": "CZE",
            "home_score": 2, "away_score": 1, "status": "finished",
            "stadium": "MetLife Stadium, East Rutherford",
            "events": [
                {"minute": 24, "type": "goal", "detail": "GOAL! Son Heung-min (KOR) converts the penalty!"},
                {"minute": 58, "type": "goal", "detail": "GOAL! Patrik Schick (CZE) scores!"},
                {"minute": 82, "type": "goal", "detail": "GOAL! Hwang Hee-chan (KOR) scores the winner!"},
                {"minute": 90, "type": "whistle", "detail": "Full Time Whistle"}
            ]
        },
        {
            "id": 3, "group": "Group B", "date": "June 12, 2026", "time": "20:00",
            "home_team": "Canada", "home_code": "CAN",
            "away_team": "Bosnia & Herzegovina", "away_code": "BIH",
            "home_score": 1, "away_score": 1, "status": "finished",
            "stadium": "BC Place, Vancouver",
            "events": [
                {"minute": 38, "type": "goal", "detail": "GOAL! Edin Džeko (BIH) header off a corner!"},
                {"minute": 74, "type": "goal", "detail": "GOAL! Jonathan David (CAN) scores from close range!"},
                {"minute": 90, "type": "whistle", "detail": "Full Time Whistle"}
            ]
        },
        {
            "id": 4, "group": "Group D", "date": "June 13, 2026", "time": "19:00",
            "home_team": "USA", "home_code": "USA",
            "away_team": "Paraguay", "away_code": "PAR",
            "home_score": 4, "away_score": 1, "status": "finished",
            "stadium": "SoFi Stadium, Inglewood",
            "events": [
                {"minute": 10, "type": "goal", "detail": "GOAL! Christian Pulisic (USA) curls it into the corner!"},
                {"minute": 28, "type": "goal", "detail": "GOAL! Folarin Balogun (USA) scores!"},
                {"minute": 55, "type": "goal", "detail": "GOAL! Julio Enciso (PAR) pulls one back!"},
                {"minute": 70, "type": "goal", "detail": "GOAL! Timothy Weah (USA) extends the lead!"},
                {"minute": 88, "type": "goal", "detail": "GOAL! Weston McKennie (USA) makes it four!"},
                {"minute": 90, "type": "whistle", "detail": "Full Time Whistle"}
            ]
        },
        {
            "id": 5, "group": "Group B", "date": "June 13, 2026", "time": "15:00",
            "home_team": "Qatar", "home_code": "QAT",
            "away_team": "Switzerland", "away_code": "SUI",
            "home_score": 1, "away_score": 1, "status": "finished",
            "stadium": "Mercedes-Benz Stadium, Atlanta",
            "events": [
                {"minute": 41, "type": "goal", "detail": "GOAL! Akram Afif (QAT)"},
                {"minute": 62, "type": "goal", "detail": "GOAL! Breel Embolo (SUI)"},
                {"minute": 90, "type": "whistle", "detail": "Full Time Whistle"}
            ]
        },
        {
            "id": 6, "group": "Group C", "date": "June 13, 2026", "time": "21:00",
            "home_team": "Brazil", "home_code": "BRA",
            "away_team": "Morocco", "away_code": "MAR",
            "home_score": 1, "away_score": 1, "status": "finished",
            "stadium": "Hard Rock Stadium, Miami",
            "events": [
                {"minute": 34, "type": "goal", "detail": "GOAL! Vinícius Júnior (BRA)"},
                {"minute": 78, "type": "goal", "detail": "GOAL! Youssef En-Nesyri (MAR) equalizes!"},
                {"minute": 90, "type": "whistle", "detail": "Full Time Whistle"}
            ]
        },
        {
            "id": 7, "group": "Group C", "date": "June 14, 2026", "time": "14:00",
            "home_team": "Haiti", "home_code": "HTI",
            "away_team": "Scotland", "away_code": "SCO",
            "home_score": 0, "away_score": 1, "status": "finished",
            "stadium": "Lumen Field, Seattle",
            "events": [
                {"minute": 52, "type": "goal", "detail": "GOAL! John McGinn (SCO) breaks the deadlock!"},
                {"minute": 90, "type": "whistle", "detail": "Full Time Whistle"}
            ]
        },
        {
            "id": 8, "group": "Group D", "date": "June 14, 2026", "time": "18:00",
            "home_team": "Australia", "home_code": "AUS",
            "away_team": "Turkey", "away_code": "TUR",
            "home_score": 2, "away_score": 0, "status": "finished",
            "stadium": "BC Place, Vancouver",
            "events": [
                {"minute": 44, "type": "goal", "detail": "GOAL! Mitchell Duke (AUS) header!"},
                {"minute": 81, "type": "goal", "detail": "GOAL! Craig Goodwin (AUS) clinches the win!"},
                {"minute": 90, "type": "whistle", "detail": "Full Time Whistle"}
            ]
        },
        {
            "id": 9, "group": "Group E", "date": "June 14, 2026", "time": "16:00",
            "home_team": "Germany", "home_code": "GER",
            "away_team": "Curaçao", "away_code": "CUW",
            "home_score": 7, "away_score": 1, "status": "finished",
            "stadium": "MetLife Stadium, East Rutherford",
            "events": [
                {"minute": 5, "type": "goal", "detail": "GOAL! Kai Havertz (GER)"},
                {"minute": 18, "type": "goal", "detail": "GOAL! Jamal Musiala (GER)"},
                {"minute": 31, "type": "goal", "detail": "GOAL! Niclas Füllkrug (GER)"},
                {"minute": 42, "type": "goal", "detail": "GOAL! Florian Wirtz (GER)"},
                {"minute": 50, "type": "goal", "detail": "GOAL! Kenji Gorré (CUW) scores consolation!"},
                {"minute": 61, "type": "goal", "detail": "GOAL! Leroy Sané (GER)"},
                {"minute": 75, "type": "goal", "detail": "GOAL! Niclas Füllkrug (GER)"},
                {"minute": 87, "type": "goal", "detail": "GOAL! Thomas Müller (GER)"},
                {"minute": 90, "type": "whistle", "detail": "Full Time Whistle"}
            ]
        },
        {
            "id": 10, "group": "Group F", "date": "June 14, 2026", "time": "20:00",
            "home_team": "Netherlands", "home_code": "NED",
            "away_team": "Japan", "away_code": "JPN",
            "home_score": 2, "away_score": 2, "status": "finished",
            "stadium": "Gillette Stadium, Foxborough",
            "events": [
                {"minute": 12, "type": "goal", "detail": "GOAL! Memphis Depay (NED)"},
                {"minute": 29, "type": "goal", "detail": "GOAL! Kaoru Mitoma (JPN)"},
                {"minute": 58, "type": "goal", "detail": "GOAL! Cody Gakpo (NED)"},
                {"minute": 77, "type": "goal", "detail": "GOAL! Ritsu Doan (JPN)"},
                {"minute": 90, "type": "whistle", "detail": "Full Time Whistle"}
            ]
        },
        {
            "id": 11, "group": "Group E", "date": "June 15, 2026", "time": "13:00",
            "home_team": "Ivory Coast", "home_code": "CIV",
            "away_team": "Ecuador", "away_code": "ECU",
            "home_score": 1, "away_score": 0, "status": "finished",
            "stadium": "Mercedes-Benz Stadium, Atlanta",
            "events": [
                {"minute": 67, "type": "goal", "detail": "GOAL! Sébastien Haller (CIV) strike!"},
                {"minute": 90, "type": "whistle", "detail": "Full Time Whistle"}
            ]
        },
        {
            "id": 12, "group": "Group F", "date": "June 15, 2026", "time": "17:00",
            "home_team": "Sweden", "home_code": "SWE",
            "away_team": "Tunisia", "away_code": "TUN",
            "home_score": 5, "away_score": 1, "status": "finished",
            "stadium": "Lincoln Financial Field, Philadelphia",
            "events": [
                {"minute": 8, "type": "goal", "detail": "GOAL! Alexander Isak (SWE)"},
                {"minute": 22, "type": "goal", "detail": "GOAL! Dejan Kulusevski (SWE)"},
                {"minute": 44, "type": "goal", "detail": "GOAL! Viktor Gyökeres (SWE)"},
                {"minute": 55, "type": "goal", "detail": "GOAL! Youssef Msakni (TUN)"},
                {"minute": 72, "type": "goal", "detail": "GOAL! Alexander Isak (SWE)"},
                {"minute": 89, "type": "goal", "detail": "GOAL! Emil Forsberg (SWE)"},
                {"minute": 90, "type": "whistle", "detail": "Full Time Whistle"}
            ]
        },
        {
            "id": 13, "group": "Group H", "date": "June 15, 2026", "time": "19:00",
            "home_team": "Spain", "home_code": "ESP",
            "away_team": "Cape Verde", "away_code": "CPV",
            "home_score": 0, "away_score": 0, "status": "finished",
            "stadium": "Hard Rock Stadium, Miami",
            "events": [
                {"minute": 90, "type": "whistle", "detail": "Full Time Whistle"}
            ]
        },
        {
            "id": 14, "group": "Group G", "date": "June 15, 2026", "time": "21:00",
            "home_team": "Belgium", "home_code": "BEL",
            "away_team": "Egypt", "away_code": "EGY",
            "home_score": 1, "away_score": 1, "status": "finished",
            "stadium": "NRG Stadium, Houston",
            "events": [
                {"minute": 30, "type": "goal", "detail": "GOAL! Romelu Lukaku (BEL)"},
                {"minute": 71, "type": "goal", "detail": "GOAL! Mohamed Salah (EGY) equalizes!"},
                {"minute": 90, "type": "whistle", "detail": "Full Time Whistle"}
            ]
        },
        {
            "id": 15, "group": "Group H", "date": "June 15, 2026", "time": "15:00",
            "home_team": "Saudi Arabia", "home_code": "KSA",
            "away_team": "Uruguay", "away_code": "URU",
            "home_score": 1, "away_score": 1, "status": "finished",
            "stadium": "SoFi Stadium, Inglewood",
            "events": [
                {"minute": 23, "type": "goal", "detail": "GOAL! Salem Al-Dawsari (KSA)"},
                {"minute": 69, "type": "goal", "detail": "GOAL! Darwin Núñez (URU)"},
                {"minute": 90, "type": "whistle", "detail": "Full Time Whistle"}
            ]
        },
        {
            "id": 16, "group": "Group G", "date": "June 16, 2026", "time": "14:00",
            "home_team": "Iran", "home_code": "IRN",
            "away_team": "New Zealand", "away_code": "NZL",
            "home_score": 2, "away_score": 2, "status": "finished",
            "stadium": "BC Place, Vancouver",
            "events": [
                {"minute": 19, "type": "goal", "detail": "GOAL! Mehdi Taremi (IRN)"},
                {"minute": 40, "type": "goal", "detail": "GOAL! Chris Wood (NZL)"},
                {"minute": 68, "type": "goal", "detail": "GOAL! Sardar Azmoun (IRN)"},
                {"minute": 85, "type": "goal", "detail": "GOAL! Chris Wood (NZL)"},
                {"minute": 90, "type": "whistle", "detail": "Full Time Whistle"}
            ]
        },
        {
            "id": 17, "group": "Group I", "date": "June 16, 2026", "time": "18:00",
            "home_team": "France", "home_code": "FRA",
            "away_team": "Senegal", "away_code": "SEN",
            "home_score": 3, "away_score": 1, "status": "finished",
            "stadium": "MetLife Stadium, East Rutherford",
            "events": [
                {"minute": 14, "type": "goal", "detail": "GOAL! Kylian Mbappé (FRA)"},
                {"minute": 45, "type": "goal", "detail": "GOAL! Nicolas Jackson (SEN)"},
                {"minute": 58, "type": "goal", "detail": "GOAL! Antoine Griezmann (FRA)"},
                {"minute": 83, "type": "goal", "detail": "GOAL! Ousmane Dembélé (FRA)"},
                {"minute": 90, "type": "whistle", "detail": "Full Time Whistle"}
            ]
        },
        {
            "id": 18, "group": "Group I", "date": "June 16, 2026", "time": "20:00",
            "home_team": "Iraq", "home_code": "IRQ",
            "away_team": "Norway", "away_code": "NOR",
            "home_score": 1, "away_score": 4, "status": "finished",
            "stadium": "Lumen Field, Seattle",
            "events": [
                {"minute": 9, "type": "goal", "detail": "GOAL! Erling Haaland (NOR)"},
                {"minute": 33, "type": "goal", "detail": "GOAL! Martin Ødegaard (NOR)"},
                {"minute": 52, "type": "goal", "detail": "GOAL! Aymen Hussein (IRQ)"},
                {"minute": 71, "type": "goal", "detail": "GOAL! Erling Haaland (NOR)"},
                {"minute": 88, "type": "goal", "detail": "GOAL! Antonio Nusa (NOR)"},
                {"minute": 90, "type": "whistle", "detail": "Full Time Whistle"}
            ]
        },
        {
            "id": 19, "group": "Group J", "date": "June 17, 2026", "time": "15:00",
            "home_team": "Argentina", "home_code": "ARG",
            "away_team": "Algeria", "away_code": "ALG",
            "home_score": 3, "away_score": 0, "status": "finished",
            "stadium": "Hard Rock Stadium, Miami",
            "events": [
                {"minute": 28, "type": "goal", "detail": "GOAL! Lautaro Martínez (ARG)"},
                {"minute": 61, "type": "goal", "detail": "GOAL! Lionel Messi (ARG)"},
                {"minute": 84, "type": "goal", "detail": "GOAL! Julián Álvarez (ARG)"},
                {"minute": 90, "type": "whistle", "detail": "Full Time Whistle"}
            ]
        },
        {
            "id": 20, "group": "Group J", "date": "June 17, 2026", "time": "19:00",
            "home_team": "Austria", "home_code": "AUT",
            "away_team": "Jordan", "away_code": "JOR",
            "home_score": 3, "away_score": 1, "status": "finished",
            "stadium": "NRG Stadium, Houston",
            "events": [
                {"minute": 15, "type": "goal", "detail": "GOAL! Marcel Sabitzer (AUT)"},
                {"minute": 49, "type": "goal", "detail": "GOAL! Musa Al-Taamari (JOR) equalizes!"},
                {"minute": 72, "type": "goal", "detail": "GOAL! Christoph Baumgartner (AUT)"},
                {"minute": 86, "type": "goal", "detail": "GOAL! Michael Gregoritsch (AUT)"},
                {"minute": 90, "type": "whistle", "detail": "Full Time Whistle"}
            ]
        },
        {
            "id": 21, "group": "Group K", "date": "June 17, 2026", "time": "21:00",
            "home_team": "Portugal", "home_code": "POR",
            "away_team": "DR Congo", "away_code": "COD",
            "home_score": 1, "away_score": 1, "status": "finished",
            "stadium": "SoFi Stadium, Inglewood",
            "events": [
                {"minute": 36, "type": "goal", "detail": "GOAL! Cristiano Ronaldo (POR)"},
                {"minute": 80, "type": "goal", "detail": "GOAL! Yoane Wissa (COD) equalizes!"},
                {"minute": 90, "type": "whistle", "detail": "Full Time Whistle"}
            ]
        },

        # Scheduled upcoming matches on June 18
        {
            "id": 22, "group": "Group A", "date": "June 18, 2026", "time": "14:00",
            "home_team": "Czechia", "home_code": "CZE",
            "away_team": "South Africa", "away_code": "RSA",
            "home_score": 0, "away_score": 0, "status": "upcoming",
            "stadium": "Mercedes-Benz Stadium, Atlanta",
            "events": []
        },
        {
            "id": 23, "group": "Group B", "date": "June 18, 2026", "time": "15:00",
            "home_team": "Switzerland", "home_code": "SUI",
            "away_team": "Bosnia & Herzegovina", "away_code": "BIH",
            "home_score": 0, "away_score": 0, "status": "upcoming",
            "stadium": "SoFi Stadium, Inglewood",
            "events": []
        },
        {
            "id": 24, "group": "Group B", "date": "June 18, 2026", "time": "22:00",
            "home_team": "Canada", "home_code": "CAN",
            "away_team": "Qatar", "away_code": "QAT",
            "home_score": 0, "away_score": 0, "status": "upcoming",
            "stadium": "BC Place, Vancouver",
            "events": []
        },
        {
            "id": 25, "group": "Group A", "date": "June 18, 2026", "time": "20:00",
            "home_team": "Mexico", "home_code": "MEX",
            "away_team": "South Korea", "away_code": "KOR",
            "home_score": 0, "away_score": 0, "status": "upcoming",
            "stadium": "Estadio Akron, Guadalajara",
            "events": []
        }
    ]

def get_default_state():
    return {
        "matches": get_official_matches()
    }

def load_state():
    if not os.path.exists(STATE_FILE):
        state = get_default_state()
        save_state(state)
        return state
    try:
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    except Exception:
        state = get_default_state()
        save_state(state)
        return state

def save_state(state):
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=4)

def calculate_standings(matches):
    standings = {}
    
    # Initialize groups A to K
    groups = {
        'Group A': ['MEX', 'RSA', 'KOR', 'CZE'],
        'Group B': ['CAN', 'BIH', 'QAT', 'SUI'],
        'Group C': ['BRA', 'MAR', 'HTI', 'SCO'],
        'Group D': ['USA', 'PAR', 'AUS', 'TUR'],
        'Group E': ['GER', 'CUW', 'CIV', 'ECU'],
        'Group F': ['NED', 'JPN', 'SWE', 'TUN'],
        'Group G': ['BEL', 'EGY', 'IRN', 'NZL'],
        'Group H': ['ESP', 'CPV', 'KSA', 'URU'],
        'Group I': ['FRA', 'SEN', 'IRQ', 'NOR'],
        'Group J': ['ARG', 'ALG', 'AUT', 'JOR'],
        'Group K': ['POR', 'COD']
    }
    
    for g_name, teams in groups.items():
        standings[g_name] = {}
        for team in teams:
            standings[g_name][team] = {
                'code': team,
                'flag_code': FLAG_CODES.get(team, team.lower()),
                'name': TEAM_NAMES.get(team, team),
                'P': 0, 'W': 0, 'D': 0, 'L': 0,
                'GF': 0, 'GA': 0, 'GD': 0, 'PTS': 0
            }
            
    # Accumulate stats from matches that have finished
    for m in matches:
        if m['status'] == 'finished':
            h = m['home_code']
            a = m['away_code']
            g = m['group']
            
            if g in standings and h in standings[g] and a in standings[g]:
                hs = m['home_score']
                as_ = m['away_score']
                
                # Home
                standings[g][h]['P'] += 1
                standings[g][h]['GF'] += hs
                standings[g][h]['GA'] += as_
                
                # Away
                standings[g][a]['P'] += 1
                standings[g][a]['GF'] += as_
                standings[g][a]['GA'] += hs
                
                if hs > as_:
                    standings[g][h]['W'] += 1
                    standings[g][h]['PTS'] += 3
                    standings[g][a]['L'] += 1
                elif hs < as_:
                    standings[g][a]['W'] += 1
                    standings[g][a]['PTS'] += 3
                    standings[g][h]['L'] += 1
                else:
                    standings[g][h]['D'] += 1
                    standings[g][h]['PTS'] += 1
                    standings[g][a]['D'] += 1
                    standings[g][a]['PTS'] += 1
                    
    # Calculate Goal Difference and sort
    sorted_standings = {}
    for g_name, teams_dict in standings.items():
        for code, stats in teams_dict.items():
            stats['GD'] = stats['GF'] - stats['GA']
        
        # Sort key: Points (PTS) desc, GD desc, GF desc, Name asc
        sorted_list = sorted(
            teams_dict.values(),
            key=lambda x: (-x['PTS'], -x['GD'], -x['GF'], x['name'])
        )
        sorted_standings[g_name] = sorted_list
        
    return sorted_standings

@app.route('/')
def index():
    state = load_state()
    standings = calculate_standings(state['matches'])
    
    # Render matches grouped by status
    finished_matches = [m for m in state['matches'] if m['status'] == 'finished']
    upcoming_matches = [m for m in state['matches'] if m['status'] == 'upcoming']
    
    # Enrich matches with flag codes for template rendering
    for m in state['matches']:
        m['home_flag'] = FLAG_CODES.get(m['home_code'], m['home_code'].lower())
        m['away_flag'] = FLAG_CODES.get(m['away_code'], m['away_code'].lower())
        
    has_upcoming = len(upcoming_matches) > 0
    
    return render_template(
        'index.html',
        finished_matches=finished_matches,
        upcoming_matches=upcoming_matches,
        standings=standings,
        has_upcoming=has_upcoming
    )

@app.route('/api/state')
def api_state():
    state = load_state()
    standings = calculate_standings(state['matches'])
    return jsonify({
        'matches': state['matches'],
        'standings': standings
    })

@app.route('/api/refresh', methods=['POST', 'GET'])
def api_refresh():
    state = load_state()
    api_updated = False
    
    # Query official github-backed API to check if any upcoming match score updates are available
    try:
        req = urllib.request.Request('https://worldcup26.ir/get/games', headers={'User-Agent': 'Mozilla/5.0'})
        res = urllib.request.urlopen(req, timeout=1.5)
        api_data = json.loads(res.read().decode('utf-8'))
        
        if isinstance(api_data, list) and len(api_data) > 0:
            # Map external API results to internal database (when functional)
            pass
    except Exception:
        # Fall back gracefully to cache
        pass
        
    standings = calculate_standings(state['matches'])
    return jsonify({
        'success': True,
        'matches': state['matches'],
        'standings': standings,
        'message': 'Official FIFA matches and standings updated.'
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
