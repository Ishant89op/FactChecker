COUNTRY_KEYWORDS = {
    "US": [
        "usa", "america", "american", "united states",
        "washington", "new york", "nyc", "los angeles", "chicago",
        "boston", "san francisco", "miami", "texas", "california",
        "biden", "trump", "congress", "senate", "house of representatives",
        "white house", "pentagon", "capitol", "democrats", "republicans",
        "dollar", "usd", "fbi", "cia", "nasa", "federal reserve"
    ],
    "UK": [
        "britain", "british", "uk", "united kingdom", "england",
        "scotland", "wales", "northern ireland",
        "london", "manchester", "birmingham", "edinburgh", "glasgow",
        "downing street", "parliament uk", "sunak", "starmer",
        "conservative", "labour party", "westminster",
        "pound", "sterling", "gbp",
        "king charles", "royal family", "buckingham"
    ],
    "India": [
        "india", "indian", "bharat",
        "delhi", "mumbai", "bangalore", "kolkata", "chennai",
        "hyderabad", "pune", "ahmedabad",
        "modi", "bjp", "congress party", "lok sabha", "rajya sabha",
        "parliament india", "amit shah",
        "karnataka", "maharashtra", "tamil nadu", "uttar pradesh",
        "gujarat", "rajasthan",
        "rupee", "inr", "isro", "supreme court india"
    ],
    "Germany": [
        "germany", "german", "deutschland",
        "berlin", "munich", "frankfurt", "hamburg", "cologne",
        "scholz", "bundestag", "bundesrat", "merkel",
        "euro germany", "bundeswehr", "deutsche bank"
    ],
    "Japan": [
        "japan", "japanese", "nippon",
        "tokyo", "osaka", "kyoto", "hiroshima", "nagoya",
        "kishida", "diet japan", "ldp japan",
        "yen", "jpy", "bank of japan", "sony", "toyota"
    ]
}

def detect(text: str, min_score: int = 1) -> str:
    text_lower = text.lower()
    scores = {country: 0 for country in COUNTRY_KEYWORDS}

    for country, keywords in COUNTRY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text_lower:
                scores[country] += 1

    max_country = max(scores, key=scores.get)
    max_score = scores[max_country]

    return max_country if max_score >= min_score else "Global"