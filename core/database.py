import sqlite3
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from config import AUDIT_MODULES

DB_PATH = Path(__file__).resolve().parents[1] / "data" / "metodo_empresa.db"

@contextmanager
def get_conn():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()

def init_db():
    with get_conn() as conn:
        conn.executescript(
            """
            PRAGMA foreign_keys = ON;

            CREATE TABLE IF NOT EXISTS companies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                legal_name TEXT,
                tax_id TEXT,
                country TEXT,
                city TEXT,
                sector TEXT,
                business_model TEXT,
                employees INTEGER DEFAULT 0,
                annual_revenue REAL DEFAULT 0,
                currency TEXT DEFAULT 'MXN',
                website TEXT,
                main_problem TEXT,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS audits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                objective TEXT,
                period_start TEXT,
                period_end TEXT,
                status TEXT DEFAULT 'No iniciado',
                created_at TEXT NOT NULL,
                FOREIGN KEY(company_id) REFERENCES companies(id)
            );

            CREATE TABLE IF NOT EXISTS company_profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                audit_id INTEGER NOT NULL UNIQUE,
                value_proposition TEXT,
                products_services TEXT,
                customer_segments TEXT,
                revenue_streams TEXT,
                strategic_objectives TEXT,
                decision_makers TEXT,
                perceived_bottlenecks TEXT,
                critical_dependencies TEXT,
                notes TEXT,
                updated_at TEXT NOT NULL,
                FOREIGN KEY(audit_id) REFERENCES audits(id)
            );

            CREATE TABLE IF NOT EXISTS module_reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                audit_id INTEGER NOT NULL,
                module_code TEXT NOT NULL,
                module_name TEXT NOT NULL,
                score REAL DEFAULT 0,
                status TEXT DEFAULT 'No iniciado',
                notes TEXT,
                updated_at TEXT NOT NULL,
                UNIQUE(audit_id, module_code),
                FOREIGN KEY(audit_id) REFERENCES audits(id)
            );

            CREATE TABLE IF NOT EXISTS findings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                audit_id INTEGER NOT NULL,
                module_code TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                evidence TEXT,
                root_cause TEXT,
                consequence TEXT,
                financial_impact REAL DEFAULT 0,
                operational_impact TEXT,
                human_impact TEXT,
                risk_level TEXT DEFAULT 'Medio',
                confidence TEXT DEFAULT 'Declarado',
                recommendation TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY(audit_id) REFERENCES audits(id)
            );

            CREATE TABLE IF NOT EXISTS actions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                finding_id INTEGER,
                audit_id INTEGER NOT NULL,
                action TEXT NOT NULL,
                owner TEXT,
                horizon TEXT,
                estimated_cost REAL DEFAULT 0,
                estimated_saving REAL DEFAULT 0,
                success_metric TEXT,
                status TEXT DEFAULT 'Pendiente',
                due_date TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY(finding_id) REFERENCES findings(id),
                FOREIGN KEY(audit_id) REFERENCES audits(id)
            );

            CREATE TABLE IF NOT EXISTS financial_rows (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                audit_id INTEGER NOT NULL,
                period TEXT,
                category TEXT,
                subcategory TEXT,
                description TEXT,
                amount REAL DEFAULT 0,
                source TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY(audit_id) REFERENCES audits(id)
            );
            """
        )

def _now():
    return datetime.utcnow().isoformat()

def create_company(data):
    with get_conn() as conn:
        cur = conn.execute(
            """
            INSERT INTO companies
            (name, legal_name, tax_id, country, city, sector, business_model,
             employees, annual_revenue, currency, website, main_problem, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                data["name"], data.get("legal_name"), data.get("tax_id"),
                data.get("country"), data.get("city"), data.get("sector"),
                data.get("business_model"), data.get("employees", 0),
                data.get("annual_revenue", 0), data.get("currency", "MXN"),
                data.get("website"), data.get("main_problem"), _now(),
            ),
        )
        return cur.lastrowid

def list_companies():
    with get_conn() as conn:
        return [dict(r) for r in conn.execute(
            "SELECT * FROM companies ORDER BY id DESC"
        ).fetchall()]

def create_audit(company_id, title, objective, period_start, period_end):
    with get_conn() as conn:
        cur = conn.execute(
            """
            INSERT INTO audits
            (company_id, title, objective, period_start, period_end, status, created_at)
            VALUES (?, ?, ?, ?, ?, 'No iniciado', ?)
            """,
            (company_id, title, objective, str(period_start), str(period_end), _now()),
        )
        audit_id = cur.lastrowid
        for module in AUDIT_MODULES:
            conn.execute(
                """
                INSERT INTO module_reviews
                (audit_id, module_code, module_name, score, status, notes, updated_at)
                VALUES (?, ?, ?, 0, 'No iniciado', '', ?)
                """,
                (audit_id, module["code"], module["name"], _now()),
            )
        conn.execute(
            "INSERT INTO company_profiles (audit_id, updated_at) VALUES (?, ?)",
            (audit_id, _now()),
        )
        return audit_id

def list_audits():
    with get_conn() as conn:
        return [dict(r) for r in conn.execute(
            """
            SELECT a.*, c.name AS company_name, c.currency, c.sector
            FROM audits a JOIN companies c ON c.id = a.company_id
            ORDER BY a.id DESC
            """
        ).fetchall()]

def get_audit(audit_id):
    with get_conn() as conn:
        row = conn.execute(
            """
            SELECT a.*, c.name AS company_name, c.currency, c.sector,
                   c.employees, c.annual_revenue, c.main_problem
            FROM audits a JOIN companies c ON c.id = a.company_id
            WHERE a.id = ?
            """,
            (audit_id,),
        ).fetchone()
        return dict(row) if row else None

def get_profile(audit_id):
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM company_profiles WHERE audit_id = ?", (audit_id,)
        ).fetchone()
        return dict(row) if row else None

def update_profile(audit_id, data):
    with get_conn() as conn:
        conn.execute(
            """
            UPDATE company_profiles SET
            value_proposition=?, products_services=?, customer_segments=?,
            revenue_streams=?, strategic_objectives=?, decision_makers=?,
            perceived_bottlenecks=?, critical_dependencies=?, notes=?, updated_at=?
            WHERE audit_id=?
            """,
            (
                data.get("value_proposition"), data.get("products_services"),
                data.get("customer_segments"), data.get("revenue_streams"),
                data.get("strategic_objectives"), data.get("decision_makers"),
                data.get("perceived_bottlenecks"), data.get("critical_dependencies"),
                data.get("notes"), _now(), audit_id,
            ),
        )

def get_module_reviews(audit_id):
    with get_conn() as conn:
        return [dict(r) for r in conn.execute(
            "SELECT * FROM module_reviews WHERE audit_id=? ORDER BY id", (audit_id,)
        ).fetchall()]

def update_module_review(audit_id, module_code, score, status, notes):
    with get_conn() as conn:
        conn.execute(
            """
            UPDATE module_reviews SET score=?, status=?, notes=?, updated_at=?
            WHERE audit_id=? AND module_code=?
            """,
            (score, status, notes, _now(), audit_id, module_code),
        )

def create_finding(data):
    with get_conn() as conn:
        cur = conn.execute(
            """
            INSERT INTO findings
            (audit_id, module_code, title, description, evidence, root_cause,
             consequence, financial_impact, operational_impact, human_impact,
             risk_level, confidence, recommendation, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                data["audit_id"], data["module_code"], data["title"],
                data.get("description"), data.get("evidence"), data.get("root_cause"),
                data.get("consequence"), data.get("financial_impact", 0),
                data.get("operational_impact"), data.get("human_impact"),
                data.get("risk_level", "Medio"), data.get("confidence", "Declarado"),
                data.get("recommendation"), _now(),
            ),
        )
        return cur.lastrowid

def list_findings(audit_id):
    with get_conn() as conn:
        return [dict(r) for r in conn.execute(
            "SELECT * FROM findings WHERE audit_id=? ORDER BY id DESC", (audit_id,)
        ).fetchall()]

def create_action(data):
    with get_conn() as conn:
        cur = conn.execute(
            """
            INSERT INTO actions
            (finding_id, audit_id, action, owner, horizon, estimated_cost,
             estimated_saving, success_metric, status, due_date, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'Pendiente', ?, ?)
            """,
            (
                data.get("finding_id"), data["audit_id"], data["action"],
                data.get("owner"), data.get("horizon"),
                data.get("estimated_cost", 0), data.get("estimated_saving", 0),
                data.get("success_metric"), data.get("due_date"), _now(),
            ),
        )
        return cur.lastrowid

def list_actions(audit_id):
    with get_conn() as conn:
        return [dict(r) for r in conn.execute(
            """
            SELECT a.*, f.title AS finding_title
            FROM actions a LEFT JOIN findings f ON f.id=a.finding_id
            WHERE a.audit_id=? ORDER BY a.id DESC
            """,
            (audit_id,),
        ).fetchall()]

def insert_financial_rows(audit_id, rows):
    with get_conn() as conn:
        for row in rows:
            conn.execute(
                """
                INSERT INTO financial_rows
                (audit_id, period, category, subcategory, description, amount, source, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    audit_id, row.get("period"), row.get("category"),
                    row.get("subcategory"), row.get("description"),
                    float(row.get("amount", 0)), row.get("source"), _now(),
                ),
            )

def list_financial_rows(audit_id):
    with get_conn() as conn:
        return [dict(r) for r in conn.execute(
            "SELECT * FROM financial_rows WHERE audit_id=? ORDER BY id DESC", (audit_id,)
        ).fetchall()]
