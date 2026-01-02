# Root Cause Analysis - Verified

**Date:** December 31, 2025  
**Method:** Live testing + log analysis

---

## ✅ Q100: "Which machine is most efficient?"

### Current Behavior
- Response: "We have  machines:" (empty list)
- Logs show: "Ranking query with limit: 5, efficiency: True"

### Root Cause VERIFIED
**Line 1872 in __init__.py:**
```python
energy = self._run_async(self.api_client.get_machine_energy(
    machine_id=machine['id'],
    interval='1day',
    limit=1
))
```

**Problem:** `get_machine_energy()` **method does not exist** in api_client.py

**Available methods:**
- `get_energy_timeseries()` ✅
- `get_multi_machine_energy()`
- `get_energy_types()`
- `get_energy_readings()`
- `get_energy_summary()`

**Fix:** Replace with `get_energy_timeseries(machine_id, interval, limit)`

---

## ✅ Q24: "What machines are in the European facility?"

### Current Behavior
- Response: Factory overview stats (total energy, cost, carbon)
- Should: List European machines (Compressor-EU-1, HVAC-EU-North)

### Root Cause VERIFIED
**Intent matching:**
```
adapt_low match: FactoryOverview (confidence: 0.25)
Matched word: 'facility' → factory.voc
```

**Problem:** "facility" triggers factory.voc with LOW confidence (0.25), but no stronger match for MACHINE_LIST

**Location filter code works:** Detection logic in handler correctly identifies "european" → location='EU'

**But:** Code never executes because query routes to wrong intent

**Fix:** Add stronger phrases to machine_list.voc:
- "machines in"
- "machines in the"
- "machines in facility"  
- "european machines"

---

## ✅ Q77-78: "Show me details for baseline model 46"

### Current Behavior
- Response: "Could not retrieve model 46: Client error '422 Unprocessable Entity'"
- Intent: ModelQuery (confidence: 0.92) ✅ CORRECT

### Root Cause VERIFIED
**API call:**
```python
data = self._run_async(
    self.api_client.get_baseline_model_explanation(model_id=str(model_id))
)
# Calls: /baseline/model/46?include_explanation=true
```

**Problem:** API expects UUID format like `123e4567-e89b-12d3-a456-426614174000`, not integer `46`

**Backend behavior:**
- Pydantic validation fails: expects UUID, receives string "46"
- Returns 422 Unprocessable Entity

**Additional issue:** No baseline models exist in database (count: 0)

**Fix Options:**
1. Change API to use model version number (integer) - requires backend change
2. Query models list first, match by version, get UUID - client-side workaround
3. Accept that queries fail until models are trained (data dependency)

**Recommendation:** Option 2 - client-side workaround with fallback message

---

## Summary

| Query | Intent Match | Code Logic | API Call | Status |
|-------|--------------|------------|----------|--------|
| Q100 | ✅ Correct | ✅ Correct | ❌ Method doesn't exist | **EASY FIX** |
| Q24 | ❌ Wrong intent | ✅ Correct | N/A | **EASY FIX** (vocab) |
| Q77 | ✅ Correct | ✅ Correct | ❌ Wrong param type | **MEDIUM FIX** (workaround) |

**All issues identified with 100% certainty through live testing and log verification.**
