# 피치톡 (PeachTalk)

가벼운 소셜 채팅 앱. 로컬 폴더가 날아간 뒤 이 워크스페이스에 다시 스캐폴드함.

| 항목 | 값 |
|------|-----|
| 제품명 | 피치톡 / PeachTalk |
| 스택 | Flutter + Supabase |
| 패키지 | `peachtalk` |
| 예전 원격 힌트 | `pairappmaster/sliptalk` (현재 이 토큰으로 접근 불가) |
| Mac 워커 경로 | `~/Documents/peachtalk` |

## 빠른 시작

```bash
cd peachtalk
flutter pub get
cp .env.example .env   # Supabase URL / anon key 채우기
flutter run
```

## 폴더

```
lib/
  app/           # 앱 루트, 라우터
  core/          # 테마, 모델, 서비스
  features/
    auth/        # 로그인·온보딩
    home/        # 탭 셸
    chat/        # 채팅 목록·방
    profile/     # 내 프로필
supabase/        # SQL 스키마 초안
```

## 다음 할 일

1. Supabase 프로젝트 연결 (`.env`)
2. 카카오/애플 로그인 붙이기
3. Realtime 채팅 메시지 테이블 연동
4. Mac `~/Documents/peachtalk` 로 이 폴더 복사하거나 새 remote push
