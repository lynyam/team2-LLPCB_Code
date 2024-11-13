import { Button, Stack, Text } from "@mantine/core";
import { useState } from "react";
import { Analysis } from "./Analysis";
import { useLocation } from "react-router-dom";

function SidePanel() {
  const [url, setUrl] = useState();

  const location = useLocation();

  console.log(location);

  const handleClick = () => {
    chrome.runtime
      .sendMessage({
        request: "url",
      })
      .then((response) => {
        const { url } = response;
        setUrl(url);
      });
  };

  return (
    <Stack p={10}>
      <Button onClick={handleClick}>Analyze</Button>
      {url && <Analysis content={url} />}
    </Stack>
  );
}

export default SidePanel;
