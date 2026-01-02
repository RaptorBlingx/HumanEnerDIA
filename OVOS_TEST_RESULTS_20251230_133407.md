# OVOS Systematic Test Results

**Date:** Tue Dec 30 13:34:07 UTC 2025
**Total Queries:** 118
**Method:** REST Bridge (curl localhost:5000/query)

---


## Query 1: `Is the energy system online?`

✅ GOT RESPONSE (5s)

**Response:** The energy management system is healthy and operational.

**Intent Match:**
```
2025-12-30 13:34:08.276 - skills - ovos_core.intent_services.service:handle_utterance:471 - INFO - adapt_high match (en-US): IntentHandlerMatch(match_type='enms-ovos-skill.a plus engineering:SystemHealth', match_data={'intent_type': 'enms-ovos-skill.a plus engineering:SystemHealth', 'enms_ovos_skill_a_plus_engineeringhealth_check': 'energy system online', 'target': None, 'confidence': 0.7407407407407407, '__tags__': [{'start_token': 2, 'entities': [{'key': 'energy system online', 'match': 'energy system online', 'data': [('energy system online', 'enms_ovos_skill_a_plus_engineeringHealth_Check')], 'confidence': 1.0}], 'confidence': 1.0, 'end_token': 4, 'match': 'energy system online', 'key': 'energy system online', 'from_context': False}], 'utterance': 'Is the energy system online'}, skill_id='enms-ovos-skill.a plus engineering', utterance='Is the energy system online', updated_session=None)
```
Status: PASS

---

## Query 2: `Check system health`

✅ GOT RESPONSE (6s)

**Response:** The energy management system is healthy and operational.

**Intent Match:**
```
2025-12-30 13:34:15.499 - skills - ovos_core.intent_services.service:handle_utterance:471 - INFO - adapt_medium match (en-US): IntentHandlerMatch(match_type='enms-ovos-skill.a plus engineering:SystemHealth', match_data={'intent_type': 'enms-ovos-skill.a plus engineering:SystemHealth', 'enms_ovos_skill_a_plus_engineeringhealth_check': 'check system', 'target': None, 'confidence': 0.47368421052631576, '__tags__': [{'start_token': 0, 'entities': [{'key': 'check system', 'match': 'check system', 'data': [('check system', 'enms_ovos_skill_a_plus_engineeringHealth_Check')], 'confidence': 1.0}], 'confidence': 1.0, 'end_token': 1, 'match': 'check system', 'key': 'check system', 'from_context': False}], 'utterance': 'Check system health'}, skill_id='enms-ovos-skill.a plus engineering', utterance='Check system health', updated_session=None)
```
Status: PASS

---

## Query 3: ``

❌ TIMEOUT (no response after 30s)
Status: TIMEOUT

**Logs:**
```
2025-12-30 13:34:22.102 - skills - ovos_core.intent_services.service:handle_utterance:450 - INFO - Parsing utterance: ['']
2025-12-30 13:34:22.103 - skills - ovos_core.intent_services.service:get_pipeline_matcher:214 - ERROR - Unknown pipeline matcher: ovos-ocp-pipeline-plugin-high
2025-12-30 13:34:22.103 - skills - ovos_core.intent_services.service:get_pipeline_matcher:214 - ERROR - Unknown pipeline matcher: ovos-ocp-pipeline-plugin-medium
2025-12-30 13:34:22.104 - skills - ovos_core.intent_services.service:get_pipeline_matcher:214 - ERROR - Unknown pipeline matcher: ovos-common-query-pipeline-plugin
2025-12-30 13:34:22.104 - skills - ovos_core.intent_services.service:get_pipeline:236 - WARNING - Requested some invalid pipeline components! filtered: ['ocp_high', 'ocp_medium', 'common_qa']
```

---

## Query 4: `Is the database connected?`

❌ TIMEOUT (no response after 30s)
Status: TIMEOUT

**Logs:**
```
2025-12-30 13:34:54.247 - skills - ovos_core.intent_services.service:handle_utterance:450 - INFO - Parsing utterance: ['Is the database connected']
2025-12-30 13:34:54.248 - skills - ovos_core.intent_services.service:get_pipeline_matcher:214 - ERROR - Unknown pipeline matcher: ovos-ocp-pipeline-plugin-high
2025-12-30 13:34:54.249 - skills - ovos_core.intent_services.service:get_pipeline_matcher:214 - ERROR - Unknown pipeline matcher: ovos-ocp-pipeline-plugin-medium
2025-12-30 13:34:54.249 - skills - ovos_core.intent_services.service:get_pipeline_matcher:214 - ERROR - Unknown pipeline matcher: ovos-common-query-pipeline-plugin
2025-12-30 13:34:54.250 - skills - ovos_core.intent_services.service:get_pipeline:236 - WARNING - Requested some invalid pipeline components! filtered: ['ocp_high', 'ocp_medium', 'common_qa']
```

---

## Query 5: `How many machines are active?`

✅ GOT RESPONSE (5s)

**Response:** There are 8 machines currently active out of 8 total machines.

**Intent Match:**
```
2025-12-30 13:35:26.932 - skills - ovos_core.intent_services.service:handle_utterance:471 - INFO - adapt_high match (en-US): IntentHandlerMatch(match_type='enms-ovos-skill.a plus engineering:MachineStatus', match_data={'intent_type': 'enms-ovos-skill.a plus engineering:MachineStatus', 'enms_ovos_skill_a_plus_engineeringmachine_status': 'how many machines are active', 'target': None, 'confidence': 1.0, '__tags__': [{'start_token': 0, 'entities': [{'key': 'how many machines are active', 'match': 'how many machines are active', 'data': [('how many machines are active', 'enms_ovos_skill_a_plus_engineeringMachine_Status'), ('how many machines are active', 'enms_ovos_skill_a_plus_engineeringSystem_Query')], 'confidence': 1.0}], 'confidence': 1.0, 'end_token': 4, 'match': 'how many machines are active', 'key': 'how many machines are active', 'from_context': False}], 'utterance': 'How many machines are active'}, skill_id='enms-ovos-skill.a plus engineering', utterance='How many machines are active', updated_session=None)
```
Status: PASS

---

## Query 6: `How much energy are we using today?`

✅ GOT RESPONSE (5s)

**Response:** Factory consumed 4219.9 kilowatt-hours today

**Intent Match:**
```
2025-12-30 13:35:34.063 - skills - ovos_core.intent_services.service:handle_utterance:471 - INFO - adapt_low match (en-US): IntentHandlerMatch(match_type='enms-ovos-skill.a plus engineering:EnergyQuery', match_data={'intent_type': 'enms-ovos-skill.a plus engineering:EnergyQuery', 'enms_ovos_skill_a_plus_engineeringenergy_metric': 'how much energy', 'target': None, 'confidence': 0.29411764705882354, '__tags__': [{'start_token': 0, 'entities': [{'key': 'how much energy', 'match': 'how much energy', 'data': [('how much energy', 'enms_ovos_skill_a_plus_engineeringEnergy_Metric')], 'confidence': 1.0}], 'confidence': 1.0, 'end_token': 2, 'match': 'how much energy', 'key': 'how much energy', 'from_context': False}], 'utterance': 'How much energy are we using today'}, skill_id='enms-ovos-skill.a plus engineering', utterance='How much energy are we using today', updated_session=None)
```
Status: PASS

---

## Query 7: ``

❌ TIMEOUT (no response after 30s)
Status: TIMEOUT

**Logs:**
```
2025-12-30 13:35:40.801 - skills - ovos_core.intent_services.service:handle_utterance:450 - INFO - Parsing utterance: ['']
2025-12-30 13:35:40.805 - skills - ovos_core.intent_services.service:get_pipeline_matcher:214 - ERROR - Unknown pipeline matcher: ovos-ocp-pipeline-plugin-high
2025-12-30 13:35:40.808 - skills - ovos_core.intent_services.service:get_pipeline_matcher:214 - ERROR - Unknown pipeline matcher: ovos-ocp-pipeline-plugin-medium
2025-12-30 13:35:40.809 - skills - ovos_core.intent_services.service:get_pipeline_matcher:214 - ERROR - Unknown pipeline matcher: ovos-common-query-pipeline-plugin
2025-12-30 13:35:40.812 - skills - ovos_core.intent_services.service:get_pipeline:236 - WARNING - Requested some invalid pipeline components! filtered: ['ocp_high', 'ocp_medium', 'common_qa']
```

---

## Query 8: `How much is energy costing us?`

✅ GOT RESPONSE (6s)

**Response:** Total energy cost is $164257.8. Daily cost rate is $839.86.

**Intent Match:**
```
2025-12-30 13:36:13.454 - skills - ovos_core.intent_services.service:handle_utterance:471 - INFO - adapt_high match (en-US): IntentHandlerMatch(match_type='enms-ovos-skill.a plus engineering:CostAnalysis', match_data={'intent_type': 'enms-ovos-skill.a plus engineering:CostAnalysis', 'enms_ovos_skill_a_plus_engineeringcost_metric': 'how much is energy costing us', 'target': None, 'confidence': 1.0, '__tags__': [{'start_token': 0, 'entities': [{'key': 'how much is energy costing us', 'match': 'how much is energy costing us', 'data': [('how much is energy costing us', 'enms_ovos_skill_a_plus_engineeringCost_Metric')], 'confidence': 1.0}], 'confidence': 1.0, 'end_token': 5, 'match': 'how much is energy costing us', 'key': 'how much is energy costing us', 'from_context': False}], 'utterance': 'How much is energy costing us'}, skill_id='enms-ovos-skill.a plus engineering', utterance='How much is energy costing us', updated_session=None)
```
Status: PASS

---

## Query 9: ``

