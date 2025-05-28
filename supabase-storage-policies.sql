-- Rule34画廊 - Supabase存储策略设置
-- 在Supabase Dashboard的SQL Editor中执行此代码

-- 1. 确保rule存储桶存在且为公开桶
INSERT INTO storage.buckets (id, name, public) 
VALUES ('rule', 'rule', true)
ON CONFLICT (id) DO UPDATE SET public = true;

-- 2. 删除现有策略（如果存在）
DROP POLICY IF EXISTS "Public Access" ON storage.objects;
DROP POLICY IF EXISTS "Allow public uploads" ON storage.objects;
DROP POLICY IF EXISTS "Allow public access" ON storage.objects;
DROP POLICY IF EXISTS "Allow public updates" ON storage.objects;
DROP POLICY IF EXISTS "Allow public deletes" ON storage.objects;

-- 3. 创建完整的公开访问策略
CREATE POLICY "Public Access All Operations" ON storage.objects
FOR ALL USING (bucket_id = 'rule');

-- 4. 或者分别创建各种操作的策略（更细粒度控制）
-- CREATE POLICY "Allow public uploads" ON storage.objects
-- FOR INSERT WITH CHECK (bucket_id = 'rule');

-- CREATE POLICY "Allow public access" ON storage.objects
-- FOR SELECT USING (bucket_id = 'rule');

-- CREATE POLICY "Allow public updates" ON storage.objects
-- FOR UPDATE USING (bucket_id = 'rule');

-- CREATE POLICY "Allow public deletes" ON storage.objects
-- FOR DELETE USING (bucket_id = 'rule');

-- 5. 验证策略是否创建成功
SELECT 
    schemaname,
    tablename,
    policyname,
    permissive,
    roles,
    cmd,
    qual
FROM pg_policies 
WHERE tablename = 'objects' AND schemaname = 'storage';

-- 完成！现在rule存储桶应该允许所有公开访问操作 