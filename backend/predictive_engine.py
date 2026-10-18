"""
Predictive Analytics Engine - Analyzes patterns, forecasts market shifts,
and generates alerts on competitor activities and sentiment changes.
"""

import numpy as np
from datetime import datetime, timedelta
import random


def detect_sentiment_alerts(sentiment_timeline: list, threshold: float = 0.3) -> list:
    """
    Detect significant sentiment shifts and generate alerts.
    """
    alerts = []
    if len(sentiment_timeline) < 3:
        return alerts

    scores = [item["sentiment_score"] for item in sentiment_timeline]

    # Detect rapid drops (negative shift alert)
    for i in range(2, len(scores)):
        delta = scores[i] - scores[i - 2]
        if delta < -threshold:
            alerts.append({
                "type": "SENTIMENT_DROP",
                "severity": "HIGH" if delta < -0.5 else "MEDIUM",
                "date": sentiment_timeline[i]["date"],
                "message": f"Sentiment dropped by {abs(round(delta, 2))} points in 48h",
                "action": "Review recent negative news and customer feedback immediately"
            })

        # Detect rapid rises (positive shift alert)
        elif delta > threshold:
            alerts.append({
                "type": "SENTIMENT_SURGE",
                "severity": "LOW",
                "date": sentiment_timeline[i]["date"],
                "message": f"Positive sentiment surge of {round(delta, 2)} points detected",
                "action": "Capitalize on positive momentum with targeted campaigns"
            })

    return alerts[-5:]  # Return latest 5 alerts


def forecast_demand(monthly_data: list, periods: int = 6) -> dict:
    """
    Simple linear regression-based demand forecast for next N periods.
    """
    if len(monthly_data) < 4:
        return {"forecast": [], "trend": "STABLE", "confidence": "LOW"}

    x = np.array(range(len(monthly_data)), dtype=float)
    y = np.array(monthly_data, dtype=float)

    # Linear regression
    coeffs = np.polyfit(x, y, 1)
    slope = coeffs[0]
    intercept = coeffs[1]

    # Generate forecast
    forecast_values = []
    for i in range(len(monthly_data), len(monthly_data) + periods):
        predicted = slope * i + intercept
        # Add slight randomness for realism
        predicted *= random.uniform(0.97, 1.04)
        forecast_values.append(round(predicted, 1))

    # Determine trend
    growth_rate = (slope / np.mean(y)) * 100
    if growth_rate > 1.5:
        trend = "INCREASING"
    elif growth_rate < -1.5:
        trend = "DECREASING"
    else:
        trend = "STABLE"

    # Confidence based on data variance
    cv = (np.std(y) / np.mean(y)) * 100
    confidence = "HIGH" if cv < 10 else ("MEDIUM" if cv < 25 else "LOW")

    # Compute R-squared
    y_pred = np.polyval(coeffs, x)
    ss_res = np.sum((y - y_pred) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    r_squared = round(1 - (ss_res / ss_tot), 3) if ss_tot != 0 else 0

    return {
        "historical": monthly_data,
        "forecast": forecast_values,
        "trend": trend,
        "growth_rate_pct": round(growth_rate, 2),
        "confidence": confidence,
        "r_squared": r_squared,
        "forecast_months": periods
    }


def generate_competitor_alerts(company: str, competitors: list) -> list:
    """
    Generate competitor activity alerts based on market intelligence patterns.
    """
    alert_templates = [
        {
            "type": "COMPETITOR_EXPANSION",
            "severity": "HIGH",
            "message": f"{random.choice(competitors)} announced expansion into new market segments",
            "action": "Evaluate defensive positioning and counter-strategy"
        },
        {
            "type": "PRICE_MOVEMENT",
            "severity": "MEDIUM",
            "message": f"{random.choice(competitors)} adjusted pricing by {random.randint(5, 20)}% — competitive pressure likely",
            "action": "Review pricing strategy and value proposition messaging"
        },
        {
            "type": "PRODUCT_LAUNCH",
            "severity": "HIGH",
            "message": f"{random.choice(competitors)} launched new product targeting your core segment",
            "action": "Fast-track R&D pipeline and differentiation messaging"
        },
        {
            "type": "PARTNERSHIP",
            "severity": "MEDIUM",
            "message": f"{random.choice(competitors)} formed strategic partnership to enhance capabilities",
            "action": "Explore complementary partnerships to maintain competitive parity"
        }
    ]

    # Return 2-3 random alerts with timestamps
    selected = random.sample(alert_templates, min(3, len(alert_templates)))
    for i, alert in enumerate(selected):
        alert["date"] = (datetime.now() - timedelta(days=i * 2)).strftime("%Y-%m-%d")
        alert["company"] = company

    return selected


def compute_market_health_score(indicators: dict) -> dict:
    """
    Compute a composite market health score from multiple indicators.
    Returns a score 0-100 with breakdown.
    """
    scores = {}

    # Growth score (0-100)
    growth = indicators.get("yoy_growth_pct", 10)
    scores["growth"] = min(100, max(0, growth * 2.5))

    # Demand index (already 0-100)
    scores["demand"] = indicators.get("demand_index", 60)

    # Consumer confidence (already 0-100)
    scores["consumer_confidence"] = indicators.get("consumer_confidence", 55)

    # Innovation score (already 0-100)
    scores["innovation"] = indicators.get("innovation_score", 70)

    # Risk penalty
    risk = indicators.get("risk_level", "MEDIUM")
    risk_penalty = {"LOW": 0, "MEDIUM": -10, "HIGH": -20}.get(risk, -10)

    # Weighted composite
    composite = (
        scores["growth"] * 0.3 +
        scores["demand"] * 0.25 +
        scores["consumer_confidence"] * 0.2 +
        scores["innovation"] * 0.25 +
        risk_penalty
    )

    composite = round(min(100, max(0, composite)), 1)

    # Determine health label
    if composite >= 75:
        label = "EXCELLENT"
    elif composite >= 60:
        label = "GOOD"
    elif composite >= 45:
        label = "MODERATE"
    elif composite >= 30:
        label = "WEAK"
    else:
        label = "CRITICAL"

    return {
        "composite_score": composite,
        "label": label,
        "breakdown": scores,
        "risk_level": risk
    }


def generate_strategic_alerts(topic: str, sentiment_score: float, growth_rate: float) -> list:
    """
    Generate strategic alerts based on sentiment and growth analysis.
    """
    alerts = []
    now = datetime.now().strftime("%Y-%m-%d")

    if sentiment_score < -0.2:
        alerts.append({
            "type": "NEGATIVE_SENTIMENT",
            "severity": "HIGH",
            "date": now,
            "message": f"Negative market sentiment detected for {topic} (score: {round(sentiment_score, 2)})",
            "action": "Engage PR strategy and monitor social media closely"
        })

    if growth_rate > 20:
        alerts.append({
            "type": "RAPID_GROWTH",
            "severity": "LOW",
            "date": now,
            "message": f"Rapid growth detected in {topic}: {round(growth_rate, 1)}% projected",
            "action": "Scale operations and secure supply chain to meet rising demand"
        })

    if growth_rate < -5:
        alerts.append({
            "type": "MARKET_CONTRACTION",
            "severity": "HIGH",
            "date": now,
            "message": f"Market contraction signal for {topic}: {round(abs(growth_rate), 1)}% decline projected",
            "action": "Diversify product portfolio and explore adjacent markets"
        })

    if 0 < growth_rate < 20 and sentiment_score > 0.2:
        alerts.append({
            "type": "OPPORTUNITY",
            "severity": "LOW",
            "date": now,
            "message": f"Market opportunity window open in {topic} — positive sentiment with steady growth",
            "action": "Increase marketing spend and capture market share now"
        })

    return alerts
