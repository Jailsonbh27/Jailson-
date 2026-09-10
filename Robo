import requests, time
from datetime import datetime

TOKEN = "8953782770:AAEpumyxo4QZ32Dyqf2jqweug-7_XN6Xr0Q"
CHAT_ID = "6206395904"

CRITERIO = {"tempo_min": 40, "chutes_min": 7, "nogol_min": 3, "posse_min": 60}
alertados = set()

def send(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "HTML"})

def get_matches():
    hoje = datetime.now().strftime("%Y%m%d")
    r = requests.get(f"https://www.fotmob.com/api/matches?date={hoje}", headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
    return r.json()

def get_details(mid):
    r = requests.get(f"https://www.fotmob.com/api/matchDetails?matchId={mid}", headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
    return r.json()

send("🤖 Robô AMASSO 1x1 ligado!\nCritério: empate 40min+ / 7 chutes / 3 no gol / 60% posse\nVou te avisar aqui!")
print("ROBÔ LIGADO")

while True:
    try:
        data = get_matches()
        live = []
        for liga in data.get("leagues", []):
            for m in liga.get("matches", []):
                if m.get("status", {}).get("liveTime"):
                    m["liga"] = liga["name"]
                    live.append(m)
        for mt in live:
            if mt["id"] in alertados: continue
            tempo_str = mt["status"]["liveTime"].get("short","0")
            tempo = int(''.join(filter(str.isdigit, tempo_str)) or 0)
            if tempo < CRITERIO["tempo_min"]: continue
            if mt["home"]["score"]!= mt["away"]["score"]: continue

            d = get_details(mt["id"])
            stats = d.get("content", {}).get("stats", {}).get("stats")
            if not stats: continue
            posse=ch=ng=0
            for s in stats:
                if s["title"] == "Ball possession": posse = max(int(s["stats"][0] or 0), int(s["stats"][1] or 0))
                if s["title"] == "Total shots": ch = max(int(s["stats"][0] or 0), int(s["stats"][1] or 0))
                if s["title"] == "Shots on target": ng = max(int(s["stats"][0] or 0), int(s["stats"][1] or 0))

            if ch >= 7 and ng >= 3 and posse >= 60:
                alertados.add(mt["id"])
                msg = f"🚨 <b>AMASSO DETECTADO</b>\n⚽ {mt['home']['name']} x {mt['away']['name']}\n📊 {mt['home']['score']}x{mt['away']['score']} aos {tempo}min - {mt['liga']}\n🔥 {ch} chutes, {ng} no gol, {posse}% posse\n💰 Odd Draw ~1.125\n⏰ {datetime.now().strftime('%H:%M')}"
                send(msg)
        time.sleep(40)
    except Exception as e:
        print(e)
        time.sleep(20)
