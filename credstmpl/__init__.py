from __future__ import print_function
from . import hilite

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

def main():
    from . import cli
    from . import template

    parser = cli.creds_tmpl()
    args = parser.parse_args()

    log = __set_logging(args.verbose)

    rendered_templates, skipped_templates = template.render(set(args.templates))

    for filename in rendered_templates:
        log.info("Rendered '{}'.".format(filename))

    if skipped_templates:
        files = "\n\t".join(skipped_templates)
        print(hilite.bad("Skipped these files due to errors:\n\t{}".format(files)))

    if rendered_templates:
        files = "\n\t".join(rendered_templates)
        print(hilite.ok("Remember to exclude these files from version control:\n\t{}".format(files)))
