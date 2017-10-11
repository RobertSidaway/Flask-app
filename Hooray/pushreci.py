"""
    This file is going to automatically insert json recipes into posgresql database
"""
import os
import json
import re

import psycopg2


# change postgres server at the beginning
conn = psycopg2.connect(database="planner", user="postgres",
                        password="mirrorcall", host="localhost",
                        port="5433")
cur = conn.cursor()


def correct_data(data):
    new = str(data).replace("'", "''")
    re.sub('\\[\w]*', '', new)

    return new.strip()


def create_table():
    global conn
    global cur

    sql = 'CREATE TABLE recipe_category (' \
        'rcid SERIAL4 PRIMARY KEY,' \
        'rc_name VARCHAR' \
        ');' \
        'CREATE TABLE recipe (' \
        '	rid SERIAL4 PRIMARY KEY,' \
        '	r_name VARCHAR UNIQUE NOT NULL,' \
        '	r_description VARCHAR,' \
        '	i_id INTEGER REFERENCES ingredient(iid),' \
        '	rc_id INTEGER REFERENCES recipe_category(rcid)' \
        ');'
    cur.execute(sql)


def main():
    global conn
    global cur

    #create_table()

    for dirpath, dirnames, files in os.walk('./recipes_JSON'):
        for f in files:
            if f == '.DS_Store':
                pass
            else:
                with open('recipes_JSON/'+f) as data_file:
                    data = json.load(data_file)
                    print(correct_data(data['ingredients'][8]))

                    break

    conn.commit()
    cur.close()
    conn.close()

if __name__ == '__main__':
    main()