# Applied Cognitive Psychology and Ergonomic UX Laws

This reference establishes the theoretical foundations, mathematical formulations, and practical implementation patterns for seven fundamental cognitive psychology laws across graphical user interfaces (GUI), command-line interfaces (CLI/DevEx), and autonomous multi-agent AI systems (HITL).

---

## 1. Fitts's Law (Target Acquisition & Motor Economy)

### 1.1. Theoretical Foundation & Mathematics
Formulated by Paul M. Fitts (1954) and modernized by I. Scott MacKenzie (1992) via Claude Shannon's Information Theory (ISO 9241-9 / ISO 9241-411):

$$\text{Index of Difficulty (ID)} = \log_2\left(\frac{D}{W} + 1\right)$$
$$\text{Movement Time (MT)} = a + b \cdot \text{ID} = a + b \cdot \log_2\left(\frac{D}{W} + 1\right)$$

Where:
- $D$ is the distance (amplitude) from the starting point to the center of the target.
- $W$ is the target width/tolerance measured along the axis of motion.
- $a$ is start/stop motor reaction time; $1/b$ is human motor channel bandwidth (throughput in bits/s).

**Corner & Edge Advantage (Infinity Edges):**
When a target is anchored against a physical display edge or corner, the effective target width $W \to \infty$. Consequently, $\lim_{W \to \infty} \log_2(D/W + 1) = 0$, reducing acquisition time to near-instantaneous ballistic movement.

### 1.2. Graphical UI & Accessibility (WCAG 2.2)
- **Minimum Target Dimensions:** Ensure touch and click targets satisfy WCAG 2.2 SC 2.5.8 (minimum $24 \times 24$ CSS px) and prefer AAA / Mobile platform baselines ($44 \times 44$ pt in Apple HIG, $48 \times 48$ dp in Material 3).
- **Proximity of Primary Actions:** Place primary confirmation and submission controls in direct visual and physical proximity to input focus, avoiding diagonal screen sweeps.
- **Accot-Zhai Steering Law:** For hierarchical dropdowns and flyout menus, widen the hover tunnel or implement directional delay polygons to prevent accidental closures when crossing narrow boundaries.

### 1.3. CLI & Terminal Ergonomics (DevEx)
- **Keystroke-Level Model (KLM-GOMS):** Distance $D$ in a terminal corresponds to physical hand and finger travel from the keyboard home row (`ASDF JKL;`). Frequent actions must leverage zero-travel modifier keys (`Tab`, `Enter`, `Ctrl+C`).
- **Tab Completion as Infinite Width:** Shell autocomplete expands semantic target width $W$ to infinity, turning a fragile string entry into a single deterministic keystroke.
- **Immediate Inline Actions:** Suggested or corrective commands must be printed on the **very last line** directly above the shell prompt, minimizing visual and motor distance to execution.

### 1.4. Agentic Systems & Multi-Agent UX
- **HITL Checkpoints:** Place approval controls (`[Approve]`, `[Reject]`, `[Revise]`) adjacent to the agent's proposed plan or tool call payload, bound to single-key accelerators (`y`, `n`, `Enter`, `Esc`).
- **Contextual Actions:** Surface high-frequency next prompts as quick-action pills directly adjacent to the input prompt area.

### 1.5. Common Pitfalls
- **Vector-Only Click Areas:** Binding click handlers solely to a 14px SVG glyph without generous padding.
- **Destructive Proximity:** Placing irreversible destructive actions (`Drop Database`) immediately adjacent to affirmative primaries (`Save Changes`) with identical geometry.

---

## 2. Hick's Law / Hick-Hyman (Decision Time & Choice Architecture)

### 2.1. Theoretical Foundation & Mathematics
Formulated by William Edmund Hick (1952) and Ray Hyman (1953):

$$RT = a + b \cdot \log_2(n + 1)$$

When options possess non-uniform probabilities, decision time scales with Shannon Entropy ($H$):

$$RT = a + b \cdot H, \quad H = \sum_{i=1}^n p_i \log_2\left(\frac{1}{p_i}\right)$$

Where:
- $RT$ is cognitive reaction time.
- $n$ is the number of equiprobable alternatives; $+1$ represents the uncertainty of whether to respond.
- $b$ is cognitive processing rate ($\approx 150\text{--}200$ ms/bit).

Decision time grows logarithmically when items can be mentally subdivided into categories, but degenerates into linear search ($O(n)$) when unstructured.

### 2.2. Graphical UI & Accessibility
- **Progressive Disclosure:** Expose only primary workflows initially; reveal advanced configurations on-demand (e.g., expandable `<details>` accordions, segmented wizards).
- **Sensible Defaults:** Pre-select the safest, most common option ($p_i \gg p_j$), reducing entropy $H \to 0$ for standard user paths.
- **Mitigating Choice Overload:** Avoid flat option dumps; cap primary navigation menus to structured groups.

### 2.3. CLI & Terminal Ergonomics (DevEx)
- **Subcommand Trees:** Use hierarchical grammar (`tool <noun> <verb>`) rather than a flat namespace with 80 unorganized flags.
- **Capped Default Output:** By default, CLIs should display the top $3\text{--}5$ most relevant candidates, providing flags (`--top N`, `--all`) for full long-tail discovery.
- **Interactive Prompts vs. Flag Bloat:** Replace combinatorial flag puzzles with guided interactive selection prompts for multi-parameter scaffolding.

### 2.4. Agentic Systems & Multi-Agent UX
- **On-Demand Tool Provisioning:** Injecting 50+ tool schemas into an LLM context causes choice degradation and argument hallucination. Route and inject only the $3\text{--}7$ tools relevant to the current agent phase.
- **Bounded HITL Decisions:** When an agent prompts a human operator, frame choices as mutually exclusive, numbered options ($2\text{--}4$ choices maximum) rather than open-ended queries.

### 2.5. Common Pitfalls
- **Flag Sprawl:** CLI `--help` outputs that dump 150 alphabetical flags without categorization.
- **Deep Nesting (Over-Pruning):** Hiding everyday options under 5 successive menu layers, where navigational travel exceeds cognitive savings.

---

## 3. Zeigarnik & Ovsiankina Effects (Open Loops & Task Closure)

### 3.1. Theoretical Foundation
Identified by Bluma Zeigarnik (1927) under Kurt Lewin's Field Theory, and expanded by Maria Ovsiankina (1928):
- **Zeigarnik Effect:** Uncompleted or interrupted tasks create a persistent quasi-need (*psychic tension*), resulting in approximately 90% higher recall than completed tasks.
- **Ovsiankina Effect:** Interrupted tasks produce an intrinsic behavioral urge to resume and finish the action once constraints are lifted.
- **Closure:** Reaching a clear completion boundary releases cognitive tension and allows memory buffers to clear.

### 3.2. Graphical UI & Accessibility
- **Onboarding Checklists:** Display partially completed progress checklists (e.g., "3 of 5 steps completed") to trigger completion motivation.
- **Stateful Forms:** Auto-save drafts and visibly highlight incomplete required fields, preserving entered data across navigation.

### 3.3. CLI & Terminal Ergonomics (DevEx)
- **Actionable Interruption States:** When a process pauses or fails due to a conflict (e.g., `git merge` conflicts), state explicitly:
  1. What is currently incomplete.
  2. How to resume and conclude (`git commit` or `tool continue`).
  3. How to abort and safely release the loop (`git merge --abort` or `tool abort`).
- **Git Status Feedback Loop:** The visual contrast of unstaged/uncommitted files in `git status` creates an open loop that drives the developer to stage, stash, or commit before context switching.

### 3.4. Agentic Systems & Multi-Agent UX
- **Structured Task Ledgers & Handoffs:** In multi-turn and multi-agent workflows, maintain an explicit ledger of open loops (`QUEUED`, `IN_PROGRESS`, `BLOCKED`). Handoff payloads (such as TOON) preserve pending tasks so resumption requires zero reconstructive overhead.
- **Clear Milestone Boundaries:** Every phase completion must yield explicit closure before opening subsequent tasks, preventing cognitive drift.

### 3.5. Common Pitfalls
- **Silent Mid-Process Failures:** Scripts that abort halfway through state mutations without recording what was done or providing a rollback pathway.
- **Notification Spam:** Abusing artificial open loops with persistent warning badges for trivial or un-actionable items.

---

## 4. Jakob's Law (Mental Models & Convention Transfer)

### 4.1. Theoretical Foundation
Formulated by Jakob Nielsen (2000):
> *"Users spend most of their time on other websites. This means that users prefer your site to work the same way as all the other sites they already know."*

Grounded in Schema Theory (Bartlett; Piaget) and Mental Models (Norman). Users transfer operational assumptions across tools. Violating established conventions forces conscious cognitive processing over interaction mechanics, widening the Gulf of Execution.

### 4.2. Graphical UI & Accessibility
- **Standard Navigation & Layouts:** Place global navigation, search bars (`Cmd+K` / `/`), and profile utilities in conventional locations.
- **Standard Keyboard Shortcuts:** Retain ubiquitous accelerators (`Ctrl/Cmd+C`, `Ctrl/Cmd+Z`, `Ctrl/Cmd+F`). Innovate on core value, not on control idioms.

### 4.3. CLI & Terminal Ergonomics (DevEx)
- **POSIX & GNU Conventions:**
  - Single-dash short flags (`-v`, `-f`, combinable as `-vf`).
  - Double-dash long options (`--verbose`, `--force`, `--help`, `--version`).
  - Mandatory help (`-h`, `--help`) and version (`-v`, `--version`) flags.
- **Unix Stream Hygiene:**
  - Pure data and structured outputs belong on `stdout` (fd 1) for pipeline composability (`tool | jq .`).
  - Diagnostics, progress, logs, and interactive questions belong on `stderr` (fd 2).
  - Clean exit codes: `0` for success, non-zero (`1..255`) for errors.
- **NO_COLOR Standard:** Adhere to `no-color.org`: suppress all ANSI escape sequences when the `NO_COLOR` environment variable is set or `TERM=dumb`.

### 4.4. Agentic Systems & Multi-Agent UX
- **Canonical Output Formats:** Emit diffs as unified diffs (`diff -u`), code inside language-tagged Markdown fences, and structured data in standard JSON/YAML schemas.
- **Standard Chat Conventions:** User inputs anchored at bottom, conversational stream with distinguishable message roles.

### 4.5. Common Pitfalls
- **Not-Invented-Here (NIH) CLI Syntax:** Inventing idiosyncratic flag styles (e.g., DOS-style `/flag` on Linux or non-standard exit codes).
- **Stream Pollution:** Printing status messages or ASCII banners to `stdout`, corrupting downstream pipeline consumers.

---

## 5. Goal-Gradient & Endowed Progress Effects (Motivational Velocity)

### 5.1. Theoretical Foundation & Mathematics
Formulated by Clark L. Hull (1932/1934) and expanded by Ran Kivetz et al. (2006) and Joseph Nunes & Xavier Drèze (2006):

$$R = \frac{k}{d^p}$$

Where:
- $R$ is response rate / motivational effort.
- $d$ is perceived distance remaining to the goal.
- $k$ is reward attractiveness and $p$ is the gradient acceleration exponent.

**Endowed Progress Effect (Nunes & Drèze):**
Effort accelerates based on **relative perceived progress** rather than absolute remaining steps. Framing a process as already underway (e.g., 2 free stamps on a 10-stamp card vs. 0 on an 8-stamp card) significantly increases completion rates and reduces time-to-finish.

### 5.2. Graphical UI & Accessibility
- **Step Indicators:** Multi-stage flows must show explicit step progression ("Step 2 of 4 — 50% Complete").
- **Determinate Progress Bars:** For operations exceeding 2 seconds, use determinate progress bars with elapsed/estimated time rather than indefinite spinners.

### 5.3. CLI & Terminal Ergonomics (DevEx)
- **Determinate Progress in Workflows:** Output measurable progress (`[3/10] Compiling modules... (30%)`) for batch operations.
- **Endowed Progress in Setup Commands:** In init or scaffolding wizards, credit the developer with immediate initial achievements:
  ```text
  [✓] Environment verified: Python 3.12, Linux x86_64 (Step 1 of 4)
  [ ] Select template...
  ```
  This immediately breaks inertia and accelerates task completion.

### 5.4. Agentic Systems & Multi-Agent UX
- **Phased Execution Telemetry:** Agents executing complex plans should report phase and task milestones deterministically:
  `[Step 2/5 — 40% complete | Next: Database Migration]`.
- **Live Tool Progress:** Stream intermediate status updates during long tool executions, preserving the operator's sense of forward momentum.

### 5.5. Common Pitfalls
- **The 99% Freeze:** Progress indicators that advance quickly to 99% and stall for 45 seconds while backend jobs finish, destroying user trust.
- **Moving Finish Lines:** Interfaces that announce "Step 3 of 3" and then reveal unexpected subsequent steps, deflating motivation.

---

## 6. Von Restorff Effect (Isolation & Perceptual Salience)

### 6.1. Theoretical Foundation
Discovered by Hedwig von Restorff (1933) and formalized in cognitive vision via Feature Integration Theory (Treisman & Gelade, 1980):
- When multiple homogeneous stimuli are presented, the stimulus that differs significantly in color, shape, weight, or size is granted pre-attentive perceptual pop-out (<200 ms) and significantly higher recall.
- **The Paradox of Over-Emphasis (Alert Fatigue):** When multiple items clamor for attention simultaneously ("when everything screams, nothing is heard"), perceptual contrast collapses into sensory noise.

### 6.2. Graphical UI & Accessibility
- **Visual Callout Hierarchy:** Standardize semantic admonitions (`NOTE`, `TIP`, `WARNING`, `CAUTION`) with consistent iconography and contrast.
- **Primary CTA Isolation:** In option matrices or pricing tables, visually isolate exactly one recommended choice; leave secondary actions subdued.
- **Colorblind-Safe Contrast:** Never rely on color alone to isolate an item; combine color with typographic weight, borders, or iconography.

### 6.3. CLI & Terminal Ergonomics (DevEx)
- **Selective ANSI Highlighting:** In terminal logs and candidate tables, isolate only the primary match (#1 recommendation) with bold accentuation. Keep secondary candidates neutral (`DIM` / plain text).
- **Theme-Neutral Styling:** Use terminal attributes (`\033[1m` bold, `\033[2m` dim) rather than hard-coded dark or bright colors that vanish on light-theme or dark-theme terminals.
- **Diff Salience:** Use distinct line markers (`+`, `-`) in addition to green/red coloring for accessibility across diverse color profiles.

### 6.4. Agentic Systems & Multi-Agent UX
- **Critical HITL Approval Gating:** When an agent transitions from read-only inspection to an action with side effects (file mutation, network push, command execution), isolate the approval card with distinct border styling, separating it from regular text output.

### 6.5. Common Pitfalls
- **Terminal Rainbows:** Outputting random combinations of magenta, cyan, yellow, and red on every line, obliterating perceptual focus.
- **Warning Inflation:** Emitting hundreds of non-actionable linter warnings, conditioning developers to ignore critical diagnostics.

---

## 7. Miller's Law & Cowan's Working Memory Limit ($7 \pm 2$ vs. $4 \pm 1$)

### 7.1. Theoretical Foundation & Working Memory
- **Miller's Law (1956):** George A. Miller established that human immediate memory span spans approximately $7 \pm 2$ discrete items. Crucially, capacity is measured not in raw bits, but in **Chunks** — meaningful cognitive units bound to prior knowledge.
- **Cowan's Limit (2001):** Nelson Cowan demonstrated that when subvocal rehearsal and automatic grouping are controlled, pure human working memory capacity is strictly **$4 \pm 1$ active chunks**.
- **Recognition vs. Recall:** The $4 \pm 1$ limit applies to information held in active memory without perceptual support. External visual aids reduce working memory load by enabling recognition over recall.

### 7.2. Graphical UI & Accessibility
- **Information Chunking:** Decompose complex dashboards, forms, and tables into discrete, scannable clusters separated by whitespace.
- **Diátaxis Documentation Architecture:** Structure technical documentation into 4 distinct quadrants matching cognitive intent: *Tutorials*, *How-To Guides*, *Reference*, and *Explanation*.

### 7.3. CLI & Terminal Ergonomics (DevEx)
- **Categorized Help Output:** Never dump long lists of commands alphabetically. Group commands into $3\text{--}5$ functional chunks (e.g., Git's work-tree, commit, history, and collaboration groupings).
- **Bounded Candidate Display:** Default routing and search proposals to top $3\text{--}5$ ranked candidates ($4 \pm 1$).

### 7.4. Agentic Systems & Multi-Agent UX
- **Prompt Architecture & Attention Degradation:** Large context windows suffer from *Lost in the Middle* attention degradation. Structure system prompts into discrete semantic chunks using XML delimiters (`<rules>`, `<tools>`, `<guidelines>`).
- **Atomic Review Chunks:** Never present a 50-file diff in a single review turn. Chunk reviews into atomic units of $3\text{--}5$ files per review checkpoint to ensure rigorous evaluation.

### 7.5. Common Pitfalls
- **The "Seven Menu Items" Fallacy:** Dogmatically restricting visible menus to 7 items when visual recognition renders working memory constraints inapplicable.
- **Unstructured Stack Traces:** Dumping 200 lines of unparsed execution traces without summarizing root causes into digestible diagnostic chunks.
