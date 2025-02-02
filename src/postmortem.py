from jinja2 import Environment, FileSystemLoader
from datetime import datetime, timezone
from pathlib import Path


def generate_postmortem(
    title: str,
    summary: str,
    root_cause: str,
    output: str,
    metrics: dict | None = None,
    findings: list[dict] | None = None,
):
    """Render a postmortem markdown report using Jinja2 template."""
    template_dir = Path(__file__).parent.parent / "templates"
    env = Environment(loader=FileSystemLoader(str(template_dir)))
    template = env.get_template("postmortem.md.j2")

    rendered = template.render(
        title=title,
        date=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        summary=summary,
        root_cause=root_cause,
        metrics=metrics,
        findings=findings or [],
    )

    with open(output, "w") as f:
        f.write(rendered)
