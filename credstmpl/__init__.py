from __future__ import print_function

def __set_logging(verbose_count):
    import logging

    logging.basicConfig(format='[%(asctime)-15s] %(levelname)-8s | %(message)s')
    log = logging.getLogger('credstmpl')

    log.setLevel(logging.WARN)

    if verbose_count > 0:
        log.setLevel(logging.INFO)
    if verbose_count > 1:
        log.setLevel(logging.DEBUG)

    return log

def __ok(text):
    # ansi escape sequences for colors, this one uses GREEN
    return '\033[92m{}\033[0m'.format(text)

def main():
    from . import cli
    from . import template

    parser = cli.creds_tmpl()
    args = parser.parse_args()

    log = __set_logging(args.verbose)

    rendered_templates = template.render(set(args.templates))

    for filename in rendered_templates:
        log.info("Rendered '{}'.".format(filename))

    if rendered_templates:
        files = "\n\t".join(rendered_templates)
        print(__ok("Remember to exclude these files from version control:\n\t{}".format(files)))
