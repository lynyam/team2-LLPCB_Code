import { Accordion, Stack, Text } from "@mantine/core";
import { ApiArticlesProcessResponseDto } from "../../../types/api_articles_process.response.dto";
import { snakeToProper } from "../../functions/snakeToProper";
import { ManipulationTypeSummary } from "./ManipulationTypeSummary";

interface Props {
  argument: ApiArticlesProcessResponseDto["arguments"][number];
}

export const ArgumentSummary = ({ argument }: Props) => {
  const numberOfManipulations = Object.values(argument.manipulations).reduce(
    (acc, curr) => acc + curr.length,
    0
  );
  return (
    <Accordion.Item key={argument.statement} value={argument.statement}>
      <Accordion.Control>
        <Stack>
          <Text>{argument.statement}</Text>
          <Text>{`Number of Manipulations: ${numberOfManipulations}`}</Text>
        </Stack>
      </Accordion.Control>
      <Accordion.Panel>
        {numberOfManipulations === 0 ? (
          <Text>
            No manipulation detected in this argument. It appears to have been
            presented in a clear and logical manner. 😊
          </Text>
        ) : (
          <Accordion>
            {Object.entries(argument.manipulations).map(([key, value]) => {
              const amount = value.length;
              if (amount === 0) {
                return null;
              }
              return (
                <ManipulationTypeSummary
                  _key={key}
                  key={key}
                  manipulations={value}
                />
              );
            })}
          </Accordion>
        )}
      </Accordion.Panel>
    </Accordion.Item>
  );
};
