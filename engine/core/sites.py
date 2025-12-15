GLOBAL = {
    "Reuters": "https://www.reuters.com",
    "AP News": "https://apnews.com",
    "BBC News": "https://www.bbc.com/news",
    "Financial Times": "https://www.ft.com",
    "The Economist": "https://www.economist.com"
}

US = {
    "Reuters US": "https://www.reuters.com/world/us",
    "Associated Press": "https://apnews.com",
    "Wall Street Journal": "https://www.wsj.com",
    "New York Times": "https://www.nytimes.com",
    "Bloomberg": "https://www.bloomberg.com"
}

UK = {
    "BBC News": "https://www.bbc.com/news",
    "Reuters UK": "https://www.reuters.com/world/uk",
    "The Guardian": "https://www.theguardian.com/uk",
    "Financial Times": "https://www.ft.com",
    "The Times": "https://www.thetimes.co.uk"
}

INDIA = {
    "The Hindu": "https://www.thehindu.com",
    "Indian Express": "https://indianexpress.com",
    "Reuters India": "https://www.reuters.com/world/india",
    "LiveMint": "https://www.livemint.com",
    "Hindustan Times": "https://www.hindustantimes.com"
}

GERMANY = {
    "Deutsche Welle": "https://www.dw.com/en",
    "Der Spiegel": "https://www.spiegel.de/international",
    "Reuters Germany": "https://www.reuters.com/world/europe",
    "FAZ": "https://www.faz.net/english",
    "Süddeutsche": "https://www.sueddeutsche.de"
}

JAPAN = {
    "NHK World": "https://www3.nhk.or.jp/nhkworld",
    "Reuters Japan": "https://www.reuters.com/world/asia-pacific",
    "Japan Times": "https://www.japantimes.co.jp",
    "Asahi Shimbun": "https://www.asahi.com/ajw",
    "Nikkei Asia": "https://asia.nikkei.com"
}

SITES = {
    "GLOBAL": GLOBAL,
    "US": US,
    "UK": UK,
    "INDIA": INDIA,
    "GERMANY": GERMANY,
    "JAPAN": JAPAN,
}

def all_sites() -> dict:
    return SITES

def sites_for_country(country: str) -> dict | None:
    return SITES.get(country.upper())

def all_countries() -> list[str]:
    return list(SITES.keys())