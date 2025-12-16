import re
from itertools import combinations

STOP_WORDS = {
    'a', 'an', 'the', 'and', 'or', 'but', 'nor', 'yet', 'so',
    'in', 'on', 'at', 'by', 'for', 'with', 'about', 'as', 'to', 'from',
    'of', 'off', 'up', 'down', 'over', 'under', 'into', 'through',
    'i', 'you', 'he', 'she', 'it', 'we', 'they', 'them', 'their',
    'this', 'that', 'these', 'those', 'my', 'your', 'his', 'her', 'its',
    'is', 'am', 'are', 'was', 'were', 'be', 'been', 'being',
    'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing',
    'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can',
    'not', 'no', 'yes', 'all', 'any', 'some', 'more', 'most', 'such',
    'very', 'too', 'also', 'just', 'only', 'now', 'then', 'than',
    'here', 'there', 'when', 'where', 'why', 'how', 'who', 'which', 'what'
}

def extract_keywords(text: str, min_length: int = 3) -> list:
    text = text.lower()
    words = re.findall(rf'\b[a-z][a-z0-9]{{{min_length}-1,}}\b', text)
    keywords = []
    seen = set()

    for word in words:
        if word in STOP_WORDS:
            continue
        
        if word in seen:
            continue
        
        keywords.append(word)
        seen.add(word)
    
    return keywords

def extract_dates(text: str) -> list:
    patterns = [
        r'\b(19|20)\d{2}\b',
        r'\b(january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{1,2},?\s+(19|20)\d{2}\b',
        r'\b\d{1,2}\s+(january|february|march|april|may|june|july|august|september|october|november|december)\s+(19|20)\d{2}\b',
        r'\b(january|february|march|april|may|june|july|august|september|october|november|december)\s+(19|20)\d{2}\b',
    ]
    
    dates = []
    text_lower = text.lower()
    
    for pattern in patterns:
        matches = re.findall(pattern, text_lower)
        for match in matches:
            if isinstance(match, tuple):
                date_str = ' '.join(str(m) for m in match if m)
            else:
                date_str = match
            if date_str not in dates:
                dates.append(date_str)
    
    return dates

def create_phrases(keywords: list, min_size: int = 2, max_size: int = 4, max_phrases: int = 20) -> list:
    phrases = []
    
    for size in range(min_size, min(max_size + 1, len(keywords) + 1)):
        for i in range(len(keywords) - size + 1):
            phrase = ' '.join(keywords[i:i+size])
            phrases.append(phrase)
            
            if len(phrases) >= max_phrases:
                return phrases
    
    return phrases

def extract_phrases_and_dates(text: str) -> dict:
    keywords = extract_keywords(text)
    phrases = create_phrases(keywords[:15])
    dates = extract_dates(text)
    
    return {
        "keywords": keywords[:10],
        "phrases": phrases,
        "dates": dates
    }