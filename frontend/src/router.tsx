import {
  createBrowserRouter,
  createHashRouter,
  createMemoryRouter,
} from "react-router-dom";
import SidePanel from "./SidePanel/SidePanel";
import { Tab } from "./Tab/Tab";

// const [tab] = await chrome.tabs.query({ active: true });
// const id = `${tab.id}`;

// console.log(id);

export const router = createHashRouter(
  [
    {
      path: "/",
      element: <SidePanel />,
    },
    {
      path: "tab",
      element: <Tab />,
    },
  ],
  {
    future: {
      v7_relativeSplatPath: true,
      v7_fetcherPersist: true,
      v7_normalizeFormMethod: true,
      v7_partialHydration: true,
      v7_skipActionErrorRevalidation: true,
    },
  }
);
