# Newspaper Report

Before running the `error_days` report, you will need to create an **errors view**, by copying and pasting the code below. This will create a table with the following columns:


| Column Name | Data | Type |
|--------|------|------|
| date        | date | date |
| errors      | total number of errors that day | bigint |
| totalvisits | total number of requests that day | bigint |
| perc        | percentage of requests that lead to errors   | numeric |

### Example data

| date                  | errors | requests | perc |
|-----------------------|--------|-------------|------|
|2016-07-01 |    274 |       38705 | 0.70 |
|2016-07-02 |    389 |       55200 | 0.70 |
|2016-07-03 |    401 |       54866 | 0.73 |
|2016-07-04 |    380 |       54903 | 0.69 |
|2016-07-05  |    423 |       54585 | 0.77 |


    create view errors as
    select a.date::date,
       b.count as errors,
       a.count as requests,
       trunc((b.count::numeric/a.count) * 100, 2) as perc
    from
    (select date_trunc('day', time) as date,
          count(id) as count
    from log
    group by date) as a
    left join
    (select date_trunc('day', time) as date,
          count(id) as count
    from log
    where status!='200 OK'
    group by date) as b on a.date=b.date
    order by a.date;

h
