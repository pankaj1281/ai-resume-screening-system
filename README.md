# AI Resume Screening and Job Recommendation System

Production-ready end-to-end project for automated resume parsing, ATS scoring, job category prediction, and resume-vs-JD matching using NLP + ML.

## Project Overview

This system helps candidates and recruiters by:
- Parsing uploaded resumes (PDF/DOCX/TXT)
- Extracting core profile details and skills
- Predicting suitable job category
- Calculating ATS compatibility score (out of 100)
- Comparing resume with job description
- Highlighting matched/missing skills and improvement suggestions

## Key Features

### Authentication
- Register
- Login (JWT)
- Change password
- Forgot password flow endpoint (demo-safe placeholder)

### Resume Analysis
- Upload resume with validation (type + size <= 10 MB)
- Parse contact details, links, skills, sections
- Job category prediction endpoint
- ATS scoring with deduction reasons
- Resume vs JD keyword + similarity analysis

### Dashboard and Visualization
- ATS score gauge
- Skill match pie chart (Chart.js)
- Experience/Education timeline placeholders wired for API-driven rendering

### Admin Panel APIs
- Manage users
- Delete users
- Platform statistics

## Architecture

- **Backend:** FastAPI + SQLAlchemy + JWT auth
- **ML/NLP:** scikit-learn pipeline, NLTK preprocessing, optional XGBoost/LightGBM support
- **Frontend:** React + Tailwind + Chart.js
- **Database:** SQLite (dev), PostgreSQL-ready via `DATABASE_URL`
- **Deployment:** Docker, docker-compose, GitHub Actions CI

Detailed note: `/docs/architecture.md`

## Folder Structure

```text
ai-resume-screening-system/
├── backend/
│   ├── app/
│   │   ├── routes/
│   │   ├── services/
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   └── ...
│   └── requirements.txt
├── frontend/
│   ├── src/
│   ├── package.json
│   └── ...
├── training/
│   ├── download_dataset.py
│   ├── preprocess.py
│   ├── train.py
│   ├── evaluate.py
│   ├── predict.py
│   └── export_model.py
├── datasets/
├── models/
├── tests/
├── docs/
├── api/
├── database/
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## API Endpoints

### Auth
- `POST /register`
- `POST /login`
- `POST /forgot-password`
- `POST /change-password`

### Core
- `POST /upload`
- `POST /predict`
- `POST /ats-score`
- `POST /compare-job`
- `GET /history`
- `GET /profile`

### Admin
- `GET /admin/users`
- `DELETE /admin/users/{user_id}`
- `GET /admin/stats`

Interactive docs available at `/docs` once backend runs.

## Local Setup

### 1) Backend
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn backend.app.main:app --reload
```

### 2) Frontend
```bash
cd frontend
npm install
npm run dev
```

### 3) Docker (Full Stack)
```bash
docker compose up --build
```

## Dataset and Training Pipeline

### Dataset
- Supported: Kaggle/custom CSV
- Place source file at: `datasets/raw/resume_dataset.csv`
- Expected columns: `resume_text`, `category`

### Training Scripts
```bash
python training/download_dataset.py
python training/preprocess.py
python training/train.py
python training/evaluate.py
python training/export_model.py
```

### Artifacts Saved
- `models/model.joblib`
- `models/vectorizer.joblib`
- `models/label_encoder.joblib`

## Evaluation Metrics

`training/evaluate.py` reports:
- Accuracy
- Precision
- Recall
- F1-score
- Classification report
- Confusion matrix image (`reports/confusion_matrix.png`)
- ROC-AUC (when `predict_proba` is available)

## Testing

Run backend/unit tests:
```bash
pytest -q
```

Run frontend build check:
```bash
cd frontend
npm install
npm run build
```

### CI Check Troubleshooting

If backend tests fail with:
`ValueError: password cannot be longer than 72 bytes...`

Use these steps:
1. Confirm `backend/requirements.txt` includes `bcrypt==4.0.1`.
2. Reinstall backend auth dependencies:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt --force-reinstall
   ```
3. Re-run checks locally:
   ```bash
   pytest -q
   cd frontend && npm run build
   ```

Current test coverage includes:
- Auth flow
- Protected prediction/ATS APIs
- ATS and JD comparison utility behavior

## Security Measures

- Password hashing with bcrypt
- JWT-based protected routes
- Upload type and size validation
- Input validation with Pydantic
- Basic rate limiting dependency

## Deployment

- **Backend:** Render/Railway (FastAPI container)
- **Frontend:** Vercel (React app)
- **CI/CD:** GitHub Actions workflow in `.github/workflows/ci.yml`

## Screenshots

Add your screenshots here after running the UI:
- Dashboard
- Upload page
- ATS report page
- Job comparison page
- Admin dashboard

## Future Improvements

- SentenceTransformer/BERT embedding benchmark in training loop
- Resume ranking and multi-resume comparison
- Interview question generator
- Grammar checking and cover letter generation
- Skill-gap roadmap and salary prediction

## License

Use MIT license for academic/open-source usage (add `LICENSE` file if required by your institution).
