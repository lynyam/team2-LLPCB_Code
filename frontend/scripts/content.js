chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
  console.log(
    sender.tab
      ? "from a content script:" + sender.tab.url
      : "from the extension"
  );
  const main = document.body;
  if (request.greeting === "hello") sendResponse({ body: main.innerText });
});
