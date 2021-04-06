"""CLI utilities writing spell checkers."""


def extend_argument_parser(
    parser,
    language=True,
):
    if language:
        parser.add_argument(
            "-l",
            "--language",
            type=str,
            default="en_US",
            help="Language to check, you'll have to install the corresponding "
            "hunspell dictionary, on Debian see apt list 'hunspell-*'.",
        )
