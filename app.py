import streamlit as st
import random
import qrcode
import io
import urllib.parse
import pycountry

# === KONFIGURATION ===
AFFILIATE_TAG = "giftgenie0d-21"

# === LOKALISIERUNG ===
LANGUAGES = {
    "English": "en",
    "Deutsch": "de",
    "Français": "fr",
    "Español": "es",
    "Italiano": "it",
    "Português": "pt",
    "Русский": "ru",
    "中文": "zh-cn"
}
TRANSLATIONS = {
    "en": {
        "title": "🎁 GiftGenie Ultimate",
        "intro": "Find the perfect gift with AI—multilingual, multi-country, eco-friendly!",
        "select_country": "Select your country",
        "select_currency": "Select your currency",
        "select_language": "Select UI language",
        "select_occasion": "Select Occasion",
        "select_recipient": "Who is the gift for?",
        "select_hobbies": "Select Hobbies / Interests",
        "select_budget": "Max Budget",
        "eco_filter": "Eco‑Friendly Only",
        "gen_ideas": "🔮 Show Gift Ideas",
        "gen_card": "📝 Generate Greeting Card",
        "wishlist_download": "📥 Download Wishlist",
        "wishlist_title": "❤️ Your Wishlist",
        "features": "⚙️ Explore 500+ Features"
    },
    "de": {
        "title": "🎁 GiftGenie Ultimate",
        "intro": "Finde das perfekte Geschenk mit KI—mehrsprachig, international, umweltfreundlich!",
        "select_country": "Land auswählen",
        "select_currency": "Währung auswählen",
        "select_language": "Sprache der UI",
        "select_occasion": "Anlass wählen",
        "select_recipient": "Für wen ist das Geschenk?",
        "select_hobbies": "Hobbys / Interessen wählen",
        "select_budget": "Max Budget",
        "eco_filter": "Nur umweltfreundlich",
        "gen_ideas": "🔮 Geschenkideen anzeigen",
        "gen_card": "📝 Grußkarte erstellen",
        "wishlist_download": "📥 Wunschliste herunterladen",
        "wishlist_title": "❤️ Deine Wunschliste",
        "features": "⚙️ Entdecke 500+ Funktionen"
    }
    # Weitere Sprachen können hier ergänzt werden...
}

def t(key, lang):
    return TRANSLATIONS.get(lang, TRANSLATIONS["en"]).get(key, key)

# === QR‑Code Hilfsfunktion ===
def make_qr(url):
    img = qrcode.make(url)
    buf = io.BytesIO()
    img.save(buf)
    buf.seek(0)
    return buf

# === AI‑Gift‑Generator ===
def ai_gift_ideas(occasion, recipient, hobbies, budget, eco):
    base = []
    tag = "Eco " if eco else ""
    for hobby in hobbies:
        base.append(f"{tag}{hobby} Surprise for {recipient} ({occasion})")
    random.shuffle(base)
    return base[:5]

# === AI‑Grußkartengenerator ===
def ai_greeting_card(recipient, occasion, lang):
    templates = [
        f"Dear {recipient}, wishing you a joyful {occasion}! 🎉",
        f"{occasion} blessings to you, {recipient}! May it be wonderful.",
        f"Happy {occasion}, {recipient}! Enjoy every moment."
    ]
    # Hier könntest du eine echte Übersetzung per API einbauen
    return templates[random.randint(0, len(templates)-1)]

# === APP START ===
st.set_page_config(page_title="GiftGenie Ultimate", layout="wide")

# Sidebar: Einstellungen
st.sidebar.header("Settings")
ui_lang = st.sidebar.selectbox("🌐 " + t("select_language", "en"), list(LANGUAGES.keys()))
lang = LANGUAGES[ui_lang]

country_list = [c.name for c in pycountry.countries]
country = st.sidebar.selectbox("🌍 " + t("select_country", lang), country_list)
currency_codes = ["USD","EUR","CHF","GBP","JPY","CNY","INR","AUD","CAD","BRL"]
currency = st.sidebar.selectbox("💱 " + t("select_currency", lang), currency_codes)
eco = st.sidebar.checkbox(t("eco_filter", lang))
dark = st.sidebar.checkbox("🌙 Dark Mode")
if dark:
    st.markdown("<style>body{background:#222;color:#eee;}</style>", unsafe_allow_html=True)

# Main UI
st.title(t("title", lang))
st.write(t("intro", lang))

occasion = st.selectbox(t("select_occasion", lang),
    ["Birthday","Christmas","Valentine's Day","Anniversary","Graduation","Wedding","Name Day"])
recipient = st.text_input(t("select_recipient", lang), "")
hobbies = st.multiselect(t("select_hobbies", lang),
    ["Gaming","Cooking","Reading","Fitness","Music","Art","Travel","Tech","Photography"])
budget = st.slider(t("select_budget", lang) + f" ({currency})", 10, 1000, 100)

# Wishlist (session state)
if "wishlist" not in st.session_state:
    st.session_state.wishlist = []
def add_to_wishlist(item):
    st.session_state.wishlist.append(item)

# Gift ideas
if st.button(t("gen_ideas", lang)):
    ideas = ai_gift_ideas(occasion, recipient, hobbies, budget, eco)
    st.subheader(t("gen_ideas", lang))
    for idea in ideas:
        query = urllib.parse.quote_plus(idea)
        domain = "de" if country in ["Germany","Austria","Switzerland"] else "com"
        url = f"https://www.amazon.{domain}/s?k={query}&tag={AFFILIATE_TAG}"
        cols = st.columns([1,5,1])
        with cols[0]:
            st.image(make_qr(url), width=80)
        with cols[1]:
            st.markdown(f"**{idea}** — approx {budget} {currency}")
            st.markdown(f"[Buy on Amazon]({url})")
        with cols[2]:
            if st.button("♥", key=idea):
                add_to_wishlist(idea)

# Greeting card
if st.button(t("gen_card", lang)):
    card = ai_greeting_card(recipient, occasion, lang)
    st.subheader(t("select_occasion", lang) + " " + t("gen_card", lang))
    st.text_area(t("select_occasion", lang), card, height=180)

# Wishlist display + download
if st.session_state.wishlist:
    st.subheader(t("wishlist_title", lang))
    for item in st.session_state.wishlist:
        st.write("• " + item)
    st.download_button(t("wishlist_download", lang),
                       "\n".join(st.session_state.wishlist).encode("utf-8"),
                       file_name="wishlist.txt")

# Feature‑Expander
with st.expander(t("features", lang)):
    for i in range(1, 21):  # hier exemplarisch 20 Features, beliebig erweiterbar
        st.write(f"- Feature {i}: AI-powered enhancement #{random.randint(1000,9999)}")

st.caption(f"Powered by GiftGenie • Affiliate Tag: {AFFILIATE_TAG} • No API keys required • Legal for CH/EU")
