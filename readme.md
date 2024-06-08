# Rare: The Publishing Platform for the Discerning Writer - Backend

### Description
This is the backend server for the Rare publishing platform, built using Python and SQLite. It provides a RESTful API to manage users, categories, posts, tags, and related entities. This server handles authentication, data management, and serves as the main data source for the Rare frontend application.

### Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

### Installation

1. **Clone the Repository**: 
    ```bash
    git clone https://github.com/your-repo/rare-backend.git
    ```
2. **Navigate to the Project Directory**:
    ```bash
    cd rare-backend
    ```
3. **Create a Virtual Environment** (optional but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```
4. **Install the Project Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
5. **Set Up the Database**:
    ```bash
    sqlite3 db.sqlite3 < loaddata.sql
    ```
6. **Run the Server**:
    ```bash
    python json-server.py
    ```

### Usage

- **Start the Development Server**:
    ```bash
    python json-server.py
    ```
  The server will start on `http://localhost:8000`.

-###  **API Endpoints**:
 ```
  - **Users**:
  - **Categories**:
  - **Posts**:
  - **Tags**:
  - **Post Tags**:
  - **Authentication**:
```
### Contributing

1. **Fork the Repository**:
    ```bash
    git clone https://github.com/your-username/rare-backend.git
    ```
2. **Create a New Branch**:
    ```bash
    git checkout -b feature/your-feature-name
    ```
3. **Make Your Changes** and **Commit Them**:
    ```bash
    git add .
    git commit -m "Your commit message"
    ```
4. **Push to the Branch**:
    ```bash
    git push origin feature/your-feature-name
    ```
5. **Create a Pull Request** on GitHub, describing the changes you made and why they are valuable.

### License

This project is licensed under the MIT License.

---

This README provides a comprehensive guide for installing, using, and contributing to the backend of the Rare publishing platform, ensuring that it complements the frontend README effectively.
