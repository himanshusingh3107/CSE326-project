import json
import logging
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Dict, Generator, List, Optional

from my_app.exceptions import DatabaseConnectionException
from my_app.models.member import Member
from my_app.repositories.base_repository import BaseRepository

logger = logging.getLogger(__name__)


class MemberRepository(BaseRepository[Member]):
    def __init__(self, database_path: Path, seed_data_path: Optional[Path] = None) -> None:
        self.database_path = database_path
        self.seed_data_path = seed_data_path
        self._initialize_schema()

    @contextmanager
    def _get_connection(self) -> Generator[sqlite3.Connection, None, None]:
        connection: Optional[sqlite3.Connection] = None
        try:
            connection = sqlite3.connect(
                self.database_path,
                check_same_thread=False,
                timeout=10.0,
            )
            connection.row_factory = sqlite3.Row
            connection.execute("PRAGMA foreign_keys = ON;")
            yield connection
        except sqlite3.OperationalError as error:
            logger.error(f"Database operational failure: {error}", exc_info=True)
            raise DatabaseConnectionException(f"Database access failure: {str(error)}")
        finally:
            if connection:
                connection.close()

    def _initialize_schema(self) -> None:
        with self._get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS members (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    age INTEGER NOT NULL,
                    gender TEXT NOT NULL,
                    phone TEXT NOT NULL UNIQUE,
                    email TEXT,
                    plan TEXT NOT NULL,
                    batch TEXT NOT NULL,
                    trainer TEXT,
                    join_date TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'Pending',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_members_phone ON members(phone);"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_members_name ON members(name);"
            )
            connection.commit()

        self._seed_initial_data_if_empty()

    def _seed_initial_data_if_empty(self) -> None:
        if not self.seed_data_path or not self.seed_data_path.exists():
            return

        with self._get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*) AS total FROM members;")
            row = cursor.fetchone()
            if row and row["total"] > 0:
                return

            try:
                with open(self.seed_data_path, "r", encoding="utf-8") as file_stream:
                    seed_records = json.load(file_stream)

                insert_query = """
                    INSERT INTO members (name, age, gender, phone, email, plan, batch, trainer, join_date, status)
                    VALUES (:name, :age, :gender, :phone, :email, :plan, :batch, :trainer, :join_date, :status);
                """
                records_to_insert = []
                for record in seed_records:
                    member_entity = Member.from_dict(record)
                    records_to_insert.append({
                        "name": member_entity.name,
                        "age": member_entity.age,
                        "gender": member_entity.gender,
                        "phone": member_entity.phone,
                        "email": member_entity.email,
                        "plan": member_entity.plan,
                        "batch": member_entity.batch,
                        "trainer": member_entity.trainer,
                        "join_date": member_entity.join_date,
                        "status": member_entity.status,
                    })

                cursor.executemany(insert_query, records_to_insert)
                connection.commit()
                logger.info(f"Seeded {len(records_to_insert)} records into members database.")
            except Exception as error:
                logger.warning(f"Could not load seed data: {error}")

    def get_all(
        self,
        search_query: Optional[str] = None,
        plan_filter: Optional[str] = None,
        fee_status: Optional[str] = None,
    ) -> List[Member]:
        query_clauses = ["1=1"]
        query_parameters: List[Any] = []

        if search_query:
            sanitized_search = f"%{search_query.strip().lower()}%"
            query_clauses.append("(LOWER(name) LIKE ? OR phone LIKE ? OR LOWER(email) LIKE ?)")
            query_parameters.extend([sanitized_search, sanitized_search, sanitized_search])

        if plan_filter:
            query_clauses.append("plan = ?")
            query_parameters.append(plan_filter.strip())

        if fee_status:
            query_clauses.append("status = ?")
            query_parameters.append(fee_status.strip())

        sql_statement = f"""
            SELECT id, name, age, gender, phone, email, plan, batch, trainer, join_date, status
            FROM members
            WHERE {' AND '.join(query_clauses)}
            ORDER BY id DESC;
        """

        with self._get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(sql_statement, query_parameters)
            rows = cursor.fetchall()
            return [Member.from_dict(dict(row)) for row in rows]

    def get_by_id(self, entity_id: int) -> Optional[Member]:
        with self._get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT id, name, age, gender, phone, email, plan, batch, trainer, join_date, status
                FROM members
                WHERE id = ?;
                """,
                (entity_id,),
            )
            row = cursor.fetchone()
            return Member.from_dict(dict(row)) if row else None

    def get_by_phone(self, phone: str) -> Optional[Member]:
        with self._get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT id, name, age, gender, phone, email, plan, batch, trainer, join_date, status
                FROM members
                WHERE phone = ?;
                """,
                (phone.strip(),),
            )
            row = cursor.fetchone()
            return Member.from_dict(dict(row)) if row else None

    def create(self, entity: Member) -> Member:
        with self._get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                INSERT INTO members (name, age, gender, phone, email, plan, batch, trainer, join_date, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                """,
                (
                    entity.name,
                    entity.age,
                    entity.gender,
                    entity.phone,
                    entity.email,
                    entity.plan,
                    entity.batch,
                    entity.trainer,
                    entity.join_date,
                    entity.status,
                ),
            )
            connection.commit()
            entity.id = cursor.lastrowid
            return entity

    def update(self, entity: Member) -> Member:
        with self._get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                UPDATE members
                SET name = ?, age = ?, gender = ?, phone = ?, email = ?,
                    plan = ?, batch = ?, trainer = ?, status = ?
                WHERE id = ?;
                """,
                (
                    entity.name,
                    entity.age,
                    entity.gender,
                    entity.phone,
                    entity.email,
                    entity.plan,
                    entity.batch,
                    entity.trainer,
                    entity.status,
                    entity.id,
                ),
            )
            connection.commit()
            return entity

    def update_fee_status(self, entity_id: int, new_status: str) -> bool:
        with self._get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE members SET status = ? WHERE id = ?;",
                (new_status, entity_id),
            )
            connection.commit()
            return cursor.rowcount > 0

    def delete(self, entity_id: int) -> bool:
        with self._get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM members WHERE id = ?;", (entity_id,))
            connection.commit()
            return cursor.rowcount > 0

    def get_summary_statistics(self) -> Dict[str, Any]:
        with self._get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*) as total_members FROM members;")
            total_members = cursor.fetchone()["total_members"]

            cursor.execute("SELECT COUNT(*) as paid_count FROM members WHERE status = 'Paid';")
            paid_count = cursor.fetchone()["paid_count"]

            cursor.execute("SELECT COUNT(*) as pending_count FROM members WHERE status = 'Pending';")
            pending_count = cursor.fetchone()["pending_count"]

            cursor.execute(
                """
                SELECT plan, COUNT(*) as count
                FROM members
                GROUP BY plan;
                """
            )
            plan_distribution = {row["plan"]: row["count"] for row in cursor.fetchall()}

            return {
                "total_members": total_members,
                "paid_members": paid_count,
                "pending_members": pending_count,
                "plan_distribution": plan_distribution,
            }
