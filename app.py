"""HealthMate - Your health. Your journey. Your community.
Python-only: Streamlit + SQLite + Pandas + Plotly + Pillow.
Run:  pip install -r requirements.txt  then  streamlit run app.py
"""
import hashlib, html, io, json, math, time, urllib.error, urllib.request, os, re, secrets, sqlite3, textwrap
from datetime import date, datetime, timedelta, time as dtime

import pandas as pd
import plotly.express as px
import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageOps

DB = "healthmate.db"
st.set_page_config(page_title="HealthMate", page_icon="⛏️", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Chakra+Petch:wght@500;600;700&family=Nunito:wght@400;600;700;800&display=swap');
:root{color-scheme:light;--bg:#f7f3e8;--paper:#fffdf7;--ink:#26352b;--muted:#6e7b70;--line:#d8ccb5;--grass:#6b9b54;--grass-dark:#426b3d;--sky:#dff2f7;--gold:#e0a43b;--dirt:#a8754f;--leaf:#dcebcf;--cloud:#fff8dc}
html,body,.stApp,button,input,textarea,select{font-family:'Nunito',sans-serif !important}.stApp{background-color:#dcefd1;color:var(--ink);background-image:linear-gradient(90deg,rgba(224,235,211,.96) 0 244px,rgba(247,243,232,.88) 244px),url('https://hebbkx1anhila5yf.public.blob.vercel-storage.com/b8999ea6a727587d6deed4d2c6e89715-Dtu8FPAUUbRwm0tCPSdB0EuIB21DUg.jpg');background-size:cover;background-position:center top;background-attachment:fixed}
.stApp p,.stApp label,.stApp li,.stApp span,.stApp small,[data-testid=stWidgetLabel] p{color:var(--ink)}[data-testid=stCaptionContainer],[data-testid=stCaptionContainer] *{color:var(--muted) !important}
h1,h2,h3,.big{font-family:'Chakra Petch',sans-serif !important;letter-spacing:-.02em;font-weight:700;color:var(--ink) !important}#MainMenu,footer{visibility:hidden;height:0}header[data-testid=stHeader]{height:3rem;background:rgba(247,243,232,.78);z-index:20}header[data-testid=stHeader] button{color:var(--grass-dark) !important;background:var(--paper);border:1px solid var(--line);border-radius:9px;margin:8px;box-shadow:0 2px 0 #d8ccb5}header[data-testid=stHeader] button:hover{background:#eaf3df}.stApp [data-testid=stSidebarCollapsedControl]{background:var(--grass);color:#fff;border-radius:9px;margin:8px;box-shadow:0 2px 0 var(--grass-dark)}.stApp [data-testid=stSidebarCollapsedControl] button{color:#fff !important}
[data-testid=stSidebar]{display:block;background:linear-gradient(180deg,#e5ead8,#dce8d2);border-right:2px solid #c9d7b9;width:220px !important;padding:24px 14px;box-shadow:4px 0 0 rgba(66,107,61,.06)}.block-container{padding:2rem 3rem;max-width:1180px}.top{display:flex;align-items:center;justify-content:flex-end;margin-bottom:18px}.top .brand{position:fixed;left:28px;top:22px;font-family:'Chakra Petch';font-size:1.35rem;font-weight:700;color:var(--grass-dark)}.top .brand i{color:var(--dirt);font-style:normal}.top .me{display:flex;gap:10px;align-items:center;background:var(--paper);border:1px solid var(--line);border-radius:12px;padding:5px 14px 5px 5px;font-weight:700}.top .me b{width:32px;height:32px;border-radius:8px;background:var(--grass);color:#fff;display:grid;place-items:center}
[data-testid=stSidebar] [data-testid=stRadio] label{border:0;border-radius:10px;padding:10px 12px;margin:3px 0;background:transparent;font-weight:700;cursor:pointer}[data-testid=stSidebar] [data-testid=stRadio] label:hover{background:#d9d0bd}[data-testid=stSidebar] [data-testid=stRadio] label:has(input:checked){background:var(--grass);box-shadow:0 3px 0 var(--grass-dark)}[data-testid=stSidebar] [data-testid=stRadio] label:has(input:checked) *{color:#fff !important}[data-testid=stSidebar] [data-testid=stRadio] label>div:first-child{display:none}
.stButton>button,.stDownloadButton>button,[data-testid=stFormSubmitButton]>button{background:var(--grass);color:#fff !important;border:0;border-radius:9px;padding:.55rem 1.2rem;font-weight:800;box-shadow:0 3px 0 var(--grass-dark)}.stButton>button:hover,[data-testid=stFormSubmitButton]>button:hover{background:var(--grass-dark)}.stButton>button p,[data-testid=stFormSubmitButton]>button p{color:#fff !important}
input,textarea,[data-baseweb=input],[data-baseweb=textarea],[data-baseweb=select]>div,[data-testid=stNumberInputContainer],[data-baseweb=base-input]{background:var(--paper) !important;color:var(--ink) !important;border-color:var(--line) !important;border-radius:9px !important}[data-baseweb=popover] *,[data-baseweb=menu]{background:var(--paper);color:var(--ink)}
[data-testid=stForm],[data-testid=stExpander],[data-testid=stChatMessage],[data-testid=stVerticalBlockBorderWrapper]{border:1px solid var(--line);border-radius:14px;background:var(--paper)}[data-testid=stPlotlyChart],[data-testid=stDataFrame]{background:var(--paper);border:1px solid var(--line);border-radius:14px;padding:8px}[data-testid=stImage] img{border-radius:12px}button[data-baseweb=tab]{color:var(--muted) !important;font-weight:800}button[data-baseweb=tab][aria-selected=true]{color:var(--grass-dark) !important}[data-baseweb=tab-highlight]{background:var(--grass) !important}
.hero,.b,.panel{background:var(--paper);border:1px solid var(--line);border-radius:14px;padding:24px;box-shadow:0 4px 0 #d8ccb5;position:relative}.hero{background:linear-gradient(135deg,#fffdf7 0%,#eef6df 100%);border-top:5px solid var(--grass)}.hero h1{margin:0;font-size:2.2rem}.b{height:100%;position:relative;overflow:hidden;margin-bottom:14px}.b.or{background:linear-gradient(145deg,var(--grass),#83ae62);border-color:var(--grass-dark);color:#fff}.b.or *{color:#fff !important}.b .k{color:var(--muted);font-size:.85rem;margin-bottom:6px}.b h1{font-size:2.3rem;margin:0 0 4px}.num{font-family:'Chakra Petch';font-size:4.2rem;font-weight:700;line-height:1}.xpbar{height:10px;background:#d9d0bd;border-radius:3px;overflow:hidden;margin-top:18px}.xpbar i{display:block;height:100%;background:var(--gold);border-radius:3px}.rings{display:flex;justify-content:space-around;gap:6px}.ring svg{width:96px}.rt{fill:none;stroke:#d9d0bd;stroke-width:9}.rf{fill:none;stroke:var(--grass);stroke-width:9;stroke-linecap:round}.ring text{fill:var(--ink);font-family:'Chakra Petch';font-weight:700;font-size:19px}.ring .rl{color:var(--muted);font-size:.8rem;text-align:center;margin-top:-4px}.quest{display:flex;gap:12px;align-items:center;padding:12px 16px;border-radius:10px;background:var(--paper);border:1px solid var(--line);margin-bottom:8px}.quest b{width:20px;height:20px;border-radius:5px;border:2px solid #b7b09f;flex:none}.quest.done{background:#edf3e9;border-color:#9cbb91}.quest.done b{background:var(--grass);border-color:var(--grass)}.quest span{margin-left:auto;color:var(--grass-dark);font-weight:800;font-size:.85rem}.card{background:var(--paper);border:1px solid var(--line);border-left:5px solid var(--grass);border-radius:10px;padding:12px 16px;margin-bottom:8px;box-shadow:0 2px 0 rgba(216,204,181,.6)}.quest{transition:transform .15s ease,box-shadow .15s ease}.quest:hover{transform:translateX(3px);box-shadow:0 3px 0 #d8ccb5}.pet-card{display:flex;overflow:hidden;margin:0 0 18px;border:1px solid var(--line);border-radius:16px;background:#fffdf7;box-shadow:0 4px 0 #d8ccb5}.pet-scene{position:relative;min-height:210px;flex:1.1;overflow:hidden;background:linear-gradient(#9bd8e8 0 48%,#b7dd7e 48% 100%)}.pixel-sun{position:absolute;right:14%;top:24px;width:58px;height:58px;border-radius:50%;background:#ffe9a9;box-shadow:0 0 0 10px rgba(255,239,171,.22)}.pixel-cloud{position:absolute;width:105px;height:26px;border-radius:22px;background:#fff8dc;opacity:.9}.pixel-cloud:before,.pixel-cloud:after{content:'';position:absolute;background:#fff8dc;border-radius:50%}.pixel-cloud:before{width:42px;height:42px;left:16px;top:-20px}.pixel-cloud:after{width:52px;height:52px;left:48px;top:-28px}.cloud-a{top:42px;left:12%}.cloud-b{top:88px;right:8%;transform:scale(.7)}.pixel-hill{position:absolute;bottom:-55px;width:120%;height:135px;border-radius:50% 50% 0 0}.hill-back{left:-28%;background:#7db568}.hill-front{left:22%;bottom:-78px;background:#6b9b54}.pet-cat{position:absolute;z-index:2;left:50%;bottom:40px;width:72px;height:70px;background:#c58a62;border:4px solid #704c3e;border-radius:22px 22px 16px 16px;transform:translateX(-50%);animation:cat-bob 2.8s ease-in-out infinite}.pet-cat:before,.pet-cat:after{content:'';position:absolute;top:-21px;width:24px;height:28px;background:#c58a62;border:4px solid #704c3e}.pet-cat:before{left:2px;transform:skewY(-24deg)}.pet-cat:after{right:2px;transform:skewY(24deg)}.pet-cat i,.pet-cat b{position:absolute;top:25px;width:7px;height:7px;border-radius:50%;background:#26352b}.pet-cat i{left:18px}.pet-cat b{right:18px}.pet-cat em{position:absolute;right:-27px;bottom:2px;width:30px;height:42px;border:6px solid #704c3e;border-left:0;border-radius:0 28px 28px 0;transform:rotate(-18deg)}.cat-l2{transform:translateX(-50%) scale(1.12)}.cat-l3{transform:translateX(-50%) scale(1.24)}.cat-l4{transform:translateX(-50%) scale(1.38)}.cat-l5{transform:translateX(-50%) scale(1.55)}@keyframes cat-bob{50%{margin-bottom:7px}}.pet-copy{flex:1;padding:26px 28px}.pet-copy h2{margin:4px 0 7px}.pet-copy p{font-weight:800;color:var(--grass-dark)}.pet-copy small{color:var(--muted)}.exercise-stage{height:106px;margin:8px 0 12px;border-radius:12px;background:linear-gradient(#dff2f7 0 62%,#dcebcf 62%);position:relative;overflow:hidden}.move-avatar{position:absolute;left:50%;bottom:18px;width:24px;height:42px;background:var(--grass);border-radius:12px 12px 5px 5px;animation:move-demo 1.4s ease-in-out infinite}.move-avatar:before{content:'';position:absolute;left:2px;top:-19px;width:20px;height:20px;border-radius:50%;background:#d99d70;border:3px solid #704c3e}.motion-lines{position:absolute;left:28%;bottom:26px;width:44%;height:3px;background:repeating-linear-gradient(90deg,transparent 0 12px,#d8b078 12px 23px);animation:slide-lines 1.4s linear infinite}@keyframes move-demo{0%,100%{transform:translateX(-50%) rotate(-5deg)}50%{transform:translateX(-50%) translateY(-9px) rotate(5deg)}}@keyframes slide-lines{to{transform:translateX(-30px)}}.cyc{display:flex;gap:3px;margin:12px 0}.cyc i{flex:1;height:36px;border-radius:4px;background:#d9d0bd}.cyc .m{background:#d98272}.cyc .f{background:#a8c18d}.cyc .o{background:var(--gold)}.cyc .l{background:#9db9c2}.cyc .t{outline:2px solid var(--ink);outline-offset:2px}.breath{width:120px;height:120px;border-radius:50%;margin:22px auto;background:radial-gradient(#c3db9a,var(--grass));animation:bx 16s ease-in-out infinite}@keyframes bx{0%{transform:scale(.55)}25%,50%{transform:scale(1)}75%,100%{transform:scale(.55)}}@media (prefers-reduced-motion:reduce){.breath{animation:none}}@media(max-width:800px){.stApp{background:var(--bg)}[data-testid=stSidebar]{width:190px !important}.block-container{padding:1.5rem}.top .brand{position:static;margin-right:auto}}
.pet-card{display:flex;gap:0;overflow:hidden;margin:0 0 18px;border:2px solid #c9d7b9;border-radius:12px;background:linear-gradient(135deg,#fffdf7 0%,#f5f9ed 100%);box-shadow:0 4px 0 #d8ccb5}.pet-art{width:25%;min-width:140px;position:relative;background:linear-gradient(180deg,#dff2f7 0%,#e8f0dc 100%);display:flex;align-items:center;justify-content:center;overflow:hidden;padding:12px}.pet-art img{display:none}.pixel-cat{display:inline-block;font-size:2.4rem;line-height:1;font-family:monospace;font-weight:bold;animation:pet-breathe 2.5s ease-in-out infinite;letter-spacing:-.25em;color:#426b3d;text-shadow:0 2px 0 rgba(0,0,0,.05)}.pixel-cat::before{content:'ᐯ^ω^ᐯ';display:block}.pet-badge{display:none}.pet-copy{padding:16px 18px;flex:1;display:flex;flex-direction:column;justify-content:center}.pet-copy h2{margin:2px 0 4px;font-size:1.15rem}.pet-copy p{font-size:.95rem;margin:0 0 8px;font-style:italic;color:#6e7b70}.pet-growth{display:flex;justify-content:space-between;font-size:.75rem;font-weight:700;color:#6e7b70;margin-top:8px}.pet-growth b{color:#426b3d}.pet-xp{height:6px;background:#e4ddca;border-radius:3px;overflow:hidden;margin:4px 0}.pet-xp i{display:block;height:100%;background:linear-gradient(90deg,#e0a43b,#c48a2e);border-radius:3px;transition:width .5s ease}@keyframes pet-breathe{0%,100%{transform:translateY(0)}50%{transform:translateY(-4px)}}@media(max-width:700px){.pet-card{display:block}.pet-art{width:100%;height:170px}.pet-copy{padding:18px}}\n.exercise-stage{height:150px;position:relative;overflow:hidden;border-radius:12px;background:linear-gradient(#dff2f7 0 62%,#9bc96d 62%);border:2px solid #c9d7b9}.exercise-stage:after{content:'';position:absolute;left:0;right:0;bottom:0;height:12px;background:repeating-linear-gradient(90deg,#6b9b54 0 18px,#83ae62 18px 36px)}.move-avatar{position:absolute;z-index:2;left:calc(50% - 22px);top:54px;width:44px;height:44px;background:#6b9b54;border:5px solid #426b3d;box-shadow:0 38px 0 -10px #a8754f,0 76px 0 -14px #426b3d;animation:quest-bob 1.4s ease-in-out infinite}.move-avatar:before{content:'';position:absolute;left:8px;top:10px;width:8px;height:8px;background:#fff;box-shadow:20px 0 #fff}.move-avatar:after{content:'';position:absolute;left:11px;top:13px;width:4px;height:4px;background:#26352b;box-shadow:20px 0 #26352b}.move-avatar.box{animation:breath-pulse 4s ease-in-out infinite}.move-avatar.g54321,.move-avatar.scan,.move-avatar.grat,.move-avatar.dump{background:#83ae62;animation:ground-sway 2.4s ease-in-out infinite}.move-avatar.circuit,.move-avatar.walk,.move-avatar.desk,.move-avatar.yoga,.move-avatar.hips{animation:exercise-step .8s ease-in-out infinite alternate}.motion-lines{position:absolute;left:20%;right:20%;bottom:34px;border-top:3px dotted rgba(66,107,61,.55);animation:lines-slide 1s linear infinite}@keyframes quest-bob{50%{transform:translateY(-12px)}}@keyframes breath-pulse{50%{transform:scale(1.16)}}@keyframes ground-sway{50%{transform:translateX(16px) rotate(4deg)}}@keyframes exercise-step{to{transform:translateY(-14px) rotate(7deg)}}@keyframes lines-slide{to{background-position:30px 0}}\n</style>""", unsafe_allow_html=True)

# ---------------------------------------------------------------- database
def db():
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    return c

def q(sql, args=(), one=False, commit=False):
    with db() as c:
        cur = c.execute(sql, args)
        if commit:
            return cur.lastrowid
        rows = cur.fetchall()
    return (rows[0] if rows else None) if one else rows

def init_db():
    with db() as c:
        c.executescript("""
        CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, username TEXT UNIQUE, salt TEXT,
            pw TEXT, display TEXT, goal_sleep REAL DEFAULT 8, goal_water REAL DEFAULT 2.5,
            goal_activity INTEGER DEFAULT 30, memory_ok INTEGER DEFAULT 1);
        CREATE TABLE IF NOT EXISTS logs(id INTEGER PRIMARY KEY, user_id INT, day TEXT,
            sleep REAL, water REAL, activity INT, mood INT, weight REAL, UNIQUE(user_id, day));
        CREATE TABLE IF NOT EXISTS stories(id INTEGER PRIMARY KEY, user_id INT, kind TEXT,
            caption TEXT, img BLOB, created TEXT, permanent INT);
        CREATE TABLE IF NOT EXISTS reactions(story_id INT, user_id INT, emoji TEXT,
            UNIQUE(story_id, user_id));
        CREATE TABLE IF NOT EXISTS friends(a INT, b INT, status TEXT, UNIQUE(a, b));
        CREATE TABLE IF NOT EXISTS challenges(id INTEGER PRIMARY KEY, name TEXT, days INT,
            metric TEXT, threshold REAL);
        CREATE TABLE IF NOT EXISTS members(challenge_id INT, user_id INT, start TEXT,
            UNIQUE(challenge_id, user_id));
        CREATE TABLE IF NOT EXISTS medical(user_id INTEGER PRIMARY KEY, conditions TEXT, allergies TEXT,
            medications TEXT, notes TEXT);
        CREATE TABLE IF NOT EXISTS cycles(user_id INT, start TEXT, plen INT, UNIQUE(user_id, start));
        CREATE TABLE IF NOT EXISTS cycle_notes(user_id INT, day TEXT, flow TEXT, symptoms TEXT, UNIQUE(user_id, day));
        CREATE TABLE IF NOT EXISTS ex_done(user_id INT, day TEXT, ex TEXT, UNIQUE(user_id, day, ex));
        CREATE TABLE IF NOT EXISTS chat(id INTEGER PRIMARY KEY, user_id INT, role TEXT, text TEXT, created TEXT);
        """)
        if not c.execute("SELECT 1 FROM challenges").fetchone():
            c.executemany("INSERT INTO challenges(name,days,metric,threshold) VALUES(?,?,?,?)", [
                ("7-Day Walking Challenge (20+ min)", 7, "activity", 20),
                ("5-Day Hydration Challenge (2+ L)", 5, "water", 2),
                ("Consistent Bedtime (7+ h sleep, 7 days)", 7, "sleep", 7),
                ("Weekly Mood Check-in (log mood 7 days)", 7, "mood", 1)])

def hash_pw(pw, salt):
    return hashlib.pbkdf2_hmac("sha256", pw.encode(), salt.encode(), 100_000).hex()

# ---------------------------------------------------------------- helpers
def user():
    return q("SELECT * FROM users WHERE id=?", (st.session_state["uid"],), one=True)

def logs_df(uid, days=None):
    rows = q("SELECT day,sleep,water,activity,mood,weight FROM logs WHERE user_id=? ORDER BY day", (uid,))
    df = pd.DataFrame([dict(r) for r in rows], columns=["day", "sleep", "water", "activity", "mood", "weight"])
    df["day"] = pd.to_datetime(df["day"])
    if days:
        df = df[df["day"] >= pd.Timestamp(date.today() - timedelta(days=days - 1))]
    return df

def friend_ids(uid):
    rows = q("SELECT a,b FROM friends WHERE status='accepted' AND (a=? OR b=?)", (uid, uid))
    return [r["b"] if r["a"] == uid else r["a"] for r in rows]

def streak(uid):
    days = {r["day"] for r in q("SELECT day FROM logs WHERE user_id=?", (uid,))}
    n, d = 0, date.today()
    if d.isoformat() not in days:
        d -= timedelta(days=1)
    while d.isoformat() in days:
        n, d = n + 1, d - timedelta(days=1)
    return n

def insights(df):
    """Careful, non-causal observations from the user's own logs."""
    out = []
    if df.empty:
        return ["Log a few days to unlock personal insights."]
    last7 = df[df["day"] >= pd.Timestamp(date.today() - timedelta(days=6))]
    prev7 = df[(df["day"] < pd.Timestamp(date.today() - timedelta(days=6))) &
               (df["day"] >= pd.Timestamp(date.today() - timedelta(days=13)))]
    for col, label, unit in [("sleep", "sleep", "h"), ("water", "water intake", "L"), ("activity", "activity", "min")]:
        a, b = last7[col].mean(), prev7[col].mean()
        if pd.notna(a) and pd.notna(b) and abs(a - b) > 0.01:
            out.append(f"Your average {label} this week is {a:.1f}{unit}, vs {b:.1f}{unit} the week before.")
    both = df.dropna(subset=["sleep", "mood"])
    if len(both) >= 5:
        short = both[both["sleep"] < both["sleep"].median()]["mood"].mean()
        long_ = both[both["sleep"] >= both["sleep"].median()]["mood"].mean()
        if long_ - short >= 0.5:
            out.append("Your records show lower mood ratings on days with shorter sleep. This doesn't establish "
                       "a cause, but you may find it helpful to explore your sleep routine.")
    return out or ["No notable patterns yet - keep logging!"]

# ---------------------------------------------------------------- story cards
THEMES = {"Lavender": ((167, 139, 250), (96, 165, 250)), "Sunset": ((251, 146, 60), (236, 72, 153)),
          "Mint": ((52, 211, 153), (56, 189, 248)), "Night": ((49, 46, 129), (124, 58, 237))}

def font(size):
    for f in ("DejaVuSans-Bold.ttf", "arialbd.ttf"):
        try:
            return ImageFont.truetype(f, size)
        except OSError:
            pass
    try:
        return ImageFont.load_default(size=size)
    except TypeError:
        return ImageFont.load_default()

def make_card(title, lines, caption, theme, name):
    w, h = 720, 1080
    c1, c2 = THEMES[theme]
    img = Image.new("RGB", (w, h))
    px_ = img.load()
    for y in range(h):
        t = y / h
        col = tuple(int(c1[i] * (1 - t) + c2[i] * t) for i in range(3))
        for x in range(w):
            px_[x, y] = col
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((50, 150, w - 50, h - 200), 40, fill=(255, 255, 255))
    d.text((90, 190), title, font=font(52), fill=(91, 75, 196))
    y = 320
    for ln in lines:
        d.text((90, y), ln, font=font(38), fill=(40, 40, 70))
        y += 80
    if caption:
        d.text((90, h - 330), caption[:42], font=font(32), fill=(110, 110, 140))
    d.text((60, 70), f"@{name}", font=font(36), fill=(255, 255, 255))
    d.text((60, h - 130), "HealthMate", font=font(40), fill=(255, 255, 255))
    buf = io.BytesIO()
    img.save(buf, "PNG")
    return buf.getvalue()

# ---------------------------------------------------------------- chatbot + routine
URGENT = r"chest pain|can'?t breathe|trouble breathing|faint|unconscious|severe bleeding|stroke|seizure|overdose|poison|blood in (stool|vomit)|coughing blood"
CRISIS = r"suicid|kill myself|end my life|self[- ]harm|hurt myself"

# (pattern, topic, what you can do, see a doctor if)
KB = [
 (r"headache|migraine", "Headache",
  "Drink water, rest in a quiet dim room, eat if you skipped a meal, relax neck/shoulders, and rest your eyes from screens. Paracetamol is commonly used for headache - follow the label for your age/weight and avoid it if you are allergic or have liver problems.",
  "it is sudden and the worst of your life, follows a head injury, comes with fever + stiff neck, vision changes, weakness, confusion, or keeps returning."),
 (r"fever|temperature", "Fever",
  "Rest, drink plenty of fluids, wear light clothing and keep the room comfortable. Paracetamol is commonly used to ease fever/discomfort - follow the label dose and check with a pharmacist if unsure.",
  "fever is above 103F/39.4C, lasts more than 3 days, or comes with rash, severe headache, breathing trouble, persistent vomiting, or you are very drowsy."),
 (r"cold|cough|runny nose|blocked nose|stuffy|flu\b", "Cold / cough",
  "Rest, warm fluids, steam inhalation, warm salt-water gargles, honey-and-warm-water for cough (not for babies under 1), and saline nasal drops. Wash hands often.",
  "symptoms last over 10 days, you wheeze or get short of breath, have high fever, or chest pain."),
 (r"sore throat|throat pain", "Sore throat",
  "Warm salt-water gargles, warm fluids, rest your voice, and stay hydrated. Lozenges may help.",
  "it lasts more than a week, you can't swallow, have a high fever, white patches, or drooling/breathing difficulty."),
 (r"stomach|acidity|bloat|indigestion|nausea|vomit|diarrh|loose motion|gas\b", "Stomach upset",
  "Sip water or ORS in small amounts often, eat light foods (rice, banana, toast, curd), avoid oily/spicy food, caffeine and alcohol, and rest. For acidity: smaller meals, don't lie down right after eating.",
  "there is blood, black stools, severe or one-sided abdominal pain, signs of dehydration (very dark urine, dizziness), symptoms over 2 days, or you can't keep fluids down."),
 (r"back pain|neck pain|shoulder pain|posture", "Back / neck pain",
  "Keep moving gently (short walks), avoid long sitting - stand and stretch every 30-45 min, set up your screen at eye level, use warm compress, and do gentle stretches. Avoid heavy lifting for a few days.",
  "pain follows an injury, spreads down a leg, comes with numbness/weakness, fever, or bladder/bowel problems, or lasts more than 2 weeks."),
 (r"period|cramp|menstrual", "Period cramps",
  "A warm compress, gentle walking/stretching, hydration, light meals, and rest help. Paracetamol or ibuprofen are commonly used - follow the label and avoid ibuprofen if you have stomach ulcers/asthma/kidney issues.",
  "pain is severe enough to stop daily life, bleeding is very heavy, periods are missed or irregular, or cycles suddenly change."),
 (r"acne|pimple|dry skin", "Skin care",
  "Wash your face gently twice a day, avoid picking, use a non-comedogenic moisturiser and sunscreen, wash pillowcases weekly, and limit very oily/sugary foods if you notice a link.",
  "acne is painful/cystic or scarring, a rash spreads quickly, or there is swelling, fever or a reaction to a product."),
 (r"eye strain|eyes? (hurt|tired|dry|burn)|screen", "Eye strain",
  "Use the 20-20-20 rule (every 20 min look 20 ft away for 20 sec), blink more, adjust screen brightness, keep the screen an arm's length away, and sleep enough.",
  "you have vision changes, eye pain, redness with discharge, or headaches that persist - get an eye test."),
 (r"constipation", "Constipation",
  "Increase fibre (fruit, vegetables, whole grains), drink water, move daily, and keep a regular toilet routine.",
  "it lasts over a week, with severe pain, blood, or unexplained weight loss."),
 (r"fatigue|tired|low energy|weak|exhaust", "Tiredness / low energy",
  "Check the basics: consistent 7-9 h sleep, water, regular meals with protein, daylight and 20-30 min of movement, and less late-night screen time/caffeine.",
  "tiredness lasts weeks despite good sleep, or comes with weight change, breathlessness, dizziness, pale skin or low mood - a blood test (e.g. iron, thyroid, vitamin D) may help."),
 (r"insomnia|can'?t sleep|cannot sleep|trouble sleeping|sleepless", "Trouble sleeping",
  "Same sleep/wake time daily, no caffeine after afternoon, screens off 1 h before bed, dark cool room, a short wind-down (reading, stretching), and don't study in bed. If awake >20 min, get up and do something calm.",
  "poor sleep lasts more than 3-4 weeks, you snore loudly/stop breathing at night, or it affects mood and daily life."),
 (r"anxiety|anxious|stress|panic|overthink|worried", "Stress / anxiety",
  "Try slow breathing (inhale 4s, exhale 6s for 2 min), a short walk, writing worries down, breaking tasks into small steps, limiting caffeine, and talking to a trusted person. Regular sleep and movement help a lot.",
  "it affects sleep, eating or studies for more than 2 weeks, you have panic attacks, or you feel hopeless - a counsellor or doctor can help (Tele-MANAS: 14416 in India)."),
 (r"muscle|sore|sprain|joint|knee", "Muscle / joint pain",
  "R.I.C.E.: Rest, Ice (15 min), Compression, Elevation for the first 1-2 days, then gentle movement. Warm up before exercise and increase intensity gradually.",
  "there is swelling you can't explain, deformity, you can't bear weight, the pain is severe, or it isn't improving in a week."),
]

SYSTEM = ("You are HealthMate's wellness companion for a student-friendly health app. Give practical, clear, friendly "
          "general health information: likely common causes, self-care steps, commonly used over-the-counter options "
          "(mention to follow the label and check allergies/conditions, no exact doses), lifestyle and routine fixes, and "
          "specific red-flag signs that mean seeing a doctor. You do not diagnose or prescribe. If symptoms could be "
          "urgent, tell them to seek care now. Use the user's logged data and medical history below when relevant. "
          "Keep answers under 250 words, use short bullet points.")

def med_hist(uid):
    return q("SELECT * FROM medical WHERE user_id=?", (uid,), one=True)

def health_context(u):
    df = logs_df(u["id"], 30)
    p = [f"Goals: sleep {u['goal_sleep']}h, water {u['goal_water']}L, activity {u['goal_activity']}min."]
    for col, lab in [("sleep", "sleep h"), ("water", "water L"), ("activity", "activity min"), ("mood", "mood/5")]:
        if df[col].notna().any():
            p.append(f"30-day avg {lab}: {df[col].mean():.1f}.")
    m = med_hist(u["id"])
    if m and u["memory_ok"]:
        for k in ("conditions", "allergies", "medications", "notes"):
            if m[k]:
                p.append(f"{k}: {m[k]}.")
    return " ".join(p)

def fmt(t):
    t = round(t * 4) / 4 % 24
    h, m = int(t), int(round((t % 1) * 60))
    return f"{(h % 12) or 12}:{m:02d} {'AM' if h < 12 else 'PM'}"

def make_routine(u, wake=7.0, study=3.0):
    df = logs_df(u["id"], 14)
    sl = float(u["goal_sleep"])
    bed = (wake - sl) % 24
    items = [(wake, "Wake up, drink a glass of water, get 10 min of daylight"),
             (wake + 0.5, "Light stretching or a short walk"),
             (wake + 1, "Balanced breakfast (protein + fruit/whole grains)"),
             (wake + 5.5, "Lunch + water, 10-min break away from screens"),
             (wake + 9, f"Exercise or brisk walk: {u['goal_activity']} min"),
             (bed - 3, "Light dinner - avoid heavy meals late"),
             (bed - 1.5, "Stop caffeine and heavy studying; write tomorrow's to-do list"),
             (bed - 1, "Screens off, dim lights, wind down (reading, music, stretching)"),
             (bed, f"Lights out - target {sl:g} h sleep")]
    if study > 0:
        items.insert(3, (wake + 2, f"Study/work: {study:g} h total in 50-min focus blocks with 10-min breaks, split morning/afternoon"))
    items.sort(key=lambda x: (x[0] - wake) % 24)
    out = ["**Your suggested daily routine**\n"] + [f"- **{fmt(t)}** - {txt}" for t, txt in items]
    tips = []
    if df["sleep"].notna().any() and df["sleep"].mean() < sl - 0.75:
        tips.append(f"You average {df['sleep'].mean():.1f}h of sleep vs your {sl:g}h goal: move bedtime 15 min earlier every few nights until you get there.")
    if df["water"].notna().any() and df["water"].mean() < float(u["goal_water"]) - 0.5:
        tips.append("Your water intake is below goal: keep a bottle at your desk and drink a glass with each meal.")
    if df["activity"].notna().any() and df["activity"].mean() < u["goal_activity"] * 0.6:
        tips.append("Activity is low: start with 10-minute walks after meals and build up.")
    if tips:
        out += ["\n**Fixes based on your logs**"] + [f"- {t}" for t in tips]
    return "\n".join(out)

def rule_reply(msg, u):
    m = msg.lower()
    df = logs_df(u["id"], 30)
    if re.search(r"routine|schedule|timetable|time table|plan my day", m):
        return make_routine(u) + "\n\n_Want it for a different wake-up time or study hours? Use the **Fix my routine** box above._"
    if re.search(r"report|summary|history|insight", m):
        if df.empty:
            return "You haven't logged anything yet. Add a few days in **My Health** and I can summarise them."
        parts = [f"Over the last 30 days you logged {len(df)} day(s)."]
        for col, lab, unit in [("sleep", "sleep", "h"), ("water", "water", "L"), ("activity", "activity", "min"), ("mood", "mood", "/5")]:
            if df[col].notna().any():
                parts.append(f"Average {lab}: {df[col].mean():.1f}{unit}.")
        return " ".join(parts + insights(df))
    for pat, name, care, doc in KB:
        if re.search(pat, m):
            r = f"**{name}** - general guidance, not a diagnosis.\n\n**What you can do:** {care}\n\n**See a doctor if** {doc}"
            mh = med_hist(u["id"])
            if mh and u["memory_ok"] and (mh["allergies"] or mh["medications"] or mh["conditions"]):
                r += "\n\n⚠️ You have allergies/conditions/medicines saved in your history - check with a doctor or pharmacist before taking any new medicine."
            return r
    if "sleep" in m:
        return make_routine(u)
    if re.search(r"water|hydrat|drink", m):
        avg = df["water"].mean() if not df.empty else float("nan")
        base = f"You average {avg:.1f}L (goal {u['goal_water']}L). " if pd.notna(avg) else ""
        return base + "Keep a bottle nearby, drink a glass on waking and with each meal, and check your urine colour (pale yellow is a good sign)."
    if re.search(r"walk|exercise|workout|activity|steps|gym", m):
        return (f"Your activity goal is {u['goal_activity']} min/day. Start with 10-minute walks after meals, add strength or "
                "bodyweight work 2-3 times a week, warm up first, and rest when sore. Try the walking challenge in **Friends & Challenges**!")
    if re.search(r"medicine|medication|tablet|dose|antibiotic|paracetamol|ibuprofen", m):
        return ("General info: always follow the label or your doctor's dose, don't mix medicines without asking, avoid "
                "antibiotics unless prescribed, and check allergies first. Tell me the symptom (e.g. headache, fever, "
                "cold) and I'll share common self-care options and when to see a doctor. For exact doses, ask a pharmacist.")
    return ("I can help with symptoms (headache, fever, cold, stomach upset, back pain, period cramps, stress, tiredness...), "
            "daily routines, sleep, water, exercise, and your logged data. Try: *'I have a headache'*, *'fix my routine'* "
            "or *'explain my report'*. I share general guidance, not a diagnosis.")

PROVIDERS = {
    "Google Gemini (free tier available)": ("gemini", "gemini-2.5-flash", "GEMINI_API_KEY"),
    "OpenAI": ("openai", "gpt-4o-mini", "OPENAI_API_KEY"),
    "Anthropic Claude": ("anthropic", "claude-sonnet-5-5", "ANTHROPIC_API_KEY"),
    "Other OpenAI-compatible (Groq, OpenRouter...)": ("compat", "", "AI_API_KEY"),
}

def post_json(url, headers, body):
    h = {"Content-Type": "application/json", "User-Agent": "HealthMate/1.0", **headers}
    req = urllib.request.Request(url, json.dumps(body).encode(), h)
    for attempt in range(4):  # retry when the provider is overloaded (503/500)
        try:
            with urllib.request.urlopen(req, timeout=40) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            if e.code not in (500, 503) or attempt == 3:
                raise
            time.sleep(2 * (attempt + 1))

def ai_config():
    kind, model, env = PROVIDERS[st.session_state.get("provider", list(PROVIDERS)[0])]
    key = st.session_state.get("api_key") or os.environ.get(env)
    return kind, key, st.session_state.get(f"ai_model_{kind}") or model

def ai_reply(msg, u, hist):
    kind, key, model = ai_config()
    if not key:
        return None
    sysmsg = SYSTEM + "\nUser data: " + health_context(u)
    turns = [{"role": r["role"], "text": r["text"]} for r in hist[-10:]]
    while turns and turns[0]["role"] != "user":
        turns.pop(0)
    turns.append({"role": "user", "text": msg})
    try:
        if kind == "gemini":
            body = {"system_instruction": {"parts": [{"text": sysmsg}]},
                    "contents": [{"role": "model" if t["role"] == "assistant" else "user",
                                  "parts": [{"text": t["text"]}]} for t in turns]}
            d = post_json(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
                          {"x-goog-api-key": key}, body)
            return d["candidates"][0]["content"]["parts"][0]["text"]
        if kind == "anthropic":
            d = post_json("https://api.anthropic.com/v1/messages",
                          {"x-api-key": key, "anthropic-version": "2023-06-01"},
                          {"model": model, "max_tokens": 700, "system": sysmsg,
                           "messages": [{"role": t["role"], "content": t["text"]} for t in turns]})
            return d["content"][0]["text"]
        base = (st.session_state.get("ai_base") if kind == "compat" else "") or "https://api.openai.com/v1"
        d = post_json(base.rstrip("/") + "/chat/completions", {"Authorization": "Bearer " + key},
                      {"model": model, "max_tokens": 700,
                       "messages": [{"role": "system", "content": sysmsg}] +
                                   [{"role": t["role"], "content": t["text"]} for t in turns]})
        return d["choices"][0]["message"]["content"]
    except Exception as e:
        detail = ""
        if hasattr(e, "read"):
            try:
                detail = " | " + e.read().decode()[:220]
            except Exception:
                pass
        st.session_state["ai_err"] = (str(e) + detail)[:300]
        return None

def bot_reply(msg, u, hist=()):
    m = msg.lower()
    if re.search(CRISIS, m):
        return ("I'm really sorry you're feeling this way. You deserve support right now. Please reach out to someone "
                "you trust, or call a helpline such as Tele-MANAS (14416 in India) or your local emergency number.")
    if re.search(URGENT, m):
        return ("⚠️ That could be an urgent symptom. Please contact a doctor or emergency services (112 in India) "
                "right away rather than waiting. I can't assess symptoms or rule out anything serious.")
    return ai_reply(msg, u, list(hist)) or rule_reply(msg, u)

def make_photo_story(data, caption, name):
    img = ImageOps.exif_transpose(Image.open(io.BytesIO(data))).convert("RGBA")
    img = ImageOps.fit(img, (720, 1080))
    ov = Image.new("RGBA", img.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    od.rectangle((0, 0, 720, 140), fill=(0, 0, 0, 90))
    od.rectangle((0, 880, 720, 1080), fill=(0, 0, 0, 140))
    img = Image.alpha_composite(img, ov).convert("RGB")
    d = ImageDraw.Draw(img)
    d.text((40, 50), f"@{name}", font=font(38), fill="white")
    for i, ln in enumerate(textwrap.wrap(caption, 28)[:2]):
        d.text((40, 910 + i * 55), ln, font=font(42), fill="white")
    d.text((520, 1020), "HealthMate", font=font(30), fill=(220, 210, 255))
    buf = io.BytesIO()
    img.save(buf, "PNG")
    return buf.getvalue()

# ---------------------------------------------------------------- pages
def page_auth():
    st.markdown("<div class='hero'><h1>HealthMate</h1><p>Your health. Your journey. Your community.</p></div>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["Log in", "Sign up"])
    with t1:
        un = st.text_input("Username", key="lu")
        pw = st.text_input("Password", type="password", key="lp")
        if st.button("Log in"):
            r = q("SELECT * FROM users WHERE username=?", (un.strip().lower(),), one=True)
            if r and secrets.compare_digest(r["pw"], hash_pw(pw, r["salt"])):
                st.session_state["uid"] = r["id"]
                st.rerun()
            st.error("Wrong username or password.")
    with t2:
        un = st.text_input("Choose a username", key="su")
        dn = st.text_input("Display name", key="sd")
        pw = st.text_input("Choose a password (6+ chars)", type="password", key="sp")
        if st.button("Create account"):
            if not re.fullmatch(r"[a-z0-9_]{3,20}", un.strip().lower()) or len(pw) < 6:
                st.error("Username: 3-20 letters/numbers/_ ; password: 6+ characters.")
            elif q("SELECT 1 FROM users WHERE username=?", (un.strip().lower(),), one=True):
                st.error("That username is taken.")
            else:
                salt = secrets.token_hex(8)
                uid = q("INSERT INTO users(username,salt,pw,display) VALUES(?,?,?,?)",
                        (un.strip().lower(), salt, hash_pw(pw, salt), dn or un), commit=True)
                st.session_state["uid"] = uid
                st.rerun()

def story_viewer(rows, uid, key):
    if not rows:
        st.info("No stories yet.")
        return
    cols = st.columns(4)
    for i, s in enumerate(rows):
        with cols[i % 4]:
            st.image(s["img"], use_container_width=True)
            st.caption(f"**{s['display']}** · {'📌 permanent' if s['permanent'] else '⏳ 24h'}")
            cnt = q("SELECT emoji,COUNT(*) n FROM reactions WHERE story_id=? GROUP BY emoji", (s["id"],))
            if cnt:
                st.write(" ".join(f"{r['emoji']}{r['n']}" for r in cnt))
            rc = st.columns(3)
            for j, e in enumerate(["💜", "🔥", "👏"]):
                if rc[j].button(e, key=f"{key}{s['id']}{e}"):
                    q("INSERT OR REPLACE INTO reactions VALUES(?,?,?)", (s["id"], uid, e), commit=True)
                    st.rerun()

def visible_stories(uid):
    ids = friend_ids(uid) + [uid]
    cutoff = (datetime.now() - timedelta(hours=24)).isoformat()
    ph = ",".join("?" * len(ids))
    return q(f"""SELECT s.*, u.display FROM stories s JOIN users u ON u.id=s.user_id
                 WHERE s.user_id IN ({ph}) AND (s.permanent=1 OR s.created>?) ORDER BY s.created DESC""",
             (*ids, cutoff))

def tile(icon, label, value):
    return f"<div class='tile'><div class='i'>{icon}</div><div class='v'>{value}</div><div class='l'>{label}</div></div>"

# ---------------------------------------------------------------- game layer
LEVELS = ["Seedling", "Sprout", "Stride", "Spark", "Blaze", "Summit", "Legend"]

def total_xp(uid):
    df = logs_df(uid); u = q("SELECT * FROM users WHERE id=?", (uid,), one=True)
    xp = len(df) * 10
    xp += int((df["activity"] >= u["goal_activity"]).sum() + (df["water"] >= u["goal_water"]).sum() + (df["sleep"] >= u["goal_sleep"] - .5).sum()) * 10
    xp += q("SELECT COUNT(*) n FROM ex_done WHERE user_id=?", (uid,), one=True)["n"] * 15
    return xp

def level_info(xp):
    lv = int((xp / 60) ** 0.5) + 1
    lo, hi = 60 * (lv - 1) ** 2, 60 * lv ** 2
    return lv, xp - lo, hi - lo

def ring(frac, val, label):
    C = 2 * math.pi * 42; f = max(0, min(1, frac))
    return (f"<div class='ring'><svg viewBox='0 0 100 100'><circle cx='50' cy='50' r='42' class='rt'/>"
            f"<circle cx='50' cy='50' r='42' class='rf' stroke-dasharray='{C * f:.1f} {C:.1f}' transform='rotate(-90 50 50)'/>"
            f"<text x='50' y='57' text-anchor='middle'>{val}</text></svg><div class='rl'>{label}</div></div>")

def nz(x):
    return 0 if x is None or pd.isna(x) else x

def spark(vals, labels, goal, w=520, h=170):
    top = max(max(vals), goal, 1) * 1.15
    pts = [(30 + i * (w - 60) / (len(vals) - 1), h - 34 - v / top * (h - 60)) for i, v in enumerate(vals)]
    line = " ".join(f"{x:.0f},{y:.0f}" for x, y in pts)
    gy = h - 34 - goal / top * (h - 60)
    lab = "".join(f"<text x='{x:.0f}' y='{h - 8}' text-anchor='middle' fill='#8d9490' font-size='12'>{l}</text>" for (x, _), l in zip(pts, labels))
    dots = "".join(f"<circle cx='{x:.0f}' cy='{y:.0f}' r='4.5' fill='#FF6A1A'/>" for x, y in pts)
    return (f"<svg viewBox='0 0 {w} {h}' style='width:100%'><defs><linearGradient id='g' x1='0' y1='0' x2='0' y2='1'>"
            "<stop offset='0' stop-color='#FF6A1A' stop-opacity='.45'/><stop offset='1' stop-color='#FF6A1A' stop-opacity='0'/></linearGradient></defs>"
            f"<line x1='20' x2='{w - 20}' y1='{gy:.0f}' y2='{gy:.0f}' stroke='#3a3f3c' stroke-dasharray='5 6'/>"
            f"<polygon points='{pts[0][0]:.0f},{h - 34} {line} {pts[-1][0]:.0f},{h - 34}' fill='url(#g)'/>"
            f"<polyline points='{line}' fill='none' stroke='#FF6A1A' stroke-width='3.5' stroke-linejoin='round'/>{dots}{lab}</svg>")

def pet_status(u, xp):
    today = q("SELECT * FROM logs WHERE user_id=? AND day=?", (u['id'], date.today().isoformat()), one=True)
    today_goals = q("SELECT COUNT(*) n FROM ex_done WHERE user_id=? AND day=?", (u['id'], date.today().isoformat()), one=True)["n"]
    completed = bool(today) or today_goals > 0
    affirmations = {
        'complete': [
            ('Lovely', 'You showed up! I am so proud.'),
            ('Joyful', 'Your health matters. Great work today!'),
            ('Confident', 'You are building something real.'),
            ('Grateful', 'Thank you for taking care of yourself.'),
        ],
        'partial': [
            ("Hopeful", "Every small step counts. You've got this."),
            ('Encouraging', 'Start where you are. You are enough.'),
            ('Gentle', 'Be kind to yourself on hard days.'),
            ('Friendly', 'Your effort today makes a difference.'),
        ],
        'empty': [
            ('Ready', 'Your health journey starts with one small step.'),
            ('Curious', 'What will you do for yourself today?'),
            ('Warm', 'I am here. Whenever you are ready.'),
            ('Patient', 'Progress, not perfection. You have got this.'),
        ],
    }
    if completed:
        moods = affirmations['complete']
    elif today or today_goals:
        moods = affirmations['partial']
    else:
        moods = affirmations['empty']
    idx = (date.today().day + xp + len(str(u['id']))) % len(moods)
    mood, message = moods[idx]
    return 1, 'Pixel', mood, message


def pet_card(u, xp):
    _, name, mood, message = pet_status(u, xp)
    st.markdown(f"<div class='pet-card'><div class='pet-art'><div class='pixel-cat' role='img' aria-label='Your cute cat companion'></div></div><div class='pet-copy'><div class='k'>YOUR COMPANION · {html.escape(name.upper())}</div><h2>{html.escape(mood)}</h2><p>{html.escape(message)}</p><small>Pixel is here to cheer you on, not judge your pace.</small></div></div>", unsafe_allow_html=True)

def page_home(u):
    hr = datetime.now().hour
    greet = "Good morning" if hr < 12 else "Good afternoon" if hr < 18 else "Good evening"
    xp = total_xp(u["id"]); lv, cur, need = level_info(xp)
    pet_card(u, xp)
    days = [date.today() - timedelta(days=i) for i in range(6, -1, -1)]
    m = {r.day.date(): r for r in logs_df(u["id"], 7).itertuples()}
    act = [nz(m[d].activity) if d in m else 0 for d in days]
    today = m.get(date.today())
    g = lambda k: nz(getattr(today, k)) if today is not None else 0
    a, b = st.columns([2, 1])
    a.markdown(f"<div class='b'><div class='k'>Level {lv} · {LEVELS[min(lv - 1, 6)]}</div><h1>{greet}, {html.escape(u['display'])}</h1>"
               f"<div class='k'>{xp} XP total · {need - cur} XP to level {lv + 1}</div><div class='xpbar'><i style='width:{100 * cur / need:.0f}%'></i></div></div>", unsafe_allow_html=True)
    b.markdown(f"<div class='b or'><div class='k'>Logging streak</div><div class='num'>{streak(u['id'])}</div><div>days in a row</div></div>", unsafe_allow_html=True)
    a, b = st.columns([1.5, 1])
    a.markdown(f"<div class='b'><div class='k'>Activity, last 7 days (dashed = your {u['goal_activity']} min goal)</div>"
               + spark(act, [d.strftime('%a') for d in days], u["goal_activity"]) + "</div>", unsafe_allow_html=True)
    b.markdown("<div class='b'><div class='k'>Today</div><div class='rings'>"
               + ring(g("sleep") / u["goal_sleep"], f"{g('sleep'):g}h", "Sleep") + ring(g("water") / u["goal_water"], f"{g('water'):g}L", "Water")
               + ring(g("activity") / u["goal_activity"], f"{g('activity'):g}m", "Move") + "</div></div>", unsafe_allow_html=True)
    ex_today = q("SELECT COUNT(*) n FROM ex_done WHERE user_id=? AND day=?", (u["id"], date.today().isoformat()), one=True)["n"]
    quests = [("Log today's numbers", today is not None, 10), ("Hit your water goal", g("water") >= u["goal_water"], 10),
              ("Reach your movement goal", g("activity") >= u["goal_activity"], 10), ("Finish one exercise in Move & Mind", ex_today > 0, 15)]
    a, b = st.columns(2)
    a.subheader("Today's quests")
    for n, ok, p in quests:
        a.markdown(f"<div class='quest {'done' if ok else ''}'><b></b>{n}<span>+{p} XP</span></div>", unsafe_allow_html=True)
    b.subheader("Insights")
    for i in insights(logs_df(u["id"], 30)):
        b.markdown(f"<div class='card'>{html.escape(i)}</div>", unsafe_allow_html=True)
    st.subheader("Friends' stories")
    story_viewer(visible_stories(u["id"]), u["id"], "h")

# ---------------------------------------------------------------- cycle tracker
PHASES = {
 "Menstrual": ("m", "Energy is often lowest. Rest is productive: warm compress, iron-rich food, gentle stretching or a slow walk."),
 "Follicular": ("f", "Energy usually climbs. A good window to try new workouts or tackle hard study sessions."),
 "Ovulation window": ("o", "Many people feel their most energetic here. Strength work and social plans tend to feel good."),
 "Luteal": ("l", "Mood dips, bloating and tiredness are common before a period. Prioritise sleep, magnesium-rich foods, and calming movement.")}
SYMPTOMS = ["Cramps", "Headache", "Bloating", "Fatigue", "Mood swings", "Acne", "Back pain", "Cravings", "Nausea", "Tender breasts"]

def cycle_stats(uid):
    rows = q("SELECT start,plen FROM cycles WHERE user_id=? ORDER BY start", (uid,))
    if not rows:
        return None
    st_ = [date.fromisoformat(r["start"]) for r in rows]
    gaps = [(b - a).days for a, b in zip(st_, st_[1:]) if 15 <= (b - a).days <= 60][-6:]
    clen = round(sum(gaps) / len(gaps)) if gaps else 28
    pl = [r["plen"] for r in rows if r["plen"]]
    plen = round(sum(pl) / len(pl)) if pl else 5
    day = (date.today() - st_[-1]).days + 1
    ov = clen - 14
    ph = "Menstrual" if day <= plen else "Follicular" if day < ov - 1 else "Ovulation window" if day <= ov + 1 else "Luteal"
    return dict(clen=clen, plen=plen, day=day, ov=ov, phase=ph, last=st_[-1], nxt=st_[-1] + timedelta(days=clen), n=len(st_))

def page_cycle(u):
    st.header("Cycle tracker")
    st.caption("Private to you - never shown in stories, friends or challenges.")
    s = cycle_stats(u["id"])
    left, right = st.columns([1.1, 1])
    with left:
        if not s:
            st.markdown("<div class='panel'>Log the first day of your last period on the right to start predictions.</div>", unsafe_allow_html=True)
        else:
            late = s["day"] - s["clen"]
            cls, tip = PHASES[s["phase"]]
            st.markdown(ring(min(s["day"], s["clen"]) / s["clen"], f"Day {s['day']}", f"{s['phase']} phase"), unsafe_allow_html=True)
            cells = "".join(f"<i class='{PHASES['Menstrual' if d <= s['plen'] else 'Follicular' if d < s['ov'] - 1 else 'Ovulation window' if d <= s['ov'] + 1 else 'Luteal'][0]}{' t' if d == s['day'] else ''}'></i>" for d in range(1, s["clen"] + 1))
            st.markdown(f"<div class='cyc'>{cells}</div>", unsafe_allow_html=True)
            when = f"expected {s['nxt'].strftime('%d %b')} (in {(s['nxt'] - date.today()).days} days)" if late < 0 else f"{late} day(s) later than your usual cycle"
            st.markdown(f"<div class='card'><b>Next period:</b> {when}<br><small>Average cycle {s['clen']} days · period {s['plen']} days · based on {s['n']} log(s)</small></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='card'>{tip}</div>", unsafe_allow_html=True)
            st.caption("Predictions are estimates from your own history and are not a contraception or fertility method. "
                       "See a doctor if cycles are shorter than 21 or longer than 35 days, you miss 3 periods, or bleeding/pain is severe.")
    with right:
        st.subheader("Log")
        d = st.date_input("Period started on", date.today(), max_value=date.today(), key="ps")
        if st.button("Save period start"):
            q("INSERT OR IGNORE INTO cycles(user_id,start) VALUES(?,?)", (u["id"], d.isoformat()), commit=True)
            st.rerun()
        if s:
            e = st.date_input("Period ended on", min(date.today(), s["last"] + timedelta(days=s["plen"] - 1)), min_value=s["last"], max_value=date.today(), key="pe")
            if st.button("Save period end"):
                q("UPDATE cycles SET plen=? WHERE user_id=? AND start=?", ((e - s["last"]).days + 1, u["id"], s["last"].isoformat()), commit=True)
                st.rerun()
        with st.form("cn"):
            flow = st.select_slider("Today's flow", ["None", "Spotting", "Light", "Medium", "Heavy"])
            sym = st.multiselect("Symptoms", SYMPTOMS)
            if st.form_submit_button("Save today"):
                q("INSERT INTO cycle_notes(user_id,day,flow,symptoms) VALUES(?,?,?,?) ON CONFLICT(user_id,day) DO UPDATE SET flow=excluded.flow, symptoms=excluded.symptoms",
                  (u["id"], date.today().isoformat(), flow, ", ".join(sym)), commit=True)
                st.success("Saved.")
    with st.expander("Past cycles and symptom log"):
        st.dataframe(pd.DataFrame([dict(r) for r in q("SELECT start, plen AS period_days FROM cycles WHERE user_id=? ORDER BY start DESC", (u["id"],))]), use_container_width=True, hide_index=True)
        st.dataframe(pd.DataFrame([dict(r) for r in q("SELECT day, flow, symptoms FROM cycle_notes WHERE user_id=? ORDER BY day DESC LIMIT 30", (u["id"],))]), use_container_width=True, hide_index=True)

# ---------------------------------------------------------------- move + mind exercises
EX = [
 ("box", "Box breathing", "Mind", 4, "Calms nerves before exams or when anxious.", ["Sit tall, shoulders loose.", "Breathe in for 4 counts, hold 4, out 4, hold 4.", "Follow the circle: grow = in, shrink = out. Repeat 8 rounds."]),
 ("g54321", "5-4-3-2-1 grounding", "Mind", 3, "Pulls you out of a spiral of worry or a panic wave.", ["Name 5 things you see.", "4 you can touch, 3 you hear.", "2 you smell, 1 you taste. Breathe slowly."]),
 ("scan", "Body scan", "Mind", 8, "Releases hidden tension and helps you fall asleep.", ["Lie down, eyes closed.", "Move attention from toes up to the scalp, one area at a time.", "Soften each area on the exhale."]),
 ("pmr", "Muscle relaxation", "Mind", 10, "Tense-and-release to lower stress and ease sleep.", ["Clench fists 5 s, release for 10 s.", "Repeat for arms, shoulders, face, belly, legs, feet.", "Notice the difference between tight and loose."]),
 ("grat", "Three good things", "Mind", 5, "Journaling that is linked with better mood over time.", ["Write 3 things that went okay today.", "Next to each, write why it happened.", "Read them once, slowly."]),
 ("dump", "Worry dump", "Mind", 5, "Gets looping thoughts out of your head.", ["Set a 5-minute timer and write every worry.", "Circle what you can act on, write one tiny next step.", "Close the page. Those thoughts have a home now."]),
 ("desk", "Desk reset", "Body", 5, "Undoes hours of study posture.", ["Neck rolls x5 each way.", "Shoulder shrugs x10, chest-opener stretch 30 s.", "Stand, reach up, forward fold 30 s."]),
 ("circuit", "No-equipment circuit", "Body", 15, "Strength and heart rate with zero gear.", ["Warm up 2 min (march, arm circles).", "Squats x15, push-ups x8-12 (knees ok), plank 30 s, lunges x10 each leg.", "Rest 45 s, repeat 3 rounds. Cool down stretch."]),
 ("walk", "Brisk walk intervals", "Body", 20, "Easy cardio that also lifts mood.", ["Walk easy 3 min.", "Fast pace 2 min, easy 2 min, repeat 4 times.", "Finish with 3 min easy."]),
 ("yoga", "Gentle yoga flow", "Cycle-friendly", 12, "Eases cramps and bloating; good in the menstrual and luteal phases.", ["Child's pose 1 min.", "Cat-cow x10, supine twist 1 min each side.", "Reclined butterfly 2 min, deep belly breaths."]),
 ("hips", "Hip and lower-back release", "Cycle-friendly", 8, "Targets the areas that ache most during periods.", ["Knees-to-chest rock 1 min.", "Figure-four stretch 1 min each side.", "Pelvic tilts x15, finish lying flat for 2 min."])]

def page_move(u):
    st.header("Move + Mind quests")
    st.caption("Choose a quest, start the timer, and move through the steps at your own pace. Every completed quest earns 15 XP.")
    s = cycle_stats(u["id"])
    if s and s["phase"] in ("Menstrual", "Luteal"):
        st.markdown("<div class='card'>Lower-energy day? The <b>Cycle-friendly</b> quests are designed for gentler movement.</div>", unsafe_allow_html=True)
    cat = st.radio("Quest type", ["All", "Mind", "Body", "Cycle-friendly"], horizontal=True, label_visibility="collapsed")
    done = {r["ex"] for r in q("SELECT ex FROM ex_done WHERE user_id=? AND day=?", (u["id"], date.today().isoformat()))}
    items = [e for e in EX if cat in ("All", e[2])]
    cols = st.columns(2)
    for i, (eid, name, kind, mins, why, steps) in enumerate(items):
        with cols[i % 2]:
            with st.container(border=True):
                status = "COMPLETED" if eid in done else f"LEVEL 1 · {mins} MIN"
                st.markdown(f"<div class='quest-title'><b>{name}</b><br><small>{kind} · {status}</small></div>", unsafe_allow_html=True)
                st.write(why)
                with st.expander("Start this quest"):
                    st.markdown(f"<div class='card'><b>Level 1 · Ready?</b><br>Set aside {mins} minutes, then follow each step in order.</div>", unsafe_allow_html=True)
                    try:
                        st.image("/vercel/share/v0-project/exercise-guide.png", use_container_width=True)
                    except:
                        pass
                    st.markdown(f"<div id='timer-{eid}' style='text-align:center;font-family:Chakra Petch;font-size:2.6rem;font-weight:700;color:#3e683d;margin:12px 0'>00:{mins:02d}:00</div><script>setInterval(function(){{const el=document.getElementById('timer-{eid}');if(!el)return;let t=el.dataset.t?Number(el.dataset.t):{mins}*60; t=Math.max(0,t-1);el.dataset.t=t;el.textContent='00:'+String(Math.floor(t/60)).padStart(2,'0')+':'+String(t%60).padStart(2,'0')}},1000)</script>", unsafe_allow_html=True)
                    for n, text in enumerate(steps, 1):
                        st.markdown(f"**Step {n}.** {text}")
                if eid in done:
                    st.success("Quest complete · +15 XP")
                elif st.button("Complete quest", key=f"ex{eid}"):
                    q("INSERT OR IGNORE INTO ex_done(user_id,day,ex) VALUES(?,?,?)", (u["id"], date.today().isoformat(), eid), commit=True)
                    st.rerun()

def page_health(u):
    st.header("My Health")
    st.caption("Leave a field empty if you didn't measure it - a missing entry is not the same as a low one.")
    with st.form("log"):
        d = st.date_input("Date", date.today(), max_value=date.today())
        c = st.columns(5)
        sleep = c[0].number_input("Sleep (h)", 0.0, 24.0, value=None, step=0.5)
        water = c[1].number_input("Water (L)", 0.0, 15.0, value=None, step=0.25)
        act = c[2].number_input("Activity (min)", 0, 1440, value=None, step=5)
        mood = c[3].number_input("Mood (1-5)", 1, 5, value=None)
        wt = c[4].number_input("Weight kg (optional)", 0.0, 400.0, value=None, step=0.1)
        if st.form_submit_button("Save entry"):
            old = q("SELECT * FROM logs WHERE user_id=? AND day=?", (u["id"], d.isoformat()), one=True)
            new = [sleep, water, act, mood, wt]
            if old:  # keep previous values for fields left empty
                new = [n if n is not None else old[k] for n, k in zip(new, ["sleep", "water", "activity", "mood", "weight"])]
            q("""INSERT INTO logs(user_id,day,sleep,water,activity,mood,weight) VALUES(?,?,?,?,?,?,?)
                 ON CONFLICT(user_id,day) DO UPDATE SET sleep=excluded.sleep, water=excluded.water,
                 activity=excluded.activity, mood=excluded.mood, weight=excluded.weight""",
              (u["id"], d.isoformat(), *new), commit=True)
            st.success("Saved!")
    rng = st.radio("Range", [7, 30, 90], horizontal=True, format_func=lambda x: f"{x} days")
    df = logs_df(u["id"], rng)
    if df.empty:
        st.info("No entries in this range yet.")
        return
    for col, label, goal in [("sleep", "Sleep (h)", u["goal_sleep"]), ("water", "Water (L)", u["goal_water"]),
                             ("activity", "Activity (min)", u["goal_activity"]), ("mood", "Mood (1-5)", None)]:
        if df[col].notna().any():
            fig = px.line(df, x="day", y=col, markers=True, title=label, color_discrete_sequence=["#FF6A1A"])
            if goal:
                fig.add_hline(y=goal, line_dash="dash", annotation_text="goal")
            fig.update_traces(connectgaps=False, line=dict(width=3))
            fig.update_layout(template="plotly_white", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                              margin=dict(l=10, r=10, t=50, b=10), font=dict(family="Nunito", color="#26352b"))
            st.plotly_chart(fig, use_container_width=True)
    st.subheader("Weekly summary")
    wk = df.set_index("day").resample("W")[["sleep", "water", "activity", "mood"]].mean().round(1)
    st.dataframe(wk, use_container_width=True)

def page_chat(u):
    st.header("AI Companion")
    cfg = st.expander("AI settings")
    st.caption("General health guidance, self-care tips and routine fixes. Not a diagnosis - see a doctor for serious or lasting symptoms.")
    cfg.selectbox("AI provider", list(PROVIDERS), key="provider")
    cfg.text_input("API key (optional)", type="password", key="api_key",
                          help="Paste a key from your chosen provider to enable smarter AI replies. Without it the built-in health guide is used.")
    kind, _, dm = ai_config()
    cfg.text_input("Model name", value=dm, key=f"ai_model_{kind}")
    if kind == "compat":
        cfg.text_input("Base URL", placeholder="https://api.groq.com/openai/v1", key="ai_base")
    has_key = bool(ai_config()[1])
    if kind == "gemini" and has_key and cfg.button("Show Gemini models my key can use"):
        try:
            req = urllib.request.Request("https://generativelanguage.googleapis.com/v1beta/models?pageSize=100",
                                         headers={"x-goog-api-key": ai_config()[1], "User-Agent": "HealthMate/1.0"})
            with urllib.request.urlopen(req, timeout=30) as r:
                ms = json.loads(r.read()).get("models", [])
            names = [m["name"].split("/")[-1] for m in ms if "generateContent" in m.get("supportedGenerationMethods", [])]
            cfg.success("Copy one of these into Model name:\n\n" + "\n".join(f"- {n}" for n in names if "gemini" in n))
        except Exception as e:
            d = e.read().decode()[:200] if hasattr(e, "read") else ""
            cfg.error(f"{e} {d}")
    if cfg.button("Test AI connection"):
        r = ai_reply("Reply with exactly: connected", u, [])
        if r:
            cfg.success("Connected: " + r[:60])
        else:
            cfg.error(st.session_state.pop("ai_err", None) or "No API key entered yet (press Enter after pasting it).")
    st.info("🧠 AI mode is on" if has_key else "📚 Built-in health guide mode. Pick a provider and add an API key in the sidebar for open-ended AI answers.")
    err = st.session_state.pop("ai_err", None)
    if err and has_key:
        st.warning(f"AI call failed, so the built-in guide answered instead. Reason: {err}")
    with st.expander("🗓️ Fix my routine"):
        c = st.columns(3)
        wake = c[0].time_input("Wake-up time", dtime(7, 0))
        study = c[1].number_input("Study/work hours", 0.0, 14.0, 3.0, 0.5)
        if c[2].button("Build my routine"):
            st.markdown(make_routine(u, wake.hour + wake.minute / 60, study))
    hist = q("SELECT role,text FROM chat WHERE user_id=? ORDER BY id", (u["id"],))
    if not hist:
        st.chat_message("assistant").write("Hi! Tell me a symptom (e.g. *I have a headache*), ask me to fix your routine, or say *explain my report*.")
    for r in hist:
        st.chat_message(r["role"]).write(r["text"])
    if p := st.chat_input("Type a message..."):
        with st.spinner("Thinking..."):
            ans = bot_reply(p, u, hist)
        now = datetime.now().isoformat()
        q("INSERT INTO chat(user_id,role,text,created) VALUES(?,?,?,?)", (u["id"], "user", p, now), commit=True)
        q("INSERT INTO chat(user_id,role,text,created) VALUES(?,?,?,?)", (u["id"], "assistant", ans, now), commit=True)
        st.rerun()

TYPES = ["🏃 Run", "🚶 Walk / Workout", "😴 Sleep", "💧 Hydration", "🧘 Meditation", "📈 Weekly summary", "✍️ Custom"]

def story_stats(kind, u):
    today = q("SELECT * FROM logs WHERE user_id=? AND day=?", (u["id"], date.today().isoformat()), one=True)
    def tv(col, default):
        return float(today[col]) if today and today[col] is not None else default
    if kind == TYPES[0]:
        c = st.columns(3)
        dist = c[0].number_input("Distance (km)", 0.1, 300.0, 5.0, 0.1, key="r_d")
        mn = c[1].number_input("Minutes", 0, 999, 25, key="r_m")
        sc = c[2].number_input("Seconds", 0, 59, 0, key="r_s")
        pace = int(round((mn * 60 + sc) / dist))
        return [("Distance", f"{dist:.2f} km"), ("Pace", f"{pace // 60}:{pace % 60:02d} /km"), ("Time", f"{mn}m {sc:02d}s")]
    if kind == TYPES[1]:
        c = st.columns(3)
        mn = c[0].number_input("Duration (min)", 1, 600, 30, key="w_m")
        dist = c[1].number_input("Distance km (0 = skip)", 0.0, 100.0, 0.0, 0.1, key="w_d")
        steps = c[2].number_input("Steps (0 = skip)", 0, 100000, 0, 100, key="w_s")
        out = [("Duration", f"{mn} min")]
        if dist: out.append(("Distance", f"{dist:.2f} km"))
        if steps: out.append(("Steps", f"{steps:,}"))
        return out
    if kind == TYPES[2]:
        c = st.columns(2)
        h = c[0].number_input("Hours slept", 0.0, 24.0, tv("sleep", 7.5), 0.5, key="s_h")
        g = c[1].number_input("Goal (h)", 4.0, 12.0, float(u["goal_sleep"]), 0.5, key="s_g")
        return [("Slept", f"{h:g} h"), ("Goal", f"{g:g} h")]
    if kind == TYPES[3]:
        c = st.columns(2)
        w = c[0].number_input("Water (L)", 0.0, 15.0, tv("water", 2.0), 0.25, key="h_w")
        g = c[1].number_input("Goal (L)", 0.5, 8.0, float(u["goal_water"]), 0.25, key="h_g")
        return [("Water", f"{w:g} L"), ("Goal", f"{g:g} L")]
    if kind == TYPES[4]:
        c = st.columns(2)
        m = c[0].number_input("Session (min)", 1, 300, 10, key="m_m")
        sk = c[1].number_input("Streak (days)", 0, 3650, streak(u["id"]), key="m_s")
        return [("Session", f"{m} min"), ("Streak", f"{sk} days")]
    if kind == TYPES[5]:
        df = logs_df(u["id"], 7)
        out = []
        if st.checkbox("Days logged", True): out.append(("Days logged", f"{len(df)} / 7"))
        if st.checkbox("Active days (goal met)", True): out.append(("Active days", str(int((df["activity"] >= u["goal_activity"]).sum()))))
        if st.checkbox("Average sleep", False) and df["sleep"].notna().any(): out.append(("Avg sleep", f"{df['sleep'].mean():.1f} h"))
        if st.checkbox("Logging streak", False): out.append(("Streak", f"{streak(u['id'])} days"))
        return out
    out = []
    for i in range(3):
        c = st.columns(2)
        l, v = c[0].text_input(f"Label {i + 1}", key=f"cl{i}", max_chars=16), c[1].text_input(f"Value {i + 1}", key=f"cv{i}", max_chars=14)
        if l and v: out.append((l, v))
    return out

def _center(d, y, text, f, fill, shadow=True):
    w = d.textlength(text, font=f)
    x = (720 - w) / 2
    if shadow:
        d.text((x + 2, y + 3), text, font=f, fill=(0, 0, 0))
    d.text((x, y), text, font=f, fill=fill)

def make_story(bg, theme, stats, caption, name, kind):
    W, H = 720, 1080
    if bg:
        img = ImageOps.fit(ImageOps.exif_transpose(Image.open(io.BytesIO(bg))).convert("RGB"), (W, H))
        img = Image.blend(img, Image.new("RGB", (W, H), (0, 0, 0)), 0.3)
    else:
        c1, c2 = THEMES[theme]
        img = Image.new("RGB", (W, H))
        pxl = img.load()
        for y in range(H):
            t = y / H
            col = tuple(int(c1[i] * (1 - t) + c2[i] * t) for i in range(3))
            for x in range(W):
                pxl[x, y] = col
    d = ImageDraw.Draw(img)
    tag = kind.split(" ", 1)[1].upper()
    _center(d, 80, tag, font(30), (255, 255, 255))
    d.rounded_rectangle((300, 128, 420, 134), 3, fill=(255, 106, 0))
    y = 230
    stats = stats or [("Feeling", "Good")]
    for label, val in stats[:4]:
        _center(d, y, label, font(34), (235, 235, 245))
        size = 92
        while size > 40 and d.textlength(val, font=font(size)) > W - 80:
            size -= 6
        _center(d, y + 48, val, font(size), (255, 255, 255))
        y += 190 if len(stats) <= 3 else 160
    if caption:
        for i, ln in enumerate(textwrap.wrap(caption, 26)[:2]):
            _center(d, 820 + i * 50, ln, font(36), (255, 255, 255))
    _center(d, 950, "HEALTHMATE", font(58), (255, 255, 255))
    _center(d, 1022, f"@{name}", font(28), (225, 225, 240), shadow=False)
    buf = io.BytesIO()
    img.save(buf, "PNG")
    return buf.getvalue()

def page_stories(u):
    st.header("Stories")
    t1, t2 = st.tabs(["✨ Create", "👀 View"])
    with t1:
        left, right = st.columns([1.2, 1])
        with left:
            kind = st.selectbox("What are you sharing?", TYPES)
            stats = story_stats(kind, u)
            src = st.radio("Background", ["📸 Take a photo", "🖼️ Upload photo", "🎨 Gradient"], horizontal=True)
            bg, theme = None, "Lavender"
            if src.startswith("📸"):
                shot = st.camera_input("Take a photo")
                bg = shot.getvalue() if shot else None
            elif src.startswith("🖼️"):
                up = st.file_uploader("Choose a photo", type=["png", "jpg", "jpeg", "webp"])
                bg = up.getvalue() if up else None
            else:
                theme = st.selectbox("Gradient", list(THEMES))
            cap = st.text_input("Caption", max_chars=60)
            perm = st.checkbox("Keep permanently (otherwise expires in 24h)")
        with right:
            card = make_story(bg, theme, stats, cap, u["username"], kind)
            st.image(card, caption="Preview", use_container_width=True)
            if st.button("🚀 Share to story"):
                q("INSERT INTO stories(user_id,kind,caption,img,created,permanent) VALUES(?,?,?,?,?,?)",
                  (u["id"], kind, cap, card, datetime.now().isoformat(), int(perm)), commit=True)
                st.success("Shared with your friends!")
        st.caption("🔒 Only what you enter here is shown. Symptoms, medical history and chats are never added automatically.")
    with t2:
        story_viewer(visible_stories(u["id"]), u["id"], "s")

def page_history(u):
    st.header("History")
    t1, t2, t3 = st.tabs(["Health log history", "Medical history", "Chat history"])
    with t1:
        st.caption("Add past days from **My Health** by choosing an earlier date. Edit or delete entries here.")
        df = logs_df(u["id"])
        if df.empty:
            st.info("No entries yet.")
        else:
            df["day"] = df["day"].dt.strftime("%Y-%m-%d")
            df = df.sort_values("day", ascending=False)
            ed = st.data_editor(df, hide_index=True, disabled=["day"], use_container_width=True, key="hist")
            c = st.columns(3)
            if c[0].button("Save changes"):
                for _, r in ed.iterrows():
                    v = [None if pd.isna(r[k]) else float(r[k]) for k in ("sleep", "water", "activity", "mood", "weight")]
                    for i in (2, 3):
                        v[i] = None if v[i] is None else int(round(v[i]))
                    q("UPDATE logs SET sleep=?,water=?,activity=?,mood=?,weight=? WHERE user_id=? AND day=?",
                      (*v, u["id"], r["day"]), commit=True)
                st.success("Updated.")
            c[1].download_button("Download CSV", df.to_csv(index=False), "healthmate_history.csv", "text/csv")
            d = st.selectbox("Delete an entry", df["day"])
            if st.button("Delete selected day"):
                q("DELETE FROM logs WHERE user_id=? AND day=?", (u["id"], d), commit=True)
                st.rerun()
    with t2:
        st.caption("🔒 Private. Only you and the AI Companion (if allowed below) can see this. Never shown to friends or in stories.")
        m = med_hist(u["id"])
        g = lambda k: (m[k] or "") if m else ""
        with st.form("med"):
            cond = st.text_area("Existing conditions", g("conditions"), placeholder="e.g. asthma")
            alg = st.text_area("Allergies", g("allergies"), placeholder="e.g. penicillin, peanuts")
            meds = st.text_area("Current medicines", g("medications"))
            notes = st.text_area("Other notes (past surgeries, family history...)", g("notes"))
            use = st.checkbox("Let the AI Companion use this to personalise advice", bool(u["memory_ok"]))
            if st.form_submit_button("Save medical history"):
                q("""INSERT INTO medical(user_id,conditions,allergies,medications,notes) VALUES(?,?,?,?,?)
                     ON CONFLICT(user_id) DO UPDATE SET conditions=excluded.conditions, allergies=excluded.allergies,
                     medications=excluded.medications, notes=excluded.notes""",
                  (u["id"], cond, alg, meds, notes), commit=True)
                q("UPDATE users SET memory_ok=? WHERE id=?", (int(use), u["id"]), commit=True)
                st.success("Saved.")
    with t3:
        rows = q("SELECT role,text,created FROM chat WHERE user_id=? ORDER BY id DESC LIMIT 100", (u["id"],))
        for r in rows:
            st.markdown(f"**{'You' if r['role'] == 'user' else 'HealthMate'}** ({r['created'][:16]}): {r['text']}")
        if rows and st.button("Clear chat history"):
            q("DELETE FROM chat WHERE user_id=?", (u["id"],), commit=True)
            st.rerun()
        if not rows:
            st.info("No chats yet.")

def page_friends(u):
    st.header("Friends & Challenges")
    t1, t2 = st.tabs(["Friends", "Challenges"])
    with t1:
        name = st.text_input("Add a friend by username")
        if st.button("Send request"):
            f = q("SELECT id FROM users WHERE username=?", (name.strip().lower(),), one=True)
            if not f or f["id"] == u["id"]:
                st.error("User not found.")
            else:
                q("INSERT OR IGNORE INTO friends VALUES(?,?,'pending')", (u["id"], f["id"]), commit=True)
                st.success("Request sent!")
        for r in q("SELECT f.a, us.display FROM friends f JOIN users us ON us.id=f.a WHERE f.b=? AND f.status='pending'", (u["id"],)):
            c = st.columns([3, 1])
            c[0].write(f"{r['display']} wants to be friends")
            if c[1].button("Accept", key=f"acc{r['a']}"):
                q("UPDATE friends SET status='accepted' WHERE a=? AND b=?", (r["a"], u["id"]), commit=True)
                st.rerun()
        st.subheader("Your friends")
        fr = friend_ids(u["id"])
        for i in fr:
            st.write("💜 " + q("SELECT display FROM users WHERE id=?", (i,), one=True)["display"])
        if not fr:
            st.info("No friends yet.")
    with t2:
        st.caption("Progress counts days a goal was met - no weights, calories or medical numbers are shown.")
        for ch in q("SELECT * FROM challenges"):
            mem = q("SELECT m.*, us.display FROM members m JOIN users us ON us.id=m.user_id WHERE challenge_id=?", (ch["id"],))
            allowed = set(friend_ids(u["id"])) | {u["id"]}
            st.markdown(f"**{ch['name']}**")
            if not any(m["user_id"] == u["id"] for m in mem):
                if st.button("Join", key=f"j{ch['id']}"):
                    q("INSERT INTO members VALUES(?,?,?)", (ch["id"], u["id"], date.today().isoformat()), commit=True)
                    st.rerun()
            for m in mem:
                if m["user_id"] not in allowed:
                    continue
                start = date.fromisoformat(m["start"])
                n = q(f"SELECT COUNT(*) n FROM logs WHERE user_id=? AND day>=? AND day<=? AND {ch['metric']}>=?",
                      (m["user_id"], m["start"], (start + timedelta(days=ch["days"] - 1)).isoformat(), ch["threshold"]), one=True)["n"]
                st.progress(min(n / ch["days"], 1.0), text=f"{m['display']}: {n}/{ch['days']} days")
                if n >= ch["days"] and m["user_id"] == u["id"]:
                    st.success("🏅 Challenge complete!")

def page_profile(u):
    st.header("Profile")
    with st.form("prof"):
        dn = st.text_input("Display name", u["display"])
        c = st.columns(3)
        gs = c[0].number_input("Sleep goal (h)", 4.0, 12.0, float(u["goal_sleep"]), 0.5)
        gw = c[1].number_input("Water goal (L)", 0.5, 8.0, float(u["goal_water"]), 0.25)
        ga = c[2].number_input("Activity goal (min)", 5, 300, int(u["goal_activity"]), 5)
        if st.form_submit_button("Save"):
            q("UPDATE users SET display=?, goal_sleep=?, goal_water=?, goal_activity=? WHERE id=?",
              (dn, gs, gw, ga, u["id"]), commit=True)
            st.success("Saved.")
    st.subheader("Badges")
    df = logs_df(u["id"])
    badges = []
    if streak(u["id"]) >= 7: badges.append("Consistency Champion")
    if (df["activity"] >= u["goal_activity"]).sum() >= 7: badges.append("Walking Streak")
    if (df["sleep"] >= 7).sum() >= 7: badges.append("Sleep Routine Progress")
    st.write(" · ".join(f"🏅 {b}" for b in badges) or "Keep logging to earn badges!")
    if st.button("Delete all my stories"):
        q("DELETE FROM stories WHERE user_id=?", (u["id"],), commit=True)
        st.success("Done.")
    if st.button("Log out"):
        st.session_state.clear()
        st.rerun()

# ---------------------------------------------------------------- main
init_db()
if "uid" not in st.session_state:
    page_auth()
else:
    u = user()
    pages = {"Home": page_home, "My Health": page_health, "Move & Mind": page_move, "Cycle": page_cycle,
             "AI Companion": page_chat, "Stories": page_stories, "Friends & Challenges": page_friends,
             "History": page_history, "Profile": page_profile}
    st.markdown(f"<div class='top'><div class='brand'>Health<i>Mate</i> · <div class='pixel-cat' style='display:inline-block' role='img' aria-label='Your cat companion'></div></div><div class='me'><b>{html.escape(u['display'][:1].upper())}</b>{html.escape(u['display'])}</div></div>", unsafe_allow_html=True)
    with st.sidebar:
        st.markdown("<div style='font-family:Chakra Petch;font-size:1rem;font-weight:700;color:#426b3d;margin:12px 0 20px'>Navigation</div>", unsafe_allow_html=True)
        choice = st.radio("Go to", list(pages), label_visibility="collapsed")
        st.divider()
        st.caption("Small steps build strong habits.")
    pages[choice](u)
    st.caption("General wellness info only - not medical advice.")
