import { sleep, getElementById } from "./utils";

const button = getElementById("activate");
button.addEventListener("click", async () => {
  const loader = getElementById("loader");
  loader.classList.add("loader");

  await sleep(1000);

  const { url } = await chrome.runtime.sendMessage({ request: "url" });

  loader.classList.remove("loader");

  const element = getElementById("url");
  element.innerText = url;
});
