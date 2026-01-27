# Forecast Page UI Enhancement - Implementation Plan

**Goal:** Transform the Forecast page from ambiguous/vague to clear, informative, and user-friendly for non-technical users.
**Design Pivot:** Shifted immediately to "Phase 5" (Industrial Design System) via `forecast2.html`.

**Start Date:** 2026-01-26
**Status:** In Progress (Redoing Phase 1 with New Design)

---

## 📅 Implementation Roadmap

### Phase 1 (Re-Do): Complete Redesign & Core Features (Active)
**Goal:** Replace old UI with `forecast2.html` using Industrial Design System + Implement "Phase 1" functional requirements.

- [x] Create `forecast2.html` with sidebar layout (matches `baseline.html`)
- [x] Implement "Industrial Card" styling
- [x] Add Contextual Tooltips (What is "Load"? What is "Horizon"?)
- [x] Display Tariff Info in clearer format
- [x] Improve Prophet Feature visualization (as badges/tags)
- [x] Add Quality Indicators (Badges for "Good/Fair" MAPE)
- [x] Update Python route (`/ui/forecast`) to serve `forecast2.html`
- [ ] Verify functionality (Manual Test)

### Phase 2: Enhanced Model Feedback (Next)
**Goal:** Better insights into *why* a model is good/bad.
- [ ] Show Training Period dates
- [ ] Visualize Feature Importance (if API supports it)
- [ ] Historical Accuracy tracking

### Phase 3: Interactive Forecasting
**Goal:** Let users play "What If" scenarios.
- [ ] Compare multiple scenarios on one chart
- [ ] Adjust "Expected Load" dynamically

### Phase 4: Scheduling & Optimization
**Goal:** Make the scheduling tool more robust.
- [ ] Gantt Chart visualization for suggested slots
- [ ] Savings calculator (Current Slot Cost vs Optimal Slot Cost)

---

## Technical Notes
- **File:** `analytics/ui/templates/forecast2.html`
- **Route:** `analytics/api/routes/ui_routes.py` -> `forecast_ui`
- **Design System:** Custom CSS variables (`--bg-surface`, `--space-6`) + Bootstrap 5 + Bootstrap Icons.
- **Charts:** Chart.js 3.x
