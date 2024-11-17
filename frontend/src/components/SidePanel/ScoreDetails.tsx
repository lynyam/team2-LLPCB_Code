import { Group, RingProgress, Text } from "@mantine/core";
import { ApiArticlesProcessResponseDto } from "../../../types/api_articles_process.response.dto";

interface Props {
  scoreDetails: ApiArticlesProcessResponseDto["score"];
}

export const ScoreDetails = ({ scoreDetails }: Props) => {
  const overall_score = +scoreDetails.overall_score;
  const color =
    overall_score > 75 ? "red" : overall_score > 25 ? "yellow" : "green";
  return (
    <Group>
      <RingProgress
        sections={[{ value: overall_score, color }]}
        label={
          <Text fw={700} ta="center" size="xl">
            {`${overall_score}`}
          </Text>
        }
      />
      <Text>{scoreDetails.interpretation}</Text>
    </Group>
  );
};
