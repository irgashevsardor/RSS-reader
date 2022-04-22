"""The module provides a function of conversion from dictionary to JSON"""

import json
import logging
from itertools import islice
from typing import Union, List, Optional

logger = logging.getLogger()


def to_json(parsed_content: List[Union[str, dict]], content_limit: Optional[int] = None) -> str:
    """Converts list containing dictionary elements to JSON

    Args:
        parsed_content: List containing the parsed feed source and the parsed news items
        content_limit: Limit of the feeds

    Returns:
        JSON formatted string of serialized (converted) objects
    """
    logger.debug('Serializing to JSON...')
    json_list = []
    if content_limit is not None and content_limit > 0:
        content_limit += 1
    for item in islice(parsed_content, 1, content_limit):
        json_item = {
            'Feed Source': parsed_content[0],
            'News Item': {
                'Title': item['title'],
                'Publication Date': item['pub_date'],
                'Description': item['description'],
                'Link': item['link']
            }
        }
        json_list.append(json_item)
    logger.debug('Serialization complete!')
    return json.dumps(json_list, indent=4)
