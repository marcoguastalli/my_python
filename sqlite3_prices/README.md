# SQLite3
Create the SQLite table PRICES adding a couple of TEST rows.

Run this script to create a fresh 'prices.sqlite' DDBB file.

# inspiring links
https://docs.python.org/3.10/library/sqlite3.html
https://www.sqlitetutorial.net/sqlite-python/create-tables/
https://likegeeks.com/es/tutorial-de-python-sqlite3/

### dependencies to install
sqlite3

# build
cd ~/dev/repository/git/my_python/sqlite3_prices

# run
python3 sqlite3_prices.py

# SQL
* delete from prices
* select * from prices order by instrument, created DESC
* select * from prices 
   where source='CDC' 
    and instrument = 'CRO_USDT'
  order by instrument, created DESC
