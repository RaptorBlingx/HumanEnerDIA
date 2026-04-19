# Rasa Chatbot Manual Acceptance Checklist

Use the live portal path for all checks:

```bash
curl -s http://localhost:8080/api/chatbot/api/rasa/webhook \
  -H 'Content-Type: application/json' \
  -d '{"sender":"manual-check","message":"What can you help me with?"}'
```

This path matches the portal widget flow:

`portal/public/js/chatbot-widget.js` -> `/api/chatbot/api/rasa/webhook` -> `chatbot/server/index.js` -> Rasa

## Scope and identity

- Prompt: `What can you help me with?`
  Expected: answer mentions ISO 50001, HumanEnerDIA guidance, reports, troubleshooting, and sends live operational questions to OVOS or live dashboards.

- Prompt: `What is OVOS and how is it different from this chatbot?`
  Expected: clear split between text knowledge/help and live operational voice queries.

## Quick-reply coverage

- Prompt: `How do I get started with HumanEnerDIA?`
  Expected: onboarding answer stays product-oriented and readable.

- Prompt: `What is ISO 50001?`
  Expected: concise standard explanation, not a mismatched boilerplate answer.

- Prompt: `Why is my Grafana dashboard not showing data?`
  Expected: focused troubleshooting answer without unrelated stitched content.

- Prompt: `What is an energy baseline?`
  Expected: concise explanation of the baseline as a reference point for expected energy performance.

## Portal how-to checks

- Prompt: `How do I generate a report?`
  Expected: report answer describes the current monthly PDF workflow using factory, year, and month.

- Prompt: `What is the Reports page?`
  Expected: report-page answer describes the monthly PDF report flow and avoids unsupported claims about report templates or scheduled email.

- Prompt: `What is the anomaly page?`
  Expected: anomaly-page answer focuses on reviewing detected events with filters, severity, and investigation support.

- Prompt: `How do I customize anomaly thresholds?`
  Expected: answer explains that threshold tuning is typically an admin or backend concern, not a guaranteed end-user menu.

## Live-query boundary checks

- Prompt: `What is the current energy of Compressor-1?`
  Expected: redirect to OVOS or live dashboards. Do not invent live values.

- Prompt: `Which machine is using the most electricity right now?`
  Expected: redirect to OVOS or live dashboards. Do not guess.

- Prompt: `Are there any active alerts right now?`
  Expected: redirect to OVOS or live dashboards. Do not claim current alert state.

## Acceptance notes

- Portal and troubleshooting answers should stay single-topic and not stitch together unrelated extra paragraphs.
- The chatbot should not promise settings screens, tabs, exports, or automation flows that are not clearly available in the current portal.
- Any request for current machine state, current energy, ranking, or active alerts should be treated as an OVOS or live-dashboard query.