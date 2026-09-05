"""Exercise the real local Sotto flow on a disposable Linux CI runner only."""

import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def main():
    # SOTTO_DATA_DIR does not isolate OS-keychain entries. Never initialise a
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
            result = subprocess.run(command, cwd=folder, env=env, input=stdin, text=True, capture_output=True, timeout=120)
            if result.returncode != expected:
                raise SystemExit(f"Unexpected exit status from {command[0]}; output withheld to keep the Emergency Kit private.")
            return result

        python = [sys.executable, str(ROOT / "python/main.py")]
        run(python, 1)
        run(["sotto", "init", "--name", "sotto-example"], 0)
        run(["sotto", "set", "DEMO_SECRET", "--stdin"], 0, "hello-from-sotto")
        result = run(["sotto", "run", "--", *python], 0)
        if result.stdout != "Sotto demo: secret loaded successfully.\n":
            raise SystemExit("Unexpected demo output (withheld).")
        run(python, 1)
        print("PASS real Sotto: missing -> init -> set -> injected success -> direct run still missing")


if __name__ == "__main__":
    main()
