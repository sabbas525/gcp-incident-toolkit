import re
from collections import Counter

PATTERNS = {
    "OOM": (r"(Out of memory|OOM|oom-kill)", "critical"),
    "Timeout": (r"(timeout|timed out|deadline exceeded)", "warning"),
    "Connection refused": (r"(connection refused|ECONNREFUSED|connect failed)", "warning"),
    "5xx errors": (r"HTTP\s+5\d{2}", "critical"),
    "Permission denied": (r"(permission denied|access denied|forbidden)", "warning"),
    "Disk pressure": (r"(no space left|disk full|disk pressure)", "critical"),
}


def parse_logs(log_file: str, window: int = 300) -> list[dict]:
    """Scan a log file for known error patterns and return findings."""
    counts: Counter = Counter()
    samples: dict[str, str] = {}

    with open(log_file) as f:
        for line in f:
            for name, (pattern, _) in PATTERNS.items():
                if re.search(pattern, line, re.IGNORECASE):
                    counts[name] += 1
                    if name not in samples:
                        samples[name] = line.strip()[:200]

    findings = []
    for name, count in counts.most_common():
        _, severity = PATTERNS[name]
        findings.append({
            "pattern": name,
            "severity": severity,
            "count": count,
            "sample": samples.get(name, ""),
        })

    return findings
