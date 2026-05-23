"""
D12 Filter Module
Synthesizes all 12 manipulation detection signals into a single
Manipulation Probability Score (0–100%) and trading recommendation.

The 12th dimension (D12) combines:
- 11 original FIASANOVA dimensions (resonance)
- Manipulation detection from 12 patterns
- Produces final trading signal: TRADE / AVOID / REDUCE
"""

import json
from datetime import datetime
from typing import Dict, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class D12Filter:
    """
    Synthesizes institutional data and manipulation patterns
    into a unified D12 Manipulation Score.
    """
    
    def __init__(self, manipulation_scores: Dict, resonance_11d: float = 0.50):
        """
        Args:
            manipulation_scores: Dict of 12 pattern detection scores
            resonance_11d: Original 11D FIASANOVA resonance (0-1)
        """
        self.manipulation_scores = manipulation_scores
        self.resonance_11d = resonance_11d
        self.manipulation_probability = 0.0
        self.recommendation = "NEUTRAL"
    
    def calculate_manipulation_probability(self) -> float:
        """
        Weighted average of all 12 manipulation detection scores.
        Returns: probability between 0 (no manipulation) and 1 (definite manipulation)
        """
        if not self.manipulation_scores:
            return 0.0
        
        # Weights for each pattern (derived from typical manipulation frequency)
        weights = {
            "pump_dump": 0.095,
            "bear_raid": 0.090,
            "spoofing": 0.085,
            "wash_trading": 0.105,
            "dark_pool_divergence": 0.120,
            "options_anomaly": 0.110,
            "institutional_coordination": 0.090,
            "liquidity_abuse": 0.080,
            "insider_accumulation": 0.075,
            "sentiment_inversion": 0.065,
            "regulatory_arbitrage": 0.055,
            "pboc_exploitation": 0.050
        }
        
        weighted_sum = 0.0
        for pattern, score in self.manipulation_scores.items():
            weight = weights.get(pattern, 0.08)
            weighted_sum += score * weight
        
        self.manipulation_probability = min(weighted_sum, 1.0)
        return self.manipulation_probability
    
    def generate_recommendation(self) -> str:
        """
        Generate trading recommendation based on:
        - Manipulation probability
        - 11D resonance
        - Combined D12 signal
        
        Returns: "TRADE", "AVOID", or "REDUCE"
        """
        manip_prob = self.manipulation_probability
        resonance = self.resonance_11d
        
        # Decision matrix
        if manip_prob < 0.30 and resonance > 0.65:
            # Low manipulation, strong resonance = BUY
            self.recommendation = "TRADE"
        elif manip_prob > 0.65 or (manip_prob > 0.50 and resonance < 0.50):
            # High manipulation or weak resonance = AVOID
            self.recommendation = "AVOID"
        elif 0.30 <= manip_prob <= 0.50 and 0.50 <= resonance <= 0.65:
            # Moderate signals = REDUCE position
            self.recommendation = "REDUCE"
        else:
            self.recommendation = "NEUTRAL"
        
        return self.recommendation
    
    def calculate_d12_score(self) -> float:
        """
        Final D12 score combines:
        - Manipulation probability (50% weight)
        - Inverted resonance distance from optimal (50% weight)
        
        Returns: D12 score 0-1 (0 = optimal, 1 = risky)
        """
        # Optimal resonance is around 0.75
        optimal_resonance = 0.75
        resonance_distance = abs(self.resonance_11d - optimal_resonance)
        resonance_risk = resonance_distance / optimal_resonance
        
        d12_score = (0.5 * self.manipulation_probability) + (0.5 * resonance_risk)
        return min(d12_score, 1.0)
    
    def get_actionable_signal(self) -> Dict:
        """Generate complete actionable trading signal."""
        manip_prob = self.calculate_manipulation_probability()
        recommendation = self.generate_recommendation()
        d12_score = self.calculate_d12_score()
        
        # Time to next clean signal (estimate)
        days_to_clean = self._estimate_days_to_clean_signal(manip_prob)
        
        return {
            "timestamp": datetime.now().isoformat(),
            "manipulation_probability": round(manip_prob, 3),
            "manipulation_percentage": int(manip_prob * 100),
            "resonance_11d": round(self.resonance_11d, 3),
            "d12_score": round(d12_score, 3),
            "recommendation": recommendation,
            "confidence": self._calculate_confidence(manip_prob),
            "estimated_days_to_clean_signal": days_to_clean,
            "risk_level": self._classify_risk_level(d12_score),
            "next_action": self._generate_next_action(recommendation),
            "details": {
                "manipulation_patterns_detected": len([s for s in self.manipulation_scores.values() if s > 0.50]),
                "high_risk_patterns": [p for p, s in self.manipulation_scores.items() if s > 0.50]
            }
        }
    
    @staticmethod
    def _estimate_days_to_clean_signal(manipulation_prob: float) -> int:
        """Estimate days until market returns to clean signal."""
        if manipulation_prob < 0.30:
            return 0
        elif manipulation_prob < 0.50:
            return 2
        elif manipulation_prob < 0.70:
            return 3
        else:
            return 5
    
    @staticmethod
    def _calculate_confidence(manipulation_prob: float) -> str:
        """Confidence in the signal."""
        if 0.30 < manipulation_prob < 0.70:
            return "MODERATE"
        elif manipulation_prob >= 0.70:
            return "HIGH"
        else:
            return "LOW"
    
    @staticmethod
    def _classify_risk_level(d12_score: float) -> str:
        """Classify overall risk level."""
        if d12_score < 0.33:
            return "LOW"
        elif d12_score < 0.66:
            return "MODERATE"
        else:
            return "HIGH"
    
    @staticmethod
    def _generate_next_action(recommendation: str) -> str:
        """Generate human-readable next action."""
        actions = {
            "TRADE": "Monitor entry conditions; execute on dips with confirmation",
            "AVOID": "Stay on sidelines; wait for cleaner signal before entry",
            "REDUCE": "Consider trimming position; raise stops to break-even",
            "NEUTRAL": "Monitor situation; no immediate action recommended"
        }
        return actions.get(recommendation, "Monitor market conditions")
    
    def format_output(self) -> str:
        """Format output for terminal display."""
        signal = self.get_actionable_signal()
        
        output = f"""
╔═══════════════════════════════════════════════════════════════════╗
║       FIASANOVA MARKET MANIPULATION DETECTOR (D12 MODULE)         ║
╚═══════════════════════════════════════════════════════════════════╝

📊 ANALYSIS RESULTS
─────────────────────────────────────────────────────────────────
  Manipulation Probability:  {signal['manipulation_percentage']}% ({signal['manipulation_probability']})
  Resonance (11D):           {signal['resonance_11d']}
  D12 Score:                 {signal['d12_score']} ({signal['risk_level']} Risk)
  Confidence:                {signal['confidence']}

🎯 TRADING SIGNAL
─────────────────────────────────────────────────────────────────
  → RECOMMENDATION: {signal['recommendation']}
  
  Next Action:  {signal['next_action']}
  
  Expected Clean Signal In:  ~{signal['estimated_days_to_clean_signal']} days

📌 PATTERN ANALYSIS
─────────────────────────────────────────────────────────────────
  Patterns Detected (>50% risk):  {signal['details']['manipulation_patterns_detected']}
  High-Risk Patterns:  {', '.join(signal['details']['high_risk_patterns']) if signal['details']['high_risk_patterns'] else 'None'}

⏰ Timestamp: {signal['timestamp']}
╔═══════════════════════════════════════════════════════════════════╗
"""
        return output


if __name__ == "__main__":
    # Demo with sample manipulation scores
    sample_scores = {
        "pump_dump": 0.65,
        "bear_raid": 0.15,
        "spoofing": 0.45,
        "wash_trading": 0.70,
        "dark_pool_divergence": 0.75,
        "options_anomaly": 0.80,
        "institutional_coordination": 0.50,
        "liquidity_abuse": 0.55,
        "insider_accumulation": 0.40,
        "sentiment_inversion": 0.25,
        "regulatory_arbitrage": 0.15,
        "pboc_exploitation": 0.40
    }
    
    filter_d12 = D12Filter(sample_scores, resonance_11d=0.45)
    print(filter_d12.format_output())
    print("\nJSON Output:")
    print(json.dumps(filter_d12.get_actionable_signal(), indent=2))
