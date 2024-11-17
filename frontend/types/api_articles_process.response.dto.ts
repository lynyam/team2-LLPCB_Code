type Argument = {
  _type: string;
  statement: string;
  connection_to_hypothesis: string;
  manipulations: {
    ad_populum: Manipulation[];
    unspecified_authority_fallacy: Manipulation[];
    appeal_to_pride: Manipulation[];
    false_dilemma: Manipulation[];
    cherry_picking_data: Manipulation[];
    stork_fallacy: Manipulation[];
    fallacy_of_composition: Manipulation[];
    fallacy_of_division: Manipulation[];
    hasty_generalization: Manipulation[];
    texas_sharpshooter_fallacy: Manipulation[];
  };
};

type Manipulation = {
  instance: string;
  explanation: string;
};

export type ApiArticlesProcessResponseDto = {
  thesis: string;
  arguments: Argument[];
};
