from create import Agents, AgentsCommissions, Offices, AgentsOffices, OfficesZipcode, Sellers, Buyers, Commissions, Listings, Sales
from create import init_db
from sqlalchemy.orm import sessionmaker
from datetime import datetime

engine = init_db()
Session = sessionmaker(bind=engine)
session = Session()

def addAgent(id, firstname, lastname, email, phone):
    if session.query(Agents).filter(Agents.id==id).count() == 0:
        session.add(Agents(id=id, firstname=firstname, lastname=lastname, email=email, phone=phone))
        session.commit()

def addOffice(id, name):
    if session.query(Offices).filter(Offices.id==id).count() == 0:
        session.add(Offices(id=id, name=name))
        session.commit()

# no more than one office in one location (i.e. no two offices with same zipcode)
def addOfficesZipcode(zipcode, officeid):
    if session.query(OfficesZipcode).filter(OfficesZipcode.zipcode==zipcode).count() == 0:
        session.add(OfficesZipcode(zipcode=zipcode, officeid=officeid))
        session.commit()

def addSeller(id, firstname, lastname, email, phone):
    if session.query(Sellers).filter(Sellers.id==id).count() == 0:
        session.add(Sellers(id=id, firstname=firstname, lastname=lastname, email=email, phone=phone))
        session.commit()

def addBuyer(id, firstname, lastname, email, phone):
    if session.query(Buyers).filter(Buyers.id==id).count() == 0:
        session.add(Buyers(id=id, firstname=firstname, lastname=lastname, email=email, phone=phone))
        session.commit()

def addCommission(upperbound, lowerbound, rate):
    if session.query(Commissions).filter(Commissions.upperbound==upperbound).count() == 0:
        session.add(Commissions(upperbound=upperbound, lowerbound=lowerbound, rate=rate))
        session.commit()

def addListing(id, zipcode, bedrooms, bathrooms, listingdate, listingmonth, listingprice, sellerid, agentid, status='unsold'):
    if session.query(Listings).filter(Listings.id==id).count() == 0:
        session.add(Listings(id=id, zipcode=zipcode, bedrooms=bedrooms, bathrooms=bathrooms, listingdate=listingdate, listingmonth=listingmonth, 
    listingprice=listingprice, sellerid=sellerid, agentid=agentid, status=status))
        officeid = session.query(OfficesZipcode.officeid).filter(OfficesZipcode.zipcode==zipcode).first()[0]
        res = session.query(AgentsOffices.agentid).filter(AgentsOffices.officeid == officeid, AgentsOffices.agentid==agentid).all()
        if res == []:
            session.add(AgentsOffices(agentid=agentid, officeid=officeid))
        session.commit()

def addSales(id, listingid, saledate, salemonth, saleprice, buyerid):
    if session.query(Sales).filter(Sales.id==id).count() == 0:
        session.add(Sales(id=id, listingid=listingid, saledate=saledate, salemonth=salemonth, saleprice=saleprice, buyerid=buyerid))
        session.query(Listings).filter(Listings.id==listingid).update({'status':'sold'})
        rate = session.query(Commissions.rate).filter(saleprice >= Commissions.lowerbound,saleprice <= Commissions.upperbound).first()[0]
        output = round(saleprice*rate/100)
        agentid = session.query(Listings.agentid).filter(Listings.id==listingid).first()[0]
        # updated = session.query(Agents.totalcommission).filter(Agents.id==agentid).first()[0] + commission
        session.query(Sales).filter(Sales.id==id).update({'commission': output})
        session.commit()

def addAgentsCommission(salemonth, agentid, agentcommission):
    if session.query(AgentsCommissions).join(Agents).filter(AgentsCommissions.salemonth==salemonth).filter(Agents.id==agentid).count() == 0:
        session.add(AgentsCommissions(salemonth=salemonth, agentid=agentid, agentcommission=agentcommission))
        session.commit()

# add agents
addAgent(1001, 'John', 'Kim', 'johnkim@jira.com', '510-999-111')
addAgent(1002, 'Kerry', 'Jin', 'kerry@bts.com', '11-998-001')
addAgent(1003, 'Kaly', 'Bill', 'kally@lm.mn', '876-987-0989')
addAgent(1004, 'Lily', 'Ben', 'lily@ben.com', '123-456-7898')
addAgent(1005, 'Cindy', 'Ken', 'cindy@gmail.com', '982-2983-292')
addAgent(1006, 'Robbin', 'Clark', 'robbin@gmail.com', '981-1092-091')

# add offices
addOffice(2001, 'San Francisco')
addOffice(2002, 'Berkeley')
addOffice(2003, 'Boston')
addOffice(2004, 'Seattle')
addOffice(2005, 'Los Angeles')
addOffice(2006, 'Pennsylvania')
addOffice(2007, 'New York')

# add zipcodes and respective offices
addOfficesZipcode(94102, 2001)
addOfficesZipcode(94107, 2001)
addOfficesZipcode(94708, 2002)
addOfficesZipcode(94710, 2002)
addOfficesZipcode(94709, 2002)
addOfficesZipcode(2110, 2003)
addOfficesZipcode(2101, 2003)
addOfficesZipcode(98113, 2004)
addOfficesZipcode(98107, 2004)
addOfficesZipcode(90009, 2005)
addOfficesZipcode(90018, 2005)
addOfficesZipcode(15042, 2006)
addOfficesZipcode(15045, 2006)
addOfficesZipcode(10008, 2007)
addOfficesZipcode(10010, 2007)
addOfficesZipcode(10017, 2007)

# add commissions
addCommission(100000, 0, 10)
addCommission(200000, 100001, 7.5)
addCommission(500000, 200001, 6)
addCommission(1000000, 500001, 5)
addCommission(10000000000000, 1000001, 4)

# add sellers
addSeller(3001, 'Ben', 'Nelson', 'ben@minervaproject.com', '908-891-091')
addSeller(3002, 'Tuan', 'Tran', 'tuan@amazingly.com', '092-098-908')
addSeller(3003, 'Precious', 'Okeke', 'precious@amazingly.com', '192-098-908')
addSeller(3004, 'Jasu', 'Zaya', 'jasu@amazingly.com', '792-098-908')
addSeller(3005, 'Bilguun', 'Munkh', 'bilguun@amazingly.com', '092-098-500')
addSeller(3006, 'Zoloo', 'Zulaa', 'zoloo@amazingly.com', '092-228-908')
addSeller(3007, 'Kelly', 'Clarkson', 'kelly@amazingly.com', '111-098-908')
addSeller(3008, 'Justin', 'Bieber', 'justin@amazingly.com', '092-999-908')

# # add listings
addListing(5001, 94102, 3, 2, datetime(2019,1,2), 201901, 190000, 3001, 1001)
addListing(5002, 10017, 5, 2, datetime(2020,3,5), 202003, 285000, 3002, 1004)
addListing(5003, 90018, 6, 4, datetime(2020,6,15), 202006, 1285000, 3003, 1006)
addListing(5004, 10010, 4, 2, datetime(2020,2,2), 202002, 200000, 3004, 1003)
addListing(5005, 98113, 9, 4, datetime(2020,10,5), 202010, 2100000, 3005, 1005)
addListing(5006, 15042, 5, 4, datetime(2020,9,6), 202009, 300000, 3006, 1003)
addListing(5007, 90009, 6, 4, datetime(2020,12,1), 202012, 450000, 3006, 1002)
addListing(5008, 2110, 4, 2, datetime(2020,12,21), 202012, 200000, 3007, 1004)
addListing(5009, 15045, 8, 6, datetime(2021,1,7), 202101, 550000, 3008, 1001)

# need to check if the AgentsOffices tables has been updated
print('''\n
    AgentsOffices Table
    -------------------''')
print(session.query(AgentsOffices).all())

# add buyers
addBuyer(4001, 'Kim', 'Seokjin', 'Jin@bts.com', '10-982-092-209')
addBuyer(4002, 'Park', 'Jimin', 'jimin@bts.com', '092-390-092')
addBuyer(4003, 'Gigi', 'Okeke', 'gigi@create.com', '111-11-111')
addBuyer(4004, 'Gumi', 'George', 'gumi@george.com', '992-390-092')
addBuyer(4005, 'Kim', 'Namjoon', 'rm@bts.com', '10-999-092-209')
addBuyer(4006, 'Park', 'Bogum', 'bogum@btsfan.com', '10-000-092-209')
addBuyer(4007, 'Min', 'Yoongi', 'suga@bts.com', '10-888-092-209')

# add sales
addSales(6001, 5001, datetime(2021,5,8), 202105, 186000, 4002)
addSales(6002, 5002, datetime(2021,4,1), 202104, 270000, 4001)
addSales(6003, 5003, datetime(2021,5,9), 202105, 1100000, 4007)
addSales(6004, 5004, datetime(2021,5,4), 202105, 210000, 4004)
addSales(6005, 5009, datetime(2021,5,1), 202105, 530000, 4005)
addSales(6006, 5008, datetime(2021,5,12), 202105, 195000, 4002)
addSales(6007, 5007, datetime(2021,5,10), 202105, 450000, 4006)
addSales(6008, 5005, datetime(2021,5,20), 202105, 2100000, 4003)

# need to check if the Listings table has been updated
print('''\n
    Listings Table
    -------------------''')
print(session.query(Listings).all())

# need to check if the Agents table has been updated
print('''\n
    Sales Table
    -------------------''')
print(session.query(Sales).all())

