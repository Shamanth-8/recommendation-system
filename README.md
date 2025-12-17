# Assessment Recommendation Engine

A Streamlit-based web application that provides personalized assessment recommendations based on user skills and performance.

## Features

- 📊 Interactive dashboard with user metrics
- 📝 Take assessments and track progress
- 💡 Get personalized recommendations
- 👤 User profile management
- 🔒 Secure authentication

## Prerequisites

- Python 3.8+
- pip (Python package manager)

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd assessment-recommendation-engine
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   - Copy `.env.example` to `.env`
   - Update the values in `.env` as needed

## Running the Application

1. **Start the Streamlit app**
   ```bash
   streamlit run app.py
   ```

2. **Access the application**
   Open your web browser and go to: `http://localhost:8501`

## Default Login Credentials

- **Admin User**
  - Email: admin@example.com
  - Password: admin123

- **Regular User**
  - Email: user@example.com
  - Password: user123

## Project Structure

```
assessment-recommendation-engine/
├── .env                    # Environment variables
├── data/                   # Data files (catalog.json)
├── requirements.txt        # Python dependencies
├── app.py                 # Main Streamlit application
├── app/                   # Application modules (models, services)
└── README.md              # This file
```

## Customization

- Update `config.yaml` to add/remove users or modify authentication settings
- Modify the assessment questions in `app.py` under the `show_assessment()` function
- Add more recommendation logic in the `show_recommendations()` function

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
