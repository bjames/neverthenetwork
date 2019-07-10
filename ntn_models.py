from sqlalchemy import Column, String, CHAR, Integer
from ntn_db import Base

class OUI_MAL(Base):
    __tablename__ = "OUI_MAL"

    '''
        MA-L large or traditional sized OUIs are 24-bits in length
    '''

    id = Column(Integer, primary_key=True)
    assignment = Column(CHAR(6))
    organization = Column(String)
    organization_address = Column(String)

    def __init__(self, assignment = None, organization = None, organization_address = None):

        self.assignment = assignment
        self.organization = organization
        self.organization_address = organization_address


class OUI_MAM(Base):
    __tablename__ = "OUI_MAM"

    '''
        MA-M (medium) 28-bit prefix in length
    '''

    id = Column(Integer, primary_key=True)
    assignment = Column(CHAR(7))
    organization = Column(String)
    organization_address = Column(String)

    def __init__(self, assignment = None, organization = None, organization_address = None):

        self.assignment = assignment
        self.organization = organization
        self.organization_address = organization_address


class OUI_MAS(Base):
    __tablename__ = "OUI_MAS"

    '''
        MA-S (small) 36-bit prefix
    '''

    id = Column(Integer, primary_key=True)
    assignment = Column(CHAR(8))
    organization = Column(String)
    organization_address = Column(String)

    def __init__(self, assignment = None, organization = None, organization_address = None):

        self.assignment = assignment
        self.organization = organization
        self.organization_address = organization_address