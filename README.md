# gcpu-hackathon-2024

# **Project Description**
The **GCPU Hackathon 2024** project aims to develop an innovative solution for analyzing online articles to extract rhetorical structure and arguments. Its primary goal is to enhance critical thinking by providing users with a clear understanding of the premises, arguments, and conclusions of a text while validating the logical coherence of the presented information.

### **Project Objectives**:
- Enable users to analyze an online article with a single click.
- Provide feedback on the argumentative logic of the article.
- Assist in verifying the validity of the arguments presented in the text.

The project comprises two main components:
1. **Frontend (React Extension)**: Allows users to submit an article for analysis with a single click on the extension. The frontend sends the article's URL to the backend for processing.
2. **Backend (API Gateway in Java)**: Manages calls to specialized services, including a Python service for analyzing the article's text and calculating a fallacy score using advanced AI tools like **Gemini-1.5-Pro and LangChain**.

---

## **Technical Documentation**

### **System Architecture**

The system is divided into several key components that interact to perform article analysis:

#### 1. **Frontend (React Extension with Mantine)**
The extension is built using **React** and **Mantine** for a modern and responsive design. Key functionalities include:
- Provides a simple interface for users to initiate article analysis.
- Capturing the URL of the page currently viewed by the user.
- Provides a simple interface for users to initiate article analysis.
- Displaying analysis results in a clear and user-friendly interface.

#### 2. **Backend (Java API Gateway)**
The backend is an API Gateway developed in **Java**, orchestrating calls to specialized services. Built with **Spring Boot**, its main responsibilities are:
- Central coordinator of the architecture.
- Routes requests between the frontend and backend services.
- Calling the **RetrieveTextService** to extract raw text from the provided URL using **Jsoup** (to fetch and parse the article text).
- Sending the extracted text to the **RhetoricDetectionService** for rhetorical analysis. Handles integration between the Java services and the Python service using RESTful APIs.
- Returning the final results to the frontend as a structured JSON.

#### 3. **RetrieveTextService (Java with Jsoup)**
This service is responsible for extracting raw content from online articles. It leverages **Jsoup**, a powerful Java library, to:
- Load the URL and parse the HTML DOM.
- Extract text while filtering out ads and unnecessary elements.

#### 4. **RhetoricDetectionService (Python with FastAPI)**
This Python service is accessible via **FastAPI** and performs advanced rhetorical analysis using:
- **Gemini-1.5-Pro**: An advanced AI model for text analysis.
- **LangChain**: A framework used to orchestrate AI agents for identifying premises, arguments, and conclusions.
- Returns a detailed JSON response containing detected premises, conclusions, and argument scores.


The project is fully containerized to ensure seamless deployment and scalability. Below are the steps to set up the Dockerized environment.


# **Steps to Launch the Project**

## **Prerequisites**
1. **Install Docker and Docker Compose**:
   - Download and install Docker Desktop or Docker Engine from [Docker's official site](https://www.docker.com/).
   - Ensure Docker Compose is included (it is usually part of most Docker installations).

2. **Verify Installation**:
   - Open a terminal and run:
     ```bash
     docker --version
     docker-compose --version
     ```
   - These commands should display the installed versions of Docker and Docker Compose.
  
Before you begin, ensure you have the following installed on your machine:

- **Node.js** (including `npm`)
  - You can download it from [Node.js official website](https://nodejs.org/).

---

## **Start the Services**

### ** 1. Build dependencies **

1. Navigate to directory ```frontend``` and run:
  - ```bash
    npm install
    npm run build
    ```
### **2. Add the extension to your chromium browser**

#### **1. Enable Developer Mode in Chrome**
1. Open Chrome.
2. Go to the **Extensions** page:
   - Enter `chrome://extensions` in the address bar, or
   - Navigate via **Menu** → **More tools** → **Extensions**.
3. Enable **Developer mode** using the toggle switch in the top-right corner.

---

#### **2. Load Your Extension**
1. On the **Extensions** page, click the **Load unpacked** button.
2. A file dialog will appear. Navigate to the folder `frontend/dist` and select it.
3. Click **Select Folder** (or equivalent on your OS).


---

#### **3. (Optional). Pin the Extension to the Toolbar**
1. Look for the **Extensions** icon (puzzle piece) in the Chrome toolbar (top-right corner).
2. Click it to open the dropdown menu.
3. Locate your extension in the list and click the **pin icon** next to it.
4. The extension’s icon will now appear in the toolbar for easy access.

#### **4. Locate the Extension ID**:
   - Once the extension is loaded, it will appear on the extensions page.
   - Look for the **ID** field under the extension's details.

#### **5. Copy the Extension ID**:
   - Highlight the ID string.
   - Right-click and select **Copy**, or use `Ctrl+C` (Windows/Linux) or `Cmd+C` (Mac).

#### **6. Paste the ExtensionID**:
   - Paste extension id in .env file next to `ALLOWED_CHROME_EXTENSION_IDS=`


### 3. Run the project
####**1. Run docker compose**:
   - Use the following command to build and start the services:
     ```bash
     docker-compose up --build
     ```
---
---

## **Structure du Projet**

### **Frontend (Extension React)**
- **`frontend/`** :
  - **`dist/`** : Contient le dossier généré pour l'extension Chrome.
  - **`src/`** : Code source de l'extension React.
  - **`public/`** : Contient les fichiers statiques comme les images et les icônes.

### **Backend (API Gateway en Java)**
- **`apigateway/`** :
  - **`src/`** : Contient le code Java du backend.
  - **`docker/`** : Contient les fichiers Docker pour le backend.
  - **`pom.xml`** : Configuration Maven du backend.

### **Services Python**
- **`python-services/`** :
  - **`rhetoric-analysis/`** : Service qui analyse la rhétorique de l'article, utilise Gemini-1.5-Pro et LangChain.

---

## **Future Improvements**

- **Enhanced Python Services**: Introduce additional analyses, such as identifying cognitive biases.  
- **Improved UI**: Develop visualizations, like graphs, to display argumentative relationships clearly.  
- **Extended Java Services**: Add new services to further refine and detail the responses provided by the LLM.  

---

