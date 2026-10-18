"""
Flask API Routes - All backend endpoints for the Intelligent Market Research Assistant
"""

from flask import Blueprint, request, jsonify
from concurrent.futures import ThreadPoolExecutor, as_completed

from backend.granite_client import (
    analyze_market_query,
    analyze_sentiment,
    generate_competitor_analysis,
    forecast_market_trend,
    generate_market_snapshot
)
from backend.data_agent import (
    fetch_rss_news,
    search_news_by_keyword,
    get_market_indicators,
    get_sentiment_timeline,
    compute_sentiment_score
)
from backend.predictive_engine import (
    detect_sentiment_alerts,
    forecast_demand,
    generate_competitor_alerts,
    compute_market_health_score,
    generate_strategic_alerts
)

api = Blueprint("api", __name__, url_prefix="/api")


@api.route("/health", methods=["GET"])
def health_check():
    """API health check endpoint."""
    return jsonify({
        "status": "healthy",
        "service": "Intelligent Market Research Assistant",
        "model": "ibm/granite-3-8b-instruct",
        "version": "1.0.0"
    })


@api.route("/analyze", methods=["POST"])
def analyze_market():
    """
    Main analysis endpoint. Accepts a market research query and returns
    comprehensive AI-powered insights from IBM Granite.
    """
    data = request.get_json()
    if not data or not data.get("query"):
        return jsonify({"error": "Query is required"}), 400

    query = data.get("query", "").strip()
    context = data.get("context", "")

    result = analyze_market_query(query, context)
    return jsonify(result)


@api.route("/news", methods=["GET"])
def get_news():
    """
    Fetch recent market news for a topic/category.
    Query params: topic (str), max_items (int)
    """
    topic = request.args.get("topic", "technology")
    max_items = int(request.args.get("max_items", 10))
    keyword = request.args.get("keyword", "")

    if keyword:
        news = search_news_by_keyword(keyword, max_items)
    else:
        news = fetch_rss_news(topic, max_items)

    return jsonify({
        "topic": topic,
        "count": len(news),
        "news": news
    })


@api.route("/sentiment", methods=["POST"])
def sentiment_analysis():
    """
    Perform sentiment analysis on provided text using IBM Granite.
    """
    data = request.get_json()
    if not data or not data.get("text"):
        return jsonify({"error": "Text is required"}), 400

    text = data.get("text", "").strip()
    entity = data.get("entity", "market")

    # TextBlob quick score
    quick_score = compute_sentiment_score(text)

    # IBM Granite deep analysis
    granite_result = analyze_sentiment(text, entity)

    return jsonify({
        "entity": entity,
        "quick_sentiment": quick_score,
        "granite_analysis": granite_result
    })


@api.route("/competitors", methods=["POST"])
def competitor_analysis():
    """
    Generate competitor analysis for a company vs its rivals.
    """
    data = request.get_json()
    if not data or not data.get("company"):
        return jsonify({"error": "Company name is required"}), 400

    company = data.get("company", "").strip()
    competitors = data.get("competitors", [])

    # IBM Granite analysis
    analysis = generate_competitor_analysis(company, competitors)

    # Generate competitor alerts
    alerts = generate_competitor_alerts(company, competitors) if competitors else []

    analysis["alerts"] = alerts
    return jsonify(analysis)


@api.route("/forecast", methods=["GET"])
def market_forecast():
    """
    Get demand forecast and market trend analysis for an industry.
    Query params: industry (str), timeframe (str)
    """
    industry = request.args.get("industry", "Technology")
    timeframe = request.args.get("timeframe", "6 months")

    # Get market indicators
    indicators = get_market_indicators(industry)

    # Statistical demand forecast
    demand_forecast = forecast_demand(indicators["monthly_revenue_trend"])

    # IBM Granite narrative forecast
    granite_forecast = forecast_market_trend(industry, timeframe)

    # Market health score
    health = compute_market_health_score(indicators)

    # Strategic alerts
    avg_sentiment = 0.2  # Default positive bias for growth sectors
    strategic_alerts = generate_strategic_alerts(
        industry, avg_sentiment, demand_forecast["growth_rate_pct"]
    )

    return jsonify({
        "industry": industry,
        "timeframe": timeframe,
        "indicators": indicators,
        "demand_forecast": demand_forecast,
        "granite_forecast": granite_forecast,
        "market_health": health,
        "strategic_alerts": strategic_alerts
    })


@api.route("/dashboard", methods=["GET"])
def dashboard_data():
    """
    Comprehensive dashboard data endpoint.
    Fetches news, indicators, and sentiment timeline concurrently,
    then runs the Granite snapshot in a separate thread so structural
    data is ready as soon as the fastest I/O finishes.
    """
    topic = request.args.get("topic", "AI")

    # ── Fan-out: run independent I/O tasks in parallel ──
    with ThreadPoolExecutor(max_workers=3) as pool:
        f_news      = pool.submit(fetch_rss_news, topic, 6)
        f_indicators = pool.submit(get_market_indicators, topic)
        f_timeline  = pool.submit(get_sentiment_timeline, topic, 30)

        news             = f_news.result()
        indicators       = f_indicators.result()
        sentiment_timeline = f_timeline.result()

    # These are all CPU-only — run after I/O resolves
    demand_forecast   = forecast_demand(indicators["monthly_revenue_trend"])
    health            = compute_market_health_score(indicators)
    sentiment_alerts  = detect_sentiment_alerts(sentiment_timeline)
    avg_sentiment     = sum(d["sentiment_score"] for d in sentiment_timeline[-7:]) / 7
    strategic_alerts  = generate_strategic_alerts(topic, avg_sentiment, demand_forecast["growth_rate_pct"])

    # ── Granite snapshot runs concurrently with the JSON assembly ──
    with ThreadPoolExecutor(max_workers=1) as pool:
        f_snapshot = pool.submit(generate_market_snapshot, topic, news)

        all_alerts = sentiment_alerts + strategic_alerts
        all_alerts.sort(key=lambda x: {"HIGH": 0, "MEDIUM": 1, "LOW": 2}.get(x.get("severity", "LOW"), 1))

        snapshot = f_snapshot.result()  # wait only at the last moment

    return jsonify({
        "topic": topic,
        "market_snapshot": snapshot,
        "indicators": indicators,
        "market_health": health,
        "sentiment_timeline": sentiment_timeline,
        "demand_forecast": demand_forecast,
        "recent_news": news,
        "alerts": all_alerts[:8]
    })


@api.route("/multimodal", methods=["POST"])
def multimodal_input():
    """
    Handle multimodal inputs: text queries, uploaded files (CSV, PDF text).
    Extracts content and routes to appropriate analysis.
    """
    query = request.form.get("query", "")
    analysis_type = request.form.get("type", "general")
    context = ""

    # Handle file upload
    if "file" in request.files:
        file = request.files["file"]
        if file.filename:
            try:
                content = file.read().decode("utf-8", errors="ignore")
                # Use first 2000 chars as context
                context = content[:2000]
            except Exception:
                pass

    if not query and not context:
        return jsonify({"error": "Query or file content is required"}), 400

    if not query:
        query = f"Analyze this market data and provide key insights: {context[:200]}"

    # Route based on analysis type
    if analysis_type == "sentiment":
        text_to_analyze = context if context else query
        quick = compute_sentiment_score(text_to_analyze)
        granite = analyze_sentiment(text_to_analyze, "market")
        return jsonify({
            "type": "sentiment",
            "quick_sentiment": quick,
            "granite_analysis": granite,
            "has_file": bool(context)
        })
    else:
        result = analyze_market_query(query, context)
        return jsonify({
            "type": "analysis",
            "result": result,
            "has_file": bool(context)
        })


@api.route("/snapshot", methods=["POST"])
def market_snapshot():
    """
    Generate a quick market snapshot for a topic with latest news synthesis.
    """
    data = request.get_json()
    topic = data.get("topic", "Technology") if data else "Technology"

    news = fetch_rss_news(topic, max_items=8)
    snapshot = generate_market_snapshot(topic, news)

    return jsonify({
        "topic": topic,
        "snapshot": snapshot,
        "news_count": len(news)
    })
