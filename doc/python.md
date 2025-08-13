
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

-----------EXAMPLE
1. Check Python and create a virtual environment (macOS)

```python
python3 --version
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
```
1. Add httpx to your requirements and install
```python
echo "httpx>=0.27.0" >> requirements.txt
pip install -r requirements.txt
```

