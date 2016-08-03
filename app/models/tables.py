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


class TVRoom(Base):
 
    __tablename__ = 'tvroom'

    id = Column(Integer, primary_key=True)
    room_id = Column(Integer)
    title = Column(VARCHAR(128))
    name = Column(VARCHAR(128))
    avatar = Column(VARCHAR(128))
    gender = Column(Integer)
    url = Column(VARCHAR(1024))
    pic = Column(VARCHAR(128))
    count = Column(Integer)
    ctg_id = Column(Integer)
    src_id = Column(Integer)
 

class TVCtg(Base)

    __tablename__ = 'tvctg'

    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(128))
    pic = Column(VARCHAR(128))


class TVSrc(Base):

    __tablename__ = 'tvsrc'

    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(128))
    pic = Column(VARCHAR(128))
    url = Column(VARCHAR(1024))
