import argparse

def creds_tmpl():
    """ This function creates an argparser for the credstmpl cli tool. """
    parser = argparse.ArgumentParser(
        description = "A command-line tool to instantiate templates from credstash.",
        epilog = "Because your credentials are sacred and should be in a temple.")

    parser.add_argument('--verbose', '-v',
        action='count', default=0,
        help="verbosity level, -v for INFO, -vv for DEBUG")
    parser.add_argument('templates',
        type=str, nargs='+',
        help="paths to any templates we wish to generate.")

    return parser
