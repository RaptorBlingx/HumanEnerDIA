# PDF Report Implementation Roadmap
**From 3/10 → 9.5/10**  
**Estimated Timeline**: 5-6 weeks  
**Status**: 🚀 IMPLEMENTATION IN PROGRESS

---

## ⚠️ CRITICAL NOTES

**OLD SYSTEM PRESERVATION:**
- `analytics/reports/` → **KEEP INTACT** (checkpoint, do not modify)
- `analytics/reports_v2/` → **NEW IMPLEMENTATION** (parallel development)
- Switchover ONLY when new system validated as true 9.5/10 SOTA
- Old system removal requires explicit approval

**PROGRESS TRACKING:**
- ✅ DONE - Marked tasks are completed and validated
- 🚀 IN PROGRESS - Currently working on
- ⏳ PENDING - Not started yet
- All progress tracked in [TODO.md](./TODO.md)

---

## 📋 PRE-IMPLEMENTATION CHECKLIST

### Requirements Validation
- [x] Current state analyzed (see PDF-REPORT-CURRENT-STATE-ANALYSIS.md)
- [x] Visual comparison created (see PDF-REPORT-VISUAL-COMPARISON.md)
- [ ] Stakeholder approval obtained
- [ ] Sample data available for testing
- [ ] Infrastructure requirements identified

### Technology Stack Decisions
- [x] PDF generation: **Playwright** (HTML → PDF via Chrome)
- [x] Templating: **Jinja2** (Python-native, familiar)
- [x] Styling: **Tailwind CSS** + custom print styles
- [x] Charts: **Plotly** (modern, interactive-capable)
- [ ] Image optimization: TBD (tinypng, pillow, etc.)
- [ ] Font licensing: Check for Helvetica Neue alternatives

---

## 🏗️ TECHNOLOGY STACK DEEP-DIVE

### 1. Playwright Setup

**Why Playwright?**
- ✅ Pixel-perfect PDF rendering (uses Chrome engine)
- ✅ Full CSS support (flexbox, grid, gradients)
- ✅ Print media queries work perfectly
- ✅ Can embed fonts
- ✅ Supports page breaks, margins, headers/footers
- ❌ Requires Node.js dependency (~200 MB)
- ❌ Slightly slower than native ReportLab

**Installation:**
```bash
# Install Playwright Python library
pip install playwright

# Install browsers (Chromium ~300 MB)
playwright install chromium

# Optional: Playwright async support
pip install playwright[async]
```

**Basic Usage:**
```python
from playwright.sync_api import sync_playwright

def generate_pdf(html_content: str, output_path: str):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.set_content(html_content)
        page.pdf(
            path=output_path,
            format='A4',
            print_background=True,
            margin={'top': '15mm', 'bottom': '15mm', 'left': '15mm', 'right': '15mm'}
        )
        browser.close()
```

**Docker Integration:**
```dockerfile
# Add to analytics/Dockerfile
RUN pip install playwright
RUN playwright install --with-deps chromium
```

---

### 2. Jinja2 Template System

**Structure:**
```python
from jinja2 import Environment, FileSystemLoader

# Initialize
env = Environment(loader=FileSystemLoader('reports_v2/templates'))

# Render template
template = env.get_template('monthly_report.html')
html = template.render(
    report_data=data,
    factory_name=factory_name,
    period=period,
    # ... other context
)
```

**Template Inheritance:**
```html
<!-- base.html -->
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{% block title %}{% endblock %}</title>
    <link rel="stylesheet" href="report.css">
    {% block extra_css %}{% endblock %}
</head>
<body>
    {% include 'header.html' %}
    
    {% block content %}{% endblock %}
    
    {% include 'footer.html' %}
</body>
</html>

<!-- monthly_report.html -->
{% extends "base.html" %}

{% block title %}Monthly EnPI Report - {{ period }}{% endblock %}

{% block content %}
    {% include 'sections/cover_page.html' %}
    {% include 'sections/toc.html' %}
    {% include 'sections/executive_dashboard.html' %}
    <!-- ... more sections -->
{% endblock %}
```

---

### 3. Tailwind CSS for Styling

**Why Tailwind?**
- ✅ Utility-first CSS (no need to write custom CSS)
- ✅ Responsive by default
- ✅ Easy to maintain consistency
- ✅ Can purge unused styles (smaller file size)
- ❌ Large initial learning curve
- ❌ HTML can look verbose

**Installation (for development):**
```bash
npm install -D tailwindcss
npx tailwindcss init

# Generate CSS
npx tailwindcss -i ./input.css -o ./output.css --watch
```

**For Production (Python):**
- Use pre-built Tailwind CDN in templates
- OR: Pre-compile CSS and include in static/

**Example HTML with Tailwind:**
```html
<div class="bg-white rounded-lg shadow-lg p-6 mb-4">
    <h2 class="text-2xl font-bold text-navy-900 mb-4">
        Executive Dashboard
    </h2>
    
    <div class="grid grid-cols-4 gap-4">
        <!-- KPI Card -->
        <div class="bg-gradient-to-br from-white to-gray-50 p-4 rounded border-l-4 border-teal-500">
            <p class="text-sm text-gray-600 uppercase">Total Energy</p>
            <p class="text-3xl font-light text-navy-900">45.7 <span class="text-lg">MWh</span></p>
            <p class="text-sm text-green-600">▲ +3.2% vs. baseline</p>
        </div>
        
        <!-- Repeat for other KPIs -->
    </div>
</div>
```

**Custom Print Styles:**
```css
/* report.css */
@media print {
    .page-break {
        page-break-after: always;
    }
    
    .no-break {
        page-break-inside: avoid;
    }
    
    @page {
        size: A4;
        margin: 15mm;
    }
    
    @page :first {
        margin-top: 0;
    }
}

/* Custom colors matching brand */
:root {
    --color-navy: #1a365d;
    --color-teal: #00A8E8;
    --color-gray-dark: #374151;
}

.text-navy-900 { color: var(--color-navy); }
.bg-teal-500 { background-color: var(--color-teal); }
```

---

### 4. Plotly Chart Generation

**Setup:**
```bash
pip install plotly kaleido
```

**Chart Factory Pattern:**
```python
# reports_v2/generators/chart_factory.py
import plotly.graph_objects as go
import plotly.express as px
from io import BytesIO

class ChartFactory:
    def __init__(self, theme='humanergy'):
        self.colors = {
            'primary': '#00A8E8',
            'secondary': '#1a365d',
            'success': '#10b981',
            'warning': '#f59e0b',
            'danger': '#ef4444'
        }
        
        # Set default layout
        self.default_layout = dict(
            font=dict(family='Helvetica Neue, Arial', size=12),
            plot_bgcolor='white',
            paper_bgcolor='white',
            margin=dict(l=50, r=50, t=50, b=50)
        )
    
    def create_gauge_chart(self, value, max_value, title):
        """Create gauge chart for KPI visualization"""
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=value,
            title={'text': title},
            delta={'reference': max_value * 0.75},
            gauge={
                'axis': {'range': [None, max_value]},
                'bar': {'color': self.colors['primary']},
                'steps': [
                    {'range': [0, max_value*0.5], 'color': self.colors['danger']},
                    {'range': [max_value*0.5, max_value*0.75], 'color': self.colors['warning']},
                    {'range': [max_value*0.75, max_value], 'color': self.colors['success']}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': max_value * 0.9
                }
            }
        ))
        
        fig.update_layout(**self.default_layout)
        return fig
    
    def create_waterfall_chart(self, categories, values, title):
        """Create waterfall chart for variance breakdown"""
        fig = go.Figure(go.Waterfall(
            name="Variance",
            orientation="v",
            measure=["relative", "relative", "relative", "total"],
            x=categories,
            y=values,
            connector={"line": {"color": "rgb(63, 63, 63)"}},
            increasing={"marker": {"color": self.colors['danger']}},
            decreasing={"marker": {"color": self.colors['success']}},
            totals={"marker": {"color": self.colors['primary']}}
        ))
        
        fig.update_layout(title=title, **self.default_layout)
        return fig
    
    def export_to_png(self, fig, width=800, height=600, scale=2):
        """Export figure to PNG (300 DPI)"""
        img_bytes = fig.to_image(
            format='png',
            width=width,
            height=height,
            scale=scale  # 2x scale = 300 DPI
        )
        return BytesIO(img_bytes)
    
    def export_to_html_div(self, fig):
        """Export as HTML div for embedding"""
        return fig.to_html(
            include_plotlyjs='cdn',
            div_id='chart',
            config={'displayModeBar': False}
        )
```

**Usage Example:**
```python
chart_factory = ChartFactory()

# Create gauge
gauge = chart_factory.create_gauge_chart(
    value=68.5,
    max_value=100,
    title="Load Factor (%)"
)

# Export to PNG for PDF
img_buffer = chart_factory.export_to_png(gauge, width=400, height=300)

# OR: Export to HTML for interactive PDF
html_div = chart_factory.export_to_html_div(gauge)
```

**New Chart Types to Implement:**
1. ✅ Gauge charts (KPIs)
2. ✅ Waterfall charts (variance)
3. ⏳ Heatmaps (hourly consumption)
4. ⏳ Sankey diagrams (energy flow)
5. ⏳ Sparklines (inline trends)
6. ⏳ Box plots (distribution analysis)
7. ⏳ Scatter plots (correlation)

---

## 🗂️ NEW FILE STRUCTURE

```
analytics/
├── reports/                    # OLD (keep for backward compatibility)
│   ├── base_report.py
│   ├── monthly_enpi_report.py
│   ├── chart_generator.py
│   └── styles.py
│
├── reports_v2/                 # NEW (9.5/10 system)
│   ├── __init__.py
│   │
│   ├── templates/              # Jinja2 HTML templates
│   │   ├── base.html           # Master layout
│   │   ├── header.html         # Report header
│   │   ├── footer.html         # Report footer
│   │   │
│   │   ├── cover/
│   │   │   └── cover_page.html
│   │   │
│   │   ├── sections/
│   │   │   ├── toc.html
│   │   │   ├── executive_dashboard.html
│   │   │   ├── energy_overview.html
│   │   │   ├── machine_ranking.html
│   │   │   ├── machine_profile.html
│   │   │   ├── seu_analysis.html
│   │   │   ├── enpi_dashboard.html
│   │   │   ├── anomalies.html
│   │   │   ├── forecast.html
│   │   │   ├── recommendations.html
│   │   │   ├── compliance.html
│   │   │   └── appendix.html
│   │   │
│   │   └── components/         # Reusable components
│   │       ├── kpi_card.html
│   │       ├── data_table.html
│   │       ├── chart_container.html
│   │       ├── callout_box.html
│   │       ├── progress_bar.html
│   │       └── status_badge.html
│   │
│   ├── static/                 # Static assets
│   │   ├── css/
│   │   │   ├── tailwind.min.css
│   │   │   └── report_print.css
│   │   │
│   │   ├── fonts/              # Embedded fonts (if needed)
│   │   │   ├── HelveticaNeue-Light.ttf
│   │   │   ├── HelveticaNeue-Regular.ttf
│   │   │   └── HelveticaNeue-Bold.ttf
│   │   │
│   │   └── images/
│   │       ├── logo_large.png
│   │       ├── iso50001_badge.png
│   │       ├── cover_bg.jpg
│   │       └── machine_photos/
│   │
│   ├── generators/             # Report generation logic
│   │   ├── __init__.py
│   │   ├── base_generator.py   # Abstract base class
│   │   ├── html_generator.py   # HTML rendering
│   │   ├── pdf_generator.py    # HTML → PDF (Playwright)
│   │   ├── chart_factory.py    # Plotly chart creator
│   │   └── data_processor.py   # Data transformation
│   │
│   ├── components/             # Python component classes
│   │   ├── __init__.py
│   │   ├── kpi_card.py
│   │   ├── data_table.py
│   │   └── chart_container.py
│   │
│   ├── reports/                # Report type implementations
│   │   ├── __init__.py
│   │   ├── monthly_enpi_v2.py
│   │   ├── quarterly_summary.py
│   │   ├── annual_review.py
│   │   └── custom_report.py
│   │
│   └── utils/                  # Utilities
│       ├── __init__.py
│       ├── formatters.py       # Number/date formatting
│       ├── validators.py       # Data validation
│       └── cache.py            # Report caching
│
└── services/
    └── report_service_v2.py    # Updated service with v2 integration
```

---

## 📅 IMPLEMENTATION TIMELINE

### **PHASE 1: Foundation (Week 1)** 🏗️

**Goals:**
- Set up HTML template system
- Integrate Playwright
- Create basic 1-page report

**Tasks:**
- [ ] **Day 1-2**: Infrastructure setup
  - [ ] Install Playwright + dependencies
  - [ ] Create `reports_v2/` directory structure
  - [ ] Set up Jinja2 environment
  - [ ] Test basic HTML → PDF conversion
  
- [ ] **Day 3-4**: Template system
  - [ ] Create `base.html` master template
  - [ ] Build header/footer templates
  - [ ] Implement page break logic
  - [ ] Test template inheritance
  
- [ ] **Day 5**: Component library
  - [ ] KPI card component (HTML + CSS)
  - [ ] Data table component
  - [ ] Chart container component
  - [ ] Test rendering

**Deliverables:**
- ✅ Working Playwright setup
- ✅ Basic template system
- ✅ Sample 1-page PDF generated

**Success Criteria:**
- Generate PDF in <3 seconds
- PDF matches HTML preview (pixel-perfect)
- Templates are reusable

---

### **PHASE 2: Visualization (Week 2)** 📊

**Goals:**
- Migrate to Plotly charts
- Implement 8 new chart types
- Create chart theming system

**Tasks:**
- [ ] **Day 1-2**: Plotly setup
  - [ ] Install Plotly + Kaleido
  - [ ] Create `ChartFactory` class
  - [ ] Define chart theme (colors, fonts)
  - [ ] Test basic chart rendering
  
- [ ] **Day 3-4**: Chart types
  - [ ] Gauge charts (KPIs)
  - [ ] Waterfall charts (variance)
  - [ ] Heatmaps (hourly patterns)
  - [ ] Bar/line combos
  - [ ] Sparklines (inline trends)
  
- [ ] **Day 5**: Integration
  - [ ] Embed charts in templates
  - [ ] Test chart export (PNG + HTML)
  - [ ] Optimize chart sizes (DPI, dimensions)
  - [ ] Add annotations/callouts

**Deliverables:**
- ✅ `ChartFactory` with 5+ chart types
- ✅ Charts embedded in PDF
- ✅ 300 DPI image quality

**Success Criteria:**
- Charts render in <1 second each
- Charts match brand colors
- Print quality (300 DPI)

---

### **PHASE 3: Content (Week 3-4)** 📝

**Goals:**
- Build all report sections (1-6)
- Implement data fetching for new metrics
- Add forecasting models

**Week 3 Tasks:**
- [ ] **Day 1**: Cover page + TOC
  - [ ] Design cover page layout
  - [ ] Generate table of contents
  - [ ] Add key findings callout
  
- [ ] **Day 2-3**: Executive dashboard
  - [ ] 8 KPI cards in grid
  - [ ] Consumption trend chart
  - [ ] Top consumer summary
  - [ ] Anomaly summary
  
- [ ] **Day 4-5**: Energy overview section
  - [ ] Total consumption analysis
  - [ ] Time-series charts (daily, hourly)
  - [ ] Comparative analysis (YoY, MoM)
  - [ ] Waterfall chart (variance)

**Week 4 Tasks:**
- [ ] **Day 1-2**: Machine & SEU analysis
  - [ ] Machine ranking table
  - [ ] Top 3 machine profile pages
  - [ ] SEU portfolio view
  - [ ] Individual machine recommendations
  
- [ ] **Day 3**: EnPI dashboard
  - [ ] Gauge charts for KPIs
  - [ ] Historical trends (6 months)
  - [ ] Benchmark comparisons
  
- [ ] **Day 4**: Anomalies & forecast
  - [ ] Anomaly timeline
  - [ ] Critical anomalies detail
  - [ ] Next month forecast (Prophet/ARIMA)
  - [ ] Scenario analysis
  
- [ ] **Day 5**: Recommendations
  - [ ] Prioritization matrix
  - [ ] Action plan table
  - [ ] Impact quantification
  - [ ] Progress tracking

**Deliverables:**
- ✅ All 6 main sections complete
- ✅ 20+ page comprehensive report
- ✅ Data-driven recommendations

**Success Criteria:**
- Report tells a coherent story
- All data is accurate
- Insights are actionable

---

### **PHASE 4: Polish (Week 5)** ✨

**Goals:**
- Perfect the design
- Add ISO 50001 compliance section
- Optimize performance

**Tasks:**
- [ ] **Day 1**: Design refinement
  - [ ] Typography audit (consistency check)
  - [ ] Color palette refinement
  - [ ] Spacing/alignment fixes
  - [ ] Page break optimization
  
- [ ] **Day 2**: Navigation
  - [ ] PDF bookmarks (outline)
  - [ ] Hyperlinks (internal + external)
  - [ ] QR codes (to Grafana dashboards)
  
- [ ] **Day 3**: ISO 50001 compliance
  - [ ] Compliance checklist section
  - [ ] Audit trail documentation
  - [ ] Methodology appendix
  - [ ] Glossary of terms
  
- [ ] **Day 4**: Performance optimization
  - [ ] Reduce PDF file size (<5 MB)
  - [ ] Optimize image compression
  - [ ] Cache frequently used data
  - [ ] Parallel chart generation
  
- [ ] **Day 5**: Testing & QA
  - [ ] Generate test reports (3 months)
  - [ ] Verify data accuracy
  - [ ] Check print quality
  - [ ] User acceptance testing

**Deliverables:**
- ✅ Print-ready PDF (300 DPI)
- ✅ File size <5 MB
- ✅ Generation time <10 seconds
- ✅ ISO 50001 compliant

**Success Criteria:**
- Passes internal 9.5/10 review
- Stakeholder approval
- Ready for production use

---

### **PHASE 5: Advanced Features (Week 6+)** 🚀

**Goals:**
- Multi-format export
- Email delivery
- Scheduled generation

**Tasks:**
- [ ] **Multi-format export:**
  - [ ] HTML version (interactive)
  - [ ] Excel export (data tables)
  - [ ] PowerPoint export (executive summary)
  
- [ ] **Email delivery:**
  - [ ] SMTP integration
  - [ ] Email templates
  - [ ] Scheduled sending
  
- [ ] **Report scheduler:**
  - [ ] Cron job setup
  - [ ] Auto-generate monthly reports
  - [ ] Store in archive
  
- [ ] **Custom report builder:**
  - [ ] UI for selecting sections
  - [ ] Date range customization
  - [ ] Machine/factory filtering
  
- [ ] **Report versioning:**
  - [ ] Store generated reports in DB
  - [ ] Compare report versions
  - [ ] Audit trail

**Deliverables:**
- ✅ Multi-format export (3+ formats)
- ✅ Automated report delivery
- ✅ Custom report builder

**Success Criteria:**
- Reports auto-generated monthly
- Users can customize sections
- Full audit trail maintained

---

## 🧪 TESTING STRATEGY

### Unit Tests
```python
# tests/test_report_generator.py
import pytest
from reports_v2.generators.pdf_generator import PDFGenerator

def test_generate_pdf():
    generator = PDFGenerator()
    html = "<h1>Test Report</h1>"
    pdf_buffer = generator.generate(html)
    
    assert pdf_buffer is not None
    assert len(pdf_buffer.getvalue()) > 1000  # Non-empty PDF

def test_chart_factory():
    from reports_v2.generators.chart_factory import ChartFactory
    
    factory = ChartFactory()
    gauge = factory.create_gauge_chart(75, 100, "Test Gauge")
    
    assert gauge is not None
    img = factory.export_to_png(gauge)
    assert img is not None
```

### Integration Tests
```python
# tests/test_monthly_report_v2.py
import pytest
from reports_v2.reports.monthly_enpi_v2 import MonthlyEnPIReportV2

@pytest.mark.asyncio
async def test_generate_monthly_report():
    report = MonthlyEnPIReportV2()
    
    pdf_buffer = await report.generate(
        year=2025,
        month=11,
        factory_id=1
    )
    
    assert pdf_buffer is not None
    assert len(pdf_buffer.getvalue()) > 100000  # >100 KB
```

### Manual QA Checklist
- [ ] Cover page looks professional
- [ ] TOC links work
- [ ] All charts render correctly
- [ ] Tables are properly formatted
- [ ] Colors match brand
- [ ] Typography is consistent
- [ ] Page breaks are logical
- [ ] Print quality is 300 DPI
- [ ] File size is <5 MB
- [ ] Generation time is <10 seconds
- [ ] Data is accurate
- [ ] Recommendations make sense

---

## 🔧 CONFIGURATION

### Environment Variables
```bash
# .env
REPORT_TEMPLATE_DIR=/app/reports_v2/templates
REPORT_STATIC_DIR=/app/reports_v2/static
REPORT_OUTPUT_DIR=/app/reports/output
REPORT_CACHE_DIR=/app/reports/cache

# Playwright
PLAYWRIGHT_BROWSER_PATH=/usr/bin/chromium-browser
PLAYWRIGHT_HEADLESS=true

# Chart settings
CHART_DPI=300
CHART_DEFAULT_WIDTH=800
CHART_DEFAULT_HEIGHT=600

# PDF settings
PDF_PAGE_SIZE=A4
PDF_MARGIN_MM=15
PDF_PRINT_BACKGROUND=true
```

### Report Configuration
```yaml
# reports_v2/config.yaml
report:
  monthly_enpi_v2:
    enabled: true
    sections:
      - cover_page
      - toc
      - executive_dashboard
      - energy_overview
      - machine_analysis
      - enpi_dashboard
      - anomalies
      - forecast
      - recommendations
      - compliance
      - appendix
    
    options:
      top_machines: 3
      anomaly_limit: 10
      forecast_months: 1
      include_photos: true
      include_qr_codes: true
    
    styling:
      theme: humanergy
      color_scheme: industrial
      font_family: Helvetica Neue
      font_size_base: 10pt
```

---

## 📊 SUCCESS METRICS

### Quantitative
- [x] Report score: 9.5/10 (internal review)
- [ ] Page count: 20-25 pages (up from 5-8)
- [ ] Chart count: 15-20 (up from 2-3)
- [ ] Data points: 100+ KPIs (up from ~20)
- [ ] Generation time: <10 seconds
- [ ] PDF size: <5 MB
- [ ] DPI: 300 (print quality)

### Qualitative
- [ ] "Executive-ready" appearance
- [ ] Clear visual hierarchy
- [ ] Actionable insights on every page
- [ ] ISO 50001 audit-compliant
- [ ] Brand-consistent design
- [ ] Easy navigation
- [ ] Professional presentation

### User Feedback
- [ ] Positive feedback from stakeholders
- [ ] Usable for investor presentations
- [ ] Accepted for ISO 50001 audits
- [ ] Reduces manual reporting time by 80%

---

## 🚨 RISK MANAGEMENT

### Technical Risks

**Risk 1: Playwright performance**
- **Impact**: Slow PDF generation (>10s)
- **Mitigation**: 
  - Cache static elements
  - Pre-render charts
  - Use Playwright async API
  - Consider headless Chrome optimization

**Risk 2: PDF file size**
- **Impact**: Large files (>10 MB) slow downloads
- **Mitigation**:
  - Compress images (tinypng)
  - Use WebP format where possible
  - Optimize chart resolution (2x scale max)
  - Remove unused CSS

**Risk 3: Chart rendering failures**
- **Impact**: Missing visuals in PDF
- **Mitigation**:
  - Fallback to ReportLab charts
  - Test all chart types thoroughly
  - Add error handling + logging

### Business Risks

**Risk 4: Stakeholder rejection**
- **Impact**: Redesign required, timeline delays
- **Mitigation**:
  - Get approval on mockups FIRST
  - Iterate in phases (show progress)
  - Keep old reports available

**Risk 5: Data accuracy issues**
- **Impact**: Wrong insights, loss of trust
- **Mitigation**:
  - Unit test all calculations
  - Cross-check with Grafana dashboards
  - Add data validation layer

---

## 📚 RESOURCES

### Documentation
- [ ] Playwright Python docs: https://playwright.dev/python/
- [ ] Jinja2 docs: https://jinja.palletsprojects.com/
- [ ] Tailwind CSS docs: https://tailwindcss.com/docs
- [ ] Plotly Python docs: https://plotly.com/python/

### Design Inspiration
- [ ] Tesla Impact Report (PDF)
- [ ] Microsoft ESG Report (PDF)
- [ ] Stripe Annual Report (PDF)
- [ ] McKinsey Insights (design style)

### Tools
- [ ] Figma (for mockup design)
- [ ] draw.io (for flowcharts)
- [ ] PDF readers (Adobe, Preview, Chrome)
- [ ] Color contrast checker (WebAIM)

---

## 🎯 NEXT ACTIONS (Immediate)

### This Session
- [x] Document current state ✅
- [x] Create visual comparison ✅
- [x] Create implementation roadmap ✅
- [ ] Design 3 mockup pages (cover, dashboard, machine profile)
- [ ] Get stakeholder approval

### Next Session
- [ ] Set up Playwright environment
- [ ] Create basic template structure
- [ ] Generate first 1-page PDF
- [ ] Test HTML → PDF quality

---

**END OF ROADMAP**

✅ Planning complete  
🎯 Ready for Phase 1 implementation  
📅 Estimated start: After stakeholder approval
