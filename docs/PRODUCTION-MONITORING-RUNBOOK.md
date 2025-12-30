# EnMS Chatbot - Production Monitoring Runbook

**Purpose:** Continuous improvement through real-world usage monitoring  
**Frequency:** Weekly analysis + on-demand troubleshooting  
**Owner:** System Administrator / AI Team

---

## 📅 Weekly Monitoring Schedule

### Monday 9:00 AM (Automated)

**Cron Job:** Analyzes previous week's query logs
```bash
# Add to crontab (crontab -e):
0 9 * * 1 /home/ubuntu/humanergy/scripts/weekly_chatbot_analysis.sh >> /var/log/chatbot_analysis.log 2>&1
```

**Output:** Report saved to `/home/ubuntu/humanergy/chatbot/reports/weekly_analysis_YYYYMMDD.txt`

**Review Time:** 15-30 minutes

---

## 🔍 What to Monitor

### 1. Success Rate
**Target:** ≥85% answered queries  
**Alert Threshold:** <75% answered

**Action if below threshold:**
- Review top failed queries
- Add missing keywords
- Expand relevant Q&A categories

### 2. Top Categories
**What to check:**
- Are users asking about expected topics?
- Any surprising category popularity?
- Any categories with zero usage?

**Action items:**
- Prioritize improvements for high-traffic categories
- Consider removing/merging unused categories

### 3. Failed Queries
**Critical:** Any query failing >3 times/week

**Action steps:**
1. Identify root cause (misspelling, missing keyword, ambiguous)
2. Add appropriate keywords to `actions.py`
3. Consider adding new Q&A pairs if topic is missing
4. Rebuild and redeploy container

### 4. Performance Metrics
**Target:** <15ms avg response time  
**Alert Threshold:** >50ms avg

**Action if slow:**
- Check database query performance
- Review keyword_to_topic dict size
- Consider caching frequent queries

### 5. Intent Distribution
**Expected:**
- `action.retrieve_answer`: 80-90%
- `action.fallback`: 5-10%
- `process`: 3-5%
- `requirement`: 2-3%

**Action if skewed:**
- High fallback rate → Missing keywords
- Low retrieve_answer → Intent routing issues

---

## 🛠️ Weekly Review Process

### Step 1: Run Analysis (Automated)
```bash
# Manual run if needed:
cd /home/ubuntu/humanergy
bash scripts/weekly_chatbot_analysis.sh
```

### Step 2: Review Report (15 min)
```bash
# View latest report
cat /home/ubuntu/humanergy/chatbot/reports/weekly_analysis_$(date +%Y%m%d).txt

# Compare to previous week
cat /home/ubuntu/humanergy/chatbot/reports/weekly_analysis_$(date -d '7 days ago' +%Y%m%d).txt
```

**Check these sections:**
1. ✅ Status Distribution - Is success rate good?
2. ✅ Top 10 Categories - Any surprises?
3. ✅ Failed Queries - Critical issues?
4. ✅ Performance Metrics - Response times okay?
5. ✅ Recommendations - Action items listed

### Step 3: Take Action (Variable time)

**For Failed Queries:**
1. Test the query manually:
   ```bash
   cd /home/ubuntu/humanergy
   python3 scripts/test_skill_chat.py "exact failing query"
   ```

2. Add missing keywords to `chatbot/rasa/actions/actions.py`:
   ```python
   keyword_to_topic = {
       # Add new mappings
       "new keyword": "ask_appropriate_category",
   }
   ```

3. Rebuild and deploy:
   ```bash
   docker compose build rasa-actions --no-cache
   docker compose restart rasa-actions
   ```

4. Re-test to verify fix

**For Missing Topics:**
1. Create new Q&A entries in `chatbot/rasa/qa_data.json`
2. Add keywords to route to new category
3. Test and deploy

### Step 4: Document Changes
Update in Git:
```bash
cd /home/ubuntu/humanergy
git add chatbot/rasa/actions/actions.py chatbot/rasa/qa_data.json
git commit -m "chore(chatbot): Add keywords for [topic] based on weekly analysis"
git push
```

---

## 🚨 Alert Thresholds & Actions

| Metric | Alert Threshold | Action |
|--------|----------------|--------|
| Success Rate | <75% | Immediate review, add keywords |
| Avg Response Time | >50ms | Check performance, optimize queries |
| Failed Query (same) | >5 times/week | Priority fix, add to backlog |
| Total Queries | <10/week | Check if chatbot is accessible |
| Fallback Rate | >20% | Review intent routing, NLU model |

---

## 📊 Manual Analysis Commands

### Check Recent Queries
```bash
tail -20 /home/ubuntu/humanergy/chatbot/rasa/logs/query_log.jsonl | jq -r '.query'
```

### Count Queries by Status
```bash
cat /home/ubuntu/humanergy/chatbot/rasa/logs/query_log.jsonl | \
  jq -r '.status' | sort | uniq -c
```

### Find All Failures
```bash
cat /home/ubuntu/humanergy/chatbot/rasa/logs/query_log.jsonl | \
  jq -r 'select(.status=="failed") | .query'
```

### Check Performance
```bash
cat /home/ubuntu/humanergy/chatbot/rasa/logs/query_log.jsonl | \
  jq -r '.response_time_ms' | \
  awk '{sum+=$1; count++} END {print "Avg:", sum/count "ms"}'
```

### Top 10 Categories
```bash
cat /home/ubuntu/humanergy/chatbot/rasa/logs/query_log.jsonl | \
  jq -r '.category' | sort | uniq -c | sort -rn | head -10
```

---

## 🧪 Testing New Improvements

### Before Deploying Changes

1. **Test locally:**
   ```bash
   python3 scripts/test_skill_chat.py "test query"
   ```

2. **Run regression tests:**
   ```bash
   cd chatbot/rasa/tests
   pytest test_regression.py -v
   ```

3. **Run comprehensive suite:**
   ```bash
   bash scripts/test_chatbot_comprehensive.sh
   ```

### After Deploying

1. **Verify container health:**
   ```bash
   docker compose ps rasa-actions
   ```

2. **Check logs for errors:**
   ```bash
   docker compose logs rasa-actions --tail 50
   ```

3. **Test previously failed queries:**
   ```bash
   python3 scripts/test_skill_chat.py "query that was failing"
   ```

---

## 📝 Monthly Review (Additional)

**When:** First Monday of each month  
**Duration:** 30-60 minutes

**Review:**
1. Aggregate statistics for past 4 weeks
2. Identify trends in query patterns
3. Plan larger improvements (new categories, UI changes)
4. Update documentation based on learnings
5. Review and update this runbook

**Deliverable:** Monthly summary document with improvement roadmap

---

## 🔧 Troubleshooting Common Issues

### Issue: High Fallback Rate

**Symptoms:** Many queries returning generic answers  
**Diagnosis:**
```bash
# Check which queries are falling back
cat query_log.jsonl | jq -r 'select(.status=="fallback") | .query'
```

**Solutions:**
1. Add keywords for common fallback queries
2. Review keyword_to_topic priorities (longest-match-first)
3. Check for misspellings not in dictionary
4. Expand Q&A content for ambiguous topics

### Issue: Slow Response Times

**Symptoms:** Avg response time >50ms  
**Diagnosis:**
```bash
# Check slowest queries
cat query_log.jsonl | jq -r '. | "\(.response_time_ms)ms - \(.query)"' | sort -rn | head -10
```

**Solutions:**
1. Check database performance
2. Review qa_data.json size (split if >1MB)
3. Add caching for frequent queries
4. Profile Python code with cProfile

### Issue: Container Crashes

**Symptoms:** rasa-actions container unhealthy/restarting  
**Diagnosis:**
```bash
docker compose logs rasa-actions --tail 100
```

**Solutions:**
1. Check for memory leaks (memory usage growing)
2. Review Python exceptions in logs
3. Verify qa_data.json is valid JSON
4. Check disk space: `df -h`
5. Restart: `docker compose restart rasa-actions`

### Issue: No Queries Logged

**Symptoms:** query_log.jsonl not updating  
**Diagnosis:**
```bash
# Check if file exists and is writable
ls -la /home/ubuntu/humanergy/chatbot/rasa/logs/query_log.jsonl

# Check container logs for write errors
docker compose logs rasa-actions | grep -i "error\|permission"
```

**Solutions:**
1. Verify logging is enabled in actions.py
2. Check file permissions: `chmod 666 query_log.jsonl`
3. Check volume mounts in docker-compose.yml
4. Recreate container: `docker compose up -d --force-recreate rasa-actions`

---

## 📚 Reference Files

| File | Purpose |
|------|---------|
| `scripts/analyze_query_logs.py` | Log analysis script |
| `scripts/weekly_chatbot_analysis.sh` | Automated weekly run |
| `chatbot/rasa/logs/query_log.jsonl` | Raw query logs |
| `chatbot/reports/weekly_analysis_*.txt` | Weekly reports |
| `chatbot/rasa/actions/actions.py` | Keyword routing logic |
| `chatbot/rasa/qa_data.json` | Q&A content database |
| `docs/KNOWLEDGE-BASE-TODO.md` | Improvement tracking |

---

## 🎯 Success Metrics

**Week-over-Week Goals:**
- ✅ Success rate increasing or stable at ≥85%
- ✅ Response time stable at <15ms avg
- ✅ Failed query count decreasing
- ✅ Query volume increasing (more usage)
- ✅ All critical failures resolved within 48 hours

**Long-term Goals (3 months):**
- ✅ Success rate ≥90%
- ✅ Zero recurring failed queries
- ✅ <5% fallback rate
- ✅ User feedback mechanism implemented
- ✅ A/B testing framework ready

---

## 🚀 Continuous Improvement Cycle

```
1. Monitor → 2. Analyze → 3. Identify Issues → 4. Fix → 5. Test → 6. Deploy → 7. Verify → [Repeat]
   ↑                                                                                        ↓
   └────────────────────────────────────────────────────────────────────────────────────────┘
```

**Remember:** The chatbot improves through real-world usage. Every failed query is an opportunity to enhance coverage!

---

**Last Updated:** 2025-12-30  
**Version:** 1.0  
**Next Review:** 2026-01-30
