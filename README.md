# Logs Analysis

# Installation

To execute the project run in a terminal:

    run.py

# Description

This is a program aimed to practice queries with Postgresql and psycopg2 python library
    
The database provides 3 tables:

* log
* authors
* articles

### Log

Column  |   Type    |
--------|-----------
path    |   text    |
ip      |   inet    |
method  |   text    |
status  |   text    |
time    |   timestamp with time zone    |  
id      |   integer |

### Authors

Column  |   Type    |
--------|-----------
name    |   text    |
bio     |   text    |
id      |   integer |
`TABLE "articles" CONSTRAINT "articles_author_fkey" FOREIGN KEY (author) REFERENCES authors(id)`
### Articles

Column  |   Type    |
--------|-----------
autho   |   integer |
title   |   text    |
slug    |   text    |
lead    |   text    |
body    |   text    |
time    |   timestamp with time zone    |
id      |   integer |
`articles_author_fkey" FOREIGN KEY (author) REFERENCES authors(id)`