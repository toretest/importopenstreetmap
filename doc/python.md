
when run
```python
python3 -m venv .venv
```


Python creates

.venv/
├── bin/            ← Python, pip, and activation scripts
├── lib/            ← All installed packages go here
├── pyvenv.cfg


```python
source .venv/bin/activate
```

Temporarily changes the PATH so that python and pip point to .venv/bin/python and .venv/bin/pip.

Overrides the system Python — but only in that terminal session.

which python    # → .venv/bin/python
pip install xyz # → installs into .venv/lib/