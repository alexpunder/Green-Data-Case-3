SELECT 
    c.table_schema AS "Схема",
    c.table_name AS "Таблица",
    c.column_name AS "Поле",
    
    c.data_type AS "Тип",
    CASE 
        WHEN c.character_maximum_length IS NOT NULL 
        THEN c.character_maximum_length::text 
        ELSE '' 
    END AS "Размер",
    CASE WHEN c.is_nullable = 'YES' THEN 'Да' ELSE 'Нет' END AS "Nullable",
    CASE WHEN c.column_default IS NOT NULL THEN c.column_default ELSE '' END AS "По умолчанию",
    
    pgd_c.description AS "Описание поля",
    
    CASE WHEN pk.column_name IS NOT NULL THEN 'PK' ELSE '' END AS "Ключ",
    
    fk_info.ref_table AS "Связана с таблицей",
    fk_info.ref_column AS "Связана с полем"

FROM information_schema.columns c

LEFT JOIN pg_catalog.pg_statio_all_tables st 
    ON c.table_schema = st.schemaname AND c.table_name = st.relname
LEFT JOIN pg_catalog.pg_description pgd_c 
    ON pgd_c.objoid = st.relid AND pgd_c.objsubid = c.ordinal_position

LEFT JOIN (
    SELECT ku.table_schema, ku.table_name, ku.column_name
    FROM information_schema.table_constraints tc
    JOIN information_schema.key_column_usage ku
        ON tc.constraint_name = ku.constraint_name
        AND tc.table_schema = ku.table_schema
    WHERE tc.constraint_type = 'PRIMARY KEY'
) pk ON c.table_schema = pk.table_schema 
    AND c.table_name = pk.table_name 
    AND c.column_name = pk.column_name

LEFT JOIN (
    SELECT 
        tc.table_schema,
        tc.table_name,
        kcu.column_name,
        ccu.table_schema AS ref_schema,
        ccu.table_name AS ref_table,
        ccu.column_name AS ref_column
    FROM information_schema.table_constraints tc
    JOIN information_schema.key_column_usage kcu
        ON tc.constraint_name = kcu.constraint_name
        AND tc.table_schema = kcu.table_schema
    JOIN information_schema.constraint_column_usage ccu
        ON ccu.constraint_name = tc.constraint_name
        AND ccu.table_schema = tc.table_schema
    WHERE tc.constraint_type = 'FOREIGN KEY'
) fk_info ON c.table_schema = fk_info.table_schema
         AND c.table_name = fk_info.table_name
         AND c.column_name = fk_info.column_name

LEFT JOIN pg_catalog.pg_description pgd_t 
    ON pgd_t.objoid = st.relid AND pgd_t.objsubid = 0

WHERE c.table_schema NOT IN ('information_schema', 'pg_catalog')
ORDER BY c.table_schema, c.table_name, c.ordinal_position;