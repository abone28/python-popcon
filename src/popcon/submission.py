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

"""Process raw popularity-contest submission data
"""

__all__ = [ "parse" ]

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

    filename = "/var/log/popularity-contest"

    # FIXME: get date and time from file contents
    ctime = datetime.fromtimestamp(
       os.stat(filename).st_mtime, pytz.utc)

    host_id = 'de2b4645-d58f-407e-9071-cf447e5cef5d'
    #ctime   = 

    s = db.new_submission(host_id, ctime)

    print s._init_db_key()

    UTC = pytz.utc

    writer = s.get_writer()
    def write(package, path, atime, ctime, tag):
        writer.insert(package, path, atime, ctime, tag)

    istream = iter_popcon_out(filename)
    for row_no, row in enumerate(istream):
        print row_no
        if not row:
            # FIXME: хз почему пустые строки встречаются
            continue
        host_id, ctime, atime, ctime, package, path, tag = row
        atime = datetime.fromtimestamp(int(atime), UTC)
        ctime = datetime.fromtimestamp(int(ctime), UTC)
        write(package, path, atime, ctime, tag)
        
    
