# -*- coding: utf-8 -*-
#
# Copyright (C) 2011  Andrey Bondarenko
#
# This file is part of python-popcon
#
# Python-popcon is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of 
# the License, or (at your option) any later version.
#
# Python-popcon is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with python-popcon. If not, see <http://www.gnu.org/licenses/>.
#

"""Process popularity-contest submission
"""

__all__ = [ "read" ]

from datetime import datetime
# FIXME: pytz is not part of python stdlib, shall we use it?



class PopconSubmission(object):

    def __init__(self):
        pass


def read(stream):
    """Read popcon submission data from a stream.

    Returns a tuple of host id, the time when submission was
    generated, a version of popularity contest package,
    iterator over popcon submission data.
    """
    # FIXME: check that stream is a file
    line = stream.readline().strip().split()

    host_id      = line[2][len("ID:"):]

    ctime = line[1][len("TIME:"):]
    ctime = datetime.utcfromtimestamp(float(ctime)).isoformat()+"Z"

    default_arch = line[3][len("ARCH:"):]
    
    popcon_version = line[4][len("POPCONVER:"):]

    # FIXME: add real iterator
    data = tuple()
    return host_id, ctime, popcon_version, data


def iter_popcon_out(filename):
    
    host_id      = None
    collect_time = None
    default_arch = None
    popcon_ver   = None

    popcon_out = open(filename, "r")
    for line in popcon_out:
        row = line.split()
        if row[0] == "POPULARITY-CONTEST-0":
            host_id      = row[2][len("ID:"):]

            collect_time = row[1][len("TIME:"):]
            collect_time = datetime.utcfromtimestamp(float(collect_time)).isoformat()+"Z"

            default_arch = row[3][len("ARCH:"):]
            popcon_ver   = row[4][len("POPCONVER:"):]

        elif row[0] == "END-POPULARITY-CONTEST-0":
            pass
        else:
            yield [host_id, collect_time] + row + [""] if len(row) == 4 else []

        
    
