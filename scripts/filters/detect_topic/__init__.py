from .output_topic_m import get_topic


"""
Step1: get subcategories (using "get_subcategories_m")
Step2: get the topic using "get_topic_and_confidence_p"
Step3: Verify the topic by confidence  number (threshhold = 0.7)
Step4: If verification fails
    - Try again with
"""


