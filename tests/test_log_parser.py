import tempfile
import os
from src.log_parser import parse_logs


def _write_temp_log(lines: list[str]) -> str:
    f = tempfile.NamedTemporaryFile(mode="w", suffix=".log", delete=False)
    f.write("\n".join(lines))
    f.close()
    return f.name


def test_detects_oom():
    path = _write_temp_log(["2025-01-01 Out of memory: killed process 1234", "normal line"])
    findings = parse_logs(path)
    os.unlink(path)
    assert any(f["pattern"] == "OOM" for f in findings)


def test_detects_5xx():
    path = _write_temp_log(["GET /api HTTP 502", "GET /api HTTP 200", "POST /data HTTP 503"])
    findings = parse_logs(path)
    os.unlink(path)
    match = next(f for f in findings if f["pattern"] == "5xx errors")
    assert match["count"] == 2


def test_no_findings_on_clean_log():
    path = _write_temp_log(["INFO all good", "DEBUG request processed"])
    findings = parse_logs(path)
    os.unlink(path)
    assert findings == []
