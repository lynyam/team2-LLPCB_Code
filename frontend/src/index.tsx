import React from "react";
import { MemoryRouter, Route, RouterProvider, Routes } from "react-router-dom";

import ReactDOM from "react-dom/client";
import { MantineProvider } from "@mantine/core";
import "@mantine/core/styles.css";
import { router } from "./router";

const root = document.createElement("div");
root.className = "container";
document.body.appendChild(root);
const rootDiv = ReactDOM.createRoot(root);
rootDiv.render(
  <React.StrictMode>
    <MantineProvider>
      <RouterProvider
        future={{
          v7_startTransition: true,
        }}
        router={router}
      />
    </MantineProvider>
  </React.StrictMode>
);
