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

def extract_keywords(text: str, max_keywords: int = 50, min_length: int = 2) -> list:
    text_lower = text.lower()
    words = re.findall(r'\b[a-z0-9]+\b', text_lower)
    
    result = []
    seen = set()

    for word in words:
        if len(word) < min_length:
            continue
        if word not in STOP_WORDS and word not in seen:
            result.append(word)
            seen.add(word)
            
            if len(result) >= max_keywords:
                break
    
    return result

def extract_numbers(text: str) -> list[str]:
    return re.findall(r'\b\d+(?:\.\d+)?\b', text)

def create_phrases(keywords: list[str]) -> list[str]:
    phrases = []

    for r in (2, 3):
        for combo in combinations(keywords, r):
            phrases.append(" ".join(combo))

    return phrases

import re

def phrase_matcher(snippet: str, phrases: list[str]) -> int:
    text = snippet.lower()
    count = 0

    for phrase in phrases:
        pattern = rf'\b{re.escape(phrase.lower())}\b'
        if re.search(pattern, text):
            count += 1

    return count

def number_matcher(snippet: str, numbers: list[str]) -> int:
    text = snippet.lower()
    count = 0

    for num in numbers:
        pattern = rf'\b{re.escape(num)}\b'
        if re.search(pattern, text):
            count += 1

    return count