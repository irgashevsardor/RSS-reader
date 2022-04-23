"""The module is the entry point for the RSS reader project"""

from logging import config, getLogger

from content_aggregator.rss_aggregator import RSSContent, output_to_console
from converters.converter import to_json
from parser.arg_parser import handle_args

config.fileConfig('log_config.ini')

logger = getLogger()
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
    rss_content = RSSContent(parser.source, parser.limit)
    parsed_rss_content = rss_content.get_parsed_rss_content()

    if parser.json:
        print(to_json(parsed_rss_content))
    else:
        output_to_console(parsed_rss_content)


if __name__ == '__main__':
    main()
