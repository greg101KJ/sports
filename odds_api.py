import requests

# 👉 Remplace ta clé API ici (elle est déjà bonne normalement)
API_KEY = '790e1e128a7c7c9314980558d91bb4eb'

# ⚙️ Paramètres pour récupérer les cotes NBA
SPORT = 'basketball_nba'
REGION = 'us'
MARKET = 'h2h'  # Pari sur vainqueur du match

# 🌍 URL pour appeler l’API OddsAPI
ODDS_API_URL = f'https://api.the-odds-api.com/v4/sports/{SPORT}/odds/?regions={REGION}&markets={MARKET}&apiKey={API_KEY}'

def get_nba_predictions():
    try:
        response = requests.get(ODDS_API_URL)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Erreur de connexion à l'API OddsAPI : {e}")
        return

    games = response.json()

    if not games:
        print("Aucun match trouvé.")
        return

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

        print(f"\n🏀 Match : {teams[0]} vs {teams[1]}")
        print(f"🕒 Heure (UTC) : {start_time}")

        team_probs = []
        for outcome in outcomes:
            team = outcome.get('name')
            odds = outcome.get('price')

            if not team or not odds:
                continue

            prob = round((1 / odds) * 100, 2)
            team_probs.append((team, odds, prob))
            print(f"{team} → Cote : {odds} | Probabilité estimée : {prob} %")

        if not team_probs:
            continue

        favorite = min(team_probs, key=lambda x: x[1])
        print(f"🏆 Équipe favorite : {favorite[0]} (Cote : {favorite[1]}) → Probabilité : {favorite[2]} %")

if __name__ == "__main__":
    get_nba_predictions()

