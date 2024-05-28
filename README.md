# PasSave with ChatGPT Integration

This is a Streamlit application that allows users to generate random passwords, save them, and check their strength using the ChatGPT API.

## Features

- **Generate Random Passwords**: Create strong, random passwords.
- **Save Passwords**: Save passwords along with a name and platform.
- **Check Password Strength**: Use the ChatGPT API to evaluate the strength of a user-created password and get suggestions for improvement.

## Installation

To get started with this project, follow these steps:

### Prerequisites

- Python 3.6 or later
- A virtual environment is recommended

### Clone the Repository

```bash
git clone https://github.com/yourusername/password-manager.git
cd password-manager
```
### Install Dependencies
### It's recommended to create a virtual environment first:


```bash
python -m venv venv
source venv/bin/activate
```
### Setup OpenAI API Key
### You need an OpenAI API key to use the ChatGPT functionality. Create a .env file in the root directory and add your API key:
```bash
OPENAI_API_KEY=your_openai_api_key_here
```
## Install python-dotenv if you haven't:
```bash
pip install python-dotenv
```
## Running the Application
### Run the Streamlit application with:
```bash
streamlit run app.py
```
## Usage
### Generate Password: Enter a name and platform, then select the desired password length and click "Generate Password".
### Save Password: After generating a password, click "Save Password" to save it to the database.
### Check Password Strength: Enter a password in the "Enter your password" field and click "Check Password Strength" to evaluate its strength using the ChatGPT API.

## File Structure
```bash
password-manager/
│
├── app.py                 # Main application file
├── passwords.db           # SQLite database file (created after first run)
├── requirements.txt       # List of dependencies
└── .env                   # Environment variables file (add your OpenAI API key here)
```
### Requirements
### Streamlit
### OpenAI
### SQLite3
### Python-dotenv
### Contributing
### Contributions are welcome! Please create an issue or open a pull request with your changes.
