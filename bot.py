import requests, time
from datetime import datetime

TOKEN="8953782770:AAEpumyxo4QZ32Dyqf2jqweug-7_XN6XrOQ"
CHAT_ID="6206395904"

CRITERIO = {"tempo_min": 40, "chutes_min": 7}
alertados = set()

def enviar(msg):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "HTML"}, timeout=10)
    except:
        pass

def get_matches():
    hoje = datetime.now().strftime("%Y%m%d")
    url = f"https://www.fotmob.com/api/matches?date={hoje}"
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
    return r.json()

def get_detalhes(match_id):
    url = f"https://www.fotmob.com/api/matchDetails?matchId={match_id}"
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
    return r.json()

enviar("🤖 <b>Robô AMASSO 1x1 LIGADO!</b>\n\n✅ Critério: Empate 40min+\n✅ 7 chutes+\n✅ 0x0")
print("ROBO LIGADO - AMASSO 1x1")

while True:
    try:
        dados = get_matches()
        ao_vivo = []
        for liga in dados.get("leagues", []):
            for m in liga.get("matches", []):
                if m.get("status", {}).get("liveTime"):
                    m["liga_nome"] = liga["name"]
                    ao_vivo.append(m)

        for mt in ao_vivo:
            mid = mt["id"]
            if mid in alertados:
                continue

            tempo_str = mt["status"]["liveTime"].get("short", "0")
            tempo = int("".join(filter(str.isdigit, tempo_str)) or 0)

            if tempo < CRITERIO["tempo_min"]:
                continue

            if mt["home"]["score"]!= mt["away"]["score"]:
                continue

            if mt["home"]["score"]!= 0:
                continue

            det = get_detalhes(mid)
            stats = det.get("content", {}).get("stats", {}).get("stats", [])
            chutes = 0
            for s in stats:
                if "Total shots" in s.get("title", "") or "Chutes" in s.get("title", ""):
                    chutes = int(s["stats"][0] or 0) + int(s["stats"][1] or 0)
                    break

            if chutes < CRITERIO["chutes_min"]:
                continue

            msg = f"⚽ <b>AMASSO 1x1 ACHADO!</b>\n\n🏟️ {mt['liga_nome']}\n{mt['home']['name']} {mt['home']['score']}x{mt['away']['score']} {mt['away']['name']}\n\n⏱️ {tempo}' de jogo\n🎯 Chutes: {chutes}\n💰 <b>ENTRADA: Próximo Gol Casa ou Empate Anula!</b>"
            enviar(msg)
            alertados.add(mid)
            print(f"Alerta: {mt['home']['name']} x {mt['away']['name']}")

        time.sleep(60)

    except Exception as e:
        print(f"Erro: {e}")
        time.sleep(60)
