#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3, codecs
from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

conn = sqlite3.connect('semantic.db')

def db_insert():
    c = conn.cursor() #создала точку соприкосновения с базой
    
    c.execute('''CREATE TABLE sintaksema (id, verb, prep, noun, padez, all_sint)''')#создали пустой лист с тремя колонками
    sintax = codecs.open('sintaksema.csv', 'r', 'utf-8')
    for line in sintax:
        line = line.strip()
        idd, verb, prep, noun, padez, all_sint = line.split(',')
        c.execute(u'''INSERT INTO sintaksema VALUES (?, ?, ?, ?, ?, ?)''', (idd, verb, prep, noun, padez, all_sint))
##    sintax.close()
    
    c.execute('''CREATE TABLE preposition (id, prep)''')
    prep = codecs.open('prep.csv', 'r', 'utf-8')
    for line in prep:
        line = line.strip()
        idd, prep = line.split(',')
        c.execute(u'''INSERT INTO preposition VALUES (?, ?)''', (idd, prep))
##    prep.close()
    
    c.execute('''CREATE TABLE verb (id, verb, sem_class)''')
    verb = codecs.open('verb.csv', 'r', 'utf-8')
    for line in verb:
        line = line.strip()
        idd, verb, sem_class = line.split(',')
        c.execute(u'''INSERT INTO verb VALUES (?, ?, ?)''', (idd, verb, sem_class))
##    verb.close()
    
    c.execute('''CREATE TABLE noun (id, noun, sem_class)''')
    noun = codecs.open('noun.csv', 'r', 'utf-8')
    for line in noun:
        line = line.strip()
        idd, noun, sem_class = line.split(',')
        c.execute(u'''INSERT INTO noun VALUES (?, ?, ?)''', (idd, noun, sem_class))
##    noun.close()
    
    c.execute('''CREATE TABLE padez (padez)''')
    padez = codecs.open('case.csv', 'r', 'utf-8')
    for line in padez:
        line = line.strip()
        padez = line.split(',')
        c.execute(u'''INSERT INTO padez VALUES (?)''', (padez))
##    padez.close()
    
    c.execute('''CREATE TABLE all_examples (id_sint, text)''')
    all_examples = codecs.open('examples.csv', 'r', 'utf-8')
    for line in all_examples:
        line = line.strip()
        id_sint, text = line.split('#')
        c.execute(u'''INSERT INTO all_examples VALUES (?, ?)''', (id_sint, text))
##    all_examples.close()
    
    c.execute('''CREATE TABLE first_example (id, year, text)''')
    c.execute('''CREATE TABLE last_example (id, year, text)''')
    conn.commit()
    conn.close()

@app.route('/')
def form():
    if request.form:
        
        conn = sqlite3.connect('test.db')
        c = conn.cursor()

        word = u''
        word = request.args['word']
        c.execute('SELECT all_sint FROM sintaksema WHERE all_sint=?', word)
        for constr in c.fetchone():
            return render_template('personal-page.html', constr = constr, word = word)
    except:
        return render_template('landing-page.html')
        

app.run(debug = True) 
