#!/usr/bin/env python3
"""
EnMS Chatbot Query Log Analyzer
Analyzes query logs to identify patterns, failures, and improvement opportunities
"""

import json
import sys
from collections import defaultdict, Counter
from datetime import datetime, timedelta
from pathlib import Path

def analyze_logs(log_file: str, days: int = 7):
    """Analyze query logs from the last N days"""
    
    if not Path(log_file).exists():
        print(f"❌ Log file not found: {log_file}")
        print(f"ℹ️  Query logging is enabled but no queries have been logged yet.")
        print(f"ℹ️  Logs will appear at: {log_file}")
        return
    
    # Parse logs
    queries = []
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    
    with open(log_file) as f:
        for line in f:
            try:
                log_entry = json.loads(line.strip())
                log_time = datetime.fromisoformat(log_entry['timestamp'].replace('Z', '+00:00'))
                
                if log_time >= cutoff_date:
                    queries.append(log_entry)
            except (json.JSONDecodeError, KeyError) as e:
                continue
    
    if not queries:
        print(f"❌ No queries found in the last {days} days")
        return
    
    print("=" * 70)
    print(f"EnMS Chatbot Query Log Analysis")
    print(f"Period: Last {days} days")
    print(f"Total Queries: {len(queries)}")
    print("=" * 70)
    print()
    
    # Analysis 1: Status Distribution
    print("## 1. Query Status Distribution")
    print()
    status_counts = Counter(q.get('status', 'unknown') for q in queries)
    for status, count in status_counts.most_common():
        pct = (count / len(queries)) * 100
        print(f"  {status:20s} {count:5d} ({pct:5.1f}%)")
    print()
    
    # Analysis 2: Top Categories
    print("## 2. Top 20 Categories (Most Queried)")
    print()
    category_counts = Counter(q.get('matched_category', 'none') for q in queries if q.get('status') == 'success')
    for category, count in category_counts.most_common(20):
        print(f"  {category:40s} {count:5d}")
    print()
    
    # Analysis 3: Failed Queries (No Match)
    print("## 3. Failed Queries (No Match / Fallback)")
    print()
    failed = [q for q in queries if q.get('status') in ['fallback', 'no_match']]
    if failed:
        print(f"Total Failed: {len(failed)} ({len(failed)/len(queries)*100:.1f}%)")
        print()
        
        # Unique failed queries
        unique_failed = {}
        for q in failed:
            query_text = q.get('query', 'unknown')
            if query_text not in unique_failed:
                unique_failed[query_text] = 0
            unique_failed[query_text] += 1
        
        print("Top 20 Failed Queries:")
        for query, count in sorted(unique_failed.items(), key=lambda x: x[1], reverse=True)[:20]:
            print(f"  [{count:3d}x] \"{query}\"")
    else:
        print("✅ No failed queries!")
    print()
    
    # Analysis 4: Intent Distribution
    print("## 4. Intent Distribution")
    print()
    intent_counts = Counter(q.get('intent', 'unknown') for q in queries)
    for intent, count in intent_counts.most_common():
        pct = (count / len(queries)) * 100
        print(f"  {intent:20s} {count:5d} ({pct:5.1f}%)")
    print()
    
    # Analysis 5: Response Time (if available)
    print("## 5. Performance Metrics")
    print()
    print(f"  Total Queries: {len(queries)}")
    print(f"  Success Rate: {len([q for q in queries if q.get('status') == 'success']) / len(queries) * 100:.1f}%")
    print(f"  Unique Users: {len(set(q.get('sender_id', 'unknown') for q in queries))}")
    print()
    
    # Analysis 6: Recommendations
    print("=" * 70)
    print("## 6. Recommendations")
    print("=" * 70)
    print()
    
    if failed:
        print(f"1. HIGH PRIORITY: Review {len(failed)} failed queries")
        print(f"   - Add Q&As for common failed queries")
        print(f"   - Add keywords to improve routing")
        print()
    
    # Check for low-usage categories
    all_categories = set()
    with open('/home/ubuntu/humanergy/chatbot/rasa/qa_data.json') as f:
        all_categories = set(json.load(f).keys())
    
    used_categories = set(q.get('matched_category') for q in queries if q.get('status') == 'success')
    unused = all_categories - used_categories
    
    if unused:
        print(f"2. MEDIUM PRIORITY: {len(unused)} categories not used in last {days} days")
        print(f"   - Consider reviewing: {', '.join(sorted(list(unused))[:5])}")
        print()
    
    # Check dominant categories
    if category_counts:
        top_cat, top_count = category_counts.most_common(1)[0]
        if top_count / len(queries) > 0.3:
            print(f"3. INFO: Category '{top_cat}' dominates ({top_count/len(queries)*100:.1f}% of queries)")
            print(f"   - Verify this is expected usage pattern")
            print()
    
    print("=" * 70)
    print(f"Analysis complete! Data from last {days} days.")
    print("=" * 70)


if __name__ == "__main__":
    log_file = "/home/ubuntu/humanergy/chatbot/rasa/logs/query_log.jsonl"
    days = 7
    
    if len(sys.argv) > 1:
        days = int(sys.argv[1])
    
    if len(sys.argv) > 2:
        log_file = sys.argv[2]
    
    analyze_logs(log_file, days)
