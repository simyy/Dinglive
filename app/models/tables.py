#!/usr/bin/env python
# encoding: utf-8

from sqlalchemy import Column, String, Integer, VARCHAR,ForeignKey, Float
from sqlalchemy.orm import relationship,backref
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Student(Base):

    __tablename__ = 'student'

    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(32))
    age = Column(Integer)


class TV(Base):
 
    __tablename__ = 'tv'

    id = Column(Integer, primary_key=True)
    anchor = Column(VARCHAR(32))
    avatar = Column(VARCHAR(256))
    room_id = Column(VARCHAR(128))
    room_name = Column(VARCHAR(128))
    room_site = Column(VARCHAR(1024))
    update_time = Column(DateTime)
    is_online = Column(Integer)
    fans_count = Column(Integer)
    audience_count = Column(Integer)
    category_id = Column(Integer)
    source_id = Column(Integer)

    @classmethod
    def new(cls, **kwargs):
        return cls(
            anchor=kwargs['anchor'],
            room_id=kwargs['room_id'],
            room_name=kwargs['room_name'],
            room_site=kwargs['room_site'],
            update_time=kwargs['update_time'],
            is_online=kwargs['is_online'],
            fans_count=kwargs['fans_count'],
            audience_count=kwargs['audience_count'],
            category_id=kwargs['category_id']
            source_id=kwargs['source_id'])
 

class TVCtg(Base)

    __tablename__ = 'tv_category'

    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(32))
    pic = Column(VARCHAR(256))
    count = Column(Integer)


class TVSrc(Base):

    __tablename__ = 'tv_source'

    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(32))
    pic = Column(VARCHAR(256))
    url = Column(VARCHAR(1024))
    count = Column(Integer)
