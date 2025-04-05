# CulinaryVertex

## Overview

CulinaryVertex is a full-stack application designed for the "Gourmet Bistro" restaurant. It features a modern web frontend for users to interact with and a Python backend that includes an AI-powered agent for handling specific tasks, potentially related to customer interactions or orders.

## Features

*   **Web Interface:** A user-friendly frontend built with Next.js and React.
*   **AI Agent:** A backend agent (for customer service or order processing) with defined operational boundaries.
*   **Menu Management:** Backend components for handling restaurant menu data.
*   **Features:**
    *   Online Ordering
    *   User Accounts
    *   Admin Dashboard (Implementation Pending)

## Tech Stack

*   **Frontend:**
    *   [Next.js](https://nextjs.org/) (React Framework)
    *   [React](https://reactjs.org/)
    *   [TypeScript](https://www.typescriptlang.org/)
    *   [Tailwind CSS](https://tailwindcss.com/)
*   **Backend:**
    *   [Python](https://www.python.org/)

## Project Structure

```
.
├── CulinaryVertexBackend/      # Python backend source code
│   ├── agent.py              # AI agent logic
│   ├── menu.py               # Menu data handling
│   ├── policies.py           # Business logic/rules
│   └── requirements.txt      # Backend Python dependencies
├── CulinaryVertexFrontend/     # Next.js frontend source code
│   ├── app/                  # Next.js App Router directory
│   ├── components/           # Reusable React components
│   ├── public/               # Static assets
│   ├── package.json          # Frontend dependencies and scripts
│   ├── tsconfig.json         # TypeScript configuration
│   └── next.config.mjs       # Next.js configuration
└── README.md                 # This file
```

## Getting Started

### Prerequisites

*   [Node.js](https://nodejs.org/) (LTS version recommended)
*   [Python](https://www.python.org/downloads/) (Version 3.x recommended)
*   `pip` and `venv` (usually included with Python)

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd CulinaryVertex
    ```

2.  **Setup Frontend:**
    ```bash
    cd CulinaryVertexFrontend
    npm install
    npx next build
    npx next start
    ```

3.  **Setup Backend:**
    ```bash
    cd ../CulinaryVertexBackend
    python -m venv venv # Create a virtual environment
    source venv/bin/activate # On Windows use `venv\Scripts\activate`
    pip install -r requirements.txt
    python agent.py start # production
    ```

### Configuration

*   **(Frontend)**: You need to create a `.env` file in `CulinaryVertexFrontend` for environment-specific variables (e.g., API endpoints). Check `CulinaryVertexFrontend/app/api/connection-details/route.ts` or component fetching data for required variables.
*   **(Backend)**: Check `CulinaryVertexBackend/agent.py` or other backend files for any required environment variables (e.g., API keys for AI services, database connection strings). Set these variables in your environment or a `.env` file recognized by the backend framework.
