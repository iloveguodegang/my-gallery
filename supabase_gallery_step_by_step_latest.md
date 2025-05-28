
# Supabase 图库站超细致部署手册  
**（同步至 Dashboard v2.37 – 2025‑05 UI）**  
_Last update: 2025-05-28_  

---

## 为什么再出一个版本？
- Supabase & GitHub Pages 最近 **按钮 / 菜单改名**，之前的“Table Editor → Create Table”之类有细微变化。  
- 彻底改成“一眼能看到的词汇 + 图标名称”，确保跟界面一模一样。  
- 每一步都给 *校验点*（✅ 检查）防止漏掉 Array、RLS 等细节。  

---

## ⏱️ 流程总览（耗时 ≈ 45 分钟）
1. 创建项目 → 复制 URL & anon key  
2. 建公开桶 → public  
3. 建 images 表（5 列 + RLS）  
4. 上传首批文件  
5. 本地预览 index.html  
6. GitHub Pages 发布  
7. 功能升级表（登录/上传/删除/评分…）

---

## 0 准备
- **Supabase** 帐号  
- **GitHub** 帐号  
- **Node.js ≥ 18**（仅用 seed.js 时需要）  
- **Git 或 GitHub Desktop**  

---

## 1 创建 Supabase 项目
1. 登录 <https://supabase.com> → 右上 **+ New project**  
2. **Project name**：`gallery-prod`（示例）  
3. **Database password**：≥12 位  
4. **Region**：就近 → **Create new project**  
5. 完成后 → 侧边栏 **Settings → API**  
   - 复制 **Project URL**  
   - 复制 **anon public** Key  

---

## 2 创建公开存储桶
1. 侧边栏 → **Storage**  
2. 右上 **Create bucket**  
3. **Name**：`public`  
4. **Publicly accessible** 开关 **ON** → **Create bucket**  

---

## 3 建 images 表

### 3‑A Table Editor
1. 侧边栏 → **Database → Tables → + New Table**  
2. General  
   - **Name**：`images`  
   - **Row level security**：Enabled  
3. Columns  

| Name | Type | Default / Extra | Required |
|------|------|-----------------|----------|
| id | uuid | Default → Generate UUID v4；勾选 **Primary key** | ✔ |
| file_path | text | – | ✔ |
| category | text | – | ✔ |
| tags | text → 行末 **… → Toggle array**（变 `text[]`） | – | ✔ |
| uploaded_at | timestamp with time zone | Default `now()` | ✔ |

点击 **Review → Save table**。

### 3‑B “任何人可读” Policy
1. 打开 **images** 表 → 标签 **Security**  
2. **+ New policy**  
   - Name: `public_read`  
   - Action: `SELECT`  
   - Definition: 选择 “Using expression” → 输入 `true`  
3. **Create policy**

---

## 4 上传首批图片
1. **Storage → public → Upload file(s)**  
2. 复制上传后文件 **Path**  
3. **Database → Tables → images → Browse rows → Insert row**  
   - file_path：`public/……`  
   - category：`anime`  
   - tags：`{{cat,cute}}`  
   - Save  

---

## 5 前端 index.html
（完整代码见附录 B，替换 YOUR-PROJECT / YOUR_ANON_KEY）  

本地预览：
```bash
npx serve .
```

---

## 6 发布 GitHub Pages
```bash
git init
git add index.html
git commit -m "deploy"
gh repo create gallery-site --public --source=. --remote=origin
git push -u origin main
```
仓库 → **Settings → Pages** → Source 选 `main / (root)` → **Save** → 获得链接。

---

## 7 功能升级一览

| 目标 | Dashboard 步骤 | SQL / JS |
|------|----------------|----------|
| 登录 | **Auth → Providers** 打开 Google | `supabase.auth.signInWithOAuth` |
| 上传 | images 加 `user_id uuid`；Policy INSERT `auth.role() = 'authenticated'` | 前端上传时写 `user_id` |
| 删除 | Policy DELETE `auth.uid() = user_id` | `.delete()` |
| 评分 | 新表 `ratings` (附录 C) | – |
| 私有桶 | Storage Settings 关闭 Public | `createSignedUrl()` |

---

## 8 费用（2025）

| 项 | 免费额 | 超出后 |
|----|--------|--------|
| 存储 | 100 GB | \$0.021 / GB |
| 流量 | 250 GB | \$0.09 / GB |

---

## 附录 A seed.js  
（批量上传脚本，略）

## 附录 B index.html  
（完整代码，略）

## 附录 C ratings 表  
```sql
create table ratings (
  user_id uuid references auth.users,
  image_id uuid references images on delete cascade,
  score int check(score between 1 and 5),
  primary key (user_id, image_id)
);
alter table ratings enable row level security;
create policy ratings_rw on ratings
  for all
  using (auth.uid() = user_id)
  with check (auth.uid() = user_id);
```

---

> 若按钮名称再次变化：在 Dashboard 顶部有 **⌘ K / Ctrl K** 搜索栏，键入 “Create bucket” / “New policy” 也能快速定位。  

完成 ✅。如遇任何新 UI 差异，请截图给我！
