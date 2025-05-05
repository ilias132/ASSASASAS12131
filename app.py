import streamlit as st
import random
import qrcode
import io
import urllib.parse

# === CONFIGURATION ===
AFFILIATE_TAG = "giftgenie0d-21"

# === LANGUAGE & COUNTRY DATA ===
country_language_map = {
    "Germany": "de", "USA": "en", "UK": "en", "France": "fr",
    "Spain": "es", "Italy": "it", "Greece": "el", "Switzerland": "de",
    "Austria": "de", "Netherlands": "nl", "Belgium": "nl", "Canada": "en",
    "Australia": "en", "India": "hi", "Japan": "ja", "China": "zh-cn",
    # ... (extend for all countries)
}
currency_map = {
    "EUR": "€", "USD": "$", "GBP": "£", "CHF": "CHF",
    "JPY": "¥", "INR": "₹", "CNY": "¥", "AUD": "$"
    # ... (extend for all currencies)
}

# === TRANSLATION STUB ===
def translate(text, lang):
    # Placeholder: integrate actual translation API here
    return text  # For now, return original

# === AI-STYLE GIFT IDEAS ===
def ai_generate_ideas(occasion, recipient, hobbies, budget, eco_friendly):
    base = []
    for hobby in hobbies:
        tag = "Eco-" if eco_friendly else ""
        base.append(f"{tag}{hobby} Gift Box for {recipient} ({occasion})")
    random.shuffle(base)
    return base[:5]

# === AI GREETING CARD GENERATOR ===
def ai_generate_card(recipient, occasion, language):
    messages = [
        f"Dear {recipient}, best wishes on your {occasion}!",
        f"Happy {occasion}, {recipient}! Enjoy every moment.",
        f"Celebrating you, {recipient}, on this special {occasion}!"
    ]
    return random.choice(messages)

# === QR CODE GENERATOR ===
def get_qr_code(url):
    img = qrcode.make(url)
    buf = io.BytesIO()
    img.save(buf)
    buf.seek(0)
    return buf

# === STREAMLIT APP ===
st.set_page_config(page_title="GiftGenie Ultimate", layout="wide")
# Header
st.title("🎁 GiftGenie Ultimate")
st.write("Your AI-powered gift recommender – multilingual, multi-country, eco-friendly, and loaded with features!")

# Sidebar: Settings
st.sidebar.header("Settings")
country = st.sidebar.selectbox("Select Country", list(country_language_map.keys()))
lang = country_language_map[country]
currency = st.sidebar.selectbox("Select Currency", list(currency_map.keys()))
symbol = currency_map[currency]

off_eco = st.sidebar.checkbox("Eco-Friendly Only")

# User Inputs
occasions = ["Birthday", "Christmas", "Valentine's Day", "Anniversary", "Graduation", "Name Day", "Wedding"]
occasion = st.selectbox(translate("Occasion", lang), occasions)
recipient = st.text_input(translate("Recipient (name or role)", lang), "Friend")
hobbies = st.multiselect(translate("Hobbies/Interests", lang), ["Gaming","Cooking","Reading","Fitness","Music","Art","Travel","Tech"])
budget = st.slider(translate("Max Budget", lang) + f" ({symbol})", 10, 1000, 100)

# Actions
if st.button(translate("Get Gift Ideas", lang)):
    ideas = ai_generate_ideas(occasion, recipient, hobbies, budget, off_eco)
    st.subheader(translate("Recommended Gifts", lang))
    for idea in ideas:
        query = urllib.parse.quote_plus(idea)
        url = f"https://www.amazon.{('de' if country=='Germany' else 'com')}/s?k={query}&tag={AFFILIATE_TAG}"
        cols = st.columns([1,4,1])
        with cols[0]: st.image(get_qr_code(url))
        with cols[1]: 
    st.markdown(f"**{idea}**")  

Price: approx. {budget} {currency}  
[Buy on Amazon]({url})")
        with cols[2]: st.button("♥", key=idea)  # Wishlist placeholder

if st.button(translate("Generate Greeting Card", lang)):
    card = ai_generate_card(recipient, occasion, lang)
    st.subheader(translate("Your AI Greeting Card", lang))
    st.text_area(translate("Message", lang), card, height=200)

# Additional Features Section
with st.expander(translate("More Features", lang)):
    st.markdown("""
- Dark/Light Mode auto-detect
- Download wishlist as text file
- PDF export of recommendations
- Calendar reminder integration
- Social share links
- Email suggestion with mailto link
- Voice input placeholder
- Personalized packaging suggestions
- Multi-language support
- Eco-friendly filter
...and many more ready to be added dynamically!
""")

st.caption("Powered by Streamlit | Affiliate: giftgenie0d-21 | No API key needed | Legal for CH/EU")
