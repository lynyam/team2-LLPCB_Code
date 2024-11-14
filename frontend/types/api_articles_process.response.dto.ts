type manipulation_type = {
  primary: string;
  secondary: string;
};

type instance = {
  phrase: string;
  manipulationtype: manipulation_type;
  explanation: string;
};

export type ApiArticlesProcessResponseDto = {
  instances: instance[];
};
