#!/usr/bin/env python
# coding: utf-8
from __future__ import unicode_literals
import shlex
from subprocess import Popen, PIPE

# django
from django.conf import settings
from django.core.management.base import BaseCommand
from logging import getLogger

# create logger
logger = getLogger("joplin_web.jw")


class Command(BaseCommand):

    help = 'Add a notebook to Joplin'

    def add_arguments(self, parser):
        parser.add_argument('notebook', type=str, help="notebook name")

    def handle(self, *args, **options):
        """
            call the command to add a notebook
        """

        logger.info("launch joplin to make a notebook %s" % options['notebook'])
        # run
        # mkbook
        line = 'joplin --profile {} mkbook {}'.format(settings.JOPLIN_PROFILE_PATH, options['notebook'])
        logger.info("%s" % line)

        args = shlex.split(line)
        # result = subprocess.run(args, shell=True)

        proc = Popen(args, stdout=PIPE, stderr=PIPE)
        out, err = proc.communicate()
        exitcode = proc.returncode

        logger.info("%s %s %s" % (out, err, exitcode))
        return out.decode()