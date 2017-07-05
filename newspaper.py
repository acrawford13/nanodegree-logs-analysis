#! /usr/bin/env python3
# coding=utf-8

import psycopg2
import datetime

# print report of top 3 articles of all time
def popular_articles():
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    c.execute('''select articles.title,
                        count(log.id) as count
                 from articles
                 left join log on log.path = '/article/'||articles.slug
                 group by articles.title
                 order by count desc
                 limit 3;''')
    heading = "\nTop 3 articles of all time:\n"
    heading += "=" * 55
    heading += "\n"
    list_format = '%-38s|%9s visits\n'
    results = c.fetchall()
    results = "".join(list_format % (title, visits)
                      for title, visits in results)
    db.close()
    print heading + results

# print report of all authors, sorted by popularity
def popular_authors():
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    c.execute('''select authors.name,
                        count(log.id) as count
                 from authors
                 left join (articles
                            join log on log.path =
                            '/article/'||articles.slug) on
                            articles.author = authors.id
                 group by authors.name
                 order by count desc;''')
    heading = "\nAuthors, sorted by popularity:\n"
    heading += "=" * 55
    heading += "\n"
    list_format = '%-38s|%9s visits\n'
    results = c.fetchall()
    results = "".join(list_format % (title, visits)
                      for title, visits in results)
    db.close()
    print heading + results

# print report of days with error rates higher than 1%
def error_days():
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    c.execute("select date, perc from errors where perc > 1")
    heading = "\nDays with error rates higher than 1%:\n"
    heading += "=" * 55
    heading += "\n"
    list_format = "%-38s|   %5.1f%% errors\n"
    date_format = "%s %d, %d"
    results = c.fetchall()
    results = "".join(list_format %
                      (date_format % (date.strftime("%B"),
                       date.day, date.year), perc)
                      for date, perc in results)
    db.close()
    print heading + results

popular_articles()
popular_authors()
error_days()
