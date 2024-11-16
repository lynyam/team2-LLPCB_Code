import { MantineProvider } from "@mantine/core";
import { RouterProvider } from "react-router-dom";
import { router } from "./router";

import newspaperTheme from "./theme";

export const App = () => {
  return (
    <MantineProvider theme={newspaperTheme}>
      <RouterProvider
        future={{
          v7_startTransition: true,
        }}
        router={router}
      />
    </MantineProvider>
  );
};
