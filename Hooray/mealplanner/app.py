import re

from flask_sqlalchemy import SQLAlchemy
#from mealplanner import models_food
from flask import Flask, redirect, render_template, json, request, jsonify, url_for
from mealplanner.forms import SearchForm
import sqlalchemy
from sqlalchemy.sql import text
from sqlalchemy import Table, Column, Integer, String, ForeignKey
import pandas as pd


app = Flask(__name__)

app.config.from_object('config')

db = SQLAlchemy(app)
db.init_app(app)

# The return value of create_engine() is our connection object
engine = sqlalchemy.create_engine(app.config['SQLALCHEMY_DATABASE_URI'], client_encoding='utf8')





'''
if not con.dialect.has_table(con, 'recipe'):  # If table don't exist, Create.
    recipe = Table('recipe', meta,
			   Column('id', Integer, primary_key=True),
			   Column('name', String), 
    		   Column('description', String), 
			   Column('steps', String)
			   )

    ingredients = Table('ingredients', meta,
	    				Column('recipeid', Integer, ForeignKey('recipe.id')), 
		    			Column('ingredient', String)
			    		)

    #create above tables
    meta.create_all(con)
'''
toInsert = [
    {'id': 1, 'name': 'chocolate cake', 'description': 'this is chocolate cake', 'steps': '1. mix ingredients 2.bake'}
]
# con.execute(meta.tables['recipe'].insert(), toInsert)

toInsert = [
    {'recipeid': 1, 'ingredient': 'flour'},
    {'recipeid': 1, 'ingredient': 'cocoa'},
    {'recipeid': 1, 'ingredient': '3 eggs'},
    {'recipeid': 1, 'ingredient': 'butter'}
]


# con.execute(meta.tables['ingredients'].insert(), toInsert)



# main page
@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        try:
            form = SearchForm()
            _query = request.form['query']
            return redirect(url_for('result', query=_query))
        except Exception as e:
            form = SearchForm()
            return render_template('index.html',
                                   title='Home',
                                   form=form)


    else:
        form = SearchForm()
        # if form.validate_on_submit():
        #    flash('Search requested for query="%s"' %
        #          (form.query.data))
        #    return redirect(url_for('result', query=form.query.data), evidence=form.evidence.data)
        return render_template('index.html',
                               title='Search',
                               form=form)
    return render_template('index.html')


# result page
@app.route('/result/<query>', methods=['GET', 'POST'])
def result(query):
    q = text("Select * from recipes where rid = '1'")
    result = engine.execute(q, i=query).fetchall()
    print(result)
    resultset = [dict(row) for row in result]
    df = pd.DataFrame(data=result, columns=['rid', 'r_name', 'r_description'])
    print(df)
    print(resultset)
    form = SearchForm()
    return render_template('result.html',
                           title='Results',
                           form=form, data=df.to_html())


"""
    :param query    str type that can be any case and return the top 5 result in json format
"""
@app.route('/autocomplete/<query>', methods=['GET'])
def autocomplete(query):
    # remove all the non-alphabet chars
    query = str.lower(str(query))
    re.sub(r'[^a-zA-Z]', '', query)
    unique_list = []
    result = []
    conn = engine.connect()
    sql = 'SELECT i.* FROM ingredient i, UNNEST(alt_names) names WHERE (lower(i_name) LIKE \'%s%s%s\') OR ' \
          '(lower(names) LIKE \'%s%s%s\') ORDER BY iid ASC LIMIT 100' % ('%', query, '%', '%', query, '%')
    rs = conn.execute(sqlalchemy.text(sql))
    for row in rs:
        if row['i_name'] not in unique_list:
            unique_list.append(row['i_name'])
            result.append(row)
            print(row)
        if len(unique_list) == 5:
            break

    rs.close()

    df = pd.DataFrame(data=result, columns=['ingredient_id', 'ingredient_name', 'ingredient_category', 'alt-name'])
    print(df)