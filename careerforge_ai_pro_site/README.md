# CareerForge AI Pro Website

A premium interview readiness website with AI-powered analysis, advanced confidence evaluation, and a luxury design system.

## What’s Included
- **Premium UI/UX** with glassmorphism, dark gradients, and modern dashboard styling.
- **Resume analysis** with PDF/DOCX upload support.
- **Career profile scoring** including technical, communication, portfolio, GitHub, and LinkedIn signals.
- **Live Confidence Lab** with webcam-based visual confidence estimation.
- **Mock Interview Simulator** for role-based practice and instant answer feedback.
- **PDF Report Generation** with downloadable career assessment.
- **QR Code Sharing** for easy report preview and sharing.

## Setup
1. Open PowerShell and navigate to the backend folder:
   ```powershell
   cd c:\Users\welcome\OneDrive\Desktop\interview\careerforge_ai_pro_site\backend
   ```
2. Install dependencies:
   ```powershell
   python -m pip install -r requirements.txt
   ```
3. Start the Flask backend server:
   ```powershell
   python app.py
   ```
4. Open your browser to:
   ```text
   http://127.0.0.1:8501
   ```

## Notes
- The application serves the static frontend from the `frontend/` folder.
- The `backend/modules/reporting.py` file generates PDF reports and QR codes on demand.
- The live confidence lab uses your webcam for a premium preparation experience.

## Next Enhancements
- Add real AI / OpenAI integration for resume and answer analysis.
- Extend mock interview with audio recording and voice transcription.
- Add cloud deployment instructions for Streamlit Community or Render.
