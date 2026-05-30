# CLAUDE.md — Lab 2 & Lab 3 Project Context

> This file tells AI assistants (Claude, Copilot, etc.) about the project
> structure, goals, and conventions so they can give accurate, context-aware help.

---

## Project Overview

| Item | Detail |
|------|--------|
| **Course** | Cloud Engineering / DevOps Fundamentals |
| **Labs** | Lab 2 (EC2 automation) · Lab 3 (debugging) |
| **Primary language** | Python 3.12 + Bash |
| **Infrastructure** | AWS EC2, optionally Docker / Kubernetes |

---

## Repository Layout

```
.
├── lab2_enhance.py        # Python generator: produces index.html + startup.sh
├── lab2_output/
│   ├── index.html         # Generated static site (DO NOT edit by hand)
│   └── startup.sh         # EC2 User Data script (generated)
├── Dockerfile             # Multi-stage: Python builder → Nginx runtime
├── docker-compose.yml     # Local dev mirror of the EC2 environment
├── k8s-lab2.yml           # Kubernetes manifests (Deployment, Service, HPA)
├── CLAUDE.md              # ← you are here
└── DEBUGGING.md           # Lab 3 debugging journal (create this file)
```

---

## Lab 2 — EC2 User Data Automation

### What the Python script does

`lab2_enhance.py` is the **single source of truth** for this lab.  
Running it produces two artifacts in `./lab2_output/`:

1. **`index.html`** — A fully styled static page that satisfies all graded requirements:
   - Student name embedded in `<h1>` and `<footer>`
   - CSS gradient background
   - `<img>` profile photo (replace the placeholder URL)
   - Three `<section>` elements: *About Me*, *Project Description*, *Contact*

2. **`startup.sh`** — A bash script ready to paste into the EC2 **User Data** field:
   - Detects Amazon Linux (yum/dnf) vs Ubuntu (apt) automatically
   - Installs Nginx, writes `index.html`, sets permissions, enables the service
   - Logs everything to `/var/log/startup.log`

### How to run

```bash
# Basic generation
python3 lab2_enhance.py --name "Your Name Here"

# With HTML validation (checks all Lab 2 graded requirements)
python3 lab2_enhance.py --name "Your Name Here" --validate

# Upload startup.sh to S3 for use with SSM or Launch Templates
python3 lab2_enhance.py --name "Your Name Here" --upload-s3 my-bucket-name
```

### Deploying to EC2

1. Open the AWS Console → EC2 → Launch Instance
2. Expand **Advanced Details** → paste the contents of `startup.sh` into **User Data**
3. Make sure **port 80** is open in the Security Group (Inbound rule: HTTP, 0.0.0.0/0)
4. Launch — the site will be live at `http://<public-ip>/` within ~60 seconds
5. To debug: SSH in and run `cat /var/log/startup.log`

### Running locally with Docker

```bash
docker compose up --build
# Then open: http://localhost:8080
```

### Running on Kubernetes

```bash
# Apply all manifests
kubectl apply -f k8s-lab2.yml

# Watch pods come up
kubectl get pods -n lab2 -w

# Get the external IP (LoadBalancer)
kubectl get svc lab2-site-lb -n lab2

# Swap the ConfigMap HTML with your generated file
kubectl create configmap lab2-html \
  --from-file=index.html=./lab2_output/index.html \
  -n lab2 --dry-run=client -o yaml | kubectl apply -f -
```

---

## Lab 3 — Debugging Exercise

### Approach

- Fork the provided repo; clone it locally
- Read **all** error output before touching code
- Make **one targeted change at a time** and re-run
- Document every step in `DEBUGGING.md` (template below)

### DEBUGGING.md template

```markdown
# Debugging Journal — Lab 3

## Initial Error
<!-- Paste the first error message exactly as shown -->

## Diagnosis
<!-- What did you look at? What did the error tell you? -->

## Changes Made
| File | Line | Before | After | Reason |
|------|------|--------|-------|--------|

## Final Result
<!-- Paste successful output or screenshot description -->
```

### Common issues to look for

| Category | Things to check |
|----------|----------------|
| **Imports** | Missing packages (`pip install …`), renamed modules |
| **Syntax** | Indentation, f-string quotes, missing colons |
| **Logic** | Off-by-one, wrong variable names, inverted conditions |
| **Environment** | Python version (`python --version`), venv activation, `.env` file |
| **Dependencies** | `requirements.txt` present? All packages pinned? |

---

## AI Assistant Instructions

When helping with this project, please:

- **Prefer targeted edits** over full rewrites (especially for Lab 3)
- **Preserve comments** in generated Bash and Python — they are graded (15 %)
- **Do not remove** the OS-detection logic in `startup.sh`; it must run on both Amazon Linux and Ubuntu
- **Keep HTML inline** (no external CSS/JS files) so `startup.sh` stays self-contained
- When suggesting Kubernetes changes, keep them compatible with **EKS 1.29+** and avoid deprecated APIs
- Reference the grading rubric weights when prioritising fixes:
  - Script runs without errors: **30 %**
  - Web page renders correctly: **30 %**
  - Required page elements: **25 %**
  - Script readability & comments: **15 %**
