import { Button, Overlay, Stack, Text } from "@mantine/core";
import { useEffect, useState } from "react";
import { Analysis } from "./Analysis";
import { Analyze } from "tabler-icons-react";

import { useLocalStorage } from "@mantine/hooks";
import { ApiArticlesProcessResponseDto } from "../../../types/api_articles_process.response.dto";

function SidePanel() {
  const [loading, setLoading] = useState(false);
  const [isError, setIsError] = useState(false);

  const [content, setContent] = useLocalStorage<
    ApiArticlesProcessResponseDto | undefined
  >({
    key: "content",
    defaultValue: undefined,
  });

  useEffect(() => {
    setContent(undefined);
  }, []);

  const handleClick = () => {
    setLoading(true);
    setIsError(false);
    setContent(undefined);
    chrome.runtime
      .sendMessage({
        request: "url",
      })
      .then((response: any) => {
        setContent(response);
        setLoading(false);
      })
      .catch((error: any) => {
        setIsError(true);
        setLoading(false);
      });
  };

  return (
    <Stack p={10}>
      <Button
        onClick={handleClick}
        loading={loading}
        rightSection={<Analyze />}
      >
        Analyze
      </Button>
      {isError && <Text>An error occured, please try again</Text>}
      {content && <Analysis content={content} />}
    </Stack>
  );
}

export default SidePanel;
