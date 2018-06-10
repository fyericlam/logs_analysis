#!/usr/bin/env python3
# An internal reporting tool that will use information from the database
# to discover what kind of articles the site's readers like.

import psycopg2
import sys

dbName = 'news'


def connect(dbName):
    """
        Connect to the PostgreSQL database
        Input: database name
        Return: database connection and cursor (db, c)
    """
    try:
        db = psycopg2.connect('dbname={}'.format(dbName))
        c = db.cursor()
        return db, c
    except psycopg2.Error:
        print('Unable to connect to database')
        sys.exit(1)


def get_query(query):
    """
        Fetch query from database
        Input: SQL query string
        Return: query results in list (results)
    """
    # Connect to database and grab cursor
    db, c = connect(dbName)
    # Execute query
    c.execute(query)
    # Store results
    results = c.fetchall()
    # Close connection
    db.close()
    return results


def top_articles():
    """Return the most popular three articles of all time"""

    query = """select title, count(*) as views
            from (select title, concat('/article/',slug) as path from articles)
                as articles_path, log
            where articles_path.path=log.path
            group by title
            order by views desc;"""

    results = get_query(query)

    top_articles = '\n'
    top_articles += '---Logs analysis---\n'
    top_articles += '\n'
    top_articles += '* The most popular three articles of all time:\n'
    for article in results[:3]:
        top_articles += \
            '\"' + article[0] + '\"' + ' -- ' + str(article[1]) + ' views\n'

    return top_articles


def top_authors():
    """Return the most popular article authors of all time"""

    query = """select name, count(*) as views
            from (select name, title, concat('/article/',slug) as path
                from authors, articles where authors.id=articles.author)
                as authorship, log
            where authorship.path=log.path
            group by name
            order by views desc;"""

    results = get_query(query)

    top_authors = '\n'
    top_authors += '---Logs analysis---\n'
    top_authors += '\n'
    top_authors += '* The most popular article authors of all time:\n'
    for author in results:
        top_authors += \
            author[0] + ' -- ' + str(author[1]) + ' views\n'

    return top_authors


def top_error_days():
    """Return days more than 1% of requests led to errors"""

    query = """select date, (100.0*v1.errors/v2.all) as percent_errors
            from (select date(time) as date_error, count(*) as errors from log
                where status like '4%' or status like '5%' group by date(time))
                as v1 join
                (select date(time), count(*) as all from log group by date(time))
                as v2 on v1.date_error=v2.date
            where (100.0*v1.errors/v2.all)>2
            order by date desc;"""

    results = get_query(query)

    bad_days = '\n'
    bad_days += '---Logs analysis---\n'
    bad_days += '\n'
    bad_days += '* Day(s) more than 1% of requests led to errors:\n'
    for day in results:
        bad_days += \
            str(day[0].strftime('%B %d, %Y')) + ' -- ' \
            + str(round(day[1], 1)) + '% errors'

    return bad_days


if __name__ == '__main__':
    print(top_articles())
    print(top_authors())
    print(top_error_days())

    file = open('report.txt', 'w')
    file.write(top_articles() + top_authors() + top_error_days())
    file.close()
