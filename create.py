from decimal import Inexact
from sqlalchemy import create_engine, Column, Text, Integer, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import DateTime, Numeric, String

Base = declarative_base() 

class Agents(Base):
    __tablename__ = 'agents'
    id = Column(Integer, primary_key=True, index=True) #indexed for faster queries - monthly reports
    firstname = Column(Text)
    lastname = Column(Text)
    email = Column(Text)
    phone = Column(Text)

    def __repr__(self):
        return 'Agents(id={}, firstname={}, lastname={}, email={}, phone={})\n'.format(self.id, self.firstname, self.lastname, self.email, self.phone)

class Offices(Base):
    __tablename__ = 'offices'
    id = Column(Integer, primary_key=True, index=True) #indexed for faster queries - monthly reports
    name = Column(Text)

    def __repr__(self):
        return 'Offices(id={}, name={})\n'.format(self.id, self.name)

class AgentsOffices(Base):
    __tablename__ = 'agentsoffices'
    agentid = Column(Integer, ForeignKey('agents.id'), primary_key=True)
    officeid = Column(Integer, ForeignKey('offices.id'), primary_key=True)
    offices = relationship(Offices)
    agents = relationship(Agents)

    def __repr__(self):
        return 'AgentsOffices(agentid={}, officeid={})\n'.format(self.agentid, self.officeid)

# one office can be responsible for more than one area, but no are has more than one office
class OfficesZipcode(Base):
    __tablename__ = 'officeszipcode'
    zipcode = Column(Integer, primary_key=True, index=True) #indexed for faster queries - monthly reports - by zipcode
    officeid = Column(Integer, ForeignKey('offices.id'), index=True) #indexed for faster queries - monthly reports - by office
    offices = relationship(Offices)
    
    def __repr__(self):
        return 'OfficesZipcode(zipcode={}, officeid={})\n'.format(self.zipcode, self.officeid)

class Sellers(Base):
    __tablename__ = 'sellers'
    id = Column(Integer, primary_key=True)
    firstname = Column(Text)
    lastname = Column(Text)
    email = Column(Text)
    phone = Column(Text)

    def __repr__(self): 
        return 'Sellers(id={}, firstname={}, lastname={}, email={}, phone={})\n'.format(self.id, self.firstname, self.lastname, self.email, self.phone)

class Buyers(Base):
    __tablename__ = 'buyers'
    id = Column(Integer, primary_key=True)
    firstname = Column(Text)
    lastname = Column(Text)
    email = Column(Text)
    phone = Column(Text)

    def __repr__(self): 
        return 'Buyers(id={}, firstname={}, lastname={}, email={}, phone={})\n'.format(self.id, self.firstname, self.lastname, self.email, self.phone)

class Commissions(Base):
    __tablename__ = 'commissions'
    upperbound = Column(Integer, primary_key=True, index=True)
    lowerbound = Column(Integer)
    rate = Column(Numeric)

    def __repr__(self):
        return 'Commissions(upperbound={}, lowerbound={}, rate={})\n'.format(self.upperbound, self.lowerbound, self.rate)

class Listings(Base):
    __tablename__ = 'listings'
    id = Column(Integer, primary_key=True)
    zipcode = Column(Integer, ForeignKey('officeszipcode.zipcode'), index=True) #indexed for faster queries - monthly reports
    bedrooms = Column(Integer)
    bathrooms = Column(Integer)
    listingdate = Column(DateTime)
    listingmonth = Column(Integer)
    listingprice = Column(Integer)
    sellerid = Column(Integer, ForeignKey('sellers.id'))
    agentid = Column(Integer, ForeignKey('agents.id'), index=True) #indexed for faster queries - monthly reports
    status = Column(String, default='unsold')

    officeszipcode = relationship(OfficesZipcode)
    sellers = relationship(Sellers)
    agents = relationship(Agents)

    def __repr__(self):
        return '''Listings(id={}, zipcode={}, bedrooms={}, bathrooms={}, listingdate={}, 
        listingmonth={}, listingprice={}, sellerid={}, agentid={}, status={})\n'''.format(self.id, self.zipcode, 
        self.bedrooms, self.bathrooms, self.listingdate, self.listingmonth, self.listingprice, 
        self.sellerid, self.agentid, self.status)

class Sales(Base):
    __tablename__ = 'sales'
    id = Column(Integer, primary_key=True)
    listingid = Column(Integer, ForeignKey('listings.id'), index=True) #indexed for faster queries - monthly reports
    saledate = Column(DateTime)
    salemonth = Column(Integer, index=True) #indexed for faster queries - monthly reports
    saleprice = Column(Integer)
    buyerid = Column(Integer, ForeignKey('buyers.id'))
    commission = Column(Integer)

    listings = relationship(Listings)
    buyers = relationship(Buyers)
    

    def __repr__(self): 
        return '''Sales(id={}, listingid={}, saledate={}, salemonth={}, saleprice={}, 
        buyerid={}, commission={})\n'''.format(self.id, self.listingid, self.saledate, self.salemonth, 
        self.saleprice, self.buyerid, self.commission)

class AgentsCommissions(Base):
    __tablename__ = 'agentscommissions'
    id = Column(Integer, primary_key=True, autoincrement='ignore_fk')
    salemonth = Column(Integer, index=True)
    agentid = Column(Integer, ForeignKey('agents.id'))
    agentcommission = Column(Integer)

    agents = relationship(Agents)

    def __repr__(self): 
        return 'AgentsCommissions(id={}, salemonth={}, agentid={}, agentcommission={})\n'.format(self.id, self.salemonth, self.agentid, self.agentcommission)

def init_db(url='sqlite:///database.db'):
    engine = create_engine(url)
    engine.connect()
    Base.metadata.create_all(bind=engine)
    return engine

if __name__ == '__main__':
    engine = init_db()

