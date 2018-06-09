#!/usr/bin/env python3
# An internal reporting tool that will use information from the database
# to discover what kind of articles the site's readers like.

import psycopg2

dbName = "news"

file = open('answers.txt', 'w')

print('---Logs analysis---\n')
file.write('---Logs analysis---\n')

# What are the most popular three articles of all time?
db = psycopg2.connect(dbname=dbName)

query = "select title, count(*) as views from (select title, concat('/article/',slug) as path from articles) as articles_path, log where articles_path.path=log.path group by title order by views desc;"

db = psycopg2.connect(dbname=dbName)
c = db.cursor()
c.execute(query)
popular_articles = c.fetchall()
db.close()
print('\n')
file.write('\n')
print('* The most popular three articles of all time:\n')
file.write('* The most popular three articles of all time:\n')
for articles in popular_articles[:3]:
    print('\"' + articles[0] + '\"' + ' -- ' +
          str(articles[1]) + ' views\n')
    file.write('\"' + articles[0] + '\"' + ' -- ' +
               str(articles[1]) + ' views\n')

# Who are the most popular article authors of all time?
db = psycopg2.connect(dbname=dbName)

query = "select name, count(*) as views from (select name, title, concat('/article/',slug) as path from authors, articles where authors.id=articles.author) as authorship, log where authorship.path=log.path group by name order by views desc;"

db = psycopg2.connect(dbname=dbName)
c = db.cursor()
c.execute(query)
popular_authors = c.fetchall()
db.close()
print('\n')
file.write('\n')
print('* The most popular article authors of all time:\n')
file.write('* The most popular article authors of all time:\n')
for author in popular_authors:
    print(author[0] + ' -- ' + str(author[1]) + ' views\n')
    file.write(author[0] + ' -- ' + str(author[1]) + ' views\n')

# On which days did more than 1% of requests lead to errors?
db = psycopg2.connect(dbname=dbName)

query = "select date, (100.0*v1.errors/v2.all) as percent_errors from (select date(time) as date_error, count(*) as errors from log where status like '4%' or status like '5%' group by date(time)) as v1 join (select date(time), count(*) as all from log group by date(time)) as v2 on v1.date_error=v2.date where (100.0*v1.errors/v2.all)>2 order by date desc;"

db = psycopg2.connect(dbname=dbName)
c = db.cursor()
c.execute(query)
bad_days = c.fetchall()
db.close()
print('\n')
file.write('\n')
print('* Day(s) more than 1% of requests led to errors:\n')
file.write('* Day(s) more than 1% of requests led to errors:\n')
for day in bad_days:
    print(str(day[0].strftime('%B %d, %Y')) +
          ' -- ' + str(round(day[1], 1)) + '% errors')
    file.write(str(day[0].strftime('%B %d, %Y')) +
               ' -- ' + str(round(day[1], 1)) + '% errors')

file.close()
