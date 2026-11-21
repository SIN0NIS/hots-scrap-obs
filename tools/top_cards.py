# (Re)writes the SinonisObs top-bar hero cards in _TopPanel.StormLayout.  Safe to run again.
#   python top_cards.py
# Card (top-bar modes "특성" / "스킬+특성"): a square per hero replacing Ahli's slanted slot -
#     [ 1][ portrait     ]
#     [ 4][              ]
#     [ 7][ health / mana]
#     [10][13][16][20]      (+ skill row Q W E trait under it in "스킬+특성")
# Skill row alone (mode "스킬"): under Ahli's own health/mana bars.
# Each card holds its own SelectionUnitStatusPanel with an explicit PlayerId (read from this slot's Blizzard talent
# frame), so bars and ability cooldowns follow that player's hero. Talent pictures are borrowed from Blizzard's
# top-bar talent icons ($TalentOverviewL0T1 ...), the portrait from Ahli's slot. Everything is Unclipped (the cards
# hang outside the player frames they live in). Spazzo's kit was only a reference; nothing is copied from it.
import json, pathlib, re

ROOT = pathlib.Path(__file__).parent.parent
LAYOUT = ROOT / "Galaxy-Observer-UI/dev/heroes/hots-scrap-obs_KOR.StormInterface/Base.StormData/UI/Layout/_TopPanel.StormLayout"
HERODATA = ROOT.parent.parent / "hots_archive/builds/hdp5/2.57.0.98348/data/herodata_98348.json"

# measured 2026-10-31: 1 UI unit = ~1.06 px on a 2000 px wide screenshot, hero slots are ~133 apart
CELL, STEP = 28, 30            # talent cell / pitch (vertical): 4 x 30 = 120 high
CELLX, STEPX = 31, 33          # horizontal: 4 x 33 = 132 wide = Ahli's slot pitch (~131.6), so the cards touch
SLOT_TO_BARS = 64              # Ahli's HeroStatus (bars) sits 64 below the top of the hero slot
HEROIC_TOP, HEROIC_LEFT = -31, -16   # heroic icon frame vs the slot bars / placeholder: picture bottom on the bars' top
HEROIC_W, HEROIC_H = 46, 26          # Ahli's 62x36 felt too big (the picture is 8 taller each way: 46x42)
ABIL, ABIL_STEP = 27, 33       # skill icon / pitch (4 across = 132, card width)
TIERS = ["1", "4", "7", "10", "13", "16", "20"]
START, END = "\t<!-- SINONIS TOP CARDS START (tools/top_cards.py) -->\n", "\t<!-- SINONIS TOP CARDS END -->\n"
U = '<Unclipped val="true"/>'


def hero_abilities():
    """unitId -> [Q, W, E, trait] ability ids from HeroesDataParser output."""
    items = json.loads(HERODATA.read_text(encoding="utf-8"))["items"]
    table = {}
    for hero in items.values():
        unit, ab = hero.get("unitId"), hero.get("abilities", {})
        if not unit:
            continue
        basic = {}
        for a in ab.get("Basic", []):
            basic.setdefault(a.get("abilityType"), a.get("abilityId"))
        trait = next((a.get("abilityId") for a in ab.get("Trait", [])), None)
        slots = [basic.get("Q"), basic.get("W"), basic.get("E"), trait]
        if any(slots):
            table[unit] = slots
    return table


def hero_portraits():
    """unitId -> square draft-screen portrait texture (sharp when scaled up, unlike the small party icon)."""
    items = json.loads(HERODATA.read_text(encoding="utf-8"))["items"]
    out = {}
    for hero in items.values():
        unit, pic = hero.get("unitId"), (hero.get("portraits") or {}).get("draftScreen")
        if unit and pic:
            out[unit] = "Assets\\Textures\\" + pic.rsplit(".", 1)[0] + ".dds"
    return out


def templates(table):
    states = []
    for unit, slots in sorted(table.items()):
        acts = "".join(f'\n\t\t\t\t<Action type="SetProperty" frame="Abil{k + 1}" AbilityLink="{a}"/>' for k, a in enumerate(slots) if a)
        hides = "".join(f'\n\t\t\t\t<Action type="SetProperty" frame="Abil{k + 1}" Visible="false"/>' for k, a in enumerate(slots) if not a)
        states.append(f'''			<State name="{unit}">
				<When type="Property" frame="$ancestor[@type=UnitStatusFrame]" unit="{unit}"/>{acts}{hides}
			</State>
''')
    icons = "".join(f'''		<Frame type="UnitStatusAbilIcon" name="Abil{k + 1}">
			<Anchor side="Top" relative="$parent" pos="Min" offset="0"/>
			<Anchor side="Left" relative="$parent" pos="Min" offset="{k * ABIL_STEP + (ABIL_STEP - ABIL) // 2}"/>
			<Width val="{ABIL}"/>
			<Height val="{ABIL}"/>
			<AbilityLink val="NULL"/>
			{U}
			<Frame type="AbilIcon" name="AbilIcon">
				<Anchor relative="$parent"/>
				{U}
				<Frame type="Image" name="IconImage">
					<Anchor relative="$parent"/>
					{U}
				</Frame>
				<!-- dark veil while on cooldown (a tinted white texture does not take the tint: it came out white) -->
				<Frame type="Image" name="CooldownImage">
					<Anchor relative="$parent"/>
					<Texture val="@UI/Storm_Generic_Background_Low"/>
					<Alpha val="140"/>
					<Visible val="false"/>
					{U}
				</Frame>
				<Frame type="Label" name="CooldownLabel">
					<Anchor relative="$parent"/>
					<Style val="SinonisSkillCooldownLabel"/>
					<RenderPriority val="650"/>
					{U}
				</Frame>
				<!-- ready = bright; cooling (the engine shows remaining seconds) = grey + veil + seconds -->
				<StateGroup name="SinonisCooldownLook">
					<DefaultState val="Cooling"/>
					<State name="ReadyHidden">
						<When type="Property" frame="$this/CooldownLabel" visible="false"/>
						<Action type="SetProperty" frame="$this/IconImage" desaturated="false"/>
						<Action type="SetProperty" frame="$this/CooldownImage" visible="false"/>
					</State>
					<State name="ReadyEmpty">
						<When type="Property" frame="$this/CooldownLabel" text=""/>
						<Action type="SetProperty" frame="$this/IconImage" desaturated="false"/>
						<Action type="SetProperty" frame="$this/CooldownImage" visible="false"/>
					</State>
					<State name="Cooling">
						<Action type="SetProperty" frame="$this/IconImage" desaturated="true"/>
						<Action type="SetProperty" frame="$this/CooldownImage" visible="true"/>
					</State>
				</StateGroup>
			</Frame>
		</Frame>
''' for k in range(4))
    pics = hero_portraits()
    pic_states = "".join(f'''			<State name="{unit}">
				<When type="Property" frame="$ancestor[@type=UnitStatusFrame]" unit="{unit}"/>
				<Action type="SetProperty" frame="$this" texture="{tex}"/>
			</State>
''' for unit, tex in sorted(pics.items()))
    portrait = f'''	<!-- card portrait: the hero's square draft-screen picture, picked by the unit this image sits in -->
	<Frame type="Image" name="SinonisPortraitTemplate">
		<RenderPriority val="230"/>
		{U}
		<StateGroup name="SinonisHeroPortrait">
			<DefaultState val="Unknown"/>
{pic_states}			<State name="Unknown"/>
		</StateGroup>
	</Frame>
'''
    return f'''	<!-- skill row: Q W E + trait of the unit this row sits in (a UnitStatusFrame), cooldowns from the engine.
		The ability per hero is set by the state group below (one state per hero, generated from hero data). -->
	<Frame type="Frame" name="SinonisSkillRowTemplate">
		<Width val="{4 * ABIL_STEP}"/>
		<Height val="{ABIL}"/>
		<RenderPriority val="750"/>
		{U}
{icons}		<StateGroup name="SinonisHeroSkills">
			<DefaultState val="Unknown"/>
{"".join(states)}			<State name="Unknown"/>
		</StateGroup>
	</Frame>
'''


def card(i, hero, ind):
    team = f"$Team{1 if i < 5 else 2}HeroOverview"
    src = f"TalentOverview{'L' if i < 5 else 'R'}{i % 5}"
    pid = f"$HeroTalentsPanelContainer/PlayerFrame{i}/TalentsContainerFrame/SelectionUnitStatusPanel/UnitStatusFrame0/HeroSelectedTalentTreeFrame/@PlayerId"
    j = [ind + "\t" * n for n in range(8)]

    def img(name, top, left, w, h, extra, lvl):
        return (f'{j[lvl]}<Frame type="Image" name="{name}">\n'
                f'{j[lvl]}\t<Anchor side="Top" relative="$parent" pos="Min" offset="{top}"/>\n'
                f'{j[lvl]}\t<Anchor side="Left" relative="$parent" pos="Min" offset="{left}"/>\n'
                f'{j[lvl]}\t<Width val="{w}"/>\n{j[lvl]}\t<Height val="{h}"/>\n'
                + "".join(f"{j[lvl]}\t{x}\n" for x in extra) + f"{j[lvl]}\t{U}\n{j[lvl]}</Frame>\n")

    body = [img("Backing", -2, -2, 4 * STEPX + 2, 4 * STEP + 2,
                ['<Texture val="@UI/Storm_Generic_Background_Low"/>', '<RenderPriority val="220"/>'], 5),
            img("Portrait", 0, STEPX + 1, 3 * STEPX - 3, 3 * STEP - 15,
                [f'<Texture val="{{{hero}/HeroPortraitImage/@Texture}}"/>',
                 # 원본 340x124: 세로 전체(124px) x 가로 159px(0.468) = 96:75 칸 비율
                 '<TextureCoords top="0" left="0.475" bottom="1" right="0.943"/>',
                 f'<Desaturated val="{{{hero}/HeroDeathTimeLabel2/@Visible}}"/>',
                 '<RenderPriority val="230"/>'], 5)]   # square hero icon (Ahli's slot portrait is a slanted cut)
    for k, (col, row) in enumerate([(0, 0), (0, 1), (0, 2), (0, 3), (1, 3), (2, 3), (3, 3)], 1):
        body.append(img(f"Cell{k}", row * STEP, col * STEPX, CELLX, CELL,
                        ['<Texture val="@UI/Storm_Generic_Background_Low"/>', '<RenderPriority val="225"/>'], 5))
        body.append(f'''{j[5]}<Frame type="Label" name="Tier{k}">
{j[6]}<Anchor relative="$parent/Cell{k}"/>
{j[6]}<Style val="SinonisTalentTierLabel"/>
{j[6]}<Text val="{TIERS[k - 1]}"/>
{j[6]}<RenderPriority val="240"/>
{j[6]}{U}
{j[5]}</Frame>
{j[5]}<Frame type="Image" name="Icon{k}">
{j[6]}<Anchor relative="$parent/Cell{k}"/>
{j[6]}<Texture val="{{${src}T{k}/IconImage/@Texture}}"/>
{j[6]}<Visible val="{{${src}T{k}/IconImage/@Visible}}"/>
{j[6]}<RenderPriority val="250"/>
{j[6]}{U}
{j[5]}</Frame>
''')
    bars_top = 3 * STEP - 14
    body.append(f'''{j[5]}<Frame type="UnitStatusShieldedHealthBar" name="HealthBar" template="UnitStatus/UnitStatusSegmentedShieldedHealthBarTemplate">
{j[6]}<Anchor side="Top" relative="$parent" pos="Min" offset="{bars_top}"/>
{j[6]}<Anchor side="Left" relative="$parent" pos="Min" offset="{STEPX + 1}"/>
{j[6]}<Anchor side="Right" relative="$parent" pos="Min" offset="{4 * STEPX - 2}"/>
{j[6]}<Anchor side="Bottom" relative="$parent" pos="Min" offset="{bars_top + 8}"/>
{j[6]}<RenderPriority val="240"/>
{j[6]}{U}
{j[5]}</Frame>
{j[5]}<Frame type="UnitStatusEnergyBar" name="EnergyBar" template="UnitStatus/UnitStatusSegmentedEnergyTemplate">
{j[6]}<Anchor side="Top" relative="$parent" pos="Min" offset="{bars_top + 9}"/>
{j[6]}<Anchor side="Left" relative="$parent" pos="Min" offset="{STEPX + 1}"/>
{j[6]}<Anchor side="Right" relative="$parent" pos="Min" offset="{4 * STEPX - 2}"/>
{j[6]}<Anchor side="Bottom" relative="$parent" pos="Min" offset="{bars_top + 13}"/>
{j[6]}<RenderPriority val="240"/>
{j[6]}{U}
{j[5]}</Frame>
{j[5]}<!-- heroic cooldown on the level-10 cell: seconds borrowed from Ahli's heroic icon; cell goes grey while cooling -->
{j[5]}<Frame type="Image" name="HeroicVeil">
{j[6]}<Anchor relative="$parent/Cell4"/>
{j[6]}<Texture val="@UI/Storm_Generic_Background_Low"/>
{j[6]}<Alpha val="150"/>
{j[6]}<Visible val="false"/>
{j[6]}<RenderPriority val="255"/>
{j[6]}{U}
{j[5]}</Frame>
{j[5]}<Frame type="Label" name="HeroicCD">
{j[6]}<Anchor relative="$parent/Cell4"/>
{j[6]}<Style val="SinonisSkillCooldownLabel"/>
{j[6]}<Text val="{{$HeroTalentsPanelContainer/PlayerFrame{i}/TalentsContainerFrame/SelectionUnitStatusPanel/UnitStatusFrame0/UnitStatusAbil/AbilIcon/CooldownLabel/@Text}}"/>
{j[6]}<RenderPriority val="260"/>
{j[6]}{U}
{j[5]}</Frame>
{j[5]}<StateGroup name="SinonisHeroicCooldown">
{j[6]}<DefaultState val="Cooling"/>
{j[6]}<State name="Ready">
{j[7]}<When type="Property" frame="HeroicCD" text=""/>
{j[7]}<Action type="SetProperty" frame="HeroicVeil" visible="false"/>
{j[7]}<Action type="SetProperty" frame="Icon4" desaturated="false"/>
{j[6]}</State>
{j[6]}<State name="Cooling">
{j[7]}<Action type="SetProperty" frame="HeroicVeil" visible="true"/>
{j[7]}<Action type="SetProperty" frame="Icon4" desaturated="true"/>
{j[6]}</State>
{j[5]}</StateGroup>
{j[5]}<!-- death timer, copied from Ahli's slot (faded out in card modes) -->
{j[5]}<Frame type="Label" name="DeathTime">
{j[6]}<Anchor relative="$parent/Portrait"/>
{j[6]}<Style val="SinonisCardDeathLabel"/>
{j[6]}<Text val="{{{hero}/HeroDeathTimeLabel2/@Text}}"/>
{j[6]}<Visible val="{{{hero}/HeroDeathTimeLabel2/@Visible}}"/>
{j[6]}<RenderPriority val="260"/>
{j[6]}{U}
{j[5]}</Frame>
''')
    return f'''{ind}<!-- SINONIS card for this slot (tools/top_cards.py): own SelectionUnitStatusPanel with an explicit PlayerId so the
{ind}	bars and ability cooldowns follow this player's hero; talent pictures borrowed from ${src}T1..T7. -->
{ind}<Frame type="Frame" name="SinonisCard">
{j[1]}<!-- top from the team panel, not the slot: one slot per team sat higher when anchored to its own HeroStatus -->
{j[1]}<Anchor side="Top" relative="{team}" pos="Min" offset="0"/>
{j[1]}<Anchor side="Left" relative="{hero}/HeroPortraitImage" pos="Min" offset="0"/>
{j[1]}<Width val="{4 * STEPX}"/>
{j[1]}<Height val="{4 * STEP}"/>
{j[1]}<RenderPriority val="750"/>
{j[1]}{U}
{j[1]}<Frame type="SelectionUnitStatusPanel" name="SelectionUnitStatusPanel">
{j[2]}<Anchor relative="$parent"/>
{j[2]}<PlayerId val="{{{pid}}}"/>
{j[2]}<HeroesOnly val="True"/>
{j[2]}<AlwaysShowHero val="True"/>
{j[2]}{U}
{j[2]}<Frame type="UnitStatusFrame" name="UnitStatusFrame0">
{j[3]}<Anchor relative="$parent"/>
{j[3]}{U}
{j[3]}<Frame type="Frame" name="Body">
{j[4]}<Anchor relative="$parent"/>
{j[4]}<Visible val="{{$SINONIS_TOP_TALENTS/@Visible}}"/>
{j[4]}{U}
{"".join(body)}{j[3]}</Frame>
{j[3]}<!-- skills under the card (mode "스킬+특성") -->
{j[3]}<Frame type="Frame" name="SkillsUnderCard" template="_TopPanel/SinonisSkillRowTemplate">
{j[4]}<Anchor side="Top" relative="$parent" pos="Min" offset="{4 * STEP + 3}"/>
{j[4]}<Anchor side="Left" relative="$parent" pos="Min" offset="0"/>
{j[4]}<Visible val="{{$SINONIS_TOP_SKILLS2/@Visible}}"/>
{j[3]}</Frame>
{j[3]}<!-- skills under Ahli's own bars (mode "스킬") -->
{j[3]}<Frame type="Frame" name="SkillsUnderBars" template="_TopPanel/SinonisSkillRowTemplate">
{j[4]}<Anchor side="Top" relative="{hero}/HeroStatus" pos="Min" offset="22"/>
{j[4]}<Anchor side="Left" relative="{hero}/HeroStatus" pos="Min" offset="2"/>
{j[4]}<Visible val="{{$SINONIS_TOP_SKILLS1/@Visible}}"/>
{j[3]}</Frame>
{j[2]}</Frame>
{j[1]}</Frame>
{ind}</Frame>
'''


def heroic(t, i, hero):
    """Pin the heroic icon (and Ahli's heroic-cooldown number above it) to this player's own slot: the bottom-left
    corner of the portrait, on Ahli's HeroicPlaceholder (the gap the bars slide right to leave for it). The game lays
    the talent player frames out on its own grid, so the template offsets put the icon between two slots.
    Goes into Ahli's existing TalentsContainerFrame override of PlayerFrame<i> (one frame of a name per parent)."""
    a = t.index(f'name="PlayerFrame{i}" template=')
    nxt = t.find('name="PlayerFrame', a + 20)
    k = t.index('<Frame type="Frame" name="SpecialSingleCDPanel">', a)
    assert nxt < 0 or k < nxt, i
    ls = t.rindex("\n", 0, k) + 1
    ind = t[ls:k]
    ph = f"{hero}/HeroStatus/HeroicPlaceholder"
    tree = (f'{ind}<!-- SINONIS heroic: icon pinned to this slot\'s portrait corner (tools/top_cards.py) -->\n'
            f'{ind}<Frame type="PlayerHeroSelectedTalentTreeFrame" name="HeroSelectedTalentTreeFrame">\n'
            f'{ind}\t<Frame type="UnitStatusTalentIcon" name="TalentTreeIcon4">\n'
            f'{ind}\t\t<Anchor side="Top" relative="{hero}/HeroStatus" pos="Min" offset="{HEROIC_TOP}"/>\n'
            f'{ind}\t\t<Width val="{HEROIC_W}"/>\n'
            f'{ind}\t\t<Height val="{HEROIC_H}"/>\n'
            + (f'{ind}\t\t<Anchor side="Left" relative="{ph}" pos="Min" offset="{HEROIC_LEFT}"/>\n' if i < 5 else
               # red team mirrored: bottom-RIGHT corner (its slots lean the other way, so the left corner is the tail
               # that pokes under the neighbour's portrait); the template's Left anchor is released ($this)
               f'{ind}\t\t<Anchor side="Left" relative="$this" pos="Max" offset="0"/>\n'
               f'{ind}\t\t<Anchor side="Right" relative="{hero}/HeroStatus" pos="Max" offset="{-HEROIC_LEFT + 1}"/>\n')
            + f'{ind}\t</Frame>\n'
            f'{ind}</Frame>\n')
    le = t.index("\n", k) + 1
    anch = (f'{ind}\t<Anchor side="Top" relative="$parent/HeroSelectedTalentTreeFrame/TalentTreeIcon4" pos="Min" offset="{HEROIC_H // 2 - 26 - 5}"/>'
            f'<!-- SINONIS heroic -->\n'
            f'{ind}\t<Anchor side="Left" relative="$parent/HeroSelectedTalentTreeFrame/TalentTreeIcon4" pos="Min" offset="{(HEROIC_W - 62) // 2}"/>'
            f'<!-- SINONIS heroic -->\n')
    return t[:ls] + tree + t[ls:le] + anch + t[le:]


def strip_old(t):
    t = re.sub(r"\n[^\n]*<!-- SINONIS heroic -->(?=\n)", "", t)
    if START in t:
        t = t[:t.index(START)] + t[t.index(END) + len(END):]
    # every generated block starts with a "<!-- SINONIS card" / "<!-- SINONIS skills" comment line and ends with the
    # first closing tag at its own indentation
    for marker, name in (("<!-- SINONIS card", None), ("<!-- SINONIS skills:", None), ("<!-- SINONIS heroic", None)):
        while (i := t.find(marker)) >= 0:
            s = t.rindex("\n", 0, i) + 1
            ind = t[s:i]
            f = t.index(f"\n{ind}<Frame ", i)
            e = t.index(f"\n{ind}</Frame>\n", f) + len(f"\n{ind}</Frame>\n")
            t = t[:s] + t[e:]
    return t


def main():
    t = strip_old(LAYOUT.read_text(encoding="utf-8"))
    t = t.replace("<Desc>\n", "<Desc>\n" + START + templates(hero_abilities()) + END, 1)
    for i in range(10):
        hero = f"$Team{1 if i < 5 else 2}HeroOverview/HeroOverview{i % 5 + 1}"
        m = re.search(r'(\t+)<Frame type="HeroTalentsPanelPlayerFrame" name="PlayerFrame%d" template="_TopPanel/HeroicTalentPlayerFrame(?:Blue|Red)">\n' % i, t)
        t = t[:m.end()] + card(i, hero, m.group(1) + "\t") + t[m.end():]
        t = heroic(t, i, hero)
    # Ahli's heroic / cooldown strip is faded by the menu (core_bar.py) in card modes, never hidden: hidden frames
    # stop counting (the card borrows the heroic cooldown from it) and collapse their layout
    t = re.sub(r'<Visible val="\{\$SINONIS_TOP_AHLISTRIP/@Visible\}"/><!-- SINONIS: hidden in the card modes -->\n\t*', "", t)
    LAYOUT.write_text(t, encoding="utf-8")
    print(f"cards: {t.count('name=\"SinonisCard\"')}, skill rows: {t.count('template=\"_TopPanel/SinonisSkillRowTemplate\"')}")


if __name__ == "__main__":
    main()
