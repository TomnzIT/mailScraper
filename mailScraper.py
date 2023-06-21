import argparse
import random
import requests
from bs4 import BeautifulSoup
from googlesearch import search
import re
from fake_useragent import UserAgent
import time

# Create the ArgumentParser object
parser = argparse.ArgumentParser(description="Search for email addresses associated with a domain on Google")

# Add arguments
parser.add_argument("-d", "--domain", type=str, help="Domain for email address search")
parser.add_argument("-o", "--output", type=str, help="Output file path to save the results")
parser.add_argument("-n", "--num-results", type=int, default=10, help="Number of results to retrieve (default: 10)")
parser.add_argument("-p", "--proxies", type=str, help="Proxy file path")

# Parse the command-line arguments
args = parser.parse_args()

# Check if the domain is specified
if not args.domain:
    parser.error("Domain must be specified with the -d option")

# Perform Google search
query = f'@{args.domain}'
results = search(query, num_results=args.num_results)

# Search for email addresses with the domain in the results
email_regex = rf'\b[A-Za-z0-9._%+-]+@{args.domain}\b'
emails = set()

# Create an instance of UserAgent
ua = UserAgent()

proxies = []

# Check if proxies are specified
if args.proxies:
    # Read proxies from the file
    with open(args.proxies, 'r') as file:
        proxies = [line.strip() for line in file.readlines()]

for result in results:
    try:
        # Select a random User-Agent
        user_agent = ua.random

        # Check if proxies are available
        if proxies:
            # Select a random proxy
            proxy = random.choice(proxies)

            # Set the request parameters with the proxy
            proxies = {
                'http': proxy,
                'https': proxy
            }
        else:
            proxies = None

        # Set the User-Agent in the request headers
        headers = {'User-Agent': user_agent}

        # Make the request using the proxy (if specified) and User-Agent
        response = requests.get(result, proxies=proxies, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Search for email addresses with the domain in the HTML content
        text = soup.get_text()
        matches = re.findall(email_regex, text)
        emails.update(matches)

        # Pause for 1 to 3 seconds between requests to avoid blocking
        time.sleep(random.uniform(1, 3))
    except requests.RequestException as e:
        # Continue execution in case of request error
        print(f"Error retrieving content from {result}. The request will be ignored. Error: {str(e)}")

# Check if an output file is specified
if args.output:
    # Save the email addresses to the output file
    with open(args.output, 'w') as file:
        for email in emails:
            file.write(email + '\n')
else:
    # Print the found email addresses
    print("Email addresses found:")
    for email in emails:
        print(email)