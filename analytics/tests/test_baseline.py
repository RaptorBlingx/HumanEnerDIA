import pytest
from uuid import uuid4

from services.driver_analysis_service import DriverAnalysisService


@pytest.mark.asyncio
async def test_driver_analysis_returns_candidates_when_baseline_missing(monkeypatch):
	service = DriverAnalysisService()

	seu = {
		"id": uuid4(),
		"name": "Compressor-1",
		"energy_source_id": uuid4(),
		"energy_source_name": "electricity",
		"energy_unit": "kWh",
		"machine_ids": [uuid4()],
	}

	async def fake_get_seu(*args, **kwargs):
		return seu

	async def fake_get_model(*args, **kwargs):
		return None

	async def fake_candidates(*args, **kwargs):
		return [
			{
				"feature": "outdoor_temp_c",
				"human_name": "Outdoor Temperature",
				"description": "Ambient weather",
				"rank": 1,
				"absolute_impact": None,
				"direction": None,
				"driver_type": "candidate",
			},
			{
				"feature": "production_count",
				"human_name": "Production Count",
				"description": "Units produced",
				"rank": 2,
				"absolute_impact": None,
				"direction": None,
				"driver_type": "candidate",
			},
		]

	monkeypatch.setattr(service, "_get_seu_by_name_and_energy_source", fake_get_seu)
	monkeypatch.setattr(service, "_get_active_model_for_seu", fake_get_model)
	monkeypatch.setattr(service, "_build_candidate_drivers", fake_candidates)

	result = await service.get_seu_driver_analysis(
		seu_name="Compressor-1",
		energy_source="electricity",
		requested_driver="temperature",
	)

	assert result["response_mode"] == "training_required"
	assert result["seu_name"] == "Compressor-1"
	assert result["matched_candidate_driver"]["human_name"] == "Outdoor Temperature"


@pytest.mark.asyncio
async def test_driver_analysis_returns_learned_driver_when_baseline_exists(monkeypatch):
	service = DriverAnalysisService()

	seu = {
		"id": uuid4(),
		"name": "Boiler-1",
		"energy_source_id": uuid4(),
		"energy_source_name": "natural_gas",
		"energy_unit": "m3",
		"machine_ids": [uuid4()],
	}
	model_id = uuid4()

	async def fake_get_seu(*args, **kwargs):
		return seu

	async def fake_get_model(*args, **kwargs):
		return {"id": model_id}

	async def fake_get_model_details(*args, **kwargs):
		return {
			"id": model_id,
			"machine_name": "Boiler-1",
			"model_version": 2,
			"r_squared": 0.93,
		}

	def fake_explain_model(*args, **kwargs):
		return {
			"accuracy_explanation": "The model explains most of the observed variance.",
			"formula_explanation": "Energy is driven by temperature and production.",
			"impact_summary": "Temperature dominates.",
			"key_drivers": [
				{
					"feature": "outdoor_temp_c",
					"human_name": "Outdoor Temperature",
					"rank": 1,
					"absolute_impact": 0.84,
					"direction": "increases",
				},
				{
					"feature": "production_count",
					"human_name": "Production Count",
					"rank": 2,
					"absolute_impact": 0.41,
					"direction": "increases",
				},
			],
		}

	monkeypatch.setattr(service, "_get_seu_by_name_and_energy_source", fake_get_seu)
	monkeypatch.setattr(service, "_get_active_model_for_seu", fake_get_model)
	monkeypatch.setattr("services.driver_analysis_service.baseline_service.get_model_details", fake_get_model_details)
	monkeypatch.setattr("services.driver_analysis_service.model_explainer.explain_model", fake_explain_model)

	result = await service.get_seu_driver_analysis(
		seu_name="Boiler-1",
		energy_source="natural_gas",
		requested_driver="temperature",
	)

	assert result["response_mode"] == "trained_baseline"
	assert result["matched_driver"]["human_name"] == "Outdoor Temperature"
	assert result["driver_count"] == 2
