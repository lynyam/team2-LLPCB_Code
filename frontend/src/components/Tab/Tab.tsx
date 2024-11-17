import { Badge, Divider, Group, Stack, Text, Title } from "@mantine/core";
import { useLocalStorage } from "@mantine/hooks";
import { ApiArticlesProcessResponseDto } from "../../../types/api_articles_process.response.dto";
import { Argument } from "./Argument";

export const Tab = () => {
  const [content, setContent] = useLocalStorage<ApiArticlesProcessResponseDto>({
    key: "content",
    defaultValue: undefined,
  });
  if (!content) {
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
      <Title size="md">{`Arguments: ${content.arguments.length}`}</Title>
      {content.arguments.map((argument, index) => (
        <Argument key={index} argument={argument} />
      ))}
    </Stack>
  );
};