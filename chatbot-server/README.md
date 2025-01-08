# 🤖 UTE Chatbot Server

UTE Chatbot Server is a chatbot application developed using 🐍 Python, leveraging the 🚀 FastAPI framework for 📡 API development and 🗄️ database management.

## 🏃‍♂️ Running the Application

To run the application, use the following command: 💻

```bash
uvicorn app.main:app --reload
```

If you want to run the 🧪 test application, use this command:

```bash
uvicorn test.test_main:app --reload
```

## 📦 Installing Dependencies

To install the required 📜 packages for the project, execute the following command:

```bash
pip install -r requirements.txt
```

## 🗄️ Initializing the Database

To initialize the database, follow these steps:

1. 🛠️ Create the database if it does not already exist:
   ```bash
   python -m app.database.database
   ```

2. 🧱 Generate the tables in the database:
   ```bash
   python -m app.database.create_tables
   ```

3. 🌱 Populate the database with sample data:
   ```bash
   python -m app.database.init_database
   ```

## 🔄 Resetting the Virtual Environment

To reset the virtual environment, follow these steps:

1. 🗑️ Remove the existing virtual environment:
   ```bash
   rmdir /s /q venv
   ```

2. 🆕 Create a new virtual environment:
   ```bash
   python -m venv venv
   ```

3. ✅ Activate the virtual environment:
   ```bash
   venv\Scripts\activate
   ```

## 🛠️ Fixing Environment Issues

If you encounter issues with the environment, follow these steps:

1. 🔍 Open the Command Palette (Ctrl+Shift+P).
2. 🔧 Search for "Python: Select Interpreter."
3. ✅ Select the virtual environment where you installed the dependencies.

## 🧹 Removing Unnecessary Files from Git

To remove unnecessary files from Git tracking, execute the following commands:

```bash
git rm --cached -r app/database/__pycache__
git rm --cached -r app/__pycache__
git rm --cached -r __pycache__
git rm --cached '*.pyc'
```

Then, 💾 commit the changes:

```bash
git commit -m "Remove __pycache__ and .pyc files from Git tracking"
```

## 📬 Contact Information

If you have any questions or need support, feel free to reach out via 📧 email: [tuankiett.cao@gmail.com](mailto:tuankiett.cao@gmail.com).

## 🤝 Contributions

Contributions to this project are welcome. Please 🍴 fork the repository, create a new branch, make your changes, and submit a pull request for review.

@🎓 Graduation_Project_2024_AI_Chatbot_(UniBot)

