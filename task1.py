import re

text = """
Hi, 
my name is Jane and my phone number is 555-123-4567. 
My email address is jane_doe@example.com. 
I live on 123 Main St. Apt. #456, and I was born on January 11th, 1990. I have an appointment on 2023-05-15 at 2:30pm at 789 Oak Ln. #3 and backup on 2023/05/21. 
Please give me a call or send me an email to confirm. In case the dates are unavailable, please set up a meeting sometime in June. I would love June 19h.
Thank you!
"""

# Define a regex pattern to match dates in various formats
date_pattern = re.compile(r'\b(?:\d{4}-\d{2}-\d{2}|\d{4}/\d{2}/\d{2}|[a-zA-Z]+\s\d{1,2}(?:st|nd|rd|th)?,\s\d{4})\b')

# Find all matches in the text
matches = date_pattern.findall(text)

# Print the extracted dates
print("Extracted Dates:")
for match in matches:
    print(match)