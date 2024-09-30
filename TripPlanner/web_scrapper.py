from bs4 import BeautifulSoup
import requests
from openai import OpenAI
import datetime


api_key = "ENTER YOUR API KEY HERE"

client = OpenAI(
    # This is the default and can be omitted
    api_key=api_key
)

role_text = """
Hi ChatGPT, hope you're doing well. Your job now is to parse through the text we feed you to extract some key information that we tell you. From now on, we’ll give you an input prompt that will only consist of the text we want you to parse, which is pertaining to various grant funding that Stanford undergraduate students can apply for. Your job is to obtain these key details:

The application deadline by which the final application for a grant is due (NOT the nomination or faculty letter of recommendation deadline. This is important.)
The amount of money that the grant is worth.

The exact format you need to return is the following. It MUST be in this format. This is very important, please ensure all outputs are only in this format, and nothing else. If there is no time, mark the time as 11:59pm PST. Please include a comma between the month and the day. 

“Month, Day, Year, Time
$”

Please list the month as an integer (e.g. August becomes 8).

If the deadline of amount cannot be found, insert “not found” in the appropriate field.

Everything below this is the text you need to perform this analysis on.
"""

grant_info_list = []

def webscrape_website(name, link, division, attrs):
    soup = BeautifulSoup(requests.get(link).text, "html.parser")
    deadline_info = soup.findAll(division, attrs={"class":attrs})

    concatenated_info = ""
    for dates in deadline_info:
        concatenated_info += dates.text + " "

    prompt_text = role_text + "\n" + concatenated_info

    print(f"prompt_text: {prompt_text}")
    print()

    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": prompt_text,
        }
    ],
    model="gpt-3.5-turbo",
    )

    generated_text = chat_completion.choices[0].message.content

    print(f"generated_text: {generated_text}")
    
    # STRING PROCESSING SO WE CAN MAKE THE OBJECT BELOW

    #deadline_date_info = datetime.datetime(2020, "july", 17)
    #print(deadline_date_info)

    #grant_info_list.append(grantInfo(name,deadline,link,amount))

    

#webscrape_website("Major Grant","https://undergradresearch.stanford.edu/fund-your-project/explore-student-grants/major", "li", "descriptor-light")
#webscrape_website("Small Grant","https://undergradresearch.stanford.edu/fund-your-project/explore-student-grants/small", "p", "plain-text")
webscrape_website("HAI Grant","https://hai.stanford.edu/research/student-affinity-groups", "li", "")