import { GoogleGenerativeAI } from "./node_modules/@google/generative-ai/dist/index.mjs";
const genAI = new GoogleGenerativeAI("AIzaSyBoaHgH2fhKTtuHloOHqHP8Qsbjfbvgysg");
const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });

const button = document.getElementById("mybutton");
button.addEventListener("click", async () => {
  const [tab] = await chrome.tabs.query({ active: true });
  const response = await chrome.tabs.sendMessage(tab.id, { greeting: "hello" });
  alert("analyzing...");

  const prompt = `Parse the following html page and return the article within this page in the form of a text:${response.body}`;

  const result = await model.generateContent(prompt);
  alert(result.response.text());
  const element = document.getElementById("response");
  const textNode = document.createTextNode(result.response.text());
  element.appendChild(textNode);
});
