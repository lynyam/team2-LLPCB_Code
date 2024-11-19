# gcpu-hackathon-2024
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

