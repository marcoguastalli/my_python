# SQLite3 Tables
Create the SQLite tables

Run this script to create a fresh DDBB files

# inspiring links
https://docs.python.org/3.10/library/sqlite3.html
https://www.sqlitetutorial.net/sqlite-python/create-tables/
https://likegeeks.com/es/tutorial-de-python-sqlite3/

### dependencies to install
sqlite3

# build
cd ~/dev/repository/git/my_python/sqlite3_tables

# run
python3 sqlite3_prices.py

# SQL
### prices.sqlite
* CREATE TABLE IF NOT EXISTS prices (
                           id INTEGER PRIMARY KEY,
                           source TEXT NOT NULL,
                           instrument TEXT NOT NULL,
                           amount REAL NOT NULL DEFAULT 0,
                           created TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
* delete from prices
-- return all the records
select * from prices
-- return all the records ordered
 select id,
        source,
        instrument,
        amount,
        created
    from prices 
  order by source, instrument, created ASC
-- return all the records for a specific source and instrument
 select id,
        source,
        instrument,
        amount,
        created
    from prices 
   where source='CDC'
     and instrument = '1INCH_USDT'
   order by source, instrument, created ASC
-- return the number of records group by source, instrument
  select source,
         instrument,
         count(*)
    from prices 
   group by source, instrument
   order by instrument, created DESC
--