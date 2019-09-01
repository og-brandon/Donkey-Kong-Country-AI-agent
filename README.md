# dkc-ai-bot

`pip install -r requirements.txt`

You will need a rom file for Donkey Kong Country and do `python -m retro.import` to import it

go to `site-packages\retro\data\stable\DonkeyKongCountry-Snes` and add this to `data.json`:
```
"x": {
    "address": 8257726,
    "type": "<u2"
  }
```


`python training.py` to train from zero 

`python training.py #` and replace `#` to train from a generation checkpoint