# Deborah Research Assistant — Complete Version History and Development Audit

Read-only forensic reconstruction, 2026-09-15. No supplied file was modified, repackaged, renamed or deleted. No application test suite was executed and no live web research was performed for this audit. Archives were opened with Python's `zipfile` in read-only mode (member listing, hashing, text extraction only); no archived code was executed.

Status vocabulary used throughout: **Implemented and verified / Implemented but unverified / Fixture-tested only / Partially implemented / Failed / Removed / Not present / Evidence unavailable.**

Evidence hierarchy applied (highest first): source code and version-to-version diffs → machine-readable test/acceptance results → complete logs → release metadata and checksums → packaged ZIP contents → audit logs and task ledgers → status/architecture documents → handoff messages → conversation claims. Where only a document or conversation supports a statement it is labelled "(claim)".

Companion files: `DEBORAH_VERSION_COMPARISON.xlsx` (10 worksheets), `DEBORAH_FINDINGS_LEDGER.csv` (44 findings), `DEBORAH_TEST_EVIDENCE.csv` (33 runs), `DEBORAH_ARCHIVE_MANIFEST.csv` (62 archives), `DEBORAH_CURRENT_STATE.md`.

---

## 1. Archive inventory and identity

62 ZIP archives were found under the workspace and hashed once each (`audit_history/scripts/manifest.py`; raw output `audit_history/data/archive_manifest_raw.csv`).

| Metric | Value | Evidence |
|---|---|---|
| Archives hashed | 62 | manifest |
| Unique SHA-256 | 43 | manifest |
| Byte-identical duplicates (second and later copies) | 19 | manifest `byte_identical_duplicate_of` |
| Distinct release-lineage builds | 17 | comparison lineage |
| Distinct version/RC designations | 13 (v1.0, v1.1, v1.2, v2.0-rc1..rc4, v2.1-rc1, v2.2-rc1, v3.0-rc1, v3.0-rc2, v3.1-rc1, v3.2-rc1, v3.2-rc2) | `app/__init__.py` + `RELEASE_METADATA.json` |
| Interim v3.0-rc1 audit-cycle builds (26 unique, under `v30/superseded_archives/` and `v30/dist/`) | identity taken from filename tag and embedded metadata only; not separately diffed | manifest |
| Archives with `.pyc`, venv, `.git`, path traversal or symlinks | 0 | manifest |
| Archives whose `RELEASE_METADATA.expected_file_count` disagrees with actual count | 0 | manifest |

Release-lineage builds (baseline = earliest available, each compared with its immediate predecessor):

| Label | File | Bytes | Files | SHA-256 (first 8) | Root folder | Constant | build_id |
|---|---|---|---|---|---|---|---|
| v1.0 | `deborah-research-assistant.zip` | 128,889 | 68 | 5661d6a7 | `deborah-research-assistant/` | 1.0.0 | none |
| v1.1 | `deborah-research-assistant-v1.1.zip` | 325,692 | 74 | 0c4dd33f | **flat (no root folder)** | 1.1.0 | none |
| v1.2 | `deborah-research-assistant-v1.2.zip` | 397,997 | 87 | bc311256 | `deborah-research-assistant-v1.2/` | **1.1.0 (stale)** | none |
| v2.0-rc1 | `deborah-research-assistant-v2.0-rc1.zip` | 1,588,230 | 323 | 5d63e097 | `deborah-research-engine-v2.0/` | 2.0.0 | none |
| v2.0-rc2 | `deborah-research-assistant-v2.0-rc2.zip` | 1,601,401 | 324 | f00f3395 | same | 2.0.0 | none |
| v2.0-rc3 | `deborah-research-assistant-v2.0-rc3.zip` | 1,621,192 | 328 | 0d36c0c6 | same | 2.0.0 | none |
| v2.0-rc4 (a) | `rc4/deborah-research-engine-v2.0/--help/deborah-research-assistant-v2.0-rc4.zip` | 1,677,720 | 347 | e69cf9be | same | 2.0.0 | rc4-20260827T185542Z |
| v2.0-rc4 (b) | `deborah-research-assistant-v2.0-rc4.zip` | 3,309,667 | 348 | 976814d7 | same | 2.0.0 | rc4-20260827T185552Z — **embeds (a) as a member** |
| v2.1-rc1 | `v21/deborah-research-assistant-v2.1-rc1.zip` | 1,735,522 | 364 | 2e55a25f | `deborah-research-engine-v2.1/` | 2.1.0 | rc1-20260901T155054Z |
| v2.2-rc1 | `v22/dist/deborah-research-assistant-v2.2-rc1.zip` (= `Deborah Research Assistant (complete application).zip`) | 1,791,835 | 374 | c10c1722 | `deborah-research-engine-v2.2/` | 2.2.0 | rc1-20260904T153111Z |
| v3.0-rc1 | `v30/dist/deborah-research-assistant-v3.0-rc1.zip` (= `v30/…rc1.zip`) | 5,708,067 | 446 | 1fddc2d9 | `deborah-research-engine-v3.0/` | 3.0.0 | rc1-20260907T015406Z |
| v3.0-rc2 | `v30/rc2_dev/dist/deborah-research-assistant-v3.0-rc2.zip` | 5,758,354 | 446 | 4d8f1dfc | same | 3.0.0 | rc2-20260907T080002Z |
| v3.1-rc1 | `v31/dist/deborah-research-assistant-v3.1-rc1.zip` | 5,799,591 | 449 | 84212ae9 | `deborah-research-engine-v3.1/` | 3.1.0-dev | rc1-20260909T224424Z |
| v3.2-rc1 (a) | `v32/evidence/test package Ω/…v3.2-rc1.zip` | 5,835,362 | 446 | fe4c7953 | `deborah-research-engine-v3.2/` | 3.2.0-dev | rc1-20260911T153938Z |
| v3.2-rc1 (b) | `v32/evidence/final test package Ω/…v3.2-rc1.zip` | 5,843,714 | 447 | 1fcc8b0e | same | 3.2.0-dev | rc1-20260911T155618Z |
| v3.2-rc1 (c, final) | `v32/dist/deborah-research-assistant-v3.2-rc1.zip` | 5,851,323 | 448 | 4fd4eb8f | same | 3.2.0-dev | rc1-20260911T161010Z |
| v3.2-rc2 | `v32/dist_rc2/deborah-research-assistant-v3.2-rc2.zip` | 5,874,995 | 460 | 3825930b | same | **3.2.0-dev (not stamped rc2)** | rc2-20260911T220332Z |

Name-versus-content checks: the v1.2 archive name is not supported by its own constant (`app/__init__.py` = 1.1.0); the v2.2 "superseded" build (sha 953d7cc4…, cited in audit cycle 3 as shipping 2.1.0) is **not among the supplied archives**; the generic `Deborah Research Assistant (complete application).zip` is byte-identical to v2.2-rc1; v3.1 and v3.2 archives carry `-dev` constants although their metadata names them release candidates. `requirements.lock` SHA-256 `e2da018d…` is identical from v3.0-rc1 through v3.2-rc2 (dependency set frozen for four RCs; v3.2's optional `google-genai==2.22.0` lives in a separate `requirements-optional.txt/.lock`).

Packaging exclusions (per `scripts/build_release_zip.py`, v2.0-rc4 onward): venvs, `.git`, `__pycache__`, runtime databases, `.env`, real keys; from v3.2-rc1 a blanket `*.pem` exclusion that also dropped the 11 synthetic TLS fixtures (`tests/fixtures/*.pem`, present in every archive from v2.0-rc1 through v3.1, absent from all three v3.2-rc1 builds, restored in v3.2-rc2 — manifest column `tls_fixture_pems`). Unexpected members: v1.2 ships `data/history.sqlite3` and six generated reports; v2.0-rc4 (b) ships a nested release zip under a folder literally named `--help/`.

---

## 2. Version-by-version reconstruction

Diff counts below are file-level (added / removed / modified) from `audit_history/data/comparison.json`; test counts marked "static" are `def test_` occurrences counted in the archive, not executions.

### 2.0 Scrapy concept (pre-v1.0)
Only referenced in conversation and the v1.0 README. No archive, code or log exists for a pre-v1.0 build. **Evidence unavailable**; not counted as a version.

### 2.1 v1.0 — first runnable application
- **Intent (claim):** a local Flask web app that drives a bounded Scrapy crawl of public sources and stores research history in SQLite.
- **Implemented (code):** 31 modules under `app/`, notably `app/webapp.py` (Flask, bound to 127.0.0.1, `DEBORAH_HOST` override, **no authentication token, no CSRF**), `app/crawler/*` (Scrapy spiders, `settings.py` without any `DOWNLOAD_VERIFY_CERTIFICATES` override — Scrapy's default at the pinned version is `False`, so crawler TLS was **not verified**), provider adapters for Wikipedia, Internet Archive, GitHub, PyPI, OpenAlex, Crossref, Brave and Tavily (regex first-seen; keyed providers off without a key), Markdown/HTML report writing, one Windows launcher `Start_Deborah_Research_Assistant.bat`.
- **Tests:** 13 test files, 67 static test defs. No execution log supplied. **Implemented but unverified.**
- **Security posture:** loopback bind and basic upload/zip size limits only. Everything later marked M1–M6 exists as a latent defect here.
- **Dependencies:** `requirements.lock` without hashes (only version in the lineage without hash pinning).

### 2.2 v1.1 — first hardening pass
- **Diff v1.0→v1.1:** 6 added, 0 removed, 34 modified. Added `app/security.py` (`token_ok`, `request_token`, `host_allowed`, `origin_allowed`, a token-bucket `allow()` limiter) and `app/crawler/resolver.py`.
- **Controls first seen (regex, corroborated in code):** bearer/session token, CSRF, CSP, SameSite/HttpOnly cookies, Host allow-list, redirect handling, symlink refusal. Lock file now hash-pinned.
- **Packaging defect:** archive has **no root folder** (74 members at top level) — the only flat archive in the lineage.
- **Verification:** 14 test files, 106 static defs; no log. v1.2's `fail_on_v11_demo.py` later reports **18/18 probes VULNERABLE** against v1.1 (claim in `AUDIT_LOG.md`; script present in v1.2 archive). **Implemented but unverified; demonstrably vulnerable by v1.2's own probes.**

### 2.3 v1.2 — audit-driven hardening (M1–M6, L1–L8)
- **Diff v1.1→v1.2:** 13 added, 0 removed, 23 modified. Added `app/net.py` (stdlib transport with public-IP admission, IP pinning, `ssl.create_default_context()`, redirect cap), `app/psl.py` + Public Suffix List data, `tests/test_v12_regressions.py`, `fail_on_v11_demo.py`.
- **Findings addressed (AUDIT_LOG v1.2 section):** M1 DNS-rebinding SSRF (resolve-then-connect gap) → pinned socket; M2 no deadline → budget; M3 unbounded results → caps; M4 Markdown link injection → escaping; M5 trusted-domain suffix spoofing → PSL match; M6 ZIP central-directory amplification → declared-size checks; L1–L8 (non-bool consent, non-atomic quota, job-limit race, retention ordering, report filename collision, coverage metrics, bootstrap token in URLs/logs, PEP 517 gap). Three production defects were found by the new tests themselves (`net.py` EBADF, slow-drip `read1`, retention ordering).
- **Identity defect:** `app/__init__.py.__version__` remains `1.1.0`.
- **Unexpected members:** `data/history.sqlite3` and six generated reports inside the release archive.
- **Claims later disproved:** "211 tests pass on 3.11–3.14" — v2.0 Phase 0 (`FINDINGS_RECONCILIATION.md` P0.D3) records a `SyntaxError` on Python 3.11, so the suite never ran on 3.11; Windows failure diagnosed as a UTF-8 file-handling problem — real cause was printing Unicode to a cp1252 console (P0-C/P0.D4); "clean Windows install" — `colorama` missing from the wheel set (P0.D2). Scrapy TLS verification still disabled (P0-B; confirmed: no override in `app/crawler/settings.py`).
- **Verification:** 15 test files, 158 static defs; "211 passed, Python 3.14.3" is a claim without a supplied log. **Partially implemented / Linux claim only.**

### 2.4 v2.0 Phase 0 (no archive)
`FINDINGS_RECONCILIATION.md` and `TASKS.md` describe P0-A (backports-zstd), P0-B (Scrapy `DOWNLOAD_VERIFY_CERTIFICATES: True` — confirmed in every v2.0+ `settings.py`), P0-C/P0.D4 (`app/console.py` UTF-8 stdio), P0.D1 (pip marker blind spot), P0.D2 (colorama), P0.D3 (3.11 syntax), P0.D5 (`Money.from_major_string`), and a "454 tests × 4 interpreters" run. No archive or log was supplied. The same document states that the external v1.2 audit's `findings.json` and `report.md` "were never received"; N1–N10 were reconstructed from the log, with N9 (ambient proxy honoured) **open** at that point and M4/M5 reopened and re-closed. **Evidence unavailable beyond documents.**

### 2.5 v2.0-rc1 — re-architecture
- **Diff v1.2→v2.0-rc1:** 249 added, 13 removed, 36 modified; 94 app modules, 61 test files, 1,771 static defs. New packages: `app/engine/*` (research loop, evidence store, entity resolution, discovery, report), `app/interfaces/{cli,restapi,webui,mcp,egress,service,ai}`, providers Wikidata, IRS, ProPublica, SEC EDGAR, Common Crawl, USAspending (regex first-seen; IRS/ProPublica appear as strings, dedicated modules come later), `windows_acceptance_kit/` (8 gates), 11 TLS negative-fixture pems (closes N10). Egress off unless `DEBORAH_INTERFACE_EGRESS=1` (`app/interfaces/egress.py`).
- **Legacy retained:** `app/webapp.py` (v1.x UI, port 8756) still present; the Windows launcher still starts it (see rc2).
- **Windows evidence (machine-readable):** `uploaded_attachments/8830b1d4…/windows_acceptance_result.json`, kit label "deborah-v2.0 windows acceptance", 2026-08-26 19:19 -0400, Python 3.14.3, Windows 11 build 26200: pytest "1 failed, 2415 passed, 2 errors in 128.82s"; gate G5 FAIL, G1–G4/G6 (0.9630)/G7/G8 pass, `all_pass: false`. The G5 detail field is 2,000 characters dominated by a flood of the letter "a", so the failing test's identity is **unrecoverable** from the artefact (this became W5).
- **Linux:** 2,417 passed (claim). **Failed on Windows.**

### 2.6 v2.0-rc2 — Windows remediation W1–W5
- **Diff:** 1 added, 0 removed, 26 modified. Fixes (AUDIT_LOG W1–W5): 51 encoding-less text operations in tests/scripts/kit; a 100,000-character node ID passed through the environment against Windows' 32,767 limit; non-ASCII, LF-only batch files; kit capture encoding; the diagnostics flood.
- **Windows result (claim, no JSON supplied):** 2,427/0/0/0, all nine gates green, `all_pass: true` — recorded by the project itself as a **false positive at release level**: gate G8 was static-only and `Start_Deborah_Research_Assistant.bat` launched `app.webapp` on port 8756, i.e. the v1.2 interface (confirmed by reading the `.bat` inside the rc1 and rc2 archives: both reference only `app.webapp` and `8756`). Findings W6–W9.
- **Status:** **Failed at release level** despite a green kit.

### 2.7 v2.0-rc3 — launcher and orchestration
- **Diff:** 4 added (incl. `app/engine/orchestrate.py`), 19 modified. Launcher now runs `app.interfaces.webui` on 8758 (confirmed in the rc3 `.bat`: `".venv\Scripts\python.exe" -m app.interfaces.webui`, legacy path described as compatibility only). G8 became a runtime gate; kit expanded to 9–10 gates.
- **Windows result (owner paste, `turn_0048`, no JSON):** G5 FAIL — 2,443 passed / 1 failed / 9 errors; G10 initially FAIL. Root causes V1–V4 were all test/kit/wrapper defects: Unix-only browser fixture; kit trusted the zip by filename; G10 blamed the product for a pre-existing listener; wrapper ran Python 3.14 instead of the intended interpreter. The owner separately validated the product path manually on that machine (claim). Linux counts during rc3: 2,490 → 2,499 → 2,502 (mutation logs). Red proofs on disk: rc3 gate run against the rc2 zip "14 failed, 1 passed".
- **Status:** **Failed (all_pass false)**; product defect not demonstrated.

### 2.8 v2.0-rc4 — kit fixes, release metadata
- **Diff rc3→rc4(a):** 20 added, 1 removed, 17 modified; adds `RELEASE_METADATA.json` (identity from archive contents, "finding V2") and `scripts/build_release_zip.py`. rc4(a)→rc4(b): 1 added (the nested zip), 1 modified (metadata). Red proof: rc4 packaged tests on the rc3 zip "2 passed, 18 errors"; rc4 kit on rc3 "26 failed".
- **Windows:** **never run** (later contradicted by v2.1 `PROJECT_STATUS.md`, which calls RC4 a "Windows-accepted baseline" and, elsewhere in the same document, says RC4 "has NOT been run on Windows").
- **Audit A-RC4-1..6 (AUDIT_LOG):** CLI `start` killed the run it started; no HTML report despite README; résumé-skills parse error; foundation playbook unreachable; comparison silently dropped rows; stale ledger. All fixed in v2.1 (claim, tests named in ledger).
- **Status:** **Implemented but unverified on Windows; packaging defect (nested archive).**

### 2.9 v2.1-rc1 — documents, discovery, providers
- **Diff rc4(b)→v2.1:** 17 added, 1 removed (the nested zip), 30 modified; 103 modules, 72 test files. New: `app/engine/{discovery,documents,jsrender}.py`, providers `ats_boards.py`, `irs_teos.py`, `sec_edgar.py`, pypdf-based PDF text, optional Playwright/Tesseract. Audit items A-V21-1 (nested archive, fixed by `test_v21_packaging`), D/E/H/J-V21 (J-V21-1: prompt-injection flags computed but not rendered).
- **Windows (machine-readable):** `uploaded_attachments/0c084c0f…/acceptance_junit.xml`, 2026-09-02, Python 3.12.6: 2,571 tests, **1 failure** `tests/test_audit_regressions.py::test_post_redirect_refused` (ConnectionError); G5 FAIL; G1–G4, G6, G7, G9, G10 pass; `all_pass: false`. Linux 2,571 passed (claim).
- **Status:** **Failed (Windows all_pass false)**.

### 2.10 v2.2-rc1 — scenarios, stale-version incident
- **Diff v2.1→v2.2:** 10 added, 46 modified; 105 modules, 80 test files. Linux 2,668 (dev) / 2,686–2,687 with the archive under a hostile-Unicode path (claims).
- **Incident (audit cycle 3, 2026-09-04):** the owner ran the shipped v2.2 archive on Windows via `Start_Deborah_Python314.bat` and the UI displayed **v2.1.0**. Root cause: `app/__init__.py` never bumped and `test_version_is_v2` pinned the stale literal, so the suite concealed the defect. Fixed and rebuilt as c10c1722…; the defective archive (953d7cc4…) is not among the supplied files. The rebuilt archive was **not re-run on Windows**.
- **AUDIT_V3.md (2026-09-04, ~41,600 LoC, 82 test files):** ten usability/architecture problems (job-id UX, no persistence, no live progress, no ETA, plain-text report, no organisation memory, no batch, no settings UI, v2.1 "stucking", Wikipedia-heavy results) — the brief for v3.0.
- **Status:** **Implemented but unverified** (stale-identity defect shipped; corrected build unverified on Windows).

### 2.11 v3.0-rc1 — platform layer, 18 audit cycles
- **Diff v2.2→v3.0-rc1:** 72 added, 52 modified; 125 modules, 119 test files, 3,191 static defs. New `app/platform/{runs,progress,estimates,profiles,intake,exports,pdfreport}`, `app/engine/{docdiscovery,docingest,finmodel,pdfdoc,sourcetier}.py`, `app/providers/propublica.py`, reportlab/openpyxl exports (PDF/XLSX/CSV/JSON), `SETUP.bat`/`START_APP.bat`, provider settings screen, batch intake, "Research Since Last Run".
- **Audit cycles (`v30/AUDIT_CYCLE_1..18.md`, `*_FIX_REPORT.md`):** cycle 1 NOT CLEAN — 1 BLOCKER (B-1: a "quick" consent approval could start a "deep" run, `webui.py:801-816`), 5 MAJOR, 6 MINOR, 5 NOTE; suite 3,637 passed (`v30/audit1_pytest.log`, on disk). Cycles 2–15 NOT CLEAN with declining severity (cycle 6 MINOR PDF table overflow; cycle 7 MAJOR export-path defect; cycle 10 MAJOR descriptor leak C10-1; cycles 13–15 MINOR only). Cycle 16 CLEAN (4,146/0/0 ×4). Cycle 17 NOT CLEAN — M17-1 (non-ASCII batch filenames refused with a false diagnosis), M17-2 (retention-deleted runs still listed "Finished"); fixed. Cycle 18 CLEAN — 4,191 passed / 0 failed / 0 skipped, four runs, 3.13 and 3.14 (claim; consistent with the Windows junit total of 4,191). 26 interim archives from these cycles survive under `v30/superseded_archives/`.
- **Windows (machine-readable):** `uploaded_attachments/eed77b4f…/acceptance_junit.xml`, 2026-09-07, Python 3.12.6: 4,191 tests, **4,178 passed, 5 failed, 7 errors, 1 skipped**. Failures: `test_v21_packaging` (stray archives on the machine), `test_v30_c11_history_store_scope`, cycle-9 export burst `[xlsx]` and `[json]` (PermissionError — product defect), `test_v30_sbom`; 7 errors in `test_v30_screen_timestamps`. Screenshot: consent dialog painted permanently. `all_pass: false`. W1–W9 raised (`WINDOWS_FINDINGS_RECONCILIATION.md`).
- **Status:** Linux suite **Implemented and verified (claim consistent with junit total)**; **Failed on Windows**.

### 2.12 v3.0-rc2 — W1–W9 remediation
- **Diff:** 15 added (`tests/test_v30_rc2_w1..w9*.py`, `RC2_FIX_REPORT.md`, `WINDOWS_REACCEPTANCE.md`), 15 removed (`notes/*.log`), 26 modified. Red proofs on disk (`v30/rc2_dev/proofs_rc1_w*.log`) show each new test failing on the rc1 tree (W1 15F/3P, W2 1/6, W3-4 10/2, W5 3/7, W6 2/27, W7 8/6, W8 9/12, W9 1/5).
- **Fixes:** W3/W4 concurrent export PermissionError; W5 machine-dependent SBOM test; W6 timestamp errors; W7 `chmod` no-op on Windows → `icacls`; W8 consent dialog always visible because `body.spa .modal-backdrop{display:flex}` outranked the UA `[hidden]` rule → `_HIDDEN_RULE` (`webui.py:1079`) with an import-time assertion, verified in jsdom only.
- **RC2 audits (`v30/rc2_dev/RC2_AUDIT_CYCLE_1/2.md`):** A-RC2-1 fix report missing from the zip (rebuilt); A-RC2-2 300-second run budget coupled to wall clock ("one failure under two concurrent full suites"); the budget increase shipped un-audited.
- **Linux:** 4,308/0/0/0 on 3.13.12 and 3.14.3 (claim; logs were written to `/tmp` and not supplied). **Windows: never run.**
- **Status:** **Implemented but unverified on the platform the findings came from.**

### 2.13 v3.1-rc1 — Gemini multimodal extraction
- **Diff:** 3 added (`app/ai/geminiextract.py`, tests, docs), 21 modified. Four gates (key present, consent, kill switch, document eligibility), schema-constrained JSON, `verify_in_document` guard, rate/budget limits, `DEBORAH_GEMINI_MODEL`. `RELEASE_METADATA` notes "no vendor SDK" (raw HTTPS to `generativelanguage.googleapis.com`).
- **Verification (`v31/V31_FEATURE_REPORT.md`):** baseline 4,308 → 4,371/0/0/0 on 3.13.12 (from the extracted archive) and 3.14.3 (build tree); +63 tests, two mutation checks. When both suites ran **concurrently**, both failed `test_v22_scenarios.py::test_keyless_foundation_run_reaches_propublica_and_labels_figures` (A-RC2-2 residual) — recorded, not fixed. Live smoke 2026-09-09 (owner key from the credential vault, never in the repo): shipped default `gemini-2.0-flash` returned 404 as retired; switched to `gemini-3.6-flash` (`geminiextract.py:116 DEFAULT_MODEL`), one call, 6/6 figures extracted and guard-tested. Free-tier behaviour, scanned PDFs, large documents: unmeasured.
- **Real-use output (independent evidence):** the uploaded `William-Flora-Hewlett-Foundation-research-report-2026-09-11.pdf` (6 pages, "Generated by Deborah Research Engine 3.1.0-dev", run finished 2026-09-11 14:59 UTC, 7 pages read from 6 domains, 28 statements). Its "What this research found" section lists journal DOIs (`10.1002/cac2.12426`, `10.1007/s00125-024-06200-w`) supported by law-review and Springer links; text contains **0 occurrences of the EIN, 0 of hewlett.org, 1 "unverified"**, and "990" only in boilerplate. The report is well-formed and wrong.
- **Windows:** never run. **Status: Implemented but unverified live at scale; real-use Failed.**

### 2.14 v3.2-rc1 — keyless nonprofit pipeline (three builds)
- **Diff v3.1→rc1(a):** 8 added, **11 removed (all TLS fixture pems)**, 13 modified; (a)→(b) 1 added, 18 modified; (b)→(c) 1 added, 1 modified. New `app/engine/nonprofit.py`, `app/engine/nonprofit_report.py`, `app/ai/genai_transport.py` (optional `google-genai==2.22.0`, host pinned to `generativelanguage.googleapis.com`, `requirements-optional.txt`), `tests/test_v32_*.py`. `GOOGLE_API_KEY` accepted from build (b).
- **Suites on disk (`v32/evidence/`):** `full_suite.log/.xml` (build a) **32 failed / 4,379 passed**; `final_suite.log/.xml` **2 failed / 4,411 passed** — `test_v20_windows_gate::test_w1_every_text_operation_states_its_encoding` (new `tests/test_v32_sdk.py:67` subprocess without encoding — the W1 class recurring) and `test_v30_providersettings::test_brave_is_recorded_as_paid_because_its_free_plan_ended`. Both suites ran the **source tree, not the zip**; the final zip omits the 11 pems, so the archive cannot reproduce the reported results (`UPGRADE_REPORT.md` "Final package blocker"; the in-archive `V32_UPGRADE_REPORT.md` predates this and is superseded by the external report).
- **Live keyless acceptance (`v32/evidence/live_acceptance.json`, one run):** ProPublica name search **HTTP 404** because the query was rewritten `William & Flora Hewlett Foundation` → `William and Flora Hewlett Foundation`; no identity, no filings; four reports saved, all marked RESEARCH INCOMPLETE. The IRS BMF fallback added afterwards was tested offline only.
- **Status:** **Failed (acceptance failed, 2 test failures, non-reproducing package).**

### 2.15 v3.2-rc2 — bounded repair (latest)
- **Diff rc1(c)→rc2:** 12 added (pems restored, `tests/test_v32_rc2_repair.py`, RC2 docs), 8 modified; 460 files.
- **Code-confirmed changes (`app/engine/nonprofit.py`):** `search_candidates()` sends the name as typed (`%26`), tries at most three phrasings via `search_terms()`, treats a 404 as zero results only when the JSON body says `total_results: 0` (lines 579–650); `run()` calls `_bmf_discover(query)` whenever the API yields no candidate (line 954), not only on exceptions; provenance excerpts redact digit runs of four or more (line 87); `normalized_profile()`, `profile_snapshots()`, `audit_reconciliation()` added and rendered in Markdown/HTML/PDF/JSON.
- **Packaged suite (machine-readable):** `v32/deliverables_rc2/packaged_suite_rc2_junit.xml` — **4,426 passed, 0 failed, 0 errors, 0 skipped**, 388.97 s, extracted rc2 tree, Linux x86_64, CPython 3.13.12.
- **Live keyless acceptance (`live_acceptance_rc2.json`, `provider_table_rc2.md`, one run, no retry):** `search.json?q=William+%26+Flora+Hewlett+Foundation` → 200 (976 B, one candidate EIN 941655673, Menlo Park CA); `organizations/941655673.json` → 200 (29,398 B); filing catalog HTML → 200; **all 12 `download-xml` requests → 403** (Cloudflare "Security Check", 1,327,400 B HTML each, refused as non-filing evidence); `irs.gov/pub/irs-soi/eo_ca.csv` → timeout during body; `index_2025.csv` → timeout; `index_2026.csv` → 200 (47,506,032 B, no usable object id). Entity lock (EIN + legal name + city/state + verified domain from a filing) not met → `ValueError: no authoritative, identity-matched filing retrieved`. Verdict **RESEARCH INCOMPLETE**; EIN shown only as a provisional candidate; 0 financial years, 0 reconciliations. Security path exercised live: anonymous settings refused, CSRF-less start 403, start without consent refused, all four downloads served.
- **Identity:** `RELEASE_METADATA` says rc2; `app/__init__.py` still `3.2.0-dev`; README mentions rc1 only.
- **Windows:** not run ("WINDOWS RE-ACCEPTANCE REQUIRED").
- **Status:** Linux packaged suite **Implemented and verified**; live nonprofit research **Failed**; Windows **Not verified**.

---

## 3. Provider matrix
See worksheet "Providers" and the same table in `DEBORAH_CURRENT_STATE.md`. Live evidence exists for exactly three providers across the whole history: ProPublica (404 in v3.2-rc1; 200/200/403×12 in rc2), IRS bulk files (timeouts; one 47.5 MB index downloaded in rc2) and Gemini (one call, v3.1). Every other provider is fixture-tested or untested. Charity Navigator and OpenCorporates exist only as tier labels in `app/engine/sourcetier.py`, not as fetchers. DuckDuckGo, OpenAI and Anthropic appear in tests/labels only. No meeting-summary module exists in any version.

## 4. Security and privacy findings
44 findings are itemised in `DEBORAH_FINDINGS_LEDGER.csv` with first-affected version, discovery point, severity, root cause, fix version, regression test, whether the test failed on the defective build, survival, recurrence and latest status. Highlights:
- **Recurrences:** Windows text-encoding omissions (Phase 0 → W1 in RC1 → again in v3.2-rc1 `test_v32_sdk.py`); M4/M5 reopened at v2.0; TLS negative fixtures dropped from v3.2-rc1 packaging.
- **Controls verified live (RC2 run):** bootstrap auth, CSRF, consent/egress gate. **Controls verified in code only:** loopback refusal, CSP/frame/nosniff/no-store headers, SameSite=Strict, proxy-ignoring pinned transport, Scrapy TLS verification (v2.0+). **Controls verified in jsdom/mocks only:** consent dialog hiding (W8), Windows `icacls` permissions (W7).
- **Secrets:** a Gemini key exists in the session credential vault (category: external vault; never inside any archive). No key material outside `tests/fixtures/` was found in any archive (manifest column `key_pem_outside_tests` empty for all 62).

## 5. Test evidence
`DEBORAH_TEST_EVIDENCE.csv` keeps every run separate by platform and interpreter. Machine-readable results exist for five runs only: Windows v2.0-rc1 (2415/1/2), Windows v2.1-rc1 (2571 tests, 1 failure), Windows v3.0-rc1 (4178/5/7/1), Linux v3.2-rc1 (`full_suite` 32 failed; `final_suite` 2 failed) and Linux v3.2-rc2 (4426/0/0/0), plus two one-shot live acceptance JSONs (both FAILED). Every Windows machine-readable run has `all_pass: false`. No build after v3.0-rc1 has any Windows evidence. Static `def test_` counts grow 67 → 3,373 across the lineage; executed counts grow 211 (claim) → 4,426 (junit).

## 6. Real-world output quality
Large green suites did not translate into correct research output: the only real-user report supplied (v3.1, Hewlett) is DOI-contaminated with no EIN or filings; both v3.2 live acceptances ended RESEARCH INCOMPLETE. What improved in v3.2 is disclosure: the reports state the failure, label the provisional EIN, and carry the full request log with redacted excerpts.

## 7. Claims contradicted by evidence
24 project claims are contradicted by later or independent evidence (worksheet "Claims vs evidence"). Four further claims (v3.0-rc2 4,308 count; v3.0-rc1 Linux 4,191; v3.2-rc2 packaged count; rc2 ampersand fix) are supported or have logs unavailable rather than contradicted.

## 8. Unresolved findings (11)
M3 scenario test (evidence unavailable); V1–V4 kit fixes never exercised on Windows; W3/W4, W7 fixes unverified on Windows; W8 real-browser unverified; A-RC2-2 residual timing coupling; V31-OUTPUT general-path contamination; V32-R2-XML403; V32-R2-IRSTO; V32-R2-IDENT; WIN-OUTSTANDING.

## 9. Missing versions and uncertain transitions
- No archive for the Scrapy concept or v2.0 Phase 0.
- v2.2 defective build 953d7cc4… (shipped 2.1.0) not supplied.
- v2.0 RC2 and RC3 Windows results exist only as prose/paste, not JSON.
- v3.0-rc2, v3.1 Linux suite logs not supplied (written to `/tmp`).
- Whether the RC3 `.bat` change alone fixed the RC2 false positive is asserted by the project, not demonstrated by a Windows JSON.
