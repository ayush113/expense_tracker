import sqlite3 #module to interact with DBMS which manages the program's data
import time #module which allows us to get real time
from datetime import datetime #module which allows us to verify user input for dates
import string
from tabulate import tabulate

db_name="Accounts.db"

#ensures referential integrity (https://pythonschool.net/databases/referential-integrity/) 
with sqlite3.connect(db_name) as db: 
    cur=db.cursor()
    cur.execute("PRAGMA foreign_keys = ON")
    db.commit()

try:    #checks if tables exist; if not, creates them
    with sqlite3.connect(db_name) as db:
        cur=db.cursor()
        cur.execute("SELECT COUNT(*) FROM users")
        pick=cur.fetchall()
        cur.execute("SELECT COUNT(*) FROM purchases")
        pick=cur.fetchall()
        db.commit()
      
except:
    with sqlite3.connect(db_name) as db:
        cur=db.cursor()
        cur.execute("DROP TABLE IF EXISTS users")
        cur.execute("DROP TABLE IF EXISTS purchases")
        cur.execute("""CREATE TABLE users(userID INTEGER,
                                          userName TEXT,
                                          pwd TEXT,
                                          question TEXT,
                                          ans TEXT,
                                          budget REAL,
                                          PRIMARY KEY(userID))""")        
     
        cur.execute("""CREATE TABLE purchases(purchaseID INTEGER,
                                              desc TEXT,
                                              userID INTEGER,
                                              cat TEXT,
                                              loc TEXT,
                                              price REAL,
                                              date DATE,
                                              PRIMARY KEY(purchaseID),
                                              FOREIGN KEY(userID) REFERENCES users(userID)
                                              ON UPDATE RESTRICT ON DELETE CASCADE)""")
        db.commit()
