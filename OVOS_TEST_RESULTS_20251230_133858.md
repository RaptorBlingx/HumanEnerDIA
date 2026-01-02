# OVOS Systematic Test Results

**Date:** Tue Dec 30 13:38:58 UTC 2025
**Total Queries:** 118
**Method:** REST Bridge (curl localhost:5000/query)

---


## Query 1: `Is the energy system online?`

**Status:** ✅ GOT RESPONSE (5.043791041s)

**Response:**
The energy management system is healthy and operational.

**Intent Match:**
```
enms-ovos-skill.a plus engineering:SystemHealth 'confidence': 0.7407407407407407
'confidence': 1.0
'confidence': 1.0
```
**Review Status:** PASS

---

## Query 2: `Check system health`

**Status:** ✅ GOT RESPONSE (5.069959211s)

**Response:**
The energy management system is healthy and operational.

**Intent Match:**
```
enms-ovos-skill.a plus engineering:SystemHealth 'confidence': 0.47368421052631576
'confidence': 1.0
'confidence': 1.0
```
**Review Status:** PASS

---

## Query 3: `What's the status of the analytics service?`

**Status:** ❌ TIMEOUT

**Intent Match:**
```
2025-12-30 13:39:13.258 - skills - ovos_core.intent_services.service:get_pipeline_matcher:214 - ERROR - Unknown pipeline matcher: ovos-common-query-pipeline-plugin
```

---

## Query 4: `Is the database connected?`

**Status:** ❌ TIMEOUT

**Intent Match:**
```
2025-12-30 13:39:45.368 - skills - ovos_core.intent_services.service:get_pipeline_matcher:214 - ERROR - Unknown pipeline matcher: ovos-common-query-pipeline-plugin
```

---

## Query 5: `How many machines are active?`

**Status:** ✅ GOT RESPONSE (5.075951645s)

**Response:**
There are 8 machines currently active out of 8 total machines.

**Intent Match:**
```
enms-ovos-skill.a plus engineering:MachineStatus 'confidence': 1.0
'confidence': 1.0
'confidence': 1.0
```
**Review Status:** PASS

---

## Query 6: `How much energy are we using today?`

**Status:** ✅ GOT RESPONSE (5.080068325s)

**Response:**
Factory consumed 4249.1 kilowatt-hours today

**Intent Match:**
```
enms-ovos-skill.a plus engineering:EnergyQuery 'confidence': 0.29411764705882354
'confidence': 1.0
'confidence': 1.0
```
**Review Status:** PASS

---

## Query 7: `What's our current power consumption?`

**Status:** ✅ GOT RESPONSE (5.076955723s)

**Response:**
The factory is currently drawing 295.5 kilowatts with 8 machines active.
Current factory-wide power consumption is 295.5 kilowatts. Average power today: 242.2 kilowatts.
All machines combined are using 295.5 kilowatts right now. 8 of 8 machines are running.
The entire facility is drawing 295.5 kilowatts of power at the moment.

**Intent Match:**
```
enms-ovos-skill.a plus engineering:PowerQuery 'confidence': 0.6944444444444444
'confidence': 1.0
'confidence': 1.0
```
**Review Status:** PASS

---

## Query 8: `How much is energy costing us?`

**Status:** ✅ GOT RESPONSE (5.070624934s)

**Response:**
Total energy cost is $164257.8. Daily cost rate is $839.86.

**Intent Match:**
```
enms-ovos-skill.a plus engineering:CostAnalysis 'confidence': 1.0
'confidence': 1.0
'confidence': 1.0
```
**Review Status:** PASS

---

## Query 9: `What's our carbon footprint?`

**Status:** ✅ GOT RESPONSE (5.077084469s)

**Response:**
Our carbon footprint is 684407.5 kilograms of CO2 total, with 3499.4 kilograms per day.

**Intent Match:**
```
enms-ovos-skill.a plus engineering:FactoryOverview 'confidence': 0.5925925925925926
'confidence': 1.0
'confidence': 1.0
```
**Review Status:** PASS

---

## Query 10: `Give me a factory overview`

**Status:** ✅ GOT RESPONSE (5.072992843s)

**Response:**
The energy management system is healthy and operational.

**Intent Match:**
```
enms-ovos-skill.a plus engineering:SystemHealth 'confidence': 0.4423076923076923
'confidence': 1.0
'confidence': 1.0
```
**Review Status:** PASS

---

## Query 11: `What's our daily energy cost?`

**Status:** ✅ GOT RESPONSE (5.076709938s)

**Response:**
Total energy cost is $164257.8. Daily cost rate is $839.86.

**Intent Match:**
```
enms-ovos-skill.a plus engineering:CostAnalysis 'confidence': 0.39285714285714285
'confidence': 1.0
'confidence': 1.0
```
**Review Status:** PASS

---

## Query 12: `What was the peak power today?`

**Status:** ✅ GOT RESPONSE (5.069497951s)

**Response:**
The factory is currently drawing 263.2 kilowatts with 8 machines active.
Current factory-wide power consumption is 263.2 kilowatts. Average power today: 242.2 kilowatts.
All machines combined are using 263.2 kilowatts right now. 8 of 8 machines are running.
The entire facility is drawing 263.2 kilowatts of power at the moment.

**Intent Match:**
```
enms-ovos-skill.a plus engineering:PowerQuery 'confidence': 0.5517241379310345
'confidence': 1.0
'confidence': 1.0
```
**Review Status:** PASS

---

## Query 13: `What's the average power consumption?`

**Status:** ✅ GOT RESPONSE (5.070661655s)

**Response:**
The factory is currently drawing 221.4 kilowatts with 6 machines active.
Current factory-wide power consumption is 221.4 kilowatts. Average power today: 242.2 kilowatts.
All machines combined are using 221.4 kilowatts right now. 6 of 8 machines are running.
The entire facility is drawing 221.4 kilowatts of power at the moment.

**Intent Match:**
```
enms-ovos-skill.a plus engineering:PowerQuery 'confidence': 0.4722222222222222
'confidence': 1.0
'confidence': 1.0
```
**Review Status:** PASS

---

## Query 14: `Show me aggregated statistics`

**Status:** ❌ TIMEOUT

**Intent Match:**
```
2025-12-30 13:41:22.855 - skills - ovos_core.intent_services.service:get_pipeline_matcher:214 - ERROR - Unknown pipeline matcher: ovos-common-query-pipeline-plugin
```

---

## Query 15: `What are the aggregated stats for this week?`

**Status:** ❌ TIMEOUT

**Intent Match:**
```
2025-12-30 13:41:54.998 - skills - ovos_core.intent_services.service:get_pipeline_matcher:214 - ERROR - Unknown pipeline matcher: ovos-common-query-pipeline-plugin
```

---

## Query 16: `Show aggregated stats for last month`

**Status:** ❌ TIMEOUT

**Intent Match:**
```
2025-12-30 13:42:27.123 - skills - ovos_core.intent_services.service:get_pipeline_matcher:214 - ERROR - Unknown pipeline matcher: ovos-common-query-pipeline-plugin
```

---

## Query 17: `Aggregated stats for today`

**Status:** ❌ TIMEOUT

**Intent Match:**
```
2025-12-30 13:42:59.258 - skills - ovos_core.intent_services.service:get_pipeline_matcher:214 - ERROR - Unknown pipeline matcher: ovos-common-query-pipeline-plugin
```

---

## Query 18: `List all machines`

**Status:** ✅ GOT RESPONSE (5.061106624s)

**Response:**
We have 8 machines: Boiler-1, Compressor-1, Compressor-EU-1, Conveyor-A, HVAC-EU-North, HVAC-Main, Hydraulic-Pump-1, Injection-Molding-1.

**Intent Match:**
```
enms-ovos-skill.a plus engineering:MachineList 'confidence': 1.0
'confidence': 1.0
'confidence': 1.0
```
**Review Status:** PASS

---

## Query 19: `Show me active machines`

**Status:** ✅ GOT RESPONSE (5.065149972s)

**Response:**
8 active machines: Boiler-1, Compressor-1, Compressor-EU-1, Conveyor-A, HVAC-EU-North, HVAC-Main, Hydraulic-Pump-1, Injection-Molding-1

**Intent Match:**
```
enms-ovos-skill.a plus engineering:MachineStatus 'confidence': 0.6086956521739131
'confidence': 1.0
'confidence': 1.0
'confidence': 1.0
'confidence': 1.0
```
**Review Status:** PASS

---

## Query 20: `Find the compressor`

**Status:** ✅ GOT RESPONSE (5.084885584s)

**Response:**
We have 2 machines: Compressor-1, Compressor-EU-1.

**Intent Match:**
```
enms-ovos-skill.a plus engineering:MachineList 'confidence': 0.42105263157894735
'confidence': 1.0
'confidence': 1.0
```
**Review Status:** PASS

---

## Query 21: `Which HVAC units do we have?`

**Status:** ❌ TIMEOUT

**Intent Match:**
```
2025-12-30 13:43:53.150 - skills - ovos_core.intent_services.service:get_pipeline_matcher:214 - ERROR - Unknown pipeline matcher: ovos-common-query-pipeline-plugin
```

---

## Query 22: `Show me active HVAC machines`

**Status:** ✅ GOT RESPONSE (5.062440626s)

**Response:**
8 active machines: Boiler-1, Compressor-1, Compressor-EU-1, Conveyor-A, HVAC-EU-North, HVAC-Main, Hydraulic-Pump-1, Injection-Molding-1

**Intent Match:**
```
enms-ovos-skill.a plus engineering:MachineStatus 'confidence': 0.5
'confidence': 1.0
'confidence': 1.0
```
**Review Status:** PASS

---

## Query 23: `Find the turbine machine`

**Status:** ✅ GOT RESPONSE (5.082645585s)

**Response:**
No machines found.

**Intent Match:**
```
enms-ovos-skill.a plus engineering:MachineList 'confidence': 0.3125
'confidence': 1.0
'confidence': 1.0
```
**Review Status:** PASS

---

## Query 24: `What machines are in the European facility?`

**Status:** ✅ GOT RESPONSE (5.071356069s)

**Response:**
The factory has consumed 1368815 kilowatt hours total. Current energy rate is 292 kilowatt hours per hour. Estimated cost is $164257.8. Carbon footprint is 684408.0 kilograms.

**Intent Match:**
```
enms-ovos-skill.a plus engineering:FactoryOverview 'confidence': 0.25
'confidence': 1.0
```
**Review Status:** PASS

---

## Query 25: `How many compressors do we have?`

**Status:** ❌ TIMEOUT

**Intent Match:**
```
2025-12-30 13:44:47.024 - skills - ovos_core.intent_services.service:get_pipeline_matcher:214 - ERROR - Unknown pipeline matcher: ovos-common-query-pipeline-plugin
```

---

## Query 26: `List all machines`

**Status:** ✅ GOT RESPONSE (5.068224142s)

**Response:**
We have 8 machines: Boiler-1, Compressor-1, Compressor-EU-1, Conveyor-A, HVAC-EU-North, HVAC-Main, Hydraulic-Pump-1, Injection-Molding-1.

**Intent Match:**
```
enms-ovos-skill.a plus engineering:MachineList 'confidence': 1.0
'confidence': 1.0
'confidence': 1.0
```
**Review Status:** PASS

---

## Query 27: `Get details for machine ID [UUID]"` (Internal/Debug use)`

**Status:** ❌ INVALID_FORMAT
**Raw Response:** {"detail":[{"type":"json_invalid","loc":["body",43],"msg":"JSON decode error","input":{},"ctx":{"error":"Expecting ',' delimiter"}}]}

---

## Query 28: `Show info for Boiler-1`

**Status:** ❌ TIMEOUT

**Intent Match:**
```
2025-12-30 13:45:28.476 - skills - ovos_core.intent_services.service:get_pipeline_matcher:214 - ERROR - Unknown pipeline matcher: ovos-common-query-pipeline-plugin
```

---

## Query 29: `N/A (API Test)`

**Status:** ❌ TIMEOUT

**Intent Match:**
```
2025-12-30 13:46:00.647 - skills - ovos_core.intent_services.service:get_pipeline_matcher:214 - ERROR - Unknown pipeline matcher: ovos-common-query-pipeline-plugin
```

---

## Query 30: `What's the status of Compressor-1?`

**Status:** ✅ GOT RESPONSE (5.089241489s)

**Response:**
Compressor-1 is currently running, using 52.0 kilowatts. Today it consumed 633.3 kilowatt-hours costing $96.6. No anomalies detected.

**Intent Match:**
```
enms-ovos-skill.a plus engineering:MachineStatus 'confidence': 0.5454545454545454
'confidence': 1.0
'confidence': 1.0
```
**Review Status:** PASS

---

## Query 31: `Is Compressor-1 running?`

**Status:** ✅ GOT RESPONSE (5.077279848s)

**Response:**
Compressor-1 is currently running, using 46.9 kilowatts. Today it consumed 633.4 kilowatt-hours costing $96.6. No anomalies detected.

**Intent Match:**
```
enms-ovos-skill.a plus engineering:MachineStatus 'confidence': 0.8260869565217391
'confidence': 1.0
'confidence': 1.0
```
**Review Status:** PASS

---

## Query 32: `What's the current power of HVAC-Main?`

**Status:** ✅ GOT RESPONSE (5.081413337s)

**Response:**
HVAC-Main is currently using 9.91 kilowatts.

**Intent Match:**
```
enms-ovos-skill.a plus engineering:PowerQuery 'confidence': 0.5945945945945946
'confidence': 1.0
'confidence': 1.0
'confidence': 1.0
```
**Review Status:** PASS

---

## Query 33: `How much energy did Compressor-1 use today?`

**Status:** ✅ GOT RESPONSE (5.081268512s)

**Response:**
Compressor-1 consumed 633.62 kilowatt hours today.

**Intent Match:**
```
enms-ovos-skill.a plus engineering:EnergyQuery 'confidence': 0.5714285714285714
'confidence': 1.0
'confidence': 1.0
'confidence': 1.0
```
**Review Status:** PASS

---

## Query 34: `What's the cost for HVAC-Main today?`

**Status:** ✅ GOT RESPONSE (5.087903986s)

**Response:**
HVAC-Main's cost today: 9.13 dollars.

**Intent Match:**
```
enms-ovos-skill.a plus engineering:CostAnalysis 'confidence': 0.3428571428571428
'confidence': 1.0
'confidence': 1.0
```
**Review Status:** PASS

---

## Query 35: `Are there anomalies on Compressor-1?`

**Status:** ✅ GOT RESPONSE (5.066981984s)

**Response:**
5 anomalies detected for Compressor-1 in the last 7 days.

**Intent Match:**
```
enms-ovos-skill.a plus engineering:AnomalyDetection 'confidence': 0.6
'confidence': 1.0
'confidence': 1.0
```
**Review Status:** PASS

---

## Query 36: `How many units did Compressor-1 produce today?`

**Status:** ✅ GOT RESPONSE (5.067546380s)

**Response:**
Compressor-1 produced 13556058 units today with 100.0% quality.

**Intent Match:**
```
enms-ovos-skill.a plus engineering:Production 'confidence': 0.45925925925925926
'confidence': 1.0
'confidence': 1.0
'confidence': 1.0
```
**Review Status:** PASS

---

## Query 37: `What's the quality rate for Compressor-1?`

**Status:** ✅ GOT RESPONSE (5.071317598s)

**Response:**
Compressor-1 produced 13558537 units today with 100.0% quality.

**Intent Match:**
```
enms-ovos-skill.a plus engineering:Production 'confidence': 0.6
'confidence': 1.0
'confidence': 1.0
'confidence': 1.0
```
**Review Status:** PASS

---

## Query 38: `What was the peak power for Compressor-1 today?`

**Status:** ✅ GOT RESPONSE (5.075223739s)

**Response:**
Compressor-1 is currently using 50.85 kilowatts.

**Intent Match:**
```
enms-ovos-skill.a plus engineering:PowerQuery 'confidence': 0.391304347826087
'confidence': 1.0
'confidence': 1.0
'confidence': 1.0
```
**Review Status:** PASS

---

## Query 39: `How long has Compressor-1 been running today?`

**Status:** ✅ GOT RESPONSE (5.068344812s)

**Response:**
Compressor-1 is currently running, using 50.7 kilowatts. Today it consumed 634.2 kilowatt-hours costing $96.6. No anomalies detected.

**Intent Match:**
```
enms-ovos-skill.a plus engineering:MachineStatus 'confidence': 0.3636363636363636
'confidence': 1.0
'confidence': 1.0
```
**Review Status:** PASS

---

## Query 40: `How much energy did Boiler-1 use today?`

**Status:** ✅ GOT RESPONSE (5.078984935s)

**Response:**
Boiler-1 consumed 1424.06 kilowatt hours today.

**Intent Match:**
```
enms-ovos-skill.a plus engineering:EnergyQuery 'confidence': 0.5614035087719298
'confidence': 1.0
'confidence': 1.0
'confidence': 1.0
```
**Review Status:** PASS

---

## Query 41: `What is the status of HVAC-Main?`

**Status:** ✅ GOT RESPONSE (5.069389182s)

**Response:**
HVAC-Main is currently running, using 8.0 kilowatts. Today it consumed 64.0 kilowatt-hours costing $9.1. No anomalies detected.

**Intent Match:**
```
enms-ovos-skill.a plus engineering:MachineStatus 'confidence': 0.4731182795698925
'confidence': 1.0
'confidence': 1.0
```
**Review Status:** PASS

---

## Query 42: `What's the energy efficiency for HVAC-Main this week?`

**Status:** ✅ GOT RESPONSE (5.067553927s)

**Response:**
HVAC-Main used 14.6% less energy than expected. Actual consumption was 111.4 kilowatt hours compared to a baseline of 130.4. This saved $2.85. This is a projection based on data through 13 hours today. Energy consumption 14.6% below baseline (projected from 13h of data).

**Intent Match:**
```
enms-ovos-skill.a plus engineering:Performance 'confidence': 0.44871794871794873
'confidence': 1.0
'confidence': 1.0
'confidence': 1.0
```
**Review Status:** PASS

---

## Query 43: `Show me energy for HVAC-Main this month`

**Status:** ❌ TIMEOUT

**Intent Match:**
```
2025-12-30 13:48:07.487 - skills - ovos_core.intent_services.service:get_pipeline_matcher:214 - ERROR - Unknown pipeline matcher: ovos-common-query-pipeline-plugin
```

---

## Query 44: `Show hourly energy consumption for Compressor-1 today`

**Status:** ✅ GOT RESPONSE (5.067481452s)

**Response:**
Compressor-1 consumed 635.03 kWh total from December 30 at 12 AM to December 30 at 1 PM. Hourly breakdown: December 30 at 12 AM: 43.2 kWh, December 30 at 1 AM: 43.3 kWh, December 30 at 2 AM: 43.3 kWh, December 30 at 3 AM: 43.3 kWh, December 30 at 4 AM: 43.3 kWh, December 30 at 5 AM: 43.3 kWh, December 30 at 6 AM: 48.1 kWh, December 30 at 7 AM: 48.1 kWh, December 30 at 8 AM: 48.1 kWh, December 30 at 9 AM: 48.1 kWh, December 30 at 10 AM: 48.1 kWh, December 30 at 11 AM: 48.0 kWh, December 30 at 12 PM: 48.1 kWh, December 30 at 1 PM: 39.0 kWh.

**Intent Match:**
```
enms-ovos-skill.a plus engineering:EnergyQuery 'confidence': 0.5911949685534591
'confidence': 1.0
'confidence': 1.0
'confidence': 1.0
```
**Review Status:** PASS

---

## Query 45: `How much energy did the HVAC use yesterday?`

**Status:** ✅ GOT RESPONSE (5.074399434s)

**Response:**
Factory consumed 4298.0 kilowatt-hours today

**Intent Match:**
```
enms-ovos-skill.a plus engineering:EnergyQuery 'confidence': 0.3333333333333333
'confidence': 1.0
'confidence': 1.0
```
**Review Status:** PASS

---

## Query 46: `Give me 15-minute energy data for Compressor-1 in the last hour`

**Status:** ✅ GOT RESPONSE (5.088152174s)

**Response:**
Compressor-1 consumed 48.09 kWh total from December 30 at 12 PM to December 30 at 1 PM. 15-minute intervals: December 30 at 12 PM: 8.9 kWh, December 30 at 1 PM: 12.0 kWh, December 30 at 1 PM: 12.0 kWh, December 30 at 1 PM: 12.0 kWh, December 30 at 1 PM: 3.1 kWh.

**Intent Match:**
```
enms-ovos-skill.a plus engineering:EnergyQuery 'confidence': 0.529100529100529
'confidence': 1.0
'confidence': 1.0
'confidence': 1.0
```
**Review Status:** PASS

---

## Query 47: `Compressor-1 energy consumption last 24 hours`

**Status:** ✅ GOT RESPONSE (5.067686066s)

**Response:**
Compressor-1's average power was 46.55 kilowatts from December 29 at 1 PM to December 30 at 1 PM.

**Intent Match:**
```
enms-ovos-skill.a plus engineering:PowerQuery 'confidence': 0.6370370370370371
'confidence': 1.0
'confidence': 1.0
'confidence': 1.0
```
**Review Status:** PASS

---

## Query 48: `What was Compressor-1 average power today?`

**Status:** ✅ GOT RESPONSE (5.060754155s)

**Response:**
Compressor-1 is currently using 47.69 kilowatts.

**Intent Match:**
```
enms-ovos-skill.a plus engineering:PowerQuery 'confidence': 0.5609756097560976
'confidence': 1.0
'confidence': 1.0
'confidence': 1.0
```
**Review Status:** PASS

---

## Query 49: `Show me Compressor-1 power in the last hour`

**Status:** ✅ GOT RESPONSE (5.057867540s)

**Response:**
Compressor-1's average power was 48.18 kilowatts from December 30 at 12 PM to December 30 at 1 PM.

**Intent Match:**
```
enms-ovos-skill.a plus engineering:PowerQuery 'confidence': 0.38372093023255816
'confidence': 1.0
'confidence': 1.0
```
**Review Status:** PASS

---

## Query 50: `What's the current power of Compressor-1?`

**Status:** ✅ GOT RESPONSE (5.058300366s)

**Response:**
Compressor-1 is currently using 47.14 kilowatts.

**Intent Match:**
```
enms-ovos-skill.a plus engineering:PowerQuery 'confidence': 0.625
'confidence': 1.0
'confidence': 1.0
'confidence': 1.0
```
**Review Status:** PASS

---

## Query 51: `Is the HVAC running right now?`

**Status:** ❌ TIMEOUT

**Intent Match:**
```
2025-12-30 13:49:30.276 - skills - ovos_core.intent_services.service:get_pipeline_matcher:214 - ERROR - Unknown pipeline matcher: ovos-common-query-pipeline-plugin
```

---

## Query 52: `Compare energy usage between Compressor-1 and HVAC-Main`

**Status:** ✅ GOT RESPONSE (5.073299994s)

**Response:**
Comparing Compressor-1 and HVAC-Main: Compressor-1 consumed 636.1 kilowatt-hours today, while HVAC-Main consumed 64.3 kilowatt-hours.

**Intent Match:**
```
enms-ovos-skill.a plus engineering:Comparison 'confidence': 0.5939393939393939
'confidence': 1.0
'confidence': 1.0
'confidence': 1.0
```
**Review Status:** PASS

---

## Query 53: `Compare all compressors this week`

**Status:** ❌ TIMEOUT

**Intent Match:**
```
2025-12-30 13:50:09.703 - skills - ovos_core.intent_services.service:get_pipeline_matcher:214 - ERROR - Unknown pipeline matcher: ovos-common-query-pipeline-plugin
```

---

## Query 54: `Check for anomalies in Compressor-1 today`

**Status:** ✅ GOT RESPONSE (5.062663730s)

**Response:**
Detected 2 anomalies in Compressor-1 using baseline model version 12.

**Intent Match:**
```
enms-ovos-skill.a plus engineering:AnomalyDetection 'confidence': 0.5853658536585366
'confidence': 1.0
'confidence': 1.0
'confidence': 1.0
```
**Review Status:** PASS

---

## Query 55: `Detect unusual patterns in HVAC-Main today`

**Status:** ✅ GOT RESPONSE (5.072157452s)

**Response:**
Detected 2 anomalies in HVAC-Main using baseline model version 8.

**Intent Match:**
```
enms-ovos-skill.a plus engineering:AnomalyDetection 'confidence': 0.5873015873015873
'confidence': 1.0
'confidence': 1.0
'confidence': 1.0
```
**Review Status:** PASS

---

## Query 56: `Run anomaly detection on HVAC today`

**Status:** ✅ GOT RESPONSE (5.075576758s)

**Response:**
9 most recent anomalies detected in the last 7 days across 2 machines: Compressor-1, HVAC-Main.

**Intent Match:**
```
enms-ovos-skill.a plus engineering:AnomalyDetection 'confidence': 0.37142857142857144
'confidence': 1.0
'confidence': 1.0
```
**Review Status:** PASS

---

## Query 57: `Show me recent anomalies`

**Status:** ✅ GOT RESPONSE (5.078755853s)

**Response:**
9 most recent anomalies detected in the last 7 days across 2 machines: Compressor-1, HVAC-Main.

**Intent Match:**
```
enms-ovos-skill.a plus engineering:AnomalyDetection 'confidence': 0.33333333333333337
'confidence': 1.0
```
**Review Status:** PASS

---

## Query 58: `What critical issues happened today?`

**Status:** ✅ GOT RESPONSE (5.071178874s)

**Response:**
No recent anomalies detected in the last 7 days.

**Intent Match:**
```
enms-ovos-skill.a plus engineering:AnomalyDetection 'confidence': 0.2857142857142857
'confidence': 1.0
'confidence': 1.0
```
**Review Status:** PASS

---

## Query 59: `List anomalies for Compressor-1`

**Status:** ✅ GOT RESPONSE (5.063619413s)

**Response:**
7 anomalies detected for Compressor-1 in the last 7 days.

**Intent Match:**
```
enms-ovos-skill.a plus engineering:AnomalyDetection 'confidence': 0.6774193548387097
'confidence': 1.0
'confidence': 1.0
```
**Review Status:** PASS

---

## Query 60: `Show anomalies`

**Status:** ✅ GOT RESPONSE (5.077455586s)

**Response:**
9 most recent anomalies detected in the last 7 days across 2 machines: Compressor-1, HVAC-Main.

**Intent Match:**
```
enms-ovos-skill.a plus engineering:AnomalyDetection 'confidence': 0.4642857142857143
'confidence': 1.0
```
**Review Status:** PASS

---

## Query 61: `Are there any active alerts?`

**Status:** ✅ GOT RESPONSE (5.084483687s)

**Response:**
There are 14 active alerts requiring attention. Recent alerts: HVAC-Main, Compressor-1.

**Intent Match:**
```
enms-ovos-skill.a plus engineering:AnomalyDetection 'confidence': 0.48148148148148145
'confidence': 1.0
```
**Review Status:** PASS

---

## Query 62: `Show me unresolved issues`

**Status:** ✅ GOT RESPONSE (5.066748258s)

**Response:**
There are 14 active alerts requiring attention. Recent alerts: HVAC-Main, Compressor-1.

**Intent Match:**
```
enms-ovos-skill.a plus engineering:AnomalyDetection 'confidence': 0.30666666666666664
'confidence': 1.0
```
**Review Status:** PASS

---

## Query 63: `What problems need attention?`

**Status:** ✅ GOT RESPONSE (5.075297704s)

**Response:**
There are 14 active alerts requiring attention. Recent alerts: HVAC-Main, Compressor-1.

**Intent Match:**
```
enms-ovos-skill.a plus engineering:AnomalyDetection 'confidence': 0.2857142857142857
'confidence': 1.0
```
**Review Status:** PASS

---

## Query 64: `Find anomalies from last month`

**Status:** ✅ GOT RESPONSE (5.075687030s)

**Response:**
No anomalies found for find in the specified time range.

**Intent Match:**
```
enms-ovos-skill.a plus engineering:AnomalyDetection 'confidence': 0.5111111111111111
'confidence': 1.0
'confidence': 1.0
'confidence': 1.0
'confidence': 1.0
```
**Review Status:** PASS

---

## Query 65: `Search for critical anomalies this week`

**Status:** ✅ GOT RESPONSE (5.059712057s)

**Response:**
No anomalies found for search for in the specified time range.

**Intent Match:**
```
enms-ovos-skill.a plus engineering:AnomalyDetection 'confidence': 0.46153846153846156
'confidence': 1.0
'confidence': 1.0
```
**Review Status:** PASS

---

## Query 66: `Search anomalies for Compressor-1 last week`

**Status:** ✅ GOT RESPONSE (5.040209972s)

**Response:**
Found 7 anomalies for Compressor-1 in the specified time range.

**Intent Match:**
```
enms-ovos-skill.a plus engineering:AnomalyDetection 'confidence': 0.46511627906976744
'confidence': 1.0
'confidence': 1.0
```
**Review Status:** PASS

---

## Query 67: `Show baseline models for Compressor-1`

**Status:** ✅ GOT RESPONSE (5.078424867s)

**Response:**
Found 13 baseline models for Compressor-1. Active model: version 12, R-squared 0.9732, trained on 477 samples.

**Intent Match:**
```
enms-ovos-skill.a plus engineering:BaselineModels 'confidence': 0.6081081081081081
'confidence': 1.0
'confidence': 1.0
'confidence': 1.0
```
**Review Status:** PASS

---

## Query 68: `What baseline models exist for HVAC-Main?`

**Status:** ✅ GOT RESPONSE (5.065580090s)

**Response:**
Found 8 baseline models for HVAC-Main. Active model: version 8, R-squared 0.2445, trained on 562 samples.

**Intent Match:**
```
enms-ovos-skill.a plus engineering:BaselineModels 'confidence': 0.575
'confidence': 1.0
'confidence': 1.0
'confidence': 1.0
```
**Review Status:** PASS

---

## Query 69: `List all baseline models in the system`

**Status:** ❌ TIMEOUT

**Intent Match:**
```
2025-12-30 13:52:30.737 - skills - ovos_core.intent_services.service:get_pipeline_matcher:214 - ERROR - Unknown pipeline matcher: ovos-common-query-pipeline-plugin
```

---

## Query 70: `What's the expected energy for Compressor-1?`

**Status:** ✅ GOT RESPONSE (5.079449604s)

**Response:**
Compressor-1 is predicted to consume 0.0 kilowatt hours with 5,000,000 units production, 22.0°C temperature, 7.0 bar pressure, and 85.0% load.

**Intent Match:**
```
enms-ovos-skill.a plus engineering:Baseline 'confidence': 0.7209302325581395
'confidence': 1.0
'confidence': 1.0
'confidence': 1.0
```
**Review Status:** PASS

---

## Query 71: `Predict energy consumption for Compressor-1 with 500 units production`

**Status:** ✅ GOT RESPONSE (5.078433469s)

**Response:**
Compressor-1 is predicted to consume 0.0 kilowatt hours with 500 units production, 22.0°C temperature, 7.0 bar pressure, and 85.0% load.

**Intent Match:**
```
enms-ovos-skill.a plus engineering:Baseline 'confidence': 0.41304347826086957
'confidence': 1.0
'confidence': 1.0
'confidence': 1.0
```
**Review Status:** PASS

---

## Query 72: `Predict energy for Compressor-1 at 30 degrees`

**Status:** ✅ GOT RESPONSE (5.076976161s)

**Response:**
Compressor-1's forecast for tomorrow is 1006.5 kilowatt hours, costing $150.98. Peak power of 52.9 kilowatts expected at 14:00:00 with 84.0% confidence.

**Intent Match:**
```
enms-ovos-skill.a plus engineering:Forecast 'confidence': 0.5777777777777777
'confidence': 1.0
'confidence': 1.0
'confidence': 1.0
```
**Review Status:** PASS

---

## Query 73: `What's the expected energy for HVAC-Main at 8 bar pressure?`

**Status:** ✅ GOT RESPONSE (5.061943267s)

**Response:**
HVAC-Main is predicted to consume 5.0 kilowatt hours with 5,000,000 units production, 22.0°C temperature, 8.0 bar pressure, and 85.0% load.

**Intent Match:**
```
enms-ovos-skill.a plus engineering:Baseline 'confidence': 0.48275862068965514
'confidence': 1.0
'confidence': 1.0
'confidence': 1.0
```
**Review Status:** PASS

---

## Query 74: `Predict energy for Compressor-1 at 90 percent load factor`

**Status:** ✅ GOT RESPONSE (5.060012060s)

**Response:**
Compressor-1 has a load factor of 83.0 percent today.

**Intent Match:**
```
enms-ovos-skill.a plus engineering:LoadFactor 'confidence': 0.4327485380116959
'confidence': 1.0
'confidence': 1.0
```
**Review Status:** PASS

---

## Query 75: `Expected energy for HVAC-Main`

**Status:** ✅ GOT RESPONSE (5.073925340s)

**Response:**
HVAC-Main is predicted to consume 5.0 kilowatt hours with 5,000,000 units production, 22.0°C temperature, 7.0 bar pressure, and 85.0% load.

**Intent Match:**
```
enms-ovos-skill.a plus engineering:Baseline 'confidence': 0.9655172413793103
'confidence': 1.0
'confidence': 1.0
'confidence': 1.0
```
**Review Status:** PASS

---

## Query 76: `Predict energy for Compressor-1 with temp 25, pressure 7.5, and 5 million units`

**Status:** ✅ GOT RESPONSE (5.079370106s)

**Response:**
Compressor-1's forecast for tomorrow is 1006.6 kilowatt hours, costing $150.98. Peak power of 52.9 kilowatts expected at 14:00:00 with 84.0% confidence.

**Intent Match:**
```
enms-ovos-skill.a plus engineering:Forecast 'confidence': 0.26160337552742613
'confidence': 1.0
'confidence': 1.0
'confidence': 1.0
```
**Review Status:** PASS

---

## Query 77: `Show me details for baseline model 46`

**Status:** ❌ TIMEOUT

**Intent Match:**
```
2025-12-30 13:53:53.859 - skills - ovos_core.intent_services.service:get_pipeline_matcher:214 - ERROR - Unknown pipeline matcher: ovos-common-query-pipeline-plugin
```

---

## Query 78: `Explain baseline model 46`

**Status:** ❌ TIMEOUT

**Intent Match:**
```
2025-12-30 13:54:25.952 - skills - ovos_core.intent_services.service:get_pipeline_matcher:214 - ERROR - Unknown pipeline matcher: ovos-common-query-pipeline-plugin
```

---

## Query 79: `Train a baseline model for Compressor-1`

**Status:** ✅ GOT RESPONSE (5.079857775s)

**Response:**
Could not train baseline for Compressor-1. Training failed for Compressor-1 electricity: duplicate key value violates unique constraint "energy_baselines_machine_energy_version_unique"
DETAIL:  Key (machine_id, energy_source_id, model_version)=(c0000000-0000-0000-0000-000000000001, 7e0d4330-5cea-411b-a97e-b0eb2003864b, 13) already exists.

**Intent Match:**
```
enms-ovos-skill.a plus engineering:TrainBaseline 'confidence': 0.5769230769230769
'confidence': 1.0
'confidence': 1.0
'confidence': 1.0
'confidence': 1.0
'confidence': 1.0
```

⚠️ **NEEDS REVIEW:** Response contains error keywords
**Review Status:** NEEDS_MANUAL_REVIEW

---

## Query 80: `Train baseline using last month's data`

**Status:** ✅ GOT RESPONSE (5.081686983s)

**Response:**
Please specify which machine to train. For example, 'train a baseline for Compressor-1'

**Intent Match:**
```
enms-ovos-skill.a plus engineering:TrainBaseline 'confidence': 0.4035087719298245
'confidence': 1.0
'confidence': 1.0
'confidence': 1.0
'confidence': 1.0
```
**Review Status:** PASS

---

## Query 81: `What are the KPIs for Compressor-1 today?`

**Status:** ✅ GOT RESPONSE (5.069071266s)

**Response:**
Compressor-1's KPIs for the period: 0.00005 kWh/unit SEC, 55.1 kW peak demand, 83% load factor, $95.9 energy cost, and 120.6 kg CO2 emissions.

**Intent Match:**
```
enms-ovos-skill.a plus engineering:KPI 'confidence': 0.4833333333333333
'confidence': 1.0
'confidence': 1.0
'confidence': 1.0
```
**Review Status:** PASS

---

## Query 82: `Show KPIs for HVAC-Main this week`

**Status:** ✅ GOT RESPONSE (5.071188843s)

**Response:**
HVAC-Main's KPIs for the period: 0.00023 kWh/unit SEC, 9.8 kW peak demand, 43.5% load factor, $8.9 energy cost, and 11.2 kg CO2 emissions.

**Intent Match:**
```
enms-ovos-skill.a plus engineering:KPI 'confidence': 0.45454545454545453
'confidence': 1.0
'confidence': 1.0
'confidence': 1.0
```
**Review Status:** PASS

---

## Query 83: `What are the cost KPIs for Compressor-1 today?`

**Status:** ✅ GOT RESPONSE (5.074368634s)

**Response:**
Compressor-1's cost today: 96.61 dollars.

**Intent Match:**
```
enms-ovos-skill.a plus engineering:CostAnalysis 'confidence': 0.3222222222222222
'confidence': 1.0
'confidence': 1.0
```
**Review Status:** PASS

---

## Query 84: `What are the cost KPIs for Compressor-1?`

**Status:** ✅ GOT RESPONSE (5.068879187s)

**Response:**
Compressor-1's cost today: 96.61 dollars.

**Intent Match:**
```
enms-ovos-skill.a plus engineering:CostAnalysis 'confidence': 0.41025641025641024
'confidence': 1.0
'confidence': 1.0
```
**Review Status:** PASS

---

## Query 85: `Analyze performance of Compressor-1`

**Status:** ✅ GOT RESPONSE (5.072715595s)

**Response:**
Compressor-1 used 5.5% more energy than expected. Actual consumption was 1103.9 kilowatt hours compared to a baseline of 1046.7. This cost an extra $8.58. This is a projection based on data through 13 hours today. Energy consumption 5.5% above baseline (projected from 13h of data).

**Intent Match:**
```
enms-ovos-skill.a plus engineering:Performance 'confidence': 0.8857142857142857
'confidence': 1.0
'confidence': 1.0
'confidence': 1.0
```
**Review Status:** PASS

---

## Query 86: `Analyze HVAC-Main performance`

**Status:** ✅ GOT RESPONSE (5.071326808s)

**Response:**
HVAC-Main used 14.1% less energy than expected. Actual consumption was 112.0 kilowatt hours compared to a baseline of 130.4. This saved $2.76. This is a projection based on data through 13 hours today. Energy consumption 14.1% below baseline (projected from 13h of data).

**Intent Match:**
```
enms-ovos-skill.a plus engineering:Performance 'confidence': 0.6896551724137931
'confidence': 1.0
'confidence': 1.0
```
**Review Status:** PASS

---

## Query 87: `Is the performance engine running?`

**Status:** ✅ GOT RESPONSE (5.064906401s)

**Response:**
8 active machines: Boiler-1, Compressor-1, Compressor-EU-1, Conveyor-A, HVAC-EU-North, HVAC-Main, Hydraulic-Pump-1, Injection-Molding-1

**Intent Match:**
```
enms-ovos-skill.a plus engineering:MachineStatus 'confidence': 0.2727272727272727
'confidence': 1.0
```
**Review Status:** PASS

---

## Query 88: `What are the energy saving opportunities?`

**Status:** ✅ GOT RESPONSE (5.068387760s)

**Response:**
error general

**Intent Match:**
```
enms-ovos-skill.a plus engineering:Performance 'confidence': 0.675
'confidence': 1.0
'confidence': 1.0
```

⚠️ **NEEDS REVIEW:** Response contains error keywords
**Review Status:** NEEDS_MANUAL_REVIEW

---

## Query 89: `Show saving opportunities for Compressor-1`

**Status:** ✅ GOT RESPONSE (5.054577081s)

**Response:**
Compressor-1 used 5.5% more energy than expected. Actual consumption was 1104.0 kilowatt hours compared to a baseline of 1046.7. This cost an extra $8.59. This is a projection based on data through 13 hours today. Energy consumption 5.5% above baseline (projected from 13h of data).

**Intent Match:**
```
enms-ovos-skill.a plus engineering:Performance 'confidence': 0.5714285714285714
'confidence': 1.0
'confidence': 1.0
'confidence': 1.0
```
**Review Status:** PASS

---

## Query 90: `Create an action plan for Compressor-1 efficiency improvement`

**Status:** ✅ GOT RESPONSE (15.155315630s)

**Response:**
Compressor-1 used 5.5% more energy than expected. Actual consumption was 1104.0 kilowatt hours compared to a baseline of 1046.7. This cost an extra $8.59. This is a projection based on data through 13 hours today. Energy consumption 5.5% above baseline (projected from 13h of data).

**Intent Match:**
```
enms-ovos-skill.a plus engineering:Performance 'confidence': 0.360655737704918
'confidence': 1.0
'confidence': 1.0
```
**Review Status:** PASS

---

## Query 91: `Forecast energy for next 24 hours`

**Status:** ✅ GOT RESPONSE (5.078099023s)

**Response:**
Tomorrow's factory-wide energy forecast is 10569.4 kilowatt hours, costing $1585.41. Peak demand of 379.0 kilowatts expected at 14:00:00 from Boiler-1.

**Intent Match:**
```
enms-ovos-skill.a plus engineering:Forecast 'confidence': 0.45454545454545453
'confidence': 1.0
'confidence': 1.0
```
**Review Status:** PASS

---

## Query 92: `What will Compressor-1 consume tomorrow?`

**Status:** ✅ GOT RESPONSE (5.073516630s)

**Response:**
Compressor-1's forecast for tomorrow is 1006.9 kilowatt hours, costing $151.03. Peak power of 52.9 kilowatts expected at 14:00:00 with 84.0% confidence.

**Intent Match:**
```
enms-ovos-skill.a plus engineering:Forecast 'confidence': 0.5128205128205128
'confidence': 1.0
'confidence': 1.0
```
**Review Status:** PASS

---

## Query 93: `What's tomorrow's energy forecast?`

**Status:** ✅ GOT RESPONSE (5.059214882s)

**Response:**
Tomorrow's factory-wide energy forecast is 10569.5 kilowatt hours, costing $1585.43. Peak demand of 379.0 kilowatts expected at 14:00:00 from Boiler-1.

**Intent Match:**
```
enms-ovos-skill.a plus engineering:Forecast 'confidence': 0.3484848484848485
'confidence': 1.0
```
**Review Status:** PASS

---

## Query 94: `Forecast energy demand for Compressor-1`

**Status:** ✅ GOT RESPONSE (5.080179520s)

**Response:**
Compressor-1's demand forecast for the next 4 periods: average 48.1 kilowatts, with 95% confidence ranging from 47.5 to 48.7 kilowatts. Forecasted using ARIMA model with 15T intervals.

**Intent Match:**
```
enms-ovos-skill.a plus engineering:Forecast 'confidence': 0.8717948717948718
'confidence': 1.0
'confidence': 1.0
'confidence': 1.0
```
**Review Status:** PASS

---

## Query 95: `Give me a detailed forecast for HVAC-Main`

**Status:** ✅ GOT RESPONSE (5.078500276s)

**Response:**
HVAC-Main is predicted to consume 5.0 kilowatt hours with 5,000,000 units production, 22.0°C temperature, 7.0 bar pressure, and 85.0% load.

**Intent Match:**
```
enms-ovos-skill.a plus engineering:Baseline 'confidence': 0.3902439024390244
'confidence': 1.0
'confidence': 1.0
```
**Review Status:** PASS

---

## Query 96: `List all significant energy uses`

**Status:** ✅ GOT RESPONSE (5.059436998s)

**Response:**
I found 7 significant energy uses.
The SEUs are: Compressor-1, Compressor-EU-1, Conveyor-A, HVAC-EU-North, HVAC-Main, Hydraulic-Pump-1, Injection-Molding-1.
0 have baseline models trained, and 7 need baselines.

**Intent Match:**
```
enms-ovos-skill.a plus engineering:SEUs 'confidence': 0.71875
'confidence': 1.0
'confidence': 1.0
```
**Review Status:** PASS

---

## Query 97: `List electricity energy uses`

**Status:** ❌ TIMEOUT

**Intent Match:**
```
2025-12-30 13:57:18.756 - skills - ovos_core.intent_services.service:get_pipeline_matcher:214 - ERROR - Unknown pipeline matcher: ovos-common-query-pipeline-plugin
```

---

## Query 98: `Give me a factory summary`

**Status:** ✅ GOT RESPONSE (5.084512063s)

**Response:**
I received your request but have no response.

**Intent Match:**
```
enms-ovos-skill.a plus engineering:FactoryOverview 'confidence': 0.28
'confidence': 1.0
```
**Review Status:** PASS

---

## Query 99: `Show top 3 energy consumers`

**Status:** ✅ GOT RESPONSE (5.072728944s)

**Response:**
Top  energy consumers:
1. Boiler-1: 1443.42 kWh (33.2% of total)
2. Compressor-EU-1: 1048.63 kWh (24.1% of total)
3. Injection-Molding-1: 685.75 kWh (15.8% of total)

**Intent Match:**
```
enms-ovos-skill.a plus engineering:Ranking 'confidence': 0.48148148148148145
'confidence': 1.0
'confidence': 1.0
```
**Review Status:** PASS

---

## Query 100: `Which machine is most efficient?`

**Status:** ❌ TIMEOUT

**Intent Match:**
```
2025-12-30 13:58:05.391 - skills - ovos_core.intent_services.service:get_pipeline_matcher:214 - ERROR - Unknown pipeline matcher: ovos-common-query-pipeline-plugin
```

---

## Query 101: `Show me the top 5 energy consumers`

**Status:** ✅ GOT RESPONSE (5.089252517s)

**Response:**
Top  energy consumers:
1. Boiler-1: 1445.46 kWh (33.2% of total)
2. Compressor-EU-1: 1049.95 kWh (24.2% of total)
3. Injection-Molding-1: 685.99 kWh (15.8% of total)
4. Compressor-1: 641.72 kWh (14.8% of total)
5. Conveyor-A: 208.31 kWh (4.8% of total)

**Intent Match:**
```
enms-ovos-skill.a plus engineering:Ranking 'confidence': 0.42647058823529416
'confidence': 1.0
'confidence': 1.0
```
**Review Status:** PASS

---

## Query 102: `Which machine uses the most power?`

**Status:** ✅ GOT RESPONSE (5.087108228s)

**Response:**
The factory is currently drawing 251.7 kilowatts with 7 machines active.
Current factory-wide power consumption is 251.7 kilowatts. Average power today: 242.9 kilowatts.
All machines combined are using 251.7 kilowatts right now. 7 of 8 machines are running.
The entire facility is drawing 251.7 kilowatts of power at the moment.

**Intent Match:**
```
enms-ovos-skill.a plus engineering:PowerQuery 'confidence': 0.36363636363636365
'confidence': 1.0
'confidence': 1.0
```
**Review Status:** PASS

---

## Query 103: `Which machine uses the most energy?`

**Status:** ✅ GOT RESPONSE (5.070547280s)

**Response:**
Top  energy consumers:
1. Boiler-1: 1445.46 kWh (33.2% of total)
2. Compressor-EU-1: 1049.95 kWh (24.2% of total)
3. Injection-Molding-1: 685.99 kWh (15.8% of total)
4. Compressor-1: 641.72 kWh (14.8% of total)
5. Conveyor-A: 208.31 kWh (4.8% of total)

**Intent Match:**
```
enms-ovos-skill.a plus engineering:Ranking 'confidence': 0.2647058823529412
'confidence': 1.0
'confidence': 1.0
```
**Review Status:** PASS

---

## Query 104: `What are the top 5 power consumers?`

**Status:** ✅ GOT RESPONSE (5.060565288s)

**Response:**
The factory is currently drawing 260.9 kilowatts with 7 machines active.
Current factory-wide power consumption is 260.9 kilowatts. Average power today: 242.9 kilowatts.
All machines combined are using 260.9 kilowatts right now. 7 of 8 machines are running.
The entire facility is drawing 260.9 kilowatts of power at the moment.

**Intent Match:**
```
enms-ovos-skill.a plus engineering:PowerQuery 'confidence': 0.3088235294117647
'confidence': 1.0
```
**Review Status:** PASS

---

## Query 105: `Which machines consume the least energy?`

**Status:** ✅ GOT RESPONSE (5.071065270s)

**Response:**
Top  energy consumers:
1. Boiler-1: 1445.46 kWh (33.2% of total)
2. Compressor-EU-1: 1049.95 kWh (24.2% of total)
3. Injection-Molding-1: 685.99 kWh (15.8% of total)
4. Compressor-1: 641.72 kWh (14.8% of total)
5. Conveyor-A: 208.31 kWh (4.8% of total)

**Intent Match:**
```
enms-ovos-skill.a plus engineering:Ranking 'confidence': 0.2564102564102564
'confidence': 1.0
'confidence': 1.0
```
**Review Status:** PASS

---

## Query 106: `What energy types does Compressor-1 use?`

**Status:** ✅ GOT RESPONSE (5.077858469s)

**Response:**
Could not get baseline prediction for Compressor-1. The machine may not have a trained model yet.

**Intent Match:**
```
enms-ovos-skill.a plus engineering:Baseline 'confidence': 0.37606837606837606
'confidence': 1.0
'confidence': 1.0
```

⚠️ **NEEDS REVIEW:** Response contains error keywords
**Review Status:** NEEDS_MANUAL_REVIEW

---

## Query 107: `Show electricity consumption for Compressor-1`

**Status:** ✅ GOT RESPONSE (5.062191097s)

**Response:**
error general

**Intent Match:**
```
enms-ovos-skill.a plus engineering:EnergyQuery 'confidence': 0.5777777777777777
'confidence': 1.0
'confidence': 1.0
'confidence': 1.0
```

⚠️ **NEEDS REVIEW:** Response contains error keywords
**Review Status:** NEEDS_MANUAL_REVIEW

---

## Query 108: `Show energy summary for all types`

**Status:** ❌ TIMEOUT

**Intent Match:**
```
2025-12-30 13:59:28.351 - skills - ovos_core.intent_services.service:get_pipeline_matcher:214 - ERROR - Unknown pipeline matcher: ovos-common-query-pipeline-plugin
```

---

## Query 109: `OVOS factory summary`

**Status:** ✅ GOT RESPONSE (5.060044362s)

**Response:**
I received your request but have no response.

**Intent Match:**
```
enms-ovos-skill.a plus engineering:FactoryOverview 'confidence': 0.35
'confidence': 1.0
```
**Review Status:** PASS

---

## Query 110: `Check factory status"` (Legacy)`

**Status:** ❌ INVALID_FORMAT
**Raw Response:** {"detail":[{"type":"json_invalid","loc":["body",30],"msg":"JSON decode error","input":{},"ctx":{"error":"Expecting ',' delimiter"}}]}

---

## Query 111: `Who are the top consumers?"` (Legacy intent)`

**Status:** ❌ INVALID_FORMAT
**Raw Response:** {"detail":[{"type":"json_invalid","loc":["body",36],"msg":"JSON decode error","input":{},"ctx":{"error":"Expecting ',' delimiter"}}]}

---

## Query 112: `Status of Compressor-1"` (Legacy intent)`

**Status:** ❌ INVALID_FORMAT
**Raw Response:** {"detail":[{"type":"json_invalid","loc":["body",32],"msg":"JSON decode error","input":{},"ctx":{"error":"Expecting ',' delimiter"}}]}

---

## Query 113: `Forecast for tomorrow"` (Legacy intent)`

**Status:** ❌ INVALID_FORMAT
**Raw Response:** {"detail":[{"type":"json_invalid","loc":["body",31],"msg":"JSON decode error","input":{},"ctx":{"error":"Expecting ',' delimiter"}}]}

---

## Query 114: `Subscribe me to critical alerts`

**Status:** ❌ TIMEOUT

**Intent Match:**
```
2025-12-30 14:00:15.893 - skills - ovos_core.intent_services.service:get_pipeline_matcher:214 - ERROR - Unknown pipeline matcher: ovos-common-query-pipeline-plugin
```

---

## Query 115: `Show energy performance indicators report`

**Status:** ❌ TIMEOUT

**Intent Match:**
```
2025-12-30 14:00:48.050 - skills - ovos_core.intent_services.service:get_pipeline_matcher:214 - ERROR - Unknown pipeline matcher: ovos-common-query-pipeline-plugin
```

---

## Query 116: `Create an ISO action plan for energy reduction`

**Status:** ✅ GOT RESPONSE (15.165533298s)

**Response:**
error general

**Intent Match:**
```
enms-ovos-skill.a plus engineering:Performance 'confidence': 0.2934782608695652
'confidence': 1.0
```

⚠️ **NEEDS REVIEW:** Response contains error keywords
**Review Status:** NEEDS_MANUAL_REVIEW

---

## Query 117: `List all ISO action plans`

**Status:** ✅ GOT RESPONSE (5.059370456s)

**Response:**
error general

**Intent Match:**
```
enms-ovos-skill.a plus engineering:Performance 'confidence': 0.48
'confidence': 1.0
```

⚠️ **NEEDS REVIEW:** Response contains error keywords
**Review Status:** NEEDS_MANUAL_REVIEW

---

## Query 118: `Update action plan progress to 50 percent`

**Status:** ✅ GOT RESPONSE (5.087468976s)

**Response:**
error general

**Intent Match:**
```
enms-ovos-skill.a plus engineering:Performance 'confidence': 0.2682926829268293
'confidence': 1.0
```

⚠️ **NEEDS REVIEW:** Response contains error keywords
**Review Status:** NEEDS_MANUAL_REVIEW

---

## Summary

- **Total Queries:** 118
- **✅ Passed:** 85
- **❌ Timeouts:** 21
- **❌ Errors:** 5
- **⚠️ Needs Review:** 7
- **Success Rate:** 72.0%
