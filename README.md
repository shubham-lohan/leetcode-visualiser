# LeetCode Visualiser

A premium, fast, and highly interactive developer dashboard that transforms static LeetCode profiles into beautiful visual statistics. Built with FastAPI and a modern frontend to help developers track their problem-solving journey, contest ratings, and compare skills seamlessly.


## Features

- **🚀 Premium Aesthetics**: Dark mode, glassmorphism UI, glowing borders, and modern typography (Outfit/Inter).
- **📊 Advanced Analytics**: Interactive difficulty breakdowns, language usage, and topic-wise performance visualizations.
- **🏆 Contest Journey**: Track your rating trajectory, best/worst ranks, and consistency across weekly contests.
- **⚡ 60fps Animations**: Smooth, staggered entrance animations and real-time counter ticking powered by Motion One.
- **⚔️ Comparison Mode**: Head-to-head "Battle Mode" to compare two LeetCode profiles side-by-side.

## Tech Stack

- **Backend**: Python 3, FastAPI, Uvicorn, HTTPX
- **Data Processing**: Pandas
- **Frontend**: HTML5, CSS3 (Vanilla CSS variables), Vanilla JavaScript
- **Templates**: Jinja2
- **Charting Engine**: ApexCharts
- **Animation Engine**: Motion One (Framer Motion's vanilla JS core)

---

## Getting Started

### Prerequisites

- Python 3.9+
- pip (Python package installer)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/shubham-lohan/leetcode-visualiser.git
   cd leetcode-visualiser
   ```

2. **Set up a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**
   ```bash
   python -m uvicorn app.main:app --reload
   ```
   *The application will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000).*

---

## Contributing

We welcome contributions! If you're looking to add a new feature, fix a bug, or improve documentation, follow the guide below.

### Contribution Workflow

1. **Fork the repository** to your own GitHub account.
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/leetcode-visualiser.git
   ```
3. **Create a new branch** for your feature or bugfix:
   ```bash
   git checkout -b feature/your-awesome-feature
   ```
4. **Make your changes**. If you are modifying the frontend, be sure to maintain the premium design system (variables found in `app/static/css/main.css`).
5. **Test your changes** locally by running the FastAPI server.
6. **Commit your changes** with clear and descriptive commit messages:
   ```bash
   git commit -m "feat: add new dark mode toggle"
   ```
7. **Push your branch** to your fork:
   ```bash
   git push origin feature/your-awesome-feature
   ```
8. **Open a Pull Request** against the `main` branch of the original repository.

### Project Structure (For Contributors)

- `app/main.py`: The entry point for the FastAPI server and route definitions.
- `app/routers/`: Specific route handlers (e.g., handling the profile data fetch).
- `app/services/`: Business logic, LeetCode API interactions, and data formatting.
- `app/templates/`: Jinja2 HTML templates (`base.html`, `index.html`, `compare.html`).
- `app/static/css/main.css`: Core design system, variables, and styling.
- `app/static/js/dashboard.js`: Client-side logic for animations, counters, and rendering ApexCharts.
