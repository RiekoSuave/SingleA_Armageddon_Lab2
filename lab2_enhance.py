#!/usr/bin/env python3
"""
lab2_enhance.py — EC2 User Data Automation Helper (Lab 2 Enhancement)

This script enhances the Lab 2 startup workflow by:
  1. Generating a polished, requirement-compliant index.html
  2. Producing a startup.sh bash script (EC2 User Data ready)
  3. Validating the generated HTML for required Lab 2 elements
  4. Optionally uploading startup.sh to an S3 bucket for use as User Data

Usage:
    python3 lab2_enhance.py [--validate] [--upload-s3 BUCKET]

Dependencies: boto3 (optional, only for S3 upload)
"""

import argparse
import os
import re
import sys

# ── Configuration ─────────────────────────────────────────────────────────────

STUDENT_NAME = "Your Name Here"          # ← change this
OUTPUT_DIR   = "./lab2_output"
HTML_FILE    = os.path.join(OUTPUT_DIR, "index.html")
BASH_FILE    = os.path.join(OUTPUT_DIR, "startup.sh")


# ── HTML Generation ───────────────────────────────────────────────────────────

def generate_html(name: str) -> str:
    """
    Returns a complete index.html string that satisfies all Lab 2 page
    requirements: name, background, embedded image, three content sections.
    """
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{name} — Lab 2</title>
  <style>
    /* ── Reset & base ── */
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

    body {{
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
      color: #e8f4f8;
      min-height: 100vh;
    }}

    /* ── Header ── */
    header {{
      text-align: center;
      padding: 3rem 1rem 2rem;
      background: rgba(255,255,255,0.05);
      border-bottom: 1px solid rgba(255,255,255,0.1);
    }}
    header h1 {{
      font-size: 2.8rem;
      letter-spacing: 2px;
      color: #7ecef4;
    }}
    header p {{
      margin-top: 0.5rem;
      font-size: 1.1rem;
      opacity: 0.75;
    }}

    /* ── Hero image ── */
    .hero-img {{
      display: block;
      margin: 2rem auto;
      width: 220px;
      height: 220px;
      object-fit: cover;
      border-radius: 50%;
      border: 4px solid #7ecef4;
      box-shadow: 0 0 30px rgba(126,206,244,0.4);
    }}

    /* ── Sections ── */
    main {{
      max-width: 900px;
      margin: 0 auto;
      padding: 2rem 1.5rem 4rem;
    }}
    section {{
      background: rgba(255,255,255,0.06);
      border-left: 4px solid #7ecef4;
      border-radius: 0 8px 8px 0;
      padding: 1.8rem 2rem;
      margin-bottom: 2rem;
      backdrop-filter: blur(6px);
    }}
    section h2 {{
      font-size: 1.5rem;
      color: #7ecef4;
      margin-bottom: 0.8rem;
    }}
    section p {{
      line-height: 1.8;
      opacity: 0.9;
    }}

    /* ── Footer ── */
    footer {{
      text-align: center;
      padding: 1.5rem;
      font-size: 0.85rem;
      opacity: 0.5;
      border-top: 1px solid rgba(255,255,255,0.08);
    }}
  </style>
</head>
<body>

  <header>
    <h1>{name}</h1>
    <p>AWS Cloud Labs — EC2 User Data Automation</p>
  </header>

  <!-- Embedded image (requirement met) -->
  <!-- Replace src with your own image URL or base64 data URI -->
  <img
    class="hero-img"
    src="https://via.placeholder.com/220/2c5364/7ecef4?text={name.split()[0] if name else 'Me'}"
    alt="Profile photo of {name}"
  />

  <main>

    <!-- Section 1: About Me -->
    <section id="about">
      <h2>About Me</h2>
      <p>
        Hi, I'm <strong>{name}</strong>. I'm a cloud engineering student passionate
        about infrastructure automation, DevOps, and building reliable systems on AWS.
        This page was generated and served automatically using an EC2 User Data script —
        no manual SSH required.
      </p>
    </section>

    <!-- Section 2: Project Description -->
    <section id="project">
      <h2>Project Description</h2>
      <p>
        <strong>Lab 2</strong> explores EC2 startup automation using Bash User Data scripts.
        On first boot, the instance installs <em>Nginx</em>, writes this HTML file to
        <code>/var/www/html/</code>, and starts the web server — all without human
        interaction. The companion Python script (<code>lab2_enhance.py</code>) generates
        the HTML and startup script, validates required elements, and can push the script
        to S3 for re-use.
      </p>
    </section>

    <!-- Section 3: Contact / Footer -->
    <section id="contact">
      <h2>Contact</h2>
      <p>
        📧 &nbsp;<a href="mailto:student@example.com" style="color:#7ecef4;">
          student@example.com
        </a><br/>
        🔗 &nbsp;<a href="https://github.com/" style="color:#7ecef4;" target="_blank">
          github.com/your-username
        </a>
      </p>
    </section>

  </main>

  <footer>
    <p>Deployed automatically via EC2 User Data • {name} © 2025</p>
  </footer>

</body>
</html>
"""


# ── Bash Script Generation ────────────────────────────────────────────────────

def generate_startup_sh(html_content: str) -> str:
    """
    Returns a bash startup script suitable for EC2 User Data.
    Supports both Amazon Linux 2/2023 (yum/dnf) and Ubuntu (apt).
    """
    # Escape backticks and $ inside the heredoc so they survive bash expansion
    safe_html = html_content.replace("\\", "\\\\").replace("`", "\\`")

    return r"""#!/bin/bash
# =============================================================================
# startup.sh — EC2 User Data Automation Script (Lab 2)
# Compatible with: Amazon Linux 2/2023 and Ubuntu 20.04+
# =============================================================================

set -euo pipefail          # exit on error, unset vars, pipe failures
exec > /var/log/startup.log 2>&1  # redirect all output to a log file

# ── Detect OS and install Nginx ───────────────────────────────────────────────
if command -v dnf &>/dev/null; then
    echo "[INFO] Detected Amazon Linux / dnf-based OS"
    dnf update -y
    dnf install -y nginx
elif command -v yum &>/dev/null; then
    echo "[INFO] Detected yum-based OS"
    yum update -y
    yum install -y nginx
elif command -v apt-get &>/dev/null; then
    echo "[INFO] Detected Debian/Ubuntu"
    apt-get update -y
    apt-get install -y nginx
else
    echo "[ERROR] Unsupported package manager — cannot install Nginx"
    exit 1
fi

# ── Configure web root ────────────────────────────────────────────────────────
WEB_ROOT="/var/www/html"
mkdir -p "$WEB_ROOT"

# ── Write index.html ─────────────────────────────────────────────────────────
cat > "$WEB_ROOT/index.html" << 'HTMLEOF'
__HTML_PLACEHOLDER__
HTMLEOF

echo "[INFO] index.html written to $WEB_ROOT"

# ── Set correct permissions ───────────────────────────────────────────────────
chown -R nginx:nginx "$WEB_ROOT" 2>/dev/null || chown -R www-data:www-data "$WEB_ROOT"
chmod -R 755 "$WEB_ROOT"

# ── Enable and start Nginx ────────────────────────────────────────────────────
systemctl enable nginx
systemctl start nginx

echo "[INFO] Nginx started successfully"
echo "[INFO] Startup script completed — site is live on port 80"
"""


def inject_html_into_script(script: str, html: str) -> str:
    """Replace the placeholder in the script with the actual HTML."""
    return script.replace("__HTML_PLACEHOLDER__", html.strip())


# ── HTML Validation ───────────────────────────────────────────────────────────

REQUIRED_CHECKS = {
    "Student name present":      lambda h, n: n.lower() in h.lower(),
    "Background color/image":    lambda h, _: "background" in h,
    "Embedded image (<img>)":    lambda h, _: bool(re.search(r"<img\b", h, re.I)),
    "About section":             lambda h, _: "about" in h.lower(),
    "Project section":           lambda h, _: "project" in h.lower(),
    "Contact/Footer section":    lambda h, _: any(k in h.lower() for k in ["contact", "footer"]),
}

def validate_html(html: str, name: str) -> bool:
    """Run Lab 2 requirement checks. Returns True if all pass."""
    print("\n── Lab 2 HTML Validation ────────────────────────────────")
    all_pass = True
    for check, fn in REQUIRED_CHECKS.items():
        passed = fn(html, name)
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {status}  {check}")
        if not passed:
            all_pass = False
    print("─────────────────────────────────────────────────────────")
    return all_pass


# ── S3 Upload (optional) ──────────────────────────────────────────────────────

def upload_to_s3(local_path: str, bucket: str, key: str = "startup.sh") -> None:
    """Upload startup.sh to S3 so it can be fetched by User Data or SSM."""
    try:
        import boto3  # type: ignore
    except ImportError:
        print("[WARN] boto3 not installed — skipping S3 upload. Run: pip install boto3")
        return

    s3 = boto3.client("s3")
    s3.upload_file(local_path, bucket, key)
    print(f"[INFO] Uploaded {local_path} → s3://{bucket}/{key}")


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="Lab 2 Enhancement Tool")
    parser.add_argument("--validate",    action="store_true",
                        help="Validate generated HTML against Lab 2 requirements")
    parser.add_argument("--upload-s3",   metavar="BUCKET",
                        help="Upload startup.sh to the given S3 bucket")
    parser.add_argument("--name",        default=STUDENT_NAME,
                        help="Student name to embed in the page")
    args = parser.parse_args()

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 1. Generate HTML
    html = generate_html(args.name)
    with open(HTML_FILE, "w") as f:
        f.write(html)
    print(f"[INFO] Generated {HTML_FILE}")

    # 2. Generate and write startup.sh
    script_template = generate_startup_sh(html)
    script = inject_html_into_script(script_template, html)
    with open(BASH_FILE, "w") as f:
        f.write(script)
    os.chmod(BASH_FILE, 0o755)
    print(f"[INFO] Generated {BASH_FILE}")

    # 3. Validate (optional flag, but always informative)
    if args.validate:
        ok = validate_html(html, args.name)
        if not ok:
            print("[WARN] Some Lab 2 requirements are missing — review above.")
            sys.exit(1)
        else:
            print("[INFO] All Lab 2 requirements satisfied.")

    # 4. Upload to S3 (optional)
    if args.upload_s3:
        upload_to_s3(BASH_FILE, args.upload_s3)

    print("\n[DONE] Lab 2 artifacts written to:", OUTPUT_DIR)
    print("       Preview: open lab2_output/index.html in a browser")
    print("       Deploy:  paste lab2_output/startup.sh into EC2 User Data")


if __name__ == "__main__":
    main()
