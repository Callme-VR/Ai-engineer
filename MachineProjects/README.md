# Machine Projects Setup

This folder contains machine learning projects and a configured Python environment.

## Environment Setup

A virtual environment `.venv` has been created with the following libraries:

- Jupyter (Notebook/Lab)
- NumPy
- Pandas
- Matplotlib
- Seaborn
- Scikit-learn
- Requests

## How to use in VS Code

1. Open this folder in VS Code.
2. Open any `.ipynb` file (e.g., `setup_test.ipynb`).
3. In the top-right corner of the notebook editor, click **Select Kernel**.
4. Choose **Python Environments**.
5. Select the environment corresponding to `.venv` (it should display `MachineProjects`).

## Running the Test Notebook

Open `setup_test.ipynb` and run the cells to verify everything is working correctly.

## Movie Recommendation System

A production-ready movie recommendation system powered by TMDB API, TF-IDF content-based filtering, and genre-based recommendations. The system consists of a FastAPI backend and Streamlit frontend.

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit     │    │   FastAPI       │    │   TMDB API      │
│   Frontend       │◄──►│   Backend       │◄──►│   External      │
│   (Streamlit    │    │   (Render)      │    │   Service       │
│    Cloud)        │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   ML Models     │
                       │   (TF-IDF)      │
                       │   Pickle Files  │
                       └─────────────────┘
```

## Features

- **Content-Based Recommendations**: TF-IDF vectorization for movie similarity
- **Genre-Based Recommendations**: Discover movies by genre
- **TMDB Integration**: Real-time movie data, posters, and metadata
- **Search Functionality**: Advanced movie search with suggestions
- **Responsive UI**: Modern Streamlit interface with custom styling
- **RESTful API**: Clean FastAPI backend with proper documentation

## Prerequisites

- Python 3.8+
- TMDB API Key (Get one from [TMDB](https://www.themoviedb.org/settings/api))
- Git
- Render Account (for backend deployment)
- Streamlit Cloud Account (for frontend deployment)

## Local Development Setup

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd MachineProjects
```

### 2. Set Up Virtual Environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Create a `.env` file:

```env
TMDB_API_KEY=your_tmdb_api_key_here
```

### 5. Run Locally

**Backend (FastAPI):**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend (Streamlit):**
```bash
streamlit run app.py --server.port 8501
```

Access the application at `http://localhost:8501`

## Production Deployment

### Backend Deployment (Render)

#### Step 1: Prepare Your Repository

Ensure your repository contains:
- `main.py` (FastAPI application)
- `requirements.txt`
- `.env` (with TMDB_API_KEY)
- All pickle files (`df.pkl`, `indices.pkl`, `tfidf_matrix.pkl`, `tfidf.pkl`)

#### Step 2: Create Render Service

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **New → Web Service**
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: `movie-recommendation-api`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: `Free` or `Starter`

#### Step 3: Environment Variables

Add environment variable in Render dashboard:
- `TMDB_API_KEY`: Your TMDB API key

#### Step 4: Deploy

Render will automatically deploy your service. Once deployed, you'll get a URL like:
`https://movie-recommendation-api.onrender.com`

### Frontend Deployment (Streamlit Community Cloud)

#### Step 1: Prepare Configuration Files

Create `config.toml` in `.streamlit/` directory:

```toml
[server]
port = 8501
headless = true
enableCORS = false

[browser]
gatherUsageStats = false
```

#### Step 2: Update API Base URL

Modify `app.py` to use your deployed backend URL:

```python
# Change this line in app.py
API_BASE = "https://your-backend-url.onrender.com"
```

#### Step 3: Deploy to Streamlit Cloud

1. Go to [Streamlit Community Cloud](https://share.streamlit.io/)
2. Click **New app**
3. Connect your GitHub repository
4. Configure:
   - **Repository**: Your repo
   - **Branch**: `main`
   - **Main file path**: `app.py`
   - **Python version**: `3.9` or higher

#### Step 4: Set Secrets

In Streamlit Cloud dashboard, add secrets:
```bash
TMDB_API_KEY=your_tmdb_api_key_here
```

## Project Structure

```
MachineProjects/
├── main.py                 # FastAPI backend application
├── app.py                  # Streamlit frontend application
├── requirements.txt        # Python dependencies
├── .env                   # Environment variables (local)
├── .streamlit/
│   └── config.toml        # Streamlit configuration
├── df.pkl                 # Movie dataset
├── indices.pkl            # Title-to-index mapping
├── tfidf_matrix.pkl       # TF-IDF matrix
├── tfidf.pkl              # TF-IDF vectorizer
├── rebuild_models.py      # Model rebuilding script
├── Recomendation_system.ipynb  # Development notebook
└── README.md              # This file
```

## API Endpoints

### Health Check
- `GET /health` - Service health status

### Movie Data
- `GET /home` - Home feed with categories (popular, trending, etc.)
- `GET /movie/id/{tmdb_id}` - Movie details by TMDB ID
- `GET /tmdb/search` - Search TMDB movies

### Recommendations
- `GET /recommend/tfidf` - TF-IDF based recommendations
- `GET /recommend/genre` - Genre-based recommendations
- `GET /movie/search` - Combined search with recommendations

## Usage Examples

### API Usage

```bash
# Get trending movies
curl "https://your-api.onrender.com/home?category=trending&limit=10"

# Get movie details
curl "https://your-api.onrender.com/movie/id/550"

# Get TF-IDF recommendations
curl "https://your-api.onrender.com/recommend/tfidf?title=Inception&top_n=5"
```

### Frontend Features

1. **Home Feed**: Browse trending, popular, top-rated movies
2. **Search**: Search movies with intelligent suggestions
3. **Movie Details**: View detailed information with recommendations
4. **Responsive Design**: Works on desktop and mobile devices

## Security Considerations

- API keys are stored as environment variables
- CORS is properly configured for production domains
- Input validation on all API endpoints
- Rate limiting considerations for TMDB API calls

## Performance Optimization

- TF-IDF models are loaded once at startup
- Efficient caching with Streamlit's `@st.cache_data`
- Optimized image loading with lazy loading
- Minimal API response payloads

## Troubleshooting

### Common Issues

1. **Backend Deployment Fails**:
   - Check if all pickle files are committed to git
   - Verify `requirements.txt` is complete
   - Ensure TMDB_API_KEY is set in Render environment

2. **Frontend Can't Connect to Backend**:
   - Verify API_BASE URL in `app.py` is correct
   - Check CORS settings in FastAPI
   - Ensure backend is deployed and accessible

3. **TMDB API Errors**:
   - Verify API key is valid and active
   - Check API rate limits
   - Ensure proper error handling

### Logs and Monitoring

- **Render**: Check logs in Render dashboard
- **Streamlit**: View logs in Streamlit Cloud dashboard
- **Local**: Check console output for debugging

## Updating Models

To update the recommendation models:

1. Run `rebuild_models.py` locally
2. Commit the updated pickle files
3. Redeploy both backend and frontend

## Scaling Considerations

- **Database**: Consider migrating from pickle files to a proper database
- **Caching**: Implement Redis for better caching
- **Load Balancing**: Use multiple instances for high traffic
- **CDN**: Use CDN for static assets and images

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue in the GitHub repository
- Check the troubleshooting section above
- Review API documentation at `/docs` endpoint

---

**Note**: This project uses The Movie Database (TMDB) API. Ensure you comply with their terms of service and attribution requirements.
