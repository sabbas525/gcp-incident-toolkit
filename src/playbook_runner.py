import yaml
import subprocess
import click


def run_playbook(playbook_file: str, auto_mode: bool = False):
    """Load and execute a YAML troubleshooting playbook."""
    with open(playbook_file) as f:
        playbook = yaml.safe_load(f)

    click.echo(f"\n{'='*60}")
    click.echo(f"Playbook: {playbook['name']}")
    click.echo(f"Trigger:  {playbook.get('trigger', 'manual')}")
    click.echo(f"{'='*60}\n")

    for i, step in enumerate(playbook["steps"], 1):
        click.echo(f"Step {i}: {step['description']}")

        if "command" in step:
            if auto_mode or click.confirm("  Run command?", default=True):
                click.echo(f"  $ {step['command']}")
                try:
                    result = subprocess.run(
                        step["command"], shell=True, capture_output=True, text=True, timeout=30
                    )
                    if result.stdout:
                        click.echo(result.stdout)
                    if result.stderr:
                        click.echo(f"  stderr: {result.stderr}")
                except subprocess.TimeoutExpired:
                    click.echo("  Command timed out.")

        if "prompt" in step and not auto_mode:
            response = click.prompt(f"  {step['prompt']}", default="n/a")
            click.echo(f"  → {response}")

        click.echo()

    if "escalation" in playbook:
        click.echo(f"Escalation: {playbook['escalation']}")
