#!/usr/bin/env python
import sys
import warnings
from pypdf import PdfReader
import os
import requests
from resume_match_ai.exceptions import RateLimitError, RequestError

from datetime import datetime

from resume_match_ai.crew import ResumeMatchAi

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information


ratelimit_api = os.getenv("RATELIMIT_API")
request_token = os.getenv("REQUEST_RATELIMIT_TOKEN")

def extract_resume():
    reader = PdfReader("./software-developer.pdf")
    resume = ""
    for page in reader.pages:
        text = page.extract_text()
        if text:
            resume += text

    return resume


def run():
    """
    Run the crew.
    """
    resume = extract_resume()

    inputs = {
        'resume': resume
    }

    try:
        # implementation of ratelimiter here
        response = requests.post(
            ratelimit_api,
            headers={"custom-header": request_token}
        )
        status_code = response.status_code

        if (status_code == 429):
            raise RateLimitError("Too many requests! Please try again tomorrow.")

        elif (status_code != 201):
            raise RequestError(f"Unexpected status code from rate limiter: {status_code}")

        ResumeMatchAi().crew().kickoff(inputs=inputs)
    except RateLimitError as e:
        print(e.message)

    except RequestError as e:
        print(e.message)

    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def test():
    """
    Test the crew execution and returns the results.
    """
    resume = extract_resume()

    inputs = {
        'resume': resume
    }

    try:
        ResumeMatchAi().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
