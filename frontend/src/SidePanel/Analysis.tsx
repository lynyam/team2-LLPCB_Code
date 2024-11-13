import { Button, Stack, Text } from "@mantine/core";
import "../../styles/analysis.css";
import { useDebouncedState, useInterval } from "@mantine/hooks";
import { useEffect, useState } from "react";

interface Props {
  content: string;
}

export const Analysis = ({ content }: Props) => {
  const handleClick = () => {
    chrome.tabs.create({
      url: "index.html#tab",
    });
  };

  const [value, setValue] = useState("");
  const [index, setIndex] = useState(0);

  const interval = useInterval(() => {
    setValue(value + content[index]);
    setIndex(index + 1);
  }, 10);

  useEffect(() => {
    interval.start();

    if (index >= content.length) {
      interval.stop();
    }
  }, [index]);

  return (
    <Stack>
      <Text
        style={{
          textWrap: "wrap",
          wordBreak: "break-word",
        }}
      >
        Analysis of {value}
      </Text>
      <Button variant="subtle" onClick={handleClick}>
        Dig deeper
      </Button>
    </Stack>
  );
};
