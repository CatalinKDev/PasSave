import streamlit as st
import openai
import sqlite3
import random
import string
from dotenv import load_dotenv
import os

# Încarcă variabilele de mediu din fișierul chatgpt_api.env
load_dotenv('chatgpt.env')

# Setează API key-ul OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

# Linie de debug pentru a verifica încărcarea API key-ului
if openai.api_key:
    st.write("API key loaded successfully.")
else:
    st.write("Failed to load API key.")

# Functia pentru initializarea bazei de date
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

# Functia pentru inserarea unei parole in baza de date
def insert_password(name, platform, password):
    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()
    c.execute('INSERT INTO passwords (name, platform, password) VALUES (?, ?, ?)', (name, platform, password))
    conn.commit()
    conn.close()

# Functia pentru obtinerea parolelor din baza de date
def get_passwords():
    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()
    c.execute('SELECT name, platform, password FROM passwords')
    passwords = c.fetchall()
    conn.close()
    return passwords

# Functia pentru generarea unei parole random
def generate_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

# Functia pentru verificarea puterii parolei folosind ChatGPT API
def check_password_strength(password):
    prompt = f"Check the strength of this password: {password}. If it's weak, provide suggestions to make it stronger."

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a password strength checker."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150
    )
    
    return response['choices'][0]['message']['content'].strip()

# Initializarea bazei de date
init_db()

st.title("Password Manager")

# Initializam st.session_state daca nu exista
if 'generated_password' not in st.session_state:
    st.session_state.generated_password = None

# Form pentru a genera si salva o parola noua
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
            # Reset the generated password after saving
            st.session_state.generated_password = None
        else:
            st.error("Please generate a password first")

# Form pentru verificarea puterii parolei
st.write("Check Password Strength:")
with st.form("password_check_form"):
    user_password = st.text_input("Enter your password", type="password")
    check_password = st.form_submit_button("Check Password Strength")

    if check_password and user_password:
        strength_feedback = check_password_strength(user_password)
        st.write(f"Password Feedback: {strength_feedback}")

# Afisarea parolelor salvate
st.write("Saved Passwords:")
passwords = get_passwords()
for name, platform, password in passwords:
    st.write(f"Name: {name}, Platform: {platform}, Password: {password}")