<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Python for GenAI Developers — The Complete Guide</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,opsz,wght@0,8..60,300;0,8..60,400;0,8..60,600;0,8..60,700;1,8..60,300;1,8..60,400&family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  :root {
    --ink:       #1a1a2e;
    --ink-light: #4a4a6a;
    --ink-muted: #8888aa;
    --bg:        #fafaf8;
    --bg-warm:   #f5f4ef;
    --bg-code:   #16162a;
    --accent:    #5b47e0;
    --accent2:   #e05b8a;
    --accent3:   #00c9a7;
    --border:    #e8e7e2;
    --tag-bg:    #ede9fe;
    --tag-fg:    #5b47e0;
  }

  html { font-size: 18px; scroll-behavior: smooth; }

  body {
    background: var(--bg);
    color: var(--ink);
    font-family: 'Source Serif 4', Georgia, serif;
    line-height: 1.8;
    -webkit-font-smoothing: antialiased;
  }

  /* ── Layout ── */
  .page-wrap  { max-width: 760px; margin: 0 auto; padding: 0 1.5rem; }
  .wide-wrap  { max-width: 960px; margin: 0 auto; padding: 0 1.5rem; }

  /* ── Header / Hero ── */
  .hero {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    padding: 5rem 2rem 4rem;
    position: relative;
    overflow: hidden;
  }
  .hero::before {
    content: '';
    position: absolute; inset: 0;
    background: radial-gradient(ellipse at 70% 50%, rgba(91,71,224,.35) 0%, transparent 65%),
                radial-gradient(ellipse at 20% 80%, rgba(0,201,167,.18) 0%, transparent 55%);
  }
  .hero-inner { max-width: 760px; margin: 0 auto; position: relative; }

  .hero-eyebrow {
    font-family: 'Inter', sans-serif;
    font-size: .72rem;
    font-weight: 600;
    letter-spacing: .18em;
    text-transform: uppercase;
    color: var(--accent3);
    margin-bottom: 1.4rem;
  }
  .hero h1 {
    font-family: 'Source Serif 4', serif;
    font-size: clamp(2rem, 5vw, 3.2rem);
    font-weight: 700;
    line-height: 1.15;
    color: #fff;
    margin-bottom: 1.2rem;
    max-width: 640px;
  }
  .hero h1 em { color: #a78bfa; font-style: normal; }
  .hero-sub {
    font-family: 'Inter', sans-serif;
    font-size: 1rem;
    font-weight: 300;
    color: #cbd5e1;
    max-width: 520px;
    line-height: 1.65;
    margin-bottom: 2rem;
  }
  .hero-meta {
    display: flex; align-items: center; gap: 1.2rem; flex-wrap: wrap;
    font-family: 'Inter', sans-serif; font-size: .8rem; color: #94a3b8;
  }
  .hero-meta .dot { opacity: .4; }
  .read-time {
    background: rgba(255,255,255,.08);
    border: 1px solid rgba(255,255,255,.12);
    border-radius: 20px; padding: .2rem .8rem;
    font-size: .72rem; color: #a78bfa;
  }

  /* ── Tags ── */
  .tags { display: flex; gap: .5rem; flex-wrap: wrap; margin: 2rem 0 .5rem; }
  .tag {
    font-family: 'Inter', sans-serif;
    font-size: .72rem; font-weight: 500;
    padding: .25rem .75rem; border-radius: 20px;
    background: var(--tag-bg); color: var(--tag-fg);
  }
  .tag.teal  { background: #d1faf3; color: #007a63; }
  .tag.pink  { background: #fce7f3; color: #9d174d; }
  .tag.amber { background: #fef3c7; color: #92400e; }

  /* ── Article body ── */
  article { padding: 3.5rem 0 5rem; }

  .lead {
    font-size: 1.18rem;
    font-weight: 400;
    color: var(--ink-light);
    line-height: 1.85;
    border-left: 3px solid var(--accent);
    padding-left: 1.4rem;
    margin-bottom: 2.8rem;
  }

  h2 {
    font-family: 'Source Serif 4', serif;
    font-size: 1.75rem;
    font-weight: 700;
    color: var(--ink);
    margin: 3.5rem 0 1rem;
    line-height: 1.25;
  }
  h2 .section-num {
    font-family: 'Inter', sans-serif;
    font-size: .75rem; font-weight: 600;
    color: var(--accent); letter-spacing: .1em;
    display: block; margin-bottom: .3rem;
    text-transform: uppercase;
  }

  h3 {
    font-family: 'Inter', sans-serif;
    font-size: 1.05rem; font-weight: 600;
    color: var(--ink); margin: 2rem 0 .6rem;
  }

  p { margin-bottom: 1.3rem; color: var(--ink-light); }
  p strong { color: var(--ink); font-weight: 600; }

  /* ── Code ── */
  .code-block {
    margin: 1.6rem 0;
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 4px 24px rgba(0,0,0,.18);
  }
  .code-label {
    background: #0d0d20;
    padding: .55rem 1.1rem;
    font-family: 'Inter', sans-serif;
    font-size: .7rem; font-weight: 500;
    color: #6b7280;
    display: flex; align-items: center; gap: .6rem;
    border-bottom: 1px solid rgba(255,255,255,.05);
  }
  .code-label .dot-red   { width:10px;height:10px;border-radius:50%;background:#ff5f57; }
  .code-label .dot-yel   { width:10px;height:10px;border-radius:50%;background:#febc2e; }
  .code-label .dot-grn   { width:10px;height:10px;border-radius:50%;background:#28c840; }
  .code-label .filename  { margin-left:.3rem; color:#9ca3af; }

  pre {
    background: var(--bg-code);
    padding: 1.4rem 1.3rem;
    overflow-x: auto;
    font-family: 'JetBrains Mono', 'Fira Code', monospace;
    font-size: .78rem; line-height: 1.75;
    color: #e2e8f0; margin: 0;
  }

  /* Syntax colours */
  .kw  { color: #c792ea; }   /* keywords */
  .fn  { color: #82aaff; }   /* functions */
  .st  { color: #c3e88d; }   /* strings */
  .cm  { color: #546e7a; font-style: italic; }  /* comments */
  .nb  { color: #f78c6c; }   /* numbers/builtins */
  .dc  { color: #ffcb6b; }   /* decorators */
  .tp  { color: #89ddff; }   /* types */
  .op  { color: #89ddff; }   /* operators */

  /* ── Callouts ── */
  .callout {
    border-radius: 8px; padding: 1.1rem 1.3rem;
    margin: 1.8rem 0; font-family: 'Inter', sans-serif; font-size: .88rem;
    line-height: 1.65;
  }
  .callout-title {
    font-weight: 600; font-size: .78rem; letter-spacing: .06em;
    text-transform: uppercase; margin-bottom: .4rem;
  }
  .callout.tip    { background:#ede9fe; border-left:3px solid #5b47e0; }
  .callout.tip .callout-title { color:#5b47e0; }
  .callout.tip p  { color:#3730a3; margin:0; }
  .callout.warn   { background:#fef3c7; border-left:3px solid #d97706; }
  .callout.warn .callout-title { color:#d97706; }
  .callout.warn p { color:#78350f; margin:0; }
  .callout.perf   { background:#d1faf3; border-left:3px solid #00c9a7; }
  .callout.perf .callout-title { color:#007a63; }
  .callout.perf p { color:#065f46; margin:0; }
  .callout.info   { background:#fce7f3; border-left:3px solid #e05b8a; }
  .callout.info .callout-title { color:#be185d; }
  .callout.info p { color:#831843; margin:0; }

  /* ── Comparison table ── */
  .table-wrap { overflow-x:auto; margin:1.6rem 0; }
  table {
    width:100%; border-collapse:collapse;
    font-family:'Inter',sans-serif; font-size:.82rem;
  }
  thead tr { background:#1a1a2e; color:#fff; }
  thead th { padding:.7rem 1rem; text-align:left; font-weight:600; font-size:.76rem; letter-spacing:.04em; }
  tbody tr:nth-child(even) { background:#f5f4ef; }
  tbody td { padding:.65rem 1rem; color:var(--ink-light); border-bottom:1px solid var(--border); vertical-align:top; }
  tbody td:first-child { font-weight:500; color:var(--ink); font-family:'JetBrains Mono',monospace; font-size:.76rem; }

  /* ── Divider ── */
  .divider {
    border:none; border-top: 1px solid var(--border);
    margin: 3rem 0;
  }
  .section-break {
    display:flex; align-items:center; gap:1rem; margin:3.5rem 0 0;
  }
  .section-break::before, .section-break::after {
    content:''; flex:1; height:1px; background:var(--border);
  }
  .section-break span {
    font-family:'Inter',sans-serif; font-size:.72rem; font-weight:600;
    color:var(--accent); letter-spacing:.12em; text-transform:uppercase;
  }

  /* ── Inline code ── */
  code {
    font-family:'JetBrains Mono',monospace;
    font-size:.82em; background:#ede9fe;
    color:#5b47e0; padding:.12em .4em; border-radius:4px;
  }

  /* ── TOC ── */
  .toc {
    background: var(--bg-warm);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1.5rem 1.8rem;
    margin: 2.5rem 0 3rem;
  }
  .toc-title {
    font-family:'Inter',sans-serif; font-size:.75rem; font-weight:600;
    color:var(--ink-muted); letter-spacing:.12em; text-transform:uppercase;
    margin-bottom: 1rem;
  }
  .toc ol { padding-left: 1.2rem; }
  .toc li { margin:.35rem 0; }
  .toc a {
    font-family:'Inter',sans-serif; font-size:.88rem; font-weight:500;
    color:var(--accent); text-decoration:none;
  }
  .toc a:hover { text-decoration:underline; }

  /* ── Decision grid ── */
  .decision-grid {
    display:grid; grid-template-columns:repeat(auto-fit,minmax(200px,1fr));
    gap:1rem; margin:1.5rem 0;
  }
  .decision-card {
    background:#fff; border:1px solid var(--border);
    border-radius:10px; padding:1.1rem 1.2rem;
    border-top:3px solid var(--accent);
  }
  .decision-card.teal  { border-top-color:#00c9a7; }
  .decision-card.pink  { border-top-color:#e05b8a; }
  .decision-card.amber { border-top-color:#f59e0b; }
  .decision-card h4 {
    font-family:'Inter',sans-serif; font-size:.8rem; font-weight:700;
    color:var(--ink); margin-bottom:.4rem;
  }
  .decision-card p { font-family:'Inter',sans-serif; font-size:.78rem; color:var(--ink-light); margin:0; line-height:1.5; }
  .decision-card .use-when { font-size:.7rem; color:var(--ink-muted); margin-top:.5rem; font-style:italic; }

  /* ── Footer ── */
  .article-footer {
    background: linear-gradient(135deg, #1a1a2e, #0f3460);
    padding: 3rem 2rem; text-align:center; margin-top:4rem;
    border-radius: 14px;
  }
  .article-footer h3 { font-family:'Source Serif 4',serif; color:#fff; font-size:1.4rem; margin-bottom:.6rem; }
  .article-footer p { font-family:'Inter',sans-serif; color:#94a3b8; font-size:.88rem; max-width:420px; margin:0 auto; }
</style>
</head>
<body>

<!-- ══════════════ HERO ══════════════ -->
<div class="hero">
  <div class="hero-inner">
    <p class="hero-eyebrow">Python for GenAI · Developer Deep Dive</p>
    <h1>Every Python Concept a <em>Generative AI Developer</em> Actually Needs to Know</h1>
    <p class="hero-sub">From async coroutines that power real-time LLM streaming, to memory tricks that let you process million-document datasets — the complete map, written for engineers building with AI today.</p>
    <div class="hero-meta">
      <span>By a practitioner, for practitioners</span>
      <span class="dot">·</span>
      <span class="read-time">⏱ 25 min read</span>
      <span class="dot">·</span>
      <span>Updated 2025</span>
    </div>
  </div>
</div>

<!-- ══════════════ ARTICLE ══════════════ -->
<div class="page-wrap">
<article>

  <div class="tags">
    <span class="tag">Python</span>
    <span class="tag teal">GenAI</span>
    <span class="tag">Async</span>
    <span class="tag pink">LLMs</span>
    <span class="tag amber">Performance</span>
    <span class="tag">Threading</span>
  </div>

  <p class="lead">
    Most Python tutorials teach you the language. This one teaches you the language <em>as a GenAI engineer uses it</em> — where every concept has a direct line to a real problem you will hit building LLM pipelines, RAG systems, and AI agents.
  </p>

  <!-- TOC -->
  <div class="toc">
    <div class="toc-title">Contents</div>
    <ol>
      <li><a href="#s1">Async / Await — The Heartbeat of Every LLM App</a></li>
      <li><a href="#s2">Threading — When Async Isn't Enough</a></li>
      <li><a href="#s3">Multiprocessing — Escaping the GIL for CPU Work</a></li>
      <li><a href="#s4">Generators — Processing Infinite Data in Finite Memory</a></li>
      <li><a href="#s5">Decorators & functools — Cross-Cutting Concerns Done Right</a></li>
      <li><a href="#s6">Context Managers — Deterministic Resource Cleanup</a></li>
      <li><a href="#s7">Type System, Dataclasses & Pydantic — Structured AI Outputs</a></li>
      <li><a href="#s8">Memory Management — Because Models Are Huge</a></li>
      <li><a href="#s9">Advanced Patterns — Metaclasses, Descriptors, Dunders</a></li>
      <li><a href="#s10">Production Patterns — Rate Limiting, Retries, Supervisors</a></li>
      <li><a href="#s11">Quick Reference</a></li>
    </ol>
  </div>

  <!-- ─────────────────────────────────────────── -->
  <h2 id="s1"><span class="section-num">Section 01</span>Async / Await — The Heartbeat of Every LLM App</h2>

  <p>Here is the brutal truth about building LLM applications: <strong>your code spends most of its time waiting</strong>. Waiting for Claude to respond. Waiting for an embedding API. Waiting for a vector database. Without async, you serve one user at a time. With async, you serve thousands concurrently — on a single thread.</p>

  <h3>What actually happens when you write <code>await</code></h3>
  <p>When Python hits an <code>await</code> expression, it pauses the current coroutine and hands control back to the event loop. The event loop looks at everything else that's ready to run, makes progress on it, and returns to your coroutine once the awaited result is available. No threads. No OS context switches. Pure cooperative multitasking.</p>

  <div class="code-block">
    <div class="code-label"><div class="dot-red"></div><div class="dot-yel"></div><div class="dot-grn"></div><span class="filename">concurrent_llm_calls.py</span></div>
    <pre><span class="kw">import</span> asyncio
<span class="kw">import</span> anthropic

client = anthropic.AsyncAnthropic()

<span class="kw">async def</span> <span class="fn">ask_claude</span>(prompt: <span class="tp">str</span>, label: <span class="tp">str</span>) -> <span class="tp">str</span>:
    <span class="cm"># Every await is a potential pause — but only if something else needs CPU</span>
    message = <span class="kw">await</span> client.messages.create(
        model=<span class="st">"claude-opus-4-5"</span>,
        max_tokens=<span class="nb">512</span>,
        messages=[{<span class="st">"role"</span>: <span class="st">"user"</span>, <span class="st">"content"</span>: prompt}]
    )
    <span class="kw">return</span> <span class="st">f"[</span><span class="nb">{label}</span><span class="st">] </span><span class="nb">{message.content[0].text}</span><span class="st">"</span>

<span class="kw">async def</span> <span class="fn">main</span>():
    questions = [
        (<span class="st">"What is a transformer architecture?"</span>,    <span class="st">"A"</span>),
        (<span class="st">"Explain RAG in one paragraph."</span>,            <span class="st">"B"</span>),
        (<span class="st">"What is chain-of-thought prompting?"</span>,      <span class="st">"C"</span>),
        (<span class="st">"Describe the attention mechanism briefly."</span>, <span class="st">"D"</span>),
        (<span class="st">"What is a vector database used for?"</span>,      <span class="st">"E"</span>),
    ]

    <span class="cm"># All 5 fire at once — total time ≈ slowest single call (~2s)</span>
    <span class="cm"># Sequential would take ~10s</span>
    results = <span class="kw">await</span> asyncio.gather(
        *[<span class="fn">ask_claude</span>(q, l) <span class="kw">for</span> q, l <span class="kw">in</span> questions]
    )
    <span class="kw">for</span> r <span class="kw">in</span> results:
        <span class="nb">print</span>(r)

asyncio.run(<span class="fn">main</span>())
</pre>
  </div>

  <div class="callout perf">
    <div class="callout-title">⚡ Real-World Impact</div>
    <p>Sequential LLM calls for 100 documents × 3 seconds each = 5 minutes. With <code>asyncio.gather()</code> they run concurrently and finish in ~3–5 seconds. That's a <strong>60× speedup</strong> with zero extra hardware.</p>
  </div>

  <h3>Tasks: fire and forget (then collect later)</h3>
  <p><code>asyncio.create_task()</code> schedules a coroutine immediately without waiting for it. This lets you kick off parallel work and collect results later — perfect for RAG pipelines where you retrieve from a vector store and a web search at the same time.</p>

  <div class="code-block">
    <div class="code-label"><div class="dot-red"></div><div class="dot-yel"></div><div class="dot-grn"></div><span class="filename">rag_parallel_retrieval.py</span></div>
    <pre><span class="kw">async def</span> <span class="fn">rag_pipeline</span>(query: <span class="tp">str</span>) -> <span class="tp">str</span>:
    <span class="cm"># Phase 1: kick off both retrievals simultaneously</span>
    task_vector = asyncio.create_task(<span class="fn">search_vector_db</span>(query))
    task_web    = asyncio.create_task(<span class="fn">search_web</span>(query))

    <span class="cm"># Both run concurrently while we do other prep work here</span>
    system_prompt = <span class="st">"You are a helpful research assistant."</span>

    <span class="cm"># Collect results — awaiting blocks only until each is ready</span>
    vector_hits, web_hits = <span class="kw">await</span> task_vector, <span class="kw">await</span> task_web

    context = <span class="fn">build_context</span>(vector_hits, web_hits)

    <span class="cm"># Phase 2: single LLM call with full context</span>
    <span class="kw">return await</span> <span class="fn">call_llm</span>(system_prompt, context, query)

<span class="cm"># Total: max(vector_latency, web_latency) + llm_latency</span>
<span class="cm"># Not:   vector_latency + web_latency + llm_latency</span>
</pre>
  </div>

  <h3>Streaming tokens in real time with async generators</h3>
  <p>ChatGPT-style streaming — where tokens appear as they're generated — requires async generators. Instead of waiting for the full response, you yield each token as it arrives and forward it to the client immediately.</p>

  <div class="code-block">
    <div class="code-label"><div class="dot-red"></div><div class="dot-yel"></div><div class="dot-grn"></div><span class="filename">streaming_response.py</span></div>
    <pre><span class="kw">import</span> anthropic

client = anthropic.AsyncAnthropic()

<span class="kw">async def</span> <span class="fn">stream_response</span>(prompt: <span class="tp">str</span>):
    <span class="st">"""Async generator — yields tokens as they arrive from the LLM."""</span>
    <span class="kw">async with</span> client.messages.stream(
        model=<span class="st">"claude-opus-4-5"</span>,
        max_tokens=<span class="nb">1024</span>,
        messages=[{<span class="st">"role"</span>: <span class="st">"user"</span>, <span class="st">"content"</span>: prompt}]
    ) <span class="kw">as</span> stream:
        <span class="kw">async for</span> text <span class="kw">in</span> stream.text_stream:
            <span class="kw">yield</span> text          <span class="cm"># each token arrives here ~50ms apart</span>

<span class="kw">async def</span> <span class="fn">handle_request</span>(prompt: <span class="tp">str</span>):
    full_text = <span class="st">""</span>
    <span class="kw">async for</span> token <span class="kw">in</span> <span class="fn">stream_response</span>(prompt):
        <span class="nb">print</span>(token, end=<span class="st">""</span>, flush=<span class="nb">True</span>)   <span class="cm"># real-time display</span>
        full_text += token
    <span class="nb">print</span>()
    <span class="kw">return</span> full_text

asyncio.run(<span class="fn">handle_request</span>(<span class="st">"Explain diffusion models simply."</span>))
</pre>
  </div>

  <h3>Locks: protecting shared state across coroutines</h3>
  <p>Even though asyncio is single-threaded, race conditions exist. If two coroutines both read-then-write a shared counter without a lock, you'll get wrong results. <code>asyncio.Lock</code> ensures only one coroutine is inside the critical section at a time.</p>

  <div class="code-block">
    <div class="code-label"><div class="dot-red"></div><div class="dot-yel"></div><div class="dot-grn"></div><span class="filename">rate_counter.py</span></div>
    <pre><span class="kw">import</span> asyncio
<span class="kw">from</span> collections <span class="kw">import</span> defaultdict

request_counts: dict[str, int] = defaultdict(<span class="nb">int</span>)
lock = asyncio.Lock()

<span class="kw">async def</span> <span class="fn">tracked_embed</span>(text: <span class="tp">str</span>, model: <span class="tp">str</span>) -> <span class="tp">list</span>[<span class="tp">float</span>]:
    <span class="kw">async with</span> lock:
        request_counts[model] += <span class="nb">1</span>
        <span class="kw">if</span> request_counts[model] > <span class="nb">1000</span>:
            <span class="kw">raise</span> <span class="tp">RuntimeError</span>(<span class="st">f"Daily limit hit for </span><span class="nb">{model}</span><span class="st">"</span>)

    <span class="kw">return await</span> <span class="fn">call_embedding_api</span>(text, model)
</pre>
  </div>

  <hr class="divider">

  <!-- ─────────────────────────────────────────── -->
  <h2 id="s2"><span class="section-num">Section 02</span>Threading — When Your Library Doesn't Speak Async</h2>

  <p>Many powerful Python libraries — <code>requests</code>, some database drivers, HuggingFace's synchronous API — are blocking. You can't just slap <code>await</code> on them. But you also can't leave performance on the table. Threading is the answer.</p>

  <h3>The GIL: what it blocks and what it doesn't</h3>
  <p>The <strong>Global Interpreter Lock (GIL)</strong> is a mutex in CPython that prevents more than one thread from running Python bytecode at the same time. It sounds like threading is useless — but it isn't, because the GIL is released during:</p>

  <div class="decision-grid">
    <div class="decision-card teal">
      <h4>I/O operations</h4>
      <p>Network calls, file reads/writes, socket operations. The GIL releases while the OS handles I/O.</p>
      <p class="use-when">→ Threads work great here</p>
    </div>
    <div class="decision-card">
      <h4>C extensions</h4>
      <p>NumPy, PyTorch ops, SciPy — all run C code that releases the GIL for the duration.</p>
      <p class="use-when">→ Threads work great here</p>
    </div>
    <div class="decision-card pink">
      <h4>Pure Python CPU</h4>
      <p>Loops, string operations, pure Python math. The GIL never releases — threads don't help.</p>
      <p class="use-when">→ Use multiprocessing instead</p>
    </div>
  </div>

  <div class="code-block">
    <div class="code-label"><div class="dot-red"></div><div class="dot-yel"></div><div class="dot-grn"></div><span class="filename">threadpool_embedding.py</span></div>
    <pre><span class="kw">from</span> concurrent.futures <span class="kw">import</span> ThreadPoolExecutor, as_completed
<span class="kw">from</span> sentence_transformers <span class="kw">import</span> SentenceTransformer

<span class="cm"># Blocking library — can't use asyncio, but threads work fine</span>
model = SentenceTransformer(<span class="st">"all-MiniLM-L6-v2"</span>)

<span class="kw">def</span> <span class="fn">embed_text</span>(text: <span class="tp">str</span>, idx: <span class="tp">int</span>) -> <span class="tp">tuple</span>:
    embedding = model.encode(text)   <span class="cm"># GIL released — C extension runs</span>
    <span class="kw">return</span> idx, embedding.tolist()

texts = [<span class="st">f"Document chunk </span><span class="nb">{i}</span><span class="st">"</span> <span class="kw">for</span> i <span class="kw">in</span> <span class="nb">range</span>(<span class="nb">50</span>)]

<span class="kw">with</span> ThreadPoolExecutor(max_workers=<span class="nb">8</span>) <span class="kw">as</span> pool:
    futures = {pool.submit(<span class="fn">embed_text</span>, t, i): i <span class="kw">for</span> i, t <span class="kw">in</span> <span class="nb">enumerate</span>(texts)}
    results = {}
    <span class="kw">for</span> future <span class="kw">in</span> as_completed(futures):
        idx, embedding = future.result()
        results[idx] = embedding

<span class="nb">print</span>(<span class="st">f"Embedded </span><span class="nb">{len(results)}</span><span class="st"> chunks"</span>)
</pre>
  </div>

  <h3>Synchronization primitives — the full toolkit</h3>

  <div class="table-wrap">
    <table>
      <thead><tr><th>Primitive</th><th>What it does</th><th>GenAI use case</th></tr></thead>
      <tbody>
        <tr><td>Lock</td><td>Only one thread at a time</td><td>Writing to a shared results dict</td></tr>
        <tr><td>RLock</td><td>Re-entrant — same thread can acquire again</td><td>Recursive pipeline stages</td></tr>
        <tr><td>Event</td><td>Binary signal: set / wait / clear</td><td>Signal when model has loaded</td></tr>
        <tr><td>Semaphore</td><td>Counter-based: allow N concurrent threads</td><td>Limit to N parallel API calls</td></tr>
        <tr><td>Condition</td><td>Complex signalling with wait/notify</td><td>Producer notifies consumer batch</td></tr>
        <tr><td>Barrier</td><td>N threads wait until all arrive</td><td>Sync pipeline stages before merge</td></tr>
      </tbody>
    </table>
  </div>

  <div class="code-block">
    <div class="code-label"><div class="dot-red"></div><div class="dot-yel"></div><div class="dot-grn"></div><span class="filename">model_loader_with_event.py</span></div>
    <pre><span class="kw">import</span> threading, time

model_ready  = threading.Event()
api_sem      = threading.Semaphore(<span class="nb">5</span>)   <span class="cm"># max 5 concurrent inference calls</span>

<span class="kw">def</span> <span class="fn">load_model</span>():
    <span class="nb">print</span>(<span class="st">"Loading model weights..."</span>)
    time.sleep(<span class="nb">3</span>)               <span class="cm"># simulate loading 7B param model</span>
    model_ready.set()           <span class="cm"># unblocks ALL waiting threads at once</span>
    <span class="nb">print</span>(<span class="st">"Model ready!"</span>)

<span class="kw">def</span> <span class="fn">inference_worker</span>(worker_id: <span class="tp">int</span>):
    model_ready.wait()          <span class="cm"># block here until model is loaded</span>
    <span class="kw">with</span> api_sem:               <span class="cm"># at most 5 simultaneous inference calls</span>
        <span class="nb">print</span>(<span class="st">f"Worker </span><span class="nb">{worker_id}</span><span class="st">: running inference"</span>)
        time.sleep(<span class="nb">0.5</span>)        <span class="cm"># simulate inference</span>

loader  = threading.Thread(target=<span class="fn">load_model</span>, daemon=<span class="nb">True</span>)
workers = [threading.Thread(target=<span class="fn">inference_worker</span>, args=(i,)) <span class="kw">for</span> i <span class="kw">in</span> <span class="nb">range</span>(<span class="nb">12</span>)]

loader.start()
<span class="kw">for</span> w <span class="kw">in</span> workers: w.start()
<span class="kw">for</span> w <span class="kw">in</span> workers: w.join()
</pre>
  </div>

  <hr class="divider">

  <!-- ─────────────────────────────────────────── -->
  <h2 id="s3"><span class="section-num">Section 03</span>Multiprocessing — Escaping the GIL for CPU-Heavy Work</h2>

  <p>Tokenising 10 million documents. Computing cosine similarity across a 100K-embedding matrix. Running feature extraction before model training. This is CPU-bound work — and threading won't help you. You need <strong>multiprocessing</strong>: separate OS processes, each with their own Python interpreter and GIL, running truly in parallel.</p>

  <div class="code-block">
    <div class="code-label"><div class="dot-red"></div><div class="dot-yel"></div><div class="dot-grn"></div><span class="filename">parallel_tokenisation.py</span></div>
    <pre><span class="kw">from</span> concurrent.futures <span class="kw">import</span> ProcessPoolExecutor
<span class="kw">from</span> transformers <span class="kw">import</span> AutoTokenizer
<span class="kw">import</span> multiprocessing <span class="kw">as</span> mp

tokenizer = <span class="nb">None</span>   <span class="cm"># process-local — each worker initialises its own</span>

<span class="kw">def</span> <span class="fn">init_worker</span>():
    <span class="cm">"""Called once per process. Avoids re-loading the tokenizer for every job."""</span>
    <span class="kw">global</span> tokenizer
    tokenizer = AutoTokenizer.from_pretrained(<span class="st">"gpt2"</span>)

<span class="kw">def</span> <span class="fn">tokenise_chunk</span>(text: <span class="tp">str</span>) -> <span class="tp">dict</span>:
    <span class="cm"># Pure CPU work — runs across all cores simultaneously</span>
    tokens = tokenizer(
        text, truncation=<span class="nb">True</span>, max_length=<span class="nb">512</span>,
        padding=<span class="st">"max_length"</span>, return_tensors=<span class="nb">None</span>
    )
    <span class="kw">return</span> {
        <span class="st">"input_ids"</span>:      tokens[<span class="st">"input_ids"</span>],
        <span class="st">"attention_mask"</span>: tokens[<span class="st">"attention_mask"</span>],
        <span class="st">"token_count"</span>:    <span class="nb">sum</span>(tokens[<span class="st">"attention_mask"</span>])
    }

<span class="kw">def</span> <span class="fn">preprocess_dataset</span>(texts: <span class="tp">list</span>[<span class="tp">str</span>]) -> <span class="tp">list</span>[<span class="tp">dict</span>]:
    n = mp.cpu_count()
    <span class="nb">print</span>(<span class="st">f"Using </span><span class="nb">{n}</span><span class="st"> cores to process </span><span class="nb">{len(texts)}</span><span class="st"> texts"</span>)
    <span class="kw">with</span> ProcessPoolExecutor(max_workers=n, initializer=<span class="fn">init_worker</span>) <span class="kw">as</span> pool:
        <span class="kw">return</span> <span class="nb">list</span>(pool.map(<span class="fn">tokenise_chunk</span>, texts, chunksize=<span class="nb">128</span>))

<span class="kw">if</span> __name__ == <span class="st">"__main__"</span>:   <span class="cm"># REQUIRED on Windows / macOS</span>
    docs = [<span class="st">f"Training document number </span><span class="nb">{i}</span><span class="st">"</span> <span class="kw">for</span> i <span class="kw">in</span> <span class="nb">range</span>(<span class="nb">100_000</span>)]
    tokenised = <span class="fn">preprocess_dataset</span>(docs)
    <span class="nb">print</span>(<span class="st">f"Done — </span><span class="nb">{len(tokenised)}</span><span class="st"> chunks tokenised"</span>)
</pre>
  </div>

  <h3>Shared memory: zero-copy arrays across processes</h3>
  <p>Passing large NumPy arrays through <code>Queue</code> serialises them through pickle — slow and memory-intensive. <code>multiprocessing.shared_memory</code> lets all processes read and write the same raw memory block. For embedding matrices, this is transformative.</p>

  <div class="code-block">
    <div class="code-label"><div class="dot-red"></div><div class="dot-yel"></div><div class="dot-grn"></div><span class="filename">shared_embedding_matrix.py</span></div>
    <pre><span class="kw">import</span> numpy <span class="kw">as</span> np
<span class="kw">from</span> multiprocessing <span class="kw">import</span> shared_memory, Process

<span class="kw">def</span> <span class="fn">fill_shard</span>(shm_name: <span class="tp">str</span>, shape: <span class="tp">tuple</span>, start: <span class="tp">int</span>, end: <span class="tp">int</span>):
    <span class="cm"># Attach to existing shared block — no data copying</span>
    shm = shared_memory.SharedMemory(name=shm_name)
    matrix = np.ndarray(shape, dtype=np.float32, buffer=shm.buf)
    <span class="kw">for</span> i <span class="kw">in</span> <span class="nb">range</span>(start, end):
        matrix[i] = np.random.randn(<span class="nb">1536</span>).astype(np.float32)
    shm.close()

<span class="kw">if</span> __name__ == <span class="st">"__main__"</span>:
    N, DIM = <span class="nb">50_000</span>, <span class="nb">1536</span>
    shape  = (N, DIM)

    <span class="cm"># One allocation shared by all processes — 300MB once, not 4×300MB</span>
    shm = shared_memory.SharedMemory(create=<span class="nb">True</span>, size=N * DIM * <span class="nb">4</span>)
    matrix = np.ndarray(shape, dtype=np.float32, buffer=shm.buf)

    chunk = N // <span class="nb">4</span>
    procs = [
        Process(target=<span class="fn">fill_shard</span>, args=(shm.name, shape, i*chunk, (i+<span class="nb">1</span>)*chunk))
        <span class="kw">for</span> i <span class="kw">in</span> <span class="nb">range</span>(<span class="nb">4</span>)
    ]
    <span class="kw">for</span> p <span class="kw">in</span> procs: p.start()
    <span class="kw">for</span> p <span class="kw">in</span> procs: p.join()

    <span class="nb">print</span>(<span class="st">f"Matrix ready: </span><span class="nb">{matrix.shape}</span><span class="st">"</span>)
    shm.unlink()   <span class="cm"># free the OS-level shared block</span>
</pre>
  </div>

  <hr class="divider">

  <!-- ─────────────────────────────────────────── -->
  <h2 id="s4"><span class="section-num">Section 04</span>Generators — Processing Infinite Data in Finite Memory</h2>

  <p>Pre-training data for a modern LLM is measured in terabytes. You cannot load it into RAM. You need to stream it, process it, and feed it to the model one batch at a time — and generators are exactly the right tool for this.</p>

  <h3>The fundamental idea: yield is a pause button</h3>
  <p>A regular function runs to completion and returns once. A generator function runs to a <code>yield</code>, returns that value, and then <em>pauses</em> — preserving all local state — until the caller asks for the next value. No list is ever built. Memory usage stays constant.</p>

  <div class="code-block">
    <div class="code-label"><div class="dot-red"></div><div class="dot-yel"></div><div class="dot-grn"></div><span class="filename">streaming_data_pipeline.py</span></div>
    <pre><span class="kw">import</span> json
<span class="kw">from</span> pathlib <span class="kw">import</span> Path
<span class="kw">import</span> itertools

<span class="kw">def</span> <span class="fn">stream_jsonl</span>(path: <span class="tp">str</span>):
    <span class="st">"""Yield one record at a time from a multi-GB JSONL file."""</span>
    <span class="kw">with</span> <span class="nb">open</span>(path, encoding=<span class="st">"utf-8"</span>) <span class="kw">as</span> f:
        <span class="kw">for</span> line <span class="kw">in</span> f:
            <span class="kw">if</span> line.strip():
                <span class="kw">yield</span> json.loads(line)   <span class="cm"># one record in memory at a time</span>

<span class="kw">def</span> <span class="fn">clean</span>(records):
    <span class="st">"""Filter + transform — another generator, no new list."""</span>
    <span class="kw">for</span> r <span class="kw">in</span> records:
        text = r.get(<span class="st">"text"</span>, <span class="st">""</span>).strip()
        <span class="kw">if</span> <span class="nb">len</span>(text) >= <span class="nb">100</span>:
            <span class="kw">yield</span> {<span class="st">"text"</span>: text, <span class="st">"source"</span>: r.get(<span class="st">"url"</span>, <span class="st">"unknown"</span>)}

<span class="kw">def</span> <span class="fn">batch</span>(iterable, size: <span class="tp">int</span>):
    <span class="st">"""Yield fixed-size batches. Classic pattern for mini-batch training."""</span>
    buf = []
    <span class="kw">for</span> item <span class="kw">in</span> iterable:
        buf.append(item)
        <span class="kw">if</span> <span class="nb">len</span>(buf) == size:
            <span class="kw">yield</span> buf
            buf = []
    <span class="kw">if</span> buf:
        <span class="kw">yield</span> buf

<span class="cm"># Compose: the ENTIRE file is processed with O(batch_size) memory</span>
pipeline = <span class="fn">batch</span>(<span class="fn">clean</span>(<span class="fn">stream_jsonl</span>(<span class="st">"training.jsonl"</span>)), size=<span class="nb">32</span>)

<span class="kw">for</span> mini_batch <span class="kw">in</span> pipeline:
    <span class="nb">print</span>(<span class="st">f"Training on batch of </span><span class="nb">{len(mini_batch)}</span><span class="st"> documents"</span>)
    <span class="cm"># trainer.step(mini_batch)</span>

<span class="cm"># Bonus: chain multiple datasets seamlessly with itertools</span>
multi_dataset = itertools.chain.from_iterable(
    <span class="fn">stream_jsonl</span>(p) <span class="kw">for</span> p <span class="kw">in</span> [<span class="st">"data1.jsonl"</span>, <span class="st">"data2.jsonl"</span>, <span class="st">"data3.jsonl"</span>]
)
</pre>
  </div>

  <div class="callout tip">
    <div class="callout-title">💡 Generator vs List Comprehension</div>
    <p><code>[x for x in data]</code> builds a full list in RAM. <code>(x for x in data)</code> is a lazy generator expression — use it when you only need to iterate once, especially over large datasets. For 1M embeddings at dim=1536, the difference is 6 GB vs a few hundred bytes.</p>
  </div>

  <hr class="divider">

  <!-- ─────────────────────────────────────────── -->
  <h2 id="s5"><span class="section-num">Section 05</span>Decorators & functools — Cross-Cutting Concerns Done Right</h2>

  <p>Every LLM call needs logging. Every external API call needs retries. Every expensive computation needs caching. You don't want this logic scattered through your code — you want it applied cleanly via decorators.</p>

  <div class="code-block">
    <div class="code-label"><div class="dot-red"></div><div class="dot-yel"></div><div class="dot-grn"></div><span class="filename">llm_decorators.py</span></div>
    <pre><span class="kw">import</span> functools, time, asyncio, logging
<span class="kw">from</span> typing <span class="kw">import</span> Callable

<span class="kw">def</span> <span class="fn">trace_llm</span>(func: <span class="tp">Callable</span>) -> <span class="tp">Callable</span>:
    <span class="st">"""Log every LLM call: inputs, latency, and any errors."""</span>
    <span class="dc">@functools.wraps(func)</span>
    <span class="kw">async def</span> <span class="fn">wrapper</span>(*args, **kwargs):
        start = time.perf_counter()
        logging.info(<span class="st">f"→ </span><span class="nb">{func.__name__}</span><span class="st">"</span>)
        <span class="kw">try</span>:
            result = <span class="kw">await</span> <span class="fn">func</span>(*args, **kwargs)
            ms = (time.perf_counter() - start) * <span class="nb">1000</span>
            logging.info(<span class="st">f"✓ </span><span class="nb">{func.__name__}</span><span class="st"> completed in </span><span class="nb">{ms:.0f}</span><span class="st">ms"</span>)
            <span class="kw">return</span> result
        <span class="kw">except</span> <span class="tp">Exception</span> <span class="kw">as</span> e:
            ms = (time.perf_counter() - start) * <span class="nb">1000</span>
            logging.error(<span class="st">f"✗ </span><span class="nb">{func.__name__}</span><span class="st"> failed after </span><span class="nb">{ms:.0f}</span><span class="st">ms: </span><span class="nb">{e}</span><span class="st">"</span>)
            <span class="kw">raise</span>
    <span class="kw">return</span> wrapper

<span class="kw">def</span> <span class="fn">retry</span>(max_attempts: <span class="tp">int</span> = <span class="nb">3</span>, base_delay: <span class="tp">float</span> = <span class="nb">1.0</span>):
    <span class="st">"""Exponential backoff retry for async functions."""</span>
    <span class="kw">def</span> <span class="fn">decorator</span>(func):
        <span class="dc">@functools.wraps(func)</span>
        <span class="kw">async def</span> <span class="fn">wrapper</span>(*args, **kwargs):
            <span class="kw">for</span> attempt <span class="kw">in</span> <span class="nb">range</span>(max_attempts):
                <span class="kw">try</span>:
                    <span class="kw">return await</span> <span class="fn">func</span>(*args, **kwargs)
                <span class="kw">except</span> (<span class="tp">ConnectionError</span>, <span class="tp">TimeoutError</span>) <span class="kw">as</span> e:
                    <span class="kw">if</span> attempt == max_attempts - <span class="nb">1</span>:
                        <span class="kw">raise</span>
                    delay = base_delay * (<span class="nb">2</span> ** attempt)
                    <span class="nb">print</span>(<span class="st">f"Retry </span><span class="nb">{attempt+1}</span><span class="st">/</span><span class="nb">{max_attempts}</span><span class="st"> in </span><span class="nb">{delay}</span><span class="st">s: </span><span class="nb">{e}</span><span class="st">"</span>)
                    <span class="kw">await</span> asyncio.sleep(delay)
        <span class="kw">return</span> wrapper
    <span class="kw">return</span> decorator

<span class="dc">@trace_llm</span>
<span class="dc">@retry(max_attempts=3)</span>
<span class="kw">async def</span> <span class="fn">generate</span>(prompt: <span class="tp">str</span>) -> <span class="tp">str</span>:
    <span class="cm"># Your actual LLM call goes here</span>
    <span class="kw">return</span> <span class="st">"response"</span>
</pre>
  </div>

  <h3>lru_cache: free performance for embedding lookups</h3>
  <p>Embedding API calls are expensive. If your app re-embeds the same query text multiple times, you're burning money. <code>@functools.lru_cache</code> memoizes function results in memory — identical inputs return the cached result instantly.</p>

  <div class="code-block">
    <div class="code-label"><div class="dot-red"></div><div class="dot-yel"></div><div class="dot-grn"></div><span class="filename">cached_embeddings.py</span></div>
    <pre><span class="kw">import</span> functools

<span class="dc">@functools.lru_cache(maxsize=10_000)</span>
<span class="kw">def</span> <span class="fn">get_embedding</span>(text: <span class="tp">str</span>, model: <span class="tp">str</span>) -> <span class="tp">tuple</span>[<span class="tp">float</span>, <span class="st">...</span>]:
    <span class="cm"># Note: returns tuple (hashable) not list, so it can be cached</span>
    embedding = call_embedding_api(text, model)
    <span class="kw">return</span> <span class="nb">tuple</span>(embedding)

<span class="cm"># First call: hits the API (~100ms)</span>
v1 = <span class="fn">get_embedding</span>(<span class="st">"What is RAG?"</span>, <span class="st">"text-embedding-3-small"</span>)

<span class="cm"># Second call: returns instantly from cache (0ms)</span>
v2 = <span class="fn">get_embedding</span>(<span class="st">"What is RAG?"</span>, <span class="st">"text-embedding-3-small"</span>)

<span class="nb">print</span>(<span class="fn">get_embedding</span>.cache_info())
<span class="cm"># CacheInfo(hits=1, misses=1, maxsize=10000, currsize=1)</span>

<span class="cm"># partial: create specialised LLM callers from a general function</span>
<span class="kw">def</span> <span class="fn">call_llm</span>(prompt, model, temperature, max_tokens): ...

creative = functools.partial(<span class="fn">call_llm</span>, model=<span class="st">"claude-opus-4-5"</span>,
                              temperature=<span class="nb">0.9</span>, max_tokens=<span class="nb">2048</span>)
analyst  = functools.partial(<span class="fn">call_llm</span>, model=<span class="st">"claude-opus-4-5"</span>,
                              temperature=<span class="nb">0.1</span>, max_tokens=<span class="nb">512</span>)
</pre>
  </div>

  <hr class="divider">

  <!-- ─────────────────────────────────────────── -->
  <h2 id="s6"><span class="section-num">Section 06</span>Context Managers — Deterministic Resource Cleanup</h2>

  <p>AI applications manage expensive, limited resources: GPU memory, HTTP connection pools, DB connection pools, temporary model checkpoints. When an exception happens mid-pipeline — and it will — you need to guarantee cleanup. Context managers are that guarantee.</p>

  <div class="code-block">
    <div class="code-label"><div class="dot-red"></div><div class="dot-yel"></div><div class="dot-grn"></div><span class="filename">pipeline_tracing.py</span></div>
    <pre><span class="kw">from</span> contextlib <span class="kw">import</span> contextmanager, asynccontextmanager
<span class="kw">import</span> time, uuid

<span class="dc">@contextmanager</span>
<span class="kw">def</span> <span class="fn">pipeline_span</span>(name: <span class="tp">str</span>):
    <span class="st">"""Trace any code block with start/end timing and error capture."""</span>
    span_id = str(uuid.uuid4())[:<span class="nb">8</span>]
    start   = time.perf_counter()
    <span class="nb">print</span>(<span class="st">f"[START] </span><span class="nb">{name}</span><span class="st"> (</span><span class="nb">{span_id}</span><span class="st">)"</span>)
    <span class="kw">try</span>:
        <span class="kw">yield</span> span_id
    <span class="kw">except</span> <span class="tp">Exception</span> <span class="kw">as</span> e:
        <span class="nb">print</span>(<span class="st">f"[ERROR] </span><span class="nb">{name}</span><span class="st">: </span><span class="nb">{e}</span><span class="st">"</span>)
        <span class="kw">raise</span>
    <span class="kw">finally</span>:
        ms = (time.perf_counter() - start) * <span class="nb">1000</span>
        <span class="nb">print</span>(<span class="st">f"[END]   </span><span class="nb">{name}</span><span class="st"> — </span><span class="nb">{ms:.1f}</span><span class="st">ms"</span>)

<span class="cm"># Nest spans to build a full trace tree</span>
<span class="kw">with</span> <span class="fn">pipeline_span</span>(<span class="st">"full_rag"</span>):
    <span class="kw">with</span> <span class="fn">pipeline_span</span>(<span class="st">"retrieval"</span>):
        time.sleep(<span class="nb">0.05</span>)
    <span class="kw">with</span> <span class="fn">pipeline_span</span>(<span class="st">"llm_call"</span>):
        time.sleep(<span class="nb">0.12</span>)

<span class="cm"># For dynamically many resources: ExitStack</span>
<span class="kw">from</span> contextlib <span class="kw">import</span> ExitStack

<span class="kw">def</span> <span class="fn">load_model_shards</span>(shard_paths: <span class="tp">list</span>[<span class="tp">str</span>]):
    <span class="kw">with</span> ExitStack() <span class="kw">as</span> stack:
        <span class="cm"># Open an unknown number of shards — all cleaned up on exit</span>
        handles = [stack.enter_context(<span class="nb">open</span>(p, <span class="st">"rb"</span>)) <span class="kw">for</span> p <span class="kw">in</span> shard_paths]
        stack.callback(<span class="kw">lambda</span>: <span class="nb">print</span>(<span class="st">"All shards closed"</span>))
        <span class="kw">for</span> i, fh <span class="kw">in</span> <span class="nb">enumerate</span>(handles):
            header = fh.read(<span class="nb">256</span>)
            <span class="nb">print</span>(<span class="st">f"Shard </span><span class="nb">{i}</span><span class="st">: read </span><span class="nb">{len(header)}</span><span class="st"> bytes"</span>)
</pre>
  </div>

  <hr class="divider">

  <!-- ─────────────────────────────────────────── -->
  <h2 id="s7"><span class="section-num">Section 07</span>Type System, Dataclasses & Pydantic — Structured AI Outputs</h2>

  <p>LLMs are probabilistic. They don't always produce valid JSON, the right fields, or values in the expected range. Your code has to validate, parse, and handle errors — and the Python type system with Pydantic makes this robust and readable.</p>

  <div class="code-block">
    <div class="code-label"><div class="dot-red"></div><div class="dot-yel"></div><div class="dot-grn"></div><span class="filename">structured_outputs.py</span></div>
    <pre><span class="kw">from</span> pydantic <span class="kw">import</span> BaseModel, Field, validator
<span class="kw">from</span> dataclasses <span class="kw">import</span> dataclass, field
<span class="kw">from</span> typing <span class="kw">import</span> Literal
<span class="kw">import</span> json, anthropic

<span class="cm"># Dataclasses: lightweight typed containers for internal use</span>
<span class="dc">@dataclass</span>
<span class="kw">class</span> <span class="tp">LLMResponse</span>:
    content:       <span class="tp">str</span>
    model:         <span class="tp">str</span>
    input_tokens:  <span class="tp">int</span>
    output_tokens: <span class="tp">int</span>
    latency_ms:    <span class="tp">float</span>
    finish_reason: Literal[<span class="st">"end_turn"</span>, <span class="st">"max_tokens"</span>, <span class="st">"stop_sequence"</span>]
    metadata: <span class="tp">dict</span> = field(default_factory=<span class="nb">dict</span>)

    <span class="dc">@property</span>
    <span class="kw">def</span> <span class="fn">total_tokens</span>(self) -> <span class="tp">int</span>:
        <span class="kw">return</span> self.input_tokens + self.output_tokens

<span class="cm"># Pydantic: for LLM-produced JSON that must be validated at runtime</span>
<span class="kw">class</span> <span class="tp">ExtractedFact</span>(BaseModel):
    claim:      <span class="tp">str</span> = Field(description=<span class="st">"The factual claim"</span>)
    confidence: <span class="tp">float</span> = Field(ge=<span class="nb">0.0</span>, le=<span class="nb">1.0</span>, description=<span class="st">"0-1 confidence"</span>)
    source:     <span class="tp">str</span> = Field(description=<span class="st">"Quote from source text"</span>)

<span class="kw">class</span> <span class="tp">FactExtractionResult</span>(BaseModel):
    facts:   <span class="tp">list</span>[<span class="tp">ExtractedFact</span>]
    summary: <span class="tp">str</span>

    <span class="dc">@validator("facts")</span>
    <span class="kw">def</span> <span class="fn">at_least_one</span>(cls, v):
        <span class="kw">if not</span> v:
            <span class="kw">raise</span> <span class="tp">ValueError</span>(<span class="st">"Must extract at least one fact"</span>)
        <span class="kw">return</span> v

<span class="kw">async def</span> <span class="fn">extract_facts</span>(text: <span class="tp">str</span>) -> <span class="tp">FactExtractionResult</span>:
    client = anthropic.AsyncAnthropic()
    resp = <span class="kw">await</span> client.messages.create(
        model=<span class="st">"claude-opus-4-5"</span>, max_tokens=<span class="nb">1024</span>,
        system=<span class="st">"Extract facts. Return ONLY valid JSON, no markdown."</span>,
        messages=[{<span class="st">"role"</span>: <span class="st">"user"</span>, <span class="st">"content"</span>: text}]
    )
    raw = resp.content[<span class="nb">0</span>].text
    <span class="kw">return</span> <span class="tp">FactExtractionResult</span>(**json.loads(raw))  <span class="cm"># validates or raises</span>
</pre>
  </div>

  <h3>Protocols: write components that work with any LLM backend</h3>

  <div class="code-block">
    <div class="code-label"><div class="dot-red"></div><div class="dot-yel"></div><div class="dot-grn"></div><span class="filename">protocols_for_rag.py</span></div>
    <pre><span class="kw">from</span> typing <span class="kw">import</span> Protocol, runtime_checkable

<span class="dc">@runtime_checkable</span>
<span class="kw">class</span> <span class="tp">Embedder</span>(Protocol):
    <span class="st">"""Any class that implements embed() satisfies this — no inheritance."""</span>
    <span class="kw">async def</span> <span class="fn">embed</span>(self, text: <span class="tp">str</span>) -> <span class="tp">list</span>[<span class="tp">float</span>]: ...
    <span class="dc">@property</span>
    <span class="kw">def</span> <span class="fn">dimension</span>(self) -> <span class="tp">int</span>: ...

<span class="dc">@runtime_checkable</span>
<span class="kw">class</span> <span class="tp">VectorStore</span>(Protocol):
    <span class="kw">async def</span> <span class="fn">upsert</span>(self, doc_id: <span class="tp">str</span>, vec: <span class="tp">list</span>[<span class="tp">float</span>], meta: <span class="tp">dict</span>) -> <span class="nb">None</span>: ...
    <span class="kw">async def</span> <span class="fn">search</span>(self, vec: <span class="tp">list</span>[<span class="tp">float</span>], top_k: <span class="tp">int</span>) -> <span class="tp">list</span>[<span class="tp">dict</span>]: ...

<span class="kw">class</span> <span class="tp">RAGPipeline</span>:
    <span class="st">"""Backend-agnostic: works with OpenAI, Cohere, or any compliant Embedder."""</span>
    <span class="kw">def</span> <span class="fn">__init__</span>(self, embedder: <span class="tp">Embedder</span>, store: <span class="tp">VectorStore</span>):
        self.embedder = embedder
        self.store    = store

    <span class="kw">async def</span> <span class="fn">ingest</span>(self, doc_id: <span class="tp">str</span>, text: <span class="tp">str</span>):
        vec = <span class="kw">await</span> self.embedder.embed(text)
        <span class="kw">await</span> self.store.upsert(doc_id, vec, {<span class="st">"text"</span>: text})

    <span class="kw">async def</span> <span class="fn">retrieve</span>(self, query: <span class="tp">str</span>, top_k: <span class="tp">int</span> = <span class="nb">5</span>) -> <span class="tp">list</span>[<span class="tp">dict</span>]:
        q_vec = <span class="kw">await</span> self.embedder.embed(query)
        <span class="kw">return await</span> self.store.search(q_vec, top_k)
</pre>
  </div>

  <hr class="divider">

  <!-- ─────────────────────────────────────────── -->
  <h2 id="s8"><span class="section-num">Section 08</span>Memory Management — Because Models Are Huge</h2>

  <p>A 7B parameter model in float16 occupies 14 GB of RAM. A 70B model needs 140 GB. Even working with embeddings at scale is a memory challenge. Understanding Python's memory model isn't academic — it directly determines what you can run and how fast.</p>

  <div class="code-block">
    <div class="code-label"><div class="dot-red"></div><div class="dot-yel"></div><div class="dot-grn"></div><span class="filename">memory_efficiency.py</span></div>
    <pre><span class="kw">import</span> sys, gc, weakref

<span class="cm"># __slots__: eliminates per-instance __dict__ — saves ~40% memory</span>
<span class="kw">class</span> <span class="tp">TokenSlotted</span>:
    __slots__ = (<span class="st">'id'</span>, <span class="st">'text'</span>, <span class="st">'logprob'</span>)
    <span class="kw">def</span> <span class="fn">__init__</span>(self, id, text, logprob):
        self.id = id; self.text = text; self.logprob = logprob

<span class="kw">class</span> <span class="tp">TokenDict</span>:
    <span class="kw">def</span> <span class="fn">__init__</span>(self, id, text, logprob):
        self.id = id; self.text = text; self.logprob = logprob

s = <span class="tp">TokenSlotted</span>(<span class="nb">1</span>, <span class="st">"hello"</span>, <span class="nb">-0.5</span>)
d = <span class="tp">TokenDict</span>(<span class="nb">1</span>, <span class="st">"hello"</span>, <span class="nb">-0.5</span>)
<span class="nb">print</span>(<span class="st">f"Slotted: </span><span class="nb">{sys.getsizeof(s)}</span><span class="st"> bytes"</span>)    <span class="cm"># ~56 bytes</span>
<span class="nb">print</span>(<span class="st">f"Dict:    </span><span class="nb">{sys.getsizeof(d)}</span><span class="st"> bytes"</span>)    <span class="cm"># ~232 bytes</span>
<span class="cm"># For 1M tokens: saves ~176MB RAM</span>

<span class="cm"># weakref: cache without preventing garbage collection</span>
<span class="kw">import</span> weakref

<span class="kw">class</span> <span class="tp">EmbeddingCache</span>:
    <span class="kw">def</span> <span class="fn">__init__</span>(self):
        self._cache: <span class="tp">dict</span>[<span class="tp">str</span>, weakref.ref] = {}

    <span class="kw">def</span> <span class="fn">put</span>(self, key: <span class="tp">str</span>, arr):
        self._cache[key] = weakref.ref(arr)

    <span class="kw">def</span> <span class="fn">get</span>(self, key: <span class="tp">str</span>):
        ref = self._cache.get(key)
        <span class="kw">return</span> ref() <span class="kw">if</span> ref <span class="kw">else</span> <span class="nb">None</span>
        <span class="cm"># Returns None if the array was garbage-collected</span>

<span class="cm"># tracemalloc: find exactly what's consuming memory</span>
<span class="kw">import</span> tracemalloc
tracemalloc.start()

<span class="kw">import</span> numpy <span class="kw">as</span> np
embeddings = np.random.randn(<span class="nb">10_000</span>, <span class="nb">1536</span>).astype(np.float32)  <span class="cm"># 60MB</span>

snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics(<span class="st">"lineno"</span>)
<span class="nb">print</span>(<span class="st">f"Top allocation: </span><span class="nb">{top_stats[0].size / 1e6:.1f}</span><span class="st">MB"</span>)
</pre>
  </div>

  <hr class="divider">

  <!-- ─────────────────────────────────────────── -->
  <h2 id="s9"><span class="section-num">Section 09</span>Advanced Patterns — Metaclasses, Descriptors, Dunders</h2>

  <p>These are the techniques used inside the frameworks you use every day. Understanding them lets you write code that feels like a framework — extensible, expressive, and self-documenting.</p>

  <h3>Metaclasses: auto-registering model providers</h3>

  <div class="code-block">
    <div class="code-label"><div class="dot-red"></div><div class="dot-yel"></div><div class="dot-grn"></div><span class="filename">model_registry.py</span></div>
    <pre><span class="kw">class</span> <span class="tp">ModelRegistry</span>(type):
    <span class="st">"""Every subclass with a model_id gets registered automatically."""</span>
    _registry: <span class="tp">dict</span>[<span class="tp">str</span>, type] = {}

    <span class="kw">def</span> <span class="fn">__new__</span>(mcs, name, bases, ns):
        cls = <span class="nb">super</span>().__new__(mcs, name, bases, ns)
        <span class="kw">if</span> <span class="st">"model_id"</span> <span class="kw">in</span> ns:
            mcs._registry[ns[<span class="st">"model_id"</span>]] = cls
        <span class="kw">return</span> cls

    <span class="dc">@classmethod</span>
    <span class="kw">def</span> <span class="fn">get</span>(mcs, model_id: <span class="tp">str</span>) -> type:
        <span class="kw">if</span> model_id <span class="kw">not in</span> mcs._registry:
            <span class="kw">raise</span> <span class="tp">KeyError</span>(<span class="st">f"Unknown: </span><span class="nb">{model_id}</span><span class="st">. Options: </span><span class="nb">{list(mcs._registry)}</span><span class="st">"</span>)
        <span class="kw">return</span> mcs._registry[model_id]

<span class="kw">class</span> <span class="tp">BaseProvider</span>(metaclass=<span class="tp">ModelRegistry</span>): pass

<span class="kw">class</span> <span class="tp">ClaudeProvider</span>(<span class="tp">BaseProvider</span>):
    model_id = <span class="st">"claude-opus-4-5"</span>
    <span class="kw">async def</span> <span class="fn">generate</span>(self, prompt): ...   <span class="cm"># auto-registered on class creation</span>

<span class="kw">class</span> <span class="tp">GPT4Provider</span>(<span class="tp">BaseProvider</span>):
    model_id = <span class="st">"gpt-4o"</span>
    <span class="kw">async def</span> <span class="fn">generate</span>(self, prompt): ...   <span class="cm"># auto-registered on class creation</span>

<span class="cm"># Dynamic selection from config — no if/elif chains</span>
provider = ModelRegistry.get(<span class="st">"claude-opus-4-5"</span>)()
</pre>
  </div>

  <h3>Dunder methods: pipelines with the <code>|</code> operator</h3>

  <div class="code-block">
    <div class="code-label"><div class="dot-red"></div><div class="dot-yel"></div><div class="dot-grn"></div><span class="filename">pipeline_dsl.py</span></div>
    <pre><span class="kw">from</span> __future__ <span class="kw">import</span> annotations
<span class="kw">from</span> typing <span class="kw">import</span> Callable, Any

<span class="kw">class</span> <span class="tp">Step</span>:
    <span class="kw">def</span> <span class="fn">__init__</span>(self, fn: <span class="tp">Callable</span>, name=<span class="st">""</span>):
        self.fn   = fn
        self.name = name <span class="kw">or</span> fn.__name__

    <span class="kw">def</span> <span class="fn">__call__</span>(self, data: <span class="tp">Any</span>) -> <span class="tp">Any</span>:
        <span class="kw">return</span> self.fn(data)

    <span class="kw">def</span> <span class="fn">__or__</span>(self, other: <span class="tp">Step</span>) -> <span class="tp">Step</span>:
        <span class="cm"># step1 | step2 → a new step that chains both</span>
        <span class="kw">def</span> <span class="fn">chained</span>(data):
            <span class="kw">return</span> <span class="fn">other</span>(self(data))
        <span class="kw">return</span> <span class="tp">Step</span>(chained, <span class="st">f"</span><span class="nb">{self.name}</span><span class="st">|</span><span class="nb">{other.name}</span><span class="st">"</span>)

    <span class="kw">def</span> <span class="fn">__repr__</span>(self): <span class="kw">return</span> <span class="st">f"Step(</span><span class="nb">{self.name!r}</span><span class="st">)"</span>

<span class="cm"># Define individual steps</span>
strip    = <span class="tp">Step</span>(str.strip,           <span class="st">"strip"</span>)
lower    = <span class="tp">Step</span>(str.lower,           <span class="st">"lower"</span>)
tokenise = <span class="tp">Step</span>(str.split,           <span class="st">"tokenise"</span>)
count    = <span class="tp">Step</span>(<span class="nb">len</span>,                 <span class="st">"count"</span>)

<span class="cm"># Compose with | — reads like Unix pipes</span>
preprocess = strip | lower | tokenise | count

<span class="nb">print</span>(preprocess(<span class="st">"  Hello World from GenAI!  "</span>))  <span class="cm"># 4</span>
<span class="nb">print</span>(<span class="nb">repr</span>(preprocess))   <span class="cm"># Step('strip|lower|tokenise|count')</span>
</pre>
  </div>

  <hr class="divider">

  <!-- ─────────────────────────────────────────── -->
  <h2 id="s10"><span class="section-num">Section 10</span>Production Patterns — Rate Limiting, Retries, Supervisors</h2>

  <p>This is where theory meets the real world. LLM APIs have rate limits. Workers crash. Tasks fail. Production AI systems need to handle all of this gracefully — not just in the happy path.</p>

  <h3>Async rate limiter with token bucket</h3>

  <div class="code-block">
    <div class="code-label"><div class="dot-red"></div><div class="dot-yel"></div><div class="dot-grn"></div><span class="filename">rate_limiter.py</span></div>
    <pre><span class="kw">import</span> asyncio, time
<span class="kw">from</span> collections <span class="kw">import</span> deque

<span class="kw">class</span> <span class="tp">RateLimiter</span>:
    <span class="st">"""Token-bucket rate limiter: max N calls per M seconds."""</span>
    <span class="kw">def</span> <span class="fn">__init__</span>(self, max_calls: <span class="tp">int</span>, period: <span class="tp">float</span> = <span class="nb">60.0</span>):
        self.max_calls = max_calls
        self.period    = period
        self._calls:   <span class="tp">deque</span>[<span class="tp">float</span>] = deque()
        self._lock     = asyncio.Lock()

    <span class="kw">async def</span> <span class="fn">acquire</span>(self):
        <span class="kw">async with</span> self._lock:
            now = time.monotonic()
            <span class="kw">while</span> self._calls <span class="kw">and</span> now - self._calls[<span class="nb">0</span>] > self.period:
                self._calls.popleft()
            <span class="kw">if</span> <span class="nb">len</span>(self._calls) >= self.max_calls:
                wait = self.period - (now - self._calls[<span class="nb">0</span>])
                <span class="kw">await</span> asyncio.sleep(wait)
            self._calls.append(time.monotonic())

    <span class="kw">async def</span> <span class="fn">__aenter__</span>(self): <span class="kw">await</span> self.acquire(); <span class="kw">return</span> self
    <span class="kw">async def</span> <span class="fn">__aexit__</span>(self, *_): <span class="kw">pass</span>

<span class="cm"># 60 RPM cap, max 10 simultaneous connections</span>
limiter = <span class="tp">RateLimiter</span>(max_calls=<span class="nb">60</span>, period=<span class="nb">60.0</span>)
sem     = asyncio.Semaphore(<span class="nb">10</span>)

<span class="kw">async def</span> <span class="fn">safe_llm_call</span>(prompt: <span class="tp">str</span>, idx: <span class="tp">int</span>) -> <span class="tp">str</span>:
    <span class="kw">async with</span> sem:         <span class="cm"># cap concurrency</span>
        <span class="kw">async with</span> limiter: <span class="cm"># cap rate</span>
            <span class="kw">await</span> asyncio.sleep(<span class="nb">0.5</span>)
            <span class="kw">return</span> <span class="st">f"[</span><span class="nb">{idx}</span><span class="st">] response"</span>

<span class="kw">async def</span> <span class="fn">process</span>(prompts: <span class="tp">list</span>[<span class="tp">str</span>]) -> <span class="tp">list</span>[<span class="tp">str</span>]:
    tasks = [<span class="fn">safe_llm_call</span>(p, i) <span class="kw">for</span> i, p <span class="kw">in</span> <span class="nb">enumerate</span>(prompts)]
    <span class="kw">return await</span> asyncio.gather(*tasks)
</pre>
  </div>

  <h3>Mixing asyncio + multiprocessing for hybrid workloads</h3>

  <div class="code-block">
    <div class="code-label"><div class="dot-red"></div><div class="dot-yel"></div><div class="dot-grn"></div><span class="filename">hybrid_pipeline.py</span></div>
    <pre><span class="kw">import</span> asyncio
<span class="kw">from</span> concurrent.futures <span class="kw">import</span> ProcessPoolExecutor
<span class="kw">import</span> numpy <span class="kw">as</span> np

<span class="kw">def</span> <span class="fn">cpu_similarity</span>(embeddings: <span class="tp">list</span>[<span class="tp">list</span>[<span class="tp">float</span>]]) -> <span class="tp">list</span>[<span class="tp">list</span>[<span class="tp">float</span>]]:
    <span class="st">"""CPU-bound work — runs in a separate process, bypasses GIL."""</span>
    arr  = np.array(embeddings, dtype=np.float32)
    norm = arr / (np.linalg.norm(arr, axis=<span class="nb">1</span>, keepdims=<span class="nb">True</span>) + <span class="nb">1e-8</span>)
    <span class="kw">return</span> (norm @ norm.T).tolist()

<span class="kw">async def</span> <span class="fn">full_pipeline</span>(texts: <span class="tp">list</span>[<span class="tp">str</span>]) -> <span class="tp">list</span>[<span class="tp">list</span>[<span class="tp">float</span>]]:
    loop = asyncio.get_running_loop()

    <span class="cm"># Phase 1: I/O-bound — async embedding fetch</span>
    embeddings = <span class="kw">await</span> <span class="fn">fetch_embeddings_async</span>(texts)

    <span class="cm"># Phase 2: CPU-bound — offload to process pool (non-blocking!)</span>
    <span class="kw">with</span> ProcessPoolExecutor(max_workers=<span class="nb">4</span>) <span class="kw">as</span> pool:
        sim_matrix = <span class="kw">await</span> loop.run_in_executor(
            pool, <span class="fn">cpu_similarity</span>, embeddings
        )
    <span class="kw">return</span> sim_matrix

<span class="cm"># run_in_executor bridges asyncio and multiprocessing cleanly:</span>
<span class="cm"># - the event loop remains unblocked during CPU work</span>
<span class="cm"># - CPU uses all available cores</span>
<span class="cm"># - result is awaited naturally</span>
</pre>
  </div>

  <hr class="divider">

  <!-- ─────────────────────────────────────────── -->
  <h2 id="s11"><span class="section-num">Section 11</span>Quick Reference</h2>

  <div class="table-wrap">
    <table>
      <thead>
        <tr><th>Scenario</th><th>Python Tool</th><th>Key Detail</th></tr>
      </thead>
      <tbody>
        <tr><td>Concurrent LLM API calls</td><td>asyncio.gather()</td><td>Total time ≈ slowest single call</td></tr>
        <tr><td>Streaming tokens to UI</td><td>async generators + async for</td><td>Yield each token, never buffer full response</td></tr>
        <tr><td>Parallel embedding (blocking lib)</td><td>ThreadPoolExecutor</td><td>GIL released during C extension compute</td></tr>
        <tr><td>Tokenising millions of docs</td><td>ProcessPoolExecutor + initializer</td><td>One tokenizer init per worker process</td></tr>
        <tr><td>Multi-GB training data</td><td>Generator pipelines</td><td>O(batch_size) memory regardless of file size</td></tr>
        <tr><td>Embedding API caching</td><td>@lru_cache (sync) / dict+Lock (async)</td><td>Cache key = hash(text + model)</td></tr>
        <tr><td>LLM rate limiting</td><td>RateLimiter + asyncio.Semaphore</td><td>Respect both RPM and concurrent-request limits</td></tr>
        <tr><td>Structured LLM outputs</td><td>Pydantic BaseModel</td><td>Validate JSON from LLM before using it</td></tr>
        <tr><td>Retry on API errors</td><td>@retry decorator + exponential backoff</td><td>Add jitter to avoid thundering herd</td></tr>
        <tr><td>Resource cleanup on error</td><td>@contextmanager / ExitStack</td><td>finally block always runs</td></tr>
        <tr><td>Backend-agnostic components</td><td>Protocol + Generic TypeVar</td><td>Swap providers without changing pipeline</td></tr>
        <tr><td>Large embedding matrices</td><td>shared_memory + numpy</td><td>Zero-copy between processes</td></tr>
        <tr><td>Mixed I/O + CPU pipeline</td><td>asyncio + run_in_executor(ProcessPool)</td><td>Best of both: async I/O + true CPU parallel</td></tr>
        <tr><td>Dynamic model provider selection</td><td>Metaclass registry</td><td>Auto-register on class definition</td></tr>
        <tr><td>Memory-heavy token objects</td><td>__slots__ or NamedTuple</td><td>~40–70% smaller than regular class instances</td></tr>
        <tr><td>Finding memory leaks</td><td>tracemalloc + gc.collect()</td><td>Profile before optimising</td></tr>
      </tbody>
    </table>
  </div>

  <hr class="divider">

  <div class="article-footer">
    <h3>That's the full picture.</h3>
    <p>Every concept here connects directly to a problem you'll hit building real GenAI systems. Bookmark it, copy the examples, and adapt them — that's what they're here for.</p>
  </div>

</article>
</div>

</body>
</html>
