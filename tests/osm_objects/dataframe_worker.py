"""Run one get_all_*_as_dataframe function over several models, in its own process.

Usage: python -I dataframe_worker.py <module> <function> <label>=<path> [<label>=<path> ...]

Prints one JSON line per model, flushed before the next model is loaded, so a process killed by a
segfault still reports every model it finished. Driven by test_dataframe_functions.py.
"""

from __future__ import annotations

import importlib
import json
import sys


def main(module: str, function: str, models: list[str]) -> None:
    import openstudio

    fn = getattr(importlib.import_module(f"openstudio_toolkit.osm_objects.{module}"), function)
    translator = openstudio.osversion.VersionTranslator()
    for spec in models:
        label, path = spec.split("=", 1)
        model = translator.loadModel(path).get()
        try:
            df = fn(model)
            line = {"model": label, "rows": len(df), "columns": [str(c) for c in df.columns]}
        except Exception as exc:  # noqa: BLE001 - the failure itself is the result
            line = {"model": label, "error": f"{type(exc).__name__}: {exc}"}
        print(json.dumps(line), flush=True)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3:])
