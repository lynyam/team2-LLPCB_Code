import { ApiArticlesProcessResponseDto } from "../../../types/api_articles_process.response.dto";
import { Accordion, Blockquote, Group, Stack, Text } from "@mantine/core";
import { snakeToProper } from "../../functions/snakeToProper";
import { HelpHover } from "../shared/HelpHover";
interface Props {
  _key: string;
  manipulations: ApiArticlesProcessResponseDto["arguments"][number]["manipulations"][keyof ApiArticlesProcessResponseDto["arguments"][number]["manipulations"]];
}

export const ManipulationTypeSummary = ({ _key, manipulations }: Props) => {
  const amount = manipulations.length;
  if (manipulations.length === 0) {
    return null;
  }

  return (
    <Accordion.Item key={_key} value={_key}>
      <Accordion.Control>
        <Group>
          <Text>{`${snakeToProper(_key)}: ${amount}`}</Text>
          <HelpHover _key={_key} />
        </Group>
      </Accordion.Control>
      <Accordion.Panel>
        {manipulations.map((manipulation, index) => {
          console.log("manipulation", manipulation);
          return (
            <Group key={index}>
              <Blockquote p="xs">{manipulation.instance}</Blockquote>
              <Text>{manipulation.explanation}</Text>
            </Group>
          );
        })}
      </Accordion.Panel>
    </Accordion.Item>
  );
};
