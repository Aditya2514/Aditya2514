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

<img src="assets/strip.svg" alt="Flagship: LexGuard — AI contract review for Indian law; 130+ commits · solo · May–Aug 2026. Studying: IIT Madras — BS in Data Science & Applications; CGPA 9.0 / 10 · 2025 – 2029. Latest win — Paradox DSA Triathlon, IIT Madras; Runner-up (2nd place) · 2026." width="100%" />

<br>

## 01 About

<img src="assets/terminal.svg" alt="Terminal session: whoami prints Aditya Singh, BS Data Science at IIT Madras (CGPA 9.0), Scaler School of Technology; now.txt says Building LLM agents that are safe to act on; git log shows the four most recent real commits; ls lists LexGuard, Pikina, Noesis, Resilion, Meta_OpenEnv and codecrafters-shell-cpp." width="100%" />

I'm studying for a BS in Data Science & Applications at IIT Madras, co-enrolled at Scaler School of Technology, and I build LLM systems that are safe to act on. In my projects the model is the reasoning layer, not the foundation: deterministic code checks what it says, retrieval grounds it, and a person approves anything that can't be undone.

> *"Language models are lazy-loaded reasoning services sitting on top of deterministic infrastructure, not the thing the infrastructure depends on."* (from the Pikina design notes)

Four rules, each one shipped in a repo:

- **Check the model in code.** LexGuard's 36 trap patterns can overrule the LLM's risk rating, and a contradiction engine cross-checks fees, dates and jurisdictions across clauses.
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

<p align="center">
<a href="https://github.com/Aditya2514/LexGuard"><img src="assets/card_lexguard.svg" width="49%" alt="Project card for LexGuard, a solo project from May to August 2026. Illustrative run: a scan passes three contract clauses; the LLM rated 'Repay 3,00,000 rupees if you resign' LOW, and one of 36 trap patterns forces it to CRITICAL. The citation verifier marks Indian Contract Act section 27 strong and section 412 hallucinated. Stack: Node.js, Redis job queue, MongoDB Atlas Vector Search." /></a>
<a href="https://github.com/Aditya2514/Pikina"><img src="assets/card_pikina.svg" width="49%" alt="Project card for Pikina, pre-alpha, started July 2026. Illustrative run in the quick panel: 'add todo call mom' matches a Tier 1 regex route, with no model call. 'remind me to pay rent' matches no regex, so it goes to a local llama3 model through Ollama, which must return a registered tool or no_match; it proposes todo.add at level 0, the Action Validation Layer checks that the tool is registered and the claimed level matches the registry, and it runs. Actions at level 4 or above, or with irreversible side effects, ask for native consent first. Stack: Python, Ollama, Electron." /></a>
</p>
<p align="center">
<a href="https://github.com/Aditya2514/Resilion"><img src="assets/card_resilion.svg" width="49%" alt="Project card for Resilion, in progress. A Gemini Risk Watcher agent turns news (GDELT headlines, Guardian articles) into structured disruption events. In this illustrative event, a news event lands on the Strait of Hormuz corridor in the NetworkX supply graph (seeded with 13 nodes and 19 edges); a 2-hop traversal lights the refineries it supplies (Jamnagar, Panipat, Mumbai) and then the industries they serve (power, petrochemicals, transport fuel, LPG). The Red Sea corridor is untouched. A human approval console is planned, drawn dashed. Stack: Python, NetworkX, Gemini, React." /></a>
<a href="https://github.com/Aditya2514/Noesis"><img src="assets/card_noesis.svg" width="49%" alt="Project card for Noesis, built by a team of 2 in August 2026. Video, audio and PDF sources send chunks into an index (Whisper with word-level timestamps, keyframes de-duplicated by perceptual hash, PyMuPDF plus RapidOCR plus a Gemini vision model). Retrieval runs BM25 plus dense bge-small, fused with RRF and reranked by a cross-encoder. In this illustrative run, a Groq gpt-oss-20b answer arrives with citation chips [video 00:14:20] and [pdf p.4], checked by an LLM audit; a 0.65 confidence gate falls back to extractive answers. Stack: Python, Groq, ChromaDB, Streamlit." /></a>
</p>

<sub>Each card loops an illustrative run of the real mechanism. Click a card for the repo.</sub>

<details>
<summary><b>LexGuard: under the hood</b></summary>
<br>

A staged agent pipeline (pre-flight context, classifier, risk analyst with an adversarial judge, deterministic audit, advocate and compliance in parallel, citation verifier, drafter) runs behind a Redis or MongoDB job queue. After the LLM passes, a deterministic detector with 36 trap patterns can force an escalation, and a reflection loop makes the model explain what it missed. The backend was squeezed into a 512 MB host with a 380 MB heap cap and post-job GC, and the AI client cascades across Gemini, Groq, Hugging Face and local Ollama when a provider runs out of quota.

On the committed May 2026 benchmark runs it got 28/30 clause types and 21/30 risk tiers right, and every miss over-flagged rather than under-flagged. Rules that matched benchmark text word for word were removed in October 2026, so a fresh run is pending. The offline unit suite runs in CI.

![Tests](https://github.com/Aditya2514/LexGuard/actions/workflows/tests.yml/badge.svg)

</details>

<details>
<summary><b>Pikina: under the hood</b></summary>
<br>

Commands that match a known pattern are handled by a Tier 1 regex router with no model call; only misses go to a local Ollama model, which must return a registered tool or `no_match`, so it can't invent actions. An Action Validation Layer checks every model-proposed action against the tool manifest, and level 4+ actions from either tier need a native confirmation dialog (MessageBoxW on Windows, zenity or kdialog on Linux). Multi-step alias chains run through a transactional executor that undoes completed steps in reverse order if one fails; a DAG scheduler with starvation protection is built and tested, waiting for the planner that will call it. Event-driven daemons and a dual-tier memory sit underneath.

</details>

<details>
<summary><b>Resilion: built vs planned</b></summary>
<br>

Built so far: data sources for GDELT, EIA, OFAC and RSS feeds, a Gemini Risk Watcher agent that turns them into structured disruption events, and a NetworkX graph of India's crude-oil supply corridors that traces which industries an event affects. Next: a Procurement Orchestrator that ranks reroutes by cost and transit delay, and an approval console so nothing executes without a person signing off.

</details>

<details>
<summary><b>Noesis: under the hood</b></summary>
<br>

Video and audio go through FFmpeg and Whisper with word-level timestamps; keyframes come from scene-change detection with perceptual-hash de-duplication; PDFs through PyMuPDF and RapidOCR. Entity canonicalisation links a term spoken in a video to the same term in a PDF diagram. Retrieval is hybrid (BM25 + bge-small embeddings) with an ms-marco reranker, and a confidence cutoff decides between a full grounded answer and an extractive fallback.

</details>

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

<img src="assets/stack.svg" alt="Technology by project matrix, derived from each repository's manifests and imports, counting only files the author committed. Python: Pikina, Resilion, Noesis, OpenEnv planner; JavaScript: LexGuard, Pikina, Resilion, ShopKart; TypeScript: BookFinder; C++: C++ shell; Gemini: LexGuard, Resilion, Noesis; Groq: LexGuard, Noesis; Ollama: LexGuard, Pikina; Hugging Face: LexGuard, OpenEnv planner; sentence-transformers: LexGuard, Pikina, Noesis; ChromaDB: Noesis; Whisper: Noesis; Node.js · Express: LexGuard, ShopKart; FastAPI: OpenEnv planner; Flask: Pikina; Pydantic: Resilion, Noesis, OpenEnv planner; MongoDB: LexGuard, ShopKart; Redis: LexGuard; NetworkX: Pikina, Resilion, Noesis; Firebase: BookFinder; React: LexGuard, Resilion, ShopKart; React Native: BookFinder; Electron: Pikina; Streamlit: Noesis; Docker: LexGuard, OpenEnv planner; GitHub Actions: LexGuard; Vercel: LexGuard, ShopKart; Hugging Face Spaces: LexGuard, OpenEnv planner." width="100%" />

<br>

## 07 Education & Honors

<img src="assets/journey.svg" alt="A timeline from August 2025 to October 2026. A line draws itself left to right and each milestone lights up as it is reached. Start: May 2025, BS in Data Science and Applications at IIT Madras, co-enrolled at Scaler School of Technology. August 2025: GitHub account created. October 2025: first public repo (portfolio). March 2026: Naukri and Fintrac. April 2026: Meta PyTorch OpenEnv Hackathon, a planner RL environment built by a team of 2. May 2026: BookFinder (React Native and TypeScript); LexGuard starts and runs to August 2026. June 2026: a POSIX shell in C++. July 2026: Pikina, then Resilion. August 2026: Noesis (team of 2). September to October 2026: ShopKart (team of 2). Also: runner-up at the Paradox DSA Triathlon, IIT Madras, 2026; CGPA 9.0 out of 10." width="100%" />

<br>

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

<img src="assets/contact.svg" alt="A terminal types: connect --with aditya. It prints linkedin.com/in/aditya-singh-8286b137a, adityasinghv05@gmail.com and github.com/Aditya2514, then: Open to AI engineering internships with teams building agents." width="100%" />

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/aditya-singh-8286b137a/)
[![Email](https://img.shields.io/badge/Email-161B22?style=for-the-badge&logo=gmail&logoColor=EA4335)](mailto:adityasinghv05@gmail.com)
[![GitHub](https://img.shields.io/badge/GitHub-161B22?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Aditya2514)

</div>
