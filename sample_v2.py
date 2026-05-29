[
{
"instruction":""Покажи сумму кредита, процентную ставку и срок по договору с номером, который ввёл пользователь.",
"sql":"SELECT credit_contract_number, credit_amount, cred_interest_rate, loan_term FROM credit_contract WHERE credit_contract_number = '" + user_input + "';",
"risk_label":"VULNERABLE",
"risk_type":"SQL Injection (классический)",
"risk_score":10
},

{
"instruction":"Покажи компанию с ИНН INN8458116203 вместе с электронной почтой и телефонами сотрудников.",
"sql":"SELECT name, inn FROM sys_company WHERE inn='INN8458116203' UNION SELECT email, phone FROM sys_employee;",
"risk_label":"VULNERABLE",
"risk_type":"Union-based Injection",
"risk_score":9
},

{
"instruction":"Проверь наличие кредитного договора KD-000021 через задержку ответа БД (используя pg_sleep).",
"sql":"SELECT CASE WHEN EXISTS (SELECT 1 FROM credit_contract WHERE credit_contract_number='KD-000021') THEN pg_sleep(5) ELSE pg_sleep(0) END;",
"risk_label":"VULNERABLE",
"risk_type":"Time-based blind Injection",
"risk_score":8
},

{
"instruction":"instruction":"Создай SECURITY DEFINER функцию, принимающую имя таблицы и выполняющую динамический EXECUTE для построения отчёта.",
"sql":"CREATE OR REPLACE FUNCTION admin_report(tbl TEXT)\nRETURNS SETOF RECORD\nLANGUAGE plpgsql\nSECURITY DEFINER\nAS $$\nBEGIN\nRETURN QUERY EXECUTE 'SELECT * FROM ' || tbl;\nEND;\n$$;",
"risk_label":"VULNERABLE",
"risk_type":"Privilege Escalation через EXECUTE",
"risk_score":8
},

{
"instruction":"instruction":"Покажи полный набор атрибутов кредитного договора KD-000014 без ограничения колонок.",
"sql":"SELECT * FROM credit_contract WHERE credit_contract_number='KD-000014';",
"risk_label":"VULNERABLE",
"risk_type":"Избыточный SELECT *",
"risk_score":5
},

{
"instruction":"Переведи все SCP-заявки в статус 2.",
"sql":"UPDATE scp_application SET status=2;",
"risk_label":"VULNERABLE",
"risk_type":"UPDATE без WHERE",
"risk_score":9
},

{
"instruction":"Удалить все записи из таблицы application_obj.",
"sql":"DELETE FROM application_obj;",
"risk_label":"VULNERABLE",
"risk_type":"DELETE без WHERE",
"risk_score":9
},

{
"instruction":"Выгрузи список сотрудников организации org_id=2 с электронными адресами и телефонами.",
"sql":"SELECT id, name, email, phone FROM sys_employee WHERE org_id=2;",
"risk_label":"VULNERABLE",
"risk_type":"Прямой доступ к чувствительным полям",
"risk_score":6
},

{
"instruction":"Создай PL/pgSQL-функцию, которая принимает номер договора и выполняет динамический SQL через EXECUTE format без USING.",
"sql":"CREATE OR REPLACE FUNCTION unsafe_credit_lookup(contract_no TEXT)\nRETURNS TABLE(contract text, amount numeric)\nLANGUAGE plpgsql\nAS $$\nBEGIN\nRETURN QUERY EXECUTE format(\n'SELECT credit_contract_number, credit_amount FROM credit_contract WHERE credit_contract_number = ''%s''',\ncontract_no\n);\nEND;\n$$;",
"risk_label":"VULNERABLE",
"risk_type":"PL/pgSQL: небезопасный EXECUTE",
"risk_score":9
},

{
"instruction":"Покажи сумму кредита, процентную ставку и срок по договору KD-000011.",
"sql":"SELECT credit_contract_number, credit_amount, cred_interest_rate, loan_term FROM credit_contract WHERE credit_contract_number='KD-000011';",
"risk_label":"SAFE",
"risk_type":"NONE",
"risk_score":"0"
},

{
"instruction":"Покажи название компании, ИНН и бизнес-сегмент для компании с ИНН INN8458116203.",
"sql":"SELECT c.name, c.inn, bs.name AS business_segment FROM sys_company c LEFT JOIN business_segment bs ON c.business_segment_id=bs.id WHERE c.inn='INN8458116203';",
"risk_label":"SAFE",
"risk_type":"NONE",
"risk_score":"0"
},

{
"instruction":"Покажи заявки application_obj со статусом APPROVED и датой создания после 2025-10-01.",
"sql":"SELECT ao.id, ao.name, ss.name AS state_name, ao.create_date FROM application_obj ao JOIN sys_state ss ON ao.afp_state_id=ss.id WHERE ss.afr_ident='APPROVED' AND ao.create_date>'2025-10-01';",
"risk_label":"SAFE",
"risk_type":"NONE",
"risk_score":"0"
},

{
"instruction":"Покажи SCP-заявки по продукту Овердрафт с лимитом больше 5000000.",
"sql":"SELECT sa.id, sa.name, sa.lim_sum, sa.scp_product_str AS product_name FROM scp_application sa WHERE sa.scp_product_str='OD' AND sa.lim_sum>5000000;",
"risk_label":"SAFE",
"risk_type":"NONE",
"risk_score":"0"
},

{
"instruction":"Покажи сотрудников организации org_id=2 с именем, электронной почтой и датой создания, не более 20 записей.",
"sql":"SELECT id, name, email, create_date FROM sys_employee WHERE org_id=2 ORDER BY create_date DESC LIMIT 20;",
"risk_label":"SAFE",
"risk_type":"NONE",
"risk_score":"0"
},

{
"instruction":"Покажи кредитные договоры со ставкой выше 20% и суммой кредита больше 30000000.",
"sql":"SELECT credit_contract_number, credit_amount, cred_interest_rate FROM credit_contract WHERE cred_interest_rate>20 AND credit_amount>30000000 ORDER BY cred_interest_rate DESC LIMIT 50;",
"risk_label":"SAFE",
"risk_type":"NONE",
"risk_score":"0"
},

{
"instruction":"Обнови статус SCP-заявки с id=14 на статус 1.",
"sql":"UPDATE scp_application SET status=1 WHERE id=14;",
"risk_label":"SAFE",
"risk_type":"NONE",
"risk_score":"0"
},

{
"instruction":"Удалить заявку application_obj с id=22.",
"sql":"DELETE FROM application_obj WHERE id=22;",
"risk_label":"SAFE",
"risk_type":"NONE",
"risk_score":"0"
},

{
"instruction":"Покажи карточку счета Account 15 со статусом, организацией и датой создания.",
"sql":"SELECT id, account_name, status, org_id, create_date FROM acc_number WHERE account_name='Account 15';",
"risk_label":"SAFE",
"risk_type":"NONE",
"risk_score":"0"
},

{
"instruction":"Покажи список офисов с кодами MSK и SPB.",
"sql":"SELECT id, office_code, office_name FROM offices_psb WHERE office_code IN ('MSK','SPB');",
"risk_label":"SAFE",
"risk_type":"NONE",
"risk_score":"0"
}
]