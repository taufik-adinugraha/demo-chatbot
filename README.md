## ChatBot Project with FastAPI and Streamlit

This project consists of a FastAPI backend and a Streamlit frontend, both running in Docker containers. Follow the steps below to set up the environment.

### Prerequisites

- [Docker](https://www.docker.com/) installed on your machine.

### Steps to Set Up the Environment

#### 1. Build Docker Images

Navigate to the directory where your Dockerfiles are located and build the images for both FastAPI and Streamlit:

```bash
# Build FastAPI image
sudo docker build -t chat_fastapi ./fastapi

# Build Streamlit image
sudo docker build -t chat_streamlit ./streamlit
```

#### 2. Create a Docker Network

```bash
sudo docker network create mynetwork
```

#### 3. Prepare .env File

Create a `.env` file in the `fastapi` directory containing your OpenAI API Key:

```env
MY_OPENAI_API_KEY=your_openai_api_key_here
DB=clickhouse
```

You can use the `cat` command to create the `.env` file:

```bash
cat > ./fastapi/.env <<EOL
MY_OPENAI_API_KEY=your_openai_api_key_here
DB=clickhouse
EOL
```

Create a `.env` file in the `streamlit` directory containing url to fastapi:

```bash
cat > ./streamlit/.env <<EOL
backend_url=http://chat_fastapi:8080
EOL
```

#### 4. Run FastAPI Container

```bash
# Run FastAPI container with .env file
sudo docker run -d --network=mynetwork --name chat_fastapi --env-file ./fastapi/.env -p 8080:8080 chat_fastapi
```

#### 5. Run Streamlit container

```bash
sudo docker run -d --network=mynetwork --name chat_streamlit --env-file ./streamlit/.env -p 8501:8501 chat_streamlit
```
