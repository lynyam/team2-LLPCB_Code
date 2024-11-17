import { HoverCard, Tooltip, Text, Button } from "@mantine/core";
import { Help } from "tabler-icons-react";

const explanations = {
  ad_populum:
    "A fallacious argument which is based on claiming a truth or affirming something is good or correct because many people think so.",
  unspecified_authority_fallacy:
    "Unspecified authority fallacy is a fallacy that occurs when the authority in question is not named or specified.",
  appeal_to_pride:
    "Appeal to pride is a fallacy that occurs when someone's pride is used to convince them of something.",
  false_dilemma:
    "A false dilemma is a type of informal fallacy in which something is falsely claimed to be an 'either/or' situation, when in fact there is at least one additional option.",
  cherry_picking_data:
    "Cherry picking, suppressing evidence, or the fallacy of incomplete evidence is the act of pointing to individual cases or data that seem to confirm a particular position while ignoring a significant portion of related and similar cases or data that may contradict that position.",
  stork_fallacy:
    "The stork fallacy is a logical fallacy that occurs when two events that occur together are assumed to have a cause-and-effect relationship.",
  fallacy_of_composition:
    "The fallacy of composition arises when one infers that something is true of the whole from the fact that it is true of some part of the whole (or even of every proper part).",
  fallacy_of_division:
    "The fallacy of division is the opposite of the fallacy of composition. It is the fallacy of inferring from the fact that some whole has a property to the conclusion that every part of the whole has that property.",
  hasty_generalization:
    "Hasty generalization is an informal fallacy of faulty generalization by reaching an inductive generalization based on insufficient evidence—essentially making a rushed conclusion without considering all of the variables.",
  texas_sharpshooter_fallacy:
    "An informal fallacy which is committed when differences in data are ignored, but similarities are overemphasized.",
};
type Props = {
  _key: string;
};
export const HelpHover = ({ _key }: Props) => (
  <Tooltip label={explanations[_key as keyof typeof explanations]}>
    <Text>
      <Help color="gray" height={15} />
    </Text>
  </Tooltip>
);
