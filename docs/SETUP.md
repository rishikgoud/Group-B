# LegalEase AI - Contract Analyzer

## Quick Start Guide

### Prerequisites
- Python 3.8+
- Node.js 16+
- MongoDB Atlas account (free tier)

### Backend Setup (FastAPI)

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp env.example .env
   # Edit .env with your API keys and MongoDB URI
   ```

5. **Run the server:**
   ```bash
   uvicorn main:app --reload
   ```

   The API will be available at `http://localhost:8000`
   API documentation at `http://localhost:8000/docs`

### Frontend Setup (React)

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Set up environment variables:**
   ```bash
   cp env.example .env
   # Edit .env with your API URL
   ```

4. **Start the development server:**
   ```bash
   npm start
   ```

   The app will be available at `http://localhost:3000`

### Environment Variables

#### Backend (.env)
```env
GEMINI_API_KEY=your_gemini_api_key_here
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/legalease
SECRET_KEY=your_secret_key_here
DEBUG=True
```

#### Frontend (.env)
```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_API_VERSION=v1
```

### API Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check
- `POST /api/v1/contracts/upload` - Upload contract
- `GET /api/v1/contracts/list` - List contracts
- `POST /api/v1/analysis/analyze` - Analyze contract
- `POST /api/v1/chat/ask` - Chat with AI
- `GET /api/v1/analytics/*` - Analytics endpoints

### Project Structure

```
legalEase-ai/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── core/           # Core configuration
│   │   ├── models/         # Database models
│   │   ├── services/       # Business logic
│   │   └── utils/          # Utility functions
│   ├── requirements.txt
│   └── main.py
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API services
│   │   ├── utils/          # Utility functions
│   │   └── styles/         # CSS/Tailwind styles
│   ├── package.json
│   └── public/
├── data/                   # Sample data and datasets
└── docs/                   # Documentation
```

### Next Steps

1. **Get API Keys:**
   - Gemini Pro API key from Google AI Studio

2. **Set up MongoDB:**
   - Create a free MongoDB Atlas cluster
   - Get connection string

3. **Test the application:**
   - Upload a sample contract
   - Try the AI chat feature
   - Explore the analytics dashboard

### Development Commands

#### Backend
```bash
# Run with auto-reload
uvicorn main:app --reload

# Run tests
pytest

# Format code
black .

# Lint code
flake8
```

#### Frontend
```bash
# Start development server
npm start

# Build for production
npm run build

# Run tests
npm test

# Lint code
npm run lint
```

### Troubleshooting

1. **Port conflicts:** Make sure ports 3000 and 8000 are available
2. **API connection:** Check that backend is running and CORS is configured
3. **File uploads:** Ensure uploads directory has write permissions
4. **MongoDB connection:** Verify connection string and network access

### Support

For issues and questions:
- Check the API documentation at `/docs`
- Review the console logs for errors
- Ensure all environment variables are set correctly
