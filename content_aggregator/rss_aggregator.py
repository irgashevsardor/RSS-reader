"""The module provides necessary functions to aggregate RSS content"""

import logging
import sys
from itertools import islice
from typing import Optional, List, Union

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger()


def fetch_rss_content(url: str) -> requests.Response:
    """Fetches RSS page based on URL passed

    Args:
        url: URL of RSS feed

    Returns:
        The Response object, which contains a server’s response to an HTTP request.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }
    logger.debug(f'Making HTTP request to {url}')
    try:
        response = requests.get(url, headers=headers, )
        response.raise_for_status()
    except requests.exceptions.ConnectionError:
        logger.error('Connection Error Occurred. Program Terminated. Try Again.')
        sys.exit()
    except requests.exceptions.HTTPError:
        logger.error('HTTP Error Occurred. Program Terminated. Try Again.')
        sys.exit()
    except requests.exceptions.Timeout:
        logger.error('The Request Timed Out. Program Terminated. Try Again.')
        sys.exit()
    except requests.exceptions.RequestException:
        logger.error('Ambiguous Exception. Program Terminated. Try Again.')
        sys.exit()
    logger.debug('Response arrived!')

    return response


def parse_rss_content(fetched_content: requests.Response) -> List[Union[str, dict]]:
    """Parses the XML contents of the Response object

    Args:
        fetched_content: The Response object, which contains a server’s response to an HTTP request.

    Returns:
        List containing the parsed feed source and the parsed news items
    """
    logger.debug('Parsing fetched content...')
    soup = BeautifulSoup(fetched_content.text, 'xml')
    feed = soup.channel.title.text
    articles = soup.find_all('item')
    news_items = [feed]
    for article in articles:
        news_item = {
            'title': article.title.text,
            'pub_date': article.pubDate.text if article.pubDate else 'No Publication Date',
            'description': article.description.text if article.description else 'No Description',
            'link': article.link.text,
        }
        news_items.append(news_item)
    logger.debug('Parsing complete!')
    return news_items


def print_rss_content(parsed_content: List[Union[str, dict]], content_limit: Optional[int] = None) -> None:
    """Prints the contents of the parsed feed-containing XML

    Args:
        parsed_content: List containing the parsed feed source and the parsed news items
        content_limit: Limit of the feeds

    Returns:
        None
    """
    print(f"\nFeed: {parsed_content[0]}\n")
    if content_limit is not None and content_limit > 0:
        content_limit += 1
    for item in islice(parsed_content, 1, content_limit):
        print(f"Title: {item['title']}")
        print(f"Date Published: {item['pub_date']}")
        print(f"Description: {item['description']}")
        print(f"Link: {item['link']}")
        print('\n====================================================================================\n')
