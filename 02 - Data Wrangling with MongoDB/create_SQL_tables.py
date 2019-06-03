import os
import sqlite3 as sq

filepath = r'S:\Code\School\WGU_DataAnalyst_NanoDegree\02 - Data Wrangling with MongoDB'

connection = sq.connect(os.path.join(filepath, 'MapData.db'))
cursor = connection.cursor()

node_query = '''CREATE TABLE nodes (
    id INTEGER PRIMARY KEY NOT NULL,
    lat REAL,
    lon REAL,
    user TEXT,
    uid INTEGER,
    version INTEGER,
    changeset INTEGER,
    timestamp TEXT
);'''

node_tags_query = '''CREATE TABLE nodes_tags (
    id INTEGER,
    key TEXT,
    value TEXT,
    type TEXT,
    FOREIGN KEY (id) REFERENCES nodes(id)
);'''

ways_query = '''CREATE TABLE ways (
    id INTEGER PRIMARY KEY NOT NULL,
    user TEXT,
    uid INTEGER,
    version TEXT,
    changeset INTEGER,
    timestamp TEXT
);'''

ways_tags_query = '''CREATE TABLE ways_tags (
    id INTEGER NOT NULL,
    key TEXT NOT NULL,
    value TEXT NOT NULL,
    type TEXT,
    FOREIGN KEY (id) REFERENCES ways(id)
);'''

ways_nodes_query = '''CREATE TABLE ways_nodes (
    id INTEGER NOT NULL,
    node_id INTEGER NOT NULL,
    FOREIGN KEY (id) REFERENCES ways(id),
    FOREIGN KEY (node_id) REFERENCES nodes(id)
);'''

queries = [node_query, node_tags_query, ways_query, ways_tags_query, ways_nodes_query]

for query in queries:
    cursor.execute(query)