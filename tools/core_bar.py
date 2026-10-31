# (Re)writes the SinonisObs menu panel (opened by the top-left [메뉴] box): the switches used while watching.
#   python core_bar.py
# Safe to run again: SinonisMenuPanel is replaced, the rest of _Sinonis.StormLayout is left alone.
import pathlib

root = pathlib.Path(__file__).parent.parent / "Galaxy-Observer-UI/dev/heroes/hots-scrap-obs_KOR.StormInterface"
lay = root / "Base.StormData/UI/Layout/_Sinonis.StormLayout"
t = lay.read_text(encoding="utf-8")

UC, UL, UU = "UIContainer/ConsoleUIContainer", "UIContainer/FullscreenLowerContainer", "UIContainer/FullscreenUpperContainer"
G = "$parent/$parent/$parent"  # CheckImage -> row -> SinonisMenuPanel -> GameUI
TP = "$HeroTalentsPanelContainer"  # Ahli's top-bar heroic/talent/cooldown strip (one PlayerFrame0-9 per hero)
# ("head", text) group heading, or (id, label, tooltip, default_shown, hotkey, kind, targets)
# kind: fade = panel alpha, vis = state frame visibility
MENU = [
    ("head", "화면"),
    # Ahli's ToggleAllUI is visible while the UI is hidden, hence the inverted state frame
    ("AllUI", "UI 전체", "모든 UI 켜기/끄기 (Ctrl+Alt+U). 꺼도 좌상단 [메뉴]는 남아요", True, "#Hotkey - Toggle all UI", "vis_inv",
     ["$ToggleAllUI"]),
    ("Top", "상단바", "상단 영웅 개요(점수·타이머)·맵 점수판·경험치 바·시간·팀 이름", True, None, "fade",
     [f"{UU}/ObserverHeroOverviewPanel", f"{UU}/TeamPanel", "$LeftTeamXpBar", "$RightTeamXpBar", f"{UU}/TimePanel", f"{UU}/ObserverTeamNamePanel"]),
    ("Minimap", "미니맵", "미니맵", True, None, "fade", [f"{UC}/MinimapPanel"]),
    ("Chat", "채팅창", "채팅창", True, None, "fade", [f"{UU}/ChatDisplay"]),
    ("Replay", "리플레이 컨트롤", "리플레이 컨트롤 박스 (관전·리플레이 조절바)", True, None, "fade", [f"{UU}/ObserverPanelMovingContainer"]),
    ("Selection", "유닛 정보", "좌하단 선택 유닛 정보 (초상화·이름·체력·공격력·기술·버프·영웅 전용 칸)", True, None, "fade",
     [f"{UC}/PortraitPanelContainer", f"{UC}/SelectionUnitStatusPanel", f"{UC}/SelectionUnitStatusPanelTopOverlay",
      f"{UC}/HeroConsolePanel", f"{UC}/HeroBuffDebuffPanel", f"{UC}/CommandPanel", f"{UC}/HeroCharacterSheetPanelContainer",
      f"{UC}/UnitSelectionInfoVerticalPositionControl", f"{UC}/HeroSpecificBackgroundStatusContainer",
      f"{UC}/HeroSpecificStatusContainer", f"{UC}/HeroSpecificFullUIModContainer",
      "UIContainer/ConsolePanel/HeroSpecificCommandCardStatusContainer"]),
    ("Events", "알림·킬 로그", "화면 위·좌·우에 뜨는 알림: 파괴·오브젝트, Ahli 알림, 토스트, 목표, 아나운서, 킬 로그", True, None, "fade",
     [f"{UL}/GameNotificationsPanel", f"{UU}/NotificationsPanel", f"{UU}/ToastPanel", f"{UU}/ObjectiveDisplay",
      f"{UU}/TalkerPanel", f"{UU}/LogMessagePanel", f"{UU}/DirectiveDisplay", "$KillLogPanel"]),
    ("head", "머리 위 이름"),
    ("Names", "이름 표시", "머리 위 이름 켜기/끄기 (Ctrl+Alt+N)", True, "#Hotkey - Toggle Player Names", "vis", ["$SINONIS_NAMES_ON"]),
    # pick-one rows: ("radio", group id, [(row id, label, tooltip)], [(kind, target, value per row)]); row 0 = default
    ("radio", "NameKind", [("User", "유저 이름", "머리 위에 유저 이름 (닉네임)"), ("Hero", "영웅 이름", "머리 위에 영웅 이름")],
     [("vis", "$SINONIS_HERO_NAME_MODE", ["false", "true"])]),
    ("head", "상단바 모드"),
    ("radio", "TopMode",
     [("Basic", "기본", "초상화·체력·마나·궁극기·사망 타이머"),
      ("Skills", "스킬", "기본 + 영웅 카드 아래 Q·W·E·고유 능력 아이콘과 쿨다운"),
      ("Talents", "특성", "영웅마다 네모 카드: ㄴ자 특성(1·4·7 세로, 10·13·16·20 가로) + 초상화·체력·자원·사망 시간"),
      ("Both", "스킬 + 특성", "네모 카드 + 그 아래 Q·W·E·고유 능력 쿨다운"),
      ("Simple", "간단", "초상화·체력·사망 타이머만 (마나·궁극기·쿨다운 숨김)"),
      ("NoHeroes", "영웅 숨김", "영웅 줄 없이 시간·팀 킬·레벨·경험치만")],
     # _TopPanel.StormLayout binds the cards / skill rows / Ahli's strip, slots and mana bars to these state frames
     #                                     기본     스킬     특성     스킬+특성 간단     영웅 숨김
     [("vis", "$SINONIS_TOP_TALENTS",   ["false", "false", "true",  "true",  "false", "false"]),
      ("vis", "$SINONIS_TOP_SKILLS1",   ["false", "true",  "false", "false", "false", "false"]),
      ("vis", "$SINONIS_TOP_SKILLS2",   ["false", "false", "false", "true",  "false", "false"]),
      ("vis", "$SINONIS_TOP_HEROIC",    ["true",  "true",  "true",  "true",  "false", "false"]),
      # Ahli's heroic / cooldown strip: faded, not hidden (the cards borrow its heroic cooldown)
     ] + [("fade", f"$HeroTalentsPanelContainer/PlayerFrame{p}/TalentsContainerFrame", ["255", "255", "0", "0", "255", "255"])
          for p in range(10)] + [
      # Ahli's hero slots: faded, never hidden - a hidden slot collapses and the cards anchored to it pile up
     ] + [("fade", f"$Team{tm}HeroOverview/HeroOverview{n}", ["255", "255", "0", "0", "255", "0"])
          for tm in (1, 2) for n in range(1, 6)] + [
      ("vis", "$SINONIS_TOP_MANA",      ["true",  "true",  "true",  "true",  "false", "false"])]),
    ("head", "하단 통계 패널 (Ahli)"),
    ("radio", "Stats",
     [("None", "없음", "하단 통계 패널 닫기"),
      ("Talents", "특성 전체 (Ctrl+1)", "모든 영웅의 고른 특성"),
      ("Damage", "사망·공성·영웅 피해 (Ctrl+2)", "사망, 공성 피해, 영웅 피해, 역할"),
      ("Apm", "APM (Ctrl+3)", "현재·평균 APM"),
      ("Xp", "경험치 (Ctrl+4)", "경험치 기여"),
      ("Heal", "사망 시간·치유 (Ctrl+5)", "사망 시간, 사망, 자힐, 치유"),
      ("Mechanic", "맵 오브젝트 (Ctrl+6)", "전장 오브젝트 기여"),
      ("Kda", "킬/데스/어시 (Ctrl+7)", "킬, 데스, 어시스트"),
      ("Cc", "적 CC 시간 (Ctrl+8)", "적 영웅에게 건 CC 시간")],
     [("vis", f"$LeaderPanelBottom/{tg}", ["true" if k == i else "false" for k in range(9)])
      for i, tg in enumerate([None, "ToggleTalentOverview", "ToggleDeathsSiegeHeroDmgRole", "ToggleCurApmAvgApm",
                              "ToggleExperience", "ToggleTimeDeadDeathsSelfHealingHealOther", "ToggleMechanic",
                              "ToggleKillsDeathsAssists", "ToggleTimeCCdEnemyHeroes"]) if tg]),
    ("head", "체력바 숫자"),
    ("HpCur", "현재 체력", "체력바 안 현재 체력 (Ctrl+Alt+H)", True, "#Hotkey - Toggle HP Current", "vis", ["$SINONIS_HP_CUR_STATE"]),
    ("HpMax", "최대 체력", "체력바 안 '/최대 체력' (Ctrl+Alt+M)", True, "#Hotkey - Toggle HP Max", "vis", ["$SINONIS_HP_MAX_STATE"]),
    ("HpPct", "퍼센트", "체력바 안 '(62%)' 퍼센트 (Ctrl+Alt+P)", True, "#Hotkey - Toggle HP Percent", "vis", ["$SINONIS_HP_PCT"]),
]
ROW_H, HEAD_H, PANEL_W = 28, 26, 270


def ctrl(kind, target, default_shown):
    path = target if target.startswith("$") else f"{G}/{target}"
    if kind == "fade":  # time 0 = default (shown), ticking fades it out
        return f'''						<Controller type="Fade" end="Pause" frame="{path}">
							<Key type="Curve" time="0" value="255"/>
							<Key type="Curve" time="0.01" value="0"/>
						</Controller>'''
    a, b = ("true", "false") if default_shown else ("false", "true")
    if kind == "vis_inv":
        a, b = b, a
    return f'''						<Controller type="Visibility" end="Pause" frame="{path}">
							<Key type="Bool" time="0" value="{a}"/>
							<Key type="Bool" time="0.01" value="{b}"/>
						</Controller>'''


rows, strings, y = [], {}, 44
for name, handle, vis in (("TopTalents", "SINONIS_TOP_TALENTS", "false"), ("TopHeroic", "SINONIS_TOP_HEROIC", "true"),
                          ("TopHeroes", "SINONIS_TOP_HEROES", "true"), ("TopMana", "SINONIS_TOP_MANA", "true"),
                          ("TopSkills1", "SINONIS_TOP_SKILLS1", "false"), ("TopSkills2", "SINONIS_TOP_SKILLS2", "false"),
                          ("TopAhliStrip", "SINONIS_TOP_AHLISTRIP", "true")):
    rows.append(f'''			<Frame type="Frame" name="Sinonis{name}State">
				<Anchor relative="$parent"/>
				<Visible val="{vis}"/>
				<Handle val="{handle}"/>
			</Frame>
''')
for item in MENU:
    if item[0] == "head":
        hid = f"Head{len(rows)}"
        strings[f"Sinonis/Menu/{hid}"] = item[1]
        rows.append(f'''			<Frame type="Label" name="{hid}">
				<Anchor side="Top" relative="$parent" pos="Min" offset="{y + 4}"/>
				<Anchor side="Left" relative="$parent" pos="Min" offset="12"/>
				<Anchor side="Right" relative="$parent" pos="Max" offset="-12"/>
				<Height val="{HEAD_H - 4}"/>
				<Style val="SinonisMenuHeadLabel"/>
				<Text val="@Sinonis/Menu/{hid}"/>
			</Frame>
''')
        y += HEAD_H
        continue
    if item[0] == "radio":
        # Pick-one rows. CheckBoxes cannot clear each other, so each row is a plain Button whose OnClick animation
        # writes every target's value for that row, plus one "row selected" state frame per row for the ticks.
        # Every key at time 0 is the default (row 0), so the load-time evaluation changes nothing.
        _, gid, choices, targets = item
        n = len(choices)
        sel = [f"SINONIS_{gid.upper()}_{rid.upper()}" for rid, _, _ in choices]
        for k, (rid, _, _) in enumerate(choices):
            rows.append(f'''			<Frame type="Frame" name="{gid}{rid}State">
				<Anchor relative="$parent"/>
				<Visible val="{'true' if k == 0 else 'false'}"/>
				<Handle val="{sel[k]}"/>
			</Frame>
''')
        for k, (rid, label, tip) in enumerate(choices):
            strings[f"Sinonis/Menu/{gid}{rid}"] = label
            strings[f"Sinonis/Menu/Tip/{gid}{rid}"] = tip
            ctr = []
            for kind, path, vals in targets + [("vis", f"${sel[j]}", ["true" if j == 0 else "false"] + ["true" if j == m else "false" for m in range(1, n)])
                                               for j in range(n)]:
                v0, v1 = vals[0], vals[k]
                if kind == "fade":
                    ctr.append(f'''						<Controller type="Fade" end="Pause" frame="{path}">
							<Key type="Curve" time="0" value="{v0}"/>
							<Key type="Curve" time="0.01" value="{v1}"/>
						</Controller>''')
                else:
                    ctr.append(f'''						<Controller type="Visibility" end="Pause" frame="{path}">
							<Key type="Bool" time="0" value="{v0}"/>
							<Key type="Bool" time="0.01" value="{v1}"/>
						</Controller>''')
            rows.append(f'''			<Frame type="Frame" name="Menu{gid}{rid}">
				<Anchor side="Top" relative="$parent" pos="Min" offset="{y}"/>
				<Anchor side="Left" relative="$parent" pos="Min" offset="20"/>
				<Anchor side="Right" relative="$parent" pos="Max" offset="-12"/>
				<Height val="{ROW_H - 2}"/>
				<Frame type="Image" name="Box">
					<Anchor side="Top" relative="$parent" pos="Min" offset="0"/>
					<Anchor side="Left" relative="$parent" pos="Min" offset="0"/>
					<Width val="22"/>
					<Height val="22"/>
					<Texture val="@UI/Storm_Checkbox_Normal"/>
					<AcceptsMouse val="false"/>
				</Frame>
				<Frame type="Image" name="Tick">
					<Anchor relative="$parent/Box"/>
					<Texture val="@UI/Storm_Checkbox_CheckMark"/>
					<AcceptsMouse val="false"/>
					<Visible val="{{${sel[k]}/@Visible}}"/>
				</Frame>
				<Frame type="Label" name="Label">
					<Anchor side="Top" relative="$parent/Box" pos="Min" offset="0"/>
					<Anchor side="Bottom" relative="$parent/Box" pos="Max" offset="0"/>
					<Anchor side="Left" relative="$parent/Box" pos="Max" offset="8"/>
					<Anchor side="Right" relative="$parent" pos="Max" offset="0"/>
					<Style val="SinonisCoreBarLabel"/>
					<Text val="@Sinonis/Menu/{gid}{rid}"/>
					<AcceptsMouse val="false"/>
				</Frame>
				<Frame type="Button" name="Click">
					<Anchor relative="$parent"/>
					<Tooltip val="@Sinonis/Menu/Tip/{gid}{rid}"/>
					<Animation name="Select">
						<Event event="OnClick" action="Restart,DirectionForward,Play"/>
{chr(10).join(ctr)}
					</Animation>
				</Frame>
			</Frame>
''')
            y += ROW_H
        continue
    cid, label, tip, shown, hotkey, kind, targets = item
    strings[f"Sinonis/Menu/{cid}"] = label
    strings[f"Sinonis/Menu/Tip/{cid}"] = tip
    ctrls = [ctrl(kind, tg, shown) for tg in targets]
    mark = ""
    if shown:
        ctrls.append('''						<Controller type="Visibility" end="Pause" frame="$parent/ShownMark">
							<Key type="Bool" time="0" value="true"/>
							<Key type="Bool" time="0.01" value="false"/>
						</Controller>''')
        mark = '''				<Frame type="Image" name="ShownMark">
					<Anchor relative="$parent/Button"/>
					<Texture val="@UI/Storm_Checkbox_CheckMark"/>
					<AcceptsMouse val="false"/>
				</Frame>
'''
    sc = f'\n					<Shortcut val="{hotkey}"/>' if hotkey else ""
    rows.append(f'''			<Frame type="CheckBox" name="Menu{cid}" template="_Sinonis/SinonisMenuRowTemplate">
				<Anchor side="Top" relative="$parent" pos="Min" offset="{y}"/>
				<Anchor side="Left" relative="$parent" pos="Min" offset="20"/>
				<Anchor side="Right" relative="$parent" pos="Max" offset="-12"/>
				<Height val="{ROW_H - 2}"/>
				<Toggled val="false"/>
				<Tooltip val="@Sinonis/Menu/Tip/{cid}"/>
				<Frame type="Button" name="Button">
					<Width val="22"/>
					<Height val="22"/>{sc}
				</Frame>
{mark}				<Frame type="Image" name="CheckImage">
{'					<Alpha val="0"/>' + chr(10) if shown else ''}					<Animation name="Apply">
						<Event event="OnShown" action="DirectionForward,Play"/>
						<Event event="OnHidden" action="DirectionReverse,Play"/>
{chr(10).join(ctrls)}
					</Animation>
				</Frame>
				<Frame type="Label" name="Label">
					<Style val="SinonisCoreBarLabel"/>
					<Text val="@Sinonis/Menu/{cid}"/>
				</Frame>
			</Frame>
''')
    y += ROW_H
height = y + 12

panel = f'''		<!-- the [메뉴] panel: the switches used while watching. Every box starts empty (Toggled is ignored in
			replays): empty = default, tick = changed. Rows whose default is "shown" draw ShownMark while empty,
			so on screen a tick still means "shown". Generated by tools/core_bar.py - edit there. -->
		<Frame type="Frame" name="SinonisMenuPanel">
			<Anchor side="Top" relative="$parent/SinonisMenuButton" pos="Max" offset="4"/>
			<Anchor side="Left" relative="$parent" pos="Min" offset="-9994"/>
			<Width val="{PANEL_W}"/>
			<Height val="{height}"/>
			<RenderPriority val="900"/>

			<Frame type="Image" name="LowImage">
				<Anchor relative="$parent"/>
				<TextureType val="Normal"/>
				<Texture val="@UI/Storm_Generic_Background_Low"/>
				<Alpha val="215"/>
			</Frame>

			<Frame type="Label" name="Title">
				<Anchor side="Top" relative="$parent" pos="Min" offset="8"/>
				<Anchor side="Left" relative="$parent" pos="Min" offset="12"/>
				<Anchor side="Right" relative="$parent" pos="Max" offset="-12"/>
				<Style val="AhliControlsHeader"/>
				<Text val="@Sinonis/MenuTitle"/>
			</Frame>

{"".join(rows)}		</Frame>
'''
# drop the earlier top-centre bar, replace the menu panel
START, END = "\t\t<!-- CORE BAR START -->\n", "\t\t<!-- CORE BAR END -->\n"
if START in t:
    t = t[:t.index(START)] + t[t.index(END) + len(END):]
s = t.index("\t\t<Frame type=\"Frame\" name=\"SinonisMenuPanel\">")
if "<!-- the [메뉴] panel" in t[:s]:
    s = t.rindex("\t\t<!-- the [메뉴] panel", 0, s)
e = t.index("\t</Frame>\n\n\t<!-- CC timer")
t = t[:s] + panel + t[e:]
# --- hero-name twins ------------------------------------------------------------------------------
# Ahli re-templates PlayerUnitNameLabel in ~30 hero nameplate templates, and most of them have their own
# HeroUnitStatusParentFrame, so a label added to one base template never reaches them. Every one of those
# parents gets a twin of the player-name label: same rect (anchored onto it), same label layout and style,
# but NameType Unit, shown only in hero-name mode (the player-name label is hidden then).
import re  # noqa: E402
us = (root / "Base.StormData/UI/Layout/_UnitStatus.StormLayout").read_text(encoding="utf-8")
us_live = re.sub(r"<!--.*?-->", "", us, flags=re.S)
parents = re.findall(r'<Frame type="UnitStatusName" name="([^"]+)/HeroUnitStatusParentFrame/PlayerUnitNameLabel" file="([^"]+)"', us_live)
twins = "".join(f'''	<Frame type="Frame" name="{tmpl}/HeroUnitStatusParentFrame" file="{fname}">
		<Frame type="UnitStatusName" name="SinonisHeroNameLabel">
			<Anchor relative="$parent/PlayerUnitNameLabel"/>
			<NameType val="Unit"/>
			<UseNameTypeVisibilityRules val="False"/>
			<VisibleToOwner val="{{$SINONIS_HERO_NAME_SHOW/@Visible}}"/>
			<VisibleToAlly val="{{$SINONIS_HERO_NAME_SHOW/@Visible}}"/>
			<VisibleToEnemy val="{{$SINONIS_HERO_NAME_SHOW/@Visible}}"/>
			<Frame type="Label" name="Label">
				<Anchor side="Top" relative="$parent" pos="Min" offset="0"/>
				<Anchor side="Left" relative="$parent" pos="Mid" offset="0"/>
				<Anchor side="Right" relative="$parent" pos="Mid" offset="0"/>
				<Style val="Storm_UnitNameLabel"/>
			</Frame>
		</Frame>
	</Frame>
''' for tmpl, fname in parents)
TW_START, TW_END = "\t<!-- HERO NAME TWINS START (tools/core_bar.py) -->\n", "\t<!-- HERO NAME TWINS END -->\n"
if TW_START in t:
    t = t[:t.index(TW_START)] + t[t.index(TW_END) + len(TW_END):]
old = t.find("\t<!-- hero-name label on the player-name spot")
if old >= 0:  # the single hand-written label this replaces
    t = t[:old] + t[t.index("\t</Frame>\n", t.index("</Frame>\n\t</Frame>", old)) + len("\t</Frame>\n"):]
t = t.replace("</Desc>", TW_START + twins + TW_END + "</Desc>")
lay.write_text(t, encoding="utf-8")
print(f"hero-name twins: {len(parents)}")

st = root / "Base.StormData/UI/FontStyles.StormStyle"
s = st.read_text(encoding="utf-8")
if "SinonisMenuHeadLabel" not in s:
    s = s.replace('\t<Style name="SinonisCoreBarLabel"',
                  '\t<Style name="SinonisMenuHeadLabel" template="StandardTemplate" height="13" textcolor="FFD24A" vjustify="Bottom" hjustify="Left" styleflags="!Shadow" fontflags="Outline"/>\n\t<Style name="SinonisCoreBarLabel"', 1)
    st.write_text(s, encoding="utf-8")

for gs in root.glob("*.StormData/LocalizedData/GameStrings.txt"):
    raw = gs.read_bytes()
    bom = raw.startswith(b"\xef\xbb\xbf")
    lines = [l for l in raw.decode("utf-8-sig").splitlines()
             if l and not l.startswith(("Sinonis/Core/", "Sinonis/Menu/", "Sinonis/MenuTitle="))]
    lines += [f"{k}={v}" for k, v in strings.items()] + ["Sinonis/MenuTitle=Sinonis 옵션 (체크 = 보임)"]
    gs.write_bytes((b"\xef\xbb\xbf" if bom else b"") + ("\r\n".join(lines) + "\r\n").encode("utf-8"))
print(f"menu: {sum(1 for m in MENU if m[0] != 'head')} switches, panel {PANEL_W}x{height}")
