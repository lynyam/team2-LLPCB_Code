chrome.runtime.onInstalled.addListener(() => {
  chrome.sidePanel.setPanelBehavior({ openPanelOnActionClick: true });
});

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.request === "url") {
    (async () => {
      const [tab] = await chrome.tabs.query({ active: true });
      sendResponse({ url: tab.url });
    })();
  }

  return true;
});
