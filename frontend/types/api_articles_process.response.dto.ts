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

type MetricsExplanation = {
  manipulation_density: string;
  affected_arguments_ratio: string;
  average_techniques_per_argument: string;
  max_techniques_in_single_argument: string;
};

type ScoreDetails = {
  overall_score: string;
  manipulation_density: string;
  affected_arguments_ratio: string;
  average_techniques_per_argument: string;
  max_techniques_in_single_argument: string;
  risk_level: string;
  interpretation: string;
  metrics_explanation: MetricsExplanation;
};

export type ApiArticlesProcessResponseDto = {
  thesis: string;
  arguments: Argument[];
  score: ScoreDetails;
};
