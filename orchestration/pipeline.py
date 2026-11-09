# Runs the whole pipeline in order and stops at the first failure.
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

DBT = str(Path(sys.executable).with_name("dbt.exe"))  # dbt inside .venv


def step(name, cmd, cwd=None):
    print(f"\n=== {name} ===", flush=True)
    start = time.time()
    result = subprocess.run(cmd, cwd=cwd)
    if result.returncode != 0:
        print(f"\nPIPELINE FAILED at step: {name}. Read the messages above.")
        sys.exit(1)
    print(f"--- {name} done in {time.time() - start:.0f}s")


if __name__ == "__main__":
    print(f"Pipeline started {datetime.now():%Y-%m-%d %H:%M:%S}")
    step("1. Land next batch", [sys.executable, "ingestion/land_next_batch.py"])
    step("2. Build and test with dbt", [DBT, "build", "--profiles-dir", "."], cwd="transform")
    step("3. Update dbt docs", [DBT, "docs", "generate", "--profiles-dir", "."], cwd="transform")
    print(f"\nPIPELINE FINISHED SUCCESSFULLY {datetime.now():%Y-%m-%d %H:%M:%S}")
