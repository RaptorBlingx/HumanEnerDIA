# 🧪 EnMS Assistant - Testing & Improvement Strategy

**Purpose:** Systematic approach to test, measure, and continuously improve the RASA chatbot  
**Date:** 2025-12-30  
**Status:** Active Testing Phase

---

## 📊 Testing Philosophy

Senior engineers approach chatbot testing with:
1. **Data-Driven Decisions** - Metrics over opinions
2. **User-Centric Testing** - Real queries, not synthetic
3. **Continuous Iteration** - Small improvements, frequent releases
4. **Failure Analysis** - Learn from every wrong answer
5. **Coverage Gaps** - Find what's missing, not just what's broken

---

## 🎯 Testing Levels

### Level 1: Unit Testing (Component Isolation)
**What:** Test individual Q&A categories in isolation  
**Goal:** Verify each category works correctly

### Level 2: Integration Testing (Keyword Collision)
**What:** Test boundary cases where keywords might conflict  
**Goal:** Ensure routing logic prioritizes correctly

### Level 3: End-to-End Testing (Real User Scenarios)
**What:** Test complete user journeys with context  
**Goal:** Validate natural conversation flow

### Level 4: Stress Testing (Performance & Scale)
**What:** Test with high query volume and concurrent users  
**Goal:** Identify bottlenecks and resource limits

---

## 🔬 Test Strategy 1: Real User Query Analysis

### Implementation
1. **Enable Query Logging**
   ```python
   # Add to chatbot/rasa/actions/actions.py
   import logging
   logger = logging.getLogger(__name__)
   
   def run(self, dispatcher, tracker, domain):
       user_message = tracker.latest_message.get("text", "")
       logger.info(f"USER_QUERY: {user_message}")
       # ... existing code
   ```

2. **Collect Real Queries** (1 week minimum)
   - Log all incoming queries to file
   - Categorize by: answered correctly, answered incorrectly, no answer
   - Analyze patterns in failed queries

3. **Metrics to Track**
   - Total queries per day
   - Success rate (user got answer)
   - No-match rate (no Q&A found)
   - Top 10 unanswered queries
   - Average response time

### Analysis Script
```bash
# Extract failed queries from logs
grep "USER_QUERY" logs/rasa-actions.log | \
  awk -F"USER_QUERY: " '{print $2}' | \
  sort | uniq -c | sort -rn > failed_queries.txt
```

---

## 🎯 Test Strategy 2: Systematic Coverage Testing

### Create Test Matrix

| Category | Sample Queries | Expected Behavior | Current Status |
|----------|----------------|-------------------|----------------|
| Portal Baseline | "How do I train baseline?", "What is R² score?", "Show me baseline chart" | Returns portal_baseline Q&As | ✅ PASS |
| Grafana Anomaly | "Anomaly dashboard", "MTTR graph", "Severity distribution" | Returns grafana_anomaly Q&As | ✅ PASS |
| OVOS Energy | "How to ask energy by voice", "Energy commands" | Returns ovos_energy Q&As | ✅ PASS |
| ... | ... | ... | ... |

### Coverage Gaps Test
```python
# Test every category has at least 5 variations
test_queries = {
    "ask_portal_baseline": [
        "What is baseline page?",
        "How to train baseline?",
        "What is R² score?",
        "Baseline prediction chart",
        "Coefficient impact bars"
    ],
    # ... repeat for all 67 categories
}
```

---

## 🔍 Test Strategy 3: Error Analysis Framework

### Classification of Failures

**Type 1: Wrong Category** (routing error)
- Query: "What is baseline?" 
- Expected: `ask_energy_baseline` (ISO 50001)
- Actual: `ask_concept_baseline` (technical concept)
- **Fix:** Adjust keyword priority or add disambiguation

**Type 2: No Match** (missing content)
- Query: "How do I export data to Excel?"
- Expected: Answer about export functionality
- Actual: No matching Q&A
- **Fix:** Add new Q&A pair to appropriate category

**Type 3: Incomplete Answer** (content quality)
- Query: "What KPIs are tracked?"
- Expected: Comprehensive list
- Actual: Generic answer missing details
- **Fix:** Improve answer quality in qa_data.json

**Type 4: Ambiguous Query** (user clarity issue)
- Query: "How does it work?"
- Expected: Needs context
- Actual: Returns generic answer
- **Fix:** Add clarifying follow-up question

### Tracking Template
```markdown
## Error Log Entry

**Date:** 2025-12-30
**Query:** "How do I see power consumption?"
**Error Type:** Wrong Category
**Expected Category:** `ask_portal_dashboard` or `ask_grafana_realtime`
**Actual Category:** `ask_ovos_energy`
**Root Cause:** Keyword "power consumption" matches OVOS voice category
**Fix Applied:** Added "power consumption page" keyword to portal
**Retest Result:** ✅ PASS
```

---

## 📈 Test Strategy 4: A/B Testing Different Approaches

### Test Scenarios

**A/B Test 1: Keyword Length Priority vs Explicit Ranking**
- **Group A:** Current system (longer keywords = higher priority)
- **Group B:** Explicit priority scores per category
- **Metric:** Accuracy on 100 test queries
- **Duration:** 1 week

**A/B Test 2: Fuzzy Matching Threshold**
- **Group A:** Current threshold (score > 0.7)
- **Group B:** Lower threshold (score > 0.6)
- **Metric:** False positive rate vs coverage
- **Duration:** 1 week

---

## 🎯 Test Strategy 5: Adversarial Testing (Break the Bot)

### Intentionally Difficult Queries

```python
adversarial_queries = [
    # Compound questions
    "What is baseline and how do I train it?",
    
    # Ambiguous context
    "Show me the dashboard",  # Which one?
    
    # Misspellings
    "What is eneregy baseline?",
    "Anaomaly detection",
    
    # Abbreviations
    "OEE calc",
    "HVAC stats",
    
    # Multi-language mix
    "What is EnPI en español?",
    
    # Extremely long queries
    "I want to know about the baseline page where I can train models...",
    
    # Edge cases
    "",  # Empty query
    "???",  # Only punctuation
    "asdfghjkl"  # Random characters
]
```

**Expected Behavior:**
- Compound questions → Answer both or suggest breaking apart
- Ambiguous → Ask for clarification
- Misspellings → Fuzzy match should handle
- Empty/nonsense → Graceful fallback message

---

## 🔧 Test Strategy 6: Automated Regression Suite

### Create Test Suite Script

```python
# File: chatbot/rasa/tests/test_regression.py
import pytest
import json
from actions.actions import ActionRetrieveAnswer

class TestRegressionSuite:
    
    @pytest.fixture
    def test_cases(self):
        """Load test cases from JSON"""
        with open('tests/test_cases.json') as f:
            return json.load(f)
    
    def test_iso_50001_queries(self, test_cases):
        """Ensure ISO 50001 queries still work"""
        for query, expected_category in test_cases['iso_50001']:
            result = self._query_chatbot(query)
            assert expected_category in result['topic']
    
    def test_portal_queries(self, test_cases):
        """Test all portal page queries"""
        for query, expected_category in test_cases['portal']:
            result = self._query_chatbot(query)
            assert expected_category in result['topic']
    
    def test_performance(self):
        """Response time should be <500ms"""
        import time
        queries = ["What is Humanergy?"] * 100
        
        start = time.time()
        for q in queries:
            self._query_chatbot(q)
        duration = (time.time() - start) / len(queries)
        
        assert duration < 0.5, f"Avg response time {duration}s exceeds 500ms"
    
    def _query_chatbot(self, query):
        # Implementation to call chatbot API
        pass
```

### Test Cases File
```json
{
  "iso_50001": [
    ["What is the scope of EnMS?", "ask_scope"],
    ["What is PDCA?", "ask_pdca"],
    ["What is management review?", "ask_management_review"]
  ],
  "portal": [
    ["What is the baseline page?", "ask_portal_baseline"],
    ["What is the anomaly page?", "ask_portal_anomaly"]
  ],
  "grafana": [
    ["Factory Overview dashboard", "ask_grafana_factory"],
    ["Cost Analytics dashboard", "ask_grafana_cost"]
  ]
}
```

### Run Tests
```bash
# Run full regression suite
cd /home/ubuntu/humanergy/chatbot/rasa
pytest tests/test_regression.py -v

# Run with coverage report
pytest tests/ --cov=actions --cov-report=html
```

---

## 📊 Test Strategy 7: Metrics & KPIs

### Key Metrics to Track

| Metric | Definition | Target | Current |
|--------|------------|--------|---------|
| **Accuracy** | % queries answered correctly | >95% | 95.5% ✅ |
| **Coverage** | % queries with any answer | >98% | TBD |
| **Response Time** | Avg latency (ms) | <500ms | 12ms ✅ |
| **No-Match Rate** | % queries with no answer | <5% | TBD |
| **User Satisfaction** | Thumbs up/down feedback | >90% | TBD |
| **Category Distribution** | Which categories used most | Balanced | TBD |

### Data Collection
```sql
-- Create metrics table
CREATE TABLE chatbot_metrics (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    query TEXT NOT NULL,
    matched_category TEXT,
    response_time_ms INTEGER,
    user_feedback TEXT, -- 'positive', 'negative', null
    session_id TEXT
);

-- Query analysis
SELECT 
    matched_category,
    COUNT(*) as query_count,
    AVG(response_time_ms) as avg_response_time,
    SUM(CASE WHEN user_feedback = 'positive' THEN 1 ELSE 0 END)::FLOAT / COUNT(*) as satisfaction_rate
FROM chatbot_metrics
WHERE timestamp > NOW() - INTERVAL '7 days'
GROUP BY matched_category
ORDER BY query_count DESC;
```

---

## 🎯 Test Strategy 8: User Feedback Loop

### Implementation

1. **Add Feedback Buttons to Chat UI**
```javascript
// chatbot/ChatBotUI.tsx
function MessageWithFeedback({ message, messageId }) {
  const [feedback, setFeedback] = useState(null);
  
  const sendFeedback = async (isPositive) => {
    await fetch('/api/chatbot/feedback', {
      method: 'POST',
      body: JSON.stringify({
        message_id: messageId,
        query: message.query,
        response: message.response,
        feedback: isPositive ? 'positive' : 'negative'
      })
    });
    setFeedback(isPositive);
  };
  
  return (
    <div>
      <div className="message">{message.response}</div>
      <div className="feedback-buttons">
        <button onClick={() => sendFeedback(true)}>👍</button>
        <button onClick={() => sendFeedback(false)}>👎</button>
      </div>
    </div>
  );
}
```

2. **Weekly Feedback Review**
```bash
# Extract negative feedback for review
psql -d enms -c "
  SELECT query, matched_category, COUNT(*) as negative_count
  FROM chatbot_metrics
  WHERE user_feedback = 'negative'
    AND timestamp > NOW() - INTERVAL '7 days'
  GROUP BY query, matched_category
  ORDER BY negative_count DESC
  LIMIT 20;
"
```

---

## 🔄 Continuous Improvement Process

### Weekly Cycle

**Monday - Data Collection**
1. Export last week's query logs
2. Calculate metrics (accuracy, coverage, response time)
3. Identify top 10 failed/negative queries

**Tuesday - Analysis**
1. Categorize failures (Type 1-4)
2. Identify root causes
3. Prioritize fixes (high impact first)

**Wednesday - Implementation**
1. Add missing Q&As
2. Adjust keywords
3. Improve answer quality
4. Update tests

**Thursday - Testing**
1. Run regression suite
2. Test fixes manually
3. Verify no new regressions
4. Update test cases

**Friday - Deployment & Monitoring**
1. Rebuild rasa-actions container
2. Deploy to production
3. Monitor for issues
4. Document changes

### Monthly Review
- Analyze trends over 4 weeks
- Identify systematic issues
- Plan larger improvements
- Update testing strategy

---

## 🛠️ Practical Testing Scripts

### Script 1: Comprehensive Test Runner
```bash
#!/bin/bash
# File: scripts/test_chatbot_comprehensive.sh

echo "🧪 EnMS Chatbot Testing Suite"
echo "=============================="
echo ""

RESULTS_FILE="/tmp/chatbot_test_results_$(date +%Y%m%d_%H%M%S).md"

{
echo "# Chatbot Test Results"
echo "**Date:** $(date)"
echo ""

# Test 1: All Categories
echo "## Test 1: Category Coverage"
echo ""
python3 << 'PYEOF'
import json
with open('/home/ubuntu/humanergy/chatbot/rasa/qa_data.json') as f:
    data = json.load(f)
    
test_results = []
for category, qas in data.items():
    if len(qas) > 0:
        # Test with first question from category
        test_results.append(f"✅ {category}: {len(qas)} Q&As")
    else:
        test_results.append(f"❌ {category}: EMPTY")

for result in sorted(test_results):
    print(result)
PYEOF

# Test 2: Performance
echo ""
echo "## Test 2: Performance"
echo ""
for i in {1..10}; do
    start=$(date +%s%N)
    curl -s -X POST http://localhost:5055/webhook \
      -H "Content-Type: application/json" \
      -d '{"next_action":"action_retrieve_answer","sender_id":"test","tracker":{"sender_id":"test","slots":{"topic":null},"latest_message":{"intent":{"name":"definition"},"text":"What is Humanergy?"},"events":[],"paused":false,"followup_action":null,"active_loop":null,"latest_action_name":null},"domain":{}}' > /dev/null 2>&1
    end=$(date +%s%N)
    ms=$(( (end - start) / 1000000 ))
    echo "Request $i: ${ms}ms"
done | awk '{sum+=$3; count++} END {print "Average: " sum/count "ms"}'

# Test 3: Collision Detection
echo ""
echo "## Test 3: Keyword Collisions"
echo ""

test_collision() {
    query="$1"
    response=$(curl -s -X POST http://localhost:5055/webhook \
      -H "Content-Type: application/json" \
      -d "{\"next_action\":\"action_retrieve_answer\",\"sender_id\":\"test\",\"tracker\":{\"sender_id\":\"test\",\"slots\":{\"topic\":null},\"latest_message\":{\"intent\":{\"name\":\"definition\"},\"text\":\"$query\"},\"events\":[],\"paused\":false,\"followup_action\":null,\"active_loop\":null,\"latest_action_name\":null},\"domain\":{}}" 2>/dev/null | jq -r '.responses[0].text' 2>/dev/null | head -c 50)
    echo "- \"$query\" → ${response}..."
}

test_collision "baseline"
test_collision "baseline page"
test_collision "energy baseline"
test_collision "anomaly"
test_collision "anomaly page"
test_collision "grafana anomaly"

} > "$RESULTS_FILE"

echo ""
echo "✅ Test complete! Results saved to: $RESULTS_FILE"
cat "$RESULTS_FILE"
```

### Script 2: Find Missing Keywords
```python
# File: scripts/analyze_coverage_gaps.py
import json
import re

# Load Q&A data
with open('chatbot/rasa/qa_data.json') as f:
    qa_data = json.load(f)

# Load keywords from actions.py
with open('chatbot/rasa/actions/actions.py') as f:
    actions_code = f.read()

# Extract all keyword mappings
keyword_pattern = r'"([^"]+)":\s*"(ask_[^"]+)"'
keywords_in_code = dict(re.findall(keyword_pattern, actions_code))

print("Coverage Analysis")
print("=" * 60)

# Check each category has keywords
for category in qa_data.keys():
    mapped_keywords = [k for k, v in keywords_in_code.items() if v == category]
    
    if len(mapped_keywords) == 0:
        print(f"❌ {category}: NO KEYWORDS MAPPED")
    elif len(mapped_keywords) < 3:
        print(f"⚠️  {category}: Only {len(mapped_keywords)} keywords")
    else:
        print(f"✅ {category}: {len(mapped_keywords)} keywords")

print("\n" + "=" * 60)
print(f"Total Categories: {len(qa_data)}")
print(f"Total Keywords: {len(keywords_in_code)}")
```

---

## 🎓 Best Practices from Senior Engineers

### 1. **Test Early, Test Often**
- Don't wait for "complete" - test after every change
- Automated tests run on every commit

### 2. **Real Data > Synthetic Data**
- Use actual user queries, not made-up examples
- A/B test in production with real users

### 3. **Measure What Matters**
- Focus on user satisfaction, not technical perfection
- 95% accuracy with good UX > 99% accuracy with poor UX

### 4. **Fail Fast, Learn Faster**
- Every failure is a test case to add
- Document why something failed, not just that it failed

### 5. **Incremental Improvement**
- Small, frequent improvements > big infrequent changes
- Each iteration should improve 1-2 metrics

### 6. **Coverage > Depth**
- Better to answer 90% of questions adequately
- Than answer 50% of questions perfectly

### 7. **Monitor in Production**
- Testing in staging ≠ testing in production
- Real users find edge cases you never imagined

---

## 📋 Testing Checklist (Use This!)

Before marking any release as "done":

- [ ] All 67 categories have ≥3 test queries
- [ ] Regression tests pass (no broken ISO 50001 queries)
- [ ] Performance: Avg response time <500ms
- [ ] Coverage: >95% of test queries get an answer
- [ ] Collision test: All priority keywords route correctly
- [ ] Quality: Sample 10 random answers for accuracy
- [ ] Feedback: Review last week's negative feedback
- [ ] Documentation: Update test cases with new queries
- [ ] Monitoring: Metrics dashboard shows healthy trends

---

## 🚀 Next Steps

### Immediate (This Week)
1. Run comprehensive test script
2. Collect real user queries for 1 week
3. Implement feedback buttons in UI
4. Create metrics tracking table

### Short-term (This Month)
1. Build automated regression suite
2. Analyze first week of real queries
3. Fix top 10 failing queries
4. Add missing Q&As based on gaps

### Long-term (Next Quarter)
1. Implement A/B testing framework
2. Build metrics dashboard
3. Train model on collected data
4. Expand to cover remaining gaps

---

**Remember:** The best chatbot is one that continuously learns from its users!
