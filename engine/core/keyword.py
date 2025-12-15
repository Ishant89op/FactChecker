import re

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

def keywords(text: str, max_keywords: int = 50, min_length: int = 2) -> list:
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