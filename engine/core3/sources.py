from dataclasses import dataclass


@dataclass
class SourceConfig:
    name: str
    search_url_template: str
    result_selector: str
    snippet_selector: str
    tier: int


SOURCES: list[SourceConfig] = [
    SourceConfig(
        name="Wikipedia",
        search_url_template="https://en.wikipedia.org/w/index.php?search={query}&title=Special%3ASearch",
        result_selector="li.mw-search-result",
        snippet_selector=".searchresult",
        tier=1,
    ),
    SourceConfig(
        name="Google",
        search_url_template="https://www.google.com/search?q={query}",
        result_selector="div.g",
        snippet_selector="div.VwiC3b, span.st",
        tier=3,
    ),
    SourceConfig(
        name="Snopes",
        search_url_template="https://www.snopes.com/?s={query}",
        result_selector="article.media-wrapper, div.article_wrapper",
        snippet_selector="p, .article_text",
        tier=2,
    ),
    SourceConfig(
        name="Reuters Fact Check",
        search_url_template="https://www.reuters.com/site-search/?query={query}&section=fact-check",
        result_selector="li.search-results__item, div[class*='MediaStory']",
        snippet_selector="h3, span[class*='Text']",
        tier=1,
    ),
    SourceConfig(
        name="AP Fact Check",
        search_url_template="https://apnews.com/search?q={query}%20fact%20check",
        result_selector="div.SearchResultsModule-results div.PageList-items-item",
        snippet_selector="h2, .PagePromo-description",
        tier=1,
    ),
    SourceConfig(
        name="FactCheck.org",
        search_url_template="https://www.factcheck.org/?s={query}",
        result_selector="article, div.entry-content",
        snippet_selector="h2 a, .entry-summary p",
        tier=2,
    ),
    SourceConfig(
        name="PolitiFact",
        search_url_template="https://www.politifact.com/search/?q={query}",
        result_selector="article.o-listease__item, div.m-result",
        snippet_selector="div.m-result__content, .o-listease__body",
        tier=2,
    ),
    SourceConfig(
        name="ScienceDirect",
        search_url_template="https://www.sciencedirect.com/search?qs={query}",
        result_selector="div.result-item-content",
        snippet_selector="span.result-list-title-link, div.result-item-content p",
        tier=3,
    ),
    SourceConfig(
        name="WHO",
        search_url_template="https://search.who.int/search?q={query}",
        result_selector="div.search-results div.result, div.list-view--item",
        snippet_selector="a.result-title, p.result-text, .list-view--item-title",
        tier=1,
    ),
    SourceConfig(
        name="CDC",
        search_url_template="https://search.cdc.gov/search/?query={query}",
        result_selector="div.searchResults li, ul.list-group li",
        snippet_selector="a, .searchResultContent",
        tier=1,
    ),
]

HEALTH_KEYWORDS = [
    "vaccine", "covid", "disease", "health", "medical", "drug", "treatment",
    "symptom", "diagnosis", "virus", "bacteria", "pandemic", "epidemic",
    "cancer", "diabetes", "heart", "blood", "surgery", "hospital", "doctor",
    "pharmaceutical", "clinical", "therapy", "infection", "immunity",
    "nutrition", "diet", "obesity", "mental health", "depression", "anxiety",
]

POLITICAL_KEYWORDS = [
    "president", "congress", "senate", "parliament", "election", "vote",
    "democrat", "republican", "liberal", "conservative", "policy", "law",
    "legislation", "campaign", "political", "government", "minister",
    "party", "biden", "trump", "modi", "immigration", "tax", "budget",
]

SCIENCE_KEYWORDS = [
    "study", "research", "experiment", "scientific", "peer-reviewed",
    "theory", "hypothesis", "data", "evidence", "journal", "published",
    "university", "professor", "climate", "physics", "chemistry", "biology",
    "evolution", "quantum", "space", "nasa", "genome", "dna", "rna",
]


def classify_claim(text: str) -> list[str]:
    text_lower = text.lower()
    categories = []

    health_hits = sum(1 for kw in HEALTH_KEYWORDS if kw in text_lower)
    political_hits = sum(1 for kw in POLITICAL_KEYWORDS if kw in text_lower)
    science_hits = sum(1 for kw in SCIENCE_KEYWORDS if kw in text_lower)

    if health_hits >= 2:
        categories.append("health")
    if political_hits >= 2:
        categories.append("political")
    if science_hits >= 2:
        categories.append("science")

    if not categories:
        categories.append("general")

    return categories


def select_sources(text: str) -> list[SourceConfig]:
    categories = classify_claim(text)
    always_include = {"Wikipedia", "Google"}
    category_sources = {
        "health": {"WHO", "CDC", "ScienceDirect", "Reuters Fact Check"},
        "political": {"PolitiFact", "FactCheck.org", "Snopes", "AP Fact Check"},
        "science": {"ScienceDirect", "WHO", "Reuters Fact Check"},
        "general": {"Snopes", "Reuters Fact Check", "AP Fact Check", "FactCheck.org"},
    }

    selected_names = set(always_include)
    for category in categories:
        selected_names.update(category_sources.get(category, set()))

    return [s for s in SOURCES if s.name in selected_names]
