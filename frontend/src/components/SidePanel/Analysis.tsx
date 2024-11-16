import { Accordion, Button, Divider, Stack, Text, Title } from "@mantine/core";
import { ApiArticlesProcessResponseDto } from "../../../types/api_articles_process.response.dto";
import { ArgumentSummary } from "./ArgumentSummary";
import { Shovel } from "tabler-icons-react";

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
      <Title
        size="lg"
        style={{
          textAlign: "center",
        }}
      >{`${content.thesis}`}</Title>
      <Divider />
      <Text>{`Arguments (${content.arguments.length}):`}</Text>
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
