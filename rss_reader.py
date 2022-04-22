"""The module is the entry point for the RSS reader project"""

import logging
from logging.config import fileConfig

from content_aggregator import rss_aggregator
from converters.converter import to_json
from parser.arg_parser import handle_args

fileConfig('log_config.ini')

# Initialize logger
logger = logging.getLogger()
logger.disabled = True


def main() -> None:
    """The entry point function

    Returns:
        None
    """
    parser = handle_args()
    if parser.verbose:
        logger.disabled = False
    logger.debug('Program started.')
    content = rss_aggregator.fetch_rss_content(parser.source)
    parsed_rss = rss_aggregator.parse_rss_content(content)
    if parser.json:
        print(to_json(parsed_rss, parser.limit))
    else:
        rss_aggregator.print_rss_content(parsed_rss, parser.limit)


if __name__ == '__main__':
    main()
