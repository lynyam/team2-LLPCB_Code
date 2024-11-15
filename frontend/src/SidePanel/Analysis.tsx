import { Button, Stack, Text } from "@mantine/core";
import "../../styles/analysis.css";
import { DelayedTextDisplay } from "./DelayedTextDisplay";
import { ApiArticlesProcessResponseDto } from "../../types/api_articles_process.response.dto";

interface Props {
  content: ApiArticlesProcessResponseDto;
}

export const Analysis = ({ content }: Props) => {
  const handleClick = () => {
    chrome.tabs.create({
      url: "index.html#tab",
    });
  };
  const title = `{Main thesis: ${content.thesis}`;

  return (
    <Stack>
      <DelayedTextDisplay text={title} />
      <Button variant="subtle" onClick={handleClick}>
        Dig deeper
      </Button>
    </Stack>
  );
};
