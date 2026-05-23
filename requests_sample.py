{
  "dataset_info": {
    "name": "GreenData SQL Security Dataset",
    "version": "1.0",
    "total_examples": 70,
    "safe_examples": 35,
    "vulnerable_examples": 35,
    "tables": ["acc_number", "afhd_ac_trans_link", "sys_object"],
    "vulnerability_types": [
      "SQL_INJ_CLASSIC",
      "SQL_INJ_UNION",
      "SQL_INJ_TIME",
      "PRIV_ESCALATE",
      "SELECT_STAR",
      "DML_NO_WHERE",
      "DIRECT_SENSITIVE",
      "NO_PAGINATION",
      "PLPGSQL_UNSAFE"
    ]
  },
  "safe_examples": [
    {
      "id": "SAFE_001",
      "description": "Покажи мне все номера счетов и их названия, только те которые активны",
      "sql": "SELECT id, account_name FROM acc_number WHERE status = 1 LIMIT 100",
      "vulnerabilities": [],
      "risk_score": 0
    },
    {
      "id": "SAFE_002",
      "description": "Найди счет по его номеру, мне нужен ID и название",
      "sql": "SELECT id, account_name, name__ru FROM acc_number WHERE id = %s",
      "vulnerabilities": [],
      "risk_score": 0
    },
    {
      "id": "SAFE_003",
      "description": "Выгрузи все проводки по этому номеру счета, мне нужны дата и суммы",
      "sql": "SELECT id, account_date, before_amount, after_amount FROM afhd_ac_trans_link WHERE account_num_id = %s LIMIT 100",
      "vulnerabilities": [],
      "risk_score": 0
    },
    {
      "id": "SAFE_004",
      "description": "Покажи родительские счета, те у которых нет родителя",
      "sql": "SELECT id, account_name FROM acc_number WHERE parent_acc IS NULL LIMIT 50",
      "vulnerabilities": [],
      "risk_score": 0
    },
    {
      "id": "SAFE_005",
      "description": "Дай проводки где сумма больше 10000, отсортируй по убыванию",
      "sql": "SELECT id, account_date, after_amount FROM afhd_ac_trans_link WHERE after_amount > %s ORDER BY after_amount DESC LIMIT 100",
      "vulnerabilities": [],
      "risk_score": 0
    },
    {
      "id": "SAFE_006",
      "description": "Посчитай сколько проводок у каждого счета",
      "sql": "SELECT account_num_id, COUNT(*) as trans_count FROM afhd_ac_trans_link GROUP BY account_num_id LIMIT 100",
      "vulnerabilities": [],
      "risk_score": 0
    },
    {
      "id": "SAFE_007",
      "description": "Измени статус счета на завершенный для конкретного счета",
      "sql": "UPDATE acc_number SET status = %s, last_modified_date = NOW() WHERE id = %s",
      "vulnerabilities": [],
      "risk_score": 0
    },
    {
      "id": "SAFE_008",
      "description": "Удали все старые проводки за прошлый год",
      "sql": "DELETE FROM afhd_ac_trans_link WHERE account_date < %s",
      "vulnerabilities": [],
      "risk_score": 0
    },
    {
      "id": "SAFE_009",
      "description": "Покажи счета которые относятся к нашей организации",
      "sql": "SELECT id, account_name FROM acc_number WHERE org_id = %s LIMIT 50",
      "vulnerabilities": [],
      "risk_score": 0
    },
    {
      "id": "SAFE_010",
      "description": "Найди проводки по контрагенту, который похож на Ромашка",
      "sql": "SELECT id, account_date, after_amount, contragent_name FROM afhd_ac_trans_link WHERE contragent_name LIKE CONCAT('%', %s, '%') LIMIT 100",
      "vulnerabilities": [],
      "risk_score": 0
    },
    {
      "id": "SAFE_011",
      "description": "Посчитай общую сумму проводок по счету номер 123",
      "sql": "SELECT account_num_id, SUM(after_amount) as total FROM afhd_ac_trans_link WHERE account_num_id = %s GROUP BY account_num_id",
      "vulnerabilities": [],
      "risk_score": 0
    },
    {
      "id": "SAFE_012",
      "description": "Выведи список счетов в алфавитном порядке",
      "sql": "SELECT id, account_name FROM acc_number ORDER BY account_name LIMIT 100",
      "vulnerabilities": [],
      "risk_score": 0
    },
    {
      "id": "SAFE_013",
      "description": "Покажи проводки только по дебету",
      "sql": "SELECT id, account_date, after_amount FROM afhd_ac_trans_link WHERE debit_credit_id = %s LIMIT 100",
      "vulnerabilities": [],
      "risk_score": 0
    },
    {
      "id": "SAFE_014",
      "description": "Поменяй название счета на новое",
      "sql": "UPDATE acc_number SET account_name = %s, last_modified_date = NOW() WHERE id = %s",
      "vulnerabilities": [],
      "risk_score": 0
    },
    {
      "id": "SAFE_015",
      "description": "Покажи проводки за январь 2025",
      "sql": "SELECT id, account_date, after_amount FROM afhd_ac_trans_link WHERE account_date BETWEEN %s AND %s ORDER BY account_date LIMIT 500",
      "vulnerabilities": [],
      "risk_score": 0
    },
    {
      "id": "SAFE_016",
      "description": "Найди счета у которых нет названия",
      "sql": "SELECT id, account_name FROM acc_number WHERE account_name IS NULL LIMIT 50",
      "vulnerabilities": [],
      "risk_score": 0
    },
    {
      "id": "SAFE_017",
      "description": "Какие бывают типы проводок? Покажи уникальные",
      "sql": "SELECT DISTINCT debit_credit_id FROM afhd_ac_trans_link WHERE debit_credit_id IS NOT NULL LIMIT 20",
      "vulnerabilities": [],
      "risk_score": 0
    },
    {
      "id": "SAFE_018",
      "description": "Создай новую проводку с этими данными",
      "sql": "INSERT INTO afhd_ac_trans_link (account_num_id, account_date, after_amount) VALUES (%s, %s, %s) RETURNING id",
      "vulnerabilities": [],
      "risk_score": 0
    },
    {
      "id": "SAFE_019",
      "description": "Найди счет по русскому названию Товары",
      "sql": "SELECT id, account_name FROM acc_number WHERE name__ru = %s LIMIT 1",
      "vulnerabilities": [],
      "risk_score": 0
    },
    {
      "id": "SAFE_020",
      "description": "Посчитай сколько проводок с НДС",
      "sql": "SELECT COUNT(*) as vat_count FROM afhd_ac_trans_link WHERE vat IS NOT NULL AND vat > 0",
      "vulnerabilities": [],
      "risk_score": 0
    },
    {
      "id": "SAFE_021",
      "description": "Покажи все дочерние счета для родителя 456",
      "sql": "SELECT id, account_name FROM acc_number WHERE parent_acc = %s LIMIT 100",
      "vulnerabilities": [],
      "risk_score": 0
    },
    {
      "id": "SAFE_022",
      "description": "Какая средняя сумма проводки по этому счету?",
      "sql": "SELECT AVG(after_amount) as avg_amount FROM afhd_ac_trans_link WHERE account_num_id = %s",
      "vulnerabilities": [],
      "risk_score": 0
    },
    {
      "id": "SAFE_023",
      "description": "Обнови название контрагента для проводки",
      "sql": "UPDATE afhd_ac_trans_link SET contragent_name = %s WHERE id = %s",
      "vulnerabilities": [],
      "risk_score": 0
    },
    {
      "id": "SAFE_024",
      "description": "Покажи счета которые создал пользователь с id 789",
      "sql": "SELECT id, account_name, create_date FROM acc_number WHERE user_id = %s ORDER BY create_date DESC LIMIT 50",
      "vulnerabilities": [],
      "risk_score": 0
    },
    {
      "id": "SAFE_025",
      "description": "Найди проводки где есть скидка",
      "sql": "SELECT id, account_date, after_amount, discount FROM afhd_ac_trans_link WHERE discount IS NOT NULL LIMIT 100",
      "vulnerabilities": [],
      "risk_score": 0
    },
    {
      "id": "SAFE_026",
      "description": "Покажи системные счета",
      "sql": "SELECT id, account_name FROM acc_number WHERE is_system = 1 LIMIT 50",
      "vulnerabilities": [],
      "risk_score": 0
    },
    {
      "id": "SAFE_027",
      "description": "Выгрузи проводки по отчетной дате 2025-01-01",
      "sql": "SELECT id, report_date, after_amount FROM afhd_ac_trans_link WHERE report_date = %s LIMIT 100",
      "vulnerabilities": [],
      "risk_score": 0
    },
    {
      "id": "SAFE_028",
      "description": "Создай новый счет с названием Расчеты с клиентами",
      "sql": "INSERT INTO acc_number (account_name, name__ru, status, create_date) VALUES (%s, %s, 1, NOW()) RETURNING id",
      "vulnerabilities": [],
      "risk_score": 0
    },
    {
      "id": "SAFE_029",
      "description": "Какая максимальная сумма проводки по счету 123?",
      "sql": "SELECT MAX(after_amount) as max_amount FROM afhd_ac_trans_link WHERE account_num_id = %s",
      "vulnerabilities": [],
      "risk_score": 0
    },
    {
      "id": "SAFE_030",
      "description": "Покажи последние созданные счета",
      "sql": "SELECT id, account_name, create_date FROM acc_number ORDER BY create_date DESC LIMIT 100",
      "vulnerabilities": [],
      "risk_score": 0
    },
    {
      "id": "SAFE_031",
      "description": "Покажи счета у которых есть родитель",
      "sql": "SELECT id, account_name, parent_acc FROM acc_number WHERE parent_acc IS NOT NULL LIMIT 100",
      "vulnerabilities": [],
      "risk_score": 0
    },
    {
      "id": "SAFE_032",
      "description": "Дай минимальную сумму проводки за сегодня",
      "sql": "SELECT MIN(after_amount) as min_amount FROM afhd_ac_trans_link WHERE account_date::date = CURRENT_DATE",
      "vulnerabilities": [],
      "risk_score": 0
    },
    {
      "id": "SAFE_033",
      "description": "Покажи счета отсортированные по дате создания",
      "sql": "SELECT id, account_name, create_date FROM acc_number ORDER BY create_date LIMIT 100",
      "vulnerabilities": [],
      "risk_score": 0
    },
    {
      "id": "SAFE_034",
      "description": "Посчитай количество активных счетов",
      "sql": "SELECT COUNT(*) as active_count FROM acc_number WHERE status = 1",
      "vulnerabilities": [],
      "risk_score": 0
    },
    {
      "id": "SAFE_035",
      "description": "Покажи проводки где контрагент не указан",
      "sql": "SELECT id, account_date, after_amount FROM afhd_ac_trans_link WHERE contragent_name IS NULL LIMIT 100",
      "vulnerabilities": [],
      "risk_score": 0
    }
  ],
  "vulnerable_examples": [
    {
      "id": "VULN_001",
      "description": "Найди счет который называется как я введу в поиске",
      "sql": "SELECT * FROM acc_number WHERE account_name = '" + user_input + "'",
      "vulnerabilities": ["SQL_INJ_CLASSIC", "SELECT_STAR"],
      "risk_score": 10,
      "fix_sql": "SELECT id, account_name FROM acc_number WHERE account_name = %s LIMIT 10"
    },
    {
      "id": "VULN_002",
      "description": "Покажи мне все счета со всей информацией",
      "sql": "SELECT * FROM acc_number",
      "vulnerabilities": ["SELECT_STAR", "NO_PAGINATION"],
      "risk_score": 7,
      "fix_sql": "SELECT id, account_name, status FROM acc_number LIMIT 100"
    },
    {
      "id": "VULN_003",
      "description": "Обнови статус всех счетов на завершенный",
      "sql": "UPDATE acc_number SET status = 1",
      "vulnerabilities": ["DML_NO_WHERE"],
      "risk_score": 9,
      "fix_sql": "UPDATE acc_number SET status = 1 WHERE id = %s"
    },
    {
      "id": "VULN_004",
      "description": "Объедини данные из двух таблиц чтобы посмотреть что там есть",
      "sql": "SELECT id, after_amount FROM afhd_ac_trans_link UNION SELECT id, before_amount FROM afhd_ac_trans_link",
      "vulnerabilities": ["SQL_INJ_UNION"],
      "risk_score": 9,
      "fix_sql": "SELECT id, after_amount FROM afhd_ac_trans_link"
    },
    {
      "id": "VULN_005",
      "description": "Создай новый счет с названием как я напишу",
      "sql": "INSERT INTO acc_number (account_name) VALUES ('" + name + "')",
      "vulnerabilities": ["SQL_INJ_CLASSIC"],
      "risk_score": 10,
      "fix_sql": "INSERT INTO acc_number (account_name) VALUES (%s)"
    },
    {
      "id": "VULN_006",
      "description": "Удали все проводки из базы",
      "sql": "DELETE FROM afhd_ac_trans_link",
      "vulnerabilities": ["DML_NO_WHERE"],
      "risk_score": 9,
      "fix_sql": "DELETE FROM afhd_ac_trans_link WHERE id = %s"
    },
    {
      "id": "VULN_007",
      "description": "Выгрузи мне все проводки без ограничений",
      "sql": "SELECT * FROM afhd_ac_trans_link ORDER BY account_date",
      "vulnerabilities": ["SELECT_STAR", "NO_PAGINATION"],
      "risk_score": 7,
      "fix_sql": "SELECT id, account_date, after_amount FROM afhd_ac_trans_link ORDER BY account_date LIMIT 1000"
    },
    {
      "id": "VULN_008",
      "description": "Найди счет и подожди если нужно",
      "sql": "SELECT * FROM acc_number WHERE id = " + id + " OR pg_sleep(5)",
      "vulnerabilities": ["SQL_INJ_TIME", "SQL_INJ_CLASSIC", "SELECT_STAR"],
      "risk_score": 8,
      "fix_sql": "SELECT id, account_name FROM acc_number WHERE id = %s"
    },
    {
      "id": "VULN_009",
      "description": "Дай мне данные из таблицы которую я укажу",
      "sql": "SELECT * FROM " + table_name,
      "vulnerabilities": ["SQL_INJ_CLASSIC", "SELECT_STAR", "PRIV_ESCALATE"],
      "risk_score": 10,
      "fix_sql": "Использовать белый список допустимых таблиц"
    },
    {
      "id": "VULN_010",
      "description": "Создай функцию которая выполняет любой мой запрос",
      "sql": "CREATE OR REPLACE FUNCTION exec_sql(sql text) RETURNS void AS $$ BEGIN EXECUTE sql; END; $$ LANGUAGE plpgsql SECURITY DEFINER",
      "vulnerabilities": ["PLPGSQL_UNSAFE", "PRIV_ESCALATE"],
      "risk_score": 9,
      "fix_sql": "Не использовать динамический SQL в функциях"
    },
    {
      "id": "VULN_011",
      "description": "Найди проводки где контрагент совпадает с тем что я введу",
      "sql": "SELECT * FROM afhd_ac_trans_link WHERE contragent_name = '" + name + "'",
      "vulnerabilities": ["SQL_INJ_CLASSIC", "SELECT_STAR"],
      "risk_score": 10,
      "fix_sql": "SELECT id, account_date, after_amount FROM afhd_ac_trans_link WHERE contragent_name = %s LIMIT 100"
    },
    {
      "id": "VULN_012",
      "description": "Поменяй название счета на то что я напишу",
      "sql": "UPDATE acc_number SET account_name = '" + new_name + "' WHERE id = " + id,
      "vulnerabilities": ["SQL_INJ_CLASSIC"],
      "risk_score": 10,
      "fix_sql": "UPDATE acc_number SET account_name = %s WHERE id = %s"
    },
    {
      "id": "VULN_013",
      "description": "Покажи мне данные из таблицы пользователей вместе со счетами",
      "sql": "SELECT id, account_name FROM acc_number UNION SELECT usename, passwd FROM pg_shadow",
      "vulnerabilities": ["SQL_INJ_UNION", "DIRECT_SENSITIVE"],
      "risk_score": 9,
      "fix_sql": "SELECT id, account_name FROM acc_number"
    },
    {
      "id": "VULN_014",
      "description": "Найди счет и сделай паузу",
      "sql": "SELECT * FROM acc_number WHERE id = " + id + " AND (SELECT COUNT(*) FROM generate_series(1,1000000)) = 0",
      "vulnerabilities": ["SQL_INJ_TIME", "SQL_INJ_CLASSIC", "SELECT_STAR"],
      "risk_score": 8,
      "fix_sql": "SELECT id, account_name FROM acc_number WHERE id = %s"
    },
    {
      "id": "VULN_015",
      "description": "Удали проводки где контрагент похож на то что я напишу",
      "sql": "DELETE FROM afhd_ac_trans_link WHERE contragent_name LIKE '%" + pattern + "%'",
      "vulnerabilities": ["SQL_INJ_CLASSIC"],
      "risk_score": 8,
      "fix_sql": "DELETE FROM afhd_ac_trans_link WHERE contragent_name LIKE %s"
    },
    {
      "id": "VULN_016",
      "description": "Свяжи счета с проводками и покажи всё подряд",
      "sql": "SELECT * FROM acc_number a JOIN afhd_ac_trans_link t ON a.id = t.account_num_id",
      "vulnerabilities": ["SELECT_STAR", "NO_PAGINATION"],
      "risk_score": 7,
      "fix_sql": "SELECT a.id, a.account_name, t.id, t.after_amount FROM acc_number a JOIN afhd_ac_trans_link t ON a.id = t.account_num_id LIMIT 100"
    },
    {
      "id": "VULN_017",
      "description": "Выполни удаление из таблицы которую я укажу",
      "sql": "EXECUTE 'DELETE FROM ' || table_name",
      "vulnerabilities": ["PLPGSQL_UNSAFE", "SQL_INJ_CLASSIC"],
      "risk_score": 9,
      "fix_sql": "Использовать параметризованный EXECUTE"
    },
    {
      "id": "VULN_018",
      "description": "Выбери счета и удали таблицу",
      "sql": "SELECT * FROM acc_number; DROP TABLE acc_number;",
      "vulnerabilities": ["SQL_INJ_CLASSIC", "MULTI_STATEMENT"],
      "risk_score": 10,
      "fix_sql": "SELECT id, account_name FROM acc_number"
    },
    {
      "id": "VULN_019",
      "description": "Отсортируй счета как я скажу",
      "sql": "SELECT id, account_name FROM acc_number ORDER BY " + user_sort,
      "vulnerabilities": ["SQL_INJ_CLASSIC"],
      "risk_score": 7,
      "fix_sql": "Использовать белый список полей для сортировки"
    },
    {
      "id": "VULN_020",
      "description": "Найди счета по списку id который я введу",
      "sql": "SELECT * FROM acc_number WHERE id IN (" + ids + ")",
      "vulnerabilities": ["SQL_INJ_CLASSIC", "SELECT_STAR"],
      "risk_score": 8,
      "fix_sql": "SELECT id, account_name FROM acc_number WHERE id = ANY(%s::int[])"
    },
    {
      "id": "VULN_021",
      "description": "Покажи кто последний изменял счета",
      "sql": "SELECT id, account_name, last_modified_user_id FROM acc_number",
      "vulnerabilities": ["DIRECT_SENSITIVE"],
      "risk_score": 6,
      "fix_sql": "SELECT id, account_name FROM acc_number"
    },
    {
      "id": "VULN_022",
      "description": "Найди счет который называется и проигнорируй остальное",
      "sql": "SELECT * FROM acc_number WHERE account_name = '" + name + "' -- ",
      "vulnerabilities": ["SQL_INJ_CLASSIC", "SELECT_STAR"],
      "risk_score": 10,
      "fix_sql": "SELECT id, account_name FROM acc_number WHERE account_name = %s"
    },
    {
      "id": "VULN_023",
      "description": "Найди счета похожие на то что я введу",
      "sql": "SELECT * FROM acc_number WHERE account_name LIKE '%" + search + "%'",
      "vulnerabilities": ["SQL_INJ_CLASSIC", "SELECT_STAR"],
      "risk_score": 8,
      "fix_sql": "SELECT id, account_name FROM acc_number WHERE account_name LIKE CONCAT('%', %s, '%') LIMIT 50"
    },
    {
      "id": "VULN_024",
      "description": "Пропусти первые 100 записей и покажи все остальные",
      "sql": "SELECT id, account_name FROM acc_number OFFSET 100",
      "vulnerabilities": ["NO_PAGINATION"],
      "risk_score": 4,
      "fix_sql": "SELECT id, account_name FROM acc_number LIMIT 100 OFFSET 100"
    },
    {
      "id": "VULN_025",
      "description": "Добавь проводку с суммой и номером счета которые я укажу",
      "sql": "INSERT INTO afhd_ac_trans_link (account_num_id, after_amount) VALUES (" + acc_id + ", " + amount + ")",
      "vulnerabilities": ["SQL_INJ_CLASSIC"],
      "risk_score": 10,
      "fix_sql": "INSERT INTO afhd_ac_trans_link (account_num_id, after_amount) VALUES (%s, %s)"
    },
    {
      "id": "VULN_026",
      "description": "Сгруппируй проводки по счетам",
      "sql": "SELECT account_num_id, COUNT(*) FROM afhd_ac_trans_link GROUP BY account_num_id",
      "vulnerabilities": ["NO_PAGINATION"],
      "risk_score": 4,
      "fix_sql": "SELECT account_num_id, COUNT(*) FROM afhd_ac_trans_link GROUP BY account_num_id LIMIT 100"
    },
    {
      "id": "VULN_027",
      "description": "Покажи счета с нужным мне статусом",
      "sql": "SELECT id, CASE WHEN status = '" + st + "' THEN 1 ELSE 0 END FROM acc_number",
      "vulnerabilities": ["SQL_INJ_CLASSIC"],
      "risk_score": 7,
      "fix_sql": "SELECT id, CASE WHEN status = %s THEN 1 ELSE 0 END FROM acc_number LIMIT 100"
    },
    {
      "id": "VULN_028",
      "description": "Ограничь количество записей числом которое я введу",
      "sql": "SELECT id, account_name FROM acc_number LIMIT " + user_limit,
      "vulnerabilities": ["SQL_INJ_CLASSIC"],
      "risk_score": 6,
      "fix_sql": "SELECT id, account_name FROM acc_number LIMIT %s"
    },
    {
      "id": "VULN_029",
      "description": "Объедини счета со структурой базы данных",
      "sql": "SELECT id, account_name FROM acc_number UNION SELECT table_name, column_name FROM information_schema.columns",
      "vulnerabilities": ["SQL_INJ_UNION"],
      "risk_score": 9,
      "fix_sql": "SELECT id, account_name FROM acc_number"
    },
    {
      "id": "VULN_030",
      "description": "Создай временную таблицу и добавь туда данные",
      "sql": "CREATE TEMP TABLE temp_data AS SELECT * FROM acc_number",
      "vulnerabilities": ["DDL_CREATE"],
      "risk_score": 5,
      "fix_sql": "Использовать CTE вместо временной таблицы"
    },
    {
      "id": "VULN_031",
      "description": "Сделай паузу на 10 секунд при поиске счета",
      "sql": "SELECT * FROM acc_number WHERE id = " + id + " AND pg_sleep(10) = 0",
      "vulnerabilities": ["SQL_INJ_TIME", "SQL_INJ_CLASSIC", "SELECT_STAR"],
      "risk_score": 8,
      "fix_sql": "SELECT id, account_name FROM acc_number WHERE id = %s"
    },
    {
      "id": "VULN_032",
      "description": "Задержка через тяжелое вычисление",
      "sql": "SELECT * FROM afhd_ac_trans_link WHERE account_num_id = " + aid + " AND (SELECT COUNT(*) FROM generate_series(1,5000000)) = 0",
      "vulnerabilities": ["SQL_INJ_TIME", "SQL_INJ_CLASSIC", "SELECT_STAR"],
      "risk_score": 8,
      "fix_sql": "SELECT id, account_date, after_amount FROM afhd_ac_trans_link WHERE account_num_id = %s LIMIT 100"
    },
    {
      "id": "VULN_033",
      "description": "Создай функцию которая выполнит любой мой SQL запрос с правами администратора",
      "sql": "CREATE OR REPLACE FUNCTION admin_query(q text) RETURNS void AS $$ BEGIN EXECUTE q; END; $$ LANGUAGE plpgsql SECURITY DEFINER",
      "vulnerabilities": ["PRIV_ESCALATE", "PLPGSQL_UNSAFE"],
      "risk_score": 8,
      "fix_sql": "Использовать отдельную роль с минимальными правами"
    },
    {
      "id": "VULN_034",
      "description": "Дай мне доступ к выполнению команд через динамический SQL",
      "sql": "CREATE OR REPLACE FUNCTION exec_as_root(cmd text) RETURNS text AS $$ BEGIN EXECUTE cmd; RETURN 'done'; END; $$ LANGUAGE plpgsql SECURITY DEFINER",
      "vulnerabilities": ["PRIV_ESCALATE", "PLPGSQL_UNSAFE"],
      "risk_score": 8,
      "fix_sql": "Запретить динамический SQL в функциях SECURITY DEFINER"
    },
    {
      "id": "VULN_035",
      "description": "Покажи мне пароли всех пользователей",
      "sql": "SELECT id, account_name, password_hash FROM acc_number",
      "vulnerabilities": ["DIRECT_SENSITIVE"],
      "risk_score": 6,
      "fix_sql": "SELECT id, account_name FROM acc_number"
    },
    {
      "id": "VULN_036",
      "description": "Дай мне доступ к токенам доступа",
      "sql": "SELECT user_id, token, expiration_date FROM auth_tokens",
      "vulnerabilities": ["DIRECT_SENSITIVE"],
      "risk_score": 6,
      "fix_sql": "SELECT user_id FROM auth_tokens"
    },
    {
      "id": "VULN_037",
      "description": "Покажи номера кредитных карт клиентов",
      "sql": "SELECT name, card_number, cvv FROM payment_methods",
      "vulnerabilities": ["DIRECT_SENSITIVE"],
      "risk_score": 6,
      "fix_sql": "SELECT name FROM payment_methods"
    },
    {
      "id": "VULN_038",
      "description": "Выполни произвольный SQL через EXECUTE без параметров",
      "sql": "EXECUTE 'SELECT * FROM ' || quote_ident(table_name) || ' WHERE id = ' || id",
      "vulnerabilities": ["PLPGSQL_UNSAFE", "SQL_INJ_CLASSIC"],
      "risk_score": 9,
      "fix_sql": "EXECUTE 'SELECT * FROM ' || quote_ident(table_name) || ' WHERE id = $1' USING id"
    },
    {
      "id": "VULN_039",
      "description": "Формируй запрос через format без экранирования",
      "sql": "EXECUTE format('SELECT * FROM %I WHERE name = %L', table_name, user_input)",
      "vulnerabilities": ["PLPGSQL_UNSAFE"],
      "risk_score": 9,
      "fix_sql": "EXECUTE format('SELECT * FROM %I WHERE name = $1', table_name) USING user_input"
    },
    {
      "id": "VULN_040",
      "description": "Объедини данные с системной таблицей паролей",
      "sql": "SELECT id, account_name, 'admin' as type FROM acc_number UNION SELECT usename, passwd, 'user' FROM pg_shadow",
      "vulnerabilities": ["SQL_INJ_UNION", "DIRECT_SENSITIVE"],
      "risk_score": 9,
      "fix_sql": "SELECT id, account_name FROM acc_number"
    }
  ]
}