from src.metrics import collect_metrics


def test_collect_metrics_returns_expected_keys():
    metrics = collect_metrics()
    expected = ["timestamp", "cpu_percent", "memory_total_mb", "memory_used_mb",
                "memory_percent", "disk_total_gb", "disk_used_gb", "disk_percent",
                "net_bytes_sent", "net_bytes_recv"]
    for key in expected:
        assert key in metrics


def test_cpu_percent_in_range():
    metrics = collect_metrics()
    assert 0 <= metrics["cpu_percent"] <= 100
