#!/usr/bin/env python3

# Copyright (C) 2015-2019 Bitergia
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# Authors:
#   Alvaro del Castillo San Felix <acs@bitergia.com>
#
#

import os
import random

secret = ''.join(random.SystemRandom().choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50))
settings_file = 'django_hatstall/settings.py'
settings = None

try:
    csrf_trusted_origins = os.environ['CSRF_TRUSTED_ORIGINS'].strip('"').split(' ')
except KeyError:
    csrf_trusted_origins = []

with open(settings_file) as f:
    settings = f.read()
    settings = settings.replace("SECRET_KEY = ''", "SECRET_KEY = '%s'" % secret)
    settings = settings.replace("DEBUG = True", "DEBUG = False")
    settings = settings.replace("ALLOWED_HOSTS = []", "ALLOWED_HOSTS = ['*']")
    settings = settings.replace("CSRF_TRUSTED_ORIGINS = []", "CSRF_TRUSTED_ORIGINS = {}".format(str(csrf_trusted_origins)))

with open(settings_file, "w") as f:
    f.write(settings)

print("Django configured for deployment (secret, debug, allowed_hosts) in", settings_file)
