import {
  Box,
  Button,
  Group,
  LoadingOverlay,
  Overlay,
  Stack,
  Text,
} from "@mantine/core";
import { useEffect, useState } from "react";
import { Analysis } from "./Analysis";
import { Analyze, Container } from "tabler-icons-react";

import { useLocalStorage } from "@mantine/hooks";
import { ApiArticlesProcessResponseDto } from "../../../types/api_articles_process.response.dto";

function SidePanel() {
  const [loading, setLoading] = useState(false);
  const [isError, setIsError] = useState(false);

  const [content, setContent] = useLocalStorage<
    ApiArticlesProcessResponseDto | "undefined"
  >({
    key: "content",
    defaultValue: "undefined",
  });

  const handleClick = () => {
    setLoading(true);
    setIsError(false);
    setContent("undefined");
    chrome.runtime
      .sendMessage({
        request: "url",
      })
      .then((response: ApiArticlesProcessResponseDto) => {
        const orderedArguments = response?.arguments.sort((a, b) => {
          const lenManA = Object.values(a.manipulations).reduce(
            (acc, curr) => acc + curr.length,
            0
          );
          const lenManB = Object.values(b.manipulations).reduce(
            (acc, curr) => acc + curr.length,
            0
          );
          if (lenManA > lenManB) {
            return -1;
          }
          if (lenManA < lenManB) {
            return 1;
          }
          return 0;
        });

        setContent({
          ...response,
          arguments: orderedArguments,
        });
        setLoading(false);
      })
      .catch((error: any) => {
        setIsError(true);
        setLoading(false);
      });
  };

  return (
    <Stack>
      <Stack p={10}>
        <Button onClick={handleClick} loading={loading}>
          Analyze
        </Button>
        {isError && <Text>An error occured, please try again</Text>}
        {content && content !== "undefined" && <Analysis content={content} />}
      </Stack>
    </Stack>
  );
}

export default SidePanel;
