from datetime import datetime
from create import Agents, AgentsCommissions, Listings, Offices, AgentsOffices, OfficesZipcode, Sellers, Buyers, Commissions, Listings, Sales
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func, desc
from create import init_db
from insert_data import addAgentsCommission

engine = init_db()
Session = sessionmaker(bind=engine)
session = Session()

def monthly_report(salemonth):
    # Find the top 5 offices with the most sales for that month.
    q = session.query(Offices.name,Offices.id,func.sum(Sales.saleprice).label('total')).join(Sales.listings
                            ).join(Listings.officeszipcode).join(OfficesZipcode.offices
                            ).filter(Sales.salemonth==salemonth
                            ).group_by(Offices.id).order_by(desc('total')).limit(5).all()

    print('''\n
        Top 5 offices with the most sales
        -------------------''')
    print(q)

    # Find the top 5 estate agents who have sold the most (include their contact details and their sales details
    q = session.query(Agents.firstname,Agents.lastname,Agents.email,Agents.phone,func.sum(Sales.saleprice).label('totalsales')
                            ).join(Sales.listings).join(Listings.agents).filter(Sales.salemonth==salemonth
                            ).group_by(Agents.id).order_by(desc('totalsales')).limit(5).all()

    print('''\n
        Top 5 estate agents who have sold the most
        -------------------''')
    print(q)

    # Calculate the commission that each estate agent must receive and store the results in a separate table.
    q = session.query(Agents.id,func.sum(Sales.commission)).join(Sales.listings).join(Listings.agents
                            ).filter(Sales.salemonth==salemonth).group_by(Agents.id).all()

    print('''\n
        The commission for agents for a month
        -------------------''')
    print(q)

    # add the monthly commissions to AgentsCommission
    for i in range(len(q)):
        addAgentsCommission(salemonth=salemonth, agentid=q[i][0], agentcommission=q[i][1])

    # need to check if the Agents table has been updated
    print('''\n
        AgentsCommissions Table
        -------------------''')
    print(session.query(AgentsCommissions).all())

    # For all houses that were sold that month, calculate the average number of days
    # that a house was on the market.
    s = session.query(Sales.saledate).join(Sales.listings
                            ).filter(Sales.salemonth==salemonth).all()
    l = session.query(Listings.listingdate).join(Sales.listings
                            ).filter(Sales.salemonth==salemonth).all()
    avg = 0
    for i in range(len(s)):
        avg += (s[i][0]-l[i][0]).days/len(l)

    print('''\n
        The average number of days that a house was on the market
        -------------------''')
    print(round(avg), ' days')

    # For all houses that were sold that month, calculate the average selling price
    q = round(session.query(func.avg(Sales.saleprice)).filter(Sales.salemonth==salemonth).first()[0])
    print('''\n
        The average selling price
        -------------------''')
    print(q, ' USD')

    # Find the zip codes with the top 5 average sales prices
    q = session.query(Listings.zipcode, func.avg(Sales.saleprice).label('avgprice')).join(Sales.listings
                            ).filter(Sales.salemonth==salemonth).group_by(Listings.zipcode
                            ).order_by(desc('avgprice')).limit(5).all()
    print('''\n
        The zip codes with the top 5 average sales prices
        -------------------''')
    print(q)

monthly_report(202105)

