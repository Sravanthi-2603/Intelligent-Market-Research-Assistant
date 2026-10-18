"""
IBM Granite AI Client - Connects to IBM WatsonX for text generation
using the ibm/granite-3-8b-instruct model
"""

import requests
import time
from backend.config import (
    IBM_API_KEY, IBM_PROJECT_ID, GRANITE_MODEL_ID,
    WATSONX_GENERATE_URL, WATSONX_TOKEN_URL
)

# ── IAM token cache (tokens live ~1 hour; refresh 5 min early) ──
_token_cache = {"token": None, "expires_at": 0}

def get_iam_token():
    """Return a cached IAM token, refreshing only when near-expiry."""
    now = time.time()
    if _token_cache["token"] and now < _token_cache["expires_at"]:
        return _token_cache["token"]

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
        "apikey": IBM_API_KEY
    }
    resp = requests.post(WATSONX_TOKEN_URL, headers=headers, data=data, timeout=30)
    resp.raise_for_status()
    payload = resp.json()
    _token_cache["token"] = payload["access_token"]
    # expiration field is epoch seconds; subtract 5 min buffer
    _token_cache["expires_at"] = payload.get("expiration", now + 3600) - 300
    return _token_cache["token"]


def granite_generate(prompt: str, max_tokens: int = 800, temperature: float = 0.7) -> str:
    """
    Send a prompt to IBM Granite 3 8B Instruct and return the generated text.
    """
    try:
        token = get_iam_token()
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        payload = {
            "model_id": GRANITE_MODEL_ID,
            "input": prompt,
            "parameters": {
                "decoding_method": "greedy",
                "max_new_tokens": max_tokens,
                "temperature": temperature,
                "repetition_penalty": 1.05
            },
            "project_id": IBM_PROJECT_ID
        }
        resp = requests.post(WATSONX_GENERATE_URL, headers=headers, json=payload, timeout=60)
        resp.raise_for_status()
        result = resp.json()
        generated = result.get("results", [{}])[0].get("generated_text", "")
        return generated.strip()
    except requests.exceptions.HTTPError as e:
        error_body = ""
        try:
            error_body = e.response.text
        except Exception:
            pass
        return f"[Granite API Error {e.response.status_code}]: {error_body}"
    except Exception as e:
        return f"[Error connecting to IBM Granite]: {str(e)}"


def analyze_market_query(query: str, context: str = "") -> dict:
    """
    Analyze a market research query using IBM Granite.
    Returns structured insights.
    """
    system_prompt = """You are an expert market research analyst powered by IBM Granite.
Your role is to provide clear, data-driven, and actionable market insights.
Always structure your response with:
1. Executive Summary (2-3 sentences)
2. Key Findings (bullet points)
3. Market Opportunities
4. Risks & Challenges
5. Recommendations

Be concise, professional, and evidence-based."""

    full_prompt = f"""{system_prompt}

Market Research Query: {query}

{f'Additional Context: {context}' if context else ''}

Provide a comprehensive market analysis:"""

    generated = granite_generate(full_prompt, max_tokens=1000)

    return {
        "query": query,
        "analysis": generated,
        "model": GRANITE_MODEL_ID,
        "status": "success" if not generated.startswith("[Error") else "error"
    }


def analyze_sentiment(text: str, entity: str = "market") -> dict:
    """
    Use IBM Granite to perform sentiment analysis on market text.
    """
    prompt = f"""Analyze the sentiment of the following market-related text about {entity}.
Classify the overall sentiment as: POSITIVE, NEGATIVE, or NEUTRAL.
Also provide:
- Confidence score (0-100)
- Key sentiment drivers (bullet list)
- Business impact assessment

Text to analyze:
\"\"\"{text}\"\"\"

Sentiment Analysis:"""

    generated = granite_generate(prompt, max_tokens=400)

    # Try to extract simple sentiment label
    sentiment_label = "NEUTRAL"
    if "POSITIVE" in generated.upper()[:100]:
        sentiment_label = "POSITIVE"
    elif "NEGATIVE" in generated.upper()[:100]:
        sentiment_label = "NEGATIVE"

    return {
        "entity": entity,
        "text_snippet": text[:200],
        "sentiment": sentiment_label,
        "analysis": generated,
        "model": GRANITE_MODEL_ID
    }


def generate_competitor_analysis(company: str, competitors: list) -> dict:
    """
    Generate a competitor analysis using IBM Granite.
    """
    competitors_str = ", ".join(competitors) if competitors else "major industry players"
    prompt = f"""As a strategic market analyst, provide a detailed competitive analysis for {company} 
against the following competitors: {competitors_str}.

Structure your response as:
1. Competitive Landscape Overview
2. {company}'s Strengths vs Competitors
3. {company}'s Weaknesses vs Competitors  
4. Competitive Threats
5. Strategic Opportunities
6. Market Position Score (1-10) for each competitor in the format: CompanyName: Score/10

Competitive Analysis:"""

    generated = granite_generate(prompt, max_tokens=900)

    return {
        "company": company,
        "competitors": competitors,
        "analysis": generated,
        "model": GRANITE_MODEL_ID
    }


def forecast_market_trend(industry: str, timeframe: str = "6 months") -> dict:
    """
    Use IBM Granite to forecast market trends for a given industry.
    """
    prompt = f"""As a predictive market analyst, forecast the market trends for the {industry} industry 
over the next {timeframe}.

Provide:
1. Trend Forecast Summary
2. Top 3 Growth Drivers (with estimated impact %)
3. Potential Disruptions
4. Demand Forecast Direction: INCREASING / DECREASING / STABLE
5. Key Metrics to Watch
6. Confidence Level (Low/Medium/High) with reasoning

Market Trend Forecast:"""

    generated = granite_generate(prompt, max_tokens=800)

    # Extract trend direction
    direction = "STABLE"
    if "INCREASING" in generated.upper():
        direction = "INCREASING"
    elif "DECREASING" in generated.upper():
        direction = "DECREASING"

    return {
        "industry": industry,
        "timeframe": timeframe,
        "forecast": generated,
        "trend_direction": direction,
        "model": GRANITE_MODEL_ID
    }


def generate_market_snapshot(topic: str, news_items: list) -> dict:
    """
    Synthesize news items into a concise market snapshot using IBM Granite.
    """
    news_text = "\n".join([
        f"- {item.get('title', '')} ({item.get('source', 'Unknown')})"
        for item in news_items[:10]
    ])

    prompt = f"""Synthesize the following recent news and developments about {topic} into a 
concise market snapshot for business decision-makers.

Recent News:
{news_text}

Market Snapshot (include: current state, momentum, key events, immediate outlook):"""

    generated = granite_generate(prompt, max_tokens=600)

    return {
        "topic": topic,
        "snapshot": generated,
        "news_count": len(news_items),
        "model": GRANITE_MODEL_ID
    }
