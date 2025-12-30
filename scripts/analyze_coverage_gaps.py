#!/usr/bin/env python3
"""
EnMS Chatbot Coverage Gap Analysis
Identifies categories without sufficient keyword mappings
"""

import json
import re
from collections import defaultdict

def analyze_coverage():
    # Load Q&A data
    with open('/home/ubuntu/humanergy/chatbot/rasa/qa_data.json') as f:
        qa_data = json.load(f)
    
    # Load keywords from actions.py
    with open('/home/ubuntu/humanergy/chatbot/rasa/actions/actions.py') as f:
        actions_code = f.read()
    
    # Extract all keyword mappings
    keyword_pattern = r'"([^"]+)":\s*"(ask_[^"]+)"'
    keywords_raw = re.findall(keyword_pattern, actions_code)
    
    # Build mapping of category -> list of keywords
    category_keywords = defaultdict(list)
    for keyword, category in keywords_raw:
        category_keywords[category].append(keyword)
    
    print("=" * 70)
    print("EnMS Chatbot Coverage Gap Analysis")
    print("=" * 70)
    print()
    
    # Analyze each category
    no_keywords = []
    few_keywords = []
    good_keywords = []
    
    for category in sorted(qa_data.keys()):
        qa_count = len(qa_data[category])
        keyword_count = len(category_keywords[category])
        
        status = ""
        if keyword_count == 0:
            status = "❌ NO KEYWORDS"
            no_keywords.append((category, qa_count, keyword_count))
        elif keyword_count < 3:
            status = f"⚠️  Only {keyword_count} keyword(s)"
            few_keywords.append((category, qa_count, keyword_count))
        else:
            status = f"✅ {keyword_count} keywords"
            good_keywords.append((category, qa_count, keyword_count))
        
        print(f"{category:45s} | Q&As: {qa_count:3d} | {status}")
    
    print()
    print("=" * 70)
    print("Summary")
    print("=" * 70)
    print()
    print(f"✅ Good coverage (≥3 keywords):  {len(good_keywords):3d} categories")
    print(f"⚠️  Low coverage (<3 keywords):  {len(few_keywords):3d} categories")
    print(f"❌ No keywords:                   {len(no_keywords):3d} categories")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"   Total:                        {len(qa_data):3d} categories")
    print()
    
    # Detailed report on problem categories
    if no_keywords:
        print("=" * 70)
        print("⚠️  CRITICAL: Categories with NO keywords")
        print("=" * 70)
        print()
        for cat, qa_count, kw_count in no_keywords:
            print(f"  {cat}")
            print(f"    - {qa_count} Q&A pairs available")
            print(f"    - Action: Add keywords to actions.py")
            # Show first question as example
            if qa_data[cat]:
                first_q = qa_data[cat][0][0]
                print(f"    - Example Q: \"{first_q}\"")
            print()
    
    if few_keywords:
        print("=" * 70)
        print("⚠️  LOW COVERAGE: Categories with <3 keywords")
        print("=" * 70)
        print()
        for cat, qa_count, kw_count in few_keywords:
            print(f"  {cat}")
            print(f"    - {qa_count} Q&A pairs, {kw_count} keyword(s)")
            print(f"    - Current keywords: {', '.join(category_keywords[cat])}")
            print(f"    - Action: Add more keyword variations")
            print()
    
    # Keyword statistics
    print("=" * 70)
    print("Keyword Statistics")
    print("=" * 70)
    print()
    
    total_keywords = sum(len(kws) for kws in category_keywords.values())
    unique_categories = len([cat for cat in qa_data.keys() if len(category_keywords[cat]) > 0])
    
    print(f"Total keywords mapped:        {total_keywords}")
    print(f"Categories with keywords:     {unique_categories}/{len(qa_data)}")
    print(f"Avg keywords per category:    {total_keywords / len(qa_data):.1f}")
    print()
    
    # Find potential duplicate keywords (same keyword -> multiple categories)
    keyword_to_categories = defaultdict(list)
    for keyword, category in keywords_raw:
        keyword_to_categories[keyword].append(category)
    
    duplicates = {k: v for k, v in keyword_to_categories.items() if len(v) > 1}
    if duplicates:
        print("=" * 70)
        print("⚠️  POTENTIAL CONFLICTS: Keywords mapped to multiple categories")
        print("=" * 70)
        print()
        for keyword, categories in sorted(duplicates.items()):
            print(f"  \"{keyword}\" → {', '.join(categories)}")
        print()
        print(f"Total conflicts: {len(duplicates)}")
        print()
    
    # Recommendations
    print("=" * 70)
    print("Recommendations")
    print("=" * 70)
    print()
    
    if no_keywords:
        print(f"1. HIGH PRIORITY: Add keywords for {len(no_keywords)} categories with no mappings")
    
    if few_keywords:
        print(f"2. MEDIUM PRIORITY: Expand keywords for {len(few_keywords)} categories with <3 mappings")
    
    if duplicates:
        print(f"3. REVIEW: Check {len(duplicates)} keyword conflicts for correct priority")
    
    coverage_pct = (len(good_keywords) / len(qa_data)) * 100
    print(f"\nCurrent Coverage: {coverage_pct:.1f}% of categories have good keyword coverage")
    
    if coverage_pct >= 95:
        print("Status: ✅ EXCELLENT - Coverage is very good!")
    elif coverage_pct >= 85:
        print("Status: ✅ GOOD - Minor improvements possible")
    elif coverage_pct >= 70:
        print("Status: ⚠️  FAIR - Significant gaps to address")
    else:
        print("Status: ❌ POOR - Major coverage issues")
    
    print()
    print("=" * 70)

if __name__ == "__main__":
    analyze_coverage()
