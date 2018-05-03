#!/usr/bin/env python3

import psycopg2
import sys
from termcolor import cprint

DATABASE = "news"

def fetch_query(query):
    # Try to connect to the DDBB
    try:
        conn = psycopg2.connect("dbname=%s" % DATABASE)
        cur = conn.cursor()
        cur.execute(query)
        res = cur.fetchall()
        conn.close()
        return res
    except:
        print("Database %s is not available") % DATABASE
        sys.exit(1)
    
def print_top_articles():
    q = """select title, count (*) as num
        from log, articles where log.path like '%' || slug || '%'
        and status like '%OK%' and path not like '/'
        group by title order by num desc limit 3;
        """
    res = fetch_query(q)
    # Print question
    cprint("What are the most popular three articles of all time?", attrs=['bold'])

    # Iterate query results
    for k, v in res:
        cprint("%s ---> %s views" % (k, str(v)), "magenta")

def print_top_authors():
    q = """select name, count(*) as num
    from authors, articles, log
    where authors.id = articles.author and log.path like '%' || slug || '%'
    group by name;"""
    res = fetch_query(q)
    # Print question
    print("\n")
    cprint("Who are the most popular article authors of all time?", attrs=['bold'])
    # Iterate query results
    for k, v in res:
        cprint("%s ---> %s views" % (k, str(v)), "magenta")

def print_top_errors_days():
    q = """select time::timestamp::date as date,
    count(case when status not like '%OK%' then 1 end) / count(*)::decimal
    * 100::decimal as percentage from log group by date
    having count(case when status not like '%OK%' then 1 end) / count(*)::decimal
    * 100::decimal > 1;"""
    res = fetch_query(q)
    # Print question
    print("\n")
    cprint("On which days did more than 1% of requests lead to errors?",
       attrs=['bold'])
    # Iterate query results
    for k, v in res:
        cprint("{0} ---> {1}% views".format(k, str(round(v, 2))), "magenta")

if __name__ == '__main__':
    print_top_articles()
    print_top_authors()
    print_top_errors_days()
