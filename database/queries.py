GET_ALL_WORKERS = """
SELECT id, vards_uzvards, datums, nostradatas_stundas, padaritais_darbs 
FROM stradnieka_apkopojums
"""

ADD_WORKER = """
INSERT INTO stradnieka_apkopojums 
(vards_uzvards, datums, nostradatas_stundas, padaritais_darbs)
VALUES (%s, %s, %s, %s)
"""

GET_ALL_EMPLOYERS = """
SELECT id, vards_uzvards, izvertejums, alga 
FROM uzņemeja_apkopojums
"""

GET_USER_BY_USERNAME = """
SELECT id, username, password_hash, salt, is_admin 
FROM users 
WHERE username = %s
"""

CREATE_USER = """
INSERT INTO users 
(username, password_hash, salt, is_admin)
VALUES (%s, %s, %s, %s)
"""