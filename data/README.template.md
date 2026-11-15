<picture>
  <source media="(max-width: 600px)" srcset="assets/blueprint/hero-mobile.svg" />
  <img src="assets/blueprint/hero.svg" width="100%" alt="Blueprint sheet 00: Aditya Singh, AI systems, agents and full-stack, IIT Madras and Scaler School of Technology. A diagram loops between three parts: the model proposes, the system checks, the person decides." />
</picture>

<p align="center"><b><a href="#featured-systems">Featured systems</a> &nbsp;·&nbsp; <a href="#engineering-decisions">Engineering decisions</a> &nbsp;·&nbsp; <a href="#more-builds">More builds</a> &nbsp;·&nbsp; <a href="#build-kit">Build kit</a> &nbsp;·&nbsp; <a href="#get-in-touch">Get in touch</a></b></p>

## About

I'm **Aditya Singh**. I study **Data Science & Applications at IIT Madras**, co-enrolled at **Scaler School of Technology**, and I build LLM systems, local desktop agents and full-stack products. My projects span contract intelligence, local desktop agents, multimodal retrieval and full-stack applications.

What interests me most is the gap between a model producing an answer and a system doing something dependable with it. I work with retrieval, explicit checks and human approval to make that gap easier to inspect.

**The model proposes. The system checks. The person stays in control.** Every drawing below uses the same three symbols:

<p align="center"><code>◇ model proposes</code> &nbsp; <code>■ system checks</code> &nbsp; <code>● person decides</code></p>

**Read the situation. Coordinate the squad. Review the mistakes. Queue again.** That's the BGMI mindset I bring to a build.

## Featured systems

Three systems, drawn from their actual code paths. Links under each drawing go to the exact lines.

<a href="https://github.com/Aditya2514/LexGuard">
<picture>
  <source media="(max-width: 600px)" srcset="assets/blueprint/lexguard-mobile.svg" />
  <img src="assets/blueprint/lexguard.svg" width="100%" alt="Blueprint of LexGuard: a contract is parsed and repaired, clauses are classified and indexed, a risk analyst rates them with an adversarial pass, a rule gate of trap patterns can escalate the rating, then a plain-language guide, an Indian law compliance check and a cross-reference audit run in parallel, citations are checked against a statute database, a drafter proposes rewrites, and the person decides from the score and dashboard." />
</picture>
</a>

**LexGuard.** Makes contract risks easier to inspect before signing. It reviews contracts under Indian law using statutory retrieval and deterministic risk checks: a staged agent pipeline examines clauses, checks explicit traps, verifies citations and proposes rewrites, and the deterministic checks can escalate the model's risk assessment.

<sub>Node.js · React · MongoDB · Redis</sub> &nbsp; **In the code:** {{code:LexGuard}}

<a href="https://github.com/Aditya2514/Pikina">
<picture>
  <source media="(max-width: 600px)" srcset="assets/blueprint/pikina-mobile.svg" />
  <img src="assets/blueprint/pikina.svg" width="100%" alt="Blueprint of Pikina: your command goes to a Tier 1 regex router; on a hit it goes straight to the validator, on a miss to a local Ollama model first. The validator checks the proposal against the capability registry, a consent gate sends high-risk actions to you for approval and lets low-risk ones run, the action executes through the OS bridge, and plans can roll back." />
</picture>
</a>

**Pikina.** Lets a local assistant help with your computer while keeping meaningful actions inspectable. It's an offline-first Windows/Linux assistant with local inference, validated tools and consent for high-risk actions: regex-first routing handles known intents, Ollama handles the rest, an action validator checks every proposed tool call, and plans support rollback.

<sub>Python · Electron · Ollama · SQLite</sub> &nbsp; **In the code:** {{code:Pikina}}

<a href="https://github.com/Aditya2514/Noesis">
<picture>
  <source media="(max-width: 600px)" srcset="assets/blueprint/noesis-mobile.svg" />
  <img src="assets/blueprint/noesis.svg" width="100%" alt="Blueprint of Noesis: video and audio, PDFs and images become SuperChunks tagged with a time window or page, which feed a dense ChromaDB index and a sparse BM25 index; results are merged with reciprocal rank fusion, reranked by a local cross-encoder, used for a grounded answer, checked by a per-claim fact audit, and shown to you cited to a time or page." />
</picture>
</a>

**Noesis.** Finds the useful moment across a collection of mixed media. It searches video, audio, PDFs and images, then links each answer to a timestamp or page: BM25 and dense retrieval feed a reranker, and source citations plus an LLM fact audit make the response inspectable. Built with **Apurva Patil**.

<sub>Python · ChromaDB · Whisper · Streamlit</sub> &nbsp; **In the code:** {{code:Noesis}}

## Engineering decisions

The decisions underneath the drawings, each linked to the line that implements it.

{{decisions}}

## More builds

| Project | What it does | Stack |
| :-- | :-- | :-- |
| [Resilion](https://github.com/Aditya2514/Resilion) | Supply-chain intelligence: a Risk Watcher turns news into structured events and an impact graph traces who is affected. | Python · NetworkX · Gemini |
| [HostelDesk](https://github.com/Aditya2514/HostelDesk) | Hostel complaints with explained ETA ranges, automatic routing and escalation. | TypeScript · React · Express · PostgreSQL · Prisma |
| [Meta OpenEnv](https://github.com/Aditya2514/Meta_OpenEnv) | An environment for agents juggling assignments, bugs, deadlines and burnout constraints. Team hackathon project. | Python · FastAPI · Docker |
| [ShopKart](https://github.com/Aditya2514/Shopkart) | Server-authoritative checkout and Razorpay test-mode payments. Built with Apurva Patil. | React · Express · MongoDB |
| [C++ Shell](https://github.com/Aditya2514/codecrafters-shell-cpp) | A shell built around fork, exec, pipe and dup2: quoting, redirection, pipelines and background jobs. | C++23 · POSIX · CMake |
| [Vidya](https://github.com/Aditya2514/Vidya) | Book discovery with debounced search, Google sign-in and persistent saved lists. | React Native · TypeScript · Firebase |
| [Fintrac](https://github.com/Aditya2514/Fintrac) | A personal budgeting dashboard with Gemini-powered spending analysis. | React · Vite · Recharts · Gemini |
| [Naukri](https://github.com/Aditya2514/Naukri) | A job-portal UI with search, saved jobs and a simulated listings API. | React · Vite |

<sub>[All repositories →](https://github.com/Aditya2514?tab=repositories)</sub>

## Build kit

<picture>
  <source media="(max-width: 600px)" srcset="assets/blueprint/parts-mobile.svg" />
  <img src="assets/blueprint/parts.svg" width="100%" alt="Parts list: languages Python, JavaScript, TypeScript, C++; AI and retrieval Ollama, Gemini, Groq, Hugging Face, ChromaDB, sentence-transformers; backend Node.js, Express, FastAPI, Flask; data PostgreSQL, MongoDB, Redis, SQLite; interfaces React, React Native, Electron, Streamlit; delivery Git, GitHub Actions, Docker, Vercel." />
</picture>

## Build log

Recent changes across the featured systems and builds.

{{buildlog}}

## Record

| Education | Achievement |
| :-- | :-- |
| **IIT Madras** · BS Data Science & Applications · 2025–2029 · CGPA **9.0/10** | **Runner-up** · Paradox DSA Triathlon · IIT Madras · 2026 |
| **Scaler School of Technology** · 2025–2029 | **Meta PyTorch OpenEnv Hackathon** · 2026 · team submission |

## Get in touch

Interested in **AI engineering internships**, **agent systems**, or a **hackathon project**? Send me the problem you're working on.

**[LinkedIn ↗](https://www.linkedin.com/in/aditya-singh-8286b137a/)** &nbsp;·&nbsp; **[Email ↗](mailto:adityasinghv05@gmail.com)** &nbsp;·&nbsp; **[All repositories ↗](https://github.com/Aditya2514?tab=repositories)**

<p align="center"><sub>Drawings and code links regenerate every six hours · last run {{generated}}</sub></p>
