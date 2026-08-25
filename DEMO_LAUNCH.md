# ECON 101 Demo Launch

## Local Demo

Run:

```bash
bash scripts/demo_launch.sh
```

The app will install/update dependencies, compile the app, import-check key pages, and launch at:

```text
http://localhost:8501
```

Use a different port if needed:

```bash
bash scripts/demo_launch.sh 8502
```

## Edit And Relaunch

1. Stop Streamlit with `Ctrl+C`.
2. Edit the app files.
3. Relaunch with `bash scripts/demo_launch.sh`.

For small edits, Streamlit usually hot-reloads automatically. Relaunch after dependency, config, or major import changes.

To force a clean relaunch on the same port:

```bash
bash scripts/relaunch_demo.sh
```

## Student Demo Notes

- For an in-class local demo, project the browser at `http://localhost:8501`.
- For students to open it on their own devices, deploy to a hosted Streamlit service or another public server. A local `localhost` URL only works on your machine.
- Keep `requirements.txt` current whenever a new package is imported.
