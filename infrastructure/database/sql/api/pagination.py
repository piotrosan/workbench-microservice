from settings import PAGINATION_PER_PAGE
from sqlalchemy import and_, or_, Select
from typing import cast

class Pagination:

    def __init__(self, select, model):
        self.offset = PAGINATION_PER_PAGE
        self.select = select
        self.model = model

    def get_page(self, page: int) -> Select:
        page = page - 1
        start = self.offset * page
        end  = start + self.offset
        return self.select.where(
            and_(
                cast(
                    "ColumnElement[bool]",
                    self.model.id >= start
                ),
                cast(
                    "ColumnElement[bool]",
                    self.model.id < end
                )
            )
        )
