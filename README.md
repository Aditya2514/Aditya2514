<picture>
  <source media="(prefers-reduced-motion: reduce) and (max-width: 600px)" srcset="assets/mission/hero-mobile-still.svg" />
  <source media="(prefers-reduced-motion: reduce)" srcset="assets/mission/hero-still.svg" />
  <source media="(max-width: 600px)" srcset="assets/mission/hero-mobile.svg" />
  <img src="assets/mission/hero.svg" width="100%" alt="Aditya Singh — AI systems, agents and full-stack. IIT Madras and Scaler School of Technology. A BGMI-inspired operator at a holographic workstation." />
</picture>

<p align="center">
<b><a href="#select-a-mission">Explore projects</a> &nbsp; / &nbsp; <a href="#engineering-brief">Engineering brief</a> &nbsp; / &nbsp; <a href="#squad-up">Squad up</a></b>
</p>

I'm **Aditya Singh**. I build LLM systems, local desktop agents and full-stack products—with a particular interest in **what happens when a model gets something wrong**.

**The model proposes. The system checks. The person stays in control.**


<picture>
  <source media="(max-width: 600px)" srcset="assets/mission/chapter-01-mobile.svg" />
  <img src="assets/mission/chapter-01.svg" width="100%" alt="Chapter 01 of the Aditya Singh engineering dossier" />
</picture>

## The operator

I study **Data Science & Applications at IIT Madras**, co-enrolled at **Scaler School of Technology**. My projects span contract intelligence, local desktop agents, multimodal retrieval and full-stack applications.

What interests me most is the gap between a model producing an answer and a system doing something dependable with it. I work with retrieval, explicit checks and human approval to make that gap easier to inspect.

**Read the situation. Coordinate the squad. Review the mistakes. Queue again.** That is the BGMI energy behind this profile—and the mindset I bring to a build.

<img src="assets/arena/terminal.svg" width="100%" alt="An animated terminal introduction with a dated snapshot of recent GitHub commits." />


<picture>
  <source media="(max-width: 600px)" srcset="assets/mission/chapter-02-mobile.svg" />
  <img src="assets/mission/chapter-02.svg" width="100%" alt="Chapter 02 of the Aditya Singh engineering dossier" />
</picture>

## Select a mission

Three systems. Three different ways to make AI easier to inspect. Click a card to explore its code.

<a href="https://github.com/Aditya2514/LexGuard">
<picture>
  <source media="(max-width: 600px)" srcset="assets/mission/lexguard-mobile.svg" />
  <img src="assets/mission/lexguard.svg" width="100%" alt="LexGuard — Reviews contracts under Indian law using statutory retrieval and deterministic risk checks." />
</picture>
</a>

**The mission:** make contract risks easier to inspect before signing. LexGuard reviews contracts under Indian law using statutory retrieval and deterministic risk checks.

**Under the hood:** a staged agent pipeline examines clauses, checks explicit traps, verifies citations and proposes rewrites. Deterministic checks can escalate the model’s risk assessment. Its repository documents benchmark context and limitations.

<sub>Node.js · React · MongoDB · Redis</sub> &nbsp; **[Inspect LexGuard →](https://github.com/Aditya2514/LexGuard)**

<a href="https://github.com/Aditya2514/Pikina">
<picture>
  <source media="(max-width: 600px)" srcset="assets/mission/pikina-mobile.svg" />
  <img src="assets/mission/pikina.svg" width="100%" alt="Pikina — An offline-first Windows/Linux assistant with local inference, validated tools and consent for high-risk actions." />
</picture>
</a>

**The mission:** let a local assistant help with your computer while keeping meaningful actions inspectable. Pikina is an offline-first Windows/Linux assistant with local inference, validated tools and consent for high-risk actions.

**Under the hood:** regex-first routing handles known intents, Ollama supports local inference, and an action validator checks proposed tools. Alias chains support rollback. The project is pre-alpha; the scheduler still awaits its planner.

<sub>Python · Electron · Ollama · SQLite · Pre-alpha</sub> &nbsp; **[Inspect Pikina →](https://github.com/Aditya2514/Pikina)**

<a href="https://github.com/Aditya2514/Noesis">
<picture>
  <source media="(max-width: 600px)" srcset="assets/mission/noesis-mobile.svg" />
  <img src="assets/mission/noesis.svg" width="100%" alt="Noesis — Searches video, audio, PDFs and images with hybrid retrieval, reranking and citations to timestamps or pages. Built with Apurva Patil." />
</picture>
</a>

**The mission:** find the useful moment across a collection of mixed media. Noesis searches video, audio, PDFs and images, then links answers to timestamps or pages.

**Under the hood:** BM25 and dense retrieval feed a reranker; source citations and an LLM audit help inspect the response. Built with **Apurva Patil**.

<sub>Python · ChromaDB · Whisper · Streamlit · Team project</sub> &nbsp; **[Inspect Noesis →](https://github.com/Aditya2514/Noesis)**

<sub>The animated sequences illustrate mechanisms; they are not live production runs.</sub>

## Engineering brief

<picture>
  <source media="(max-width: 600px)" srcset="assets/mission/decision-mobile.svg" />
  <img src="assets/mission/decision.svg" width="100%" alt="A rotating engineering decision from LexGuard, Pikina or Noesis. Read the implementation notes below." />
</picture>

**The decisions beneath the visuals**

| System | Design decision | What to inspect |
| :-- | :-- | :-- |
| [LexGuard](https://github.com/Aditya2514/LexGuard) | Deterministic trap checks can escalate an LLM's risk assessment; retrieval grounds statutory citations. | Its README explains benchmarks and limitations. |
| [Pikina](https://github.com/Aditya2514/Pikina) | Validate model proposals against registered capabilities; request consent for high-risk actions. | Alias chains support rollback. The scheduler still awaits its planner. |
| [Noesis](https://github.com/Aditya2514/Noesis) | Combine BM25 and dense retrieval, rerank results, and make sources inspectable. | Source citations and an LLM audit help inspect answers. Built with Apurva Patil. |
| [Resilion](https://github.com/Aditya2514/Resilion) | Turn news into structured risk events and trace affected industries through a supply graph. | Graph and Risk Watcher built; rerouting, API and approval console are planned. |

**Mission replay — an illustrative LexGuard walkthrough**

<img src="assets/arena/lexguard_flow.svg" width="100%" alt="Illustrative LexGuard sequence: classify clauses, assess risks, check traps and citations, propose rewrites." />


<picture>
  <source media="(max-width: 600px)" srcset="assets/mission/chapter-03-mobile.svg" />
  <img src="assets/mission/chapter-03.svg" width="100%" alt="Chapter 03 of the Aditya Singh engineering dossier" />
</picture>

## Project lobby

**Also building [Resilion](https://github.com/Aditya2514/Resilion):** supply-chain intelligence with a Risk Watcher and impact graph. Python · NetworkX · Gemini. In progress.

<!-- PROJECT-LOBBY:START -->

<p align="center">
<a href="https://github.com/Aditya2514/HostelDesk"><img src="assets/catalog/hosteldesk.svg" width="49%" alt="HostelDesk — Hostel complaints with explained ETA ranges, automatic routing, completion proof and escalation. Stack: TypeScript, React, Express, PostgreSQL, Prisma" /></a>
<a href="https://github.com/Aditya2514/Meta_OpenEnv"><img src="assets/catalog/meta_openenv.svg" width="49%" alt="Meta OpenEnv — An environment for agents juggling assignments, bugs, deadlines and burnout constraints. Team hackathon project. Stack: Python, FastAPI, Docker" /></a>
</p>

<p align="center">
<a href="https://github.com/Aditya2514/Shopkart"><img src="assets/catalog/shopkart.svg" width="49%" alt="ShopKart — Server-authoritative checkout and Razorpay test-mode payments. Built with Apurva Patil. Stack: React, Express, MongoDB" /></a>
<a href="https://github.com/Aditya2514/codecrafters-shell-cpp"><img src="assets/catalog/codecrafters-shell-cpp.svg" width="49%" alt="C++ Shell — A shell built around fork, exec, pipe and dup2: quoting, redirection, pipelines and background jobs. Stack: C++23, POSIX, CMake" /></a>
</p>

<p align="center">
<a href="https://github.com/Aditya2514/Vidya"><img src="assets/catalog/vidya.svg" width="49%" alt="Vidya / BookFinder — Book discovery, debounced search, Google sign-in and persistent saved lists. Stack: React Native, TypeScript, Firebase" /></a>
<a href="https://github.com/Aditya2514/Fintrac"><img src="assets/catalog/fintrac.svg" width="49%" alt="Fintrac — A personal budgeting dashboard with Gemini-powered spending analysis. Stack: React, Vite, Recharts, Gemini" /></a>
</p>

<p align="center">
<a href="https://github.com/Aditya2514/Naukri"><img src="assets/catalog/naukri.svg" width="49%" alt="Naukri / Jobee — A job-portal UI with search, saved jobs and a simulated listings API. Stack: React, Vite" /></a>
<a href="https://github.com/Aditya2514/BenchShield"><img src="assets/catalog/benchshield.svg" width="49%" alt="BenchShield — Explore the source, documentation and latest changes. Stack: Python" /></a>
</p>

<p align="center">
<a href="https://github.com/Aditya2514/Mobius"><img src="assets/catalog/mobius.svg" width="49%" alt="Mobius — Explore the source, documentation and latest changes. Stack: TypeScript" /></a>
<a href="https://github.com/Aditya2514?tab=repositories"><img src="assets/catalog/browse.svg" width="49%" alt="Explore all repositories" /></a>
</p>

<!-- PROJECT-LOBBY:END -->

[Earlier experiments](https://github.com/Aditya2514?tab=repositories): FinancePro · Simple Soundboard · First portfolio.


<picture>
  <source media="(max-width: 600px)" srcset="assets/mission/chapter-04-mobile.svg" />
  <img src="assets/mission/chapter-04.svg" width="100%" alt="Chapter 04 of the Aditya Singh engineering dossier" />
</picture>

## Build kit

<picture>
  <source media="(max-width: 600px)" srcset="assets/mission/arsenal-mobile.svg" />
  <img src="assets/mission/arsenal.svg" width="100%" alt="Build kit: languages, AI and retrieval, backend, data, interfaces and delivery tools." />
</picture>


## Utility belt

**Game wali utility. Builder wala purpose.** Four animated links into the work.

<p align="center">
<a href="https://github.com/Aditya2514/Noesis"><img src="assets/actions/smoke.svg" width="49%" alt="Smoke daal. Noise hata. Explore Noesis and its evidence retrieval." /></a>
<a href="https://github.com/Aditya2514/LexGuard"><img src="assets/actions/frag.svg" width="49%" alt="Frag out. Bug out. Explore LexGuard and its checks." /></a>
</p>
<p align="center">
<a href="https://github.com/Aditya2514/codecrafters-shell-cpp"><img src="assets/actions/molotov.svg" width="49%" alt="Debt jalao. Clean build. Explore the C++ shell." /></a>
<a href="https://github.com/Aditya2514/HostelDesk"><img src="assets/actions/boost.svg" width="49%" alt="Boost on. Build on. Explore HostelDesk." /></a>
</p>


<picture>
  <source media="(max-width: 600px)" srcset="assets/mission/chapter-05-mobile.svg" />
  <img src="assets/mission/chapter-05.svg" width="100%" alt="Chapter 05 of the Aditya Singh engineering dossier" />
</picture>

## Match history

## Build transmissions

<!-- MISSION-FEED:START -->

| Repository | Recent change | Date (UTC) |
| :-- | :-- | :-- |
| Pikina | [fix(switcher): review findings — Ctrl+C, git config execution, robustness](https://github.com/Aditya2514/Pikina/commit/21e6e432e8653851d9680c458f8814e7e942b6e9) | 2026-10-22 |
| Pikina | [feat: project switcher (&quot;work on &lt;project&gt;&quot;) as the built-in workspace plugin](https://github.com/Aditya2514/Pikina/commit/a1b73fa721aaa649689d0b1412fa3d13e56c6f09) | 2026-10-22 |
| Pikina | [phase1: close the gaps found when re-verifying the review fixes](https://github.com/Aditya2514/Pikina/commit/11b49a84714332dfcaa3a8681c22d143dbd24271) | 2026-10-22 |

<sub>Recent non-merge changes from LexGuard, Pikina and Noesis. Refreshed 08 Nov 2026, 22:04 UTC. Scheduled every six hours; the last successful snapshot stays visible if refresh fails.</sub>

<!-- MISSION-FEED:END -->


<img src="assets/arena/signal.svg" width="100%" alt="GitHub contributions and language distribution, with the last generation date on the card." />
<img src="assets/arena/rhythm.svg" width="100%" alt="Commit activity by hour in IST and by weekday." />
<img src="assets/catalog/ranked-grind.svg" width="100%" alt="Active contribution weeks represented as a tactical map. The scope animation is decorative." />

<sub>Generated from GitHub data. Scheduled every six hours; each card keeps its last successful update.</sub>


<picture>
  <source media="(max-width: 600px)" srcset="assets/mission/chapter-06-mobile.svg" />
  <img src="assets/mission/chapter-06.svg" width="100%" alt="Chapter 06 of the Aditya Singh engineering dossier" />
</picture>

## Career campaign

<img src="assets/arena/journey.svg" width="100%" alt="Animated education and project milestone timeline." />

| Education | Achievement |
| :-- | :-- |
| **IIT Madras** · BS Data Science & Applications · 2025–2029 · CGPA **9.0/10** | **Runner-up** · Paradox DSA Triathlon · IIT Madras · 2026 |
| **Scaler School of Technology** · 2025–2029 | **Meta PyTorch OpenEnv Hackathon** · 2026 · Team submission |

**The BGMI connection:** read the situation, communicate with the squad, learn from the replay, queue again. That same competitive curiosity shapes how I build.


<picture>
  <source media="(max-width: 600px)" srcset="assets/mission/outro-mobile.svg" />
  <img src="assets/mission/outro.svg" width="100%" alt="Squad up. Build something worth finding. AI engineering, agents and hackathons." />
</picture>

## Squad up

Interested in **AI engineering internships**, **agent systems**, or a **hackathon project**? Send me the problem you're working on.

**[LinkedIn ↗](https://www.linkedin.com/in/aditya-singh-8286b137a/)** &nbsp; / &nbsp; **[Email ↗](mailto:adityasinghv05@gmail.com)** &nbsp; / &nbsp; **[All repositories ↗](https://github.com/Aditya2514?tab=repositories)**

---

<p align="center"><b>GG. Now go inspect the code.</b><br/><sub>BGMI-inspired spirit. Engineering you can inspect.</sub></p>
