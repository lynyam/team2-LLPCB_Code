import { Button, Stack, Text } from "@mantine/core";
import { useState } from "react";
import { Analysis } from "./Analysis";

function SidePanel() {
  const [data, setData] = useState();
  const [loading, setLoading] = useState(false);
  const [isError, setIsError] = useState(false);

  const handleClick = () => {
    setLoading(true);
    setIsError(false);
    chrome.runtime
      .sendMessage({
        request: "url",
      })
      .then((response: any) => {
        setData(response);
        setLoading(false);
      })
      .catch((error: any) => {
        setIsError(true);
        setLoading(false);
      });
  };

  return (
    <Stack p={10}>
      <Button onClick={handleClick} loading={loading}>
        Analyze
      </Button>
      {isError && <Text>An error occured, please try again</Text>}
      {data && <Analysis content={data} />}
    </Stack>
  );
}

export default SidePanel;
