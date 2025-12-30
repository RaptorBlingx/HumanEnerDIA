# User Feedback Mechanism - Implementation Plan

**Goal:** Enable users to rate chatbot responses for continuous improvement  
**Priority:** Medium (Phase 10 - Priority 3)  
**Estimated Effort:** 2-3 hours  
**Status:** Design Complete, Ready for Implementation

---

## Overview

Add thumbs up/down buttons to each chatbot response, store feedback with query logs, and analyze patterns to identify Q&A improvements needed.

---

## Architecture

```
┌─────────────────┐
│   Chatbot UI    │
│  (React/TSX)    │
│                 │
│  Message        │
│  [👍] [👎]      │
└────────┬────────┘
         │ POST /feedback
         ▼
┌─────────────────┐
│  RASA Actions   │
│   (actions.py)  │
│                 │
│  Log feedback   │
└────────┬────────┘
         │ Append to log
         ▼
┌─────────────────┐
│ query_log.jsonl │
│                 │
│ {feedback: true}│
└────────┬────────┘
         │ Weekly analysis
         ▼
┌─────────────────┐
│  Analysis Tool  │
│                 │
│ Identify issues │
└─────────────────┘
```

---

## Implementation Steps

### Step 1: Update UI (ChatBotUI.tsx)

**Location:** `/home/ubuntu/humanergy/chatbot/ChatBotUI.tsx`

**Add feedback buttons to each bot message:**

```tsx
interface Message {
  text: string;
  sender: 'user' | 'bot';
  timestamp: Date;
  messageId?: string; // Add unique ID
  feedback?: 'positive' | 'negative' | null;
}

// Add after bot message display
{message.sender === 'bot' && (
  <div className="flex gap-2 mt-2">
    <button
      onClick={() => handleFeedback(message.messageId, 'positive')}
      className={`p-2 rounded ${
        message.feedback === 'positive' 
          ? 'bg-green-100 text-green-600' 
          : 'bg-gray-100 hover:bg-gray-200'
      }`}
      title="Helpful"
      disabled={message.feedback !== null}
    >
      👍
    </button>
    <button
      onClick={() => handleFeedback(message.messageId, 'negative')}
      className={`p-2 rounded ${
        message.feedback === 'negative' 
          ? 'bg-red-100 text-red-600' 
          : 'bg-gray-100 hover:bg-gray-200'
      }`}
      title="Not helpful"
      disabled={message.feedback !== null}
    >
      👎
    </button>
  </div>
)}
```

**Add feedback handler:**

```tsx
const handleFeedback = async (messageId: string, feedbackType: 'positive' | 'negative') => {
  try {
    // Update UI immediately
    setMessages(prev => 
      prev.map(msg => 
        msg.messageId === messageId 
          ? { ...msg, feedback: feedbackType }
          : msg
      )
    );

    // Send to backend
    const response = await fetch('http://localhost:5055/feedback', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message_id: messageId,
        feedback: feedbackType,
        timestamp: new Date().toISOString()
      })
    });

    if (!response.ok) {
      console.error('Failed to submit feedback');
    }
  } catch (error) {
    console.error('Error submitting feedback:', error);
  }
};
```

**Generate unique message IDs:**

```tsx
// When bot sends response
const botMessage: Message = {
  text: response.text,
  sender: 'bot',
  timestamp: new Date(),
  messageId: `msg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
  feedback: null
};
```

---

### Step 2: Update Backend (actions.py)

**Location:** `/home/ubuntu/humanergy/chatbot/rasa/actions/actions.py`

**Add feedback endpoint (Flask/Sanic route):**

```python
# Add after ActionRetrieveAnswer class

from sanic import Sanic, response
from sanic.request import Request

# Get the Sanic app instance from rasa_sdk
app = Sanic.get_app("rasa_sdk")

@app.route("/feedback", methods=["POST"])
async def handle_feedback(request: Request):
    """
    Receive user feedback on chatbot responses.
    
    Expected payload:
    {
        "message_id": "msg_1234_abc",
        "feedback": "positive" or "negative",
        "timestamp": "2025-12-30T10:00:00Z"
    }
    """
    try:
        data = request.json
        message_id = data.get("message_id")
        feedback_type = data.get("feedback")
        timestamp = data.get("timestamp")
        
        # Validate input
        if not message_id or feedback_type not in ["positive", "negative"]:
            return response.json(
                {"error": "Invalid feedback data"},
                status=400
            )
        
        # Log feedback to query log
        log_file = "/app/logs/query_log.jsonl"
        feedback_entry = {
            "type": "feedback",
            "message_id": message_id,
            "feedback": feedback_type,
            "timestamp": timestamp,
            "recorded_at": datetime.utcnow().isoformat()
        }
        
        with open(log_file, "a") as f:
            f.write(json.dumps(feedback_entry) + "\n")
        
        logger.info(f"Feedback recorded: {message_id} = {feedback_type}")
        
        return response.json(
            {"success": True, "message": "Feedback recorded"},
            status=200
        )
        
    except Exception as e:
        logger.error(f"Error handling feedback: {e}")
        return response.json(
            {"error": "Internal server error"},
            status=500
        )
```

**Update query logging to include message ID:**

```python
# In ActionRetrieveAnswer.run() method
# After generating response

message_id = f"msg_{int(datetime.utcnow().timestamp() * 1000)}_{uuid.uuid4().hex[:8]}"

log_entry = {
    "timestamp": datetime.utcnow().isoformat(),
    "message_id": message_id,  # Add this
    "query": user_message,
    "category": selected_category or "unknown",
    "status": "answered" if selected_category else "failed",
    "response_time_ms": response_time_ms
}

# Return message ID to UI (add to response metadata)
```

---

### Step 3: Update Analysis Tool

**Location:** `/home/ubuntu/humanergy/scripts/analyze_query_logs.py`

**Add feedback analysis section:**

```python
def analyze_feedback(entries):
    """Analyze user feedback on responses."""
    feedback_entries = [e for e in entries if e.get('type') == 'feedback']
    
    if not feedback_entries:
        return "No feedback data yet."
    
    positive = sum(1 for e in feedback_entries if e['feedback'] == 'positive')
    negative = sum(1 for e in feedback_entries if e['feedback'] == 'negative')
    total = len(feedback_entries)
    
    satisfaction_rate = (positive / total * 100) if total > 0 else 0
    
    output = f"\n7. USER FEEDBACK\n"
    output += f"   Total feedback: {total}\n"
    output += f"   👍 Positive: {positive} ({positive/total*100:.1f}%)\n"
    output += f"   👎 Negative: {negative} ({negative/total*100:.1f}%)\n"
    output += f"   Satisfaction Rate: {satisfaction_rate:.1f}%\n\n"
    
    # Find queries with negative feedback
    negative_messages = [e['message_id'] for e in feedback_entries if e['feedback'] == 'negative']
    
    if negative_messages:
        output += "   Queries with negative feedback (need review):\n"
        # Match message IDs to original queries
        query_map = {e.get('message_id'): e.get('query') for e in entries if e.get('message_id')}
        
        for msg_id in negative_messages[:10]:  # Show top 10
            query = query_map.get(msg_id, 'Unknown query')
            output += f"   - \"{query}\"\n"
    
    return output

# Add to main analysis function
sections.append(analyze_feedback(entries))
```

---

### Step 4: Docker Configuration

**Update docker-compose.yml if needed:**

```yaml
services:
  rasa-actions:
    # ... existing config
    ports:
      - "5055:5055"  # Already exposed
    volumes:
      - ./chatbot/rasa/logs:/app/logs  # Ensure logs volume mounted
```

**No changes needed** - current setup already supports this.

---

## Testing Plan

### Test 1: UI Feedback Buttons

1. Send message to chatbot
2. Verify thumbs up/down buttons appear
3. Click thumbs up → button should highlight green
4. Verify button becomes disabled after click
5. Refresh page → feedback state should persist (optional enhancement)

### Test 2: Backend Logging

```bash
# Send test feedback
curl -X POST http://localhost:5055/feedback \
  -H "Content-Type: application/json" \
  -d '{
    "message_id": "msg_test_123",
    "feedback": "positive",
    "timestamp": "2025-12-30T10:00:00Z"
  }'

# Verify logged
tail -1 /home/ubuntu/humanergy/chatbot/rasa/logs/query_log.jsonl | jq
```

Expected output:
```json
{
  "type": "feedback",
  "message_id": "msg_test_123",
  "feedback": "positive",
  "timestamp": "2025-12-30T10:00:00Z",
  "recorded_at": "2025-12-30T10:00:01.234Z"
}
```

### Test 3: Analysis Integration

```bash
# Run analysis
python3 scripts/analyze_query_logs.py 7

# Check for section 7: USER FEEDBACK
# Should show positive/negative counts
```

---

## Deployment Steps

1. **Update UI:**
   ```bash
   cd /home/ubuntu/humanergy/chatbot
   # Edit ChatBotUI.tsx with feedback buttons
   npm run build
   ```

2. **Update Backend:**
   ```bash
   cd /home/ubuntu/humanergy
   # Edit chatbot/rasa/actions/actions.py
   docker compose build rasa-actions --no-cache
   docker compose restart rasa-actions
   ```

3. **Update Analysis:**
   ```bash
   # Edit scripts/analyze_query_logs.py
   chmod +x scripts/analyze_query_logs.py
   ```

4. **Test:**
   ```bash
   # Test feedback endpoint
   curl -X POST http://localhost:5055/feedback \
     -H "Content-Type: application/json" \
     -d '{"message_id": "test", "feedback": "positive", "timestamp": "2025-12-30T10:00:00Z"}'
   
   # Verify in UI
   # Open http://localhost:3001/chat
   ```

---

## Success Metrics

**Week 1:**
- ✅ Feedback buttons visible on all bot messages
- ✅ At least 10 feedback submissions logged
- ✅ Analysis tool shows feedback section

**Month 1:**
- ✅ Satisfaction rate ≥80%
- ✅ Negative feedback patterns identified
- ✅ At least 3 improvements made based on feedback

**Long-term:**
- ✅ Satisfaction rate ≥90%
- ✅ Feedback-driven improvements documented
- ✅ Correlation between feedback and query success

---

## Future Enhancements

### Priority 1 (Next Phase)
- [ ] Feedback comments: "Why was this not helpful?"
- [ ] Feedback analytics dashboard
- [ ] Auto-notify team on multiple negative feedbacks

### Priority 2 (Later)
- [ ] Sentiment analysis on user messages
- [ ] A/B testing different responses
- [ ] Feedback-driven Q&A ranking

### Priority 3 (Nice to have)
- [ ] User session tracking
- [ ] Personalized responses based on history
- [ ] Chatbot improvement suggestions via ML

---

## Benefits

1. **Data-Driven Improvements:** Know exactly which responses need work
2. **User Engagement:** Users feel heard and contribute to improvements
3. **Quality Metrics:** Measurable satisfaction rate over time
4. **Priority Setting:** Focus on frequently disliked responses first
5. **Validation:** Confirm improvements actually help users

---

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Low feedback rate | Can't identify issues | Make buttons prominent, add tooltip |
| Feedback gaming | Bad data | Rate limiting, user tracking |
| Storage bloat | Log files too large | Rotate logs, aggregate feedback data |
| Privacy concerns | User trust issues | Don't log PII, clear privacy policy |

---

## Estimated Timeline

| Task | Time | Owner |
|------|------|-------|
| UI implementation | 1 hour | Frontend Dev |
| Backend endpoint | 1 hour | Backend Dev |
| Analysis tool update | 30 min | Data Team |
| Testing | 30 min | QA |
| Documentation | 30 min | Tech Writer |
| **Total** | **3.5 hours** | Team |

---

## Approval Checklist

- [ ] UI mockup approved
- [ ] Backend design reviewed
- [ ] Privacy compliance verified
- [ ] Testing plan approved
- [ ] Deployment plan ready
- [ ] Rollback plan documented

---

**Status:** ✅ Design Complete - Ready for Implementation  
**Next Step:** Assign to development team and schedule implementation

**Priority:** Medium (can be done in parallel with other improvements)

---

## Quick Start (For Developers)

```bash
# 1. Edit UI
vim /home/ubuntu/humanergy/chatbot/ChatBotUI.tsx
# Add feedback buttons (see Step 1)

# 2. Edit Backend
vim /home/ubuntu/humanergy/chatbot/rasa/actions/actions.py
# Add feedback endpoint (see Step 2)

# 3. Edit Analysis
vim /home/ubuntu/humanergy/scripts/analyze_query_logs.py
# Add feedback analysis (see Step 3)

# 4. Build & Deploy
cd /home/ubuntu/humanergy
docker compose build rasa-actions --no-cache
docker compose restart rasa-actions

# 5. Test
curl -X POST http://localhost:5055/feedback \
  -H "Content-Type: application/json" \
  -d '{"message_id": "test", "feedback": "positive", "timestamp": "2025-12-30T10:00:00Z"}'
```

---

**Last Updated:** 2025-12-30  
**Version:** 1.0
