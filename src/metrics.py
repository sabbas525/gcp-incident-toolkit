import psutil
from datetime import datetime, timezone


def collect_metrics() -> dict:
    """Collect system metrics using psutil."""
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    net = psutil.net_io_counters()

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "cpu_percent": cpu,
        "memory_total_mb": round(mem.total / 1024 / 1024),
        "memory_used_mb": round(mem.used / 1024 / 1024),
        "memory_percent": mem.percent,
        "disk_total_gb": round(disk.total / 1024 / 1024 / 1024, 1),
        "disk_used_gb": round(disk.used / 1024 / 1024 / 1024, 1),
        "disk_percent": disk.percent,
        "net_bytes_sent": net.bytes_sent,
        "net_bytes_recv": net.bytes_recv,
    }
