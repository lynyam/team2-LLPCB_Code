import axios from "axios";
// import { testApiArticlesProcessResponseDto } from "./test";

chrome.runtime.onInstalled.addListener(() => {
  chrome.sidePanel.setPanelBehavior({ openPanelOnActionClick: true });
});

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.request === "url") {
    (async () => {
      const [tab] = await chrome.tabs.query({ active: true });
      try {
        const response = await axios.post(
          "http://localhost:8080/api/articles/process",
          {
            url: tab.url,
          }
        );
        sendResponse(response.data);
      } catch (error) {
        sendResponse(error);
      }
      // sendResponse(testApiArticlesProcessResponseDto);
    })();
  }

  return true;
});

export {};
