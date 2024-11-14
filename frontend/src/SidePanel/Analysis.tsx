import { Button, Stack, Text } from "@mantine/core";
import "../../styles/analysis.css";
import { DelayedTextDisplay } from "./DelayedTextDisplay";

interface Props {
  content: any;
}

export const Analysis = ({ content }: Props) => {
  const handleClick = () => {
    chrome.tabs.create({
      url: "index.html#tab",
    });
  };

  return (
    <Stack>
      <DelayedTextDisplay text={"Analysis"} />
      <Button variant="subtle" onClick={handleClick}>
        Dig deeper
      </Button>
    </Stack>
  );
};
