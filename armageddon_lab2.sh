#!/bin/bash
# ============================================================
# EC2 User Data Startup Script
# Cloud Foundations Lab – Static Website on Apache
# Runs automatically at instance launch (root privileges)
# ============================================================

# ── 1. Update package index ─────────────────────────────────
yum update -y

# ── 2. Install Apache web server ────────────────────────────
yum install -y httpd

# ── 3. Enable Apache to start on every reboot ───────────────
systemctl enable httpd

# ── 4. Start Apache now ─────────────────────────────────────
systemctl start httpd

# ── 5. Write the HTML page to Apache's document root ────────
cat > /var/www/html/index.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Cloud Foundations · Live</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;700;800&display=swap" rel="stylesheet" />
  <style>
    /* ── Reset & base ─────────────────────────────────────── */
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    :root {
      --bg:        #0a0c10;
      --surface:   #111318;
      --border:    #1e2330;
      --accent:    #00e5a0;
      --accent2:   #0088ff;
      --text:      #e2e8f0;
      --muted:     #64748b;
      --mono:      'Space Mono', monospace;
      --sans:      'Syne', sans-serif;
    }

    html, body {
      height: 100%;
      background: var(--bg);
      color: var(--text);
      font-family: var(--sans);
      overflow-x: hidden;
    }

    /* ── Noise grain overlay ──────────────────────────────── */
    body::before {
      content: '';
      position: fixed; inset: 0; z-index: 0;
      background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.035'/%3E%3C/svg%3E");
      pointer-events: none;
    }

    /* ── Grid background ──────────────────────────────────── */
    body::after {
      content: '';
      position: fixed; inset: 0; z-index: 0;
      background-image:
        linear-gradient(var(--border) 1px, transparent 1px),
        linear-gradient(90deg, var(--border) 1px, transparent 1px);
      background-size: 40px 40px;
      opacity: 0.4;
      pointer-events: none;
    }

    /* ── Layout ───────────────────────────────────────────── */
    .page {
      position: relative; z-index: 1;
      min-height: 100vh;
      display: grid;
      grid-template-rows: auto 1fr auto;
      padding: 32px;
      gap: 32px;
    }

    /* ── Top bar ──────────────────────────────────────────── */
    header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      border: 1px solid var(--border);
      background: rgba(17,19,24,0.8);
      backdrop-filter: blur(8px);
      padding: 14px 24px;
      border-radius: 8px;
    }

    .logo {
      font-family: var(--mono);
      font-size: 0.75rem;
      letter-spacing: 0.15em;
      color: var(--accent);
      text-transform: uppercase;
    }

    .status-pill {
      display: flex; align-items: center; gap: 8px;
      font-family: var(--mono);
      font-size: 0.7rem;
      color: var(--accent);
      text-transform: uppercase;
      letter-spacing: 0.1em;
    }

    .dot {
      width: 8px; height: 8px;
      background: var(--accent);
      border-radius: 50%;
      animation: pulse 2s ease-in-out infinite;
    }

    @keyframes pulse {
      0%, 100% { opacity: 1; transform: scale(1); box-shadow: 0 0 0 0 rgba(0,229,160,0.4); }
      50%       { opacity: 0.7; transform: scale(1.1); box-shadow: 0 0 0 6px rgba(0,229,160,0); }
    }

    /* ── Hero ─────────────────────────────────────────────── */
    .hero {
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: flex-start;
      max-width: 900px;
      margin: 0 auto;
      width: 100%;
      gap: 24px;
      animation: fadeUp 0.8s ease both;
    }

    @keyframes fadeUp {
      from { opacity: 0; transform: translateY(24px); }
      to   { opacity: 1; transform: translateY(0); }
    }

    .eyebrow {
      font-family: var(--mono);
      font-size: 0.7rem;
      letter-spacing: 0.2em;
      color: var(--muted);
      text-transform: uppercase;
      border-left: 2px solid var(--accent);
      padding-left: 10px;
    }

    h1 {
      font-size: clamp(2.5rem, 6vw, 5rem);
      font-weight: 800;
      line-height: 1.05;
      letter-spacing: -0.03em;
    }

    h1 em {
      font-style: normal;
      background: linear-gradient(135deg, var(--accent), var(--accent2));
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }

    .subtitle {
      font-size: 1.05rem;
      color: var(--muted);
      line-height: 1.7;
      max-width: 520px;
    }

    /* ── Cards ────────────────────────────────────────────── */
    .cards {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 16px;
      width: 100%;
      animation: fadeUp 0.8s 0.2s ease both;
    }

    .card {
      border: 1px solid var(--border);
      background: var(--surface);
      border-radius: 8px;
      padding: 20px;
      transition: border-color 0.2s, transform 0.2s;
    }

    .card:hover {
      border-color: var(--accent);
      transform: translateY(-3px);
    }

    .card-label {
      font-family: var(--mono);
      font-size: 0.65rem;
      letter-spacing: 0.15em;
      color: var(--muted);
      text-transform: uppercase;
      margin-bottom: 8px;
    }

    .card-value {
      font-size: 1.1rem;
      font-weight: 700;
      color: var(--text);
      word-break: break-all;
    }

    .card-value.accent { color: var(--accent); }

    /* ── Terminal block ───────────────────────────────────── */
    .terminal {
      font-family: var(--mono);
      font-size: 0.8rem;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 20px 24px;
      line-height: 1.9;
      width: 100%;
      animation: fadeUp 0.8s 0.35s ease both;
    }

    .terminal .cmd  { color: var(--accent2); }
    .terminal .ok   { color: var(--accent); }
    .terminal .dim  { color: var(--muted); }

    /* ── Footer ───────────────────────────────────────────── */
    footer {
      font-family: var(--mono);
      font-size: 0.65rem;
      color: var(--muted);
      text-align: center;
      letter-spacing: 0.08em;
    }
  </style>
</head>
<body>
  <div class="page">

    <header>
      <span class="logo">☁ Cloud Foundations</span>
      <span class="status-pill"><span class="dot"></span>Instance Running</span>
    </header>

    <main class="hero">
      <p class="eyebrow">EC2 · User Data · Apache HTTP</p>
      <h1>Server is <em>live</em>.<br>Zero manual config.</h1>
      <p class="subtitle">
        This page was served automatically — provisioned by a Bash startup
        script injected via EC2 User Data at launch time. No SSH. No manual
        setup. Just infrastructure as code.
      </p>

      <div class="cards">
        <div class="card">
          <div class="card-label">Web Server</div>
          <div class="card-value accent">Apache (httpd)</div>
        </div>
        <div class="card">
          <div class="card-label">Protocol</div>
          <div class="card-value">HTTP · Port 80</div>
        </div>
        <div class="card">
          <div class="card-label">Document Root</div>
          <div class="card-value">/var/www/html/</div>
        </div>
        <div class="card">
          <div class="card-label">Provisioned By</div>
          <div class="card-value">EC2 User Data</div>
        </div>
      </div>

      <div class="terminal">
        <div><span class="dim">$</span> <span class="cmd">yum install -y httpd</span></div>
        <div><span class="ok">✔</span> <span class="dim">apache installed</span></div>
        <div><span class="dim">$</span> <span class="cmd">systemctl enable --now httpd</span></div>
        <div><span class="ok">✔</span> <span class="dim">service started &amp; enabled on boot</span></div>
        <div><span class="dim">$</span> <span class="cmd">cat &gt; /var/www/html/index.html</span></div>
        <div><span class="ok">✔</span> <span class="dim">page deployed — you're looking at it</span></div>
      </div>
    </main>

    <footer>CLOUD FOUNDATIONS LAB &nbsp;·&nbsp; EC2 USER DATA DEMO &nbsp;·&nbsp; APACHE 2.4</footer>

  </div>
</body>
</html>
EOF

# ── 6. Lock down file permissions ───────────────────────────
chmod 644 /var/www/html/index.html
chown apache:apache /var/www/html/index.html

# ── Done ─────────────────────────────────────────────────────
# Apache is now serving /var/www/html/index.html on port 80.
# Make sure your EC2 Security Group allows inbound TCP on port 80.