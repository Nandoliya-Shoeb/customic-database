# customic-database — deploy guide

Steps to prepare and deploy this Flask app:

1. Create a virtual environment and install dependencies

```bash
python -m venv venv
venv\Scripts\activate    # Windows
pip install -r requirements.txt
```

2. Create a `.env` (or set env vars) based on `.env.example` and set a strong `SECRET_KEY`.

3. Initialize Git, commit, and push to GitHub. Then deploy on a provider (Render/Heroku/Railway):

```bash
# initialize git (if not already)
git init
git add .
git commit -m "Initial commit"

# create remote on GitHub (or use gh CLI)
# git remote add origin https://github.com/<username>/<repo>.git
# git push -u origin main
```

4. Deploy options

- Heroku: create app, set env vars, and push; ensure `Procfile` present.
- Render: link the GitHub repo, set build command `pip install -r requirements.txt`, start command `gunicorn app:app`.

Notes
- In production don't run `app.run()`; the `Procfile` uses `gunicorn`.
- The app uses SQLite (`database.db`) by default — for scaled production use a managed DB and update `DATABASE` accordingly.
