import PyPDF2
import urllib
from io import StringIO
from IPython.display import display, HTML
from redlines import Redlines
import openai
from pathlib import Path


def get_key():
    key = open('/Users/ivalenzuela/Desktop/key.txt', 'r').read()
    openai.api_key = key


def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,  # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]


def getPriceFromInvoice():
    sample_pdf = open('/Users/ivalenzuela/Desktop/invoice.pdf', mode='rb')
    pdfdoc = PyPDF2.PdfReader(sample_pdf)

    text = ""
    for page in range(len(pdfdoc.pages)):
        text += pdfdoc.pages[page].extract_text()

    prompt = f"""
    Your task is to get the total price of the invoice.
    Output a dictionary with invoice number as key and the price as value.

    Invoice: ```{text}```
    """
    response = get_completion(prompt)
    print(response)


def summarizeResume():
    sample_pdf = open('/Users/ivalenzuela/Desktop/resume2.pdf', mode='rb')
    pdfdoc = PyPDF2.PdfReader(sample_pdf)

    text = ""
    for page in range(len(pdfdoc.pages)):
        text += pdfdoc.pages[page].extract_text()

    prompt = f"""
    Your task is to list the main highlights of resume in 5 bullet points.
    Resume: ```{text}```
    """
    response = get_completion(prompt)
    print(response)


def readBenefits():
    # define url
    ''' url = 'https://github.com/ivalenzuela1/OpenAiDemo/blob/main/benefits.pdf' '''
    url = 'https://www.africau.edu/images/default/sample.pdf'

    sample_pdf = open('/Users/ivalenzuela/Desktop/benefits.pdf', mode='rb')
    pdfdoc = PyPDF2.PdfReader(sample_pdf)
    pagehandle = pdfdoc.pages[0]
    print(pagehandle.extract_text())

    text = ""
    for page in range(10):
        text += pdfdoc.pages[page].extract_text()

    prompt = f"""
    Your task is to help pregnant women understand their benefits plan.
    List bullet points with most important benefits relating to maternity leave

    Benefit plan: ```{text}```
    """
    response = get_completion(prompt)
    print(response)


def slangToFormal():
    prompt2 = f"""
    Translate the following from slang to a business letter:
    'Dude, This is Joe, check out this spec on this standing lamp.'
    """
    response = get_completion(prompt2)
    print(response)


def jsonToHtml():
    data_json = {"resturant employees": [
        {"name": "Shyam", "email": "shyamjaiswal@gmail.com"},
        {"name": "Bob", "email": "bob32@gmail.com"},
        {"name": "Jai", "email": "jai87@gmail.com"}
    ]}

    prompt = f"""
    Translate the following python dictionary from JSON to an HTML \
    table with column headers and title: {data_json}
    """
    response = get_completion(prompt)
    print(response)


def proofReadAndCorrect():
    text = f"""
    Got this for my daughter for her birthday cuz she keeps taking \
    mine from my room.  Yes, adults also like pandas too.  She takes \
    it everywhere with her, and it's super soft and cute.  One of the \
    ears is a bit lower than the other, and I don't think that was \
    designed to be asymmetrical. It's a bit small for what I paid for it \
    though. I think there might be other options that are bigger for \
    the same price.  It arrived a day earlier than expected, so I got \
    to play with it myself before I gave it to my daughter.
    """
    prompt = f"proofread and correct this review: ```{text}```"
    response = get_completion(prompt)
    diff = Redlines(text, response)
    display((diff.output_markdown))


def runPrompt_factChair():

    fact_sheet_chair = """OVERVIEW
    - Part of a beautiful family of mid-century inspired office furniture,
    including filing cabinets, desks, bookcases, meeting tables, and more.
    - Several options of shell color and base finishes.
    - Available with plastic back and front upholstery (SWC-100)
    or full upholstery (SWC-110) in 10 fabric and 6 leather options.
    - Base finish options are: stainless steel, matte black,
    gloss white, or chrome.
    - Chair is available with or without armrests.
    - Suitable for home or business settings.
    - Qualified for contract use.

    CONSTRUCTION
    - 5-wheel plastic coated aluminum base.
    - Pneumatic chair adjust for easy raise/lower action.

    DIMENSIONS
    - WIDTH 53 CM | 20.87”
    - DEPTH 51 CM | 20.08”
    - HEIGHT 80 CM | 31.50”
    - SEAT HEIGHT 44 CM | 17.32”
    - SEAT DEPTH 41 CM | 16.14”

    OPTIONS
    - Soft or hard-floor caster options.
    - Two choices of seat foam densities:
    medium (1.8 lb/ft3) or high (2.8 lb/ft3)
    - Armless or 8 position PU armrests

    MATERIALS
    SHELL BASE GLIDER
    - Cast Aluminum with modified nylon PA6/PA66 coating.
    - Shell thickness: 10 mm.
    SEAT
    - HD36 foam

    COUNTRY OF ORIGIN
    - Italy
    """

    prompt = f"""
    Your task is to help a marketing team create a
    description for a retail website of a product based
    on a technical fact sheet.

    Write a product description based on the information
    provided in the technical specifications delimited by
    triple backticks.

    The description is intended for furniture retailers,
    so should be technical in nature and focus on the
    materials the product is constructed from.

    At the end of the description, include every 7-character
    Product ID in the technical specification.

    After the description, include a table that gives the
    product's dimensions. The table should have two columns.
    In the first column include the name of the dimension.
    In the second column include the measurements in inches only.

    Give the table the title 'Product Dimensions'.

    Format everything as HTML that can be used in a website.
    Place the description in a <div> element. Also, can you style the website.

    Technical specifications: ```{fact_sheet_chair}```
    """

    response = get_completion(prompt)
    print(response)
    display(HTML(response))
    '''print(response)'''


if __name__ == "__main__":
    get_key()
    summarizeResume()
