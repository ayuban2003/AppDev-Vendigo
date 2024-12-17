import mysql.connector
import hashlib
import secrets

def connectDB():
    regisDB = mysql.connector.connect(
        host="localhost",
        user="root",
        database="vendigodb"
    )

    return regisDB

def generate_salt():
    return secrets.token_hex(12)

def hash_password(password, salt):
    salted_password = password + salt
    hashed_password = hashlib.sha256(salted_password.encode()).hexdigest()
    return hashed_password

def store_user(user, usertype, password):
   connect = connectDB()
   cursor = connect.cursor()

   salt = generate_salt()
   hashed_password = hash_password(password, salt)

   cursor.execute("INSERT INTO users (User, UserType, Password, Salt) VALUES (%s, %s, %s, %s)", (user, usertype, hashed_password, salt))
   
   connect.commit()
   connect.close()

def main():
    username = input("Set the name of the Admin:\n")
    password = input("Set the password of Admin:\n")
    usertype = input("Set the Role of User:\nUser Type:\n - Normal\n - Admin\n")

    store_user(username, usertype, password)
    print("Success!")
    exit()

main()
   