# ⚙️ AiEngineer Project

_Part of the [Master AI Repository](../README.md)_

A comprehensive AI engineering project repository containing machine learning applications, Python learning materials, and advanced programming concepts.

## 📁 Project Structure

```
AiEngineer/
├── MachineProjects/                    # Machine Learning Applications
│   ├── app.py                         # Streamlit frontend for movie recommendation
│   ├── main.py                        # FastAPI backend for movie recommendation
│   ├── Recomendation_system.ipynb     # Jupyter notebook for development
│   ├── MoviesData.csv                 # Movie dataset
│   ├── *.pkl                          # Serialized ML models and data
│   ├── requirements.txt               # Python dependencies
│   └── README.md                      # Detailed project documentation
│
└── PythonwithBasicandAdvanced/        # Python Learning Materials
    ├── RecursionandFunctions/         # Advanced Python concepts
    │   ├── Oops.py                    # Object-Oriented Programming examples
    │   └── function.PY                # Function examples
    │
    └── simplePython/                  # Basic Python tutorials
        ├── first.py                   # Basic Python syntax and variables
        ├── secondString.py            # String operations
        ├── ListandTuple.py            # List and tuple operations
        ├── DictionaryandTuple.py      # Dictionary operations
        ├── FORLOOPS.py                # Loop constructs
        └── LoopsinPython.py           # Advanced loop examples
```

## 🚀 Featured Projects

### 1. Movie Recommendation System

A production-ready movie recommendation system with the following features:

#### 🎯 Key Features

- **Content-Based Filtering**: TF-IDF vectorization for movie similarity
- **Genre-Based Recommendations**: Discover movies by genre
- **TMDB Integration**: Real-time movie data, posters, and metadata
- **Modern Architecture**: FastAPI backend + Streamlit frontend
- **Search Functionality**: Advanced movie search with intelligent suggestions
- **Responsive UI**: Modern interface with custom styling

#### 🛠️ Technology Stack

- **Backend**: FastAPI with Python
- **Frontend**: Streamlit
- **Machine Learning**: Scikit-learn (TF-IDF)
- **External API**: TMDB (The Movie Database)
- **Deployment**: Render (backend), Streamlit Cloud (frontend)

#### 📊 ML Models

- TF-IDF Vectorizer for content similarity
- Pre-computed similarity matrices
- Genre-based filtering
- Efficient caching for performance

#### 🌐 Live Demo

- **Backend API**: Deployed on Render
- **Frontend**: Deployed on Streamlit Cloud
- **Real-time Integration**: TMDB API for up-to-date movie data

### 2. Python Learning Path

Comprehensive Python tutorials from basics to advanced concepts:

#### 📚 Beginner Level (`simplePython/`)

- **first.py**: Basic Python syntax, variables, and data types
- **secondString.py**: String manipulation and operations
- **ListandTuple.py**: List and tuple data structures
- **DictionaryandTuple.py**: Dictionary operations and methods
- **FORLOOPS.py**: Loop constructs and iteration
- **LoopsinPython.py**: Advanced looping patterns

#### 🎓 Advanced Level (`RecursionandFunctions/`)

- **function.PY**: Function definitions and parameters
- **Oops.py**: Object-Oriented Programming concepts
  - Class definitions
  - Object instantiation
  - Constructor methods (`__init__`)
  - Attributes and methods

## 🛠️ Development Environment

### Prerequisites

- Python 3.8+
- Git
- TMDB API Key (for movie recommendation system)

### Setup Instructions

#### 1. Clone the Repository

```bash
git clone <repository-url>
cd AiEngineer
```

#### 2. Movie Recommendation System Setup

```bash
cd MachineProjects

# Create virtual environment
python -m venv .venv

# Activate environment
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
echo "TMDB_API_KEY=your_api_key_here" > .env
```

#### 3. Run Movie Recommendation System

```bash
# Start backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Start frontend (in separate terminal)
streamlit run app.py --server.port 8501
```

#### 4. Python Learning Modules

```bash
cd PythonwithBasicandAdvanced

# Run individual learning modules
python simplePython/first.py
python simplePython/secondString.py
python RecursionandFunctions/Oops.py
```

## 📖 Learning Path

### Phase 1: Python Fundamentals

1. **Basic Syntax** (`first.py`)
   - Variables and data types
   - Print statements and basic operations
2. **String Operations** (`secondString.py`)
   - String manipulation
   - String methods and formatting
3. **Data Structures**
   - Lists and Tuples (`ListandTuple.py`)
   - Dictionaries (`DictionaryandTuple.py`)
4. **Control Flow**
   - For loops (`FORLOOPS.py`)
   - Advanced looping patterns (`LoopsinPython.py`)

### Phase 2: Advanced Concepts

1. **Functions** (`function.PY`)
   - Function definition and parameters
   - Return values and scope
2. **Object-Oriented Programming** (`Oops.py`)
   - Classes and objects
   - Constructors and methods
   - Attributes and inheritance basics

### Phase 3: Applied Machine Learning

1. **Data Analysis** (`Recomendation_system.ipynb`)
   - Pandas for data manipulation
   - Data cleaning and preprocessing
2. **Machine Learning Models**
   - TF-IDF vectorization
   - Content-based filtering
   - Model serialization with pickle
3. **Web Development**
   - FastAPI for REST APIs
   - Streamlit for web applications
   - API integration and deployment

## 🎯 Key Learning Outcomes

### Python Programming

- ✅ Master basic Python syntax and data types
- ✅ Understand object-oriented programming principles
- ✅ Implement functions and control structures
- ✅ Work with various data structures

### Machine Learning

- ✅ Data preprocessing and cleaning
- ✅ Feature engineering with TF-IDF
- ✅ Building recommendation systems
- ✅ Model deployment and serialization

### Web Development

- ✅ RESTful API development with FastAPI
- ✅ Interactive web apps with Streamlit
- ✅ External API integration
- ✅ Cloud deployment strategies

### Software Engineering

- ✅ Project structure and organization
- ✅ Environment management
- ✅ Version control with Git
- ✅ Documentation best practices

## 🔧 Configuration Files

### Requirements.txt

```
fastapi==0.104.1
uvicorn==0.24.0
streamlit==1.28.1
pandas==2.1.3
numpy==1.25.2
scikit-learn==1.3.2
requests==2.31.0
python-dotenv==1.0.0
jupyter==1.0.0
matplotlib==3.8.2
seaborn==0.13.0
```

### Environment Variables (.env)

```env
TMDB_API_KEY=your_tmdb_api_key_here
```

## 🌟 Project Highlights

### Technical Achievements

- **Scalable Architecture**: Microservices with FastAPI + Streamlit
- **ML Integration**: Real-time recommendation engine
- **API Design**: RESTful endpoints with proper documentation
- **Performance**: Efficient caching and model optimization
- **Deployment**: Production-ready cloud deployment

### Educational Value

- **Progressive Learning**: From basics to advanced concepts
- **Practical Examples**: Real-world applications
- **Code Quality**: Clean, documented, and maintainable code
- **Best Practices**: Industry-standard development workflows

## 🚀 Deployment Information

### Movie Recommendation System

- **Backend**: Deployed on Render (FastAPI)
- **Frontend**: Deployed on Streamlit Cloud
- **Database**: Serialized models (pickle files)
- **External APIs**: TMDB for movie data

### Access Points

- API Documentation: Available at `/docs` endpoint
- Interactive Demo: Streamlit Cloud application
- Source Code: Complete repository with all components

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 Development Guidelines

### Code Standards

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add comments for complex logic
- Include docstrings for functions and classes

### Project Organization

- Keep related files in appropriate directories
- Use descriptive file names
- Maintain clean project structure
- Update documentation for new features

## 🐛 Troubleshooting

### Common Issues

1. **Virtual Environment**: Ensure proper activation
2. **Dependencies**: Install all requirements.txt packages
3. **API Keys**: Set up TMDB API key correctly
4. **Port Conflicts**: Use different ports if needed

### Getting Help

- Check individual project README files
- Review code comments and documentation
- Test components individually
- Use Python's built-in help system

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **TMDB** for providing the movie database API
- **FastAPI** team for the excellent web framework
- **Streamlit** for the intuitive app development platform
- **Scikit-learn** for machine learning tools

---

**Note**: This repository is designed for both learning and practical application. The movie recommendation system demonstrates real-world AI engineering practices, while the Python modules provide a solid foundation for programming concepts.

Happy Learning! 🎓✨