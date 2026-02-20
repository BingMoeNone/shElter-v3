# shElter-v3

[![Version](https://img.shields.io/badge/version-3.1.0-blue)](https://github.com/shelter-v3)
[![Python](https://img.shields.io/badge/python-3.10+-green)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/fastapi-0.109.0-blue)](https://fastapi.tiangolo.com/)
[![Vue](https://img.shields.io/badge/vue-3.x-green)](https://vuejs.org/)
[![License](https://img.shields.io/badge/license-MIT-yellow)](LICENSE)

> 鍩轰簬 FastAPI + Vue 3 鐨勭幇浠ｅ寲 Wiki 骞冲彴锛屾敮鎸佹枃绔犵鐞嗐€佺敤鎴风ぞ浜ゃ€侀煶涔愭挱鏀俱€佸湴閾佸湴鍥剧瓑鐗硅壊鍔熻兘銆?
## 鉁?椤圭洰浠嬬粛

shElter-v3 鏄竴涓幇浠ｅ寲鐨?Wiki 骞冲彴锛岄噰鐢ㄥ墠鍚庣鍒嗙鏋舵瀯锛岄泦鎴愪簡浠ヤ笅鏍稿績鍔熻兘锛?
- 馃摑 **鏂囩珷绯荤粺** - Markdown 鏀寔銆佺増鏈帶鍒躲€佹潈闄愮鐞?- 馃懃 **绀句氦鍔熻兘** - 鐢ㄦ埛鍏虫敞銆佸ソ鍙嬪叧绯汇€佷釜浜轰富椤?- 馃幍 **闊充箰鎾斁鍣?* - 姝屽崟绠＄悊銆佸湪绾挎挱鏀?- 馃殗 **鍦伴搧鍦板浘** - 绾胯矾灞曠ず銆佺珯鐐规煡璇?- 馃攳 **鎼滅储鍔熻兘** - 鍏ㄦ枃鎼滅储銆佸垎绫绘祻瑙?- 馃攼 **瀹夊叏璁よ瘉** - JWT RS256銆丷ate Limiting

## 馃彈锔?椤圭洰鏋舵瀯

```
shElter-v3/
鈹溾攢鈹€ backend/              # FastAPI 鍚庣
鈹?  鈹溾攢鈹€ src/
鈹?  鈹?  鈹溾攢鈹€ api/         # API 璺敱
鈹?  鈹?  鈹溾攢鈹€ auth/        # JWT 璁よ瘉 (RS256)
鈹?  鈹?  鈹溾攢鈹€ core/        # 鏍稿績妯″潡
鈹?  鈹?  鈹溾攢鈹€ models/      # 鏁版嵁搴撴ā鍨?鈹?  鈹?  鈹斺攢鈹€ services/    # 涓氬姟閫昏緫
鈹?  鈹溾攢鈹€ keys/            # RSA 瀵嗛挜
鈹?  鈹溾攢鈹€ alembic/         # 鏁版嵁搴撹縼绉?鈹?  鈹斺攢鈹€ tests/           # 娴嬭瘯
鈹?鈹溾攢鈹€ frontend/            # Vue 3 鍓嶇
鈹?  鈹溾攢鈹€ src/
鈹?  鈹?  鈹溾攢鈹€ components/  # Vue 缁勪欢
鈹?  鈹?  鈹溾攢鈹€ views/       # 椤甸潰瑙嗗浘
鈹?  鈹?  鈹溾攢鈹€ stores/      # Pinia 鐘舵€佺鐞?鈹?  鈹?  鈹斺攢鈹€ services/    # API 鏈嶅姟
鈹?  鈹斺攢鈹€ ...
鈹?鈹溾攢鈹€ specs/               # 椤圭洰瑙勮寖鏂囨。
鈹溾攢鈹€ docker-compose.yml   # Docker 缂栨帓
鈹斺攢鈹€ README.md
```

## 馃搳 鐗堟湰瀵规瘮

| 鐗堟湰 | 璇勫垎 | 鎶€鏈爤 | 鐗圭偣 |
|------|------|--------|------|
| **v1** | 58/100 | PHP | 鍘熷鐗堟湰锛屽姛鑳藉畬鏁翠絾瀹夊叏宸?|
| **v2** | 84/100 | FastAPI + Vue | 鐜颁唬鍖栭噸鏋勶紝瀹夊叏瀹屽杽 |
| **v3** | 83/100 | FastAPI + Vue | Docker 浼樺寲锛屽畨鍏ㄥ寮?|

**褰撳墠鐗堟湰**: v3.1.0 (Security Enhanced)

## 馃殌 蹇€熷紑濮?
### 鍓嶇疆瑕佹眰

| 缁勪欢 | 瑕佹眰 |
|------|------|
| Python | 3.10+ |
| Node.js | 18+ |
| PostgreSQL | 15+ (鍙€?SQLite 寮€鍙? |
| Docker | 20+ (鎺ㄨ崘) |

### Docker 閮ㄧ讲 (鎺ㄨ崘)

```bash
# 鍏嬮殕椤圭洰
git clone https://github.com/your-repo/shelter-v3.git
cd shelter-v3

# 鍚姩鏈嶅姟
docker-compose up -d

# 璁块棶搴旂敤
# 鍓嶇: http://localhost:5173
# 鍚庣: http://localhost:8000
# API 鏂囨。: http://localhost:8000/api/docs
```

### 鎵嬪姩閮ㄧ讲

#### 1. 鍚庣璁剧疆

```bash
cd backend

# 鍒涘缓铏氭嫙鐜
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 鎴?.\venv\Scripts\activate  # Windows

# 瀹夎渚濊禆
pip install -r requirements.txt

# 鐢熸垚 RSA 瀵嗛挜
python generate_keys.py

# 閰嶇疆鐜鍙橀噺
cp .env.example .env
# 缂栬緫 .env 鏂囦欢

# 鍚姩鏈嶅姟
uvicorn src.main:app --reload
```

#### 2. 鍓嶇璁剧疆

```bash
cd frontend

# 瀹夎渚濊禆
npm install

# 鍚姩寮€鍙戞湇鍔″櫒
npm run dev
```

## 馃摉 浣跨敤鎸囧崡

### 鐢ㄦ埛鍔熻兘

1. **娉ㄥ唽/鐧诲綍** - 璁块棶 `/login` 鎴?`/register`
2. **鍒涘缓鏂囩珷** - 鐧诲綍鍚庣偣鍑?鏂板缓鏂囩珷"
3. **缂栬緫鏂囩珷** - 鏂囩珷椤甸潰鐐瑰嚮"缂栬緫"鎸夐挳
4. **绀句氦浜掑姩** - 鍏虫敞鐢ㄦ埛銆佸彂琛ㄨ瘎璁?
### API 浣跨敤

```bash
# 鐧诲綍鑾峰彇 Token
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","username":"user","password":"Password123"}'

# 浣跨敤 Token 璁块棶鍙椾繚鎶よ祫婧?curl -X GET http://localhost:8000/api/v1/articles \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 鈿欙笍 閰嶇疆璇存槑

### 鐜鍙橀噺

| 鍙橀噺 | 榛樿鍊?| 璇存槑 |
|------|--------|------|
| `DATABASE_URL` | SQLite | 鏁版嵁搴撹繛鎺?|
| `ALGORITHM` | RS256 | JWT 鍔犲瘑绠楁硶 |
| `DEBUG` | False | 璋冭瘯妯″紡 |
| `RATE_LIMIT_ENABLED` | True | 鍚敤棰戠巼闄愬埗 |

### 瀹夊叏閰嶇疆 (v3.1.0)

- JWT: RS256 闈炲绉板姞瀵?- Rate Limiting: slowapi
- 瀵嗙爜: bcrypt 鍝堝笇
- 瀹夊叏澶? HSTS, X-Frame-Options 绛?
## 馃И 娴嬭瘯

```bash
# 鍚庣娴嬭瘯
cd backend
pytest --cov=src

# 鍓嶇娴嬭瘯
cd frontend
npm run test
```

## 馃搧 椤圭洰鏂囨。

| 鏂囨。 | 璇存槑 |
|------|------|
| [backend/README.md](backend/README.md) | 鍚庣璇︾粏鏂囨。 |
| [UPGRADE_GUIDE.md](UPGRADE_GUIDE.md) | v3.1.0 鍗囩骇鎸囧崡 |
| [SECURITY_AUDIT_REPORT.md](SECURITY_AUDIT_REPORT.md) | 瀹夊叏瀹¤鎶ュ憡 |
| [specs/](specs/) | 椤圭洰瑙勮寖鏂囨。 |

## 馃 璐＄尞鎸囧崡

娆㈣繋璐＄尞浠ｇ爜锛佽閬靛惊浠ヤ笅姝ラ锛?
1. Fork 鏈粨搴?2. 鍒涘缓鐗规€у垎鏀?(`git checkout -b feature/amazing-feature`)
3. 鎻愪氦鏇存敼 (`git commit -m 'Add amazing feature'`)
4. 鎺ㄩ€佸垎鏀?(`git push origin feature/amazing-feature`)
5. 鍒涘缓 Pull Request

### 浠ｇ爜瑙勮寖

- **Python**: PEP 8, 浣跨敤 `black` 鏍煎紡鍖?- **鍓嶇**: Vue 3 + TypeScript, ESLint 妫€鏌?- **鎻愪氦**: 浣跨敤娓呮櫚鐨勬彁浜や俊鎭牸寮?- **娴嬭瘯**: 鏂板姛鑳介渶鍖呭惈瀵瑰簲娴嬭瘯

## 鉂?甯歌闂

### Q: 濡備綍杩愯椤圭洰锛?A: 鎺ㄨ崘浣跨敤 Docker锛岃瑙佷笂鏂广€孌ocker 閮ㄧ讲銆嶉儴鍒嗐€?
### Q: 濡備綍瀵煎叆 v1 鏁版嵁锛?A: 
```bash
cd backend
python scripts/migrate_v1_users.py
python scripts/migrate_v1_content.py
python scripts/copy_music_files.py
```

### Q: 蹇樿瀵嗙爜鎬庝箞鍔烇紵
A: 鐩墠闇€閫氳繃鏁版嵁搴撶洿鎺ヤ慨鏀癸紝鍚庣画鐗堟湰浼氭坊鍔犲瘑鐮侀噸缃姛鑳姐€?
### Q: 濡備綍鎴愪负绠＄悊鍛橈紵
A: 杩愯 `python scripts/create_admin.py` 鍒涘缓绠＄悊鍛樿处鎴枫€?
### Q: v3.1.0 鍗囩骇娉ㄦ剰浠€涔堬紵
A: 璇峰弬鑰?[UPGRADE_GUIDE.md](UPGRADE_GUIDE.md) 杩涜鍗囩骇銆?
## 馃搫 鐗堟湰鍘嗗彶

| 鐗堟湰 | 鏃ユ湡 | 鍙樻洿 |
|------|------|------|
| 1.0.0 | 2026-02-12 | 鍒濆鐗堟湰 |
| 3.0.0 | 2026-02-15 | v3 闆嗘垚 |
| **3.1.0** | **2026-02-17** | **瀹夊叏澧炲己 (RS256, Rate Limiting)** |

## 馃摓 鏀寔

- 鎻愪氦 [Issue](https://github.com/your-repo/shelter-v3/issues)
- 鍔犲叆璁ㄨ缇?- 鑱旂郴缁存姢鑰?
---

**shElter-v3** - 鐜颁唬鍖?Wiki 骞冲彴
