import os
import psycopg2
import bcrypt

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "RenderDB")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "root")

def connect_db():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return conn
    except Exception as e:
        print("Error connecting to the database:", e)
        return None

# Register a new user
def register_user(user_id, password, full_name, email):
    conn = connect_db()
    if conn:
        try:
            with conn.cursor() as cur:
                # Check if user_id already exists
                cur.execute("SELECT COUNT(*) FROM users WHERE user_id = %s", (user_id,))
                if cur.fetchone()[0] > 0:
                    print("User ID already exists.")
                    return False
                
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                cur.execute("""
                    INSERT INTO users (user_id, password, full_name, email)
                    VALUES (%s, %s, %s, %s)
                """, (user_id, hashed_password, full_name, email))
                conn.commit()
                return True
        except Exception as e:
            print("Error during registration:", e)
            return False
        finally:
            conn.close()

# Verify login credentials
def login_user(user_id, password):
    conn = connect_db()
    if conn:
        try:
            with conn.cursor() as cur:
                # Check if the user exists
                cur.execute("SELECT password FROM users WHERE user_id = %s", (user_id,))
                result = cur.fetchone()

                if result is None:
                    return "User ID not found."  # Specific error message

                stored_password = result[0].tobytes().decode('utf-8')

                if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                    return "Login successful!"
                else:
                    return "Incorrect password."  # Specific error message
        except Exception as e:
            print("Error during login:", e)
            return "An error occurred during login."
        finally:
            conn.close()
            
# Fetch user details
def get_user_details(user_id):
    conn = connect_db()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT user_id, full_name, email FROM users WHERE user_id = %s", 
                    (user_id,)
                )
                result = cur.fetchone()
                if result:
                    return {"user_id": result[0], "full_name": result[1], "email": result[2]}
        except Exception as e:
            print("Error fetching user details:", e)
        finally:
            conn.close()
    return None