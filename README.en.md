[한국어](README.md) | **English**

# hots-scrap-obs (SinonisObs)

A replay / observer interface for Heroes of the Storm.
One small **[Menu]** button in the top-left corner shows and hides parts of the UI, and turns the top bar into hero cards with talents and ability cooldowns.

## ⬇ Download

### [English (ENG)](https://github.com/SIN0NIS/hots-scrap-obs/releases/latest/download/hots-scrap-obs_ENG.StormInterface) · [한국어 (KOR)](https://github.com/SIN0NIS/hots-scrap-obs/releases/latest/download/hots-scrap-obs_KOR.StormInterface)

The file downloads right away. Save it into this folder:

```
%userprofile%\Documents\Heroes of the Storm\Interfaces
```

Then pick `hots-scrap-obs_ENG` (or `_KOR`) in game under **Options → Observer / Replay → Replay Interface**. Done.

## Credits

- **v1.0.0** · made by **SINONIS**, with help from AI (Claude).

- **Based on AhliObs** — modified from AhliObs in Ahli's (Christoph Ahlers) [Galaxy-Observer-UI](https://github.com/Ahli/Galaxy-Observer-UI). AhliObs is MIT licensed; the original copyright notice is kept in [LICENSE](LICENSE).
- **Inspired by Spazzo** — the top-bar hero card design (talent and cooldown layout) was inspired by spazzo966's [SpazzoReplayStatKit](https://github.com/spazzo966/SpazzoReplayStatKit). Only the design idea was referenced; no code was copied.
- Hero portraits and talent / ability icons are referenced from the game at runtime; no Blizzard art is included. Heroes of the Storm is a trademark of Blizzard Entertainment.

## Downloads

Pick the file for your language. You can also install both and choose in game.

| File | Menu language |
|---|---|
| `hots-scrap-obs_KOR.StormInterface` | Korean |
| `hots-scrap-obs_ENG.StormInterface` | English |

## Install

1. Put the `.StormInterface` file in this folder (create it if it does not exist):
   ```
   Documents\Heroes of the Storm\Interfaces
   ```
   (`Win + R` → `%userprofile%\Documents\Heroes of the Storm\Interfaces`)
2. Start the game, open **Options → Observer / Replay** and set **Replay Interface** (and Observer Interface, if you want it there too) to `hots-scrap-obs_KOR` or `hots-scrap-obs_ENG`.
3. Open a replay. It starts like the default replay screen, with all UI shown.

> Swap the file only while the game is closed; the game locks it while running.

## How to use — [Menu]

Click the small **[Menu]** button in the top-left corner. **Checked = shown.**

### Screen
| Item | What it does |
|---|---|
| All UI | Show/hide all UI (Ctrl+Alt+U). The [Menu] button stays |
| Top bar | Top hero row, score, time, XP bars, team names |
| Minimap | Minimap |
| Chat | Chat |
| Replay controls | Play / speed control box |
| Unit info | Bottom-left selected unit info (portrait, health, damage, abilities, buffs, hero-specific panels) |
| Alerts & kill log | Structure / objective alerts, announcer, kill log |

### Overhead names
- **Show names** on/off (Ctrl+Alt+N)
- Pick **Player name** or **Hero name**

### Top bar mode
| Mode | Looks like |
|---|---|
| Basic | Portrait, health, mana, heroic, death timer |
| Skills | Basic + Q, W, E and trait icons under each hero. Bright when ready, grey + seconds left while on cooldown |
| Talents | A square card per hero. Talents 1/4/7 down the left, 10 in the corner (shows the heroic cooldown), 13/16/20 along the bottom. Portrait, health and resource bars inside; grey + respawn time while dead |
| Skills + Talents | Square card + ability cooldowns under it |
| Simple | Portrait, health and death timer only |
| No heroes | Time, team kills, level and XP only |

### Bottom stats panel (Ahli)
None / All talents / Deaths, siege, hero damage / APM / Experience / Time dead, healing / Map objectives / Kills, deaths, assists / Enemy CC time (Ctrl+1–8)

### Health bar numbers
- Turn **Current HP** (Ctrl+Alt+H), **Max HP** (Ctrl+Alt+M) and **Percent** (Ctrl+Alt+P) on or off. All on: `1234/2000 (62%)`
- Shields are not mixed into health: while a hero has a shield, it shows separately as a light-blue `+320` just right of the bar

## Build from source

The `hots-scrap-obs_KOR.StormInterface` folder is the source. Pack it with Ahli's Galaxy-Observer-UI builder (`compile-spring-boot.jar --compile=<folder>`).

- `tools/core_bar.py` — regenerates the [Menu] panel
- `tools/top_cards.py` — regenerates the top-bar hero cards (needs a separate hero data JSON)
- `tools/make_eng.py` — makes `hots-scrap-obs_ENG.StormInterface` next to it, with English text only
