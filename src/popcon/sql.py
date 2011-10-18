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
"""SQL storage for popularity-contest data
"""

__all__ = [ "PopconDB", "PopconStats" ]


from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table

from sqlalchemy.sql import and_
from sqlalchemy.sql import bindparam


TABLE_POPCON_SNAP  = "popcon_snap"
TABLE_POPCON_STATS = "popcon_stats"

BULK_BUF_SIZE = 100


class PopconDB(object):

    def __init__(self, url):
        self.engine = create_engine(url)

    def new_submission(self, host_id, collect_time):
        return PopconSubmission(self.engine, host_id, collect_time)

    def new_stats(self, url, timestamp=None):
        return PopconStats(self.engine, url, timestamp)
        
    def pkg_bulk_writer(self, snap):
        return _BulkPkgWriter(self.engine, snap)


class PopconSubmission(object):
    """Handler for a single snapshot of popcon statistics
    """
    def __init__(self, engine, host_id, ctime):
        self._engine = engine

        self.submission_id = None
        self.host_id       = host_id
        self.ctime         = ctime

    def _init_db_key(self):
        engine = self._engine
        t = Table("popcon_submission", MetaData(bind=engine), autoload=True)
        #try:
            # autocommit here
        t.insert().\
            values(host_id = self.host_id, submit_time = self.ctime).\
            execute()
        # except sqlalchemy.exc.IntegrityError:
        #     pass    # assuming target snap_id already exists
        result = t.select(and_(
                t.c.host_id == self.host_id,
                t.c.submit_time  == self.ctime
                )).execute()
        self.submission_id = result.fetchone()[0]
        return self.submission_id

    def get_writer(self):
        return _SubmissionBulkWriter(self._engine, self.submission_id)
        


class PopconStats(object):
    """Handler for a single snapshot of popcon statistics
    """

    def __init__(self, engine, popcon_url, timestamp=None):
        self._engine     = engine
        self.snap_id     = None
        self.snap_time   = timestamp or datetime.now()
        self.popcon_url  = popcon_url
        self.submissions = None
        # FIXME: fill timezone

    def _init_snap_id(self):
        engine = self._engine
        t = Table(TABLE_POPCON_SNAP, MetaData(bind=engine), autoload=True)
        #try:
            # autocommit here
        t.insert().\
            values(snap_time = self.snap_time, popcon_url = self.popcon_url).\
            execute()
        # except sqlalchemy.exc.IntegrityError:
        #     pass    # assuming target snap_id already exists
        result = t.select(and_(
                t.c.popcon_url == self.popcon_url,
                t.c.snap_time  == self.snap_time
                )).execute()
        self.snap_id = result.fetchone()[0]
        return self.snap_id

    def set_submissions(self, value):
        engine = self._engine
        t = Table(TABLE_POPCON_SNAP, MetaData(bind=engine), autoload=True)
        
        t.update().\
            where(and_(
                t.c.popcon_url == self.popcon_url,
                t.c.snap_time  == self.snap_time
                )).\
            values(submissions = value).execute()
        self.submissions = value

    def pkg_bulk_writer(self):
        return _BulkPkgWriter(self._engine, self.snap_id)


class _SubmissionBulkWriter(object):
    def __init__(self, engine, key):
        self.key = key

        self._c   = engine.connect()
        self._trx = self._c.begin()

        t  = Table("popcon_submission_data", MetaData(bind=engine), autoload=True)
        self._insert = t.insert().values(
            submission_id = bindparam("b_submission_id"),
            package       = bindparam("b_package"),
            path          = bindparam("b_path"),
            atime         = bindparam("b_atime"),
            ctime         = bindparam("b_ctime"),
            tag           = bindparam("b_tag")
            )
    
    def insert(self, package, path, atime, ctime, tag):
        self._c.execute(self._insert, {
                "b_submission_id" : self.key,
                "b_package"       : package,
                "b_path"          : path,
                "b_atime"         : atime,
                "b_ctime"         : ctime,
                "b_tag"           : tag
                })

    def commit(self):
        self._trx.commit()
        self._trx = self._c.begin()

    def rollback(self):
        self._trx.rollback()
        self._trx = self._c.begin()

    def __del__(self):
        self._trx.commit()


class _BulkPkgWriter(object):
    """Writer class for effective uploading popcon stats into database
    """

    def __init__(self, engine, snap):
        self._c = engine.connect()
        self.snap = snap

        self._trans = self._c.begin()
        self._bufsz = BULK_BUF_SIZE

        t  = Table(TABLE_POPCON_STATS, MetaData(bind=engine), autoload=True)
        self._insert = t.insert().values(
            snap_id = bindparam("b_snap"),
            package = bindparam("b_package"),
            vote    = bindparam("b_vote"),
            olde    = bindparam("b_olde"),
            recent  = bindparam("b_recent"),
            nofiles = bindparam("b_nofiles")
            )

    def insert(self, package, vote, olde, recent, nofiles):
        self._c.execute(self._insert, {
                "b_snap"   : self.snap,
                "b_package": package,
                "b_vote"   : vote,
                "b_olde"   : olde,
                "b_recent" : recent,
                "b_nofiles": nofiles
                })

    def commit(self):
        self._trans.commit()
        self._trans = self.conn.begin()

    def rollback(self):
        self._trans.rollback()
        self._trans = self.conn.begin()

    def __del__(self):
        self._trans.commit()
