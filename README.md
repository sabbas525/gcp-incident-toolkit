# gcp-incident-toolkit

A Python CLI tool for structured incident management. Collects system metrics, parses logs for anomalies, walks through YAML-defined troubleshooting playbooks, and generates postmortem reports in markdown.

## Architecture

```
                    ┌─────────────────────────┐
                    │      CLI (Click)         │
                    │  collect │ diagnose │    │
                    │  playbook│ postmortem    │
                    └────┬─────┬─────┬────┬───┘
                         │     │     │    │
              ┌──────────┘     │     │    └──────────┐
              ▼                ▼     ▼               ▼
        ┌──────────┐   ┌──────────┐ ┌──────────┐ ┌──────────┐
        │ Metrics  │   │   Log    │ │ Playbook │ │Postmortem│
        │Collector │   │  Parser  │ │  Runner  │ │Generator │
        │(psutil)  │   │ (regex)  │ │  (YAML)  │ │(Jinja2)  │
        └──────────┘   └──────────┘ └──────────┘ └──────────┘
```

## Tech Stack

- Python 3.11+, Click, PyYAML, psutil, Jinja2
- Shell scripts for metric collection
- Docker + Kubernetes (Helm chart)

## Setup

```bash
pip install -r requirements.txt
```

## Usage

```bash
# Collect system metrics
python -m src.cli collect
python -m src.cli collect --json

# Diagnose a log file
python -m src.cli diagnose /var/log/syslog

# Run a troubleshooting playbook
python -m src.cli playbook playbooks/high-cpu.yaml
python -m src.cli playbook playbooks/high-cpu.yaml --auto

# Generate a postmortem
python -m src.cli postmortem \
  --title "API Outage 2025-03-15" \
  --summary "API returned 503 for 45 minutes" \
  --root-cause "OOM kill on primary pod due to memory leak" \
  --output incident-report.md
```

## Playbook Format

```yaml
name: High CPU Usage
trigger: cpu_percent > 90
steps:
  - description: Check top processes
    command: "ps aux --sort=-%cpu | head -20"
  - description: Check recent deployments
    prompt: "Were there any deployments in the last hour?"
escalation: "Page the on-call SRE if unresolved after 15 minutes"
```

## Docker

```bash
docker build -t incident-toolkit .
docker run incident-toolkit collect --json
```

## Kubernetes (Helm)

```bash
helm install incident-toolkit helm/incident-toolkit/
```

Deploys as a CronJob that runs health checks on a schedule.

## Project Structure

```
gcp-incident-toolkit/
├── src/
│   ├── cli.py               # Click CLI entry point
│   ├── metrics.py            # System metrics (psutil)
│   ├── log_parser.py         # Log anomaly detection
│   ├── playbook_runner.py    # YAML playbook executor
│   └── postmortem.py         # Jinja2 report generator
├── scripts/
│   ├── collect-metrics.sh    # Shell-based metric collection
│   └── health-check.sh       # Endpoint health probe
├── playbooks/
│   ├── high-cpu.yaml
│   ├── disk-full.yaml
│   └── service-down.yaml
├── templates/
│   └── postmortem.md.j2      # Postmortem markdown template
├── helm/
│   └── incident-toolkit/
│       ├── Chart.yaml
│       ├── values.yaml
│       └── templates/
│           └── deployment.yaml
├── tests/
│   ├── test_metrics.py
│   ├── test_log_parser.py
│   └── test_playbook_runner.py
├── Dockerfile
├── requirements.txt
└── requirements-dev.txt
```

## Running Tests

```bash
pip install -r requirements-dev.txt
pytest
```
