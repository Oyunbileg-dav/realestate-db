# Retail estate database application
#### Oyunbileg Davaanyam

# Instructions to run

Run the following to install all required packages:

`python3 -m venv venv`

`source venv/bin/activate`

`pip3 install -r requirements.txt`

## Declare models and create the database

Run the following to declare models and create the database, a sqlite file 'database.db' in the same directory:

`python3 create.py`

Models created: Agents, Offices, AgentsOffices, OfficesZipcode, Listings, Sellers, Buyers, Sales, AgentsCommissions

## Insert data

Run the following to insert dummy data to test the database application:

`python3 insert_data.py`

Two scenarios requiring insertion/updating of data have been coded:
- When a new house is listed
- When a house is sold

## Querying the data

Run the following to query the database:
`python3 query_data.py`

The queries print results corresponding to the following for the month of May 2021:

- top 5 offices with the most sales
- top 5 estate agents who have sold the most
- commission that each estate agent must receive
- average number of days that a sold house was on the market
- average selling price of sold houses
- zip codes with the top 5 average sales prices

These queries can be used to generate monthly results by calling the monthly_report() function with a specific month as an integer input. (the format: May 2021 => 202105)

# Data normalization

Most tables are in the third normalized form which made it a bit complex for queries as seen in `query_data.py`. Nevertheless, it prevents database anomalies when things are modified. Some applications of data normalization are in cross-tables such as `agentsoffices` and `officeszipcode` (as an office can be responsible for multiple zipcodes). These cross tables define the many-to-many relationship between agents and offices and many-to-one relationship between zipcodes and offices. Doing so, we can avoid repetition in the database.

# Indexing

Multiple columns in tables have been indexed for faster queries. For example, `salemonth` in the `Sales` table has been indexed. This will speed up the generation of monthly reports significantly as the database scales. Monthly reports are largely concerned with houses sold in a particular month, so all queries filter by `Sales.salemonth`. Indexing reduces the lookup time for rows with the desired salemonth with the use of dictionary key-value pairs.

# Transactions

In `insert_data.py`, transactions have been used to illustrate the insertion of data when a house is listed, and when a house is sold. Transactions are helpful because they prevent database anomalies in the case of a an interrupted transaction. The transactions are done with specifically defined functions `addSales` and `addListing` which ensures reliable transaction by updating relevant information when a house is listed or sold. 