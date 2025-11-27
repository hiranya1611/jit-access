import sqlite3, bcrypt

DB="../database/jit_access.db"

username="admin"
password="admin123"

hashed=bcrypt.hashpw(password.encode(),bcrypt.gensalt())

conn=sqlite3.connect(DB)
cur=conn.cursor()

cur.execute("INSERT INTO users(username,password,role) VALUES(?,?,?)",
            (username,hashed,"ADMIN"))

conn.commit()
conn.close()

print("Admin created successfully!")
