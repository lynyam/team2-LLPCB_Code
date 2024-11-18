import { Group, RingProgress, Stack, Text } from "@mantine/core";
import { ApiArticlesProcessResponseDto } from "../../../types/api_articles_process.response.dto";

interface Props {
  scoreDetails: ApiArticlesProcessResponseDto["score"];
}

export const ScoreDetails = ({ scoreDetails }: Props) => {
  const overall_score = +scoreDetails.overall_score;
  const color =
    overall_score > 75 ? "red" : overall_score > 25 ? "yellow" : "green";
  return (
    <Group wrap="nowrap">
      <Stack gap={2} align="center">
        <Text size="lg">Score</Text>
        <RingProgress
          sections={[{ value: overall_score, color }]}
          label={
            <Text fw={700} ta="center" size="xl">
              {`${overall_score}`}
            </Text>
          }
        />
      </Stack>
      <Text>{`The score of ${overall_score} means that ${
        scoreDetails.interpretation[0].toLowerCase() +
        scoreDetails.interpretation.slice(1)
      }`}</Text>
    </Group>
  );
};
