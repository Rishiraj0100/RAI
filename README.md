# RAI

RAI is a web platform that allows users to **create AI models** and **chat with them**. It provides a simple interface to experiment with AI and explore conversational models. Think of it as your personal AI studio just like Instagram AI Studio.

---

## 🚀 Features

- Create and manage AI models
- Chat with AI models in real-time
- Create user accounts with username and email
- Lightweight, easy to use, and open-source

---

## 🛠️ Technologies

- **Frontend:** HTML (Jinja2 templating), Tailwind CSS
- **Backend:** Python (Quart framework)
- **AI:** Ollama for AI models

---

## 📦 Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/Rishiraj0100/RAI.git
    cd RAI
    ```

2. Create Virtual Environment:
    ```bash
    python3 -m venv .venv
    ```

3. Install Dependencies:
    ```bash
    python3 -m pip install -r requirements.txt
    ```

4. Install Ollama:
   - Download Ollama from [Ollama's official website](https://ollama.com/download)
   - Pull some models using `ollama pull <model>`
        ```bash
        ollama pull llama3.2
        ```
   - Add the model names to [routes/models.py (Line 29)](routes/models.py#L29)

5. Setup database and run the project
    ```bash
    python3 -m aerich init-db
    python3 run.py
    ```
    - Now open http://localhost:8090/x to create admin user.
    - You can change the credentials at [run.py (Line 43)](run.py#L43).

---
Now your project is ready for production deployment.

---
## Production Deployment
Make necessary changes in [run.sh (Line 2)](run.sh#L2) and then run:
```bash
chmod +x run.sh
bash run.sh
```

## 🙏 Acknowledgements & Contribution

- The chat interface UI is inspired by [ChatGPT](https://chat.openai.com/).
- Interested in contributing? Contributions are welcome! Check out [CONTRIBUTING.md](CONTRIBUTING.md) and follow our [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
