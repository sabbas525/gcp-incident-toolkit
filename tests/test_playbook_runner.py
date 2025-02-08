import yaml
import tempfile
import os
from src.playbook_runner import run_playbook


def test_playbook_loads_and_runs_auto(capsys):
    playbook = {
        "name": "Test Playbook",
        "trigger": "manual",
        "steps": [
            {"description": "Echo test", "command": "echo hello"},
        ],
        "escalation": "Call someone",
    }
    f = tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False)
    yaml.dump(playbook, f)
    f.close()

    run_playbook(f.name, auto_mode=True)
    os.unlink(f.name)

    captured = capsys.readouterr()
    assert "Test Playbook" in captured.out
    assert "hello" in captured.out
