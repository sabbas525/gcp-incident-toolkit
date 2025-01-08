import click
from src.metrics import collect_metrics
from src.log_parser import parse_logs
from src.playbook_runner import run_playbook
from src.postmortem import generate_postmortem


@click.group()
def cli():
    """GCP Incident Toolkit — collect metrics, diagnose issues, generate postmortems."""
    pass


@cli.command()
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
def collect(as_json):
    """Collect system metrics (CPU, memory, disk, network)."""
    metrics = collect_metrics()
    if as_json:
        import json
        click.echo(json.dumps(metrics, indent=2))
    else:
        for k, v in metrics.items():
            click.echo(f"{k}: {v}")


@cli.command()
@click.argument("log_file", type=click.Path(exists=True))
@click.option("--window", default=300, help="Time window in seconds for rate detection")
def diagnose(log_file, window):
    """Parse log file for anomalies and error patterns."""
    findings = parse_logs(log_file, window)
    if not findings:
        click.echo("No anomalies detected.")
        return
    for f in findings:
        click.echo(f"[{f['severity']}] {f['pattern']}: {f['count']} occurrences — {f['sample']}")


@cli.command()
@click.argument("playbook_file", type=click.Path(exists=True))
@click.option("--auto", is_flag=True, help="Run all steps without prompting")
def playbook(playbook_file, auto):
    """Run a troubleshooting playbook."""
    run_playbook(playbook_file, auto_mode=auto)


@cli.command()
@click.option("--title", required=True, help="Incident title")
@click.option("--summary", required=True, help="Brief summary")
@click.option("--root-cause", required=True, help="Root cause description")
@click.option("--output", default="postmortem.md", help="Output file path")
@click.option("--metrics-json", type=click.Path(exists=True), help="Metrics JSON file")
@click.option("--log-file", type=click.Path(exists=True), help="Log file to include findings from")
def postmortem(title, summary, root_cause, output, metrics_json, log_file):
    """Generate a postmortem report."""
    metrics = None
    findings = None
    if metrics_json:
        import json
        with open(metrics_json) as f:
            metrics = json.load(f)
    if log_file:
        findings = parse_logs(log_file)
    generate_postmortem(title, summary, root_cause, output, metrics=metrics, findings=findings)
    click.echo(f"Postmortem written to {output}")


if __name__ == "__main__":
    cli()
