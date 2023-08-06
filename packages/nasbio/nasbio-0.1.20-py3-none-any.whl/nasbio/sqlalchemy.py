from datetime import datetime
from math import ceil
from typing import Any, Dict, Iterator, List, Optional, Tuple
from dataclasses import dataclass

import strawberry
from sqlalchemy import Column, DateTime, func, Integer, String, Table
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Query

from .db import create_session, engine


@dataclass(init=False)
class CreateUpdateFields:
    # Keep track when records are created and updated.
    created_at: Optional[datetime] = Column(DateTime(), index=True, default=datetime.utcnow)
    updated_at: Optional[datetime] = Column(DateTime(), index=True, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(String)
    updated_by = Column(String)


class ResourceMixin(CreateUpdateFields):
    __table__: Table

    @classmethod
    def _bulk_insert(cls, data, label: str, dtype: str = '') -> None:
        """
        Bulk insert data to the model and log it. This is much more efficient than adding 1 row at a time in a loop.

        :param data: Data to be saved
        :type data: list
        :param dtype: Data type
        :type dtype: str
        :param label: Label for the output
        :type label: str
        :return: None
        """
        engine.execute(cls.__table__.insert(), data)
        print(f'Finished inserting {len(data):,} {(dtype + " ") if dtype else ""}{label}.')

        return None


class ResourceMixinWithVersion(ResourceMixin):
    version: Optional[int] = Column(Integer, nullable=False)
    __mapper_args__ = {'version_id_col': version}


@dataclass(init=False)
class RefSeqFields:
    id: strawberry.ID = Column(String(24), primary_key=True)  # RefSeq acc version, e.g. NM_003331.5 / NP_003322.3.
    acc: str = Column(String(16), nullable=False, unique=True)


class RefseqMixin(RefSeqFields):
    @classmethod
    def find_by_refseq_id(cls, refseq_id: str):
        """Find a model by its RefSeq accession ID."""
        with create_session() as db:
            return db.query(cls).filter((cls.id == refseq_id) | (cls.acc == refseq_id.split('.')[0])).first()


class ExternalResourceMixin:
    # Keep track when records are created and updated.
    created_at = Column(DateTime(), index=True, default=datetime.utcnow)
    updated_at = Column(DateTime(), index=True, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(String)
    updated_by = Column(String)

    # @classmethod
    # def get_by_id(cls, id: Union[int, str, List[str]]):
    #     try:
    #         return cls.query.get(id)
    #     except ValueError:
    #         return None


# def sort_query(model: Any, query: Query, sort_keys: Dict[str, InstrumentedAttribute],
#                order_by: Iterator[str]) -> Query:
#     """Sort list with order_by fields, append id_ASC/id_DESC if not present."""
#     sort_list = [order.split('_') for order in order_by]
#     query = query.order_by(*[sort_keys[sort_key].desc() if sort_order == 'DESC' else sort_keys[sort_key]
#                              for (sort_key, sort_order) in sort_list if sort_key in sort_keys])
#     if not ('id_ASC' in order_by or 'id_DESC' in order_by):
#         query = query.order_by(model.id.desc() if sort_list[0][1] == 'DESC' else model.id)
#
#     return query


def sort_query(model: Any, query: Query, sort_keys: Dict[str, Any], order_by: Iterator[str]) -> Query:
    """Sort list with order_by fields, append id_ASC/id_DESC if not present."""
    sort_list = [order.split('_') for order in order_by]
    # query = query.order_by(*[sort_keys[sort_key].desc() if sort_order == 'DESC' else sort_keys[sort_key]
    #                          for (sort_key, sort_order) in sort_list if sort_key in sort_keys])
    ordering_params = []
    for sort_key, sort_order in sort_list:
        if sort_key in sort_keys:
            if sort_order == 'DESC':
                if isinstance(sort_keys[sort_key], Tuple):
                    for ordering_param in sort_keys[sort_key]:
                        ordering_params.append(ordering_param.desc())
                else:
                    ordering_params.append(sort_keys[sort_key].desc())
            else:
                if isinstance(sort_keys[sort_key], Tuple):
                    for ordering_param in sort_keys[sort_key]:
                        ordering_params.append(ordering_param)
                else:
                    ordering_params.append(sort_keys[sort_key])

    query = query.order_by(*ordering_params)
    if not ('id_ASC' in order_by or 'id_DESC' in order_by):
        query = query.order_by(model.id.desc() if sort_list[0][1] == 'DESC' else model.id)

    return query


class Pagination(object):
    def __init__(self, items: List[Any], page: int, per_page: int, total: int):
        self.page = page
        self.items = items
        self.prev_page = None
        self.next_page = None
        self.has_prev = page > 1
        if self.has_prev:
            self.prev_page = page - 1
        previous_items = (page - 1) * per_page
        self.has_next = previous_items + len(items) < total
        if self.has_next:
            self.next_page = page + 1
        self.total = total
        self.pages = int(ceil(total / float(per_page)))


def paginate(query: Query, page: int, per_page: int):
    if page <= 0:
        raise AttributeError('page needs to be >= 1')
    if per_page <= 0:
        raise AttributeError('per_page needs to be >= 1')
    if per_page > 100:
        raise AttributeError('per_page needs to be <= 100')

    items = query.limit(per_page).offset((page - 1) * per_page).all()
    total = query.order_by(None).count()
    # total = session.execute(query.statement.with_only_columns([func.count()]).order_by(None)).scalar()

    return Pagination(items, page, per_page, total)


async def async_paginate(session: AsyncSession, query: Query, page: int, per_page: int):
    if page <= 0:
        raise AttributeError('page must be >= 1')
    if per_page <= 0:
        raise AttributeError('per_page must be >= 1')
    if per_page > 100:
        raise AttributeError('per_page needs to be <= 100')

    paginated_query = query.limit(per_page).offset((page - 1) * per_page)
    result = await session.execute(paginated_query)

    items = result.scalars().all()
    total_result = await session.execute(select(func.count()).select_from(query))
    total = total_result.scalar_one()

    return Pagination(items, page, per_page, total)
