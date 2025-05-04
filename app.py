from flask import Flask, render_template_string
import requests

app = Flask(__name__)

API_KEY = '790e1e128a7c7c9314980558d91bb4eb'
SPORT = 'basketball_nba'
REGION = 'us'
MARKET = 'h2h'

ODDS_API_URL = f'https://api.the-odds-api.com/v4/sports/{SPORT}/odds/?regions={REGION}&markets={MARKET}&apiKey={API_KEY}'

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>🏀 Prédictions NBA</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        h1 { color: #333366; }
        .match { border: 1px solid #ddd; padding: 10px; margin-bottom: 15px; border-radius: 5px; }
        .favorite { color: green; font-weight: bold; }
    </style>
</head>
<body>
    <h1>🏀 Prédictions NBA</h1>
    {% if matches %}
        {% for match in matches %}
            <div class="match">
                <p><strong>{{ match.teams[0] }} vs {{ match.teams[1] }}</strong></p>
                <p>Heure (UTC) : {{ match.start_time }}</p>
                <ul>
                    {% for team in match.teams_info %}
                        <li>{{ team.name }} → Cote : {{ team.odds }} | Probabilité : {{ team.probability }}%</li>
                    {% endfor %}
                </ul>
                <p class="favorite">🏆 Équipe favorite : {{ match.favorite }}</p>
            </div>
        {% endfor %}
    {% else %}
        <p>Aucun match disponible pour le moment.</p>
    {% endif %}
</body>
</html>
"""

def get_nba_predictions():
    try:
        response = requests.get(ODDS_API_URL)
        response.raise_for_status()
    except requests.RequestException:
        return []

    games = response.json()
    matches = []

    for game in games:
        teams = game.get('teams', [])
        start_time = game.get('commence_time', 'Inconnue')
        bookmakers = game.get('bookmakers', [])

        if len(teams) != 2 or not bookmakers:
            continue

        bookmaker = bookmakers[0]
        markets = bookmaker.get('markets', [])
        if not markets:
            continue

        outcomes = markets[0].get('outcomes', [])
        if len(outcomes) < 2:
            continue

        teams_info = []
        for outcome in outcomes:
            name = outcome.get('name')
            odds = outcome.get('price')
            if not name or not odds:
                continue
            probability = round((1 / odds) * 100, 2)
            teams_info.append({'name': name, 'odds': odds, 'probability': probability})

        if not teams_info:
            continue

        favorite = min(teams_info, key=lambda x: x['odds'])['name']

        matches.append({
            'teams': teams,
            'start_time': start_time,
            'teams_info': teams_info,
            'favorite': favorite
        })

    return matches

@app.route("/")
def index():
    matches = get_nba_predictions()
    return render_template_string(HTML_TEMPLATE, matches=matches)

if __name__ == "__main__":
    app.run(debug=True)
