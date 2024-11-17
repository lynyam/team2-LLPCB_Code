import { Badge, Divider, Group, Stack, Text, Title } from "@mantine/core";
import { useLocalStorage } from "@mantine/hooks";
import { ApiArticlesProcessResponseDto } from "../../../types/api_articles_process.response.dto";
import { Argument } from "./Argument";
import { ScoreDetails } from "../SidePanel/ScoreDetails";

export const Tab = () => {
  const [content, setContent] = useLocalStorage<
    ApiArticlesProcessResponseDto | "undefined"
  >({
    key: "content",
    defaultValue: "undefined",
  });
  if (!content || content === "undefined") {
    return <Text>No content found</Text>;
  }

  return (
    <Stack p={10}>
      <Title
        size="xl"
        style={{
          textAlign: "center",
        }}
      >{`${content.thesis}`}</Title>
      <Divider />
      <ScoreDetails scoreDetails={content.score} />
      <Title size="lg">{`Number of Arguments: ${content.arguments.length}`}</Title>
      {content.arguments.map((argument, index) => (
        <Argument key={index} argument={argument} />
      ))}
    </Stack>
  );
};
