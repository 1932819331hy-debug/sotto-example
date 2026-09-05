import os
import sys

if not os.environ.get("DEMO_SECRET"):
    print("DEMO_SECRET is missing or empty. Set it with `sotto set DEMO_SECRET`, then run this demo with `sotto run -- <command>`.", file=sys.stderr)
    sys.exit(1)

print("Sotto demo: secret loaded successfully.")
