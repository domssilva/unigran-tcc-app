# unigran-tcc-app

project description TBD

## 🛠 Setup Environment Variables

1. **Create a `.env` file** in the project root (same folder as `app.py`):  
   ```bash
   touch .env  # Linux/Mac
   # OR
   type nul > .env  # Windows
   ```

 .env example:
 ```
# .env
SECRET_KEY=your-random-secret-key
DATABASE_URL=sqlite:///app.db      # SQLite file path
 ```

🚫**Warning** - Never commit the .env to the git repo!
Ensure that .env is in the `.gitignore` file!

2. Installing dependencies
pip install -r requirements.txt


