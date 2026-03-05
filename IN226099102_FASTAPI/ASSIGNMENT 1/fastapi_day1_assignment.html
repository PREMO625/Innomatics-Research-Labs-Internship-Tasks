<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>FastAPI — Day 1 Assignment</title>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@300;400;500;600;700;900&display=swap" rel="stylesheet">
<style>
:root {
  --bg:#0a0e1a; --surface:#111827; --surface2:#1f2937;
  --border:#2d3748; --text:#e2e8f0; --dim:#64748b;
  --green:#10b981; --blue:#3b82f6; --yellow:#f59e0b;
  --red:#ef4444; --purple:#8b5cf6; --cyan:#06b6d4;
}
* { margin:0; padding:0; box-sizing:border-box; }
body { background:var(--bg); color:var(--text); font-family:'Inter',sans-serif; padding:40px 24px 80px; }

.page { max-width:820px; margin:0 auto; }

/* Header */
.header {
  text-align:center; padding:48px 32px;
  background:linear-gradient(135deg,#0f172a,#1e1b4b,#0f172a);
  border-radius:20px; margin-bottom:36px;
  border:1px solid #2d3748; position:relative; overflow:hidden;
}
.header::before {
  content:''; position:absolute; top:-60%; right:-10%;
  width:400px; height:400px; border-radius:50%;
  background:radial-gradient(circle,rgba(59,130,246,.07),transparent 70%);
}
.header-tag {
  display:inline-flex; align-items:center; gap:6px;
  padding:5px 14px; border-radius:20px; font-size:12px; font-weight:700;
  background:rgba(59,130,246,.15); border:1px solid rgba(59,130,246,.3);
  color:#93c5fd; margin-bottom:18px; letter-spacing:1px;
}
.header h1 {
  font-size:clamp(26px,4vw,42px); font-weight:900; line-height:1.2;
  background:linear-gradient(135deg,#fff,#93c5fd,#6ee7b7);
  -webkit-background-clip:text; -webkit-text-fill-color:transparent;
  margin-bottom:10px;
}
.header-desc { color:#94a3b8; font-size:15px; max-width:500px; margin:0 auto 20px; }
.header-pills { display:flex; gap:10px; justify-content:center; flex-wrap:wrap; }
.pill {
  padding:5px 14px; border-radius:20px; font-size:12px; font-weight:600;
  display:flex; align-items:center; gap:5px; border:1px solid;
}
.pill.blue  { background:rgba(59,130,246,.1); border-color:rgba(59,130,246,.3); color:#93c5fd; }
.pill.green { background:rgba(16,185,129,.1); border-color:rgba(16,185,129,.3); color:#6ee7b7; }
.pill.yellow{ background:rgba(245,158,11,.1); border-color:rgba(245,158,11,.3); color:#fcd34d; }
.pill.purple{ background:rgba(139,92,246,.1); border-color:rgba(139,92,246,.3); color:#c4b5fd; }

/* Rules box */
.rules-box {
  background:rgba(245,158,11,.06); border:1px solid rgba(245,158,11,.25);
  border-radius:14px; padding:20px 24px; margin-bottom:32px;
  display:flex; gap:14px;
}
.rules-icon { font-size:24px; flex-shrink:0; }
.rules-body h3 { font-size:15px; font-weight:700; color:#fcd34d; margin-bottom:8px; }
.rules-body ul { list-style:none; display:flex; flex-direction:column; gap:5px; }
.rules-body li { font-size:13px; color:#94a3b8; display:flex; align-items:flex-start; gap:8px; }
.rules-body li::before { content:'→'; color:#f59e0b; flex-shrink:0; margin-top:1px; }

/* Question cards */
.q-card {
  background:var(--surface); border:1px solid var(--border);
  border-radius:18px; margin-bottom:24px; overflow:hidden;
  transition:border-color .3s;
}
.q-card:hover { border-color:#3b82f6; }

.q-header {
  padding:22px 26px; display:flex; align-items:flex-start; gap:16px;
  border-bottom:1px solid var(--border);
}
.q-badge {
  display:flex; flex-direction:column; align-items:center; gap:4px;
  flex-shrink:0;
}
.q-num {
  width:44px; height:44px; border-radius:12px;
  display:flex; align-items:center; justify-content:center;
  font-family:'JetBrains Mono',monospace; font-weight:900; font-size:18px; color:#fff;
}
.q-num.q1 { background:linear-gradient(135deg,#10b981,#06b6d4); }
.q-num.q2 { background:linear-gradient(135deg,#3b82f6,#8b5cf6); }
.q-num.q3 { background:linear-gradient(135deg,#f59e0b,#ef4444); }
.q-num.q4 { background:linear-gradient(135deg,#ec4899,#f97316); }
.q-num.q5 { background:linear-gradient(135deg,#8b5cf6,#06b6d4); }

.difficulty {
  font-size:9px; font-weight:700; letter-spacing:1px;
  padding:2px 8px; border-radius:10px; text-transform:uppercase;
}
.diff-easy   { background:rgba(16,185,129,.15);  color:#10b981; border:1px solid rgba(16,185,129,.3);  }
.diff-medium { background:rgba(245,158,11,.15);  color:#f59e0b; border:1px solid rgba(245,158,11,.3);  }
.diff-hard   { background:rgba(239,68,68,.15);   color:#ef4444; border:1px solid rgba(239,68,68,.3);   }
.diff-bonus  { background:rgba(139,92,246,.15);  color:#8b5cf6; border:1px solid rgba(139,92,246,.3);  }

.q-title-wrap { flex:1; }
.q-title { font-size:17px; font-weight:800; color:#fff; margin-bottom:4px; }
.q-scenario {
  font-size:13px; color:#94a3b8; line-height:1.6;
  background:rgba(59,130,246,.05); border:1px solid rgba(59,130,246,.15);
  border-radius:8px; padding:10px 14px; margin-top:10px;
  font-style:italic;
}
.q-scenario strong { color:#93c5fd; font-style:normal; }

.q-body { padding:22px 26px; }
.task-label {
  font-size:10px; font-weight:700; letter-spacing:2px; text-transform:uppercase;
  color:var(--dim); margin-bottom:10px;
}
.task-list { display:flex; flex-direction:column; gap:8px; margin-bottom:18px; }
.task-item {
  display:flex; align-items:flex-start; gap:10px;
  padding:10px 14px; border-radius:10px;
  background:var(--surface2); border:1px solid var(--border);
  font-size:13px; line-height:1.6;
}
.task-item .t-icon { font-size:16px; flex-shrink:0; margin-top:1px; }
.task-item p { color:var(--text); }
.task-item code {
  font-family:'JetBrains Mono',monospace; font-size:11px;
  background:#0d1117; border:1px solid var(--border);
  padding:1px 6px; border-radius:4px; color:#38bdf8;
}

/* Hint box */
.hint-toggle {
  display:flex; align-items:center; gap:8px; cursor:pointer;
  padding:8px 14px; border-radius:8px; width:fit-content;
  background:rgba(139,92,246,.08); border:1px solid rgba(139,92,246,.2);
  color:#c4b5fd; font-size:12px; font-weight:600;
  transition:background .2s; margin-bottom:0;
  user-select:none;
}
.hint-toggle:hover { background:rgba(139,92,246,.15); }
.hint-box {
  display:none; margin-top:12px;
  background:#0d1117; border:1px solid rgba(139,92,246,.25);
  border-radius:10px; overflow:hidden;
}
.hint-box.open { display:block; }
.hint-header {
  padding:8px 16px; background:rgba(139,92,246,.1);
  font-size:10px; font-weight:700; letter-spacing:2px;
  text-transform:uppercase; color:#c4b5fd;
  border-bottom:1px solid rgba(139,92,246,.2);
}
.hint-code {
  padding:16px; font-family:'JetBrains Mono',monospace;
  font-size:12px; line-height:1.8; color:#e2e8f0; overflow-x:auto;
}
.kw{color:#ff7b72;} .fn{color:#d2a8ff;} .str{color:#a5d6ff;}
.cm{color:#8b949e;font-style:italic;} .dec{color:#79c0ff;} .num{color:#f2cc60;}

/* Expected output */
.expected {
  margin-top:14px; background:#0d1117;
  border:1px solid rgba(16,185,129,.2); border-radius:10px; overflow:hidden;
}
.expected-header {
  padding:7px 16px; background:rgba(16,185,129,.08);
  font-size:10px; font-weight:700; letter-spacing:2px;
  text-transform:uppercase; color:#10b981;
  border-bottom:1px solid rgba(16,185,129,.2);
  display:flex; justify-content:space-between; align-items:center;
}
.expected-code {
  padding:14px 16px; font-family:'JetBrains Mono',monospace;
  font-size:12px; line-height:1.8; color:#e2e8f0;
}
.j-key{color:#93c5fd;} .j-str{color:#86efac;} .j-num{color:#fcd34d;}
.j-bool{color:#34d399;} .j-brace{color:#94a3b8;}

/* Test URLs */
.test-urls { margin-top:14px; display:flex; flex-direction:column; gap:6px; }
.test-url {
  display:flex; align-items:center; gap:10px;
  padding:8px 14px; border-radius:8px;
  background:var(--surface2); border:1px solid var(--border);
  font-family:'JetBrains Mono',monospace; font-size:12px;
}
.get-badge {
  padding:2px 8px; border-radius:5px; font-size:10px; font-weight:800;
  background:rgba(16,185,129,.15); border:1px solid rgba(16,185,129,.4); color:#10b981;
  flex-shrink:0;
}
.url-text { color:#38bdf8; flex:1; }
.url-note { font-size:11px; color:var(--dim); font-family:'Inter',sans-serif; }

/* Submission checklist */
.submit-box {
  background:linear-gradient(135deg,rgba(16,185,129,.06),rgba(59,130,246,.06));
  border:1px solid rgba(16,185,129,.25); border-radius:16px;
  padding:24px 28px; margin-top:36px;
}
.submit-box h3 { font-size:17px; font-weight:800; color:#fff; margin-bottom:16px; display:flex; align-items:center; gap:8px; }
.submit-list { display:flex; flex-direction:column; gap:8px; }
.submit-item {
  display:flex; align-items:center; gap:12px;
  padding:10px 16px; border-radius:10px;
  background:rgba(255,255,255,.03); border:1px solid var(--border);
  font-size:13px; cursor:pointer; transition:all .2s;
}
.submit-item:hover { border-color:var(--green); }
.submit-item.checked { background:rgba(16,185,129,.06); border-color:rgba(16,185,129,.3); }
.s-box {
  width:20px; height:20px; border-radius:5px;
  border:2px solid var(--border); display:flex; align-items:center; justify-content:center;
  font-size:12px; flex-shrink:0; transition:all .2s;
}
.submit-item.checked .s-box { background:var(--green); border-color:var(--green); color:#fff; }
.submit-item.checked span { text-decoration:line-through; color:var(--dim); }

/* Footer */
.footer {
  text-align:center; margin-top:48px; padding:24px;
  border-top:1px solid var(--border); color:var(--dim); font-size:13px;
}
.footer strong { color:var(--cyan); }
</style>
</head>
<body>
<div class="page">

  <!-- Header -->
  <div class="header">
    <div class="header-tag">📝 ASSIGNMENT</div>
    <h1>FastAPI — Day 1<br>Practice Tasks</h1>
    <p class="header-desc">Complete these tasks before Day 2. Build on top of what you learned today.</p>
    <div class="header-pills">
      <div class="pill blue">⏱ 45–60 min</div>
      <div class="pill green">5 Questions</div>
      <div class="pill yellow">🛠 Hands-On</div>
      <div class="pill purple">⭐ 1 Bonus</div>
    </div>
  </div>

  <!-- Rules -->
  <div class="rules-box">
    <div class="rules-icon">📌</div>
    <div class="rules-body">
      <h3>Rules & Instructions</h3>
      <ul>
        <li>All tasks must be done in the same <code style="font-family:'JetBrains Mono';font-size:11px;background:#0d1117;border:1px solid #2d3748;padding:1px 6px;border-radius:4px;color:#38bdf8">main.py</code> file you created today</li>
        <li>Server must be running and all URLs must work in browser</li>
        <li>Test every endpoint in Swagger UI at <code style="font-family:'JetBrains Mono';font-size:11px;background:#0d1117;border:1px solid #2d3748;padding:1px 6px;border-radius:4px;color:#38bdf8">http://127.0.0.1:8000/docs</code></li>
        <li>Take a screenshot of your browser showing the output for each task</li>
        <li>Don't copy from each other — try yourself first, use the hints only if stuck</li>
      </ul>
    </div>
  </div>

  <!-- ── Q1 ── -->
  <div class="q-card">
    <div class="q-header">
      <div class="q-badge">
        <div class="q-num q1">1</div>
        <span class="difficulty diff-easy">Easy</span>
      </div>
      <div class="q-title-wrap">
        <div class="q-title">Add 3 More Products</div>
        <div class="q-scenario">
          <strong>Scenario:</strong> Your client just added 3 new items to their store — a Laptop Stand, a Mechanical Keyboard, and a Webcam. The mobile app needs to show them. Add these to your products list.
        </div>
      </div>
    </div>
    <div class="q-body">
      <div class="task-label">Your Tasks</div>
      <div class="task-list">
        <div class="task-item">
          <span class="t-icon">➕</span>
          <p>Add 3 new products to the <code>products</code> list in <code>main.py</code> with IDs 5, 6, 7</p>
        </div>
        <div class="task-item">
          <span class="t-icon">✅</span>
          <p>Each product must have: <code>id</code>, <code>name</code>, <code>price</code>, <code>category</code>, <code>in_stock</code></p>
        </div>
        <div class="task-item">
          <span class="t-icon">🔍</span>
          <p>Visit <code>/products</code> — confirm total now shows <code>7</code> instead of <code>4</code></p>
        </div>
      </div>
      <div class="expected">
        <div class="expected-header">Expected Output at /products</div>
        <div class="expected-code"><span class="j-brace">{</span> <span class="j-key">"products"</span>: [...], <span class="j-key">"total"</span>: <span class="j-num">7</span> <span class="j-brace">}</span></div>
      </div>
      <div style="margin-top:14px;">
        <div class="hint-toggle" onclick="toggleHint('h1')">💡 Show Hint</div>
        <div class="hint-box" id="h1">
          <div class="hint-header">Hint — Add this inside the products list</div>
          <div class="hint-code"><span class="cm"># Add these inside the products = [ ... ] list</span>
{<span class="str">"id"</span>: <span class="num">5</span>, <span class="str">"name"</span>: <span class="str">"Laptop Stand"</span>, <span class="str">"price"</span>: <span class="num">1299</span>, <span class="str">"category"</span>: <span class="str">"Electronics"</span>, <span class="str">"in_stock"</span>: <span class="kw">True</span>},
{<span class="str">"id"</span>: <span class="num">6</span>, <span class="str">"name"</span>: <span class="str">"Mechanical Keyboard"</span>, <span class="str">"price"</span>: <span class="num">2499</span>, <span class="str">"category"</span>: <span class="str">"Electronics"</span>, <span class="str">"in_stock"</span>: <span class="kw">True</span>},
{<span class="str">"id"</span>: <span class="num">7</span>, <span class="str">"name"</span>: <span class="str">"Webcam"</span>, <span class="str">"price"</span>: <span class="num">1899</span>, <span class="str">"category"</span>: <span class="str">"Electronics"</span>, <span class="str">"in_stock"</span>: <span class="kw">False</span>},</div>
        </div>
      </div>
    </div>
  </div>

  <!-- ── Q2 ── -->
  <div class="q-card">
    <div class="q-header">
      <div class="q-badge">
        <div class="q-num q2">2</div>
        <span class="difficulty diff-easy">Easy</span>
      </div>
      <div class="q-title-wrap">
        <div class="q-title">Add a Category Filter Endpoint</div>
        <div class="q-scenario">
          <strong>Scenario:</strong> The mobile app wants to show only Electronics on one page and only Stationery on another. You need a new endpoint that filters products by category.
        </div>
      </div>
    </div>
    <div class="q-body">
      <div class="task-label">Your Tasks</div>
      <div class="task-list">
        <div class="task-item">
          <span class="t-icon">🔧</span>
          <p>Create a new endpoint: <code>GET /products/category/{category_name}</code></p>
        </div>
        <div class="task-item">
          <span class="t-icon">🔍</span>
          <p>It should return only products where <code>category</code> matches the given name</p>
        </div>
        <div class="task-item">
          <span class="t-icon">⚠️</span>
          <p>If no products found for that category, return <code>{"error": "No products found in this category"}</code></p>
        </div>
      </div>
      <div class="test-urls">
        <div class="task-label" style="margin-bottom:6px">Test These URLs</div>
        <div class="test-url"><span class="get-badge">GET</span><span class="url-text">/products/category/Electronics</span><span class="url-note">→ shows only Electronics</span></div>
        <div class="test-url"><span class="get-badge">GET</span><span class="url-text">/products/category/Stationery</span><span class="url-note">→ shows only Stationery</span></div>
        <div class="test-url"><span class="get-badge">GET</span><span class="url-text">/products/category/Furniture</span><span class="url-note">→ shows error message</span></div>
      </div>
      <div style="margin-top:14px;">
        <div class="hint-toggle" onclick="toggleHint('h2')">💡 Show Hint</div>
        <div class="hint-box" id="h2">
          <div class="hint-header">Hint — Structure of the new endpoint</div>
          <div class="hint-code"><span class="dec">@app.get</span>(<span class="str">"/products/category/{category_name}"</span>)
<span class="kw">def</span> <span class="fn">get_by_category</span>(category_name: <span class="fn">str</span>):
    result = [p <span class="kw">for</span> p <span class="kw">in</span> products <span class="kw">if</span> p[<span class="str">"category"</span>] == category_name]
    <span class="kw">if not</span> result:
        <span class="kw">return</span> {<span class="str">"error"</span>: <span class="str">"No products found in this category"</span>}
    <span class="kw">return</span> {<span class="str">"category"</span>: category_name, <span class="str">"products"</span>: result, <span class="str">"total"</span>: <span class="fn">len</span>(result)}</div>
        </div>
      </div>
    </div>
  </div>

  <!-- ── Q3 ── -->
  <div class="q-card">
    <div class="q-header">
      <div class="q-badge">
        <div class="q-num q3">3</div>
        <span class="difficulty diff-medium">Medium</span>
      </div>
      <div class="q-title-wrap">
        <div class="q-title">Show Only In-Stock Products</div>
        <div class="q-scenario">
          <strong>Scenario:</strong> Customers are complaining they can see products that are out of stock and then get disappointed. The app team wants a separate endpoint that returns ONLY available products.
        </div>
      </div>
    </div>
    <div class="q-body">
      <div class="task-label">Your Tasks</div>
      <div class="task-list">
        <div class="task-item">
          <span class="t-icon">🔧</span>
          <p>Create endpoint: <code>GET /products/instock</code></p>
        </div>
        <div class="task-item">
          <span class="t-icon">✅</span>
          <p>Return only products where <code>in_stock</code> is <code>True</code></p>
        </div>
        <div class="task-item">
          <span class="t-icon">📊</span>
          <p>Also return a count of how many in-stock products there are</p>
        </div>
      </div>
      <div class="expected">
        <div class="expected-header">Expected Output at /products/instock</div>
        <div class="expected-code"><span class="j-brace">{</span>
  <span class="j-key">"in_stock_products"</span>: [<span class="cm">...only in_stock: true items...</span>],
  <span class="j-key">"count"</span>: <span class="j-num">5</span>  <span class="cm">← depends on how many you have</span>
<span class="j-brace">}</span></div>
      </div>
      <div style="margin-top:14px;">
        <div class="hint-toggle" onclick="toggleHint('h3')">💡 Show Hint</div>
        <div class="hint-box" id="h3">
          <div class="hint-header">Hint</div>
          <div class="hint-code"><span class="dec">@app.get</span>(<span class="str">"/products/instock"</span>)
<span class="kw">def</span> <span class="fn">get_instock</span>():
    available = [p <span class="kw">for</span> p <span class="kw">in</span> products <span class="kw">if</span> p[<span class="str">"in_stock"</span>] == <span class="kw">True</span>]
    <span class="kw">return</span> {<span class="str">"in_stock_products"</span>: available, <span class="str">"count"</span>: <span class="fn">len</span>(available)}</div>
        </div>
      </div>
    </div>
  </div>

  <!-- ── Q4 ── -->
  <div class="q-card">
    <div class="q-header">
      <div class="q-badge">
        <div class="q-num q4">4</div>
        <span class="difficulty diff-medium">Medium</span>
      </div>
      <div class="q-title-wrap">
        <div class="q-title">Build a Store Info Endpoint</div>
        <div class="q-scenario">
          <strong>Scenario:</strong> The mobile app's home screen needs to show a summary of the store — total products, how many are in stock, and all available categories. Build one endpoint that returns all of this.
        </div>
      </div>
    </div>
    <div class="q-body">
      <div class="task-label">Your Tasks</div>
      <div class="task-list">
        <div class="task-item">
          <span class="t-icon">🔧</span>
          <p>Create endpoint: <code>GET /store/summary</code></p>
        </div>
        <div class="task-item">
          <span class="t-icon">📊</span>
          <p>Return: total products count, in-stock count, out-of-stock count</p>
        </div>
        <div class="task-item">
          <span class="t-icon">📋</span>
          <p>Also return a list of unique categories available in the store</p>
        </div>
      </div>
      <div class="expected">
        <div class="expected-header">Expected Output at /store/summary</div>
        <div class="expected-code"><span class="j-brace">{</span>
  <span class="j-key">"store_name"</span>: <span class="j-str">"My E-commerce Store"</span>,
  <span class="j-key">"total_products"</span>: <span class="j-num">7</span>,
  <span class="j-key">"in_stock"</span>: <span class="j-num">5</span>,
  <span class="j-key">"out_of_stock"</span>: <span class="j-num">2</span>,
  <span class="j-key">"categories"</span>: [<span class="j-str">"Electronics"</span>, <span class="j-str">"Stationery"</span>]
<span class="j-brace">}</span></div>
      </div>
      <div style="margin-top:14px;">
        <div class="hint-toggle" onclick="toggleHint('h4')">💡 Show Hint</div>
        <div class="hint-box" id="h4">
          <div class="hint-header">Hint</div>
          <div class="hint-code"><span class="dec">@app.get</span>(<span class="str">"/store/summary"</span>)
<span class="kw">def</span> <span class="fn">store_summary</span>():
    in_stock_count  = <span class="fn">len</span>([p <span class="kw">for</span> p <span class="kw">in</span> products <span class="kw">if</span> p[<span class="str">"in_stock"</span>]])
    out_stock_count = <span class="fn">len</span>(products) - in_stock_count
    categories      = <span class="fn">list</span>(<span class="fn">set</span>([p[<span class="str">"category"</span>] <span class="kw">for</span> p <span class="kw">in</span> products]))
    <span class="kw">return</span> {
        <span class="str">"store_name"</span>:     <span class="str">"My E-commerce Store"</span>,
        <span class="str">"total_products"</span>: <span class="fn">len</span>(products),
        <span class="str">"in_stock"</span>:       in_stock_count,
        <span class="str">"out_of_stock"</span>:   out_stock_count,
        <span class="str">"categories"</span>:     categories,
    }</div>
        </div>
      </div>
    </div>
  </div>

  <!-- ── Q5 ── -->
  <div class="q-card">
    <div class="q-header">
      <div class="q-badge">
        <div class="q-num q5">5</div>
        <span class="difficulty diff-hard">Hard</span>
      </div>
      <div class="q-title-wrap">
        <div class="q-title">Search Products by Name</div>
        <div class="q-scenario">
          <strong>Scenario:</strong> Users want to search for products. When they type "mouse" in the search bar, the app should show all products whose name contains that word. Build this search endpoint.
        </div>
      </div>
    </div>
    <div class="q-body">
      <div class="task-label">Your Tasks</div>
      <div class="task-list">
        <div class="task-item">
          <span class="t-icon">🔧</span>
          <p>Create endpoint: <code>GET /products/search/{keyword}</code></p>
        </div>
        <div class="task-item">
          <span class="t-icon">🔍</span>
          <p>Search should be <strong>case-insensitive</strong> — searching "MOUSE" or "mouse" should give same result</p>
        </div>
        <div class="task-item">
          <span class="t-icon">⚠️</span>
          <p>If nothing found, return <code>{"message": "No products matched your search"}</code></p>
        </div>
        <div class="task-item">
          <span class="t-icon">📊</span>
          <p>Return matched products and total count of matches</p>
        </div>
      </div>
      <div class="test-urls">
        <div class="task-label" style="margin-bottom:6px">Test These URLs</div>
        <div class="test-url"><span class="get-badge">GET</span><span class="url-text">/products/search/mouse</span><span class="url-note">→ Wireless Mouse</span></div>
        <div class="test-url"><span class="get-badge">GET</span><span class="url-text">/products/search/BOOK</span><span class="url-note">→ Notebook (case-insensitive!)</span></div>
        <div class="test-url"><span class="get-badge">GET</span><span class="url-text">/products/search/xyz</span><span class="url-note">→ No products matched</span></div>
      </div>
      <div style="margin-top:14px;">
        <div class="hint-toggle" onclick="toggleHint('h5')">💡 Show Hint</div>
        <div class="hint-box" id="h5">
          <div class="hint-header">Hint — Use .lower() for case-insensitive search</div>
          <div class="hint-code"><span class="dec">@app.get</span>(<span class="str">"/products/search/{keyword}"</span>)
<span class="kw">def</span> <span class="fn">search_products</span>(keyword: <span class="fn">str</span>):
    results = [
        p <span class="kw">for</span> p <span class="kw">in</span> products
        <span class="kw">if</span> keyword.<span class="fn">lower</span>() <span class="kw">in</span> p[<span class="str">"name"</span>].<span class="fn">lower</span>()
    ]
    <span class="kw">if not</span> results:
        <span class="kw">return</span> {<span class="str">"message"</span>: <span class="str">"No products matched your search"</span>}
    <span class="kw">return</span> {<span class="str">"keyword"</span>: keyword, <span class="str">"results"</span>: results, <span class="str">"total_matches"</span>: <span class="fn">len</span>(results)}</div>
        </div>
      </div>
    </div>
  </div>

  <!-- ── BONUS ── -->
  <div class="q-card" style="border-color:rgba(139,92,246,.4);background:linear-gradient(135deg,rgba(139,92,246,.04),rgba(59,130,246,.04));">
    <div class="q-header" style="border-bottom-color:rgba(139,92,246,.2);">
      <div class="q-badge">
        <div class="q-num q5">⭐</div>
        <span class="difficulty diff-bonus">Bonus</span>
      </div>
      <div class="q-title-wrap">
        <div class="q-title">Cheapest & Most Expensive Product</div>
        <div class="q-scenario">
          <strong>Scenario:</strong> The app wants to show a "Best Deal" section (cheapest product) and a "Premium Pick" section (most expensive product) on the home screen. Build one endpoint that returns both.
        </div>
      </div>
    </div>
    <div class="q-body">
      <div class="task-label">Your Tasks</div>
      <div class="task-list">
        <div class="task-item">
          <span class="t-icon">🔧</span>
          <p>Create endpoint: <code>GET /products/deals</code></p>
        </div>
        <div class="task-item">
          <span class="t-icon">💸</span>
          <p>Return the product with the <strong>lowest price</strong> as <code>"best_deal"</code></p>
        </div>
        <div class="task-item">
          <span class="t-icon">👑</span>
          <p>Return the product with the <strong>highest price</strong> as <code>"premium_pick"</code></p>
        </div>
      </div>
      <div class="expected">
        <div class="expected-header">Expected Output at /products/deals</div>
        <div class="expected-code"><span class="j-brace">{</span>
  <span class="j-key">"best_deal"</span>:     <span class="j-brace">{</span><span class="j-key">"name"</span>: <span class="j-str">"Pen Set"</span>, <span class="j-key">"price"</span>: <span class="j-num">49</span>, ...<span class="j-brace">}</span>,
  <span class="j-key">"premium_pick"</span>:  <span class="j-brace">{</span><span class="j-key">"name"</span>: <span class="j-str">"Mechanical Keyboard"</span>, <span class="j-key">"price"</span>: <span class="j-num">2499</span>, ...<span class="j-brace">}</span>
<span class="j-brace">}</span></div>
      </div>
      <div style="margin-top:14px;">
        <div class="hint-toggle" onclick="toggleHint('hb')">💡 Show Hint</div>
        <div class="hint-box" id="hb">
          <div class="hint-header">Hint — Use Python's min() and max() with a key</div>
          <div class="hint-code"><span class="dec">@app.get</span>(<span class="str">"/products/deals"</span>)
<span class="kw">def</span> <span class="fn">get_deals</span>():
    cheapest  = <span class="fn">min</span>(products, key=<span class="kw">lambda</span> p: p[<span class="str">"price"</span>])
    expensive = <span class="fn">max</span>(products, key=<span class="kw">lambda</span> p: p[<span class="str">"price"</span>])
    <span class="kw">return</span> {
        <span class="str">"best_deal"</span>:    cheapest,
        <span class="str">"premium_pick"</span>: expensive,
    }</div>
        </div>
      </div>
    </div>
  </div>

  <!-- Submission checklist -->
  <div class="submit-box">
    <h3>✅ Submission Checklist</h3>
    <div class="submit-list">
      <div class="submit-item" onclick="toggleCheck(this)"><div class="s-box">✓</div><span>Q1 — /products returns total: 7</span></div>
      <div class="submit-item" onclick="toggleCheck(this)"><div class="s-box">✓</div><span>Q2 — /products/category/Electronics works</span></div>
      <div class="submit-item" onclick="toggleCheck(this)"><div class="s-box">✓</div><span>Q3 — /products/instock shows only available products</span></div>
      <div class="submit-item" onclick="toggleCheck(this)"><div class="s-box">✓</div><span>Q4 — /store/summary shows full store overview</span></div>
      <div class="submit-item" onclick="toggleCheck(this)"><div class="s-box">✓</div><span>Q5 — /products/search/mouse returns Wireless Mouse</span></div>
      <div class="submit-item" onclick="toggleCheck(this)"><div class="s-box">✓</div><span>Q5 — /products/search/BOOK also works (case-insensitive)</span></div>
      <div class="submit-item" onclick="toggleCheck(this)"><div class="s-box">✓</div><span>All endpoints tested in Swagger UI at /docs</span></div>
      <div class="submit-item" onclick="toggleCheck(this)"><div class="s-box">✓</div><span>⭐ Bonus — /products/deals returns cheapest and most expensive</span></div>
    </div>
  </div>

  <div class="footer">
    Built for <strong>FastAPI Internship Training</strong> · Day 1 Assignment · Good luck! 🚀
  </div>

</div>
<script>
function toggleHint(id){
  const box=document.getElementById(id);
  box.classList.toggle('open');
  const btn=box.previousElementSibling;
  btn.textContent=box.classList.contains('open')?'🙈 Hide Hint':'💡 Show Hint';
}
function toggleCheck(item){
  item.classList.toggle('checked');
}
</script>
</body>
</html>
