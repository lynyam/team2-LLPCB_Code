const button = document.getElementById("mybutton");
button.addEventListener("click", async () => {
  const [tab] = await chrome.tabs.query({ active: true });
  const response = await chrome.tabs.sendMessage(tab.id, { greeting: "hello" });
  alert(response.body);
  console.log(response.body);
});
