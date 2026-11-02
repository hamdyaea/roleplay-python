# Fantasy RPG Adventure — Python

**Developer:** Hamdy Abou El Anein  
**Contact:** info@daylightlinux.ch  
**License:** GPL v3 (see LICENSE).

A terminal role-playing game written in Python 3 using `rich` and `click`. The current maintenance update fixes independent inventory defaults for each player and handles multiple level-ups correctly when experience rewards cross several thresholds. The existing game flow and terminal interface are preserved.

```sh
python3 -m pip install rich click
python3 play.py
python3 -m unittest discover -s tests -v
```

Historical source: [old branch](https://github.com/hamdyaea/roleplay-python/tree/old).
