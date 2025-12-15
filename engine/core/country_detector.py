COUNTRY_KEYWORDS = {
    "US": [
        # Country names
        "usa", "america", "american", "united states",
        
        # Major cities
        "washington", "new york", "nyc", "los angeles", "chicago",
        "boston", "san francisco", "miami", "texas", "california",
        
        # Political
        "biden", "trump", "congress", "senate", "house of representatives",
        "white house", "pentagon", "capitol", "democrats", "republicans",
        
        # Currency
        "dollar", "usd",
        
        # Organizations
        "fbi", "cia", "nasa", "federal reserve"
    ],
    
    "UK": [
        # Country names
        "britain", "british", "uk", "united kingdom", "england",
        "scotland", "wales", "northern ireland",
        
        # Cities
        "london", "manchester", "birmingham", "edinburgh", "glasgow",
        
        # Political
        "downing street", "parliament uk", "sunak", "starmer",
        "conservative", "labour party", "westminster",
        
        # Currency
        "pound", "sterling", "gbp",
        
        # Royalty
        "king charles", "royal family", "buckingham"
    ],
    
    "India": [
        # Country name
        "india", "indian", "bharat",
        
        # Cities
        "delhi", "mumbai", "bangalore", "kolkata", "chennai",
        "hyderabad", "pune", "ahmedabad",
        
        # Political
        "modi", "bjp", "congress party", "lok sabha", "rajya sabha",
        "parliament india", "amit shah",
        
        # States
        "karnataka", "maharashtra", "tamil nadu", "uttar pradesh",
        "gujarat", "rajasthan",
        
        # Currency
        "rupee", "inr",
        
        # Organizations
        "isro", "supreme court india"
    ],
    
    "Germany": [
        # Country name
        "germany", "german", "deutschland",
        
        # Cities
        "berlin", "munich", "frankfurt", "hamburg", "cologne",
        
        # Political
        "scholz", "bundestag", "bundesrat", "merkel",
        
        # Currency
        "euro germany",
        
        # Organizations
        "bundeswehr", "deutsche bank"
    ],
    
    "Japan": [
        # Country name
        "japan", "japanese", "nippon",
        
        # Cities
        "tokyo", "osaka", "kyoto", "hiroshima", "nagoya",
        
        # Political
        "kishida", "diet japan", "ldp japan",
        
        # Currency
        "yen", "jpy",
        
        # Organizations
        "bank of japan", "sony", "toyota"
    ]
}

def detect(text: str, min_score: int = 1) -> str:
    text = text.lower()
    scores = {}

    for country, keywords in COUNTRY_KEYWORDS.items():
        score = 0
        for keyword in keywords:
            if keyword in text:
                score += 1
        
            scores[country] = score
    

    max_country = max(scores, key=scores.get)
    max_score = scores[max_country]

    if max_score < min_score:
        return "Global"
    
    return max_country