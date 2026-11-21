# Makes the English copy of hots-scrap-obs_KOR next to it: hots-scrap-obs_ENG.StormInterface.
#   python make_eng.py        (run after core_bar.py / top_cards.py, then build both folders)
# Only GameStrings differ - every Korean value below is swapped for its English text in every locale.
import pathlib
import shutil
import sys

heroes = pathlib.Path(__file__).parent.parent / "Galaxy-Observer-UI/dev/heroes"
src, dst = heroes / "hots-scrap-obs_KOR.StormInterface", heroes / "hots-scrap-obs_ENG.StormInterface"

EN = {
    "Sinonis 옵션": "Sinonis options",
    "UI 전체": "All UI",
    "플레이어 이름": "Player names",
    "HP: 잔여": "HP: current",
    "HP: 최대": "HP: max",
    "HP: 퍼센트": "HP: percent",
    "메뉴": "Menu",
    "화면": "Screen",
    "모든 UI 켜기/끄기 (Ctrl+Alt+U). 꺼도 좌상단 [메뉴]는 남아요": "Show/hide all UI (Ctrl+Alt+U). The top-left [Menu] stays",
    "상단바": "Top bar",
    "상단 영웅 개요(점수·타이머)·맵 점수판·경험치 바·시간·팀 이름": "Top hero overview (score, timer), map score, XP bars, time, team names",
    "미니맵": "Minimap",
    "채팅창": "Chat",
    "리플레이 컨트롤": "Replay controls",
    "리플레이 컨트롤 박스 (관전·리플레이 조절바)": "Replay / observer control box",
    "유닛 정보": "Unit info",
    "좌하단 선택 유닛 정보 (초상화·이름·체력·공격력·기술·버프·영웅 전용 칸)":
        "Bottom-left selected unit info (portrait, name, health, damage, abilities, buffs, hero-specific panels)",
    "알림·킬 로그": "Alerts & kill log",
    "화면 위·좌·우에 뜨는 알림: 파괴·오브젝트, Ahli 알림, 토스트, 목표, 아나운서, 킬 로그":
        "Alerts at the top, left and right: structures, objectives, Ahli alerts, toasts, goals, announcer, kill log",
    "머리 위 이름": "Overhead names",
    "이름 표시": "Show names",
    "머리 위 이름 켜기/끄기 (Ctrl+Alt+N)": "Show/hide overhead names (Ctrl+Alt+N)",
    "유저 이름": "Player name",
    "머리 위에 유저 이름 (닉네임)": "Player (battle tag) name above heroes",
    "영웅 이름": "Hero name",
    "머리 위에 영웅 이름": "Hero name above heroes",
    "상단바 모드": "Top bar mode",
    "기본": "Basic",
    "초상화·체력·마나·궁극기·사망 타이머": "Portrait, health, mana, heroic, death timer",
    "스킬": "Skills",
    "기본 + 영웅 카드 아래 Q·W·E·고유 능력 아이콘과 쿨다운": "Basic + Q, W, E and trait icons with cooldowns under each hero",
    "특성": "Talents",
    "영웅마다 네모 카드: ㄴ자 특성(1·4·7 세로, 10·13·16·20 가로) + 초상화·체력·자원·사망 시간":
        "A square card per hero: L-shaped talents (1/4/7 down, 10/13/16/20 across) + portrait, health, resource, death timer",
    "스킬 + 특성": "Skills + Talents",
    "네모 카드 + 그 아래 Q·W·E·고유 능력 쿨다운": "Square card + Q, W, E and trait cooldowns under it",
    "간단": "Simple",
    "초상화·체력·사망 타이머만 (마나·궁극기·쿨다운 숨김)": "Portrait, health and death timer only (no mana, heroic, cooldowns)",
    "영웅 숨김": "No heroes",
    "영웅 칸·틀 없이 시간·팀 킬·레벨·경험치·핵 체력만": "No hero slots or frame - time, team kills, level, XP and core health only",
    "하단 통계 패널 (Ahli)": "Bottom stats panel (Ahli)",
    "없음": "None",
    "하단 통계 패널 닫기": "Close the bottom stats panel",
    "특성 전체": "All talents",
    "사망·공성·영웅 피해": "Deaths, siege, hero damage",
    "APM": "APM",
    "경험치": "Experience",
    "사망 시간·치유": "Time dead, healing",
    "맵 오브젝트": "Map objectives",
    "킬/데스/어시": "Kills / deaths / assists",
    "적 CC 시간": "Enemy CC time",
    "특성 전체 (Ctrl+1)": "All talents (Ctrl+1)",
    "모든 영웅의 고른 특성": "Talents picked by every hero",
    "사망·공성·영웅 피해 (Ctrl+2)": "Deaths, siege, hero damage (Ctrl+2)",
    "사망, 공성 피해, 영웅 피해, 역할": "Deaths, siege damage, hero damage, role",
    "현재·평균 APM": "Current and average APM",
    "경험치 (Ctrl+4)": "Experience (Ctrl+4)",
    "경험치 기여": "Experience contribution",
    "사망 시간·치유 (Ctrl+5)": "Time dead, healing (Ctrl+5)",
    "사망 시간, 사망, 자힐, 치유": "Time dead, deaths, self healing, healing",
    "맵 오브젝트 (Ctrl+6)": "Map objectives (Ctrl+6)",
    "전장 오브젝트 기여": "Battleground objective contribution",
    "킬/데스/어시 (Ctrl+7)": "Kills / deaths / assists (Ctrl+7)",
    "킬, 데스, 어시스트": "Kills, deaths, assists",
    "적 CC 시간 (Ctrl+8)": "Enemy CC time (Ctrl+8)",
    "적 영웅에게 건 CC 시간": "Crowd control time on enemy heroes",
    "체력바 숫자": "Health bar numbers",
    "현재 체력": "Current HP",
    "체력바 안 현재 체력 (Ctrl+Alt+H)": "Current HP in the health bar (Ctrl+Alt+H)",
    "최대 체력": "Max HP",
    "체력바 안 '/최대 체력' (Ctrl+Alt+M)": "'/max HP' in the health bar (Ctrl+Alt+M)",
    "퍼센트": "Percent",
    "체력바 안 '(62%)' 퍼센트 (Ctrl+Alt+P)": "'(62%)' percent in the health bar (Ctrl+Alt+P)",
    "Sinonis 옵션 (체크 = 보임)": "Sinonis options (checked = shown)",
    "옵션 (체크 = 보임)": "Options (checked = shown)",
    "옵션 열기/닫기 (Ctrl+Alt+O)": "Open/close options (Ctrl+Alt+O)",
    "hots-scrap-obs v1.0.4 · 제작 SINONIS": "hots-scrap-obs v1.0.4 · by SINONIS",
    "AhliObs(MIT) 기반 · Spazzo 디자인 참고": "Based on AhliObs (MIT) · Spazzo-inspired",
    "AI(Claude) 도움을 받아 만들었어요": "Made with help from AI (Claude)",
}

shutil.rmtree(dst, ignore_errors=True)
shutil.copytree(src, dst)
missing = set()
for gs in dst.glob("*.StormData/LocalizedData/GameStrings.txt"):
    raw = gs.read_bytes()
    bom = raw.startswith(b"\xef\xbb\xbf")
    out = []
    for line in raw.decode("utf-8-sig").splitlines():
        key, eq, val = line.partition("=")
        if eq and any("가" <= c <= "힣" for c in val):
            if val in EN:
                val = EN[val]
            else:
                missing.add(val)
        out.append(f"{key}{eq}{val}")
    gs.write_bytes((b"\xef\xbb\xbf" if bom else b"") + ("\r\n".join(out) + "\r\n").encode("utf-8"))
if missing:
    sys.exit("no English text for: " + " | ".join(sorted(missing)))
print(f"made {dst.name}")
