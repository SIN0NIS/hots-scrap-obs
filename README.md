**한국어** | [English](README.en.md)

# SinonisObs

히어로즈 오브 더 스톰(Heroes of the Storm) 리플레이·관전용 인터페이스예요.
왼쪽 위 **[메뉴]** 버튼 하나로 화면 UI를 켜고 끄고, 상단바를 영웅 카드(특성·스킬 쿨다운)로 바꿔 볼 수 있어요.

## 출처

- **AhliObs 기반** — Ahli(Christoph Ahlers)의 [Galaxy-Observer-UI](https://github.com/Ahli/Galaxy-Observer-UI) 에 있는 AhliObs 를 바탕으로 수정했어요. AhliObs 는 MIT 라이선스이고, 원 저작권 표기는 [LICENSE](LICENSE) 에 그대로 남겨 두었어요.
- **Spazzo 참고** — 상단바 영웅 카드(특성·스킬 쿨다운 배치)의 디자인은 spazzo966 의 [SpazzoReplayStatKit](https://github.com/spazzo966/SpazzoReplayStatKit) 을 참고했어요. 디자인 아이디어만 참고했고 코드는 가져오지 않았어요.
- 영웅 초상화·특성·스킬 아이콘은 게임 안의 그림을 불러 쓰는 것이고, 블리자드 그림 파일은 들어 있지 않아요. Heroes of the Storm 은 Blizzard Entertainment 의 상표예요.

## 받을 파일

언어에 맞는 파일 하나만 받으면 돼요. 둘 다 넣어 두고 게임에서 골라 써도 돼요.

| 파일 | 메뉴 언어 |
|---|---|
| `SinonisObs_KOR.StormInterface` | 한국어 |
| `SinonisObs_ENG.StormInterface` | English |

## 설치

1. 받은 `.StormInterface` 파일을 아래 폴더에 넣어요. 폴더가 없으면 새로 만들어요.
   ```
   문서\Heroes of the Storm\Interfaces
   ```
   (`Win + R` → `%userprofile%\Documents\Heroes of the Storm\Interfaces` 입력)
2. 게임을 켜고 **설정 → 관전·리플레이** 에서 **리플레이 인터페이스**(관전에도 쓰려면 관전 인터페이스까지)를 `SinonisObs_KOR` 또는 `SinonisObs_ENG` 로 골라요.
3. 리플레이를 열면 바로 적용돼요. 처음에는 기본 리플레이 화면과 똑같이 모든 UI가 보이는 상태로 시작해요.

> 파일을 바꿔 넣을 때는 게임을 끈 상태에서 바꿔야 해요. 켜져 있으면 파일이 잠겨 있어요.

## 사용법 — [메뉴]

왼쪽 위의 작은 **[메뉴]** 버튼을 누르면 설정 창이 열려요. **체크 = 보임** 이에요.

### 화면
| 항목 | 하는 일 |
|---|---|
| UI 전체 | 모든 UI 켜기/끄기 (Ctrl+Alt+U). 꺼도 [메뉴] 버튼은 남아요 |
| 상단바 | 상단 영웅 줄·점수·시간·경험치 바·팀 이름 |
| 미니맵 | 미니맵 |
| 채팅창 | 채팅창 |
| 리플레이 컨트롤 | 재생·속도 조절 박스 |
| 유닛 정보 | 왼쪽 아래 선택한 유닛 정보 (초상화·체력·공격력·기술·버프·영웅 전용 칸) |
| 알림·킬 로그 | 파괴·오브젝트 알림, 아나운서, 킬 로그 |

### 머리 위 이름
- **이름 표시** 로 켜고 끄기 (Ctrl+Alt+N)
- **유저 이름 / 영웅 이름** 중 하나를 골라요

### 상단바 모드
| 모드 | 모습 |
|---|---|
| 기본 | 초상화·체력·마나·궁극기·사망 타이머 |
| 스킬 | 기본 + 영웅 아래 Q·W·E·고유 능력 아이콘. 쓸 수 있으면 밝게, 쿨다운 중이면 회색 + 남은 초 |
| 특성 | 영웅마다 네모 카드. 왼쪽 세로 1·4·7, 모서리 10(궁극기 쿨다운 표시), 아래 가로 13·16·20 특성. 안쪽에 초상화·체력·자원 막대, 죽으면 회색 + 부활 시간 |
| 스킬 + 특성 | 네모 카드 + 그 아래 스킬 쿨다운 |
| 간단 | 초상화·체력·사망 타이머만 |
| 영웅 숨김 | 영웅 줄 없이 시간·팀 킬·레벨·경험치만 |

### 하단 통계 패널 (Ahli)
없음 / 특성 전체 / 사망·공성·영웅 피해 / APM / 경험치 / 사망 시간·치유 / 맵 오브젝트 / 킬·데스·어시 / 적 CC 시간 중 하나 (Ctrl+1~8)

### 체력바 숫자
- **현재 체력**(Ctrl+Alt+H), **최대 체력**(Ctrl+Alt+M), **퍼센트**(Ctrl+Alt+P)를 각각 켜고 꺼요. 모두 켜면 `1234/2000 (62%)`
- 쉴드는 체력에 섞지 않고, 쉴드가 있을 때만 막대 오른쪽에 하늘색 `+320` 으로 따로 나와요

## 직접 빌드

`SinonisObs.StormInterface` 폴더가 소스예요. Ahli 의 Galaxy-Observer-UI 빌더(`compile-spring-boot.jar --compile=<폴더>`)로 묶어요.

- `tools/core_bar.py` — [메뉴] 창을 다시 만들어요
- `tools/top_cards.py` — 상단 영웅 카드를 다시 만들어요 (영웅 데이터 JSON 이 따로 필요해요)
- `tools/make_eng.py` — 문구만 영어로 바꾼 `SinonisObs_ENG.StormInterface` 를 옆에 만들어요
