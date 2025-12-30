# 🤝 Handoff: Knowledge Base Chatbot Expansion

**Date:** 2024-12-30  
**Status:** Ready for implementation  
**Previous Session:** Discovery and planning complete

---

## 🎯 The Goal

Expand the existing RASA text chatbot (currently ISO 50001-only) to answer questions about **all Humanergy platform features** - portal pages, Grafana dashboards, OVOS voice commands, and technical concepts.

Users should be able to ask things like:
- "What is the baseline page for?"
- "What can I ask the voice assistant?"
- "What is the difference between baseline and forecasting?"
- "What does the SOTA ISO 50001 dashboard show?"

---

## 📁 Key Files to Review

### The Chatbot System
| File | Purpose |
|------|---------|
| `/home/ubuntu/humanergy/chatbot/rasa/qa_data.json` | Q&A knowledge base (JSON format) |
| `/home/ubuntu/humanergy/chatbot/rasa/actions/actions.py` | Keyword routing + answer retrieval logic |
| `/home/ubuntu/humanergy/chatbot/server/index.js` | Express proxy to Rasa |

### Portal Features to Document
| File | What it shows |
|------|---------------|
| `/home/ubuntu/humanergy/portal/public/js/sidebar.js` | All portal navigation/pages |
| `/home/ubuntu/humanergy/analytics/ui/templates/*.html` | Analytics page templates |
| `/home/ubuntu/humanergy/grafana/dashboards/*.json` | Grafana dashboard definitions |

### OVOS Voice Capabilities
| File | Purpose |
|------|---------|
| `/home/ubuntu/ovos-llm/enms-ovos-skill/enms_ovos_skill/__init__.py` | All voice intent handlers |

### Planning Document (my analysis)
| File | Contains |
|------|----------|
| `/home/ubuntu/humanergy/docs/KNOWLEDGE-BASE-EXPANSION-PLAN.md` | Detailed discovery findings, proposed categories, implementation approach |

---

## 💡 Context

**Current state:**
- RASA chatbot works and is integrated into portal via floating widget
- Knowledge base has 19 ISO 50001 categories (~10K lines of Q&A)
- System uses keyword matching + fuzzy search to find answers

**What's missing:**
- No documentation about Humanergy-specific features
- Users can't ask about portal pages, dashboards, or voice commands
- Technical concepts (EnPI, baseline, forecast) not explained in platform context

---

## 🔍 Suggested Starting Points

1. **Understand existing system**: Review `qa_data.json` format and `actions.py` logic
2. **Identify what to document**: Browse portal pages, Grafana dashboards, OVOS handlers
3. **Start small**: Add one test category, verify it works
4. **Expand**: Create content for remaining features

---

## ⚠️ Notes

- The chatbot runs in Docker (`docker-compose.yml` in humanergy/)
- Testing: Use the chat widget on the portal or API at `/api/chatbot/api/rasa/webhook`
- The planning doc has estimated ~35 new categories and 8-12 hours work

---

**The detailed plan and discovery notes are in:**  
[KNOWLEDGE-BASE-EXPANSION-PLAN.md](KNOWLEDGE-BASE-EXPANSION-PLAN.md)

Good luck! 🚀
