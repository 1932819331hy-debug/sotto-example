"""Exercise the real local Sotto flow on a disposable Linux CI runner only."""

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def main():
    # SOTTO_DATA_DIR does not isolate OS keychain entries. Never initialise a
    # throwaway identity in a developer's real keychain.
    if sys.platform != "linux" or os.environ.get("GITHUB_ACTIONS") != "true":
        raise SystemExit("Run this check only on the disposable Linux GitHub Actions runner.")
    with tempfile.TemporaryDirectory(prefix="sotto-example-") as folder:
        env = os.environ.copy()
        env.pop("SOTTO_TOKEN", None)
        env.pop("DEMO_SECRET", None)
        env["SOTTO_DATA_DIR"] = str(Path(folder) / "store")
        env["SOTTO_PASSWORD"] = "disposable-ci-demo-password"

        def run(command, expected, stdin=None):
            result = subprocess.run(
                command,
                cwd=folder,
                env=env,
                input=stdin,
                text=True,
                capture_output=True,
                timeout=120,
            )
            if result.returncode != expected:
                raise SystemExit(
                    f"Unexpected exit status from {command[:2]}; output withheld to keep the Emergency Kit private."
                )
            return result

        def status():
            return json.loads(run(["sotto", "status", "--json"], 0).stdout)

        python = [sys.executable, str(ROOT / "python/main.py")]
        run(python, 1)

        if status() != {"initialized": False, "unlocked": False, "project": None}:
            raise SystemExit("Unexpected initial status before init.")

        run(["sotto", "init", "--name", "sotto-example"], 0)

        if status() != {
            "initialized": True,
            "unlocked": True,
            "project": {"name": "sotto-example", "environment": "dev"},
        }:
            raise SystemExit("Unexpected status after init.")

        envs_out = run(["sotto", "env", "ls"], 0).stdout
        envs = {line.lstrip("* ").strip() for line in envs_out.splitlines() if line.strip()}
        if envs != {"dev", "staging", "prod"}:
            raise SystemExit("Unexpected environment list after init.")

        run(["sotto", "set", "DEMO_SECRET", "--stdin"], 0, "hello-from-sotto")

        if json.loads(run(["sotto", "ls", "--json"], 0).stdout) != ["DEMO_SECRET"]:
            raise SystemExit("Unexpected secret list in dev.")

        result = run(["sotto", "run", "--", *python], 0)
        if result.stdout != "Sotto demo: secret loaded successfully.\n":
            raise SystemExit("Unexpected demo output in dev (withheld).")

        run(["sotto", "env", "copy", "dev", "staging", "--confirm"], 0)
        staging_result = run(["sotto", "run", "--env", "staging", "--", *python], 0)
        if staging_result.stdout != "Sotto demo: secret loaded successfully.\n":
            raise SystemExit("Unexpected demo output in staging (withheld).")

        dotenv_path = Path(folder) / ".env.staging"
        dotenv_path.write_text("IMPORTED_KEY=synthetic-dotenv-value\n", encoding="utf-8")
        run(["sotto", "import", "--env", "staging", str(dotenv_path)], 0)
        if json.loads(run(["sotto", "ls", "--env", "staging", "--json"], 0).stdout) != [
            "DEMO_SECRET",
            "IMPORTED_KEY",
        ]:
            raise SystemExit("Unexpected secret list in staging after dotenv import.")

        run(["sotto", "lock"], 0)
        if status()["unlocked"] is not False:
            raise SystemExit("Expected session to be locked after sotto lock.")

        run(["sotto", "unlock"], 0)
        if status()["unlocked"] is not True:
            raise SystemExit("Expected session to be unlocked after sotto unlock.")

        run(python, 1)
        print(
            "PASS real Sotto: status -> init -> env ls -> set -> ls -> run -> env copy -> import -> lock/unlock -> direct run still missing"
        )


if __name__ == "__main__":
    main()
