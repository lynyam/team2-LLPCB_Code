import { Button, Stack, Text } from "@mantine/core";
import { useState } from "react";
import { Analysis } from "./Analysis";

function SidePanel() {
  const [data, setData] = useState();
  const [loading, setLoading] = useState(false);

  const handleClick = () => {
    setLoading(true);
    chrome.runtime
      .sendMessage({
        request: "url",
      })
      .then((response: any) => {
        setData(response);
        setLoading(false);
      });
  };

  return (
    <Stack p={10}>
      <Button onClick={handleClick} loading={loading}>
        Analyze
      </Button>
      {data && <Analysis content={data} />}
    </Stack>
  );
}

export default SidePanel;
