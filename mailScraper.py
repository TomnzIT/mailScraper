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

# Add the arguments
parser.add_argument("-d", "--domain", type=str, help="Domain to search for email addresses")
parser.add_argument("-o", "--output", type=str, help="Output file path to save the results")
parser.add_argument("-n", "--num-results", type=int, default=10, help="Number of results to retrieve (default: 10)")
parser.add_argument("-p", "--proxies", type=str, help="File path containing proxies")

# Parse the command-line arguments
args = parser.parse_args()

# Check if the domain is specified
if not args.domain:
    parser.error("The domain must be specified with the -d option")

# Perform the Google search
query = f'@{args.domain}'
results = search(query, num_results=args.num_results)

# Search for email addresses in the results
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
            while True:
                # Select a random proxy
                proxy = random.choice(proxies)

                # Set the request parameters with the proxy
                proxy_dict = {
                    'http': proxy,
                    'https': proxy
                }

                try:
                    # Check proxy validity using ipinfo.io
                    response = requests.get('https://ipinfo.io/json', proxies=proxy_dict, timeout=5)
                    response.raise_for_status()
                    data = response.json()

                    # Verify if the response contains the IP information
                    if 'ip' in data:
                        print(f"Valid proxy: {proxy}")
                        break  # Proxy is valid, break out of the while loop
                    else:
                        print(f"Invalid proxy: {proxy}")
                except (requests.RequestException, ValueError):
                    # Proxy is invalid or request failed, try another proxy
                    print(f"Invalid proxy: {proxy}")
                    continue

        else:
            proxy_dict = None

        # Set the User-Agent in the request headers
        headers = {'User-Agent': user_agent}

        # Make the request using the proxy (if specified) and the User-Agent
        response = requests.get(result, proxies=proxy_dict, headers=headers, timeout=5)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Search for email addresses in the HTML content
        text = soup.get_text()
        matches = re.findall(email_regex, text)
        emails.update(matches)

        # Pause for 1 to 3 seconds between requests to avoid blocking
        time.sleep(random.uniform(1, 3))

    except requests.RequestException as e:
        # Continue execution in case of request error
        print(f"Error retrieving content from {result}. The request will be skipped. Error: {str(e)}")
    except IndexError as e:
        # Handle the case when no valid proxy is available
        print("No valid proxy available. The request will be skipped.")
        continue

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
