# AI-GROCERY-TRACKER-SYSTEM


# AI Grocery Tracker System

A Streamlit-based app for tracking grocery expiry dates using Azure Document Intelligence OCR. Features include user authentication, item management, insights, alerts, and recycle bin.

## Features
- Authentication and user sessions
- Add items manually or via image OCR (single/dual photos)
- Product list with search, filter, and status (expired, soon, fresh)
- Insights dashboard and expiry alerts
- Recycle bin for deleted items
- Dark/light theme toggle

## Prerequisites
- Python 3.8+ installed
- Azure Document Intelligence resource (endpoint and API key)
- Optional: MongoDB for persistent storage

## Setup Instructions for Local Run

### 1. Clone the Repository
git clone https://github.com/Armanwarraich/AI-GROCERY-TRACKER-SYSTEM.git
cd AI-GROCERY-TRACKER-SYSTEM

text

### 2. Create and Activate Virtual Environment
python -m venv venv
venv\Scripts\activate # Windows

source venv/bin/activate # macOS/Linux
text

### 3. Install Dependencies
pip install -r requirements.txt

text

### 4. Set Up Environment Variables
Create a `.env` file in the root with your Azure credentials:
AZURE_DOC_INTELLIGENCE_ENDPOINT=https://your-endpoint.cognitiveservices.azure.com/
AZURE_DOC_INTELLIGENCE_KEY=your-api-key

text
- Add other vars if needed (e.g., MongoDB URI).

### 5. Run the App
streamlit run app.py

text
- Open http://localhost:8501 in your browser.
- Sign up/log in to use.

### 6. Usage
- **Add Item**: Use the tab to upload images for OCR or add manually.
- **Products**: View and manage your grocery list.
- **Insights/Alerts**: Check stats and upcoming expiries.
- **Recycle Bin**: Restore deleted items.
- Theme: Switch in the sidebar.

## Troubleshooting
- **Credentials Error**: Verify `.env` values and reload the app.
- **Import Errors**: Ensure all files are in place and dependencies are installed.
- **OCR Issues**: Test images under 50MB; check Azure quota.
- For Git issues, see .gitignore for ignored files.

## Contributing
Fork, make changes, and submit PRs. Report issues on GitHub.

## License
MIT License.
Commit and Push the README:

text
git add README.md
git commit -m "Added detailed README for project setup"
git push origin main