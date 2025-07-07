# Clinic Intake Form Web App

This is a Flask-based web application for collecting clinic event and participant information and storing it in an Excel file.

## Features

- Multi-step form for event and participant data collection
- Data saved to `clinic_intake_form.xlsx`
- Flash messages for validation feedback
- Deployable on Render with public URL for integration with LegalServer

## Deployment Instructions

### 1. Upload to GitHub

1. Create a new repository on GitHub.
2. Upload the following files:
   - `app.py`
   - `clinic_intake_form.xlsx`
   - `requirements.txt`
   - `render.yaml`
   - `.gitignore`
   - `README.md`
   - `templates/form.html`

### 2. Deploy on Render

1. Go to https://render.com and log in or sign up.
2. Click **New +** → **Web Service**.
3. Connect your GitHub account and select the repository.
4. Render will auto-detect the environment and use:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
5. Choose the Free plan and deploy.
6. After deployment, you'll receive a public URL to use in LegalServer.

## Local Development

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/clinic-intake-form.git
   cd clinic-intake-form
   ```