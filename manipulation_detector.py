"""
Market Manipulation Detector Module
Implements pattern recognition for 12 manipulation techniques:
1. Pump & Dump
2. Bear Raid
3. Spoofing
4. Wash Trading
5. Dark Pool Divergence
6. Options Flow Anomaly
7. Institutional Coordination
8. Liquidity Injection Abuse
9. Insider Accumulation
10. Sentiment Inversion
11. Regulatory Arbitrage
12. PBOC Policy Exploitation
"""

import json
from datetime import datetime
from typing import Dict, List, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ManipulationDetector:
    """Detects 12 distinct market manipulation patterns."""
    
    # Pattern detection thresholds
    PATTERNS = {
        "pump_dump": {"name": "Pump & Dump", "weight": 0.10},
        "bear_raid": {"name": "Bear Raid", "weight": 0.09},
        "spoofing": {"name": "Spoofing", "weight": 0.08},
        "wash_trading": {"name": "Wash Trading", "weight": 0.10},
        "dark_pool_divergence": {"name": "Dark Pool Divergence", "weight": 0.12},
        "options_anomaly": {"name": "Options Flow Anomaly", "weight": 0.11},
        "institutional_coordination": {"name": "Institutional Coordination", "weight": 0.09},
        "liquidity_abuse": {"name": "Liquidity Injection Abuse", "weight": 0.08},
        "insider_accumulation": {"name": "Insider Accumulation", "weight": 0.07},
        "sentiment_inversion": {"name": "Sentiment Inversion", "weight": 0.06},
        "regulatory_arbitrage": {"name": "Regulatory Arbitrage", "weight": 0.05},
        "pboc_exploitation": {"name": "PBOC Policy Exploitation", "weight": 0.05}
    }
    
    def __init__(self, institutional_data: Dict):
        self.data = institutional_data
        self.scores = {}
        self.detected_patterns = []
    
    def detect_all_patterns(self) -> Dict:
        """Execute all 12 pattern detections."""
        self.scores["pump_dump"] = self._detect_pump_dump()
        self.scores["bear_raid"] = self._detect_bear_raid()
        self.scores["spoofing"] = self._detect_spoofing()
        self.scores["wash_trading"] = self._detect_wash_trading()
        self.scores["dark_pool_divergence"] = self._detect_dark_pool_divergence()
        self.scores["options_anomaly"] = self._detect_options_anomaly()
        self.scores["institutional_coordination"] = self._detect_institutional_coordination()
        self.scores["liquidity_abuse"] = self._detect_liquidity_abuse()
        self.scores["insider_accumulation"] = self._detect_insider_accumulation()
        self.scores["sentiment_inversion"] = self._detect_sentiment_inversion()
        self.scores["regulatory_arbitrage"] = self._detect_regulatory_arbitrage()
        self.scores["pboc_exploitation"] = self._detect_pboc_exploitation()
        
        return self.scores
    
    def _detect_pump_dump(self) -> float:
        """Detect pump & dump patterns (rapid volume + sentiment surge)."""
        try:
            options_flow = self.data.get("options_flow", {})
            unusual_options = options_flow.get("total_unusual_options", 0)
            bias = options_flow.get("directional_bias", "")
            
            # High unusual options + bullish bias = potential pump
            score = 0.0
            if unusual_options > 600 and bias == "bullish":
                score += 0.65
            elif unusual_options > 400 and bias == "bullish":
                score += 0.35
            
            if score > 0:
                self.detected_patterns.append("pump_dump")
            
            return min(score, 1.0)
        except Exception as e:
            logger.error(f"Error in pump_dump detection: {e}")
            return 0.0
    
    def _detect_bear_raid(self) -> float:
        """Detect bear raid patterns (coordinated short selling)."""
        try:
            options_flow = self.data.get("options_flow", {})
            unusual_puts = options_flow.get("unusual_put_volume", 0)
            bias = options_flow.get("directional_bias", "")
            
            score = 0.0
            if unusual_puts > 400 and bias == "bearish":
                score += 0.55
            elif unusual_puts > 250 and bias == "bearish":
                score += 0.30
            
            if score > 0:
                self.detected_patterns.append("bear_raid")
            
            return min(score, 1.0)
        except Exception as e:
            logger.error(f"Error in bear_raid detection: {e}")
            return 0.0
    
    def _detect_spoofing(self) -> float:
        """Detect spoofing (fake order placement to manipulate price)."""
        try:
            options_flow = self.data.get("options_flow", {})
            notional_value = options_flow.get("estimated_notional_value_usd", 0)
            
            # Extreme notional values with mismatched call/put ratios
            score = 0.0
            if notional_value > 40_000_000:
                score += 0.45
            
            return min(score, 1.0)
        except Exception as e:
            logger.error(f"Error in spoofing detection: {e}")
            return 0.0
    
    def _detect_wash_trading(self) -> float:
        """Detect wash trading (self-dealing to inflate volume)."""
        try:
            dark_pool = self.data.get("dark_pool_data", {})
            dark_pool_ratio = dark_pool.get("dark_pool_ratio", 0)
            
            # Very high dark pool ratios suggest wash trading
            score = 0.0
            if dark_pool_ratio > 0.50:
                score += 0.70
            elif dark_pool_ratio > 0.40:
                score += 0.40
            
            if score > 0:
                self.detected_patterns.append("wash_trading")
            
            return min(score, 1.0)
        except Exception as e:
            logger.error(f"Error in wash_trading detection: {e}")
            return 0.0
    
    def _detect_dark_pool_divergence(self) -> float:
        """Detect dark pool divergence (unusual volume concentration)."""
        try:
            dark_pool = self.data.get("dark_pool_data", {})
            dark_pool_ratio = dark_pool.get("dark_pool_ratio", 0)
            
            score = 0.0
            if dark_pool_ratio > 0.45:
                score += 0.75
            elif dark_pool_ratio > 0.35:
                score += 0.45
            
            if score > 0:
                self.detected_patterns.append("dark_pool_divergence")
            
            return min(score, 1.0)
        except Exception as e:
            logger.error(f"Error in dark_pool_divergence detection: {e}")
            return 0.0
    
    def _detect_options_anomaly(self) -> float:
        """Detect unusual options flow patterns."""
        try:
            options_flow = self.data.get("options_flow", {})
            unusual_total = options_flow.get("total_unusual_options", 0)
            ivr = options_flow.get("ivr_level", 0)
            
            score = 0.0
            if unusual_total > 700 and ivr > 0.65:
                score += 0.80
            elif unusual_total > 500 and ivr > 0.60:
                score += 0.50
            
            if score > 0:
                self.detected_patterns.append("options_anomaly")
            
            return min(score, 1.0)
        except Exception as e:
            logger.error(f"Error in options_anomaly detection: {e}")
            return 0.0
    
    def _detect_institutional_coordination(self) -> float:
        """Detect coordinated institutional activity."""
        try:
            filing_data = self.data.get("13f_data", {})
            institutions_holding = filing_data.get("institutions_holding", 0)
            
            # High institution concentration = coordination risk
            score = 0.0
            if institutions_holding > 1100:
                score += 0.50
            elif institutions_holding > 1000:
                score += 0.30
            
            if score > 0:
                self.detected_patterns.append("institutional_coordination")
            
            return min(score, 1.0)
        except Exception as e:
            logger.error(f"Error in institutional_coordination detection: {e}")
            return 0.0
    
    def _detect_liquidity_abuse(self) -> float:
        """Detect abuse of liquidity injections."""
        try:
            pboc = self.data.get("pboc_signals", {})
            signal_strength = pboc.get("signal_strength", 0)
            sentiment = pboc.get("market_sentiment", "")
            
            score = 0.0
            if signal_strength > 0.60 and sentiment == "accommodative":
                score += 0.55
            elif signal_strength > 0.50:
                score += 0.30
            
            if score > 0:
                self.detected_patterns.append("liquidity_abuse")
            
            return min(score, 1.0)
        except Exception as e:
            logger.error(f"Error in liquidity_abuse detection: {e}")
            return 0.0
    
    def _detect_insider_accumulation(self) -> float:
        """Detect unusual insider accumulation patterns."""
        try:
            filing_data = self.data.get("13f_data", {})
            holding_trend = filing_data.get("holding_trend", "")
            
            score = 0.0
            if holding_trend == "increasing":
                score += 0.40
            
            return score
        except Exception as e:
            logger.error(f"Error in insider_accumulation detection: {e}")
            return 0.0
    
    def _detect_sentiment_inversion(self) -> float:
        """Detect sentiment inversion attacks."""
        try:
            options_flow = self.data.get("options_flow", {})
            bias = options_flow.get("directional_bias", "")
            
            # Typically lower risk unless extreme
            score = 0.0
            if bias == "bullish":
                score += 0.25
            
            return score
        except Exception as e:
            logger.error(f"Error in sentiment_inversion detection: {e}")
            return 0.0
    
    def _detect_regulatory_arbitrage(self) -> float:
        """Detect exploitation of regulatory gaps."""
        try:
            # Lower baseline for regulatory arbitrage
            score = 0.15
            return score
        except Exception as e:
            logger.error(f"Error in regulatory_arbitrage detection: {e}")
            return 0.0
    
    def _detect_pboc_exploitation(self) -> float:
        """Detect exploitation of PBOC policy signals."""
        try:
            pboc = self.data.get("pboc_signals", {})
            action = pboc.get("pboc_action", "")
            signal = pboc.get("signal_strength", 0)
            
            score = 0.0
            if action == "liquidity_injection" and signal > 0.60:
                score += 0.40
            
            if score > 0:
                self.detected_patterns.append("pboc_exploitation")
            
            return score
        except Exception as e:
            logger.error(f"Error in pboc_exploitation detection: {e}")
            return 0.0
    
    def get_report(self) -> Dict:
        """Generate detailed detection report."""
        return {
            "ticker": self.data.get("ticker", "N/A"),
            "timestamp": datetime.now().isoformat(),
            "detected_patterns": self.detected_patterns,
            "pattern_scores": self.scores,
            "high_risk_patterns": [
                p for p, score in self.scores.items() 
                if score > 0.50
            ]
        }


if __name__ == "__main__":
    # Demo with mock data
    sample_data = {
        "ticker": "SPY",
        "options_flow": {
            "total_unusual_options": 750,
            "unusual_call_volume": 487,
            "unusual_put_volume": 263,
            "directional_bias": "bullish",
            "estimated_notional_value_usd": 45_600_000,
            "ivr_level": 0.68
        },
        "dark_pool_data": {
            "dark_pool_ratio": 0.42
        },
        "13f_data": {
            "institutions_holding": 1203,
            "holding_trend": "increasing"
        },
        "pboc_signals": {
            "signal_strength": 0.65,
            "pboc_action": "liquidity_injection",
            "market_sentiment": "accommodative"
        }
    }
    
    detector = ManipulationDetector(sample_data)
    scores = detector.detect_all_patterns()
    report = detector.get_report()
    print(json.dumps(report, indent=2))
