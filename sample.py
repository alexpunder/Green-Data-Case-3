{
  "dataset_info": {
    "name": "GreenData SQL Dataset (Human-like, Final)",
    "version": "4.0",
    "total": 100,
    "safe": 50,
    "vulnerable": 50,
    "description": "Финальная версия датасета с максимально естественными формулировками запросов."
  },
  "examples": [
    {
      "id": "SAFE_001",
      "description": "Посмотри счет номер 179, забыл его название",
      "sql": "SELECT id, account_name FROM acc_number WHERE id = 179",
      "vulnerabilities": [],
      "risk_score": 0
    },
    {
      "id": "SAFE_002",
      "description": "Найди все проводки контрагента 'Ренейссанс Хэви Индастрис Ronesans Endustri'",
      "sql": "SELECT id, account_date, after_amount FROM afhd_ac_trans_link WHERE contragent_name = 'Ренейссанс Хэви Индастрис Ronesans Endustri' LIMIT 100",
      "vulnerabilities": [],
      "risk_score": 0
    },
    {
      "id": "SAFE_003",
      "description": "Покажи заявку DOC-000001, что там по статусу?",
      "sql": "SELECT id, name, status, create_date FROM application_obj WHERE afl_doc_num = 'DOC-000001'",
      "vulnerabilities": [],
      "risk_score": 0
    },
    {
      "id": "SAFE_004",
      "description": "Выгрузи проводки по счету 179, где сумма больше 500000",
      "sql": "SELECT id, account_date, after_amount, contragent_name FROM afhd_ac_trans_link WHERE account_num_id = 179 AND after_amount > 500000 LIMIT 50",
      "vulnerabilities": [],
      "risk_score": 0
    },
    {
      "id": "SAFE_005",
      "description": "Дай данные по кредитному договору KD-000001",
      "sql": "SELECT id, credit_contract_number, credit_amount, cred_interest_rate FROM credit_contract WHERE credit_contract_number = 'KD-000001'",
      "vulnerabilities": [],
      "risk_score": 0
    },
    {
      "id": "SAFE_006",
      "description": "Найди сотрудника с почтой marija_37@example.org",
      "sql": "SELECT id, name, first_name, sur_name FROM sys_employee WHERE email = 'marija_37@example.org'",
      "vulnerabilities": [],
      "risk_score": 0
    },
    {
      "id": "SAFE_007",
      "description": "Какая компания имеет ИНН INN8605573518?",
      "sql": "SELECT id, name, inn, business_segment_id FROM sys_company WHERE inn = 'INN8605573518'",
      "vulnerabilities": [],
      "risk_score": 0
    },
    {
      "id": "SAFE_008",
      "description": "Нужны все проводки за январь 2026 года",
      "sql": "SELECT id, account_date, after_amount, contragent_name FROM afhd_ac_trans_link WHERE account_date BETWEEN '2026-01-01' AND '2026-01-31' LIMIT 200",
      "vulnerabilities": [],
      "risk_score": 0
    },
    {
      "id": "SAFE_009",
      "description": "Покажи одобренные заявки (статус 3)",
      "sql": "SELECT id, name, afl_doc_num, create_date FROM application_obj WHERE status = 3 LIMIT 50",
      "vulnerabilities": [],
      "risk_score": 0
    },
    {
      "id": "SAFE_010",
      "description": "Найди проводки 'Ситибанк' с НДС 20%",
      "sql": "SELECT id, account_date, after_amount, vat FROM afhd_ac_trans_link WHERE contragent_name = 'Ситибанк' AND vat = 20 LIMIT 100",
      "vulnerabilities": [],
      "risk_score": 0
    },
    {
      "id": "SAFE_011",
      "description": "Счета, созданные в 2025 году",
      "sql": "SELECT id, account_name, create_date FROM acc_number WHERE create_date BETWEEN '2025-01-01' AND '2025-12-31' LIMIT 100",
      "vulnerabilities": [],
      "risk_score": 0
    },
    {
      "id": "SAFE_012",
      "description": "Найди всех с фамилией 'Дементьев'",
      "sql": "SELECT id, name, first_name, sur_name, email FROM sys_employee WHERE sur_name = 'Дементьев' LIMIT 10",
      "vulnerabilities": [],
      "risk_score": 0
    },
    {
      "id": "SAFE_013",
      "description": "Компании из сегмента МСБ (business_segment_id = 1)",
      "sql": "SELECT id, name, inn FROM sys_company WHERE business_segment_id = 1 LIMIT 50",
      "vulnerabilities": [],
      "risk_score": 0
    },
    {
      "id": "SAFE_014",
      "description": "Проводки со скидкой больше 10%",
      "sql": "SELECT id, account_date, after_amount, discount, contragent_name FROM afhd_ac_trans_link WHERE discount > 10 LIMIT 100",
      "vulnerabilities": [],
      "risk_score": 0
    },
    {
      "id": "SAFE_015",
      "description": "Что за заявка 'Application 1'?",
      "sql": "SELECT id, name, status, afl_doc_num, create_date FROM application_obj WHERE name = 'Application 1'",
      "vulnerabilities": [],
      "risk_score": 0
    },
    {
      "id": "SAFE_016",
      "description": "Кредитные договоры со ставкой выше 20%",
      "sql": "SELECT id, credit_contract_number, credit_amount, cred_interest_rate FROM credit_contract WHERE cred_interest_rate > 20 LIMIT 50",
      "vulnerabilities": [],
      "risk_score": 0
    },
    {
      "id": "SAFE_017",
      "description": "Проводки за февраль 2026",
      "sql": "SELECT id, account_date, after_amount FROM afhd_ac_trans_link WHERE account_date BETWEEN '2026-02-01' AND '2026-02-28' LIMIT 200",
      "vulnerabilities": [],
      "risk_score": 0
    },
    {
      "id": "SAFE_018",
      "description": "Покажи дочерние счета для счета 10",
      "sql": "SELECT id, account_name, parent_acc FROM acc_number WHERE parent_acc = 10 LIMIT 50",
      "vulnerabilities": [],
      "risk_score": 0
    },
    {
      "id": "SAFE_019",
      "description": "Заявки, созданные в мае 2026",
      "sql": "SELECT id, name, create_date FROM application_obj WHERE create_date BETWEEN '2026-05-01' AND '2026-05-31' LIMIT 100",
      "vulnerabilities": [],
      "risk_score": 0
    },
    {
      "id": "SAFE_020",
      "description": "Движения по контрагенту 'ГК Орими Трэйд'",
      "sql": "SELECT id, account_date, after_amount FROM afhd_ac_trans_link WHERE contragent_name = 'ГК Орими Трэйд' LIMIT 50",
      "vulnerabilities": [],
      "risk_score": 0
    },
    {
      "id": "SAFE_021",
      "description": "Найди компанию 'ООО «Белоусова»'",
      "sql": "SELECT id, name, inn FROM sys_company WHERE short_name = 'ООО «Белоусова»'",
      "vulnerabilities": [],
      "risk_score": 0
    },
    {
      "id": "SAFE_022",
      "description": "Проводки с отрицательным дисконтом",
      "sql": "SELECT id, account_date, after_amount, discount FROM afhd_ac_trans_link WHERE discount < 0 LIMIT 50",
      "vulnerabilities": [],
      "risk_score": 0
    },
    {
      "id": "SAFE_023",
      "description": "Сотрудники из головного офиса (org_id = 1)",
      "sql": "SELECT id, name, email, phone FROM sys_employee WHERE org_id = 1 LIMIT 50",
      "vulnerabilities": [],
      "risk_score": 0
    },
    {
      "id": "SAFE_024",
      "description": "Заявки инициатора 97",
      "sql": "SELECT id, name, afl_doc_num, status FROM application_obj WHERE initiator_id = 97 LIMIT 50",
      "vulnerabilities": [],
      "risk_score": 0
    },
    {
      "id": "SAFE_025",
      "description": "Проводки за последние 3 месяца",
      "sql": "SELECT id, account_date, after_amount, contragent_name FROM afhd_ac_trans_link WHERE account_date > NOW() - INTERVAL '3 months' LIMIT 500",
      "vulnerabilities": [],
      "risk_score": 0
    },
    {
      "id": "SAFE_026",
      "description": "Кредиты клиента 147",
      "sql": "SELECT id, credit_contract_number, credit_amount FROM credit_contract WHERE link_customer_id = 147 LIMIT 20",
      "vulnerabilities": [],
      "risk_score": 0
    },
    {
      "id": "SAFE_027",
      "description": "Выгрузи все счета по порядку",
      "sql": "SELECT id, account_name, status FROM acc_number ORDER BY id LIMIT 100",
      "vulnerabilities": [],
      "risk_score": 0
    },
    {
      "id": "SAFE_028",
      "description": "Проводки на сумму от 100 до 500 тысяч",
      "sql": "SELECT id, account_date, after_amount FROM afhd_ac_trans_link WHERE after_amount BETWEEN 100000 AND 500000 LIMIT 200",
      "vulnerabilities": [],
      "risk_score": 0
    },
    {
      "id": "SAFE_029",
      "description": "Заявки менеджера 105",
      "sql": "SELECT id, name, afl_doc_num FROM application_obj WHERE emp_id = 105 LIMIT 50",
      "vulnerabilities": [],
      "risk_score": 0
    },
    {
      "id": "SAFE_030",
      "description": "Проводки 'Fonbet'",
      "sql": "SELECT id, account_date, after_amount FROM afhd_ac_trans_link WHERE contragent_name = 'Fonbet' LIMIT 20",
      "vulnerabilities": [],
      "risk_score": 0
    },
    {
      "id": "SAFE_031",
      "description": "Компании из 3-го офиса",
      "sql": "SELECT id, name, inn FROM sys_company WHERE org_id = 3 LIMIT 50",
      "vulnerabilities": [],
      "risk_score": 0
    },
    {
      "id": "SAFE_032",
      "description": "Проводки без НДС (vat = 0)",
      "sql": "SELECT id, account_date, after_amount, contragent_name FROM afhd_ac_trans_link WHERE vat = 0 LIMIT 200",
      "vulnerabilities": [],
      "risk_score": 0
    },
    {
      "id": "SAFE_033",
      "description": "Активные счета (status = 1)",
      "sql": "SELECT id, account_name FROM acc_number WHERE status = 1 LIMIT 50",
      "vulnerabilities": [],
      "risk_score": 0
    },
    {
      "id": "SAFE_034",
      "description": "Сотрудник с телефоном 8 357 566 4236",
      "sql": "SELECT id, name, sur_name FROM sys_employee WHERE phone = '8 357 566 4236'",
      "vulnerabilities": [],
      "risk_score": 0
    },
    {
      "id": "SAFE_035",
      "description": "Заявки после 1 марта 2026",
      "sql": "SELECT id, name, create_date FROM application_obj WHERE create_date > '2026-03-01' ORDER BY create_date LIMIT 100",
      "vulnerabilities": [],
      "risk_score": 0
    },
    {
      "id": "SAFE_036",
      "description": "Проводки со скидкой меньше 1%",
      "sql": "SELECT id, account_date, after_amount, discount FROM afhd_ac_trans_link WHERE discount < 1 LIMIT 100",
      "vulnerabilities": [],
      "risk_score": 0
    },
    {
      "id": "SAFE_037",
      "description": "Кредиты сроком более 36 месяцев",
      "sql": "SELECT id, credit_contract_number, loan_term, credit_amount FROM credit_contract WHERE loan_term > 36 LIMIT 50",
      "vulnerabilities": [],
      "risk_score": 0
    },
    {
      "id": "SAFE_038",
      "description": "Движения по 'Ренейссанс Констракшн'",
      "sql": "SELECT id, account_date, after_amount FROM afhd_ac_trans_link WHERE contragent_name = 'Ренейссанс Констракшн (Ronesans Holding Anonim Sirketi)' LIMIT 50",
      "vulnerabilities": [],
      "risk_score": 0
    },
    {
      "id": "SAFE_039",
      "description": "Завершенные заявки (status = 5)",
      "sql": "SELECT id, name, afl_doc_num, create_date FROM application_obj WHERE status = 5 LIMIT 50",
      "vulnerabilities": [],
      "risk_score": 0
    },
    {
      "id": "SAFE_040",
      "description": "Системные счета (is_system = 1)",
      "sql": "SELECT id, account_name FROM acc_number WHERE is_system = 1 LIMIT 50",
      "vulnerabilities": [],
      "risk_score": 0
    },
    {
      "id": "SAFE_041",
      "description": "Проводки 'Ситибанк' за 2025 год",
      "sql": "SELECT id, account_date, after_amount FROM afhd_ac_trans_link WHERE contragent_name = 'Ситибанк' AND account_date BETWEEN '2025-01-01' AND '2025-12-31' LIMIT 100",
      "vulnerabilities": [],
      "risk_score": 0
    },
    {
      "id": "SAFE_042",
      "description": "Сотрудники с именем 'Ираида'",
      "sql": "SELECT id, name, sur_name, email FROM sys_employee WHERE first_name = 'Ираида' LIMIT 10",
      "vulnerabilities": [],
      "risk_score": 0
    },
    {
      "id": "SAFE_043",
      "description": "VIP-компании (business_segment_id = 4)",
      "sql": "SELECT id, name FROM sys_company WHERE business_segment_id = 4 LIMIT 30",
      "vulnerabilities": [],
      "risk_score": 0
    },
    {
      "id": "SAFE_044",
      "description": "Исключенные проводки (is_excepted = 1)",
      "sql": "SELECT id, account_date, after_amount, contragent_name FROM afhd_ac_trans_link WHERE is_excepted = 1 LIMIT 100",
      "vulnerabilities": [],
      "risk_score": 0
    },
    {
      "id": "SAFE_045",
      "description": "Заявки с 100 по 200",
      "sql": "SELECT id, name, status, create_date FROM application_obj WHERE id BETWEEN 100 AND 200 LIMIT 100",
      "vulnerabilities": [],
      "risk_score": 0
    },
    {
      "id": "SAFE_046",
      "description": "Проводки по дебету (debit_credit_id = 1)",
      "sql": "SELECT id, account_date, after_amount FROM afhd_ac_trans_link WHERE debit_credit_id = 1 LIMIT 200",
      "vulnerabilities": [],
      "risk_score": 0
    },
    {
      "id": "SAFE_047",
      "description": "Отказанные кредиты (status = 2)",
      "sql": "SELECT id, credit_contract_number, credit_amount FROM credit_contract WHERE status = 2 LIMIT 50",
      "vulnerabilities": [],
      "risk_score": 0
    },
    {
      "id": "SAFE_048",
      "description": "Проводки 'ВымпелКом'",
      "sql": "SELECT id, account_date, after_amount FROM afhd_ac_trans_link WHERE contragent_name = 'ВымпелКом' LIMIT 50",
      "vulnerabilities": [],
      "risk_score": 0
    },
    {
      "id": "SAFE_049",
      "description": "Счета с ord больше 50",
      "sql": "SELECT id, account_name, ord FROM acc_number WHERE ord > 50 LIMIT 100",
      "vulnerabilities": [],
      "risk_score": 0
    },
    {
      "id": "SAFE_050",
      "description": "Заявки декабря 2025",
      "sql": "SELECT id, name, create_date FROM application_obj WHERE create_date BETWEEN '2025-12-01' AND '2025-12-31' LIMIT 50",
      "vulnerabilities": [],
      "risk_score": 0
    },
    {
      "id": "VULN_001",
      "description": "Найди счет с названием 'Расчетный счет 1'",
      "sql": "SELECT * FROM acc_number WHERE account_name = 'Расчетный счет 1'",
      "vulnerabilities": ["SQL_INJ_CLASSIC", "SELECT_STAR"],
      "risk_score": 10,
      "fix_sql": "SELECT id, account_name FROM acc_number WHERE account_name = %s LIMIT 10"
    },
    {
      "id": "VULN_002",
      "description": "Найди проводки контрагента 'Ренейссанс Хэви Индастрис'",
      "sql": "SELECT * FROM afhd_ac_trans_link WHERE contragent_name = 'Ренейссанс Хэви Индастрис'",
      "vulnerabilities": ["SQL_INJ_CLASSIC", "SELECT_STAR"],
      "risk_score": 10,
      "fix_sql": "SELECT id, account_date, after_amount FROM afhd_ac_trans_link WHERE contragent_name = %s LIMIT 100"
    },
    {
      "id": "VULN_003",
      "description": "Поменяй статус у заявки DOC-000001 на 5",
      "sql": "UPDATE application_obj SET status = 5 WHERE afl_doc_num = 'DOC-000001'",
      "vulnerabilities": ["DML_NO_WHERE"],
      "risk_score": 8,
      "fix_sql": "UPDATE application_obj SET status = %s WHERE id = %s"
    },
    {
      "id": "VULN_004",
      "description": "Покажи все проводки по счету 179",
      "sql": "SELECT * FROM afhd_ac_trans_link WHERE account_num_id = 179",
      "vulnerabilities": ["SELECT_STAR", "NO_PAGINATION"],
      "risk_score": 7,
      "fix_sql": "SELECT id, account_date, after_amount FROM afhd_ac_trans_link WHERE account_num_id = %s LIMIT 100"
    },
    {
      "id": "VULN_005",
      "description": "Выгрузи все счета",
      "sql": "SELECT * FROM acc_number",
      "vulnerabilities": ["SELECT_STAR", "NO_PAGINATION"],
      "risk_score": 7,
      "fix_sql": "SELECT id, account_name, status FROM acc_number LIMIT 100"
    },
    {
      "id": "VULN_006",
      "description": "Обнови ставку для договора KD-000001 на 15.5",
      "sql": "UPDATE credit_contract SET cred_interest_rate = 15.5 WHERE credit_contract_number = 'KD-000001'",
      "vulnerabilities": ["DML_NO_WHERE"],
      "risk_score": 8,
      "fix_sql": "UPDATE credit_contract SET cred_interest_rate = %s WHERE id = %s"
    },
    {
      "id": "VULN_007",
      "description": "Найди сотрудника marija_37@example.org",
      "sql": "SELECT * FROM sys_employee WHERE email = 'marija_37@example.org'",
      "vulnerabilities": ["SELECT_STAR"],
      "risk_score": 5,
      "fix_sql": "SELECT id, name, email FROM sys_employee WHERE email = %s LIMIT 1"
    },
    {
      "id": "VULN_008",
      "description": "Покажи все проводки за январь 2026",
      "sql": "SELECT * FROM afhd_ac_trans_link WHERE account_date BETWEEN '2026-01-01' AND '2026-01-31'",
      "vulnerabilities": ["SELECT_STAR", "NO_PAGINATION"],
      "risk_score": 7,
      "fix_sql": "SELECT id, account_date, after_amount FROM afhd_ac_trans_link WHERE account_date BETWEEN %s AND %s LIMIT 1000"
    },
    {
      "id": "VULN_009",
      "description": "Удали все заявки со статусом 4",
      "sql": "DELETE FROM application_obj WHERE status = 4",
      "vulnerabilities": ["DML_NO_WHERE"],
      "risk_score": 9,
      "fix_sql": "DELETE FROM application_obj WHERE id = %s"
    },
    {
      "id": "VULN_010",
      "description": "Активируй все счета (status = 1)",
      "sql": "UPDATE acc_number SET status = 1",
      "vulnerabilities": ["DML_NO_WHERE"],
      "risk_score": 9,
      "fix_sql": "UPDATE acc_number SET status = 1 WHERE id = %s"
    },
    {
      "id": "VULN_011",
      "description": "Найди проводки с контрагентом 'Fonbet'",
      "sql": "SELECT * FROM afhd_ac_trans_link WHERE contragent_name = 'Fonbet'",
      "vulnerabilities": ["SELECT_STAR"],
      "risk_score": 5,
      "fix_sql": "SELECT id, account_date, after_amount FROM afhd_ac_trans_link WHERE contragent_name = %s LIMIT 100"
    },
    {
      "id": "VULN_012",
      "description": "Добавь проводку для счета 179 на сумму 99999",
      "sql": "INSERT INTO afhd_ac_trans_link (account_num_id, after_amount) VALUES (179, 99999)",
      "vulnerabilities": [],
      "risk_score": 0,
      "fix_sql": null
    },
    {
      "id": "VULN_013",
      "description": "Найди компанию INN8605573518",
      "sql": "SELECT * FROM sys_company WHERE inn = 'INN8605573518'",
      "vulnerabilities": ["SELECT_STAR"],
      "risk_score": 5,
      "fix_sql": "SELECT id, name, inn FROM sys_company WHERE inn = %s LIMIT 1"
    },
    {
      "id": "VULN_014",
      "description": "Покажи названия счетов и имена сотрудников вместе",
      "sql": "SELECT account_name FROM acc_number UNION SELECT name FROM sys_employee",
      "vulnerabilities": ["SQL_INJ_UNION"],
      "risk_score": 9,
      "fix_sql": "SELECT account_name FROM acc_number"
    },
    {
      "id": "VULN_015",
      "description": "Найди проводку 12345 и подожди",
      "sql": "SELECT * FROM afhd_ac_trans_link WHERE id = 12345 OR pg_sleep(5)",
      "vulnerabilities": ["SQL_INJ_TIME", "SELECT_STAR"],
      "risk_score": 8,
      "fix_sql": "SELECT id, account_date, after_amount FROM afhd_ac_trans_link WHERE id = %s"
    },
    {
      "id": "VULN_016",
      "description": "Все заявки за 2026 год без сортировки",
      "sql": "SELECT * FROM application_obj WHERE create_date > '2026-01-01'",
      "vulnerabilities": ["SELECT_STAR", "NO_PAGINATION"],
      "risk_score": 7,
      "fix_sql": "SELECT id, name, status, create_date FROM application_obj WHERE create_date > %s LIMIT 1000"
    },
    {
      "id": "VULN_017",
      "description": "Очисти все проводки по счету 179",
      "sql": "DELETE FROM afhd_ac_trans_link WHERE account_num_id = 179",
      "vulnerabilities": ["DML_NO_WHERE"],
      "risk_score": 9,
      "fix_sql": "DELETE FROM afhd_ac_trans_link WHERE id = %s"
    },
    {
      "id": "VULN_018",
      "description": "Переименуй компанию INN8605573518 в 'Новое Имя'",
      "sql": "UPDATE sys_company SET name = 'Новое Имя' WHERE inn = 'INN8605573518'",
      "vulnerabilities": ["DML_NO_WHERE"],
      "risk_score": 8,
      "fix_sql": "UPDATE sys_company SET name = %s WHERE id = %s"
    },
    {
      "id": "VULN_019",
      "description": "Найди все договоры со ставкой выше 15",
      "sql": "SELECT * FROM credit_contract WHERE cred_interest_rate > 15",
      "vulnerabilities": ["SELECT_STAR", "NO_PAGINATION"],
      "risk_score": 7,
      "fix_sql": "SELECT id, credit_contract_number, credit_amount FROM credit_contract WHERE cred_interest_rate > %s LIMIT 200"
    },
    {
      "id": "VULN_020",
      "description": "Добавь нового сотрудника Петрова",
      "sql": "INSERT INTO sys_employee (name, email) VALUES ('Петров', 'petrov@example.com')",
      "vulnerabilities": [],
      "risk_score": 0,
      "fix_sql": null
    },
    {
      "id": "VULN_021",
      "description": "Найди заявку DOC-999999",
      "sql": "SELECT * FROM application_obj WHERE afl_doc_num = 'DOC-999999'",
      "vulnerabilities": ["SELECT_STAR"],
      "risk_score": 5,
      "fix_sql": "SELECT id, name, afl_doc_num FROM application_obj WHERE afl_doc_num = %s LIMIT 1"
    },
    {
      "id": "VULN_022",
      "description": "Покажи проводки 'ГК Орими Трэйд'",
      "sql": "SELECT * FROM afhd_ac_trans_link WHERE contragent_name = 'ГК Орими Трэйд'",
      "vulnerabilities": ["SELECT_STAR"],
      "risk_score": 5,
      "fix_sql": "SELECT id, account_date, after_amount, discount FROM afhd_ac_trans_link WHERE contragent_name = %s LIMIT 100"
    },
    {
      "id": "VULN_023",
      "description": "Обнови почту сотрудника с id 1 на new@example.com",
      "sql": "UPDATE sys_employee SET email = 'new@example.com' WHERE id = 1",
      "vulnerabilities": [],
      "risk_score": 0,
      "fix_sql": null
    },
    {
      "id": "VULN_024",
      "description": "Покажи все заявки инициатора 97",
      "sql": "SELECT * FROM application_obj WHERE initiator_id = 97",
      "vulnerabilities": ["SELECT_STAR", "NO_PAGINATION"],
      "risk_score": 7,
      "fix_sql": "SELECT id, name, afl_doc_num, create_date FROM application_obj WHERE initiator_id = %s LIMIT 100"
    },
    {
      "id": "VULN_025",
      "description": "Объедини счета и состояния",
      "sql": "SELECT account_name FROM acc_number UNION SELECT name FROM sys_state",
      "vulnerabilities": ["SQL_INJ_UNION"],
      "risk_score": 9,
      "fix_sql": "SELECT account_name FROM acc_number"
    },
    {
      "id": "VULN_026",
      "description": "Найди проводку 12345 и посчитай миллион строк",
      "sql": "SELECT * FROM afhd_ac_trans_link WHERE id = 12345 OR (SELECT COUNT(*) FROM generate_series(1,1000000)) = 0",
      "vulnerabilities": ["SQL_INJ_TIME", "SELECT_STAR"],
      "risk_score": 8,
      "fix_sql": "SELECT id FROM afhd_ac_trans_link WHERE id = %s"
    },
    {
      "id": "VULN_027",
      "description": "Удали проводки 'Fonbet'",
      "sql": "DELETE FROM afhd_ac_trans_link WHERE contragent_name = 'Fonbet'",
      "vulnerabilities": ["DML_NO_WHERE"],
      "risk_score": 9,
      "fix_sql": "DELETE FROM afhd_ac_trans_link WHERE id = %s"
    },
    {
      "id": "VULN_028",
      "description": "Выгрузи всех сотрудников",
      "sql": "SELECT * FROM sys_employee",
      "vulnerabilities": ["SELECT_STAR", "NO_PAGINATION"],
      "risk_score": 7,
      "fix_sql": "SELECT id, name, email FROM sys_employee LIMIT 100"
    },
    {
      "id": "VULN_029",
      "description": "Найди договоры с суммой больше 1000000",
      "sql": "SELECT * FROM credit_contract WHERE credit_amount > 1000000",
      "vulnerabilities": ["SELECT_STAR", "NO_PAGINATION"],
      "risk_score": 7,
      "fix_sql": "SELECT id, credit_contract_number, credit_amount FROM credit_contract WHERE credit_amount > %s LIMIT 200"
    },
    {
      "id": "VULN_030",
      "description": "Обнови статус всех одобренных заявок на завершено",
      "sql": "UPDATE application_obj SET status = 5 WHERE status = 3",
      "vulnerabilities": ["DML_NO_WHERE"],
      "risk_score": 8,
      "fix_sql": "UPDATE application_obj SET status = %s WHERE id = %s"
    },
    {
      "id": "VULN_031",
      "description": "Покажи счета с 10 по 20",
      "sql": "SELECT * FROM acc_number WHERE id BETWEEN 10 AND 20",
      "vulnerabilities": ["SELECT_STAR"],
      "risk_score": 5,
      "fix_sql": "SELECT id, account_name FROM acc_number WHERE id BETWEEN %s AND %s LIMIT 100"
    },
    {
      "id": "VULN_032",
      "description": "Проводки за январь 2025",
      "sql": "SELECT * FROM afhd_ac_trans_link WHERE account_date BETWEEN '2025-01-01' AND '2025-01-31'",
      "vulnerabilities": ["SELECT_STAR", "NO_PAGINATION"],
      "risk_score": 7,
      "fix_sql": "SELECT id, account_date, after_amount FROM afhd_ac_trans_link WHERE account_date BETWEEN %s AND %s LIMIT 1000"
    },
    {
      "id": "VULN_033",
      "description": "Объедини компании и таблицы БД",
      "sql": "SELECT name FROM sys_company UNION SELECT table_name FROM information_schema.tables",
      "vulnerabilities": ["SQL_INJ_UNION"],
      "risk_score": 9,
      "fix_sql": "SELECT name FROM sys_company"
    },
    {
      "id": "VULN_034",
      "description": "Создай функцию для выполнения команд",
      "sql": "CREATE FUNCTION exec(cmd text) RETURNS void AS $$ BEGIN EXECUTE cmd; END; $$ LANGUAGE plpgsql SECURITY DEFINER",
      "vulnerabilities": ["PRIV_ESCALATE", "PLPGSQL_UNSAFE"],
      "risk_score": 9,
      "fix_sql": "Не использовать динамический SQL"
    },
    {
      "id": "VULN_035",
      "description": "Покажи пароли сотрудников",
      "sql": "SELECT id, name, password FROM sys_employee",
      "vulnerabilities": ["DIRECT_SENSITIVE"],
      "risk_score": 6,
      "fix_sql": "SELECT id, name FROM sys_employee"
    },
    {
      "id": "VULN_036",
      "description": "Заявки после 1 марта 2026 без лимита",
      "sql": "SELECT * FROM application_obj WHERE create_date > '2026-03-01'",
      "vulnerabilities": ["SELECT_STAR", "NO_PAGINATION"],
      "risk_score": 7,
      "fix_sql": "SELECT id, name, create_date FROM application_obj WHERE create_date > %s LIMIT 500"
    },
    {
      "id": "VULN_037",
      "description": "Обнови сумму кредита KD-000001 на 5000000",
      "sql": "UPDATE credit_contract SET credit_amount = 5000000 WHERE credit_contract_number = 'KD-000001'",
      "vulnerabilities": ["DML_NO_WHERE"],
      "risk_score": 8,
      "fix_sql": "UPDATE credit_contract SET credit_amount = %s WHERE id = %s"
    },
    {
      "id": "VULN_038",
      "description": "Найди компанию 'ООО Ромашка'",
      "sql": "SELECT * FROM sys_company WHERE name = 'ООО Ромашка'",
      "vulnerabilities": ["SELECT_STAR"],
      "risk_score": 5,
      "fix_sql": "SELECT id, name, inn FROM sys_company WHERE name = %s LIMIT 10"
    },
    {
      "id": "VULN_039",
      "description": "Удали счет acc_number с id 12345",
      "sql": "DELETE FROM acc_number WHERE id = 12345",
      "vulnerabilities": ["DML_NO_WHERE"],
      "risk_score": 8,
      "fix_sql": "DELETE FROM acc_number WHERE id = %s"
    },
    {
      "id": "VULN_040",
      "description": "Отсортируй счета по названию",
      "sql": "SELECT id, account_name FROM acc_number ORDER BY account_name",
      "vulnerabilities": ["NO_PAGINATION"],
      "risk_score": 4,
      "fix_sql": "SELECT id, account_name FROM acc_number ORDER BY account_name LIMIT 100"
    },
    {
      "id": "VULN_041",
      "description": "Найди счета с id 1,2,3",
      "sql": "SELECT * FROM acc_number WHERE id IN (1,2,3)",
      "vulnerabilities": ["SELECT_STAR"],
      "risk_score": 5,
      "fix_sql": "SELECT id, account_name FROM acc_number WHERE id IN (%s)"
    },
    {
      "id": "VULN_042",
      "description": "Проводки с дисконтом больше 0",
      "sql": "SELECT * FROM afhd_ac_trans_link WHERE discount > 0",
      "vulnerabilities": ["SELECT_STAR", "NO_PAGINATION"],
      "risk_score": 7,
      "fix_sql": "SELECT id, account_date, after_amount, discount FROM afhd_ac_trans_link WHERE discount > %s LIMIT 1000"
    },
    {
      "id": "VULN_043",
      "description": "Дочерние счета для parent_acc 10",
      "sql": "SELECT * FROM acc_number WHERE parent_acc = 10",
      "vulnerabilities": ["SELECT_STAR"],
      "risk_score": 5,
      "fix_sql": "SELECT id, account_name FROM acc_number WHERE parent_acc = %s LIMIT 50"
    },
    {
      "id": "VULN_044",
      "description": "Обнови телефон для email ivan@example.com",
      "sql": "UPDATE sys_employee SET phone = '123456' WHERE email = 'ivan@example.com'",
      "vulnerabilities": ["DML_NO_WHERE"],
      "risk_score": 8,
      "fix_sql": "UPDATE sys_employee SET phone = %s WHERE id = %s"
    },
    {
      "id": "VULN_045",
      "description": "Все заявки с 100 по 200 без лимита",
      "sql": "SELECT * FROM application_obj WHERE id BETWEEN 100 AND 200",
      "vulnerabilities": ["SELECT_STAR"],
      "risk_score": 5,
      "fix_sql": "SELECT id, name, create_date FROM application_obj WHERE id BETWEEN %s AND %s LIMIT 100"
    },
    {
      "id": "VULN_046",
      "description": "Объедини контрагентов и компании",
      "sql": "SELECT contragent_name FROM afhd_ac_trans_link UNION SELECT name FROM sys_company",
      "vulnerabilities": ["SQL_INJ_UNION"],
      "risk_score": 9,
      "fix_sql": "SELECT contragent_name FROM afhd_ac_trans_link"
    },
    {
      "id": "VULN_047",
      "description": "Выбери счета и удали таблицу",
      "sql": "SELECT * FROM acc_number; DROP TABLE acc_number;",
      "vulnerabilities": ["MULTI_STATEMENT"],
      "risk_score": 10,
      "fix_sql": "SELECT id, account_name FROM acc_number"
    },
    {
      "id": "VULN_048",
      "description": "Все кредитные договоры без фильтра",
      "sql": "SELECT * FROM credit_contract",
      "vulnerabilities": ["SELECT_STAR", "NO_PAGINATION"],
      "risk_score": 7,
      "fix_sql": "SELECT id, credit_contract_number, credit_amount FROM credit_contract LIMIT 200"
    },
    {
      "id": "VULN_049",
      "description": "Заявки менеджера 105 без фильтра",
      "sql": "SELECT * FROM application_obj WHERE emp_id = 105",
      "vulnerabilities": ["SELECT_STAR", "NO_PAGINATION"],
      "risk_score": 7,
      "fix_sql": "SELECT id, name, afl_doc_num FROM application_obj WHERE emp_id = %s LIMIT 100"
    },
    {
      "id": "VULN_050",
      "description": "Обнови статус всех дебетовых проводок на исключен",
      "sql": "UPDATE afhd_ac_trans_link SET is_excepted = 1 WHERE debit_credit_id = 1",
      "vulnerabilities": ["DML_NO_WHERE"],
      "risk_score": 8,
      "fix_sql": "UPDATE afhd_ac_trans_link SET is_excepted = 1 WHERE id = %s"
    }
  ]
}