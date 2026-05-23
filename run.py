#!/usr/bin/env python3
"""
FIASANOVA Market Manipulation Detector (D12 Module)
Main entry point for running the complete detection pipeline.

Usage:
    python run.py [TICKER] [--resonance SCORE] [--output-format FORMAT]

Examples:
    python run.py SPY
    python run.py AAPL --resonance 0.65
    python run.py SPY --output-format json > output.json
"""

import sys
import json
import argparse
from datetime import datetime
from pathlib import Path

# Import our modules
from institutional_data_collector import InstitutionalDataCollector
from manipulation_detector import ManipulationDetector
from d12_filter import D12Filter


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="FIASANOVA Market Manipulation Detector (D12 Module)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run.py SPY
  python run.py AAPL --resonance 0.65
  python run.py SPY --output-format json > output.json
  python run.py SPY --save-csv results.csv
        """
    )
    
    parser.add_argument(
        "ticker",
        nargs="?",
        default="SPY",
        help="Stock ticker to analyze (default: SPY)"
    )
    
    parser.add_argument(
        "--resonance",
        type=float,
        default=0.50,
        help="11D FIASANOVA resonance score (0-1, default: 0.50)"
    )
    
    parser.add_argument(
        "--output-format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)"
    )
    
    parser.add_argument(
        "--save-csv",
        type=str,
        help="Save results to CSV file"
    )
    
    parser.add_argument(
        "--save-json",
        type=str,
        help="Save results to JSON file"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    
    return parser.parse_args()


def run_detection_pipeline(ticker: str, resonance_11d: float) -> dict:
    """
    Execute the complete D12 detection pipeline:
    1. Collect institutional data
    2. Detect manipulation patterns
    3. Filter and generate final signal
    
    Args:
        ticker: Stock ticker symbol
        resonance_11d: 11D resonance score
    
    Returns:
        dict: Complete analysis result
    """
    
    print(f"\n{'='*70}")
    print(f"FIASANOVA D12 MARKET MANIPULATION DETECTOR")
    print(f"{'='*70}\n")
    
    # Step 1: Collect institutional data
    print(f"[1/3] Collecting institutional data for {ticker}...")
    collector = InstitutionalDataCollector(ticker)
    institutional_data = collector.aggregate_institutional_data()
    print(f"      ✓ Data collected (13F, dark pool, options, PBOC)")
    
    # Step 2: Detect manipulation patterns
    print(f"\n[2/3] Analyzing 12 manipulation patterns...")
    detector = ManipulationDetector(institutional_data)
    manipulation_scores = detector.detect_all_patterns()
    print(f"      ✓ {len([s for s in manipulation_scores.values() if s > 0.50])} high-risk patterns detected")
    
    # Step 3: Generate D12 signal
    print(f"\n[3/3] Generating D12 trading signal...")
    d12_filter = D12Filter(manipulation_scores, resonance_11d=resonance_11d)
    signal = d12_filter.get_actionable_signal()
    signal["ticker"] = ticker
    signal["institutional_data_summary"] = {
        "dark_pool_ratio": institutional_data["dark_pool_data"]["dark_pool_ratio"],
        "institutions_holding": institutional_data["13f_data"]["institutions_holding"],
        "unusual_options": institutional_data["options_flow"]["total_unusual_options"],
        "pboc_signal_strength": institutional_data["pboc_signals"]["signal_strength"]
    }
    print(f"      ✓ Signal generated: {signal['recommendation']}")
    
    return {
        "ticker": ticker,
        "analysis_timestamp": datetime.now().isoformat(),
        "institutional_data": institutional_data,
        "manipulation_scores": manipulation_scores,
        "d12_signal": signal,
        "formatted_output": d12_filter.format_output()
    }


def save_to_csv(result: dict, filepath: str):
    """Save results to CSV format."""
    try:
        import csv
        
        signal = result["d12_signal"]
        
        with open(filepath, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=[
                "timestamp",
                "ticker",
                "manipulation_probability",
                "manipulation_percentage",
                "resonance_11d",
                "d12_score",
                "recommendation",
                "risk_level",
                "dark_pool_ratio",
                "institutions_holding",
                "unusual_options",
                "pboc_signal_strength"
            ])
            
            writer.writeheader()
            writer.writerow({
                "timestamp": signal["timestamp"],
                "ticker": result["ticker"],
                "manipulation_probability": signal["manipulation_probability"],
                "manipulation_percentage": signal["manipulation_percentage"],
                "resonance_11d": signal["resonance_11d"],
                "d12_score": signal["d12_score"],
                "recommendation": signal["recommendation"],
                "risk_level": signal["risk_level"],
                "dark_pool_ratio": signal["institutional_data_summary"]["dark_pool_ratio"],
                "institutions_holding": signal["institutional_data_summary"]["institutions_holding"],
                "unusual_options": signal["institutional_data_summary"]["unusual_options"],
                "pboc_signal_strength": signal["institutional_data_summary"]["pboc_signal_strength"]
            })
        
        print(f"✓ CSV saved to: {filepath}")
    except Exception as e:
        print(f"✗ Error saving CSV: {e}")


def save_to_json(result: dict, filepath: str):
    """Save results to JSON format."""
    try:
        output = {
            "ticker": result["ticker"],
            "analysis_timestamp": result["analysis_timestamp"],
            "d12_signal": result["d12_signal"],
            "manipulation_scores": result["manipulation_scores"]
        }
        
        with open(filepath, "w") as f:
            json.dump(output, f, indent=2)
        
        print(f"✓ JSON saved to: {filepath}")
    except Exception as e:
        print(f"✗ Error saving JSON: {e}")


def main():
    """Main execution function."""
    args = parse_arguments()
    
    # Validate resonance score
    if not 0 <= args.resonance <= 1:
        print(f"Error: Resonance must be between 0 and 1. Got: {args.resonance}")
        sys.exit(1)
    
    try:
        # Run the detection pipeline
        result = run_detection_pipeline(args.ticker, args.resonance)
        
        # Output results
        if args.output_format == "json":
            print(json.dumps(result["d12_signal"], indent=2))
        else:
            print(result["formatted_output"])
        
        # Save to files if requested
        if args.save_csv:
            save_to_csv(result, args.save_csv)
        
        if args.save_json:
            save_to_json(result, args.save_json)
        
        # Print summary
        print(f"\n{'='*70}")
        print(f"Analysis complete for {args.ticker}")
        print(f"Recommendation: {result['d12_signal']['recommendation']}")
        print(f"Risk Level: {result['d12_signal']['risk_level']}")
        print(f"{'='*70}\n")
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\n⚠ Analysis interrupted by user")
        return 130
    except Exception as e:
        print(f"\n✗ Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
