# Newspaper Report

This code is for generating reports based on the data in an existing database (`news`), containing three tables (`articles`, `authors` and `log`) and one additional view (`errors` - see below for more info on creating this view).

It contains three functions:
* `popular_articles()` - lists top 3 articles of all time along with total number of visits
* `popular_authors()` - lists authors by popularity along with total number of visits to their published articles
* `error_days()` - lists days on which the percentage of requests resulting in errors was higher than 1%

## Generating the reports:
By default, all three reports will be generated when you run `newspaper.py`.

You can change the output by commenting out unwanted function calls in lines 69 - 71 of `newspaper.py`

### Important:

Before running the `error_days` report, you will need to create an **errors view**, by copying and pasting the code below:

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

## License
This project is licensed under the terms of the [MIT license](https://opensource.org/licenses/MIT).
