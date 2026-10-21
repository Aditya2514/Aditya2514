<div align="center">

<sub>[ LINKEDIN ](https://www.linkedin.com/in/aditya-singh-8286b137a/) &nbsp;·&nbsp; [ EMAIL ](mailto:adityasinghv05@gmail.com) &nbsp;·&nbsp; [ FLAGSHIP: LEXGUARD ](https://github.com/Aditya2514/LexGuard)</sub>

<img src="assets/hero.svg" alt="Aditya Singh: LLM systems, AI agents, full-stack. A typed line cycles through: I build LLM agents that are safe to act on, checked by deterministic code, grounded by retrieval, approved by a person before anything irreversible. A pulse runs from MODEL to VERIFY to PERSON. IIT Madras, BS Data Science, CGPA 9.0; runner-up, Paradox DSA Triathlon 2026." width="100%" />

</div>

<table>
<tr>
<td width="25%"><a href="#01-about"><code>01</code> ABOUT</a></td>
<td width="25%"><a href="#02-how-i-build"><code>02</code> HOW I BUILD</a></td>
<td width="25%"><a href="#03-flagship-systems"><code>03</code> FLAGSHIP</a></td>
<td width="25%"><a href="#04-more-projects"><code>04</code> PROJECTS</a></td>
</tr>
<tr>
<td><a href="#05-live-signal"><code>05</code> SIGNAL</a></td>
<td><a href="#06-stack"><code>06</code> STACK</a></td>
<td><a href="#07-education--honors"><code>07</code> EDUCATION</a></td>
<td><a href="#08-contact"><code>08</code> CONTACT</a></td>
</tr>
</table>

<table>
<tr>
<td width="33%" valign="top">

<sub>FLAGSHIP // LEXGUARD</sub><br>
**AI contract review for Indian law**<br>
130+ commits · solo · May – Aug 2026

</td>
<td width="33%" valign="top">

<sub>STUDYING // IIT MADRAS</sub><br>
**BS in Data Science & Applications**<br>
CGPA 9.0 / 10 · 2025 – 2029

</td>
<td width="33%" valign="top">

<sub>LATEST // WIN</sub><br>
**Paradox DSA Triathlon, IIT Madras**<br>
Runner-up (2nd place) · 2026

</td>
</tr>
</table>

<br>

## 01 About

<img src="assets/terminal.svg" alt="Terminal session: whoami prints Aditya Singh, BS Data Science at IIT Madras (CGPA 9.0), Scaler School of Technology; now.txt says Building LLM agents that are safe to act on; git log shows the four most recent real commits; ls lists LexGuard, Pikina, Noesis, Resilion, Meta_OpenEnv and codecrafters-shell-cpp." width="100%" />

I'm studying for a BS in Data Science & Applications at IIT Madras, co-enrolled at Scaler School of Technology, and I build LLM systems that are safe to act on. In my projects the model is the reasoning layer, not the foundation: deterministic code checks what it says, retrieval grounds it, and a person approves anything that can't be undone.

> *"Language models are lazy-loaded reasoning services sitting on top of deterministic infrastructure, not the thing the infrastructure depends on."* (from the Pikina design notes)

Four rules, each one shipped in a repo:

- **Check the model in code.** LexGuard's 38 trap patterns can overrule the LLM's risk rating, and a contradiction engine cross-checks fees, dates and jurisdictions across clauses.
- **Ground every answer.** Noesis answers cite the timestamp, page or frame behind each claim, and an LLM auditor checks them; LexGuard cites statutes retrieved from 7,556+ Indian law sections.
- **Ask before acting.** Pikina validates every model-proposed action against a tool manifest and pops a native consent dialog before high-risk OS actions.
- **Degrade, don't die.** LexGuard falls back across four LLM providers and fits its backend in 512 MB; Pikina answers known commands with plain regex routing before it ever calls a model.

<br>

## 02 How I Build

<img src="assets/pattern.svg" alt="How I build: in LexGuard, Resilion, Pikina and Noesis a model proposes, code verifies, and a person decides. Each row lists the mechanism used at each stage." width="100%" />

<br>

## 03 Flagship Systems

<img src="assets/lexguard_flow.svg" alt="Animated walkthrough of LexGuard on an illustrative four-clause contract: the classifier tags clause types, the risk analyst rates them, the safety net catches a training-bond clause the LLM rated LOW and flips it to CRITICAL, the citation verifier marks two real Indian Contract Act sections as strong and a non-existent section 412 as hallucinated, and a fairer rewrite is drafted." width="100%" />

<br>

<table>
<tr>
<td width="50%" valign="top">

**◉ LexGuard**<br>
<sub>`N.01` · LEGAL AI · CONTRACT REVIEW</sub>

![Node.js](https://img.shields.io/badge/Node.js-161B22?style=flat-square&logo=nodedotjs&logoColor=5FA04E) ![React](https://img.shields.io/badge/React-161B22?style=flat-square&logo=react&logoColor=61DAFB) ![MongoDB](https://img.shields.io/badge/MongoDB_Atlas-161B22?style=flat-square&logo=mongodb&logoColor=47A248) ![Gemini](https://img.shields.io/badge/Gemini-161B22?style=flat-square&logo=googlegemini&logoColor=8E75B2) ![Tests](https://github.com/Aditya2514/LexGuard/actions/workflows/tests.yml/badge.svg)

Upload an employment, freelance or vendor contract. LexGuard splits it into clauses, rates how risky each one is for the signer, explains it in plain language, cites the Indian statute it touches, and drafts a fairer rewrite.

<details>
<summary>Engineering notes</summary>
<br>

A sequential agent pipeline (pre-flight context, classifier, risk analyst, adversarial judge, advocate, compliance) runs behind a Redis or MongoDB job queue. After the LLM passes, a deterministic detector with 38 trap patterns can force an escalation, and a reflection loop makes the model explain what it missed. The backend was squeezed into a 512 MB host with a 380 MB heap cap and post-job GC, and the AI client cascades across Gemini, Groq, Hugging Face and local Ollama when a provider runs out of quota.

On the committed benchmarks it gets 28/30 clause types and 21/30 risk tiers right on the master suite, and every miss over-flags rather than under-flags. The offline unit suite runs in CI.

</details>

[Source](https://github.com/Aditya2514/LexGuard)

</td>
<td width="50%" valign="top">

**◉ Pikina**<br>
<sub>`N.02` · LOCAL AI · DESKTOP AGENT</sub>

![Python](https://img.shields.io/badge/Python-161B22?style=flat-square&logo=python&logoColor=3776AB) ![Ollama](https://img.shields.io/badge/Ollama-161B22?style=flat-square&logo=ollama&logoColor=white) ![Electron](https://img.shields.io/badge/Electron-161B22?style=flat-square&logo=electron&logoColor=47848F) ![Windows](https://img.shields.io/badge/Windows-161B22?style=flat-square&logo=windows&logoColor=0078D4) ![Linux](https://img.shields.io/badge/Linux-161B22?style=flat-square&logo=linux&logoColor=FCC624)

An offline-first personal operating layer for Windows and Linux. Press a hotkey and type what you want; Pikina routes it to a tool, validates the action, and asks first when it is risky. Pre-alpha.

<details>
<summary>Engineering notes</summary>
<br>

Commands that match a known pattern are handled by a Tier 1 regex router with no model call; only misses go to a local Ollama model, which must return a registered tool or `no_match`, so it can't invent actions. An Action Validation Layer checks every model-proposed action against the tool manifest, and level 4+ actions from either tier need a native confirmation dialog (MessageBoxW on Windows, zenity or kdialog on Linux). Multi-step alias chains run through a transactional executor that undoes completed steps in reverse order if one fails; a DAG scheduler with starvation protection is built and tested, waiting for the planner that will call it. Event-driven daemons and a dual-tier memory sit underneath.

</details>

[Source](https://github.com/Aditya2514/Pikina)

</td>
</tr>
<tr>
<td width="50%" valign="top">

**◉ Resilion**<br>
<sub>`N.03` · AGENTS · SUPPLY-CHAIN RISK</sub>

![Python](https://img.shields.io/badge/Python-161B22?style=flat-square&logo=python&logoColor=3776AB) ![FastAPI](https://img.shields.io/badge/FastAPI-161B22?style=flat-square&logo=fastapi&logoColor=009688) ![React](https://img.shields.io/badge/React-161B22?style=flat-square&logo=react&logoColor=61DAFB) ![NetworkX](https://img.shields.io/badge/NetworkX-161B22?style=flat-square) ![Gemini](https://img.shields.io/badge/Gemini-161B22?style=flat-square&logo=googlegemini&logoColor=8E75B2)

India imports most of its crude oil, much of it through the Strait of Hormuz. Resilion watches geopolitical signals and shows which refineries and industries are exposed when a route is at risk. In progress: ranking alternative supply routes for a person to approve.

<details>
<summary>Engineering notes</summary>
<br>

Built so far: data sources for GDELT, EIA, OFAC and RSS feeds, a Gemini Risk Watcher agent that turns them into structured disruption events, and a NetworkX graph of India's crude-oil supply corridors that traces which industries an event affects. Next: a Procurement Orchestrator that ranks reroutes by cost and transit delay, and an approval console so nothing executes without a person signing off.

</details>

[Source](https://github.com/Aditya2514/Resilion)

</td>
<td width="50%" valign="top">

**◉ Noesis**<br>
<sub>`N.04` · MULTIMODAL RAG</sub>

![Python](https://img.shields.io/badge/Python-161B22?style=flat-square&logo=python&logoColor=3776AB) ![Groq](https://img.shields.io/badge/Groq-161B22?style=flat-square) ![ChromaDB](https://img.shields.io/badge/ChromaDB-161B22?style=flat-square) ![Streamlit](https://img.shields.io/badge/Streamlit-161B22?style=flat-square&logo=streamlit&logoColor=FF4B4B)

Ask one question across videos, podcasts, PDFs and scanned pages, and get an answer that points to the exact timestamp, page or frame it came from. Built with [@apurva202](https://github.com/apurva202).

<details>
<summary>Engineering notes</summary>
<br>

Video and audio go through FFmpeg and Whisper with word-level timestamps; keyframes come from scene-change detection with perceptual-hash de-duplication; PDFs through PyMuPDF and RapidOCR. Entity canonicalisation links a term spoken in a video to the same term in a PDF diagram. Retrieval is hybrid (BM25 + bge-small embeddings) with an ms-marco reranker, and a confidence cutoff decides between a full grounded answer and an extractive fallback.

</details>

[Source](https://github.com/Aditya2514/Noesis)

</td>
</tr>
</table>

<br>

## 04 More Projects

| Project | What it is | Stack |
| :-- | :-- | :-- |
| [**Meta_OpenEnv**](https://github.com/Aditya2514/Meta_OpenEnv) | Built for the Meta PyTorch OpenEnv Hackathon (2026): an OpenEnv environment where an RL or LLM agent triages assignments and production bugs against deadlines and a burnout budget. 110-test suite in CI. Team project. | Python · FastAPI · Docker · HF Spaces |
| [**ShopKart**](https://github.com/Aditya2514/Shopkart) | Full-stack store: JWT auth, catalog, wishlist, cart, server-side checkout, Razorpay payments. Built with [@apurva202](https://github.com/apurva202). | React · Express · MongoDB · Vercel |
| [**C++ shell**](https://github.com/Aditya2514/codecrafters-shell-cpp) | POSIX-style shell from scratch: quoting, redirection, multi-stage pipelines and background jobs on `fork`/`exec`/`pipe`/`dup2`. | C++23 |
| [**Vidya**](https://github.com/Aditya2514/Vidya) | Book discovery app with debounced search, infinite scroll, Firebase and Google sign-in, and persisted saved lists. | React Native · TypeScript · Redux Toolkit |
| [**Fintrac**](https://github.com/Aditya2514/Fintrac) | Personal finance tracker and budget dashboard with Gemini-powered spending analysis. | React · Vite · Recharts |
| [**Naukri**](https://github.com/Aditya2514/Naukri) | Dark-mode job portal UI with API-backed listings and saved jobs. | React · Vite |

<br>

## 05 Live Signal

<img src="assets/signal.svg" alt="Live GitHub signal for the last 12 months: total contributions, active months, longest streak, busiest week and public repos; weekly contribution bars with the peak week and weekly average marked; languages by bytes of code." width="100%" />

<img src="assets/rhythm.svg" alt="Build rhythm: a 24-hour clock of when I actually commit, in IST, with bar length equal to commits in each hour, the busiest hour highlighted, the share of night commits, the busiest weekday and a chronotype derived from commit times." width="100%" />

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Aditya2514/Aditya2514/output/github-snake-dark.svg" />
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Aditya2514/Aditya2514/output/github-snake.svg" />
  <img alt="A snake eating the last 12 months of contribution squares" src="https://raw.githubusercontent.com/Aditya2514/Aditya2514/output/github-snake-dark.svg" width="100%" />
</picture>

<sub>Generated from the GitHub API by GitHub Actions, not typed in by hand: stats, build rhythm and the terminal's git log refresh every 6 hours; the snake daily.</sub>

<br>

## 06 Stack

<table>
<tr>
<td width="50%" valign="top">

**LANGUAGES**<br>
![Python](https://img.shields.io/badge/Python-161B22?style=flat-square&logo=python&logoColor=3776AB)
![JavaScript](https://img.shields.io/badge/JavaScript-161B22?style=flat-square&logo=javascript&logoColor=F7DF1E)
![TypeScript](https://img.shields.io/badge/TypeScript-161B22?style=flat-square&logo=typescript&logoColor=3178C6)
![C++](https://img.shields.io/badge/C++-161B22?style=flat-square&logo=cplusplus&logoColor=00599C)

**AI / LLM**<br>
![Gemini](https://img.shields.io/badge/Gemini-161B22?style=flat-square&logo=googlegemini&logoColor=8E75B2)
![Groq](https://img.shields.io/badge/Groq-161B22?style=flat-square)
![Ollama](https://img.shields.io/badge/Ollama-161B22?style=flat-square&logo=ollama&logoColor=white)
![Hugging Face](https://img.shields.io/badge/Hugging_Face-161B22?style=flat-square&logo=huggingface&logoColor=FFD21E)
![ChromaDB](https://img.shields.io/badge/ChromaDB-161B22?style=flat-square)
![Whisper](https://img.shields.io/badge/Whisper-161B22?style=flat-square)

</td>
<td width="50%" valign="top">

**BACKEND & DATA**<br>
![Node.js](https://img.shields.io/badge/Node.js-161B22?style=flat-square&logo=nodedotjs&logoColor=5FA04E)
![Express](https://img.shields.io/badge/Express-161B22?style=flat-square&logo=express&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-161B22?style=flat-square&logo=fastapi&logoColor=009688)
![MongoDB](https://img.shields.io/badge/MongoDB-161B22?style=flat-square&logo=mongodb&logoColor=47A248)
![Redis](https://img.shields.io/badge/Redis-161B22?style=flat-square&logo=redis&logoColor=FF4438)
![NetworkX](https://img.shields.io/badge/NetworkX-161B22?style=flat-square)

**FRONTEND, MOBILE & INFRA**<br>
![React](https://img.shields.io/badge/React-161B22?style=flat-square&logo=react&logoColor=61DAFB)
![React Native](https://img.shields.io/badge/React_Native-161B22?style=flat-square&logo=react&logoColor=61DAFB)
![Electron](https://img.shields.io/badge/Electron-161B22?style=flat-square&logo=electron&logoColor=47848F)
![Docker](https://img.shields.io/badge/Docker-161B22?style=flat-square&logo=docker&logoColor=2496ED)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-161B22?style=flat-square&logo=githubactions&logoColor=2088FF)
![Vercel](https://img.shields.io/badge/Vercel-161B22?style=flat-square&logo=vercel&logoColor=white)

</td>
</tr>
</table>

<br>

## 07 Education & Honors

**Education**

| Program | Institution | When | Result |
| :-- | :-- | :-- | :-- |
| BS in Data Science & Applications | Indian Institute of Technology Madras | 2025 – 2029 | CGPA **9.0 / 10** |
| Co-enrolled with the IITM BS degree | Scaler School of Technology | 2025 – 2029 | |

**Honors**

| When | Event | Result |
| :-- | :-- | :-- |
| 2026 | Paradox DSA Triathlon, IIT Madras | **Runner-up (2nd place)** |
| 2026 | Meta PyTorch OpenEnv Hackathon | Built and submitted [Meta_OpenEnv](https://github.com/Aditya2514/Meta_OpenEnv) with a team |

<br>

## 08 Contact

<div align="center">

Happy to talk about LLM systems, agents with guardrails, or any of the repos above.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/aditya-singh-8286b137a/)
[![Email](https://img.shields.io/badge/Email-161B22?style=for-the-badge&logo=gmail&logoColor=EA4335)](mailto:adityasinghv05@gmail.com)
[![GitHub](https://img.shields.io/badge/GitHub-161B22?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Aditya2514)

</div>
