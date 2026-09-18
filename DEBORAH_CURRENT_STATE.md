# Deborah Research Assistant — Current State Assessment (as of 2026-09-15)

Latest supplied build: **v3.2-rc2** — `v32/dist_rc2/deborah-research-assistant-v3.2-rc2.zip`, 5,874,995 bytes, 460 files, SHA-256 `3825930b…`, `RELEASE_METADATA.build_id = rc2-20260911T220332Z`, `app/__init__.__version__ = 3.2.0-dev`. Statements below are graded with the audit vocabulary; each is tied to code, a machine-readable artefact, or is marked as a project claim.

## What demonstrably works today

| Capability | Status | Evidence |
|---|---|---|
| Installation, packaged test suite on Linux | Implemented and verified — 4,426 passed / 0 failed / 0 errors / 0 skipped, CPython 3.13.12, 388.97 s, run from the extracted rc2 archive | `v32/deliverables_rc2/packaged_suite_rc2_junit.xml` |
| Web UI start, bootstrap token, CSRF, consent-gated egress | Implemented and verified live (anonymous settings refused; CSRF-less start → 403; start without consent refused) | `live_acceptance_rc2.json`; `app/interfaces/webui.py` `_harden` l.5000–5007, Origin check l.4975, loopback refusal in `main()` |
| Loopback-only bind, CSP / nosniff / no-referrer / no-store / X-Frame DENY, SameSite=Strict cookies | Implemented, verified in code and unit tests only | `webui.py` l.5000–5043 |
| Pinned HTTPS transport (public-IP admission, 2,000,000-byte response cap, 3 redirects, `ssl.create_default_context`, proxies never consulted) | Implemented and verified by fixture tests; live requests logged with sizes/status | `app/net.py` l.18, 47, 59, 217, 279; `provider_table_rc2.md` |
| Uploaded-file and ZIP inspection guards (declared-size, ratio, member count, symlink refusal) | Fixture-tested only (M6 regression tests) | `tests/test_v12_regressions.py`, later suites |
| Report generation MD / HTML / PDF / JSON (+ CSV / XLSX exports of runs) | Implemented and verified for the honest-incomplete case: four report files produced live in RC2 | `live_acceptance_rc2.json` |
| Run history, progress screens, estimates, batch intake, provider settings screen | Implemented; unit/jsdom tested; no Windows or browser-automation evidence after v3.0-rc1 | `app/platform/*`, `tests/test_v30_*` |
| Windows helpers (`SETUP.bat`, `START_APP.bat`, `icacls` permissions, encoding-declared subprocesses) | Implemented but unverified — not executed on Windows for any build after v3.0-rc1 | `RC2_REPORT.md` "WINDOWS RE-ACCEPTANCE REQUIRED" |

## What is offline / demo / fixture-only
Every provider except ProPublica, IRS bulk files and Gemini has only fixture evidence (see table below). Entity resolution beyond the ProPublica candidate step, SEC EDGAR, USAspending, Common Crawl, Wikidata, GitHub, PyPI, OpenAlex, Crossref, arXiv, Internet Archive, ATS boards, Playwright rendering and Tesseract OCR: **Fixture-tested only / Untested live**. Meeting-summary: **Not present** in any version.

## Without any key
The keyless path (ProPublica → IRS fallback → bounded crawl) starts, resolves a **provisional** candidate (EIN 941655673, Menlo Park CA) and then **fails to lock identity** because no authoritative filing can be retrieved: all 12 ProPublica `download-xml` requests returned HTTP 403 Cloudflare challenge pages (1,327,400 B each), `eo_ca.csv` and `index_2025.csv` timed out, `index_2026.csv` (47,506,032 B) downloaded but yielded no usable object id. Result: `ValueError: no authoritative, identity-matched filing retrieved`; reports marked RESEARCH INCOMPLETE with 0 financial years (`live_acceptance_rc2.json`, single run, no retry). Keyless output is therefore honest but empty of financial substance.

## With optional keys
- **Gemini (`GOOGLE_API_KEY`/`GEMINI_API_KEY`, `DEBORAH_GEMINI_MODEL`, default `gemini-3.6-flash` at `geminiextract.py:112`):** one live call ever (2026-09-09, v3.1, 6/6 figures on one PDF, claim in `V31_FEATURE_REPORT.md`). Requires consent, sends whole documents off-machine, host-pinned via `genai_transport.py`. Free-tier limits, scanned PDFs, large documents: unmeasured. It cannot help while no filing PDF is retrieved.
- **Brave / Tavily / Perplexity / GitHub token:** Untested live in any version; Brave recorded as paid-only (`providersettings`).
No key is present in any archive; a Gemini key exists only in the session credential vault (never exposed here).

## Platform verification
- **Linux:** the only platform with post-v3.0-rc1 evidence (junit + live JSON).
- **Windows:** last machine-readable run is v3.0-rc1 (2026-09-07, Python 3.12.6): 4,191 tests, 4,178 passed / 5 failed / 7 errors / 1 skipped, `all_pass: false`. Builds v3.0-rc2, v3.1-rc1, v3.2-rc1, v3.2-rc2 have **no Windows execution evidence**. All three Windows runs supplied as JSON/junit (v2.0-rc1, v2.1-rc1, v3.0-rc1) ended `all_pass: false`; the only green Windows run (v2.0-rc2, prose only) was a documented false positive (launcher started the v1.2 UI).

## Does it resolve nonprofits?
**Partially implemented.** Name → candidate EIN works live for one organisation (v3.2-rc2). Candidate → locked identity (EIN + legal name + city/state + verified domain from a filing) has never succeeded live. BMF fallback: Implemented but unverified live (timeouts).

## Does it obtain authoritative Form 990 / 990-EZ / 990-PF data?
**Failed live** in both v3.2 acceptances. Parsing of 990-PF/990/990-EZ XML and the `finmodel` reconciliation are Fixture-tested only. Aggregator JSON amounts are deliberately never treated as financial figures (`nonprofit.py` design, confirmed in code).

## Genuine money-flow / grants / compensation analysis?
**Not achieved live.** Grants tables, officer compensation and multi-year comparison depend on filing XML that has not been retrieved. Modules exist (`finmodel.py`, `nonprofit_report.py` snapshots/reconciliation) and are Fixture-tested only.

## Safe file processing?
Controls are present in code since v1.2 (M6) and covered by regression tests; no independent fuzzing or malicious-sample evidence beyond the project's own fixtures. **Implemented, fixture-verified.**

## Are the UI controls functional?
On Linux, exercised by unit and jsdom tests and one live loop (RC2). Consent-dialog visibility (W8) and Windows file-permission handling (W7) are verified only in jsdom/mocks. The last real-browser screenshot evidence (v3.0-rc1, Windows) showed the consent dialog painted permanently. **Implemented but unverified in a real browser after v3.0-rc1.**

## Provider table (latest version)

| Provider | Introduced | Key | Purpose | Module | Default | Live/fixture status | Env var | Limitation |
|---|---|---|---|---|---|---|---|---|
| ProPublica Nonprofit Explorer | v2.0-rc1 (string) / module v3.0 | keyless | 990 search, org JSON, filing XML | `app/providers/propublica.py`, `app/engine/nonprofit.py` | on | Live RC2: search 200, org 200, XML 403 ×12 | – | Cloudflare blocks XML; aggregator amounts never used as figures |
| IRS TEOS / EO BMF / 990 index | v2.0-rc1 (string) / `irs_teos.py` v2.1 | keyless | EIN, exempt status, filing index | `app/providers/irs_teos.py`, `nonprofit._bmf_discover` | on | Live RC2: two timeouts, one 47.5 MB index with no usable id | – | Bulk bodies time out; no per-object XML route |
| Official websites (bounded crawl) | v1.0 | keyless | Sitemaps, pages | `app/crawler/*`, `app/engine/discovery.py` | on | Fixture; TLS verification off in v1.x, on from v2.0 | – | Verified pages only tier-2/3 evidence |
| Wikipedia | v1.0 | keyless | Context | `app/providers/wikipedia.py` | on | Live in v3.1 Hewlett run (tier 3) | – | "Wikipedia-heavy" results (AUDIT_V3) |
| Internet Archive | v1.0 | keyless | Archived copies | `app/providers/internet_archive.py` | on | Fixture-tested only | – | – |
| GitHub | v1.0 | keyless / optional token | Presence | `app/providers/github.py` | on | Fixture-tested only | `GITHUB_TOKEN` | rate limits unmeasured |
| PyPI | v1.0 | keyless | Presence | `app/providers/pypi.py` | on | Fixture-tested only | – | marginal for nonprofits |
| OpenAlex | v1.0 | keyless | Scholarly works | `app/providers/openalex.py` | on | Fixture-tested only | – | DOI-contamination path (v3.1 PDF) |
| Crossref | v1.0 | keyless | DOI metadata | `app/providers/crossref.py` | on | Fixture-tested only | – | same |
| arXiv | v1.1 | keyless | Preprints | `app/providers/arxiv.py` | on | Fixture-tested only | – | marginal |
| Brave Search | v1.0 | keyed | Web search | `app/providers/brave.py` | off | Untested live | `BRAVE_API_KEY` | paid-only since Feb 2026 |
| Tavily | v1.0 | keyed | Web search | `app/providers/tavily.py` | off | Untested live | `TAVILY_API_KEY` | – |
| Wikidata | v2.0-rc1 | keyless | Identifiers | `app/providers/wikidata.py` | on | Fixture-tested only | – | – |
| SEC EDGAR | v2.0-rc1 / module v2.1 | keyless | Corporate filings | `app/providers/sec_edgar.py` | on | Fixture-tested only | – | UA policy not live-verified |
| Common Crawl | v2.0-rc1 | keyless | Index lookups | `app/providers/commoncrawl.py` | on | Fixture-tested only | – | – |
| USAspending | v2.0-rc1 | keyless | Federal awards | `app/providers/usaspending.py` | on | Fixture-tested only | – | – |
| ATS job boards | v2.1-rc1 | keyless | Job postings | `app/providers/ats_boards.py` | on | Fixture-tested only | – | – |
| Playwright / Tesseract | v2.1-rc1 | local binaries | JS render / OCR | `app/engine/jsrender.py`, `documents.py` | off unless installed | Untested live | – | optional |
| Charity Navigator, OpenCorporates | v3.0-rc1 | n/a | Source-tier labels only | `app/engine/sourcetier.py` | n/a | not fetchers | – | – |
| Google Gemini | v3.1-rc1 | keyed | PDF figure extraction | `app/ai/geminiextract.py`, `genai_transport.py` | off (key + consent) | 1 live call (v3.1) | `GOOGLE_API_KEY`/`GEMINI_API_KEY`, `DEBORAH_GEMINI_MODEL` | free tier unmeasured; documents leave machine |
| Perplexity search | v3.2 (settings label) | keyed | Optional search | providersettings | off | Untested | `PERPLEXITY_API_KEY` | not used live |
| DuckDuckGo / OpenAI / Anthropic | tests only | – | – | – | – | Not present as modules | – | – |

## Which version is the safest baseline
**v3.2-rc2 — for Linux, keyless, with the understanding that nonprofit output is currently honest-incomplete.** Justification: only build with a machine-readable packaged suite at 0 failures, restored TLS negative fixtures, live-exercised auth/CSRF/consent gates, redacted provenance and truthful RESEARCH INCOMPLETE verdicts. For **Windows the safest baseline is undetermined**: the only v3 build with Windows evidence (v3.0-rc1) failed 5/7/1, and every later build is unverified there.

## Which version has the most functionality
v3.2-rc2 (superset of v3.1's Gemini extraction plus the nonprofit pipeline, snapshots and reconciliation; 130 app modules, 132 test files).

## Which versions not to use
- **v1.0–v1.2:** Scrapy TLS verification disabled (P0-B), v1.0 has no UI auth token, v1.1 was shown 18/18 vulnerable by v1.2's probes, v1.2 ships a stale version constant and a runtime database.
- **v2.0-rc2:** launcher starts the unauthenticated v1.2 interface on port 8756 while the kit reports green.
- **v2.2 build 953d7cc4… (not supplied):** displays v2.1.0.
- **v3.2-rc1 (all three builds):** package omits TLS fixtures, suites do not reproduce from the archive, ProPublica query rewrite yields 404.
- **v3.1-rc1 for nonprofit research:** produces confident, DOI-contaminated reports (Hewlett PDF).

## Five highest-priority gaps (observed, not recommendations)
1. Authoritative Form 990 XML retrieval fails live (ProPublica 403 Cloudflare; no direct IRS per-object route) — blocks entity lock and every financial figure (`live_acceptance_rc2.json`).
2. IRS bulk fallback (EO BMF CSV, annual index) times out during body from the test environment; fallback has never succeeded live (`provider_table_rc2.md`).
3. No Windows execution of any build since v3.0-rc1; W1–W9 fixes, `icacls`, consent-dialog CSS verified only on Linux/jsdom (`RC2_REPORT.md`, `RELEASE_METADATA` notes).
4. General research path admits entity-unrelated scholarly/DOI content as findings (v3.1 Hewlett PDF); the v3.2 nonprofit pipeline is a separate branch and does not fix the general path.
5. Release identity inconsistency in the latest archive (`__version__` 3.2.0-dev, README rc1-only, metadata rc2) and the A-RC2-2 residual wall-clock coupling that fails under concurrent suites.

## Counts (consistent with CSV/XLSX)
Versions identified: 13 designations (17 lineage builds; 26 additional interim v3.0-rc1 audit-cycle archives). Archives hashed: 62 (43 unique SHA-256). Duplicate archives: 19. Claims contradicted by evidence: 24. Unresolved findings (open, or fix never verified on the affected platform, or evidence unavailable): 11.
