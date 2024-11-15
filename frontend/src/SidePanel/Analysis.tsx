import { Badge, Button, Grid, Group, Stack, Text } from "@mantine/core";
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
  const title = `Main thesis: ${content.thesis}`;
  const foundArguments = `Found ${content.arguments.length} arguments`;

  return (
    <Stack>
      <DelayedTextDisplay text={title} />
      <DelayedTextDisplay text={foundArguments} />
      {content.arguments.map((argument, index) => {
        const numberOfManipulations = Object.values(
          argument.manipulations
        ).reduce((acc, curr) => acc + curr.length, 0);
        return (
          <Group key={index}>
            <Text>{argument.statement}</Text>
            {numberOfManipulations && <Badge>{numberOfManipulations}</Badge>}
          </Group>
        );
      })}

      <Button variant="subtle" onClick={handleClick}>
        Dig deeper
      </Button>
    </Stack>
  );
};
