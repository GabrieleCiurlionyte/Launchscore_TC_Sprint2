from dataclasses import asdict
from langchain.tools import tool

from rag.tools.googleTrends.googleTrends import GoogleTrendsClient


@tool
def google_trends(keyword: str, geo: str = "") -> dict:
    """Fetch Google Trends data for a keyword and optional country code.
    
    Key parameter describes keywords to get Google Trend data for.
    
    Country code is a two letter country abbreviation.
    For example United States is 'US'
    If country code is not provided it defaults to World
    More detail available for States/Provinces by specifying additional abbreviations
    For example: Alabama would be 'US-AL'
    For example: England would be 'GB-ENG'
    """
    google_trends_client = GoogleTrendsClient()
    result = google_trends_client.run(keyword=keyword, geo=geo)
    return asdict(result)
