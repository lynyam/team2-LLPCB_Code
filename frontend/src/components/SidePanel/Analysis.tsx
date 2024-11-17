import {
  Accordion,
  Button,
  Divider,
  Group,
  RingProgress,
  Stack,
  Text,
  Title,
} from "@mantine/core";
import { ApiArticlesProcessResponseDto } from "../../../types/api_articles_process.response.dto";
import { ArgumentSummary } from "./ArgumentSummary";
import { Shovel } from "tabler-icons-react";
import { ScoreDetails } from "./ScoreDetails";

interface Props {
  content: ApiArticlesProcessResponseDto;
}

export const Analysis = ({ content }: Props) => {
  const handleClick = () => {
    chrome.tabs.create({
      url: "index.html#tab",
    });
  };

  return (
    <Stack>
      <ScoreDetails scoreDetails={content.score} />
      <Divider />
      <Group gap={2}>
        <Text size="xl" fw="bold">
          Main thesis:{" "}
        </Text>
        <Text size="xl">{content.thesis}</Text>
      </Group>
      <Divider />
      <Title size="md">{`Number of Arguments: ${content.arguments.length}`}</Title>
      <Accordion>
        {content.arguments.map((argument, index) => (
          <ArgumentSummary key={index} argument={argument} />
        ))}
      </Accordion>

      <Button onClick={handleClick} variant="outline" rightSection={<Shovel />}>
        Dig deeper
      </Button>
    </Stack>
  );
};
