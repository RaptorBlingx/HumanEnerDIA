# 📚 Humanergy Knowledge Base Expansion Plan

**Created:** 2025-01-XX  
**Status:** Planning Phase  
**Priority:** P2 from WASABI Proposal

---

## 🎯 Objective

Expand the existing RASA chatbot knowledge base from ISO 50001-only content to cover:
- All Humanergy portal features
- OVOS voice assistant capabilities  
- Grafana dashboards
- Node-RED flows
- Analytics pages (Baseline, Forecast, KPIs, Anomalies)
- Technical concepts (what is EnPI, SEC, Load Factor, etc.)

---

## 📊 Current State Analysis

### Existing RASA Chatbot Architecture

```
chatbot/
├── rasa/
│   ├── qa_data.json          # 10,243 lines, 19 ISO 50001 categories
│   ├── actions/
│   │   └── actions.py        # ActionRetrieveAnswer with keyword routing
│   ├── endpoints.yml         # Points to rasa-actions:5055
│   └── models/               # Trained model
├── server/
│   └── index.js              # Express proxy to Rasa (port 5006)
└── ChatBotUI.tsx             # React frontend
```

### Current Q&A Categories (19 ISO 50001 topics)
1. `ask_action_plans`
2. `ask_benchmarking`
3. `ask_checking`
4. `ask_definitions`
5. `ask_energy_baseline`
6. `ask_energy_planning`
7. `ask_energy_policy`
8. `ask_enpi`
9. `ask_general_info`
10. `ask_implementation`
11. `ask_internal_audit`
12. `ask_iso_standards`
13. `ask_management_responsibility`
14. `ask_management_review`
15. `ask_pdca`
16. `ask_scope`
17. `ask_terms_definitions`
18. `process`
19. `requirement`

### How Q&A Retrieval Works

1. User sends message → Rasa classifies intent (definition/purpose/process/requirement)
2. `ActionRetrieveAnswer` in `actions.py` extracts keywords
3. Maps keywords → topic via `keyword_to_topic` dictionary
4. Searches `qa_data.json` for best matching Q&A pair using:
   - Fuzzy string matching (SequenceMatcher)
   - Keyword scoring with important terms
   - Question type matching (what/how/when)
5. Returns best answer or falls back to domain response

---

## 🗂️ Proposed New Categories

### Group 1: Portal Features
| Category | Description | Sample Questions |
|----------|-------------|------------------|
| `ask_portal_dashboard` | Main dashboard features | "What can I see on the dashboard?" |
| `ask_portal_reports` | Reports page functionality | "How do I download reports?" |
| `ask_portal_baseline` | Baseline analysis page | "What is the baseline page for?" |
| `ask_portal_forecast` | Forecasting page | "What is Optimal Load Scheduling?" |
| `ask_portal_kpi` | KPIs page | "What KPIs can I track?" |
| `ask_portal_anomaly` | Anomaly detection page | "How does anomaly detection work?" |

### Group 2: Visualizations
| Category | Description | Sample Questions |
|----------|-------------|------------------|
| `ask_viz_sankey` | Sankey diagram | "What does the Sankey diagram show?" |
| `ask_viz_heatmap` | Anomaly heatmap | "How to read the heatmap?" |
| `ask_viz_comparison` | Machine comparison | "How to compare machines?" |
| `ask_viz_model_performance` | ML model metrics | "What is R² score?" |

### Group 3: Grafana Dashboards
| Category | Description | Sample Questions |
|----------|-------------|------------------|
| `ask_grafana_iso50001` | SOTA ISO 50001 EnPI | "What is SOTA ISO 50001 EnPI dashboard?" |
| `ask_grafana_overview` | Factory Overview | "What shows in Factory Overview?" |
| `ask_grafana_anomaly` | Anomaly Detection | "Where to see anomalies in Grafana?" |
| `ask_grafana_cost` | Cost Analytics | "How to see energy costs?" |
| `ask_grafana_executive` | Executive Summary | "What's in Executive Summary?" |
| `ask_grafana_machine_health` | Machine Health | "Where to check machine health?" |
| `ask_grafana_ml` | ML Performance | "How to monitor ML models?" |
| `ask_grafana_operational` | Operational Efficiency | "What is operational efficiency dashboard?" |
| `ask_grafana_predictive` | Predictive Analytics | "What predictions does Grafana show?" |
| `ask_grafana_realtime` | Real-time Production | "Where to see real-time data?" |

### Group 4: OVOS Voice Commands
| Category | Description | Sample Questions |
|----------|-------------|------------------|
| `ask_ovos_capabilities` | What OVOS can do | "What can I ask the voice assistant?" |
| `ask_ovos_energy` | Energy queries | "How to ask about energy consumption?" |
| `ask_ovos_status` | Status queries | "How to check machine status by voice?" |
| `ask_ovos_reports` | Voice reports | "Can I get reports by voice?" |
| `ask_ovos_forecast` | Voice forecasting | "How to ask for forecasts?" |
| `ask_ovos_kpi` | Voice KPI queries | "How to get KPIs by voice?" |

### Group 5: Technical Concepts
| Category | Description | Sample Questions |
|----------|-------------|------------------|
| `ask_concept_baseline` | Energy baseline concept | "What is energy baseline?" |
| `ask_concept_enpi` | EnPI explanation | "What is EnPI and how is it calculated?" |
| `ask_concept_sec` | SEC (Specific Energy) | "What is Specific Energy Consumption?" |
| `ask_concept_loadfactor` | Load Factor | "What is load factor?" |
| `ask_concept_peakdemand` | Peak Demand | "What is peak demand?" |
| `ask_concept_seu` | Significant Energy Uses | "What are SEUs?" |
| `ask_concept_arima` | ARIMA forecasting | "What is ARIMA model?" |
| `ask_concept_anomaly` | Anomaly detection ML | "How does anomaly detection work?" |

### Group 6: System Integration
| Category | Description | Sample Questions |
|----------|-------------|------------------|
| `ask_nodered` | Node-RED flows | "What is Node-RED used for?" |
| `ask_mqtt` | MQTT messaging | "What is MQTT?" |
| `ask_timescaledb` | Time-series database | "How is data stored?" |
| `ask_simulator` | Factory simulator | "What does the simulator do?" |

---

## 📝 Implementation Phases

### Phase 1: Test Infrastructure (1-2 hours)
**Goal:** Verify we can add new categories without breaking existing chatbot

1. Add 1 test category: `ask_humanergy_test`
2. Add 5 sample Q&A pairs to `qa_data.json`
3. Add keywords to `keyword_to_topic` in `actions.py`
4. Add domain response fallback
5. Test via portal widget

**Verification:**
- Ask: "What is Humanergy?" → Should return test answer
- Ask: "What is EnPI?" → Should still work (existing ISO 50001)

### Phase 2: Portal Features (2-3 hours)
**Goal:** Document all portal pages

**Content per category (~10 Q&A pairs each):**
- What is this page for?
- What information does it show?
- How to use the main features?
- What do the charts/metrics mean?
- Common use cases
- Tips and best practices

**Pages to document:**
1. Dashboard (`/`)
2. Baseline (`/api/analytics/ui/baseline`)
3. Anomaly (`/api/analytics/ui/anomaly`)
4. KPIs (`/api/analytics/ui/kpi`)
5. Forecast (`/api/analytics/ui/forecast`)
6. Reports (`/reports.html`)
7. Visualizations (Sankey, Heatmap, Comparison, Model Performance)

### Phase 3: Grafana Dashboards (2-3 hours)
**Goal:** Document all SOTA dashboards

**11 dashboards to document:**
1. SOTA-iso50001-enpi
2. SOTA-factory-overview
3. SOTA-anomaly-detection
4. SOTA-cost-analytics
5. SOTA-executive-summary
6. SOTA-machine-health
7. SOTA-ml-performance
8. SOTA-operational-efficiency
9. SOTA-predictive-analytics
10. SOTA-realtime-production
11. SOTA-environmental-impact

**Content per dashboard (~8 Q&A pairs each):**
- What does this dashboard show?
- What panels are included?
- How to filter/interact?
- What time ranges are available?
- Key metrics explained

### Phase 4: OVOS Voice Capabilities (1-2 hours)
**Goal:** Document all 25 voice commands

**OVOS Handlers to document:**
1. Energy queries
2. System health
3. Machine status
4. Factory overview
5. Anomaly detection
6. Rankings
7. Machine list
8. Comparison
9. Cost analysis
10. Forecasting
11. Baseline queries
12. Train baseline
13. Baseline models
14. Baseline explanation
15. SEUs (Significant Energy Uses)
16. KPIs
17. Performance
18. Production
19. Power queries
20. Load factor
21. Peak demand
22. SEC (Specific Energy Consumption)
23. Reports (PDF generation)
24. Help command

**Content per handler (~5 Q&A pairs each):**
- What can I say to trigger this?
- Example phrases
- What information will I get?
- Tips for best results

### Phase 5: Technical Concepts (2 hours)
**Goal:** Explain ISO 50001 concepts in Humanergy context

**Concepts to document:**
- Energy Baseline vs Forecasting (difference)
- EnPI calculation
- SEC formula
- Load Factor meaning
- Peak Demand importance
- SEU identification
- ARIMA/Prophet models
- Anomaly detection algorithms
- CUSUM monitoring
- Real-time vs aggregated data

---

## 🔧 Technical Implementation Details

### 1. Modify `qa_data.json`

```json
{
  "ask_action_plans": [...],  // Existing
  ...
  "ask_portal_baseline": [    // NEW
    [
      "What is the baseline page?",
      "The Baseline page shows energy consumption patterns and ML model predictions for each machine. It helps you understand normal energy usage and identify deviations."
    ],
    [
      "What is the difference between baseline and forecast?",
      "Baseline shows what energy consumption SHOULD be based on current conditions (temperature, production). Forecast predicts what consumption WILL be in the future using time-series analysis."
    ]
  ],
  "ask_ovos_capabilities": [  // NEW
    [
      "What can I ask the voice assistant?",
      "You can ask about energy consumption, machine status, KPIs, forecasts, anomalies, rankings, and even generate PDF reports. Try: 'How much energy did the factory use today?' or 'What's the status of Compressor-1?'"
    ]
  ]
}
```

### 2. Update `keyword_to_topic` in `actions.py`

```python
keyword_to_topic = {
    # Existing ISO 50001 keywords...
    
    # Portal Features
    "baseline page": "ask_portal_baseline",
    "baseline analysis": "ask_portal_baseline",
    "forecast page": "ask_portal_forecast",
    "forecasting page": "ask_portal_forecast",
    "optimal load": "ask_portal_forecast",
    "load scheduling": "ask_portal_forecast",
    "kpi page": "ask_portal_kpi",
    "anomaly page": "ask_portal_anomaly",
    "dashboard": "ask_portal_dashboard",
    
    # Grafana
    "grafana": "ask_grafana_overview",
    "sota dashboard": "ask_grafana_iso50001",
    "iso 50001 dashboard": "ask_grafana_iso50001",
    "executive summary": "ask_grafana_executive",
    
    # OVOS
    "voice assistant": "ask_ovos_capabilities",
    "ovos": "ask_ovos_capabilities",
    "voice command": "ask_ovos_capabilities",
    "what can i ask": "ask_ovos_capabilities",
    
    # Concepts
    "difference between baseline and forecast": "ask_concept_baseline",
    "baseline vs forecast": "ask_concept_baseline",
    ...
}
```

### 3. Add Domain Responses (fallback)

Add to `domain.yml`:
```yaml
responses:
  utter_ask_portal_baseline:
    - text: "The Baseline page analyzes energy consumption patterns using machine learning models."
  utter_ask_ovos_capabilities:
    - text: "The voice assistant can answer questions about energy, status, KPIs, forecasts, and generate reports."
```

---

## 📋 Content Creation Checklist

### Per Category Template
- [ ] Write 8-15 Q&A pairs
- [ ] Include "what is" questions
- [ ] Include "how to" questions
- [ ] Include "where can I find" questions
- [ ] Add practical examples
- [ ] Cross-reference related features
- [ ] Test each Q&A manually

### Quality Criteria
- [ ] Answers are concise (1-3 sentences)
- [ ] Technical terms are explained
- [ ] Links to related categories exist
- [ ] No duplicate Q&A across categories
- [ ] Natural language (not robotic)

---

## 🧪 Testing Strategy

### Unit Tests
```python
# Test new category detection
def test_portal_baseline_category():
    response = chatbot.ask("What is the baseline page?")
    assert "baseline" in response.lower()
    assert "energy" in response.lower()
```

### Integration Tests
1. Test via portal widget
2. Test keyword routing accuracy
3. Test fallback responses
4. Test cross-category questions

### Manual Testing Queries
```
# Portal Features
"What is the baseline page?"
"How do I use the forecast page?"
"What does optimal load scheduling mean?"
"Where can I see KPIs?"

# Grafana
"What is the SOTA ISO 50001 dashboard?"
"Where can I see energy costs?"
"What dashboards are available?"

# OVOS
"What can I ask the voice assistant?"
"How do I check machine status by voice?"
"Can I get a PDF report by voice?"

# Concepts
"What is the difference between baseline and forecasting?"
"How is EnPI calculated?"
"What is load factor?"
```

---

## ⏱️ Timeline Estimate

| Phase | Duration | Deliverable |
|-------|----------|-------------|
| Phase 1: Test | 1-2 hours | Verified add-category workflow |
| Phase 2: Portal | 2-3 hours | 7 portal page categories |
| Phase 3: Grafana | 2-3 hours | 11 dashboard categories |
| Phase 4: OVOS | 1-2 hours | 6 voice capability categories |
| Phase 5: Concepts | 2 hours | 10 technical concept categories |
| **Total** | **8-12 hours** | **~35 new categories, ~300 Q&A pairs** |

---

## 🔄 Maintenance Plan

### Monthly Review
- Add Q&A for new features
- Update outdated answers
- Analyze unanswered queries
- Improve low-confidence matches

### Analytics to Track
- Most asked questions
- Fallback rate (no good match)
- Category distribution
- User satisfaction (if rated)

---

## 📎 Related Documents

- [WASABI Proposal](docs/HumanEnerDIA_WASABI_1st Open Call_Proposal.txt) - Project context
- [copilot-instructions.md](.github/copilot-instructions.md) - Architecture reference
- [OVOS Skill README](../ovos-llm/enms-ovos-skill/README.md) - Voice capabilities

---

## ✅ Next Steps

1. **Immediate:** Review this plan with stakeholder
2. **Phase 1:** Execute test infrastructure (verify we can add categories)
3. **Content Creation:** Start with highest-value categories (OVOS capabilities, Portal features)
4. **Iterate:** Test and refine based on real user queries
