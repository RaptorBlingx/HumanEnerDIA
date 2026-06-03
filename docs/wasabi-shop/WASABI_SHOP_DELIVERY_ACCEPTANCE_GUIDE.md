# HumanEnerDIA WASABI Shop Delivery Acceptance Guide

This guide is the final operator checklist for confirming the WASABI shop,
PrestaShop listing, HumanEnerDIA full stack, and downloadable products are ready
before asking the team lead to create public URLs.

Use it in order. Do not mark the delivery as done until every required check has
an owner, date, and result.

## 1. Current Local Endpoints

Current local/LAN server:

- Server IP: `10.33.10.104`
- WASABI/PrestaShop front office: `http://10.33.10.104:18080/`
- WASABI/PrestaShop category: `http://10.33.10.104:18080/12-skills`
- PrestaShop back office: `http://10.33.10.104:18080/wasabiSHOP/`
- HumanEnerDIA portal/reverse proxy: `http://10.33.10.104:8080/`
- HumanEnerDIA HTTPS reverse proxy port: `8443`
- Analytics API/UI: `http://10.33.10.104:8001/`
- OVOS REST bridge: `http://10.33.10.104:5000/`
- Grafana: `http://10.33.10.104:3001/`
- Node-RED: `http://10.33.10.104:1881/`

Only the public web entry points should be exposed through DNS/TLS. Do not expose
PostgreSQL, MySQL, Redis, MQTT, or internal service ports directly to the public
internet.

## 2. Product URLs

Current HumanEnerDIA WASABI products:

- Product 38: `HumanEnerDIA OVOS Skill for Industrial Energy Management`
- Product 38 URL: `http://10.33.10.104:18080/skills/38-humanenerdia-ovos-skill-for-industrial-energy-management.html`
- Product 39: `HumanEnerDIA Full Stack for Industrial Energy Management`
- Product 39 URL: `http://10.33.10.104:18080/skills/39-humanenerdia-full-stack-for-industrial-energy-management.html`

Both products must remain:

- Active
- Visible in the `Skills` category
- Free for the initial WASABI release
- Virtual products
- Downloadable products
- Available for order

## 3. Host And Container Checks

Run from `/home/ubuntu/humanergy`.

```bash
docker ps --format 'table {{.Names}}\t{{.Ports}}\t{{.Status}}'
docker compose --env-file .env ps
```

Required healthy/running containers:

- `wasabi-project`
- `wasabi-db`
- `enms-nginx`
- `enms-analytics`
- `ovos-enms`
- `enms-auth-service`
- `enms-grafana`
- `enms-chatbot`
- `enms-rasa`
- `enms-rasa-actions`
- `enms-nodered`
- `enms-mqtt`
- `enms-postgres`
- `enms-redis`
- `enms-simulator`

Required restart policies:

```bash
docker inspect wasabi-project --format '{{json .HostConfig.RestartPolicy}}'
docker inspect wasabi-db --format '{{json .HostConfig.RestartPolicy}}'
docker inspect enms-analytics --format '{{json .HostConfig.RestartPolicy}}'
docker inspect ovos-enms --format '{{json .HostConfig.RestartPolicy}}'
```

Expected:

- `wasabi-project`: `always`
- `wasabi-db`: `always`
- HumanEnerDIA services: `unless-stopped` or documented equivalent

## 4. PrestaShop Admin Checks

Log in to the PrestaShop back office:

```text
http://10.33.10.104:18080/wasabiSHOP/
```

Use the current admin credentials from the secure project password store. Rotate
any default credentials before public exposure.

Check:

- Dashboard loads without a 500 error.
- Catalog > Products opens.
- Product 38 opens and saves without error.
- Product 39 opens and saves without error.
- Product images are visible.
- Product downloads are attached.
- Orders page opens.
- Order detail pages for orders containing Product 38 and Product 39 open.
- Advanced Parameters > Performance has Apache optimization enabled.
- Shop Parameters > Traffic & SEO uses the expected shop domain.
- International > Localization has the intended default language/country.
- Payment settings allow free virtual checkout.
- Email settings use a real SMTP account before public delivery. Do not rely on
  the default PHP mail transport for Gmail or external customer mailboxes.

Database sanity checks:

```bash
docker exec wasabi-db mysql -uroot -proot wasabi -e "
SELECT p.id_product, pl.name, p.active, ps.active AS shop_active,
       p.product_type, p.is_virtual, ps.available_for_order,
       pd.display_filename, pd.active AS download_active, st.quantity, ps.price
FROM wa_product p
JOIN wa_product_shop ps ON p.id_product=ps.id_product AND ps.id_shop=1
JOIN wa_product_lang pl ON p.id_product=pl.id_product AND pl.id_shop=1 AND pl.id_lang=2
LEFT JOIN wa_product_download pd ON p.id_product=pd.id_product
LEFT JOIN wa_stock_available st ON p.id_product=st.id_product AND st.id_product_attribute=0
WHERE p.id_product IN (38,39);

SELECT COUNT(*) AS null_supplier_refs
FROM wa_order_detail
WHERE product_id IN (38,39) AND product_supplier_reference IS NULL;
"
```

Expected:

- Both products show `active=1`, `shop_active=1`, `product_type=virtual`,
  `is_virtual=1`, `available_for_order=1`, and `download_active=1`.
- `null_supplier_refs` is `0`.

## 5. Public Shop Page Checks

Run:

```bash
curl -fsSL http://10.33.10.104:18080/ >/tmp/wasabi-home.html
curl -fsSL http://10.33.10.104:18080/12-skills >/tmp/wasabi-skills.html
curl -fsSL http://10.33.10.104:18080/skills/38-humanenerdia-ovos-skill-for-industrial-energy-management.html >/tmp/wasabi-p38.html
curl -fsSL http://10.33.10.104:18080/skills/39-humanenerdia-full-stack-for-industrial-energy-management.html >/tmp/wasabi-p39.html

rg -i 'HumanEnerDIA|OVOS|Full Stack' /tmp/wasabi-*.html
```

Expected:

- All four `curl` commands exit successfully.
- Category page lists both HumanEnerDIA products.
- Product pages show the correct title, image, description, price, and add-to-cart
  flow.

## 6. Buyer / End-User Checkout Checks

Use a non-admin buyer account.

For each product:

- Open the product page.
- Add the product to cart.
- Complete checkout as a free virtual product.
- Confirm the order reaches an accepted/paid/downloadable state.
- Confirm the order confirmation page shows a `Download package` button for each
  virtual product.
- Open My account > Order history and details > Details for the order.
- Download the file.
- Re-download the same file.
- Confirm the downloaded file name matches the product:
  - `HumanEnerDIA-OVOS-skill-v1.0.0.zip`
  - `HumanEnerDIA-full-stack-v1.0.0.tar.gz`

Expected buyer behavior:

- The buyer does not need a PrestaShop Addons or distribution.prestashop.net
  account to download HumanEnerDIA packages from this WASABI shop.
- The buyer must be logged in to the same shop account that placed the order.
- If the browser opens the login page after clicking a package link, log in as
  the buyer and return to My account > Order history and details.
- The `Dataspace ID` and `Dataspace URL` fields are WASABI federation metadata.
  They are not a replacement for the PrestaShop buyer account login.

Email acceptance check:

```bash
docker exec wasabi-db mysql -uroot -proot wasabi -e "
SELECT id_log, severity, message, date_add
FROM wa_log
WHERE message LIKE '%Swift Error%'
ORDER BY id_log DESC
LIMIT 10;
"
```

Expected:

- No new `Swift Error` rows after the checkout test.
- The buyer receives the `download_product` email in the external mailbox used
  for the test account.
- If SMTP is not configured yet, mark email delivery as `Not ready`; the buyer
  can still download from the confirmation page and account order details.

After checkout, return to the back office and confirm:

- The new order appears.
- The order detail page opens.
- The product download is visible on the order.
- No PHP 500 error appears in the browser.

## 7. Artifact Integrity Checks

Run:

```bash
sha256sum /home/ubuntu/ovos-llm/releases/HumanEnerDIA-OVOS-skill-v1.0.0.zip
cat /home/ubuntu/ovos-llm/releases/HumanEnerDIA-OVOS-skill-v1.0.0.zip.sha256

sha256sum /home/ubuntu/humanergy/releases/HumanEnerDIA-full-stack-v1.0.0.tar.gz
cat /home/ubuntu/humanergy/releases/HumanEnerDIA-full-stack-v1.0.0.tar.gz.sha256
```

The calculated checksum must match the published checksum file.

Confirm uploaded PrestaShop download files match the release files:

```bash
docker exec wasabi-db mysql -uroot -proot wasabi -e "
SELECT id_product, display_filename, filename, active, date_add
FROM wa_product_download
WHERE id_product IN (38,39)
ORDER BY id_product;
"
```

Then compare the hashed file under `/home/ubuntu/wasabi/download/` with the
corresponding release artifact.

## 8. HumanEnerDIA Runtime Checks

Run:

```bash
curl -fsS http://localhost:8080/health
curl -fsS http://localhost:8001/api/v1/health
curl -fsS http://localhost:5000/health
curl -sS -X POST http://localhost:5000/query \
  -H 'Content-Type: application/json' \
  -d '{"text":"what is the power of compressor one","session_id":"delivery-acceptance"}'
```

Expected:

- Nginx health returns `healthy`.
- Analytics health returns JSON with `"status":"healthy"`.
- OVOS health returns JSON with `"status":"healthy"` and
  `"messagebus_connected":true`.
- OVOS query returns `success:true` and a meaningful machine-status response.

## 9. Analytics Scheduled Job Checks

Run direct anomaly detection:

```bash
curl -sS -X POST http://localhost:8001/api/v1/anomaly/detect \
  -H 'Content-Type: application/json' \
  -d '{
    "machine_id":"c0000000-0000-0000-0000-000000000001",
    "start":"2026-06-01T12:00:00Z",
    "end":"2026-06-01T13:00:00Z",
    "use_baseline":true
  }'
```

Run the scheduled job manually:

```bash
curl -sS -X POST http://localhost:8001/api/v1/scheduler/trigger/anomaly_detect
sleep 10
docker logs --since 2m enms-analytics | rg 'Anomaly detection job completed|Failed to detect|ERROR|avg_load_factor|quality_percent|Could not convert|unsupported operand'
```

Expected:

- Direct anomaly detection returns HTTP 200 JSON.
- Scheduler trigger returns `success:true`.
- Logs show `Anomaly detection job completed`.
- Logs do not show `Failed to detect`, `avg_load_factor`, `quality_percent`,
  `Could not convert`, or `unsupported operand` errors.

## 10. Release Packaging Checks

Rebuild the full-stack package whenever code, docs, configuration examples, or
included install scripts change:

```bash
cd /home/ubuntu/humanergy
./scripts/package_wasabi_full_stack.sh 1.0.0
```

Re-publish the full-stack product after rebuilding:

```bash
cd /home/ubuntu/wasabi
./tools/publish_humanerdia_catalog.sh full-stack
```

Re-publish both products only when both artifacts changed:

```bash
cd /home/ubuntu/wasabi
./tools/publish_humanerdia_catalog.sh all
```

Archive exclusion checks:

```bash
tar -tzf /home/ubuntu/humanergy/releases/HumanEnerDIA-full-stack-v1.0.0.tar.gz \
  | rg '(^|/)(\\.env$|\\.git/|node_modules/|__pycache__/|\\.gguf$|logs/)'

unzip -l /home/ubuntu/ovos-llm/releases/HumanEnerDIA-OVOS-skill-v1.0.0.zip \
  | rg '(\\.env$|\\.git/|node_modules/|__pycache__/|\\.gguf$|logs/)'
```

Expected:

- No live `.env`.
- No Git metadata.
- No `node_modules`.
- No Python cache directories.
- No GGUF model files.
- No runtime logs.

## 11. Public URL Handoff To Team Lead

Give the team lead:

- Server IP: `10.33.10.104`
- WASABI shop internal target: `10.33.10.104:18080`
- HumanEnerDIA portal internal target: `10.33.10.104:8080`
- Optional analytics API internal target: `10.33.10.104:8001`
- Optional OVOS bridge internal target: `10.33.10.104:5000`

Recommended public routing:

- Public WASABI shop domain -> reverse proxy -> `10.33.10.104:18080`
- Public HumanEnerDIA portal domain -> reverse proxy -> `10.33.10.104:8080`
- Public API domains only if required, protected by TLS and access policy

Before opening public access:

- Add DNS records.
- Terminate TLS with valid certificates.
- Force HTTP to HTTPS.
- Restrict admin/back-office paths by VPN, IP allow-list, or strong credentials.
- Rotate default/admin credentials.
- Confirm `.env` secrets are unique and not committed.
- Enable database and artifact backups.
- Define who monitors uptime and logs.

## 12. Final Acceptance Sign-Off

Use this table for the final delivery review.

| Area | Required result | Status | Owner | Date |
| --- | --- | --- | --- | --- |
| WASABI front office | Home/category/product pages load |  |  |  |
| PrestaShop back office | Product and order detail pages open |  |  |  |
| Product 38 | Active virtual download, buyer can download |  |  |  |
| Product 39 | Active virtual download, buyer can download |  |  |  |
| Checksums | Shop downloads match release checksums |  |  |  |
| HumanEnerDIA health | Nginx, analytics, OVOS healthy |  |  |  |
| OVOS query | Smoke query returns success |  |  |  |
| Analytics scheduler | Anomaly job completes without errors |  |  |  |
| Security | Credentials rotated, DNS/TLS plan ready |  |  |  |
| Backups | Database/artifact/upload backup plan active |  |  |  |

When every row is complete, it is reasonable to tell the team lead the local
delivery is ready for public DNS/TLS routing.
