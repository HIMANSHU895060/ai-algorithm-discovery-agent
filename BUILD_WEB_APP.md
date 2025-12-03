# Build Web App for AI Algorithm Discovery Agent

## Quick Start (5 Minutes)

### Option 1: Fully Automated Setup

```bash
# Clone the repo
git clone https://github.com/HIMANSHU895060/ai-algorithm-discovery-agent
cd ai-algorithm-discovery-agent

# Run setup script (creates everything)
bash setup.sh
```

### Option 2: Manual Setup

#### Step 1: Setup Backend
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py  # Runs on http://localhost:5000
```

#### Step 2: Setup Frontend (in new terminal)
```bash
cd frontend
npm install
npm start  # Runs on http://localhost:3000
```

---

## Directory Structure

```
ai-algorithm-discovery-agent/
├── app.py                      # Flask backend
├── agent_core.py               # AI logic
├── requirements.txt            # Python dependencies
├── frontend/                   # React app
│  ├── public/
│  ├── src/
│  │  ├── App.jsx
│  │  ├── components/
│  │  │  ├── DiscoveryForm.jsx
│  │  │  ├── ResultCard.jsx
│  │  │  ├── Dashboard.jsx
│  │  │  └── AlgorithmHistory.jsx
│  │  ├── App.css
│  │  └── index.js
│  └── package.json
├── .github/
│  └── workflows/
│     └── deploy.yml
└── setup.sh                    # Automation script
```

---

## Features Included

### Backend (Flask)
- ✅ REST API endpoints for algorithm discovery
- ✅ Reinforcement Learning agent
- ✅ Genetic algorithm optimization
- ✅ Database support (SQLAlchemy)
- ✅ Redis caching
- ✅ CORS enabled
- ✅ Comprehensive error handling

### Frontend (React)
- ✅ Beautiful UI with Tailwind CSS
- ✅ Real-time algorithm discovery
- ✅ Performance visualization with Recharts
- ✅ Algorithm history tracking
- ✅ Responsive design (mobile + desktop)
- ✅ Loading states & error handling
- ✅ Dark theme optimized for coding

---

## Deployment

### Deploy Frontend to Vercel (FREE)
```bash
cd frontend
npm install -g vercel
vercel deploy
```

### Deploy Backend to Railway (FREE)
1. Go to Railway.app
2. Connect GitHub repo
3. Set environment variables
4. Deploy

### Or use Render (FREE)
```bash
# Push to GitHub
git push origin main

# Connect repo to Render.com
# Select Python as runtime
# Deploy
```

---

## API Endpoints

### 1. Discover Algorithm
```bash
curl -X POST http://localhost:5000/discover \
  -H "Content-Type: application/json" \
  -d '{
    "problem_type": "sorting",
    "input_size": 1000,
    "constraints": {"time_limit": 1.0}
  }'
```

**Response:**
```json
{
  "algorithm": "quicksort",
  "fitness_score": 0.95,
  "time_complexity": "O(n log n)",
  "space_complexity": "O(log n)",
  "estimated_time": 0.045,
  "implementation": "def quicksort(arr): ..."
}
```

### 2. Get Algorithm History
```bash
curl http://localhost:5000/history?limit=10
```

### 3. Health Check
```bash
curl http://localhost:5000/health
```

---

## Development Workflow

### For Backend Developers
```bash
# Activate virtual environment
source venv/bin/activate

# Run with debug mode
FLASK_ENV=development python app.py

# Run tests
pytest

# Format code
black .
flake8 .
```

### For Frontend Developers
```bash
cd frontend

# Dev server with hot reload
npm start

# Build for production
npm run build

# Run tests
npm test
```

---

## Testing

### Backend Tests
```bash
pytest tests/test_api.py -v
pytest --cov=. --cov-report=html
```

### Frontend Tests
```bash
cd frontend
npm test -- --coverage
```

---

## Troubleshooting

### Port Already in Use
```bash
# Backend
lsof -i :5000
kill -9 <PID>

# Frontend
lsof -i :3000
kill -9 <PID>
```

### CORS Issues
Make sure Flask has CORS enabled:
```python
from flask_cors import CORS
CORS(app)
```

### Database Connection Error
```bash
# Ensure database exists
python -c "from models import db; db.create_all()"
```

---

## Performance Tips

1. **Enable Redis Caching**
   ```bash
   redis-cli ping
   # Start Redis: redis-server
   ```

2. **Production Server**
   ```bash
   gunicorn --workers 4 --bind 0.0.0.0:5000 app:app
   ```

3. **Frontend Optimization**
   - Use code splitting
   - Lazy load components
   - Enable gzip compression

---

## Project Showcase

### For Interviews, Explain:

1. **Architecture**: Microservices with React frontend & Flask backend
2. **Tech Stack**: React, Flask, SQLAlchemy, Redux, Tailwind CSS
3. **Features**: Real-time API, caching, optimization algorithms, responsive UI
4. **Deployment**: Vercel + Railway (production-grade)
5. **Code Quality**: Jest, Pytest, ESLint, Black

### Key Files to Show:
- `frontend/src/components/` - UI component architecture
- `agent_core.py` - RL + GA implementation
- `app.py` - RESTful API design
- `.github/workflows/` - CI/CD pipeline

---

## Next Steps

1. ✅ Clone repo
2. ✅ Run `bash setup.sh`
3. ✅ Open http://localhost:3000
4. ✅ Test the app
5. ✅ Deploy to Vercel + Railway
6. ✅ Share link in resume

---

## Resources

- [React Docs](https://react.dev)
- [Flask Docs](https://flask.palletsprojects.com)
- [Tailwind CSS](https://tailwindcss.com)
- [Recharts](https://recharts.org)
- [Railway Deployment](https://railway.app)
- [Vercel Deployment](https://vercel.com)

---

## Support

Having issues? 
- Check GitHub Issues
- Review this guide again
- Debug with `console.log()` / print statements

---

**Built for placement success! 🚀**
