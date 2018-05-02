#!/usr/bin/env python3

import psycopg2
from termcolor import cprint

DATABASE = "news"
# Try to connect to the DDBB
try:
    conn = psycopg2.connect("dbname=%s" % DATABASE)
except:
    print("Database %s is not available") % DATABASE

# First query
cur = conn.cursor()
cur.execute("""select title, count (*) as num
from log, articles where log.path like '%' || slug || '%'
and status like '%OK%' and path not like '/'
group by title order by num desc limit 3;
""")
res = cur.fetchall()
# Print question
cprint("What are the most popular three articles of all time?", attrs=['bold'])

# Iterate query results
for k, v in res:
    cprint("%s ---> %s views" % (k, str(v)), "magenta")

# Second query
cur.execute("""select name, count(*) as num
from authors, articles, log
where authors.id = articles.author and log.path like '%' || slug || '%'
group by name;""")
print("\n")

# Print question
cprint("Who are the most popular article authors of all time?", attrs=['bold'])
res = cur.fetchall()

# Iterate query results
for k, v in res:
    cprint("%s ---> %s views" % (k, str(v)), "magenta")

# Third query
cur.execute("""select time::timestamp::date as date,
count(case when status not like '%OK%' then 1 end) / count(*)::decimal
* 100::decimal as percentage from log group by date
having count(case when status not like '%OK%' then 1 end) / count(*)::decimal
* 100::decimal > 1;""")
print("\n")

# Print question
cprint("On which days did more than 1% of requests lead to errors?",
       attrs=['bold'])
res = cur.fetchall()

# Iterate query results
for k, v in res:
    cprint("{0} ---> {1}% views".format(k, str(round(v, 2))), "magenta")