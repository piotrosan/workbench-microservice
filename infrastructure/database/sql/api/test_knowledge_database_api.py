import logging
from typing import Iterable, List, cast, Generator, Iterator, Dict, Tuple

from sqlalchemy.engine.result import Result
from sqlalchemy.orm import joinedload, Session
from typing_extensions import Any

from sqlalchemy import select, text, and_
from sqlalchemy import exc

from infrastructure.database.sql.api.analytics import AnalyticsSQLMixin
from infrastructure.database.sql.api.engine import DBEngine, DBEngineAbstract
from infrastructure.database.sql.models import Language, TestKnowledge
from infrastructure.database.sql.models.initiative import TestKnowledge, \
    AssociationKnowledgeFlashCard
from infrastructure.database.sql.models.task import FlashCard
from infrastructure.database.sql.api.exception.test_knowledge_exception import TestKnowledgeHttpException
from infrastructure.routers.models.request.knowledge import \
    CreateKnowledgeRequest

logger = logging.getLogger("root")


class CreateTestKnowledgeDBAPIMixin(DBEngineAbstract):

    def insert(
            self,
            test_knowledge_data: CreateKnowledgeRequest,
            list_flash_cards: List[Tuple[FlashCard]]
    ) -> TestKnowledge | None:

        session: Session = self.get_session()
        try:
            test_knowledge = TestKnowledge(
                planned_start=test_knowledge_data.planned_start,
                user_identifier=test_knowledge_data.user_identifier
            )
            session.add(test_knowledge)

            asso = [
                AssociationKnowledgeFlashCard(
                    test_knowledge=test_knowledge,
                    flash_card=flsh[0]
                )
                for flsh in list_flash_cards
            ]
            session.add_all(asso)
        except exc.SQLAlchemyError as e:
            session.rollback()
            logger.critical(
                f"Problem wile insert test "
                f"knowledge {test_knowledge_data} -> {e}"
            )
            raise TestKnowledgeHttpException(
                detail="Can not insert test knowledge",
                status_code=400
            )
        else:
            session.commit()
            return test_knowledge


class GetTestKnowledgeDBAPIMixin(DBEngineAbstract):

    def _select_all_test_knowledge_sql(
            self,
            column: List[str] = None,
            order: List[str] = None
    ):
        tmp_select = select(TestKnowledge)

        if column:
            tmp_select.column(*[text(col) for col in column])

        if order:
            tmp_select.order_by(*[text(col) for col in order])

        return tmp_select

    def _select_test_knowledge_from_id_sql(
            self,
            id_test_knowledge: int
    ):
        try:
            return select(TestKnowledge).where(
                cast(
                    "ColumnElement[bool]",
                    TestKnowledge.id == id_test_knowledge
                )
            )
        except exc.SQLAlchemyError as e:
            logger.critical(
                f"Problem wile select flash card from id {e}")
            raise TestKnowledgeHttpException(
                detail="Can not create select test knowledge",
                status_code=400
            )

    def _select_test_knowledge_from_id_and_user_sql(
            self,
            id_test_knowledge: int,
            user_identifier: str
    ):
        try:
            return select(TestKnowledge).where(
                and_(
                    cast(
                        "ColumnElement[bool]",
                        TestKnowledge.user_identifier == user_identifier
                    ),
                )
            )
        except exc.SQLAlchemyError as e:
            logger.critical(
                f"Problem wile select flash card from id {e}")
            raise TestKnowledgeHttpException(
                detail="Can not create select test knowledge",
                status_code=400
            )

    def _slct_tst_know_flsh_crd_from_user_sql(
            self,
            id_test_knowledge: int,
            user_identifier: str
    ):
        try:
            return (
                select(TestKnowledge)
                .join_from(
                    TestKnowledge,
                    FlashCard,
                    TestKnowledge.flash_cards.any(
                        and_(
                            TestKnowledge.id == AssociationKnowledgeFlashCard.test_knowledge_id,
                            FlashCard.id == AssociationKnowledgeFlashCard.flash_card_id,
                            TestKnowledge.user_identifier == user_identifier
                        )
                    )
                )
                .join_from(
                    FlashCard,
                    Language,
                    FlashCard.language.any(
                        and_(FlashCard.language_id == Language.id)
                    )
                )
                .where(
                    cast(
                        "ColumnElement[bool]",
                        TestKnowledge.user_identifier == user_identifier
                    ),
                    cast(
                        "ColumnElement[bool]",
                        TestKnowledge.id == id_test_knowledge
                    ),
                )
                .options(
                    joinedload(TestKnowledge.flash_cards)
                    .joinedload(FlashCard.language)
                )
            )
        except exc.SQLAlchemyError as e:
            logger.critical(
                f"Problem wile select flash card from id {e}")
            raise TestKnowledgeHttpException(
                detail="Can not create select test knowledge",
                status_code=400
            )

    def _slct_tst_know_with_for_user_sql(
            self,
            hash_identifier: str
    ):
        try:
            return (
                select(TestKnowledge)
                .where(
                    and_(
                        cast(
                            "ColumnElement[bool]",
                            TestKnowledge.hash_identifier == hash_identifier
                        ),
                    )
                )
            )
        except exc.SQLAlchemyError as e:
            logger.critical(
                f"Problem wile select test knowledge for user {hash_identifier},  {e}")
            raise TestKnowledgeHttpException(
                detail="Can not select select test knowledge",
                status_code=400
            )

    def query_all_tests_knowledge_generator(
            self,
            column: List[str] = None,
            order: List[str] = None
    ) -> Iterator[Any]:
        try:
            return self.query_statement(
                self._select_all_test_knowledge_sql(column, order)
            )
        except exc.SQLAlchemyError as e:
            logger.critical("Problem wile select all test knowledge")
            raise TestKnowledgeHttpException(
                detail="Can not select test knowledge",
                status_code=400
            )

    def query_all_test_knowledge_paginate_generator(
            self,
            column: List[str] = None,
            order: List[str] = None,
            page: int = None
    ) -> Iterator[Any]:
        try:
            return self.query_statement(
                self._select_all_test_knowledge_sql(column, order),
                page=page
            )
        except exc.SQLAlchemyError as e:
            logger.critical("Problem wile select all test knowledge")
            raise TestKnowledgeHttpException(
                detail="Can not select test knowledge",
                status_code=400
            )

    def qet_tsts_know_for_user(
            self,
            page_id: int,
            hash_identifier: str,
    ) -> Iterator[Any]:
        return self.query_statement(
            self._slct_tst_know_with_for_user_sql(
                hash_identifier
            ),
            TestKnowledge,
            page=page_id
        )

    def query_test_knowledge_from_id(
            self,
            id_knowledge: int
    ) -> TestKnowledge:
        try:
            result: Result =  next(self.query_statement(
                self._select_test_knowledge_from_id_sql(id_knowledge)
            ))
            return result.scalar()
        except exc.SQLAlchemyError as e:
            logger.critical(
                f"Problem wile select test knowledge {id_knowledge} -> {e}"
            )
            raise TestKnowledgeHttpException(
                detail=f"Can not select test knowledge {id_knowledge}",
                status_code=400
            )

    def query_test_for_user(
            self,
            id_knowledge: int,
            hash_identifier: str
    ) -> Iterator[Any]:
        try:
            return self.query_statement(
                self._select_test_knowledge_from_id_and_user_sql(
                    id_knowledge,
                    hash_identifier
                )
            )
        except exc.SQLAlchemyError as e:
            logger.critical(
                f"Problem wile select test knowledge {id_knowledge} -> {e}"
            )
            raise TestKnowledgeHttpException(
                detail=f"Can not select test knowledge {id_knowledge}",
                status_code=400
            )


    def get_tsts_with_cards_for_user(
            self,
            hash_identifier: str,
            id_test_knowledge: int,
    ) -> Iterator[Any]:
        try:
            return self.query_statement(
                self._slct_tst_know_flsh_crd_from_user_sql(
                    id_test_knowledge,
                    hash_identifier
                ),
            )
        except exc.SQLAlchemyError as e:
            logger.critical(
                f"Problem wile select tests knowledge "
                f"for user {hash_identifier} -> {e}"
            )
            raise TestKnowledgeHttpException(
                detail=f"Can not select tests knowledge "
                       f"for user {hash_identifier}",
                status_code=400
            )


class UpdateKnowledgeDBAPIMixin(DBEngineAbstract):

    def update_test(
        self,
        test_data: Dict[str, int | str],
    ) -> bool:
        try:
            return self.update_object(TestKnowledge, [test_data])
        except exc.SQLAlchemyError as e:
            logger.critical(
                f"Problem wile update Test Knowledge "
                f" -> {e}"
            )
            raise TestKnowledgeHttpException(
                detail=f"Can not update tests knowledge ",
                status_code=400
            )



class TestKnowledgeDBAPI(
    CreateTestKnowledgeDBAPIMixin,
    GetTestKnowledgeDBAPIMixin,
    UpdateKnowledgeDBAPIMixin,
    AnalyticsSQLMixin,
    DBEngine
):

    def get_count_test_knowledge(self):
        try:
            return next(
                self.query_statement(
                    self._count_model_sql(TestKnowledge)
                )
            ).first()
        except exc.SQLAlchemyError as e:
            logger.critical(
                f"Problem with count model {TestKnowledge} -> {e}"
            )
            raise TestKnowledgeHttpException(
                detail=f"Can not count model {TestKnowledge}",
                status_code=400
            )