import sqlalchemy as db
from sqlalchemy.sql.expression import select

from infrastructure.database.sql.api.engine import DBEngine
from infrastructure.database.sql.models.base import Base


class AnalyticsSQLMixin(DBEngine):

    def _count_model_sql(self, model: type[Base]) -> select:
        return db.select(
            db.func.count()
        ).select_from(model)