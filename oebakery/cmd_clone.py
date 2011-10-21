import optparse, sys, os
import oebakery

arguments = "<repository> [directory]"
description = """Clone an OE-lite development environment into a new directory

Arguments:
  repository            OE-lite (git) repository to clone
  directory             directory to to clone into (default is current dir)"""

def run(parser, options, args, config):

    if len(args) < 1:
        parser.error('too few arguments')
    if len(args) > 2:
        parser.error('too many arguments')

    if not args:
        parser.error("repository argument required")
    options.repository = args.pop(0)

    if args:
        options.directory = args.pop(0)
    else:
        options.directory = options.repository.strip("/")
        options.directory = os.path.basename(options.directory)
        if options.directory[-4:] == '.git':
            options.directory = options.directory[:-4]

    if not oebakery.call('git clone --recursive %s %s'%(
            options.repository, options.directory)):
        return 1

    topdir = oebakery.set_topdir(options.directory)
    oebakery.chdir(options.directory)

    oebakery.copy_local_conf_sample("conf")

    if not oebakery.call('git config push.default tracking'):
        print 'Failed to set push.default = tracking'

    return ("update", ({}, []), config)