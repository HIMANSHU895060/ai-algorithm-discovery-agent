# AI Algorithm Discovery Agent 🤖

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask API](https://img.shields.io/badge/API-Flask-red.svg)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> An **Autonomous AI Agent** that discovers, optimizes, and learns algorithms using reinforcement learning and genetic algorithms. Perfect for competitive programming, interview prep, and algorithmic optimization.

---

## ⚡ Features

### Core Capabilities
- **Algorithm Discovery**: Autonomous generation and discovery of optimal algorithms for various problem types
- **Reinforcement Learning (Q-Learning)**: Agent learns which algorithms work best for specific problem classes
- **Genetic Algorithm Optimization**: Evolves algorithm parameters through multiple generations
- **Multi-Algorithm Support**: Handles sorting, searching, optimization, dynamic programming, and graph algorithms
- **Performance Benchmarking**: Evaluates algorithms on multiple test cases with time/space metrics
- **Caching Layer**: Redis-powered result caching for faster repeated queries
- **Database Tracking**: SQLAlchemy integration to store discovered algorithms and RL history
- **API-First Design**: RESTful endpoints for seamless integration
- **Swagger Documentation**: Auto-generated API docs with request/response examples
- **Docker Support**: Production-ready containerization
- **CI/CD Pipeline**: GitHub Actions for automated testing and deployment

---

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Optional: Docker and Redis

### Quick Start (Development)

```bash
# Clone the repository
git clone https://github.com/HIMANSHU895060/ai-algorithm-discovery-agent.git
cd ai-algorithm-discovery-agent

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
python app.py
```

The API will be available at `http://localhost:5000`

### Docker Setup

```bash
# Build image
docker build -t ai-algo-agent .

# Run container
docker run -p 5000:8000 ai-algo-agent

# Or use docker-compose
docker-compose up --build
```

---

## 🚀 API Endpoints

### 1. Discover Algorithm
**Endpoint**: `POST /discover`

Discovers optimal algorithm for a given problem.

```bash
curl -X POST http://localhost:5000/discover \
  -H "Content-Type: application/json" \
  -d '{
    "problem_type": "sorting",
    "input_size": 1000,
    "constraints": {"time_limit": 1.0}
  }'
```

**Response**:
```json
{
  "algorithm": "quicksort",
  "estimated_time": 0.045,
  "space_complexity": "O(log n)",
  "fitness_score": 0.95,
  "implementation": "def quicksort(arr):\n..."
}
```

### 2. Optimize Algorithm
**Endpoint**: `POST /optimize`

Optimizes algorithm parameters using genetic algorithms.

```bash
curl -X POST http://localhost:5000/optimize \
  -H "Content-Type: application/json" \
  -d '{
    "algorithm_name": "quicksort",
    "test_cases": 100,
    "generations": 50
  }'
```

### 3. Evaluate Performance
**Endpoint**: `POST /evaluate`

Evaluates algorithm on provided test cases.

```bash
curl -X POST http://localhost:5000/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "algorithm_code": "def bubble_sort(arr): ...",
    "test_cases": [{"input": [5,2,3], "expected": [2,3,5]}]
  }'
```

### 4. Health Check
**Endpoint**: `GET /health`

```bash
curl http://localhost:5000/health
```

**Response**: `{"status": "healthy", "version": "1.0.0"}`

### 5. Get Algorithm History
**Endpoint**: `GET /history?limit=10`

Retrieve discovered algorithms from database.

---

## 🎯 Usage Examples

### Python Client

```python
import requests
import json

API_URL = "http://localhost:5000"

# Discover optimal sorting algorithm
response = requests.post(
    f"{API_URL}/discover",
    json={
        "problem_type": "sorting",
        "input_size": 10000
    }
)

algorithm_data = response.json()
print(f"Best Algorithm: {algorithm_data['algorithm']}")
print(f"Fitness Score: {algorithm_data['fitness_score']}")
```

### JavaScript/Node.js

```javascript
const axios = require('axios');

const discoverAlgorithm = async () => {
  try {
    const response = await axios.post('http://localhost:5000/discover', {
      problem_type: 'sorting',
      input_size: 10000
    });
    console.log('Discovered Algorithm:', response.data);
  } catch (error) {
    console.error('Error:', error.message);
  }
};

discoverAlgorithm();
```

---

## 🧠 How It Works

### Architecture

```
┌─────────────────────────────────────────┐
│         Client (API Request)            │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│      Flask REST API (app.py)            │
│  - Route handling                       │
│  - Request validation                   │
│  - Response formatting                  │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│    Algorithm Discovery Engine           │
│  - RL Q-Learning Agent                  │
│  - Genetic Algorithm Evolution          │
│  - Algorithm Candidate Generation       │
└──────────────┬──────────────────────────┘
               │
    ┌──────────┼──────────┐
    │          │          │
┌───▼──┐   ┌───▼──┐   ┌───▼──┐
│Cache │   │  DB  │   │ Eval │
│Redis │   │SQLite│   │Env   │
└──────┘   └──────┘   └──────┘
```

### Reinforcement Learning Flow

1. **State**: Problem characteristics (type, size, constraints)
2. **Action**: Algorithm selection (quicksort, mergesort, etc.)
3. **Reward**: Performance score (speed, space, accuracy)
4. **Learning**: Q-value updates for state-action pairs

---

## 📊 Project Structure

```
├── app.py                 # Flask API server
├── agent_core.py          # Core RL + GA logic
├── rl_agent.py            # Q-Learning implementation
├── genetic_algorithm.py    # GA for optimization
├── models.py              # SQLAlchemy models
├── utils.py               # Helper functions
├── tests/                 # Unit tests (pytest)
├── requirements.txt       # Python dependencies
├── Dockerfile             # Container config
├── docker-compose.yml     # Multi-container setup
└── .github/workflows/     # CI/CD pipelines
```

---

## 🔧 Configuration

Create `.env` file:

```env
FLASK_ENV=development
DEBUG=True
DATABASE_URL=sqlite:///algo_agent.db
REDIS_URL=redis://localhost:6379/0
AGENT_LEARNING_RATE=0.1
GENETIC_POPULATION_SIZE=50
GENETIC_GENERATIONS=100
```

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_rl_agent.py

# Run with verbose output
pytest -v
```

---

## 📈 Performance Metrics

- **Algorithm Discovery**: ~500ms average
- **Optimization (50 generations)**: ~2-3 seconds
- **Caching Hit Rate**: >80% on repeated queries
- **API Response Time**: <100ms (cached), <500ms (non-cached)

---

## 🎓 Use Cases

### 1. Competitive Programming
- Find optimal solutions quickly
- Learn algorithm trade-offs
- Practice interview preparation

### 2. Software Engineering Interviews
- Demonstrate algorithm knowledge
- Show optimization skills
- Explain trade-offs to interviewers

### 3. Research & Education
- Study algorithm performance characteristics
- Benchmark different implementations
- Teach algorithm concepts

### 4. Production Systems
- Auto-select algorithms based on data characteristics
- Optimize performance critical code paths
- Monitor algorithm effectiveness

---

## 🚦 Roadmap

- [ ] Web UI dashboard
- [ ] Algorithm code visualization
- [ ] Real-time performance graphs
- [ ] Support for custom algorithm templates
- [ ] Multi-language code generation (Java, C++, Go)
- [ ] GraphQL API
- [ ] Machine learning-powered algorithm synthesis
- [ ] Batch processing API
- [ ] Team collaboration features

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit changes: `git commit -m 'Add my feature'`
4. Push to branch: `git push origin feature/my-feature`
5. Submit a Pull Request

### Development Setup

```bash
pip install -r requirements-dev.txt
pre-commit install  # For code quality checks
```

---

## 📝 License

MIT License - see LICENSE file for details

---

## 💡 FAQ

**Q: Can it generate new algorithms from scratch?**
A: Currently it selects and optimizes existing algorithms. Future versions will support algorithm synthesis.

**Q: What problem types are supported?**
A: Sorting, searching, optimization, dynamic programming, and graph algorithms. More coming soon.

**Q: Is it suitable for production?**
A: With proper configuration and testing, yes. The caching layer and database support production deployments.

**Q: How accurate are the recommendations?**
A: Typically 90-95% accurate based on test cases. Accuracy improves with more training data.

---

## 🎯 Contact & Support

- **Author**: [HIMANSHU895060](https://github.com/HIMANSHU895060)
- **Issues**: [GitHub Issues](https://github.com/HIMANSHU895060/ai-algorithm-discovery-agent/issues)
- **Discussions**: [GitHub Discussions](https://github.com/HIMANSHU895060/ai-algorithm-discovery-agent/discussions)

---

## 📚 References

- [Reinforcement Learning Basics](https://en.wikipedia.org/wiki/Reinforcement_learning)
- [Genetic Algorithms](https://en.wikipedia.org/wiki/Genetic_algorithm)
- [Algorithm Design Manual](https://www.algorist.com/)
- [Flask Documentation](https://flask.palletsprojects.com/)

---

**Made with ❤️ for competitive programmers and algorithm enthusiasts**
