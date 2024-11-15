import { Badge, Group, Stack, Text } from "@mantine/core";
import { ApiArticlesProcessResponseDto } from "../../types/api_articles_process.response.dto";

interface Props {
  content: ApiArticlesProcessResponseDto;
}

export const Tab = ({ content }: Props) => {
  return (
    <Stack p={10}>
      <Text>{`Main thesis ${content.thesis}`}</Text>
      <Group>
        <Text>Arguments</Text>
        <Badge>{content.arguments.length}</Badge>
      </Group>
      {content.arguments.map((argument, index) => {
        const numberOfManipulations = Object.values(
          argument.manipulations
        ).reduce((acc, curr) => acc + curr.length, 0);
        return (
          <Stack key={index}>
            <Group>
              <Text>{argument.statement}</Text>
              <Badge>{argument.type}</Badge>
              <Badge>{numberOfManipulations}</Badge>
            </Group>
            <Text>{`Connection to hypothesis: ${argument.connection_to_hypothesis}`}</Text>
            {Object.entries(argument.manipulations).map(([key, value]) => {
              if (value.length === 0) {
                return (
                  <Text key={key}>No manipulation found for this argument</Text>
                );
              }
              return (
                <Stack key={key}>
                  <Text>{key}</Text>
                  {value.map((manipulation, index) => {
                    return (
                      <Group key={index}>
                        <Text>{manipulation.instance}</Text>
                        <Text>{manipulation.explanation}</Text>
                      </Group>
                    );
                  })}
                </Stack>
              );
            })}
          </Stack>
        );
      })}
      s
    </Stack>
  );
};
