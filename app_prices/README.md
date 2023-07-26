# Prices App
Connect to API and insert into 'prices.sqlite'

### dependencies to install
colorama

### play
cd ~/dev/repository/gitpy/my_python/app_prices
python3 app_prices.py

##### pm2
pm2 start app_prices.py  --interpreter python3
pm2 start app_prices_in_one_script.py  --interpreter python3
pm2 restart app_prices.py  --interpreter python3
pm2 stop app_prices  --interpreter python3
pm2 logs app_prices  --interpreter python3
pm2 monit
pm2 flush
pm2 delete all

# SQL
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
   order by created ASC
-- return the number of records group by source, instrument
  select source,
         instrument,
         count(*)
    from prices 
   group by source, instrument
   order by instrument, created DESC
-- return records for variation calculation
SELECT amount, source, instrument, created from prices order by source, instrument, created ASC
-- select all variation
select * from variation order by created asc
-- select WARN variation
select * 
  from variation 
 where variation >= 1
    or variation <= -1
 order by created asc
-- select TOP PERFORMERS variation
select * 
  from variation 
 where variation >= 1
 order by variation DESC