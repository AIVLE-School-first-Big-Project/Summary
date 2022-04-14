BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "Member" (
	"m_id"	INTEGER,
	"m_email"	TEXT,
	"password"	TEXT,
	"tocken"	TEXT,
	"nickname"	TEXT,
	PRIMARY KEY("m_id" AUTOINCREMENT)
);
COMMIT;
