from logger import get_logger

log = get_logger()

def get_score_details(text_analysis: dict) -> dict:
   manipulation_score = calculate_manipulation_score(text_analysis)
   interpreted_score = interpret_score(manipulation_score)
   
   return {
       # Metrics from manipulation_score
       'overall_score': manipulation_score.get('overall_score', 'not_calculated'),
       'manipulation_density': manipulation_score.get('manipulation_density', 'not_calculated'), 
       'affected_arguments_ratio': manipulation_score.get('affected_arguments_ratio', 'not_calculated'),
       'average_techniques_per_argument': manipulation_score.get('average_techniques_per_argument', 'not_calculated'),
       'max_techniques_in_single_argument': manipulation_score.get('max_techniques_in_single_argument', 'not_calculated'),
       
       # Interpretation details
       'risk_level': interpreted_score.get('risk_level', 'not_calculated'),
       'interpretation': interpreted_score.get('interpretation', 'not_calculated'),
       'metrics_explanation': interpreted_score.get('metrics_explanation', {
           'manipulation_density': 'not_calculated',
           'affected_arguments_ratio': 'not_calculated', 
           'average_techniques_per_argument': 'not_calculated',
           'max_techniques_in_single_argument': 'not_calculated'
       })
   }

def calculate_manipulation_score(text_analysis: dict) -> dict:
    """
    Calculate a manipulation score for a text based on arguments and manipulation techniques.
    
    Parameters:
    text_analysis: dict containing:
        - 'thesis': str
        - 'arguments': list of dicts, each containing:
            - 'content': str
            - 'manipulations': list of detected manipulation techniques
        
    Returns:
    dict with various scoring metrics and an overall score
    """
    arguments = text_analysis.get('arguments', {})
    total_arguments = len(arguments)
    if total_arguments == 0:
        return {
            'overall_score': 0,
            'manipulation_density': 0,
            'affected_arguments_ratio': 0,
            'average_techniques_per_argument': 0,
            'max_techniques_in_single_argument': 0
        }
    
    manipulation_counts = {
        f'argument_{i+1}': len([m for m in arg.get('manipulations', {}).values() if m])
        for i, arg in enumerate(arguments)
    }
    
    # Extract statistics in one pass
    techniques_per_argument = list(manipulation_counts.values())
    manipulated_arguments = sum(1 for count in techniques_per_argument if count > 0)
    log.trace(f'manipulated arguments: {manipulated_arguments}')
    log.trace(f'techniques_per_argument: {techniques_per_argument}')


    
    # # Calculate manipulation techniques per argument
    # # Calculate key metrics
    affected_arguments_ratio = manipulated_arguments / total_arguments
    max_techniques = max(techniques_per_argument)
    avg_techniques = sum(techniques_per_argument) / total_arguments
        
    # # Calculate manipulation density
    # # This considers both how many arguments are affected and how many techniques are used
    manipulation_density = sum(techniques_per_argument) / (total_arguments * 10)  # 10 being max possible techniques
    
    # # Calculate overall score (0-100)
    # # Weighted combination of different factors
    overall_score = (
        (affected_arguments_ratio * 0.4) +  # 40% weight for breadth of manipulation
        (manipulation_density * 0.4) +      # 40% weight for density of techniques
        (max_techniques / 10 * 0.2)         # 20% weight for maximum manipulation in a single argument
    ) * 100
    
    return {
        'overall_score': round(overall_score, 2),
        'manipulation_density': round(manipulation_density, 3),
        'affected_arguments_ratio': round(affected_arguments_ratio, 3),
        'average_techniques_per_argument': round(avg_techniques, 2),
        'max_techniques_in_single_argument': max_techniques
    }

def interpret_score(score_data):
    """
    Provide interpretation of the manipulation/reasoning score using a three-tier system.
    Returns interpretation details including risk level and interpretation.
    
    Score ranges:
    0-25: Excellent (Well-Reasoned)
    26-75: Moderate (Some Issues)
    76-100: Poor (Highly Manipulative)
    """
    SCORE_INTERPRETATIONS = {
        (0, 26): {
            "risk_level": "Excellent",
            "interpretation": "This text is well-reasoned, with minimal signs of manipulation or fallacious arguments. However, it's always good to remain critical and verify information independently."
        },
        (26, 76): {
            "risk_level": "Moderate",
            "interpretation": "This text contains a mix of logical and manipulative arguments. Review highlighted sections for potential fallacies."
        },
        (76, 101): {  # Using 101 to include 100 in the range
            "risk_level": "Poor",
            "interpretation": "This text shows frequent use of manipulative rhetoric and fallacies. Approach with caution and verify its claims."
        }
    }

    score = score_data.get('overall_score')
    
    if score is None:
        result = {
            "risk_level": "Not Calculated",
            "interpretation": "Score calculation could not be completed"
        }
    else:
        # Find the matching score range
        result = next(
            (interp for (low, high), interp in SCORE_INTERPRETATIONS.items()
             if low <= score < high),
            {
                "risk_level": "Invalid",
                "interpretation": "Score outside expected range"
            }
        )

    return result