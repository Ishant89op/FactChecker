import re

STOP_WORDS = {
    # Articles
    'a', 'an', 'the',
    
    # Conjunctions
    'and', 'or', 'but', 'nor', 'yet', 'so',
    
    # Prepositions
    'in', 'on', 'at', 'by', 'for', 'with', 'about', 'as', 'to', 'from',
    'of', 'off', 'up', 'down', 'over', 'under', 'into', 'through',
    
    # Pronouns
    'i', 'you', 'he', 'she', 'it', 'we', 'they', 'them', 'their',
    'this', 'that', 'these', 'those', 'my', 'your', 'his', 'her', 'its',
    
    # Verbs (common)
    'is', 'am', 'are', 'was', 'were', 'be', 'been', 'being',
    'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing',
    'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can',
    
    # Others
    'not', 'no', 'yes', 'all', 'any', 'some', 'more', 'most', 'such',
    'very', 'too', 'also', 'just', 'only', 'now', 'then', 'than',
    'here', 'there', 'when', 'where', 'why', 'how', 'who', 'which', 'what'
}

def keywords(text: str, max_keywords: int = 50, min_length: int = 3) -> list:
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
        
        if len(keywords) >= max_keywords:
            break
    
    return keywords