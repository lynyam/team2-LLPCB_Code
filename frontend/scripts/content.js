chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
  const main = document.body;
  if (request.greeting === "hello") sendResponse({ body: main.innerText });
});
