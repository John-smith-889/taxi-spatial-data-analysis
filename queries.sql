-----------------------------------------------------------------------------------------
-- In which day of the week the most quantity of taxi rides han beed reported in 2014? --
-----------------------------------------------------------------------------------------

SELECT FORMAT_DATE('%A', DATE(pickup_datetime)) as DAY, count(*) as COUNT
FROM `bigquery-public-data.new_york_taxi_trips.tlc_green_trips_2014`
group by DAY
order by count(*) desc

----------------------------------------------------------------------
-- Describe cash vs card payment methods changes over time in 2014. --
----------------------------------------------------------------------

-- card - total quantity of payments
SELECT FORMAT_DATE('%B', DATE(pickup_datetime)) as MONTH, count(*) as COUNT
FROM `bigquery-public-data.new_york_taxi_trips.tlc_green_trips_2014`
where payment_type=1
group by MONTH
order by MONTH='December', MONTH='November', MONTH='October',MONTH='September',
MONTH='August', MONTH='July', MONTH='June', MONTH='May',MONTH='April', 
MONTH='March', MONTH='February',MONTH='January'

-- card - sum of payments
SELECT FORMAT_DATE('%B', DATE(pickup_datetime)) as MONTH, cast(round(sum(ifnull(total_amount,0)), 0) as numeric) as SUM
FROM `bigquery-public-data.new_york_taxi_trips.tlc_green_trips_2014`
where payment_type=1
group by MONTH
order by MONTH='December', MONTH='November', MONTH='October',MONTH='September',
MONTH='August', MONTH='July', MONTH='June', MONTH='May',MONTH='April', 
MONTH='March', MONTH='February',MONTH='January'