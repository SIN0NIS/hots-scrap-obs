# SinonisObs

히어로즈 오브 더 스톰(Heroes of the Storm) 리플레이·관전용 인터페이스예요.
A replay / observer interface for Heroes of the Storm.

## 출처 / Credits

- **AhliObs 기반** — 이 인터페이스는 Ahli(Christoph Ahlers)의 [Galaxy-Observer-UI](https://github.com/Ahli/Galaxy-Observer-UI) 의 AhliObs 를 바탕으로 수정한 것이에요. AhliObs 는 MIT 라이선스이며, 원 저작권 표기는 [LICENSE](LICENSE) 에 그대로 남겨 두었어요.
  Based on AhliObs from Ahli's Galaxy-Observer-UI (MIT). The original copyright notice is kept in LICENSE.
- **Spazzo 참고** — 상단바 영웅 카드(특성·스킬 쿨다운 배치)의 디자인은 spazzo966 의 [SpazzoReplayStatKit](https://github.com/spazzo966/SpazzoReplayStatKit) 을 참고했어요. 디자인 아이디어만 참고했고 코드는 가져오지 않았어요.
  The top-bar hero card design was inspired by spazzo966's SpazzoReplayStatKit. Only the design idea was referenced; no code was copied.
- 영웅 초상화·특성·스킬 아이콘은 게임 안의 그림을 불러 쓰는 것이고, 이 저장소에 블리자드 그림 파일은 들어 있지 않아요. Heroes of the Storm 은 Blizzard Entertainment 의 상표예요.
  Hero portraits and icons are referenced from the game at runtime; no Blizzard art is included.

## 설치 / Install

1. [Releases](../../releases) 에서 `SinonisObs.StormInterface` 를 받아요.
2. `%userprofile%\Documents\Heroes of the Storm\Interfaces` 폴더에 넣어요.
3. 게임 설정 → 관전 및 리플레이 → 리플레이 인터페이스에서 `SinonisObs` 를 골라요.

## 기능 / Features

왼쪽 위 **[메뉴]** 버튼으로 엽니다.

- **화면** — UI 전체, 상단바, 미니맵, 채팅창, 리플레이 컨트롤, 유닛 정보, 알림·킬 로그를 각각 켜고 끄기
- **머리 위 이름** — 끄기 / 유저 이름 / 영웅 이름
- **상단바 모드** — 기본 / 스킬 / 특성 / 스킬 + 특성 / 간단 / 영웅 숨김
  - 특성 모드: 영웅마다 정사각형 카드(1·4·7 왼쪽 세로, 10 모서리, 13·16·20 아래 가로), 초상화·체력·자원 막대, 궁극기 쿨다운, 사망 시 회색
  - 스킬 모드: Q W E 특성 아이콘, 쿨다운 중엔 회색 + 남은 초
- **하단 통계 패널** — Ahli 통계표(Ctrl+1~8)
- **체력바 숫자** — 현재 / 최대 / 퍼센트, 쉴드는 막대 오른쪽에 `+숫자` 로 따로

## 직접 빌드 / Build from source

`SinonisObs.StormInterface` 폴더가 소스예요. Ahli 의 Galaxy-Observer-UI 빌더(`compile-spring-boot.jar --compile=<폴더>`)로 묶어요.
`tools/` 의 스크립트는 메뉴(`core_bar.py`)와 상단 카드(`top_cards.py`)를 다시 만드는 생성기이고, `top_cards.py` 는 영웅 데이터 JSON(herodata)이 따로 있어야 돌아가요.
