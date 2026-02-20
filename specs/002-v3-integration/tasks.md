# Implementation Tasks: shElter-v3 Integration

## Phase 1: Foundation & Schema (Backend)

- [ ] 1.1 Extend User Model
    - Add `level` (int) and `avatar_url` (str) to `src/models/user.py`.
    - Update Pydantic schemas in `src/schemas/user.py`.
    - Generate Alembic migration.
    - **Depends on**: None
    - **Requirement**: FR-001, v1-Integration

- [ ] 1.2 Implement Metro Map Models
    - Create `src/models/metro.py` with `Station`, `Line`, `StationLineJunction`.
    - Create repository/CRUD layer in `src/api/metro.py` (placeholder).
    - Generate Alembic migration.
    - **Depends on**: 1.1
    - **Requirement**: v1-Metro-Map

- [ ] 1.3 Implement Music Models
    - Create `src/models/music.py` with `Track`, `Playlist`.
    - Generate Alembic migration.
    - **Depends on**: 1.1
    - **Requirement**: v1-Music-Player

## Phase 2: Data Migration (One-Off)

- [ ] 2.1 [P] Develop User Migration Script
    - Write `scripts/migrate_v1_users.py`.
    - Logic: Read `shElter-v1/00_shElter/02_SoulLoom/*/00_identity.dat`.
    - Handle GBK/UTF-8 encoding issues.
    - Create users in DB with default passwords.
    - **Depends on**: 1.1
    - **Requirement**: Data-Safety

- [ ] 2.2 [P] Develop Content Migration Script
    - Write `scripts/migrate_v1_content.py`.
    - Logic: Scan `shElter-v1` directories to populate `Station` table.
    - Logic: Scan `03_Echoom/music` to populate `Track` table.
    - **Depends on**: 1.2, 1.3
    - **Requirement**: Data-Safety

## Phase 3: Backend API Implementation

- [ ] 3.1 Metro Map API
    - Implement `GET /api/v1/metro/map`.
    - Logic: Return stations and lines filtered by `current_user.level`.
    - **Depends on**: 1.2
    - **Requirement**: v1-Metro-Map

- [ ] 3.2 Music API
    - Implement `GET /api/v1/music/tracks`.
    - Implement `GET /api/v1/music/stream/{track_id}`.
    - Implement `GET /api/v1/music/lyrics/{track_id}`.
    - **Depends on**: 1.3
    - **Requirement**: v1-Music-Player

## Phase 4: Frontend Visual Core (Vue 3)

- [ ] 4.1 Setup Metro Layout
    - Create `src/layouts/MetroLayout.vue`.
    - Implement retro CRT effect overlay.
    - Configure global styles to match v1 dark theme.
    - **Depends on**: None
    - **Requirement**: Visual-Fidelity

- [ ] 4.2 Implement Metro Map Component
    - Create `src/components/metro/StationMap.vue`.
    - Use SVG/CSS to render lines and stations.
    - Fetch data from `3.1 Metro Map API`.
    - **Depends on**: 3.1, 4.1
    - **Requirement**: v1-Metro-Map

- [ ] 4.3 Implement Global Music Player
    - Create `src/components/music/RetroPlayer.vue`.
    - Implement AudioContext logic for playback.
    - Implement Lyrics scrolling sync.
    - Integrate with Pinia store `usePlayerStore`.
    - **Depends on**: 3.2
    - **Requirement**: v1-Music-Player

## Phase 5: Feature Integration

- [ ] 5.1 Wiki UI Porting
    - Update `ArticlesView.vue` to match `01_Cryptonomicon` visual style.
    - Ensure Markdown rendering matches v1 text styling.
    - **Depends on**: 4.1
    - **Requirement**: v1-Wiki

- [ ] 5.2 Social UI Porting
    - Update `UserProfileView.vue` to match `02_SoulLoom` visual style.
    - Display User Level/Rank prominentely.
    - **Depends on**: 1.1
    - **Requirement**: v1-Social

## Phase 6: Verification

- [ ] 6.1 Visual Regression Testing
    - Manual comparison of v1 `index.php` vs v3 `HomeView`.
    - Manual comparison of Music Player behavior.
    - **Depends on**: All previous
    - **Requirement**: Quality-Assurance
