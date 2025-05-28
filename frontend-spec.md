# Rule34‑lite Front‑End Spec

This markdown file describes the **minimum‑viable front‑end** for a Rule34‑style image gallery powered by Supabase.
Drop this file in your project root so that AI coding tools (e.g. Cursor’s “Generate Code”) can reference a clear,
structured spec.

---

## 1. Tech Stack

| Layer           | Choice                 | Reason |
|-----------------|------------------------|--------|
| Framework       | Next.js 14 / React 18  | File‑based routing, RSC/SSR optional |
| State/Data      | Supabase JS v2         | Auth + Postgres + Storage in one SDK |
| Styling         | Tailwind CSS           | Utility‑first, fast prototyping |
| Type checking   | TypeScript             | Safer refactors |
| Tooling         | pnpm / ESLint / Prettier | Speed & consistency |

---

## 2. Pages & Component Tree

| Route                | Component tree (top → leaf)                                                                                                   | Purpose |
|----------------------|-------------------------------------------------------------------------------------------------------------------------------|---------|
| `/` (Home)           | `<App>` → `<GalleryLayout>` → `<SidebarCategories>` ∥ `<ThumbnailGrid>` → `<ThumbnailCard>`                                   | Grid of all images, filters by category & search |
| `/img/[id]`          | `<ImageDetailLayout>` → `<ImageHero>` ∥ `<TagList>` ∥ `<RelatedGrid>` → `<ThumbnailCard>`                                     | Full‑size image + metadata + related |
| `*` (404 fallback)   | `<NotFound>`                                                                                                                  | Generic 404 page |

**Shared UI widgets**

| Component        | Notes |
|------------------|-------|
| `<SearchBar>`    | Global top‑right, redirects to `/?q=` |
| `<Loader>`       | Full‑page or inline spinner/skeleton |
| `<ErrorBoundary>`| Catches Supabase/network errors |

---

## 3. ASCII Wireframes (Low‑Fi)

```text
+-----------------------------------------------------------+
| Rule34‑lite (logo)            | [ Search…  🔍 ] | ☰ |      |
+--------------------+--------------------------------------+
| # Categories       | ▢ ▢ ▢ ▢  ▢ ▢ ▢ ▢  ▢ ▢ ▢ ▢            |
| - All (1234)       | ▢ ▢ ▢ ▢  ▢ ▢ ▢ ▢  ▢ ▢ ▢ ▢   …        |
| - Anime (820)      |                                      |
| - Western (210)    | ← infinite scroll grid               |
| - Furry (204)      |                                      |
+--------------------+--------------------------------------+
| © 2025 YourSite                                ↑ Top      |
+-----------------------------------------------------------+
```

```text
ImageDetail  (/img/abc123)
┌─────────────────────────────────────────────────────────┐
│ ← Back   [1920×1080]  Download ▼                       │
├─────────────────────────────────────────────────────────┤
│               (responsive FULL image)                  │
│ ┌─────────────────────────────────────────────────────┐ │
│ │   Tag pills  (clickable, route to /?q=tag)          │ │
│ └─────────────────────────────────────────────────────┘ │
├────────────  Related (same category & ≥1 tag)  ─────────┤
│ ▢ ▢ ▢ ▢ ▢ ▢ ▢ ▢ ▢ ▢ ▢ ▢                                │
└─────────────────────────────────────────────────────────┘
```

---

## 4. Suggested Directory Layout

```txt
src/
├─ components/
│  ├─ layout/
│  │   ├─ GalleryLayout.tsx
│  │   └─ ImageDetailLayout.tsx
│  ├─ ui/
│  │   ├─ SidebarCategories.tsx
│  │   ├─ ThumbnailCard.tsx
│  │   ├─ TagPill.tsx
│  │   └─ Loader.tsx
│  └─ common/
│      └─ ErrorBoundary.tsx
├─ pages/                # or app/ in Next 14
│  ├─ index.tsx
│  ├─ img/
│  │   └─ [id].tsx
│  └─ 404.tsx
├─ lib/
│  ├─ supabase.ts
│  └─ queries.ts
├─ styles/               # Tailwind layers or SCSS
└─ types/
    └─ Image.ts
```

---

## 5. Supabase Schema & Queries

### Table: `images`

| column       | type        | notes                         |
|--------------|-------------|-------------------------------|
| `id`         | uuid PK     | `default gen_random_uuid()`   |
| `category`   | text        | “anime” / “western” / …       |
| `tags`       | text[]      | GIN‑indexed for `@>` and `&&` |
| `width`      | integer     |                               |
| `height`     | integer     |                               |
| `file_url`   | text        | From storage public bucket    |
| `uploaded_at`| timestamptz | `default now()`               |

**Row‑level security**  
```sql
alter table images enable row level security;
create policy "Public read" on images
  for select using (true);
```

### `lib/queries.ts` (excerpt)

```ts
import { createClient } from '@supabase/supabase-js'

export const supabase = createClient(
  import.meta.env.PUBLIC_SUPABASE_URL!,
  import.meta.env.PUBLIC_SUPABASE_ANON_KEY!
)

export const getCategories = () =>
  supabase
    .from('images')
    .select('category, count:id', { groupBy: 'category' })
    .order('count', { ascending: false })

export const getImages = ({
  category,
  query,
  limit = 40,
  from = 0,
}) => {
  let q = supabase
    .from('images')
    .select('*', { order: 'uploaded_at', ascending: false })
    .range(from, from + limit - 1)

  if (category && category !== 'all') q = q.eq('category', category)
  if (query) q = q.contains('tags', [query])

  return q
}

export const getImageById = (id: string) =>
  supabase.from('images').select('*').eq('id', id).single()

export const getRelated = (image) =>
  supabase
    .from('images')
    .select('*')
    .neq('id', image.id)
    .eq('category', image.category)
    .overlaps('tags', image.tags)
    .limit(12)
```

---

## 6. Interaction Flow

1. **Home load** → fetch `getCategories` & first `getImages` in parallel.  
2. **Filter** (sidebar click) → update URL `?cat=xxx` → reload grid from offset 0.  
3. **Search** → update URL `?q=fox` → highlight matching tag pills.  
4. **Infinite scroll** → IntersectionObserver loads next page when sentinel enters viewport.  
5. **Detail page** → after main image fetch, call `getRelated`.  
6. **Errors** → throw if Supabase error; show `<ErrorBoundary>` with retry button.

---

## 7. Styles & Accessibility

* **Dark default**: `bg‑[#111] text‑[#fafafa]`.
* Thumbnail uses `object‑cover` and `loading="lazy"`.
* Grid: 2 cols (mobile) → 4 (sm) → 6 (md) → 8 (xl).
* Color contrast ≥ 4.5:1; focus rings via Tailwind `focus-visible:outline`.

---

## 8. Quick Start (demo script)

```bash
pnpm create next-app rule34-lite --ts --tailwind --eslint
cd rule34-lite
pnpm i @supabase/supabase-js
# .env.local →  PUBLIC_SUPABASE_URL=  PUBLIC_SUPABASE_ANON_KEY=
pnpm dev
```

Copy the directory layout above into `src/`, paste the query snippets, and let Cursor **⌘ K → “Generate file”** to scaffold each component.

---

## 9. Roadmap

| Feature           | DB change                 | Front‑end addition |
|-------------------|---------------------------|--------------------|
| Likes / Favorites | `likes (user_id, img_id)` | Heart icon, login  |
| Tag pages         | separate `tags` table     | `/tag/[name]` page |
| Reports           | `reports` table           | “Report” button    |

---

### License

MIT — do whatever you like.  
© 2025 YourName
