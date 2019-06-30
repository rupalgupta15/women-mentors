import tweepy
import time

import pandas as pd
import numpy as np
import os
import json
import time

import sqlite3

consumer_key = os.getenv("CONSUMER_KEY_TWITTER")
consumer_secret = os.getenv("CONSUMER_SECRET_TWITTER")
access_token = os.getenv("ACCESS_KEY_TWITTER")
access_token_secret = os.getenv("ACCESS_SECRET_TWITTER")

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


conn = sqlite3.connect('mentors.db')
c = conn.cursor()


# SCHEMA: Id (Int), Desc (text),
def create_table(table):
    c.execute("CREATE TABLE IF NOT EXISTS {} (unix INTEGER, id INTEGER, description TEXT)".format(table))
    # c.execute("SELECT * FROM {} LIMIT 5".format(table))
    # info = c.fetchall()
    conn.commit()


def read_table(table, n):
    c.execute("SELECT * FROM {} LIMIT {}".format(table, n))
    info = c.fetchall()
    print(info)


def update_table(table, dict):
    # For every row fill the value from dict into the table
    unix = dict["unix"]
    id = dict["id"]
    description = dict["description"]
    c.execute("INSERT INTO {} (unix, id, description) "
              "VALUES (?, ?, ?)".format(table), (unix, id, description))

    conn.commit()


def delete_table(table):
    c.execute("DROP TABLE {} ".format(table))
    conn.commit()


if __name__ == "__main__":
    create_table('mentees')
    update_table('mentees', {'unix': int(time.time()),'id': 1, 'description': 'Python, Java'})
    read_table('mentees', 2)

