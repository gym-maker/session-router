# session-router (세션분배)

Claude Code 세션 여러 개를 역할(메인 1 + 서브 N)로 나눠, 메인이 사용자 요청을 분류해 서브에 넘기고
현황판·일지·대화 기록으로 세션 간 기억을 나눠 쓰는 스킬.

## 설치

```
git clone https://github.com/gym-maker/session-router ~/.claude/skills/session-router
```

Windows PowerShell이면 `~` 대신 `$HOME`을 쓴다. 설치 뒤 Claude Code를 다시 켜면 스킬이 잡힌다.

## 처음 쓸 때

1. `SKILL.md`의 1절(세션 역할)과 3절(폴더 주인) 표를 내 구성에 맞게 고친다.
2. 서브 세션을 5절 명령으로 띄운다(Remote Control 사용).
3. 메인 세션에서 평소처럼 말하면 메인이 알아서 서브에 넘긴다.

세션 지도 만들기(AI 안 씀): `python ~/.claude/skills/session-router/scripts/make_map.py`
