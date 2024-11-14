import axios from "axios";

chrome.runtime.onInstalled.addListener(() => {
  chrome.sidePanel.setPanelBehavior({ openPanelOnActionClick: true });
});

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.request === "url") {
    (async () => {
      const [tab] = await chrome.tabs.query({ active: true });

      const response = await axios.post(
        "http://localhost:8080/api/articles/process",
        {
          url: tab.url,
        }
      );
      sendResponse(response.data);
    })();
  }

  return true;
});

export {};
