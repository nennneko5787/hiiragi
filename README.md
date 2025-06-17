# hiiragi

Re-implementation of e-amusement server.

## How to run

```
python3 -m venv venv (if you use windows, run py -m venv venv )
source venv/bin/activate (if you use windows, run ./venv/Scripts/Activate )
pip install -r requirements.txt
uvicorn main:app --host localhost --port 8083
```

## How to make plugin

View [plugins/BeatStream/plugin.py](./plugins/BeatStream/plugin.py).
