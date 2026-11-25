<!-- Generated from data/README.template.md by scripts/build_aurora.py. Edit the template, not this file. -->
<div align="center">

<sub>[ LINKEDIN ](https://www.linkedin.com/in/aditya-singh-8286b137a/) &nbsp;·&nbsp; [ EMAIL ](mailto:adityasinghv05@gmail.com) &nbsp;·&nbsp; [ HOSTELDESK LIVE ](https://hostel-desk-three.vercel.app) &nbsp;·&nbsp; [ REPOSITORIES ](https://github.com/Aditya2514?tab=repositories)</sub>

<img src="assets/aurora/hero.svg" width="100%" alt="Aditya Singh: AI systems, agents and full-stack. IIT Madras and Scaler School of Technology. Northern lights over snowy mountains, and three chips: the model proposes, the system checks, the person decides." />

<br>

<img src="assets/aurora/sky.svg" width="100%" alt="The last 12 months of GitHub contributions drawn as northern lights over mountains: one curtain of light per week, its height that week's contributions, with totals for contributions, commits, active days, longest streak and public repositories." />

<sub>Live from the GitHub API. Every curtain of light is one real week of contributions, redrawn every six hours.</sub>

</div>

<br>

<div align="center">

[`01` BASE CAMP](#01-base-camp) &nbsp;·&nbsp; [`02` ASCENT](#02-ascent) &nbsp;·&nbsp; [`03` EXPEDITIONS](#03-expeditions) &nbsp;·&nbsp; [`04` FIELD NOTES](#04-field-notes) &nbsp;·&nbsp; [`05` RHYTHM](#05-rhythm) &nbsp;·&nbsp; [`06` INSTRUMENTS](#06-instruments)<br>
[`07` TERRAIN](#07-terrain) &nbsp;·&nbsp; [`08` BEDROCK](#08-bedrock) &nbsp;·&nbsp; [`09` TRAIL LOG](#09-trail-log) &nbsp;·&nbsp; [`10` RECORD](#10-record) &nbsp;·&nbsp; [`11` SEND A SIGNAL](#11-send-a-signal)

</div>

<table>
<tr>
<td width="25%" valign="top">

<sub>NOW // STUDYING</sub><br>
**BS Data Science & Applications**<br>
IIT Madras · CGPA **9.0**<br>+ Scaler School of Technology

</td>
<td width="25%" valign="top">

<sub>LATEST // PODIUM</sub><br>
**Runner-up**<br>
Paradox DSA Triathlon<br>IIT Madras · 2026

</td>
<td width="25%" valign="top">

<sub>LATEST // HACKATHON</sub><br>
**Meta PyTorch OpenEnv**<br>
Team submission · 2026<br>[Meta OpenEnv →](https://github.com/Aditya2514/Meta_OpenEnv)

</td>
<td width="25%" valign="top">

<sub>LATEST // BUILD</sub><br>
**BenchShield**<br>
Leak audits for AI benchmarks<br>[Open →](https://github.com/Aditya2514/BenchShield)

</td>
</tr>
</table>

<img src="assets/aurora/divider-01.svg" width="100%" alt="" />

## 01 Base camp

<sub>AURORA // 01</sub>

<img src="assets/aurora/basecamp.svg" width="100%" alt="Base camp. What happens when the model is wrong? Aditya studies at IIT Madras and Scaler School of Technology and builds the layer around the model: rules that can overrule it, retrieval that keeps it honest, consent before it acts and a way to undo. The loop: the model proposes, the system checks, the person decides." />

<img src="assets/aurora/divider-02.svg" width="100%" alt="" />

## 02 Ascent

<sub>AURORA // 02</sub>

<img src="assets/aurora/ascent.svg" width="100%" alt="Every public repository as a star in the order it began, rising from a static portfolio through a first live deploy, a first hackathon, multi-agent contract review, a local desktop agent and multimodal search, to database-enforced billing and AI-evaluation security." />

<sub>Each star is a real repository, placed in the order it was created. The line only climbs.</sub>

<img src="assets/aurora/divider-03.svg" width="100%" alt="" />

## 03 Expeditions

<sub>AURORA // 03</sub>

<img src="assets/aurora/expeditions.svg" width="100%" alt="Six flagship systems with a live number from each repository: LexGuard's trap checks, Pikina's schema-checked capabilities, Noesis's media types, and the test suites of Mobius, BenchShield and HostelDesk; plus Resilion, ShopKart, Meta OpenEnv and a C++ shell." />

<sub>Every number on these cards is re-read from its own repository each time the page refreshes.</sub>

<img src="assets/aurora/divider-01.svg" width="100%" alt="" />

## 04 Field notes

<sub>AURORA // 04 · open any card for the architecture, and the code links for the exact lines</sub>

<table>
<tr>
<td width="50%" valign="top">

**LexGuard**<br>
<sub>LEGAL AI · INDIAN LAW</sub>

![Node.js](https://img.shields.io/badge/Node.js-08141F?style=flat-square&logo=nodedotjs&logoColor=339933) ![React](https://img.shields.io/badge/React-08141F?style=flat-square&logo=react&logoColor=61DAFB) ![MongoDB](https://img.shields.io/badge/MongoDB-08141F?style=flat-square&logo=mongodb&logoColor=47A248) ![Redis](https://img.shields.io/badge/Redis-08141F?style=flat-square&logo=redis&logoColor=DC382D)

Makes contract risks easier to inspect before signing. A staged agent pipeline examines clauses, checks explicit traps, **verifies every statute it cites** and proposes rewrites.

`33 tests` `CI` `Docker`

<details>
<summary>Architecture notes</summary>
<br>

A deterministic auditor runs hand-written trap patterns before any agent reads a risk level, and it can force an escalation: LLMs under-rate predatory clauses written in calm legal language. Citations are looked up and graded against a statute database. Providers fail mid-document, so the AI client falls through Gemini, Groq, Hugging Face, Grok and local Ollama. PDFs are repaired by a two-pass chunker before any model sees them, and clauses are keyed by position because LLM-echoed IDs drifted. It runs inside 512 MB: a 380 MB V8 heap cap, idle models unloaded, GC after each job.

</details>

**In the code:** [`rule gate`](https://github.com/Aditya2514/LexGuard/blob/2e6cb460aa9efabc2a51d3aa3c7aaf02849169a5/backend/src/services/jobQueueService.js#L107) · [`citation check`](https://github.com/Aditya2514/LexGuard/blob/2e6cb460aa9efabc2a51d3aa3c7aaf02849169a5/backend/src/services/citationVerifier.js#L404) · [`512 MB budget`](https://github.com/Aditya2514/LexGuard/blob/2e6cb460aa9efabc2a51d3aa3c7aaf02849169a5/backend/package.json#L8)

[Source →](https://github.com/Aditya2514/LexGuard)

</td>
<td width="50%" valign="top">

**Pikina**<br>
<sub>AGENT · OFFLINE DESKTOP</sub>

![Python](https://img.shields.io/badge/Python-08141F?style=flat-square&logo=python&logoColor=3776AB) ![Electron](https://img.shields.io/badge/Electron-08141F?style=flat-square&logo=electron&logoColor=47848F) ![Ollama](https://img.shields.io/badge/Ollama-08141F?style=flat-square&logo=ollama&logoColor=FFFFFF) ![SQLite](https://img.shields.io/badge/SQLite-08141F?style=flat-square&logo=sqlite&logoColor=74B9E8)

An offline-first Windows/Linux assistant with local inference, validated tools and **consent for anything high-risk**.

`287 tests` `CI`

<details>
<summary>Architecture notes</summary>
<br>

Known intents go through a regex router with no model call; everything else goes to a local model through Ollama. Every proposed action is schema-checked against a capability registry. One consent rule covers every entry point: level 4 always asks, and level 3 asks when the action can't be rolled back. Multi-step plans run as transactions and roll back step by step when one fails.

</details>

**In the code:** [`validator`](https://github.com/Aditya2514/Pikina/blob/ba2ae048fa05442cbc1a6c83fc253384c8562f34/src/pikina/validation/schema_check.py#L10) · [`consent rule`](https://github.com/Aditya2514/Pikina/blob/ba2ae048fa05442cbc1a6c83fc253384c8562f34/src/pikina/registry/gatekeeper.py#L16) · [`rollback`](https://github.com/Aditya2514/Pikina/blob/ba2ae048fa05442cbc1a6c83fc253384c8562f34/src/pikina/transactions/rollback_engine.py#L15)

[Source →](https://github.com/Aditya2514/Pikina)

</td>
</tr>
<tr>
<td width="50%" valign="top">

**Noesis**<br>
<sub>MULTIMODAL RAG · with Apurva Patil</sub>

![Python](https://img.shields.io/badge/Python-08141F?style=flat-square&logo=python&logoColor=3776AB) ![ChromaDB](https://img.shields.io/badge/ChromaDB-08141F?style=flat-square&logo=databricks&logoColor=FF6B6B) ![Whisper](https://img.shields.io/badge/Whisper-08141F?style=flat-square&logo=openai&logoColor=FFFFFF) ![Streamlit](https://img.shields.io/badge/Streamlit-08141F?style=flat-square&logo=streamlit&logoColor=FF4B4B)

Finds the useful moment across a pile of mixed media. Video, audio, PDFs and images go in; **every answer links to a timestamp or page**.

`3 tests`

<details>
<summary>Architecture notes</summary>
<br>

Each source becomes a SuperChunk that keeps its time window or page. Dense (ChromaDB) and sparse (BM25) results are merged with reciprocal rank fusion, a local cross-encoder reranks them, and a separate fact-audit pass labels every claim in the answer as supported, partially supported or unsupported.

</details>

**In the code:** [`RRF fusion`](https://github.com/Aditya2514/Noesis/blob/fde4e09283833cd25ec9e58777d0f6d74fa33bce/hybrid_retrieve.py#L177) · [`local reranker`](https://github.com/Aditya2514/Noesis/blob/fde4e09283833cd25ec9e58777d0f6d74fa33bce/hybrid_retrieve.py#L28) · [`fact audit`](https://github.com/Aditya2514/Noesis/blob/fde4e09283833cd25ec9e58777d0f6d74fa33bce/grounded_generate.py#L205)

[Source →](https://github.com/Aditya2514/Noesis)

</td>
<td width="50%" valign="top">

**Mobius**<br>
<sub>BILLING · POSTGRES INVARIANTS · with Apurva Patil</sub>

![TypeScript](https://img.shields.io/badge/TypeScript-08141F?style=flat-square&logo=typescript&logoColor=3178C6) ![Node.js](https://img.shields.io/badge/Node.js-08141F?style=flat-square&logo=nodedotjs&logoColor=339933) ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-08141F?style=flat-square&logo=postgresql&logoColor=4169E1) ![Prisma](https://img.shields.io/badge/Prisma-08141F?style=flat-square&logo=prisma&logoColor=FFFFFF) ![React](https://img.shields.io/badge/React-08141F?style=flat-square&logo=react&logoColor=61DAFB) ![MUI](https://img.shields.io/badge/MUI-08141F?style=flat-square&logo=mui&logoColor=007FFF)

Runs the whole life of a subscription, from quotation to recurring invoices and payments, and **the database itself enforces that billing is correct**.

`98 tests` `CI` `Docker`

<details>
<summary>Architecture notes</summary>
<br>

Quotation → confirmation → activation → recurring invoices → payments → reports, across an admin console, a staff workspace and a customer portal, with product variants, GST, discount campaigns and four billing cadences. A `UNIQUE (subscription_id, period_start)` constraint plus `ON CONFLICT DO NOTHING` means re-runs and parallel runs cannot double-bill; each subscription is locked `FOR UPDATE SKIP LOCKED`; a catch-up loop bills every period missed during downtime; and a discount slot is claimed with one conditional `UPDATE`, so two invoices can never take the last one. Money is computed to the paisa.

</details>

**In the code:** [`no double billing`](https://github.com/Aditya2514/Mobius/blob/fec1c089ead7dc6c91479c97c859c7f334f288ed/server/prisma/migrations/0001_init/migration.sql#L230) · [`idempotent insert`](https://github.com/Aditya2514/Mobius/blob/fec1c089ead7dc6c91479c97c859c7f334f288ed/server/src/modules/billing/engine.ts#L80) · [`parallel-safe lock`](https://github.com/Aditya2514/Mobius/blob/fec1c089ead7dc6c91479c97c859c7f334f288ed/server/src/modules/billing/engine.ts#L55) · [`atomic discount claim`](https://github.com/Aditya2514/Mobius/blob/fec1c089ead7dc6c91479c97c859c7f334f288ed/server/src/modules/billing/engine.ts#L164)

[Source →](https://github.com/Aditya2514/Mobius)

</td>
</tr>
<tr>
<td width="50%" valign="top">

**BenchShield**<br>
<sub>AI EVALUATION · SECURITY · with Rudra Patel</sub>

![Python](https://img.shields.io/badge/Python-08141F?style=flat-square&logo=python&logoColor=3776AB) ![FastAPI](https://img.shields.io/badge/FastAPI-08141F?style=flat-square&logo=fastapi&logoColor=009688) ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-08141F?style=flat-square&logo=postgresql&logoColor=4169E1) ![Pydantic](https://img.shields.io/badge/Pydantic-08141F?style=flat-square&logo=pydantic&logoColor=E92063) ![uv](https://img.shields.io/badge/uv-08141F?style=flat-square&logo=uv&logoColor=DE5FE9)

Finds where an AI benchmark's questions and answers have leaked onto the web, and **backs every finding with pinned, human-reviewed evidence**.

`117 tests` `Docker` `7 ADRs`

<details>
<summary>Architecture notes</summary>
<br>

Benchmarks lose their value once their answers leak, because browsing agents can look them up instead of solving the task. BenchShield keeps four steps apart (discovery, verification, agent experiments and human review) so a promising search hit can never become an unsupported contamination claim. Protected answers live in a vault encrypted with AES-256-GCM. Long-running work runs on a durable PostgreSQL worker with leases, heartbeats and fencing tokens, and every major design choice is written down as an architecture decision record.

</details>

**In the code:** [`AES-256-GCM vault`](https://github.com/Aditya2514/BenchShield/blob/d1beb1b0ce341d6aac0860adc49e549554ab36b1/apps/backend/src/benchshield/storage/vault_encryption.py#L5) · [`durable worker`](https://github.com/Aditya2514/BenchShield/blob/d1beb1b0ce341d6aac0860adc49e549554ab36b1/apps/backend/src/benchshield/workers/durable_worker.py#L1) · [`fenced task claim`](https://github.com/Aditya2514/BenchShield/blob/d1beb1b0ce341d6aac0860adc49e549554ab36b1/apps/backend/src/benchshield/workers/durable_worker.py#L104)

[Source →](https://github.com/Aditya2514/BenchShield)

</td>
<td width="50%" valign="top">

**Resilion**<br>
<sub>SUPPLY-CHAIN INTELLIGENCE</sub>

![Python](https://img.shields.io/badge/Python-08141F?style=flat-square&logo=python&logoColor=3776AB) ![NetworkX](https://img.shields.io/badge/NetworkX-08141F?style=flat-square&logo=python&logoColor=8FB8FF) ![Gemini](https://img.shields.io/badge/Gemini-08141F?style=flat-square&logo=googlegemini&logoColor=8E75B2)

Turns supply-chain news into structured risk events and **traces which industries get hit**.

<details>
<summary>Architecture notes</summary>
<br>

Gemini extracts events from articles; validators reject any event type, severity or trade corridor the graph doesn't already know, so the model can't invent a place. Graph traversal then walks from the disrupted corridor to the refineries and industries downstream and scores their exposure.

</details>

**In the code:** [`no invented corridors`](https://github.com/Aditya2514/Resilion/blob/c6c3dbb3c883da1731f3ecaac6666d49ff75bf2e/backend/agents/risk_agent.py#L194) · [`impact traversal`](https://github.com/Aditya2514/Resilion/blob/c6c3dbb3c883da1731f3ecaac6666d49ff75bf2e/backend/graph/traversal.py#L34)

[Source →](https://github.com/Aditya2514/Resilion)

</td>
</tr>
<tr>
<td width="50%" valign="top">

**HostelDesk**<br>
<sub>PRODUCT · OPERATIONS</sub>

![TypeScript](https://img.shields.io/badge/TypeScript-08141F?style=flat-square&logo=typescript&logoColor=3178C6) ![React](https://img.shields.io/badge/React-08141F?style=flat-square&logo=react&logoColor=61DAFB) ![Express](https://img.shields.io/badge/Express-08141F?style=flat-square&logo=express&logoColor=FFFFFF) ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-08141F?style=flat-square&logo=postgresql&logoColor=4169E1) ![Prisma](https://img.shields.io/badge/Prisma-08141F?style=flat-square&logo=prisma&logoColor=FFFFFF)

Hostel complaints with **explained ETA ranges**, automatic routing and escalation. Live on Neon and Render.

`201 tests` **[● live ↗](https://hostel-desk-three.vercel.app)**

<details>
<summary>Architecture notes</summary>
<br>

Tickets route to the right staff member automatically. ETAs come from simulating that person's whole open queue rather than a fixed SLA, a late ticket tells the student why it is late, and a background job escalates anything past its deadline.

</details>

**In the code:** [`delay reasons`](https://github.com/Aditya2514/HostelDesk/blob/9c978ace415069e1f1f8b07e55d0869ec28b1260/server/src/modules/scheduling/eta.service.ts#L78) · [`escalation job`](https://github.com/Aditya2514/HostelDesk/blob/9c978ace415069e1f1f8b07e55d0869ec28b1260/server/src/jobs/escalation.job.ts#L21)

[Source →](https://github.com/Aditya2514/HostelDesk)

</td>
<td width="50%" valign="top">

**ShopKart**<br>
<sub>E-COMMERCE · with Apurva Patil</sub>

![React](https://img.shields.io/badge/React-08141F?style=flat-square&logo=react&logoColor=61DAFB) ![Express](https://img.shields.io/badge/Express-08141F?style=flat-square&logo=express&logoColor=FFFFFF) ![MongoDB](https://img.shields.io/badge/MongoDB-08141F?style=flat-square&logo=mongodb&logoColor=47A248) ![Razorpay](https://img.shields.io/badge/Razorpay-08141F?style=flat-square&logo=razorpay&logoColor=3395FF)

A store whose checkout **never trusts the browser with a price**.

<details>
<summary>Architecture notes</summary>
<br>

The server rebuilds every order from database prices and live stock, and an order is marked paid only after Razorpay's signature checks out with HMAC-SHA256 on the server.

</details>

**In the code:** [`server-side total`](https://github.com/Aditya2514/Shopkart/blob/3a909ed607c55817e66ba5d623886d44ea2e0460/server/controllers/order.controller.js#L71) · [`signature check`](https://github.com/Aditya2514/Shopkart/blob/3a909ed607c55817e66ba5d623886d44ea2e0460/server/controllers/order.controller.js#L171)

[Source →](https://github.com/Aditya2514/Shopkart)

</td>
</tr>
<tr>
<td width="50%" valign="top">

**C++ Shell**<br>
<sub>SYSTEMS · POSIX</sub>

![C++23](https://img.shields.io/badge/C%2B%2B23-08141F?style=flat-square&logo=cplusplus&logoColor=00599C) ![POSIX](https://img.shields.io/badge/POSIX-08141F?style=flat-square&logo=linux&logoColor=FCC624) ![CMake](https://img.shields.io/badge/CMake-08141F?style=flat-square&logo=cmake&logoColor=064F8C)

A shell built on **fork, exec, pipe and dup2**: quoting, redirection, pipelines and background jobs.

<details>
<summary>Architecture notes</summary>
<br>

Builtins, PATH lookup, a quoting state machine for single and double quotes, I/O redirection and multi-stage pipelines. Each stage's stdin is rewired to the previous stage's pipe with dup2, and every unused pipe end is closed so the next stage sees EOF.

</details>

**In the code:** [`fork`](https://github.com/Aditya2514/codecrafters-shell-cpp/blob/c4adda13d0f55a81f540b209b496a4cb087a1e1d/src/main.cpp#L366) · [`dup2 wiring`](https://github.com/Aditya2514/codecrafters-shell-cpp/blob/c4adda13d0f55a81f540b209b496a4cb087a1e1d/src/main.cpp#L369) · [`quote parser`](https://github.com/Aditya2514/codecrafters-shell-cpp/blob/c4adda13d0f55a81f540b209b496a4cb087a1e1d/src/main.cpp#L168)

[Source →](https://github.com/Aditya2514/codecrafters-shell-cpp)

</td>
<td width="50%" valign="top">

**Meta OpenEnv**<br>
<sub>AGENT ENVIRONMENT · HACKATHON</sub>

![Python](https://img.shields.io/badge/Python-08141F?style=flat-square&logo=python&logoColor=3776AB) ![FastAPI](https://img.shields.io/badge/FastAPI-08141F?style=flat-square&logo=fastapi&logoColor=009688) ![Docker](https://img.shields.io/badge/Docker-08141F?style=flat-square&logo=docker&logoColor=2496ED)

An environment where agents juggle assignments, bugs and deadlines, and **finishing by burning out still loses points**.

`CI` `Docker`

<details>
<summary>Architecture notes</summary>
<br>

Built for the Meta PyTorch OpenEnv Hackathon. An agent schedules work against hard deadlines across easy, medium and hard tasks; the graders reward finished work and add bonuses only for burnout-free days (none over 8 hours) and balanced schedules.

</details>

**In the code:** [`step contract`](https://github.com/Aditya2514/Meta_OpenEnv/blob/328688b03ec3310cf8498f83ad6fd8dd7e1b00f6/src/envs/assignment_planner/environment.py#L106) · [`burnout rule`](https://github.com/Aditya2514/Meta_OpenEnv/blob/328688b03ec3310cf8498f83ad6fd8dd7e1b00f6/src/envs/assignment_planner/graders.py#L190)

[Source →](https://github.com/Aditya2514/Meta_OpenEnv)

</td>
</tr>
</table>

<br>

**Smaller climbs**

| Project | What it does | Stack |
| :-- | :-- | :-- |
| [Vidya](https://github.com/Aditya2514/Vidya) | Book discovery in React Native: debounced search, Firebase sign-in, saved lists, strict TypeScript. | React Native · TypeScript · Firebase |
| [Fintrac](https://github.com/Aditya2514/Fintrac) | Personal budgeting with Gemini-powered spending analysis. | React · Vite · Recharts · Gemini |
| [Naukri](https://github.com/Aditya2514/Naukri) · [live ↗](https://Aditya2514.github.io/Naukri/) | A dark-mode job portal with a 100-entry API, persistent saved jobs and sliding-window pagination. | React · Vite |
| [FinancePro](https://github.com/Aditya2514/FinancePro) | A vanilla-JavaScript finance dashboard: multiple profiles, analytics and goal tracking. | JavaScript |

<img src="assets/aurora/divider-02.svg" width="100%" alt="" />

## 05 Rhythm

<sub>AURORA // 05</sub>

<img src="assets/aurora/rhythm.svg" width="100%" alt="When the code ships: commits bucketed by hour of day in IST, drawn as rays of light over a horizon while a sun and a moon cross the sky every 24 seconds and light each hour in turn; below, seven nights of aurora, one band per weekday, brightest where commits cluster; plus the derived chronotype, focus window, weekend share and the longest unbroken session." />

<sub>Every commit I've authored on the default branch of my public repos in the last year, bucketed by IST hour and weekday and recomputed every six hours. The chronotype is derived from the data, not chosen.</sub>

<img src="assets/aurora/divider-03.svg" width="100%" alt="" />

## 06 Instruments

<sub>AURORA // 06</sub>

<img src="assets/aurora/instruments.svg" width="100%" alt="Engineering signals counted across every public repository: test cases, test files, CI workflows, dockerised repos, design documents and architecture decision records, and pull requests, with a signal board per repository and the people these were built with." />

<img src="assets/aurora/divider-01.svg" width="100%" alt="" />

## 07 Terrain

<sub>AURORA // 07</sub>

<img src="assets/aurora/terrain.svg" width="100%" alt="Every public repository drawn as a mountain peak: its height is the amount of code, its position is when it began, and its colour is its kind: AI systems, agents, products or systems. Flags mark the systems described above." />

<sub>Each new repository rises on the right the next time the page refreshes.</sub>

<img src="assets/aurora/divider-02.svg" width="100%" alt="" />

## 08 Bedrock

<sub>AURORA // 08</sub>

<img src="assets/aurora/bedrock.svg" width="100%" alt="Languages drawn as layers of rock under a snowy forest, each layer as thick as its share of the code across all public repositories." />

| | |
| :-- | :-- |
| <sub>**LANGUAGES**</sub><br><sub>Write the core logic</sub> | ![Python](https://img.shields.io/badge/Python-08141F?style=flat-square&logo=python&logoColor=3776AB) ![JavaScript](https://img.shields.io/badge/JavaScript-08141F?style=flat-square&logo=javascript&logoColor=F7DF1E) ![TypeScript](https://img.shields.io/badge/TypeScript-08141F?style=flat-square&logo=typescript&logoColor=3178C6) ![C++](https://img.shields.io/badge/C%2B%2B-08141F?style=flat-square&logo=cplusplus&logoColor=00599C) |
| <sub>**AI &amp; RETRIEVAL**</sub><br><sub>Ground answers and connect models</sub> | ![Ollama](https://img.shields.io/badge/Ollama-08141F?style=flat-square&logo=ollama&logoColor=FFFFFF) ![Gemini](https://img.shields.io/badge/Gemini-08141F?style=flat-square&logo=googlegemini&logoColor=8E75B2) ![Groq](https://img.shields.io/badge/Groq-08141F?style=flat-square&logo=groq&logoColor=F55036) ![Hugging Face](https://img.shields.io/badge/Hugging%20Face-08141F?style=flat-square&logo=huggingface&logoColor=FFD21E) ![ChromaDB](https://img.shields.io/badge/ChromaDB-08141F?style=flat-square&logo=databricks&logoColor=FF6B6B) ![sentence-transformers](https://img.shields.io/badge/sentence--transformers-08141F?style=flat-square&logo=pytorch&logoColor=EE4C2C) |
| <sub>**BACKEND**</sub><br><sub>Expose services and coordinate work</sub> | ![Node.js](https://img.shields.io/badge/Node.js-08141F?style=flat-square&logo=nodedotjs&logoColor=339933) ![Express](https://img.shields.io/badge/Express-08141F?style=flat-square&logo=express&logoColor=FFFFFF) ![FastAPI](https://img.shields.io/badge/FastAPI-08141F?style=flat-square&logo=fastapi&logoColor=009688) ![Flask](https://img.shields.io/badge/Flask-08141F?style=flat-square&logo=flask&logoColor=FFFFFF) |
| <sub>**DATA**</sub><br><sub>Store, query and cache</sub> | ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-08141F?style=flat-square&logo=postgresql&logoColor=4169E1) ![MongoDB](https://img.shields.io/badge/MongoDB-08141F?style=flat-square&logo=mongodb&logoColor=47A248) ![Redis](https://img.shields.io/badge/Redis-08141F?style=flat-square&logo=redis&logoColor=DC382D) ![SQLite](https://img.shields.io/badge/SQLite-08141F?style=flat-square&logo=sqlite&logoColor=74B9E8) |
| <sub>**INTERFACES**</sub><br><sub>Make systems usable</sub> | ![React](https://img.shields.io/badge/React-08141F?style=flat-square&logo=react&logoColor=61DAFB) ![React Native](https://img.shields.io/badge/React%20Native-08141F?style=flat-square&logo=react&logoColor=61DAFB) ![Electron](https://img.shields.io/badge/Electron-08141F?style=flat-square&logo=electron&logoColor=47848F) ![Streamlit](https://img.shields.io/badge/Streamlit-08141F?style=flat-square&logo=streamlit&logoColor=FF4B4B) |
| <sub>**DELIVERY**</sub><br><sub>Version, test and ship</sub> | ![Git](https://img.shields.io/badge/Git-08141F?style=flat-square&logo=git&logoColor=F05032) ![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-08141F?style=flat-square&logo=githubactions&logoColor=2088FF) ![Docker](https://img.shields.io/badge/Docker-08141F?style=flat-square&logo=docker&logoColor=2496ED) ![Vercel](https://img.shields.io/badge/Vercel-08141F?style=flat-square&logo=vercel&logoColor=FFFFFF) |

<img src="assets/aurora/divider-03.svg" width="100%" alt="" />

## 09 Trail log

<sub>AURORA // 09</sub>

<img src="assets/aurora/trail.svg" width="100%" alt="The latest commits across the systems above, drawn as waypoints on a trail climbing a mountain under the northern lights, newest at the summit." />

<img src="assets/aurora/divider-01.svg" width="100%" alt="" />

## 10 Record

<sub>AURORA // 10</sub>

| Education | Achievement |
| :-- | :-- |
| **IIT Madras** · BS Data Science & Applications · 2025–2029 · CGPA **9.0/10** | **Runner-up** · Paradox DSA Triathlon · IIT Madras · 2026 |
| **Scaler School of Technology** · 2025–2029 | **Meta PyTorch OpenEnv Hackathon** · 2026 · team submission |

<img src="assets/aurora/divider-02.svg" width="100%" alt="" />

## 11 Send a signal

<sub>AURORA // 11</sub>

<img src="assets/aurora/flare.svg" width="100%" alt="A signal flare rises from a mountain into the northern lights over a still lake. Let's build something worth finding: AI engineering internships, agent systems, hackathon teams." />

<div align="center">

<a href="https://www.linkedin.com/in/aditya-singh-8286b137a/"><img src="assets/aurora/channel-linkedin.svg" width="32%" alt="LinkedIn" /></a>
<a href="mailto:adityasinghv05@gmail.com"><img src="assets/aurora/channel-email.svg" width="32%" alt="Email" /></a>
<a href="https://github.com/Aditya2514?tab=repositories"><img src="assets/aurora/channel-github.svg" width="32%" alt="GitHub repositories" /></a>

<sub>Scenes redrawn from live GitHub data every six hours · last run 25 Nov 2026, 08:33 UTC</sub>

</div>
