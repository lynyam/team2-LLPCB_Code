import {
  Accordion,
  Badge,
  Blockquote,
  Divider,
  Group,
  Paper,
  Spoiler,
  Stack,
  Text,
  Title,
} from "@mantine/core";
import { ApiArticlesProcessResponseDto } from "../../../types/api_articles_process.response.dto";
import { snakeToProper } from "../../functions/snakeToProper";
import { HelpHover } from "../shared/HelpHover";

interface Props {
  argument: ApiArticlesProcessResponseDto["arguments"][number];
}

export const Argument = ({ argument }: Props) => {
  const numberOfManipulations = Object.values(argument.manipulations).reduce(
    (acc, curr) => acc + curr.length,
    0
  );

  return (
    <Paper shadow="sm" p="lg">
      <Stack>
        <Accordion>
          <Accordion.Item key="default" value="default">
            <Accordion.Control>
              <Title size="md">{argument.statement}</Title>
              <Text>{`Connection to hypothesis: ${argument.connection_to_hypothesis}`}</Text>
              <Text>{`Number of manipulations: ${numberOfManipulations}`}</Text>
            </Accordion.Control>
            <Accordion.Panel>
              {numberOfManipulations === 0 ? (
                <Text>
                  No manipulation detected in this argument. It appears to have
                  been presented in a clear and logical manner. 😊
                </Text>
              ) : (
                <Stack>
                  {Object.entries(argument.manipulations).map(
                    ([key, value], index) => {
                      if (value.length === 0) {
                        return null;
                      }
                      return (
                        <Stack key={key}>
                          {index !== 0 && <Divider />}
                          <Group>
                            <Text fw="bold">{`${snakeToProper(key)}: ${
                              value.length
                            }`}</Text>
                            <HelpHover _key={key} />
                          </Group>

                          {value.map((manipulation, index) => {
                            return (
                              <Group key={index}>
                                <Blockquote p="xs">
                                  {manipulation.instance}
                                </Blockquote>
                                <Text>{manipulation.explanation}</Text>
                              </Group>
                            );
                          })}
                        </Stack>
                      );
                    }
                  )}
                </Stack>
              )}
            </Accordion.Panel>
          </Accordion.Item>
        </Accordion>
      </Stack>
    </Paper>
  );
};
