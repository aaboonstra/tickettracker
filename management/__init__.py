#!/usr/bin/env python
# vim: set ts=4 sw=4 sts=4 et:
#=======================================================================
# Copyright (C) 2011 Alex Boonstra at OSSO B.V.
# This file is part of ticket-tracker.
#
# ticket-tracker is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ticket-tracker is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ticket-tracker. If not, see <http://www.gnu.org/licenses/>.
#=======================================================================


import coverage
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from django.db.models.signals import post_syncdb
from django.test.simple import DjangoTestSuiteRunner


def add_view_permissions(sender, **kwargs):
    """
    This syncdb hook takes care of adding a view permission too all our 
    content types.
    """
    # for each of our content types
    for content_type in ContentType.objects.all():
        # build our permission slug
        codename = "view_%s" % content_type.model

        # if it doesn't exist..
        if not Permission.objects.filter(content_type=content_type, codename=codename):
            # add it
            Permission.objects.create(content_type=content_type,
                                      codename=codename,
                                      name="Can view %s" % content_type.name)
            print "Added view permission for %s" % content_type.name

# check for all our view permissions after a syncdb
post_syncdb.connect(add_view_permissions)




class CoverageRunner(DjangoTestSuiteRunner):

    def run_tests(self, *args, **kwargs):
        run_with_coverage = hasattr(settings, 'COVERAGE_MODULES')

        if run_with_coverage:
            coverage.use_cache(0)
            coverage.start()

        result = super(CoverageRunner, self).run_tests(*args, **kwargs)

        if run_with_coverage:
            coverage.stop()
            print ''
            print '-' * 80
            print ' Unit Test Code Coverage Results'
            print '-' * 80
            coverage_modules = []
            for module in settings.COVERAGE_MODULES:
                coverage_modules.append(__import__(module, globals(),
                                                   locals(), ['']))
            coverage.report(coverage_modules, show_missing=1)
            print '-' * 80

        return result
