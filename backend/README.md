# shElter-v3 Backend

shElter-v3 鍚庣鍩轰簬 FastAPI 鏋勫缓锛岄噰鐢ㄤ簡 Service-Oriented Monolith 鏋舵瀯锛岄泦鎴愪簡 shElter-v2 鐨勪笟鍔￠€昏緫鍜?shElter-v1 鐨勭壒鑹叉暟鎹紙Metro/Music锛夈€?
## 馃摝 鎶€鏈爤

- **妗嗘灦**: FastAPI 0.109.0
- **鏁版嵁搴?*: PostgreSQL + SQLAlchemy 2.0
- **杩佺Щ宸ュ叿**: Alembic
- **楠岃瘉**: Pydantic 2.0
- **璁よ瘉**: JWT (RS256 闈炲绉板姞瀵?
- **瀹夊叏**: slowapi (Rate Limiting)

## 鉁?鍔熻兘鐗规€?
### 鏍稿績鍔熻兘
- 馃摑 **鏂囩珷绯荤粺** - 鍒涘缓銆佺紪杈戙€佸彂甯冦€佺増鏈帶鍒?- 馃懁 **鐢ㄦ埛绯荤粺** - 娉ㄥ唽銆佺櫥褰曘€丷BAC鏉冮檺鎺у埗
- 馃搨 **鍒嗙被绠＄悊** - 灞傜骇鍒嗙被銆佹爣绛剧郴缁?- 馃挰 **璇勮绯荤粺** - 宓屽璇勮銆佹潈闄愭帶鍒?- 馃攳 **鎼滅储鍔熻兘** - 鍏ㄦ枃鎼滅储銆佽繃婊ゆ帓搴?- 馃懃 **绀句氦鍔熻兘** - 鐢ㄦ埛鍏虫敞銆佸ソ鍙嬪叧绯?
### 鐗硅壊妯″潡
- 馃幍 **闊充箰鎾斁鍣?* - 闊充箰鍒楄〃銆佸厓鏁版嵁绠＄悊
- 馃殗 **鍦伴搧鍦板浘** - 绾胯矾鏁版嵁銆佺珯鐐逛俊鎭?
### 瀹夊叏鐗规€?(v3.1.0)
- 馃攼 JWT RS256 闈炲绉板姞瀵?- 鈴憋笍 Rate Limiting 璇锋眰棰戠巼闄愬埗
- 馃搵 缁熶竴鍝嶅簲鏍煎紡
- 馃洝锔?瀹夊叏鍝嶅簲澶?(HSTS, X-Frame-Options 绛?
- 馃敀 瀵嗙爜 bcrypt 鍝堝笇

## 馃殌 蹇€熷紑濮?
### 鐜瑕佹眰

| 缁勪欢 | 鏈€浣庣増鏈?|
|------|----------|
| Python | 3.10+ |
| PostgreSQL | 15+ |
| Node.js | 18+ (鍓嶇) |

### 1. 鐜鍑嗗

```bash
cd backend
python -m venv venv

# Windows
.\venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 2. 瀹夎渚濊禆

```bash
pip install -r requirements.txt
```

### 3. 鐢熸垚RSA瀵嗛挜 (v3.1.0 瀹夊叏鍗囩骇)

```bash
# 鑷姩鐢熸垚 RSA 瀵嗛挜瀵?python generate_keys.py
```

杩欏皢鍒涘缓锛?- `keys/private_key.pem` - 绉侀挜 (濡ュ杽淇濈!)
- `keys/public_key.pem` - 鍏挜

### 4. 鏁版嵁搴撻厤缃?
鍒涘缓 `.env` 鏂囦欢锛堝弬鑰?`.env.example`锛夛細

```env
# 鏁版嵁搴?DATABASE_URL=postgresql://user:password@localhost/shelter_v3

# JWT 閰嶇疆 (v3.1.0 寮哄埗 RS256)
ALGORITHM=RS256
PRIVATE_KEY_PATH=keys/private_key.pem
PUBLIC_KEY_PATH=keys/public_key.pem
SECRET_KEY=your-secret-key-change-in-production

# Token 璁剧疆
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# 瀹夊叏璁剧疆
DEBUG=False

# Rate Limiting
RATE_LIMIT_ENABLED=True
```

### 5. 鏁版嵁搴撹縼绉?
鍒濆鍖栨暟鎹簱缁撴瀯锛?
```bash
alembic upgrade head
```

### 6. 鏁版嵁杩佺Щ (浠?v1)

濡傛灉浣犻渶瑕佸鍏?shElter-v1 鐨勬暟鎹紝璇锋寜椤哄簭鎵ц浠ヤ笅鑴氭湰锛?
```bash
# 1. 杩佺Щ鐢ㄦ埛鏁版嵁
python scripts/migrate_v1_users.py

# 2. 杩佺Щ鏂囩珷涓庤瘎璁哄唴瀹?python scripts/migrate_v1_content.py

# 3. 澶嶅埗闊充箰鏂囦欢
python scripts/copy_music_files.py
```

### 7. 鍚姩鏈嶅姟

```bash
# 寮€鍙戞ā寮?uvicorn src.main:app --reload

# 鐢熶骇妯″紡
uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
```

鏈嶅姟灏嗗湪 `http://localhost:8000` 鍚姩銆?
## 馃摎 API 鏂囨。

鍚姩鏈嶅姟鍚庯紝璁块棶浠ヤ笅鍦板潃鏌ョ湅瀹屾暣鎺ュ彛鏂囨。锛?
| 鏂囨。 | 鍦板潃 |
|------|------|
| Swagger UI | http://localhost:8000/api/docs |
| ReDoc | http://localhost:8000/api/redoc |
| OpenAPI JSON | http://localhost:8000/api/openapi.json |

### API 绔偣姒傝

| 妯″潡 | 鍓嶇紑 | 鎻忚堪 |
|------|------|------|
| 璁よ瘉 | `/api/v1/auth` | 鐧诲綍銆佹敞鍐屻€佸埛鏂颁护鐗?|
| 鐢ㄦ埛 | `/api/v1/users` | 鐢ㄦ埛璧勬枡銆佸叧娉?|
| 鏂囩珷 | `/api/v1/articles` | CRUD銆佺増鏈帶鍒?|
| 鍒嗙被 | `/api/v1/categories` | 鍒嗙被绠＄悊 |
| 鏍囩 | `/api/v1/tags` | 鏍囩绠＄悊 |
| 璇勮 | `/api/v1/comments` | 璇勮绯荤粺 |
| 鎼滅储 | `/api/v1/search` | 鍏ㄦ枃鎼滅储 |
| Metro | `/api/v1/metro` | 鍦伴搧鏁版嵁 |
| Music | `/api/v1/music` | 闊充箰绠＄悊 |

## 馃幍 闈欐€佽祫婧?
- **闊充箰鏂囦欢**: 鎸傝浇浜?`/static/music`锛屽彲閫氳繃 `/music/filename.mp3` 鐩存帴璁块棶銆?- **Metro API**: `/api/v1/metro` 鎻愪緵鍦伴搧绾胯矾涓庣珯鐐规暟鎹€?- **Music API**: `/api/v1/music` 鎻愪緵闊充箰鍒楄〃涓庡厓鏁版嵁銆?
## 馃И 娴嬭瘯

杩愯娴嬭瘯濂椾欢锛?
```bash
# 鎵€鏈夋祴璇?pytest

# 甯﹁鐩栫巼
pytest --cov=src --cov-report=html

# 鐗瑰畾妯″潡
pytest tests/test_auth.py -v
```

## 鈿欙笍 閰嶇疆璇存槑

### 鐜鍙橀噺

| 鍙橀噺 | 榛樿鍊?| 鎻忚堪 |
|------|--------|------|
| `DATABASE_URL` | - | PostgreSQL 杩炴帴瀛楃涓?|
| `ALGORITHM` | RS256 | JWT 鍔犲瘑绠楁硶 |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | 30 | Access Token 杩囨湡鏃堕棿 |
| `REFRESH_TOKEN_EXPIRE_DAYS` | 7 | Refresh Token 杩囨湡鏃堕棿 |
| `DEBUG` | False | 璋冭瘯妯″紡 |
| `RATE_LIMIT_ENABLED` | True | 鍚敤 Rate Limiting |

### Rate Limiting 閰嶇疆

| 绔偣 | 闄愬埗 |
|------|------|
| `/auth/login` | 10娆?鍒嗛挓 |
| `/auth/register` | 5娆?鍒嗛挓 |
| `/auth/refresh` | 10娆?鍒嗛挓 |
| 鍏朵粬API | 60娆?鍒嗛挓 |

## 馃惓 Docker 閮ㄧ讲

### 浣跨敤 Docker Compose

```bash
# 鏋勫缓骞跺惎鍔?docker-compose up -d

# 鏌ョ湅鏃ュ織
docker-compose logs -f backend

# 鍋滄
docker-compose down
```

### 鏋勫缓闀滃儚

```bash
docker build -t shelter-v3-backend:latest .
```

## 馃搧 椤圭洰缁撴瀯

```
backend/
鈹溾攢鈹€ src/
鈹?  鈹溾攢鈹€ api/              # API 璺敱
鈹?  鈹?  鈹溾攢鈹€ auth.py        # 璁よ瘉鎺ュ彛
鈹?  鈹?  鈹溾攢鈹€ articles.py    # 鏂囩珷鎺ュ彛
鈹?  鈹?  鈹溾攢鈹€ users.py       # 鐢ㄦ埛鎺ュ彛
鈹?  鈹?  鈹斺攢鈹€ ...
鈹?  鈹溾攢鈹€ auth/             # JWT 璁よ瘉
鈹?  鈹?  鈹斺攢鈹€ jwt.py        # RS256 鍔犲瘑
鈹?  鈹溾攢鈹€ core/             # 鏍稿績妯″潡
鈹?  鈹?  鈹溾攢鈹€ response.py   # 缁熶竴鍝嶅簲
鈹?  鈹?  鈹斺攢鈹€ security.py   # Rate Limiter
鈹?  鈹溾攢鈹€ models/           # SQLAlchemy 妯″瀷
鈹?  鈹溾攢鈹€ schemas/          # Pydantic schemas
鈹?  鈹溾攢鈹€ services/         # 涓氬姟閫昏緫
鈹?  鈹溾攢鈹€ utils/            # 宸ュ叿鍑芥暟
鈹?  鈹斺攢鈹€ main.py           # 搴旂敤鍏ュ彛
鈹溾攢鈹€ keys/                 # RSA 瀵嗛挜
鈹溾攢鈹€ alembic/              # 鏁版嵁搴撹縼绉?鈹溾攢鈹€ scripts/              # 鏁版嵁杩佺Щ鑴氭湰
鈹溾攢鈹€ tests/                # 娴嬭瘯
鈹溾攢鈹€ requirements.txt      # Python 渚濊禆
鈹溾攢鈹€ generate_keys.py      # RSA 瀵嗛挜鐢熸垚
鈹斺攢鈹€ Dockerfile
```

## 馃 璐＄尞鎸囧崡

娆㈣繋璐＄尞浠ｇ爜锛佽閬靛惊浠ヤ笅姝ラ锛?
1. **Fork** 鏈粨搴?2. 鍒涘缓鐗规€у垎鏀?(`git checkout -b feature/amazing-feature`)
3. 鎻愪氦鏇存敼 (`git commit -m 'Add amazing feature'`)
4. 鎺ㄩ€佸垎鏀?(`git push origin feature/amazing-feature`)
5. 鍒涘缓 **Pull Request**

### 浠ｇ爜瑙勮寖

- Python: 閬靛惊 PEP 8锛屼娇鐢?`black` 鍜?`isort` 鏍煎紡鍖?- 鎻愪氦淇℃伅: 浣跨敤娓呮櫚鐨勬彁浜や俊鎭牸寮?- 娴嬭瘯: 鏂板姛鑳介渶鍖呭惈瀵瑰簲娴嬭瘯

## 鉂?甯歌闂

### Q: 濡備綍閲嶇疆瀵嗙爜锛?A: 鐩墠鐗堟湰閫氳繃鏁版嵁搴撶洿鎺ヤ慨鏀圭敤鎴疯褰曪紝鎴栫瓑寰呭悗缁増鏈疄鐜板瘑鐮侀噸缃姛鑳姐€?
### Q: 濡備綍娣诲姞绠＄悊鍛樼敤鎴凤紵
A: 杩愯 `python scripts/create_admin.py` 鍒涘缓绠＄悊鍛樿处鎴枫€?
### Q: 濡備綍澶囦唤鏁版嵁锛?A: 浣跨敤 PostgreSQL 鐨?`pg_dump` 鍛戒护杩涜鏁版嵁搴撳浠斤細
```bash
pg_dump -U user shelter_v3 > backup.sql
```

### Q: v3.1.0 鍗囩骇鍚庨渶瑕佸仛浠€涔堬紵
A: 璇峰弬鑰?[UPGRADE_GUIDE.md](../UPGRADE_GUIDE.md) 杩涜鍗囩骇銆?
## 馃搫 鐗堟湰鍘嗗彶

| 鐗堟湰 | 鏃ユ湡 | 鍙樻洿 |
|------|------|------|
| 1.0.0 | 2026-02-12 | 鍒濆鐗堟湰 |
| 3.0.0 | 2026-02-15 | v3 闆嗘垚 |
| **3.1.0** | **2026-02-17** | **瀹夊叏澧炲己 (RS256, Rate Limiting)** |

## 馃摓 鏀寔

濡傛湁闂锛岃鎻愪氦 Issue 鎴栬仈绯荤淮鎶よ€呫€?
---

**shElter-v3** - 鍩轰簬 FastAPI 鐨勭幇浠ｅ寲 Wiki 骞冲彴
