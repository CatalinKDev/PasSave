import streamlit as st
import sqlite3
import random
import string

def init_db():
    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            platform TEXT,
            password TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_password(name, platform, password):
    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()
    c.execute('INSERT INTO passwords (name, platform, password) VALUES (?, ?, ?)', (name, platform, password))
    conn.commit()
    conn.close()

def get_passwords():
    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()
    c.execute('SELECT name, platform, password FROM passwords')
    passwords = c.fetchall()
    conn.close()
    return passwords

def generate_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

init_db()

st.title("Password Manager")

if 'generated_password' not in st.session_state:
    st.session_state.generated_password = None

with st.form("password_form"):
    name = st.text_input("Name")
    platform = st.text_input("Platform")
    password_length = st.slider("Password Length", 6, 24, 12)
    generate = st.form_submit_button("Generate Password")
    save = st.form_submit_button("Save Password")

    if generate:
        st.session_state.generated_password = generate_password(password_length)
        st.write(f"Generated Password: {st.session_state.generated_password}")

    if save and name and platform:
        if st.session_state.generated_password:
            insert_password(name, platform, st.session_state.generated_password)
            st.success(f"Password saved for {name} on {platform}")
            st.session_state.generated_password = None
        else:
            st.error("Please generate a password first")

# Afisarea parolelor salvate
st.write("Saved Passwords:")
passwords = get_passwords()
for name, platform, password in passwords:
    st.write(f"Name: {name}, Platform: {platform}, Password: {password}")