import { Text } from "@mantine/core";
import { useInterval } from "@mantine/hooks";

import { useEffect, useState } from "react";

interface Props {
  text: string;
}

export const DelayedTextDisplay = ({ text }: Props) => {
  const [value, setValue] = useState("");
  const [index, setIndex] = useState(0);

  const interval = useInterval(() => {
    setValue(value + text[index]);
    setIndex(index + 1);
  }, 10);

  useEffect(() => {
    interval.start();

    if (index >= text.length) {
      interval.stop();
    }
  }, [index]);

  return (
    <Text
      style={{
        textWrap: "wrap",
        wordBreak: "break-word",
      }}
    >
      {value}
    </Text>
  );
};
