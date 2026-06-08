#!/usr/bin/env python3
"""
Generate the final WASABI / HumanEnerDIA / OVOS-EnMS DOCX package.

This script intentionally reads no private .env file and does not modify
application source code. It produces delivery documents, source Markdown, and
diagram assets under docs/final-delivery/.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import List, Optional, Sequence, Tuple, Union

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor
from PIL import Image, ImageDraw, ImageFont


ROOT = Path("/home/ubuntu/humanergy")
OVOS_ROOT = Path("/home/ubuntu/ovos-llm")
OUT_DIR = ROOT / "docs" / "final-delivery"
ASSET_DIR = OUT_DIR / "assets"
SOURCE_DIR = OUT_DIR / "source"
DOC_DATE = date(2026, 6, 8).isoformat()
PROJECT_NAME = "WASABI / HumanEnerDIA / OVOS-EnMS"
DOC_VERSION = "1.0"
DOC_STATUS = "Final delivery documentation package"


TextBlock = Union[str, Tuple[str, str]]


@dataclass
class Section:
    title: str
    paragraphs: List[TextBlock] = field(default_factory=list)
    bullets: List[str] = field(default_factory=list)
    table: Optional[Tuple[List[str], List[List[str]]]] = None
    figure: Optional[Tuple[str, str]] = None
    subsections: List["Section"] = field(default_factory=list)


@dataclass
class DocSpec:
    filename: str
    title: str
    purpose: str
    audience: str
    evidence_note: str
    sections: List[Section]


def safe_path(path: Path) -> str:
    return str(path)


EVIDENCE = {
    "compose": "docker-compose.yml",
    "compose_ovos_overlay": "scripts/release/docker-compose.ovos.yml",
    "setup": "setup.sh",
    "verify_release": "scripts/verify-wasabi-release.sh",
    "nginx": "nginx/nginx.conf; nginx/conf.d/default.conf",
    "database_schema": "database/init/02-schema.sql; database/init/03-timescaledb-setup.sql; database/init/04-functions.sql",
    "seed_data": "database/init/06-seed-data.sql",
    "analytics_main": "analytics/main.py",
    "analytics_routes": "analytics/api/routes/",
    "analytics_services": "analytics/services/",
    "analytics_models": "analytics/models/",
    "reports": "analytics/api/routes/reports.py; analytics/reports/; analytics/reports_v2/",
    "grafana": "grafana/provisioning/; grafana/dashboards/",
    "nodered": "nodered/data/flows.json; nodered/settings.js; nodered/package.json",
    "simulator": "simulator/main.py; simulator/api/routes.py; simulator/simulator_manager.py; simulator/mqtt_publisher.py",
    "auth": "auth-service/app.py; auth-service/auth_service.py; database/init/05-auth-schema.sql",
    "chatbot": "chatbot/server/index.js; chatbot/rasa/actions/actions.py; chatbot/rasa/qa_data.json",
    "ovos_readme": "/home/ubuntu/ovos-llm/README.md; /home/ubuntu/ovos-llm/enms-ovos-skill/README.md",
    "ovos_bridge": "/home/ubuntu/ovos-llm/enms-ovos-skill/bridge/ovos_rest_bridge.py",
    "ovos_skill": "/home/ubuntu/ovos-llm/enms-ovos-skill/enms_ovos_skill/__init__.py",
    "ovos_parser": "/home/ubuntu/ovos-llm/enms-ovos-skill/enms_ovos_skill/lib/intent_parser.py; lib/adapt_parser.py; lib/llm_parser.py",
    "ovos_validator": "/home/ubuntu/ovos-llm/enms-ovos-skill/enms_ovos_skill/lib/validator.py",
    "ovos_client": "/home/ubuntu/ovos-llm/enms-ovos-skill/enms_ovos_skill/lib/api_client.py",
    "ovos_formatter": "/home/ubuntu/ovos-llm/enms-ovos-skill/enms_ovos_skill/lib/response_formatter.py",
    "ovos_config": "/home/ubuntu/ovos-llm/docker-compose.yml; Dockerfile; enms-ovos-skill/config.yaml.template; settings.docker.json; settingsmeta.yaml",
}


SERVICE_ROWS = [
    ["nginx", "nginx:1.25-alpine", "8080; 8443 mapped but HTTPS server block is optional/commented until certificates are configured", "Public gateway, portal/static hosting, reverse proxy", "Yes"],
    ["postgres", "timescale/timescaledb:latest-pg16", "5433", "PostgreSQL with TimescaleDB extension and persistent data volume", "Yes"],
    ["mqtt", "build ./mqtt", "1883, 9001", "Mosquitto telemetry broker with configured credentials", "Yes"],
    ["redis", "redis:7-alpine", "6380", "Redis cache and Pub/Sub support for analytics event paths", "Yes"],
    ["simulator", "build ./simulator", "internal 8003", "FastAPI synthetic telemetry generator loaded from database machines", "Yes"],
    ["nodered", "build ./nodered", "1881", "MQTT-to-database ingestion and automation flow runtime", "Yes"],
    ["grafana", "grafana/grafana:10.2.0", "3001, /grafana", "Provisioned dashboards backed by PostgreSQL/TimescaleDB", "Yes"],
    ["analytics", "build ./analytics", "8001, /api/analytics", "FastAPI analytics, KPI, reports, ISO 50001, and OVOS proxy APIs", "Yes"],
    ["query-service", "build ./query-service", "8002", "Reserved placeholder; healthcheck disabled and not a readiness signal", "No"],
    ["auth-service", "build ./auth-service", "5500", "Flask auth, admin, contact, pilot/application APIs", "Yes"],
    ["rasa-actions", "build ./chatbot/rasa", "5055", "Rasa custom action server", "Yes"],
    ["rasa", "build ./chatbot/rasa", "5005", "Rasa NLU text chatbot server", "Yes"],
    ["chatbot", "build ./chatbot", "5006", "Express backend and built chatbot frontend proxying to Rasa and OVOS", "Yes"],
]


ACCESS_ROWS = [
    ["Unified portal", "http://<host>:8080", "Served by Nginx from portal/public"],
    ["Grafana", "http://<host>:8080/grafana", "Sub-path proxy to Grafana with provisioned dashboards"],
    ["Analytics UI", "http://<host>:8080/analytics/ui/", "FastAPI-rendered analytics templates"],
    ["Analytics API docs", "http://<host>:8080/api/analytics/docs", "Nginx proxy to analytics OpenAPI docs"],
    ["Simulator docs", "http://<host>:8080/api/simulator/docs", "Nginx proxy to simulator OpenAPI docs"],
    ["Node-RED", "http://<host>:1881 or http://<host>:8080/nodered/", "Admin UI protected by Node-RED credentials"],
    ["OVOS bridge", "http://<host>:5000/health", "Available when OVOS stack/overlay is deployed"],
]


API_ROUTE_ROWS = [
    ["Health and system", "/api/v1/health, /api/v1/stats/system, /api/v1/stats/connections", "analytics/main.py"],
    ["Baselines", "/api/v1/baseline/train, /deviation, /predict, /models, /train-seu", "analytics/api/routes/baseline.py"],
    ["KPIs", "/api/v1/kpi/sec, /peak-demand, /load-factor, /energy-cost, /carbon, /all, /factory", "analytics/api/routes/kpi.py"],
    ["Forecasting", "/api/v1/forecast/train/arima, /train/prophet, /predict, /demand, /peak, /short-term", "analytics/api/routes/forecast.py"],
    ["Anomalies", "/api/v1/anomaly/create, /detect, /search, /recent, /active, /{id}/resolve", "analytics/api/routes/anomaly.py"],
    ["Machines and time series", "/api/v1/machines, /machines/status/{name}, /timeseries/energy, /power, /latest/{id}", "analytics/api/routes/machines.py; timeseries.py"],
    ["ISO 50001 and SEUs", "/api/v1/iso50001/*, /api/v1/seus, /api/v1/reports/seu-performance", "analytics/api/routes/iso50001.py; seu.py; seus.py"],
    ["Reports", "/api/v1/reports/types, /generate, /preview, /v2/generate, /v2/download/{id}, /v2/status", "analytics/api/routes/reports.py"],
    ["OVOS integration", "/api/v1/ovos/*, /api/v1/ovos/voice/query, /voice/health, /voice/config", "analytics/api/routes/ovos.py; ovos_voice.py"],
    ["Visualization data", "/api/v1/sankey/data, /heatmap/hourly, /comparison/machines, /compare/machines", "analytics/api/routes/sankey.py; heatmap.py; comparison.py; compare.py"],
]


KPI_ROWS = [
    ["Specific Energy Consumption", "SEC = total energy kWh / total production units", "calculate_sec() over energy_readings_1hour and production_data_1hour", "database/init/04-functions.sql; /api/v1/kpi/sec"],
    ["Peak demand", "Maximum 15-minute peak_demand_kw in selected period", "calculate_peak_demand() over energy_readings_15min", "database/init/04-functions.sql; /api/v1/kpi/peak-demand"],
    ["Load factor", "Average power divided by maximum power", "calculate_load_factor() over energy_readings_15min", "database/init/04-functions.sql; /api/v1/kpi/load-factor"],
    ["Energy cost", "Energy multiplied by tariff rate; active time-of-use tariff selected when configured", "calculate_energy_cost() queries energy_tariffs with default fallback rate", "database/init/04-functions.sql; /api/v1/kpi/energy-cost"],
    ["Carbon intensity/emissions", "Energy multiplied by active carbon factor, with default factor fallback", "calculate_carbon_intensity() queries carbon_factors", "database/init/04-functions.sql; /api/v1/kpi/carbon"],
    ["Combined KPI response", "Aggregates SEC, peak demand, load factor, cost, and carbon", "calculate_all_kpis() and KPIService.calculate_all_kpis()", "database/init/04-functions.sql; analytics/services/kpi_service.py"],
]


DASHBOARD_ROWS = [
    ["SOTA Factory Overview", "Active machines, energy today, cost today, active anomalies, current power, machine status"],
    ["SOTA Machine Health", "Health score, current power, baseline variance, production, actual vs baseline, anomalies"],
    ["SOTA ISO 50001 EnPI", "EnPI score, energy savings, compliance rate, CUSUM, baseline vs actual, SEU performance"],
    ["SOTA Energy Cost Analytics", "Cost trend, time-of-use cost, top cost contributors, savings opportunities"],
    ["SOTA Environmental Impact", "Monthly carbon footprint, CO2 trend, emission intensity, emissions by machine"],
    ["SOTA Predictive Analytics", "Forecast metrics, forecast vs actual, accuracy trends, recent forecasts"],
    ["SOTA Anomaly Detection", "Active and critical anomalies, severity distribution, machine-hour heatmap, unresolved list"],
    ["SOTA ML Model Performance", "Active models, R2/RMSE, model performance trends, training history"],
    ["SOTA Operational Efficiency", "OEE, availability, performance rate, production vs energy efficiency"],
    ["SOTA Real-Time Production", "Live factory status, active machines, current power"],
    ["SOTA Executive Summary", "Operational concerns, 12-month energy trend, energy intensity, monthly summary"],
]


INTENT_ROWS = [
    ["energy_query", "Energy use questions by machine or factory scope"],
    ["power_query", "Current or historical power demand questions"],
    ["machine_status", "Machine running/offline/status checks"],
    ["factory_overview", "Factory/facility summaries, machine lists, aggregate status"],
    ["comparison", "Machine-to-machine comparisons"],
    ["ranking", "Top or lowest machines by energy, power, cost, efficiency, or alerts"],
    ["anomaly_detection", "Active/recent anomaly and alert queries"],
    ["cost_analysis", "Cost and spending questions"],
    ["forecast", "Forecasted demand and future energy usage"],
    ["baseline, baseline_models, baseline_explanation", "Baseline prediction, model inventory, and driver explanation"],
    ["driver_analysis", "Energy driver analysis for factory or SEU/machine context"],
    ["seus", "Significant Energy Use listing and context"],
    ["kpi, performance, production", "KPIs, performance analysis, production/OEE-related queries"],
    ["report", "Report type, preview, and generation workflows"],
    ["help, health", "Capability help and system health checks"],
]


LIMITATION_ROWS = [
    ["query-service", "Placeholder only; Docker service exists, healthcheck disabled, and it is excluded from release readiness expectations."],
    ["Runtime verification", "This documentation package records compose validation. Live health checks require a running deployment and are not implied unless run separately."],
    ["OVOS release artifact", "The OVOS source tree may contain local GGUF model files, but release notes state optional GGUF weights are not bundled by default."],
    ["Third-party EnMS support", "OVOS portability is through a HumanEnerDIA-compatible API or adapter/proxy, not zero-code support for arbitrary vendor APIs."],
    ["Reports V2", "V2 report code is implemented, but some service calculations use derived/proportional or placeholder values; final stakeholders should review report semantics before audit use."],
    ["Simulator inventory", "The simulator code supports boiler in addition to compressor, HVAC, motor, pump, and injection molding. One simulator info response still lists five machine types."],
    ["Security posture", "The codebase provides secret placeholders, generated first-run credentials, JWT/bcrypt auth, health checks, and hardening guidance. Public production exposure still requires operator DNS/TLS/firewall/credential work."],
]


def load_font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def wrap_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont, max_width: int) -> List[str]:
    words = text.split()
    lines: List[str] = []
    current: List[str] = []
    for word in words:
        trial = " ".join(current + [word])
        width = draw.textbbox((0, 0), trial, font=font)[2]
        if width <= max_width or not current:
            current.append(word)
        else:
            lines.append(" ".join(current))
            current = [word]
    if current:
        lines.append(" ".join(current))
    return lines


def draw_box(draw: ImageDraw.ImageDraw, box: Tuple[int, int, int, int], title: str, body: str, fill: Tuple[int, int, int], outline: Tuple[int, int, int]) -> None:
    x1, y1, x2, y2 = box
    draw.rounded_rectangle(box, radius=12, fill=fill, outline=outline, width=3)
    title_font = load_font(21, True)
    body_font = load_font(16)
    max_width = x2 - x1 - 36

    y = y1 + 14
    for line in wrap_text(draw, title, title_font, max_width):
        draw.text((x1 + 18, y), line, fill=(20, 32, 45), font=title_font)
        y += 26

    y += 8
    for line in wrap_text(draw, body, body_font, max_width):
        if y + 19 > y2 - 12:
            break
        draw.text((x1 + 18, y), line, fill=(42, 54, 68), font=body_font)
        y += 21


def draw_arrow(draw: ImageDraw.ImageDraw, start: Tuple[int, int], end: Tuple[int, int], color=(71, 85, 105)) -> None:
    draw.line([start, end], fill=color, width=4)
    sx, sy = start
    ex, ey = end
    if abs(ex - sx) > abs(ey - sy):
        sign = 1 if ex > sx else -1
        points = [(ex, ey), (ex - sign * 14, ey - 9), (ex - sign * 14, ey + 9)]
    else:
        sign = 1 if ey > sy else -1
        points = [(ex, ey), (ex - 9, ey - sign * 14), (ex + 9, ey - sign * 14)]
    draw.polygon(points, fill=color)


def make_diagram(filename: str, title: str, boxes: Sequence[Tuple[Tuple[int, int, int, int], str, str]], arrows: Sequence[Tuple[Tuple[int, int], Tuple[int, int]]], size=(1500, 900)) -> str:
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    img = Image.new("RGB", size, (248, 250, 252))
    draw = ImageDraw.Draw(img)
    title_font = load_font(34, True)
    draw.text((50, 32), title, fill=(15, 23, 42), font=title_font)
    for start, end in arrows:
        draw_arrow(draw, start, end)
    palette = [
        ((226, 232, 240), (71, 85, 105)),
        ((219, 234, 254), (37, 99, 235)),
        ((220, 252, 231), (22, 101, 52)),
        ((254, 243, 199), (180, 83, 9)),
        ((243, 232, 255), (126, 34, 206)),
    ]
    for idx, (box, title_text, body) in enumerate(boxes):
        fill, outline = palette[idx % len(palette)]
        draw_box(draw, box, title_text, body, fill, outline)
    path = ASSET_DIR / filename
    img.save(path)
    return str(path)


def generate_diagrams() -> dict:
    diagrams = {}
    diagrams["system_context"] = make_diagram(
        "system-context.png",
        "System Context",
        [
            ((70, 150, 360, 310), "Users and Operators", "Portal, Grafana, analytics UI, Rasa chatbot, and OVOS voice/text queries"),
            ((470, 130, 780, 330), "Nginx Gateway", "Public HTTP gateway. Routes portal, APIs, Grafana, Node-RED, auth, chatbot, and OVOS proxy paths. TLS block is optional/commented"),
            ((880, 100, 1240, 250), "HumanEnerDIA Core", "Analytics, simulator, Node-RED, auth-service, chatbot/Rasa, Grafana, query-service placeholder"),
            ((880, 330, 1240, 500), "Data and Messaging", "TimescaleDB/PostgreSQL, Mosquitto MQTT, Redis, Grafana provisioning, persistent volumes"),
            ((470, 520, 780, 710), "OVOS-EnMS Layer", "OVOS REST bridge, messagebus, EnMS skill, parser, validator, API client, response formatter"),
        ],
        [
            ((360, 230), (470, 230)),
            ((780, 230), (880, 180)),
            ((1060, 250), (1060, 330)),
            ((630, 520), (880, 440)),
            ((780, 615), (900, 240)),
        ],
    )
    diagrams["telemetry_flow"] = make_diagram(
        "telemetry-data-flow.png",
        "Telemetry and Analytics Data Flow",
        [
            ((70, 150, 330, 300), "Simulator / Devices", "Publishes factory telemetry streams to MQTT"),
            ((430, 150, 690, 300), "MQTT Broker", "Mosquitto receives factory/# telemetry streams"),
            ((790, 150, 1060, 330), "Node-RED", "Parses topics, routes by type, validates payloads, and writes to PostgreSQL"),
            ((1160, 150, 1440, 330), "TimescaleDB", "Raw hypertables and 1min/15min/1hour/1day continuous aggregates"),
            ((790, 500, 1060, 680), "Analytics APIs", "KPIs, baselines, forecasts, anomalies, reports, ISO 50001, OVOS-facing responses"),
            ((1150, 500, 1450, 690), "Dashboards and Reports", "Grafana dashboards, analytics UI, PDF/report endpoints, Rasa/OVOS consumers"),
        ],
        [
            ((330, 225), (430, 225)),
            ((690, 225), (790, 225)),
            ((1060, 240), (1160, 240)),
            ((1300, 330), (1060, 540)),
            ((1060, 590), (1160, 590)),
        ],
    )
    diagrams["ovos_lifecycle"] = make_diagram(
        "ovos-query-lifecycle.png",
        "OVOS Query Lifecycle",
        [
            ((50, 150, 290, 310), "User / Portal", "Natural-language text or voice-derived request"),
            ((340, 150, 580, 330), "REST Bridge", "POST /query or /query/voice emits recognizer_loop:utterance"),
            ((630, 150, 870, 330), "OVOS Messagebus", "Carries utterance, speak event, and enms.skill.response payloads"),
            ((920, 150, 1160, 330), "EnMS Skill", "Parser, validator, API client, handlers, context, and response formatter"),
            ((1210, 150, 1450, 330), "HumanEnerDIA API", "Configured HumanEnerDIA-compatible /api/v1 backend"),
            ((1210, 500, 1450, 680), "Response", "Bridge returns voice text, data, insights, and optional report metadata"),
        ],
        [
            ((290, 230), (340, 230)),
            ((580, 230), (630, 230)),
            ((870, 230), (920, 230)),
            ((1160, 230), (1210, 230)),
            ((1330, 330), (1330, 500)),
        ],
    )
    diagrams["deployment_flow"] = make_diagram(
        "deployment-startup-flow.png",
        "Deployment Startup Flow",
        [
            ((70, 150, 360, 310), "Prepare Host", "Docker Engine and Compose v2, repository or release bundle, .env.example available"),
            ((470, 150, 760, 330), "setup.sh", "Creates .env if needed, generates first-run secrets, updates URLs, selects OVOS overlay when present"),
            ((870, 150, 1160, 330), "Compose Validation", "docker compose config validates base stack and optional OVOS overlay"),
            ((470, 510, 760, 690), "Build and Start", "docker compose build and up -d, optionally with --wait"),
            ((870, 510, 1160, 690), "Verify", "Health endpoints, release verifier, smoke query when OVOS is deployed"),
        ],
        [
            ((360, 230), (470, 230)),
            ((760, 240), (870, 240)),
            ((1010, 330), (760, 560)),
            ((760, 600), (870, 600)),
        ],
    )
    diagrams["docker_topology"] = make_diagram(
        "docker-service-topology.png",
        "Docker Service Topology",
        [
            ((60, 150, 330, 310), "Host Access", "Browser/API users reach Nginx on 8080. Direct ports are mapped for selected operations services"),
            ((420, 130, 700, 330), "Nginx", "Routes portal, analytics, Grafana, Node-RED, auth, chatbot, simulator, and OVOS proxy paths"),
            ((790, 130, 1090, 330), "App Services", "analytics, auth-service, chatbot, Rasa, rasa-actions, simulator, query-service placeholder"),
            ((1180, 130, 1460, 330), "Data Services", "PostgreSQL/TimescaleDB, MQTT broker, Redis, named persistent volumes"),
            ((420, 500, 700, 680), "Operator UIs", "Grafana dashboards, Node-RED editor, analytics UI, static portal"),
            ((790, 500, 1090, 680), "Optional OVOS", "OVOS bridge, messagebus, EnMS skill joined to enms-network"),
        ],
        [
            ((330, 230), (420, 230)),
            ((700, 230), (790, 230)),
            ((1090, 230), (1180, 230)),
            ((560, 330), (560, 500)),
            ((940, 500), (940, 330)),
            ((700, 590), (790, 590)),
        ],
    )
    return diagrams


def set_cell_text(cell, text: str, bold: bool = False) -> None:
    cell.text = ""
    p = cell.paragraphs[0]
    run = p.add_run(text)
    run.bold = bold
    run.font.size = Pt(8.5)
    cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.TOP


def shade_cell(cell, fill: str) -> None:
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), fill)
    tc_pr.append(shd)


def set_repeat_table_header(row) -> None:
    tr_pr = row._tr.get_or_add_trPr()
    tbl_header = OxmlElement("w:tblHeader")
    tbl_header.set(qn("w:val"), "true")
    tr_pr.append(tbl_header)


def add_table(doc: Document, headers: Sequence[str], rows: Sequence[Sequence[str]]) -> None:
    table = doc.add_table(rows=1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.style = "Table Grid"
    header_cells = table.rows[0].cells
    for idx, header in enumerate(headers):
        set_cell_text(header_cells[idx], header, bold=True)
        shade_cell(header_cells[idx], "D9EAF7")
    set_repeat_table_header(table.rows[0])
    for row in rows:
        cells = table.add_row().cells
        for idx, value in enumerate(row):
            set_cell_text(cells[idx], value)
    doc.add_paragraph()


def configure_document(doc: Document) -> None:
    styles = doc.styles
    styles["Normal"].font.name = "Aptos"
    styles["Normal"].font.size = Pt(10)
    styles["Title"].font.name = "Aptos Display"
    styles["Title"].font.size = Pt(26)
    styles["Heading 1"].font.name = "Aptos Display"
    styles["Heading 1"].font.size = Pt(16)
    styles["Heading 1"].font.bold = True
    styles["Heading 1"].font.color.rgb = RGBColor(15, 23, 42)
    styles["Heading 2"].font.name = "Aptos Display"
    styles["Heading 2"].font.size = Pt(13)
    styles["Heading 2"].font.bold = True
    styles["Heading 2"].font.color.rgb = RGBColor(30, 64, 175)
    for section in doc.sections:
        section.top_margin = Inches(0.65)
        section.bottom_margin = Inches(0.65)
        section.left_margin = Inches(0.65)
        section.right_margin = Inches(0.65)


def add_footer(doc: Document, title: str) -> None:
    for section in doc.sections:
        footer = section.footer
        p = footer.paragraphs[0]
        p.text = f"{PROJECT_NAME} | {title} | Version {DOC_VERSION} | {DOC_DATE}"
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in p.runs:
            run.font.size = Pt(8)
            run.font.color.rgb = RGBColor(100, 116, 139)


def add_title_page(doc: Document, spec: DocSpec) -> None:
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(PROJECT_NAME)
    run.bold = True
    run.font.size = Pt(16)
    run.font.color.rgb = RGBColor(30, 64, 175)

    doc.add_paragraph()
    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = title.add_run(spec.title)
    run.bold = True
    run.font.size = Pt(26)
    run.font.color.rgb = RGBColor(15, 23, 42)

    doc.add_paragraph()
    meta = doc.add_table(rows=5, cols=2)
    meta.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta.style = "Table Grid"
    rows = [
        ["Version", DOC_VERSION],
        ["Date", DOC_DATE],
        ["Status", DOC_STATUS],
        ["Purpose", spec.purpose],
        ["Intended audience", spec.audience],
    ]
    for row_idx, row in enumerate(rows):
        for col_idx, value in enumerate(row):
            set_cell_text(meta.rows[row_idx].cells[col_idx], value, bold=(col_idx == 0))
            if col_idx == 0:
                shade_cell(meta.rows[row_idx].cells[col_idx], "E2E8F0")
    doc.add_paragraph()
    note = doc.add_paragraph()
    note.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = note.add_run("Evidence rule: ")
    r.bold = True
    note.add_run(spec.evidence_note)
    doc.add_page_break()


def add_toc(doc: Document, spec: DocSpec) -> None:
    doc.add_heading("Table of Contents", level=1)
    for idx, section in enumerate(spec.sections, start=1):
        doc.add_paragraph(f"{idx}. {section.title}")
        for sub_idx, sub in enumerate(section.subsections, start=1):
            doc.add_paragraph(f"{idx}.{sub_idx} {sub.title}", style="List Bullet")
    doc.add_page_break()


def add_text_block(paragraph, block: TextBlock) -> None:
    if isinstance(block, tuple):
        label, text = block
        run = paragraph.add_run(label.rstrip())
        run.bold = True
        paragraph.add_run(f" {text.lstrip()}")
    else:
        paragraph.add_run(block)


def add_section(doc: Document, section: Section, level: int = 1) -> None:
    doc.add_heading(section.title, level=level)
    if section.figure:
        image_name, caption = section.figure
        image_path = ASSET_DIR / image_name
        if image_path.exists():
            doc.add_picture(str(image_path), width=Inches(6.7))
            cap = doc.add_paragraph(caption)
            cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for run in cap.runs:
                run.italic = True
                run.font.size = Pt(8.5)
    for para in section.paragraphs:
        p = doc.add_paragraph()
        add_text_block(p, para)
    for bullet in section.bullets:
        doc.add_paragraph(bullet, style="List Bullet")
    if section.table:
        add_table(doc, section.table[0], section.table[1])
    for sub in section.subsections:
        add_section(doc, sub, level=min(level + 1, 3))


def build_document(spec: DocSpec) -> None:
    doc = Document()
    configure_document(doc)
    add_title_page(doc, spec)
    add_toc(doc, spec)
    for section in spec.sections:
        add_section(doc, section)
    add_footer(doc, spec.title)
    output = OUT_DIR / spec.filename
    doc.save(output)


def section_evidence(rows: Sequence[Sequence[str]]) -> Section:
    return Section(
        "Evidence References",
        paragraphs=[
            "The table below lists the main local evidence used for this document. It is not a full file inventory; it identifies the sources behind the material claims."
        ],
        table=(["Topic", "Evidence"], rows),
    )


def common_limitations_section() -> Section:
    return Section(
        "Limitations And Assumptions",
        paragraphs=[
            "The following items should be reviewed before stakeholder distribution. They are documented to avoid overstating the current implementation."
        ],
        table=(["Item", "Status"], LIMITATION_ROWS),
    )


def build_system_architecture(diagrams: dict) -> DocSpec:
    return DocSpec(
        filename="System Architecture Report.docx",
        title="System Architecture Report",
        purpose="Describe the implemented HumanEnerDIA / EnMS architecture and the OVOS-EnMS integration boundary.",
        audience="Project managers, technical reviewers, deployment stakeholders, and external partners.",
        evidence_note="Claims are tied to local source code, Docker configuration, SQL initialization files, and verified compose validation.",
        sections=[
            Section(
                "Executive Summary",
                paragraphs=[
                    "HumanEnerDIA is implemented as a Docker Compose based industrial energy management stack. It combines an Nginx gateway, a static portal, FastAPI analytics APIs, PostgreSQL/TimescaleDB storage, MQTT telemetry, Node-RED ingestion, Grafana dashboards, a simulator, authentication services, a Rasa text chatbot path, and an optional OVOS-EnMS voice/natural-language assistant layer.",
                    "The OVOS-EnMS component is a separate assistant runtime that connects to the HumanEnerDIA-compatible analytics API. Its REST bridge does not calculate energy answers by itself; it forwards user queries to the OVOS messagebus, where the EnMS skill parses, validates, executes API calls, and formats responses.",
                    ("Observed in code/config: ", "The base stack is defined in docker-compose.yml. The full-stack release can add OVOS through scripts/release/docker-compose.ovos.yml or the OVOS repository compose file under /home/ubuntu/ovos-llm."),
                ],
            ),
            Section(
                "System Context",
                figure=("system-context.png", "Figure 1. System context and product boundaries."),
                paragraphs=[
                    "The system has three boundaries that must remain distinct in delivery documentation. HumanEnerDIA / EnMS is the energy management backend and visualization stack. OVOS-EnMS is the voice/natural-language assistant layer that integrates with the analytics API. The Rasa chatbot is a text-oriented help and knowledge path, not the same runtime as the OVOS skill.",
                ],
                table=(
                    ["Boundary", "Included components", "Evidence"],
                    [
                        ["HumanEnerDIA / EnMS", "Nginx, portal, analytics, PostgreSQL/TimescaleDB, MQTT, Node-RED, Grafana, simulator, auth-service, Rasa/chatbot services", EVIDENCE["compose"]],
                        ["OVOS-EnMS", "OVOS runtime, REST bridge, messagebus, EnMS skill, parser, validator, API client, response formatter", EVIDENCE["ovos_skill"]],
                        ["External users/integrators", "Browser users, API clients, OVOS clients, operators, WASABI release reviewers", "README.md; docs/README.md; docs/OPERATIONS_RUNBOOK.md"],
                    ],
                ),
            ),
            Section(
                "Runtime Services",
                paragraphs=[
                    "The base runtime service inventory below is taken from docker-compose.yml and verified by docker compose config --quiet during this documentation pass."
                ],
                table=(["Service", "Image or build context", "External port/path", "Responsibility", "Healthcheck"], SERVICE_ROWS),
            ),
            Section(
                "Data And Message Flow",
                figure=("telemetry-data-flow.png", "Figure 2. Telemetry ingestion and analytics data flow."),
                paragraphs=[
                    "Synthetic factory data or external device data enters through MQTT. Node-RED subscribes to factory/#, parses the topic structure, routes by payload type, validates required fields, and writes energy, production, environmental, and status data into PostgreSQL.",
                    "TimescaleDB hypertables and continuous aggregates provide raw and aggregated time-series views. The analytics service reads from those tables and aggregate views to support KPIs, baselines, forecasts, anomalies, reports, Grafana dashboards, and OVOS-facing responses.",
                ],
                table=(
                    ["Stage", "Observed implementation", "Evidence"],
                    [
                        ["Telemetry source", "simulator loads active machines from PostgreSQL and publishes MQTT messages for energy, production, environmental, status, and multi-energy boiler topics", EVIDENCE["simulator"]],
                        ["Broker", "mqtt service exposes 1883 and websocket 9001 with credentials supplied through environment variables", EVIDENCE["compose"]],
                        ["Ingestion", "Node-RED flow includes Subscribe: factory/#, Parse Topic, Route by Type, Process Energy/Production/Environmental/Status, and PostgreSQL output nodes", EVIDENCE["nodered"]],
                        ["Storage", "energy_readings, production_data, and environmental_data are converted to TimescaleDB hypertables with continuous aggregates", EVIDENCE["database_schema"]],
                        ["Consumption", "Analytics API, Grafana dashboards, portal, chatbot, and OVOS integration consume database-backed data", EVIDENCE["analytics_main"]],
                    ],
                ),
            ),
            Section(
                "External And Internal Interfaces",
                paragraphs=[
                    "External browser access normally enters through Nginx. Direct service ports are exposed for operations and development; production exposure should be restricted by firewall or reverse proxy policy."
                ],
                table=(["Interface", "Route or endpoint", "Evidence/notes"], ACCESS_ROWS + [
                    ["Analytics health", "Direct service path /api/v1/health; through Nginx analytics proxy /api/analytics/api/v1/health", "analytics/main.py; nginx/conf.d/default.conf"],
                    ["OVOS proxy via EnMS", "/api/ovos/* -> /api/v1/ovos/*", "nginx/conf.d/default.conf; analytics/api/routes/ovos_voice.py"],
                    ["OVOS direct bridge", "POST /query, POST /query/voice, GET /health", EVIDENCE["ovos_bridge"]],
                ]),
            ),
            Section(
                "OVOS-EnMS Integration",
                figure=("ovos-query-lifecycle.png", "Figure 3. OVOS request and response lifecycle."),
                paragraphs=[
                    "The OVOS bridge receives text queries through /query or /query/voice. It emits recognizer_loop:utterance to the OVOS messagebus and listens for speak and enms.skill.response events. The skill handles intent routing, context, validation, backend API calls, and deterministic response formatting.",
                    "HumanEnerDIA also exposes /api/v1/ovos/voice/query and /api/v1/ovos/voice/health as a proxy route from the analytics service to the OVOS bridge. This supports portal-side integration without making the portal responsible for OVOS messagebus details.",
                ],
            ),
            Section(
                "Security And Operational Considerations",
                paragraphs=[
                    "The repository supports several operational controls, but public production hardening remains an operator responsibility. The setup helper creates .env from .env.example when needed and generates first-run secrets for database, Grafana, Node-RED, Redis, MQTT, JWT, and API key values.",
                    "Authentication is implemented by auth-service using bcrypt password hashing, JWT sessions, email verification and password reset flows, admin allow-listing from environment variables, session tracking, and audit tables. Node-RED has admin authentication configured through environment-provided credentials.",
                ],
                bullets=[
                    "Do not commit .env, generated secrets, runtime logs, database dumps, model caches, or Docker volumes.",
                    "Restrict direct exposure of PostgreSQL, Redis, MQTT, Grafana, Node-RED, and service debug ports in production.",
                    "Terminate TLS at Nginx or an upstream reverse proxy before internet-facing deployment.",
                    "Rotate credentials before public use, especially any generated first-run secrets.",
                ],
            ),
            common_limitations_section(),
            section_evidence([
                ["Runtime topology", EVIDENCE["compose"]],
                ["OVOS overlay", EVIDENCE["compose_ovos_overlay"]],
                ["Routing", EVIDENCE["nginx"]],
                ["Database and KPIs", EVIDENCE["database_schema"]],
                ["Analytics API", EVIDENCE["analytics_main"]],
                ["OVOS bridge and skill", f"{EVIDENCE['ovos_bridge']}; {EVIDENCE['ovos_skill']}"],
                ["Compose validation", "docker compose config --quiet returned success for /home/ubuntu/humanergy and /home/ubuntu/ovos-llm"],
            ]),
        ],
    )


def build_software_design() -> DocSpec:
    return DocSpec(
        filename="Software Design Documentation.docx",
        title="Software Design Documentation",
        purpose="Document the implemented software modules, interfaces, data model, and design constraints.",
        audience="Developers, maintainers, technical reviewers, and integration engineers.",
        evidence_note="Claims prefer route registration, service code, SQL schema, compose files, and tests over README-level descriptions.",
        sections=[
            Section(
                "Design Overview",
                paragraphs=[
                    "HumanEnerDIA uses a service-oriented design. Nginx centralizes browser and API routing; analytics owns most domain APIs; PostgreSQL/TimescaleDB owns persistent operational and time-series data; MQTT and Node-RED connect telemetry ingestion; Grafana presents dashboards; simulator produces demo telemetry; auth-service owns user/account workflows; Rasa/chatbot provides a text help assistant; OVOS-EnMS provides a separate assistant layer.",
                    "The repository favors explicit route modules and service modules rather than a single monolithic backend. The analytics service mounts routers for baselines, anomalies, KPIs, machines, forecasts, time series, visualization data, model performance, production, SEU/ISO 50001 features, reports, and OVOS-facing integration.",
                ],
            ),
            Section(
                "Module Responsibility Matrix",
                table=(
                    ["Subsystem", "Responsibilities", "Primary evidence"],
                    [
                        ["analytics/api/routes", "FastAPI request handlers and route-specific request/response behavior", EVIDENCE["analytics_routes"]],
                        ["analytics/services", "Business logic for KPIs, baselines, forecasts, anomaly handling, performance, event publishing, reports, and Redis coordination", EVIDENCE["analytics_services"]],
                        ["analytics/models", "ML/statistical model implementations and model persistence helpers", EVIDENCE["analytics_models"]],
                        ["database/init", "First-start schema, hypertables, continuous aggregates, SQL functions, seed data, ISO 50001 and model-performance tables", EVIDENCE["database_schema"]],
                        ["simulator", "FastAPI control endpoints, machine simulation classes, MQTT publisher, auto anomaly injection support", EVIDENCE["simulator"]],
                        ["nodered", "MQTT topic parsing, data validation, and PostgreSQL write pipeline", EVIDENCE["nodered"]],
                        ["auth-service", "Registration, login, JWT verification, admin APIs, email verification/reset, pilot/contact forms", EVIDENCE["auth"]],
                        ["chatbot/rasa", "Text help chatbot, QA retrieval actions, Rasa runtime, Express proxy backend", EVIDENCE["chatbot"]],
                    ],
                ),
            ),
            Section(
                "Analytics Service Design",
                paragraphs=[
                    "The analytics service is a FastAPI application with lifespan-managed database connection, optional Redis event subscriber, scheduler startup, route registration, CORS middleware, request logging, timeout handling, and generic exception handling.",
                    "Router registration in analytics/main.py shows the implemented surface: baseline, anomaly, KPI, machines, forecast, time series, sankey, heatmap, comparison, model performance, stats, production, SEU/factory/performance/ISO 50001/multi-energy, OVOS, OVOS voice proxy, and reports.",
                ],
                table=(["API area", "Representative endpoints", "Evidence"], API_ROUTE_ROWS),
            ),
            Section(
                "Database And Schema Design",
                paragraphs=[
                    "The database initialization files create core dimensions, time-series facts, current-state tables, baseline/anomaly/tariff/carbon/audit tables, auth tables, ISO 50001 tables, model-performance tables, forecast output tables, and action-plan workflow tables.",
                    "TimescaleDB is used for high-frequency time-series storage. The initialization scripts create hypertables for energy_readings, production_data, environmental_data, and energy_forecasts, plus continuous aggregates at 1 minute, 15 minutes, 1 hour, and 1 day where implemented.",
                ],
                table=(
                    ["Database object group", "Implemented objects", "Evidence"],
                    [
                        ["Core entities", "factories, machines, energy_readings, production_data, environmental_data, machine_status", "database/init/02-schema.sql"],
                        ["Analytics metadata", "energy_baselines, anomalies, energy_tariffs, carbon_factors, model performance/training/alert tables", "database/init/02-schema.sql; 11-13 model scripts"],
                        ["ISO 50001", "energy_sources, seus, seu_energy_performance, enpi_baselines, enpi_performance, energy_targets, action_plans", "database/init/07-iso50001-schema.sql; 15-16 scripts"],
                        ["Aggregates", "energy, production, and environmental aggregate materialized views", "database/init/03-timescaledb-setup.sql"],
                        ["KPI functions", "calculate_sec, calculate_peak_demand, calculate_load_factor, calculate_energy_cost, calculate_carbon_intensity, calculate_all_kpis", "database/init/04-functions.sql"],
                    ],
                ),
            ),
            Section(
                "Simulator And Ingestion Design",
                paragraphs=[
                    "The simulator is a FastAPI service with lifecycle initialization. It connects to PostgreSQL, connects to MQTT, loads active machines from the database, creates simulator instances by machine type, and can auto-start based on configuration.",
                    "Machine implementations generate energy, production, environmental, and status payloads. The boiler path supports multi-energy publication for electricity, natural gas, and steam style payloads. Node-RED processes subscribed MQTT traffic and writes normalized records into the database.",
                ],
                table=(
                    ["Area", "Design details", "Evidence"],
                    [
                        ["Control API", "start, stop, runtime config, status, list machines, machine detail, inject/clear anomaly, info", "simulator/api/routes.py"],
                        ["Machine loading", "Loads active machines from database with type, rated_power_kw, interval, and MQTT topic", "simulator/simulator_manager.py"],
                        ["MQTT publishing", "Publishes energy, multi-energy, production, environmental, and retained status messages", "simulator/mqtt_publisher.py"],
                        ["Node-RED flow", "Subscribe: factory/#, Parse Topic, Route by Type, Process Energy/Production/Environmental/Status", "nodered/data/flows.json"],
                    ],
                ),
            ),
            Section(
                "Authentication, Portal, And Chatbot Design",
                paragraphs=[
                    "auth-service is a Flask application backed by demo_users, demo_sessions, demo_audit_log, and pilot_factory_applications tables. It implements registration, login, JWT verification, email verification, password reset, admin user management, CSV export, pilot factory application workflows, and contact form handling.",
                    "The portal is static HTML/CSS/JS served by Nginx. It includes general pages, authentication pages, admin pages, report pages, and an OVOS voice widget script. The chatbot backend is an Express service that serves the built frontend and proxies to Rasa and OVOS endpoints.",
                    "The Rasa custom action loads qa_data.json and retrieves knowledge/help answers using exact match, special cases, keyword routing, abbreviation expansion, misspelling correction, and fuzzy-style matching logic. This is a text help path; it should not be confused with live OVOS operational queries.",
                ],
            ),
            Section(
                "Configuration, Validation, Logging, And Error Handling",
                bullets=[
                    "Configuration is primarily environment-driven through .env.example, docker-compose.yml, analytics/config.py, simulator/config.py, Node-RED settings, and OVOS settings/config files.",
                    "The setup helper preserves existing non-placeholder .env values, generates missing first-run secrets, validates Compose, builds images, and starts services.",
                    "FastAPI services use health endpoints, request logging, validation exception handlers, and generic exception handlers.",
                    "OVOS skill validation uses Pydantic schemas, confidence thresholding, machine whitelists, fuzzy matching, metric validation, time-range parsing, and entity normalization.",
                    "auth-service uses bcrypt password hashing, JWT sessions, email verification gates, admin decorators, and parameterized SQL queries.",
                ],
            ),
            Section(
                "Known Design Gaps And Placeholders",
                table=(["Gap or caution", "Evidence-based status"], [
                    ["query-service", "Only Dockerfile and empty route/schema/service folders observed; compose healthcheck disabled."],
                    ["Report V2 semantics", "V2 routes and generator exist, but some service values are proportional or placeholder-derived, such as efficiency sparkline and estimated baseline cost."],
                    ["Simulator machine list inconsistency", "Code supports boiler; simulator info endpoint text still lists five machine types."],
                    ["Direct public exposure", "Several internal service ports are externally mapped for development/ops; production hardening requires operator firewall/TLS review."],
                    ["README claims", "Root README contains high-level feature claims; final documents use code/config evidence where details differ."],
                ]),
            ),
            section_evidence([
                ["Analytics app and routers", f"{EVIDENCE['analytics_main']}; {EVIDENCE['analytics_routes']}"],
                ["SQL schema/functions", EVIDENCE["database_schema"]],
                ["Simulator", EVIDENCE["simulator"]],
                ["Node-RED", EVIDENCE["nodered"]],
                ["Auth", EVIDENCE["auth"]],
                ["Chatbot/Rasa", EVIDENCE["chatbot"]],
                ["Tests", "analytics/tests/test_*.py; /home/ubuntu/ovos-llm/enms-ovos-skill/tests/test_*.py"],
            ]),
        ],
    )


def build_skill_doc(diagrams: dict) -> DocSpec:
    return DocSpec(
        filename="Skill Documentation.docx",
        title="Skill Documentation",
        purpose="Document the OVOS-EnMS skill, REST bridge, parser, validation, API client, and response behavior.",
        audience="OVOS integrators, WASABI technical reviewers, backend maintainers, and external partners.",
        evidence_note="OVOS-EnMS evidence comes from /home/ubuntu/ovos-llm, with HumanEnerDIA API integration evidence from /home/ubuntu/humanergy.",
        sections=[
            Section(
                "Purpose And Boundaries",
                paragraphs=[
                    "The HumanEnerDIA OVOS skill is the natural-language assistant layer for industrial energy-management questions. It is not the HumanEnerDIA backend and does not own telemetry storage or KPI calculation. It connects to a reachable HumanEnerDIA-compatible analytics API.",
                    "The production integration boundary is the HumanEnerDIA-compatible REST API. The repository includes adapter abstractions, but v1.0.0 documentation states that arbitrary third-party EnMS APIs require an adapter or proxy that exposes the expected API contract.",
                ],
            ),
            Section(
                "Deployment And Configuration",
                paragraphs=[
                    "The OVOS repository provides a Docker Compose service that exposes the REST bridge on port 5000 and the OVOS messagebus on port 8181. The full-stack HumanEnerDIA release can include an OVOS overlay that builds from ./ovos-stack and joins the enms-network.",
                    "Key configuration includes ENMS_API_URL, OVOS_BRIDGE_PORT, STRUCTURED_RESPONSE_GRACE_SECONDS, OVOS_TTS_ENABLED, LOG_LEVEL, OVOS_CONFIG_PATH, and XDG_CONFIG_HOME. Skill-level settings include enms_api_base_url, llm_model_path, confidence_threshold, and progress feedback options.",
                ],
                table=(
                    ["Configuration item", "Observed default or behavior", "Evidence"],
                    [
                        ["ENMS_API_URL", "Docker default points at a HumanEnerDIA-compatible /api/v1 backend", "/home/ubuntu/ovos-llm/docker-compose.yml"],
                        ["enms_api_base_url", "Skill setting for backend API URL", "settings.docker.json; settingsmeta.yaml"],
                        ["confidence_threshold", "Default 0.85 in settings and validator configuration", "settings.docker.json; lib/validator.py"],
                        ["INSTALL_LLM_FALLBACK", "Build argument for installing optional LLM dependencies in the Dockerfile", "/home/ubuntu/ovos-llm/Dockerfile"],
                    ],
                ),
            ),
            Section(
                "Query Lifecycle",
                figure=("ovos-query-lifecycle.png", "Figure 1. REST bridge, messagebus, skill, API, and response lifecycle."),
                paragraphs=[
                    "The REST bridge exposes GET /health and POST /query. POST /query/voice is an alias used by the analytics proxy when audio-capable flows request the same bridge behavior.",
                    "For each query, the bridge creates or uses a session id, emits recognizer_loop:utterance to the OVOS messagebus, and waits for a speak message plus, when available, an enms.skill.response structured payload. The response returns success status, spoken response text, intent, confidence, data, insights, timestamp, and session id.",
                    "The EnMS skill receives the utterance through OVOS intent handlers or fallback handling. It parses the utterance, validates intent/entity output, calls the configured backend API, formats a deterministic response, speaks it, and emits structured response data for the bridge or portal widget.",
                ],
            ),
            Section(
                "Supported Intent And Query Families",
                paragraphs=[
                    "The active IntentType enum and skill handlers show the supported query families below. This table is not a guarantee that every phrasing is understood; it identifies implemented categories in the skill code."
                ],
                table=(["Intent family", "Purpose"], INTENT_ROWS),
            ),
            Section(
                "Intent Parsing And Routing",
                paragraphs=[
                    "The parser is hybrid. Tier 1 is regex-based heuristic routing for common operational queries. Tier 2 uses Adapt pattern matching and registered vocabulary. Tier 3 is an optional local Qwen GGUF LLM parser used as fallback when dependencies and model files are available.",
                    "The active parser code includes patterns for production, anomaly detection, forecasts, KPIs, performance, baselines, driver analysis, SEUs, rankings, factory overview, status, power, and related query types. Adapt vocabulary registers machine names, spoken number variants, energy/power/status/cost/KPI/factory/comparison/time/forecast/anomaly/help terms and more.",
                ],
                table=(
                    ["Tier", "Implementation", "Important note"],
                    [
                        ["Heuristic", "Regex patterns in lib/intent_parser.py", "Fast path for common operational wording."],
                        ["Adapt", "IntentDeterminationEngine in lib/adapt_parser.py", "Pattern/vocabulary matching with registered machine and domain terms."],
                        ["LLM", "Qwen3Parser in lib/llm_parser.py", "Optional fallback requiring llama-cpp-python and a GGUF model file."],
                    ],
                ),
            ),
            Section(
                "Validation And Fuzzy Matching",
                paragraphs=[
                    "Validation is deliberately conservative. The validator builds a Pydantic Intent model, checks confidence, rejects unknown intent types, validates machine names against a whitelist, supports fuzzy matching and number-word normalization, detects ambiguity, validates multi-machine comparisons, and performs soft metric validation.",
                    "Machine discovery can refresh the whitelist from the backend API during runtime; fallback machine names are configured for cases where API discovery fails. This helps prevent hallucinated machine names from becoming backend calls.",
                ],
            ),
            Section(
                "Backend API Client And Adapter Behavior",
                paragraphs=[
                    "The ENMSClient wraps async HTTP calls to the configured backend. It uses connection pooling, request timeout management, and tenacity retry behavior that retries connection/timeouts and server-side 5xx responses while avoiding retries on ordinary 4xx client errors.",
                    "Client methods cover health, stats, machines, time series, top consumers, anomalies, KPIs, performance opportunities, action plans, forecasts, baseline models/explanations, SEU/energy-source data, reports, and ISO 50001 EnPI/action-plan endpoints. The production path remains HumanEnerDIA-compatible API usage.",
                ],
                table=(
                    ["Client area", "Representative methods", "Evidence"],
                    [
                        ["System and machines", "health_check, system_stats, factory_summary, list_machines, get_machine_status", EVIDENCE["ovos_client"]],
                        ["Telemetry", "get_energy_timeseries, get_power_timeseries, get_latest_reading, get_multi_machine_energy", EVIDENCE["ovos_client"]],
                        ["Analytics", "detect_anomalies, get_all_kpis, analyze_performance, forecast_demand, predict_baseline", EVIDENCE["ovos_client"]],
                        ["Reports and ISO", "get_enpi_report, list_action_plans, get_report_types, preview_report, generate_report", EVIDENCE["ovos_client"]],
                    ],
                ),
            ),
            Section(
                "Response Formatting",
                paragraphs=[
                    "The response formatter uses Jinja2 templates and custom number/unit/time filters. The formatter documentation and code explicitly state that final responses should come from API data and templates rather than free-form LLM generation.",
                    "Additional enrichment exists for anomaly responses, including severity grouping, resolved/unresolved counts, metric/anomaly label humanization, and concise spoken examples.",
                ],
            ),
            Section(
                "Example Supported Queries",
                bullets=[
                    "What is the power of Compressor-1?",
                    "Is HVAC-Main running?",
                    "How much energy did Boiler-1 use yesterday?",
                    "Show me the top three energy consumers.",
                    "Any anomalies today?",
                    "What is tomorrow's energy forecast?",
                    "Give me a factory overview.",
                    "List SEUs.",
                    "Generate a monthly energy report.",
                ],
            ),
            Section(
                "Optional LLM Fallback",
                paragraphs=[
                    "The default release documentation states that fast heuristic and Adapt routing are the normal path and that large GGUF model files are not bundled by default. The local development tree contains model files, but release packaging excludes models. To enable local LLM fallback in the release path, the operator must provide the GGUF model under the skill models directory and build with INSTALL_LLM_FALLBACK=true.",
                    "The LLM parser uses llama-cpp-python when installed, loads a configured GGUF model, performs deterministic JSON intent classification, and returns None on missing dependencies, missing model, parse failures, or timeout. It should be documented as optional fallback, not as required normal operation.",
                ],
            ),
            common_limitations_section(),
            section_evidence([
                ["REST bridge", EVIDENCE["ovos_bridge"]],
                ["Skill lifecycle and handlers", EVIDENCE["ovos_skill"]],
                ["Intent parser tiers", EVIDENCE["ovos_parser"]],
                ["Validation", EVIDENCE["ovos_validator"]],
                ["API client", EVIDENCE["ovos_client"]],
                ["Response formatter", EVIDENCE["ovos_formatter"]],
                ["Configuration and deployment", EVIDENCE["ovos_config"]],
            ]),
        ],
    )


def build_kpi_doc(diagrams: dict) -> DocSpec:
    return DocSpec(
        filename="Energy Management System Reports and KPI Reports.docx",
        title="Energy Management System Reports and KPI Reports",
        purpose="Document implemented energy data, KPI, dashboard, and report capabilities with formulas and evidence.",
        audience="Energy managers, project reviewers, operators, analytics maintainers, and external partners.",
        evidence_note="KPI formulas are included only where defined in SQL functions, code, dashboard queries, or existing local documentation.",
        sections=[
            Section(
                "Energy Data Model",
                figure=("telemetry-data-flow.png", "Figure 1. Data path from telemetry to KPI/report consumers."),
                paragraphs=[
                    "HumanEnerDIA stores factory/site records, machines/SEUs, high-frequency energy readings, production data, environmental context, machine status, baseline metadata, anomaly records, tariffs, carbon factors, audit records, ISO 50001 entities, model tracking, forecast output, and action plans.",
                    "The first-start seed data defines two sample factories and eight sample machines across the demo and European facilities. The machine examples include Compressor-1, HVAC-Main, Conveyor-A, Hydraulic-Pump-1, Injection-Molding-1, Boiler-1, Compressor-EU-1, and HVAC-EU-North.",
                ],
                table=(
                    ["Concept", "Implemented representation", "Evidence"],
                    [
                        ["Factories", "factories table and seed data for Demo Manufacturing Plant and European Production Facility", "database/init/02-schema.sql; 06-seed-data.sql"],
                        ["Machines/SEUs", "machines table plus ISO-oriented seus and SEU performance tables", "database/init/02-schema.sql; 07-iso50001-schema.sql"],
                        ["Energy readings", "energy_readings hypertable with energy_type, power, energy, electrical quality fields, metadata", "database/init/02-schema.sql; 03-timescaledb-setup.sql"],
                        ["Production data", "production_data hypertable for production count, quality, throughput, mode, downtime", "database/init/02-schema.sql"],
                        ["Environmental data", "environmental_data hypertable for temperature, humidity, pressure, flow, HVAC, vibration context", "database/init/02-schema.sql"],
                        ["Energy sources", "energy_sources and energy_source_features support multi-energy/source-aware modeling", "database/init/07-iso50001-schema.sql; 10a-energy-source-features.sql"],
                    ],
                ),
            ),
            Section(
                "KPI Formula Evidence",
                paragraphs=[
                    "The following KPI formulas are implemented as database functions and wrapped by analytics/services/kpi_service.py. Some additional API routes compute aggregate factory cost/carbon estimates with constants; those should be described as route-level estimates rather than tariff/factor driven SQL functions."
                ],
                table=(["KPI", "Formula or calculation", "Implementation", "Evidence"], KPI_ROWS),
            ),
            Section(
                "Analytics Endpoints And Modules",
                table=(
                    ["Capability area", "Implemented routes/modules", "Notes"],
                    [
                        ["KPI", "/api/v1/kpi/sec, /factory, /factories, /peak-demand, /load-factor, /energy-cost, /carbon, /all", "Machine and factory KPI endpoints exist; formulas vary by endpoint."],
                        ["Baselines", "/baseline/train, /deviation, /predict, /models, /drivers, /train-seu", "ML baseline model metadata and saved model files are present."],
                        ["Forecasts", "/forecast/train/arima, /train/prophet, /predict, /demand, /optimal-schedule, /models, /peak, /short-term", "Uses forecasting model modules and forecast prediction tables."],
                        ["Anomalies", "/anomaly/create, /detect, /search, /recent, /active, /resolve", "Anomaly detection and search APIs with anomaly table evidence."],
                        ["Performance and ISO 50001", "/performance/analyze, /opportunities, /action-plan, /health; /iso50001/*", "Performance engine and ISO 50001 action-plan/reporting workflows are implemented."],
                        ["Production", "/production/{machine_id}", "Production metrics and related energy/cost/carbon estimates are exposed."],
                        ["Reports", "/reports/generate, /preview, /v2/generate, /v2/download/{id}, /v2/status", "Legacy monthly EnPI PDF and newer V2 report system exist."],
                    ],
                ),
            ),
            Section(
                "Grafana Dashboard Capabilities",
                paragraphs=[
                    "Grafana provisioning and dashboard JSON files are present. The dashboard inventory below is based on the tracked JSON dashboard titles and panel names. Dashboard presence is evidence of configured reporting views, while exact metric correctness should be reviewed against each panel SQL query for audit-grade use."
                ],
                table=(["Dashboard", "Panel themes"], DASHBOARD_ROWS),
            ),
            Section(
                "Node-RED Ingestion Pipeline",
                paragraphs=[
                    "The tracked Node-RED flow subscribes to MQTT topic factory/# and includes function nodes for topic parsing, route selection, payload validation, database preparation, success counting, error catching, and a 30-second statistics dashboard update. Credential files are intentionally not inspected or reproduced in this package.",
                ],
                table=(
                    ["Flow area", "Observed nodes", "Evidence"],
                    [
                        ["Input", "MQTT in node Subscribe: factory/#", "nodered/data/flows.json"],
                        ["Routing", "Parse Topic, Route by Type", "nodered/data/flows.json"],
                        ["Processing", "Process Energy, Process Production, Process Environmental, Process Status", "nodered/data/flows.json"],
                        ["Storage", "PostgreSQL nodes via node-red-contrib-postgresql", "nodered/package.json; nodered/data/flows.json"],
                        ["Monitoring/errors", "Count Success, Catch All Errors, Log Error, Stats Dashboard", "nodered/data/flows.json"],
                    ],
                ),
            ),
            Section(
                "Report Generation Capabilities",
                paragraphs=[
                    "The legacy report path exposes a monthly_enpi report type, generates report data, generates machine and daily trend charts, and returns a ReportLab PDF. The V2 report path creates a report id, writes a PDF under /tmp, and exposes a download endpoint. V2 components include cover page, executive dashboard, energy overview, machine analysis, cost analysis, and carbon analysis templates/components.",
                    "Important caution: the V2 generator is implemented, but some values are derived or placeholder-like in code. Examples include proportional cost/carbon trend assumptions and constant efficiency sparkline values. The final report should therefore be presented as implemented reporting capability, not as independently audited KPI methodology.",
                ],
                table=(
                    ["Report path", "Implemented behavior", "Evidence"],
                    [
                        ["Legacy monthly EnPI", "GET /types, POST /generate, GET /preview for monthly_enpi", "analytics/api/routes/reports.py; analytics/reports/monthly_enpi_report.py"],
                        ["V2 PDF report", "POST /v2/generate, GET /v2/download/{report_id}, GET /v2/status", "analytics/api/routes/reports.py; analytics/reports_v2/services/report_service.py"],
                        ["V2 templates", "Base, header/footer, KPI cards, chart containers, cover, executive dashboard, energy overview, machine ranking/profile, cost, carbon sections", "analytics/reports_v2/templates/"],
                    ],
                ),
            ),
            Section(
                "Implemented, Configured, Partial, And Demo Data Distinctions",
                table=(
                    ["Capability", "Classification", "Reason"],
                    [
                        ["TimescaleDB energy/production/environmental storage", "Supported by implementation", "Tables, hypertables, and aggregate views are created by SQL init scripts."],
                        ["SEC, peak demand, load factor, cost, carbon KPI functions", "Supported by implementation", "SQL functions and service wrappers exist."],
                        ["Grafana dashboards", "Configured", "Dashboard JSON and provisioning are tracked."],
                        ["Node-RED ingestion", "Configured and implemented", "Flow nodes and settings are tracked; runtime execution not verified in this pass."],
                        ["Sample factories and machines", "Demo/sample data", "Seed SQL inserts named sample facilities and machines."],
                        ["V2 report polish/semantic completeness", "Partially implemented", "Routes/templates exist, but some data calculations are placeholders or estimates."],
                        ["query-service reports", "Out of scope", "query-service is a placeholder."],
                    ],
                ),
            ),
            common_limitations_section(),
            section_evidence([
                ["KPI functions", "database/init/04-functions.sql"],
                ["KPI routes and service", "analytics/api/routes/kpi.py; analytics/services/kpi_service.py"],
                ["Report routes/services", EVIDENCE["reports"]],
                ["Database schema", EVIDENCE["database_schema"]],
                ["Node-RED", EVIDENCE["nodered"]],
                ["Grafana", EVIDENCE["grafana"]],
                ["Simulator seed data", EVIDENCE["seed_data"]],
            ]),
        ],
    )


def build_docker_doc(diagrams: dict) -> DocSpec:
    return DocSpec(
        filename="Docker Deployment Report.docx",
        title="Docker Deployment Report",
        purpose="Document Docker Compose deployment, configuration, startup, verification, health checks, and operational troubleshooting.",
        audience="Operators, deployment engineers, technical reviewers, and external partner infrastructure teams.",
        evidence_note="Deployment claims are based on compose files, Dockerfiles, setup and verification scripts, and local compose validation.",
        sections=[
            Section(
                "Deployment Overview",
                figure=("deployment-startup-flow.png", "Figure 1. Deployment preparation, setup, validation, build, start, and verification flow."),
                paragraphs=[
                    "The deployment target described by the repository is a Linux host running Docker Engine and Docker Compose v2. The base stack is defined by docker-compose.yml. Full-stack release bundles can include docker-compose.ovos.yml to add the OVOS runtime and skill.",
                    "The setup helper is the intended guided path. It creates .env from .env.example when needed, generates first-run secrets for placeholders, validates Docker Compose, builds images, and starts the stack. It also adjusts OVOS_BRIDGE_HOST when an OVOS overlay is present.",
                ],
            ),
            Section(
                "Compose Service Topology",
                figure=("docker-service-topology.png", "Figure 2. Docker Compose service topology and optional OVOS attachment."),
                paragraphs=[
                    "The base deployment uses one Docker bridge network for HumanEnerDIA services. Nginx is the browser/API gateway; analytics, auth-service, chatbot/Rasa, simulator, Node-RED, Grafana, PostgreSQL/TimescaleDB, MQTT, and Redis communicate on the internal network. OVOS can be added as a separate service joined to the same network."
                ],
            ),
            Section(
                "Docker Compose Services",
                table=(["Service", "Image or build context", "External port/path", "Responsibility", "Healthcheck"], SERVICE_ROWS),
            ),
            Section(
                "Networks, Volumes, And Ports",
                paragraphs=[
                    "All core services join the Docker bridge network named by ENMS_NETWORK_NAME, defaulting to enms-network. The OVOS overlay also joins that network and depends on analytics service health.",
                    "Persistent named volumes include PostgreSQL data, MQTT data/logs, Redis data, Node-RED data, Grafana data, and OVOS/supervisor logs when the OVOS overlay is used.",
                ],
                table=(
                    ["Resource", "Configured name/default", "Purpose"],
                    [
                        ["Network", "${ENMS_NETWORK_NAME:-enms-network}", "Service-to-service communication"],
                        ["postgres-data", "${VOLUME_PREFIX:-enms}-postgres-data", "PostgreSQL/TimescaleDB persistent data"],
                        ["grafana-data", "${VOLUME_PREFIX:-enms}-grafana-data", "Grafana runtime data"],
                        ["redis-data", "${VOLUME_PREFIX:-enms}-redis-data", "Redis append-only persistence"],
                        ["mqtt-data/logs", "${VOLUME_PREFIX:-enms}-mqtt-data and -mqtt-logs", "Mosquitto runtime data and logs"],
                        ["ovos-logs", "${VOLUME_PREFIX:-enms}-ovos-logs", "OVOS runtime logs when overlay deployed"],
                    ],
                ),
            ),
            Section(
                "Environment Variables And Configuration",
                paragraphs=[
                    ".env.example is the safe public configuration template. The real .env file is intentionally not included and must not be committed or copied into documentation. The setup helper generates first-run values for placeholders and preserves existing non-placeholder values.",
                    "Important configuration groups include database credentials, Redis password, MQTT credentials, Grafana admin credentials, Node-RED credential secret and password hash, JWT secret, API key, server IP/frontend URL, Grafana root URL, simulator controls, OVOS bridge host/port/timeout, and SMTP/admin settings.",
                ],
                bullets=[
                    "Use .env.example in documentation, not .env.",
                    "Rotate generated first-run credentials before production exposure.",
                    "Set DNS, TLS, firewall rules, and public URLs explicitly for production.",
                ],
            ),
            Section(
                "Startup, Shutdown, And Reinstall Procedures",
                paragraphs=[
                    "Supported startup paths are ./setup.sh or manual Docker Compose commands after .env is prepared. Supported stop/start procedures use docker compose down/up or docker compose restart without deleting volumes. Destructive volume deletion is not part of routine operations.",
                ],
                table=(
                    ["Procedure", "Command or source", "Notes"],
                    [
                        ["Guided setup", "./setup.sh [--server-ip HOST] [--no-build] [--no-start]", "Creates/updates .env, validates compose, builds and starts by default."],
                        ["Manual validation", "docker compose config", "Base validation succeeded in this documentation pass."],
                        ["Manual start", "docker compose build; docker compose up -d", "Use after .env has no placeholders."],
                        ["Restart service", "docker compose restart analytics", "Use service-specific logs to confirm recovery."],
                        ["Stop without deleting data", "docker compose down", "Keeps persistent volumes."],
                        ["Clean reinstall", "Only when data removal is intended; do not use down -v casually", "Back up data first."],
                    ],
                ),
            ),
            Section(
                "Verification Scripts And Health Checks",
                paragraphs=[
                    "The repository provides release and API verification scripts. These scripts are evidence of intended operational checks, but their success depends on a running stack and reachable services. In this documentation run, compose validation was executed; live health checks were not implied."
                ],
                table=(
                    ["Check", "Purpose", "Evidence/status"],
                    [
                        ["docker compose config --quiet", "Validate Compose syntax/resolution", "Ran successfully for base HumanEnerDIA stack."],
                        ["docker compose -f /home/ubuntu/ovos-llm/docker-compose.yml config --quiet", "Validate OVOS-only compose", "Ran successfully."],
                        ["scripts/verify-wasabi-release.sh --skip-shop", "Checks Nginx, analytics, OVOS bridge, OVOS smoke query when services are running", "Script inspected; not run because runtime stack health was not established."],
                        ["scripts/validate_api_documentation.sh", "Checks critical analytics/API documentation endpoints against a running service", "Script inspected; not run because it requires live analytics and test data."],
                        ["Service healthchecks", "Container-level checks for most services", "Configured in docker-compose.yml; query-service disabled."],
                    ],
                ),
            ),
            Section(
                "Production Hardening And Troubleshooting",
                paragraphs=[
                    "The repository provides release-oriented defaults, placeholders, health checks, and hardening notes, but it should not be represented as automatically production-hardened. Operator action is required for DNS, TLS, firewall restrictions, credential rotation, backups, and monitoring policy.",
                ],
                table=(
                    ["Symptom", "Likely area", "First checks"],
                    [
                        ["Portal does not load", "Nginx or portal static files", "curl /health; docker compose logs nginx"],
                        ["Analytics API returns 500", "Analytics, PostgreSQL, Redis", "logs for analytics/postgres/redis; /api/v1/health"],
                        ["No new telemetry", "Simulator, MQTT, Node-RED", "logs for simulator/mqtt/nodered; Node-RED flow status"],
                        ["Grafana unavailable", "Grafana or database", "Grafana health endpoint; credentials and volume status"],
                        ["Auth errors", "auth-service, database, SMTP", "/api/auth/health; auth-service logs"],
                        ["OVOS voice path unavailable", "OVOS bridge/messagebus or analytics proxy", "OVOS /health; analytics /api/v1/ovos/voice/health"],
                        ["query-service health missing", "Expected placeholder state", "Do not use query-service as readiness blocker."],
                    ],
                ),
            ),
            common_limitations_section(),
            section_evidence([
                ["Base compose", EVIDENCE["compose"]],
                ["OVOS overlay", EVIDENCE["compose_ovos_overlay"]],
                ["Setup helper", EVIDENCE["setup"]],
                ["Verifier", EVIDENCE["verify_release"]],
                ["Operations", "docs/OPERATIONS_RUNBOOK.md; docs/DELIVERY_READINESS.md"],
                ["OVOS Docker", "/home/ubuntu/ovos-llm/Dockerfile; /home/ubuntu/ovos-llm/docker-compose.yml"],
            ]),
        ],
    )


def build_final_system(diagrams: dict) -> DocSpec:
    return DocSpec(
        filename="Final System Documentation.docx",
        title="Final System Documentation",
        purpose="Provide a stakeholder-ready end-to-end overview, installation/operation guide, workflows, and final delivery notes.",
        audience="Managers, reviewers, operators, users, integrators, and external WASABI partners.",
        evidence_note="This document summarizes the evidence-backed content of the technical documents and points readers to implemented local sources.",
        sections=[
            Section(
                "Project Overview",
                figure=("system-context.png", "Figure 1. Relationship between HumanEnerDIA, OVOS-EnMS, data services, dashboards, and users."),
                paragraphs=[
                    "HumanEnerDIA is an open-source industrial energy management system developed for the WASABI project delivery context. It monitors and analyzes simulated or ingested factory energy data, provides dashboards and APIs, supports ISO 50001-oriented concepts, and integrates with an OVOS assistant layer for natural-language operational queries.",
                    "The final package should be described as a Docker Compose deployable system with a companion OVOS-EnMS assistant. It includes implemented backend services, dashboards, reports, simulator, ingestion flow, authentication, text chatbot, and OVOS voice/natural-language paths. It also includes documented limitations that must remain visible for review.",
                ],
            ),
            Section(
                "Installation And Access",
                paragraphs=[
                    "For a local or evaluation deployment, use the guided setup script from the repository or extracted release bundle. For remote browser access, pass a server host or IP so generated URLs match the expected access path. Generated credentials are stored in .env and must be kept private.",
                ],
                table=(["Access point", "Default URL", "Notes"], ACCESS_ROWS),
            ),
            Section(
                "Main Workflows",
                table=(
                    ["Workflow", "Implementation path", "Result"],
                    [
                        ["Start system", "./setup.sh or docker compose build/up", "Services start with generated or configured environment values."],
                        ["Generate telemetry", "simulator -> MQTT -> Node-RED -> PostgreSQL", "Energy, production, environmental, status, and selected multi-energy data are stored."],
                        ["View dashboards", "Grafana through Nginx or direct port", "Configured SOTA dashboard JSON views are available."],
                        ["Use analytics APIs", "FastAPI analytics service under /api/v1", "KPIs, baselines, forecasts, anomalies, reports, and related data are exposed."],
                        ["Authenticate/admin", "auth-service through portal and /api/auth, /api/admin", "Registration/login/admin/session flows use JWT and database tables."],
                        ["Ask text help questions", "chatbot Express proxy -> Rasa -> custom action QA retrieval", "Knowledge/help answers from qa_data.json categories."],
                        ["Ask operational assistant questions", "OVOS REST bridge -> messagebus -> EnMS skill -> analytics API", "Voice/text operational responses with structured data."],
                        ["Generate reports", "analytics report endpoints", "Legacy monthly EnPI PDF and V2 PDF paths are available."],
                    ],
                ),
            ),
            Section(
                "Operator Guide",
                bullets=[
                    "Use docker compose ps and service health endpoints for daily status checks.",
                    "Check Nginx first for browser routing issues, then the owning upstream service.",
                    "Inspect simulator, MQTT, Node-RED, and PostgreSQL together for data-ingestion issues.",
                    "Use scripts/backup-grafana-dashboards.sh for tracked Grafana dashboard JSON backups.",
                    "Use pg_dump or platform backup tooling for PostgreSQL; no generic tracked database backup script exists.",
                    "Avoid docker compose down -v unless the purpose is deliberate persistent data deletion.",
                ],
            ),
            Section(
                "Analytics, Dashboards, Reports, And Assistants",
                paragraphs=[
                    "Analytics capabilities include baseline training/prediction/deviation, KPI functions, forecasting, anomaly detection/search, machine status and time series, comparison/visualization data, model performance, production metrics, performance analysis, ISO 50001/SEU endpoints, and report generation.",
                    "Dashboards are configured in Grafana JSON and provisioned through the Grafana provisioning directory. The Rasa chatbot is a text help/knowledge assistant, while OVOS-EnMS is the operational natural-language assistant integrated with live backend APIs.",
                ],
                table=(["Dashboard or assistant", "Purpose"], [
                    ["Grafana dashboards", "Operational, executive, cost, carbon, ISO 50001, anomaly, model, production, and predictive views."],
                    ["Analytics UI", "FastAPI-rendered pages for dashboards, baselines, anomalies, KPIs, forecasts, Sankey, heatmap, comparison, and model performance."],
                    ["Rasa chatbot", "Text knowledge/help assistant using QA categories and custom retrieval action."],
                    ["OVOS-EnMS", "Operational assistant for energy, power, machine status, rankings, anomalies, forecasts, baselines, KPIs, reports, help, and health checks."],
                ]),
            ),
            Section(
                "Maintenance And Troubleshooting",
                paragraphs=[
                    "Maintenance should focus on credential rotation, backup verification, dashboard export/commit policy, disk usage, restart counts, recent errors, image/base dependency review, and firewall/public route review. Production hardening requires operator policy beyond the repository defaults.",
                ],
                table=(
                    ["Maintenance area", "Recommended review"],
                    [
                        ["Credentials", "Rotate generated first-run values and any exposed credentials."],
                        ["Backups", "Test PostgreSQL restore; back up Grafana dashboards and Docker volumes."],
                        ["Dashboards", "Commit intended Grafana JSON changes after backup/export."],
                        ["Telemetry", "Confirm simulator/MQTT/Node-RED/PostgreSQL are all healthy when data appears stale."],
                        ["OVOS", "Confirm /health messagebus_connected and smoke query when assistant is required."],
                        ["Docs", "Update final documents when route, schema, compose, or packaging behavior changes."],
                    ],
                ),
            ),
            Section(
                "Final Delivery Notes",
                bullets=[
                    "Product 1 is the OVOS skill artifact; Product 2 is the full-stack HumanEnerDIA artifact according to docs/DELIVERY_READINESS.md.",
                    "SHA256 checksums are expected for release artifacts.",
                    ".env is not shipped and must not be disclosed.",
                    "The optional Qwen GGUF model is not bundled in the main release artifacts according to delivery readiness notes.",
                    "query-service is intentionally excluded from release readiness expectations.",
                    "Runtime health must be verified on the actual target deployment before stakeholder demonstration or handover.",
                ],
            ),
            common_limitations_section(),
            section_evidence([
                ["Overview/docs", "README.md; docs/README.md; docs/TECHNICAL_ARCHITECTURE_GUIDE.md; docs/OPERATIONS_RUNBOOK.md"],
                ["Deployment", f"{EVIDENCE['compose']}; {EVIDENCE['setup']}; {EVIDENCE['verify_release']}"],
                ["Analytics/database", f"{EVIDENCE['analytics_main']}; {EVIDENCE['database_schema']}"],
                ["Dashboards and reports", f"{EVIDENCE['grafana']}; {EVIDENCE['reports']}"],
                ["OVOS-EnMS", f"{EVIDENCE['ovos_readme']}; {EVIDENCE['ovos_bridge']}; {EVIDENCE['ovos_skill']}"],
                ["Delivery readiness", "docs/DELIVERY_READINESS.md; releases/HumanEnerDIA-full-stack-v1.0.0-release-notes.md"],
            ]),
        ],
    )


def build_markdown(spec: DocSpec) -> str:
    lines = [
        f"# {spec.title}",
        "",
        f"Project: {PROJECT_NAME}",
        f"Version: {DOC_VERSION}",
        f"Date: {DOC_DATE}",
        f"Status: {DOC_STATUS}",
        "",
        f"Purpose: {spec.purpose}",
        f"Audience: {spec.audience}",
        "",
        f"Evidence rule: {spec.evidence_note}",
        "",
    ]
    for section in spec.sections:
        render_markdown_section(lines, section, 2)
    return "\n".join(lines).rstrip() + "\n"


def render_markdown_section(lines: List[str], section: Section, level: int) -> None:
    lines.append(f"{'#' * level} {section.title}")
    lines.append("")
    if section.figure:
        image_name, caption = section.figure
        lines.append(f"![{caption}](../assets/{image_name})")
        lines.append("")
    for para in section.paragraphs:
        if isinstance(para, tuple):
            lines.append(f"**{para[0].rstrip()}** {para[1].lstrip()}")
        else:
            lines.append(para)
        lines.append("")
    for bullet in section.bullets:
        lines.append(f"- {bullet}")
    if section.bullets:
        lines.append("")
    if section.table:
        headers, rows = section.table
        lines.append("| " + " | ".join(headers) + " |")
        lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
        for row in rows:
            lines.append("| " + " | ".join(str(cell).replace("\n", " ") for cell in row) + " |")
        lines.append("")
    for sub in section.subsections:
        render_markdown_section(lines, sub, level + 1)


def write_sources(specs: Sequence[DocSpec]) -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    for spec in specs:
        source_name = spec.filename.replace(".docx", ".md")
        (SOURCE_DIR / source_name).write_text(build_markdown(spec), encoding="utf-8")

    evidence_lines = [
        "# Evidence Map",
        "",
        f"Project: {PROJECT_NAME}",
        f"Generated: {DOC_DATE}",
        "",
        "This file maps recurring documentation claims to local evidence. It intentionally avoids .env values and credential-bearing runtime files.",
        "",
        "| Key | Evidence |",
        "| --- | --- |",
    ]
    for key in sorted(EVIDENCE):
        evidence_lines.append(f"| {key} | {EVIDENCE[key]} |")
    evidence_lines.extend([
        "",
        "## Validation Performed",
        "",
        "- `docker compose config --quiet` in `/home/ubuntu/humanergy`: passed.",
        "- `docker compose -f /home/ubuntu/ovos-llm/docker-compose.yml config --quiet`: passed.",
        "- Runtime health checks were not run by this generator; they require a running deployment.",
    ])
    (SOURCE_DIR / "evidence-map.md").write_text("\n".join(evidence_lines) + "\n", encoding="utf-8")


def build_specs(diagrams: dict) -> List[DocSpec]:
    return [
        build_system_architecture(diagrams),
        build_software_design(),
        build_skill_doc(diagrams),
        build_kpi_doc(diagrams),
        build_docker_doc(diagrams),
        build_final_system(diagrams),
    ]


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    diagrams = generate_diagrams()
    specs = build_specs(diagrams)
    write_sources(specs)
    for spec in specs:
        build_document(spec)
    print("Generated DOCX files:")
    for spec in specs:
        print(OUT_DIR / spec.filename)


if __name__ == "__main__":
    main()
