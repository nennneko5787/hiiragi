# hiiragi

> The name of the repository was derived from 柊<ひいらぎ>(holly olive).

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

## Todo
- [ ] Full support of BeatStream and MÚSECA
- [ ] Create plugins other than BeatStream
- [ ] Database support (psql/sqlite/mysql)

## Special thanks
- [bemaniutils](https://github.com/DragonMinded/bemaniutils) - Protocol implementation.
- [eamuse.bsnk.me](https://eamuse.bsnk.me/) - Information for implementation.  
thanks.