#!/usr/bin/env python
# encoding: utf-8

from sqlalchemy import Column, String, Integer, VARCHAR,ForeignKey, Float
from sqlalchemy.orm import relationship,backref
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Student(Base):

    __tablename__ = 'student'

    id = Column(Integer, primary_key = True)
    name = Column(VARCHAR(32))
    age = Column(Integer)
