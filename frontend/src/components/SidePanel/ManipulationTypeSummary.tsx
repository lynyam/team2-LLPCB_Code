import { ApiArticlesProcessResponseDto } from "../../../types/api_articles_process.response.dto";
import { Accordion, Blockquote, Group, Stack, Text } from "@mantine/core";
import { snakeToProper } from "../../functions/snakeToProper";
import { HelpHover } from "../shared/HelpHover";
import {
  ArrowsJoin,
  Box,
  BoxMultiple,
  Certificate,
  ChartBar,
  ChartDots,
  Crown,
  SwitchHorizontal,
  Target,
  Users,
} from "tabler-icons-react";
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
          {ManipulationIcons[_key as keyof typeof ManipulationIcons]}
          <Text>{`${snakeToProper(_key)}: ${amount}`}</Text>
          <HelpHover _key={_key} />
        </Group>
      </Accordion.Control>
      <Accordion.Panel>
        {manipulations.map((manipulation, index) => {
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

export const ManipulationIcons = {
  ad_populum: <Users />,
  unspecified_authority_fallacy: <Certificate />,
  appeal_to_pride: <Crown />,
  false_dilemma: <SwitchHorizontal />,
  cherry_picking_data: <ChartDots />,
  stork_fallacy: <ArrowsJoin />,
  fallacy_of_composition: <BoxMultiple />,
  fallacy_of_division: <Box />,
  hasty_generalization: <ChartBar />,
  texas_sharpshooter_fallacy: <Target />,
};
