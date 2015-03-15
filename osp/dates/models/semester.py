

import time

from osp.common.config import config
from osp.common.models.base import BaseModel
from osp.corpus.models.document import Document
from peewee import *
from datetime import datetime


class Document_Date_Semester(BaseModel):


    document = ForeignKeyField(Document, unique=True)
    offset = IntegerField()
    semester = CharField(index=True)
    year = CharField(index=True)


    @property
    def date(self):

        """
        Convert the raw semester/year strings into a date.

        Returns:
            datetime
        """

        # 4-digit year:
        if len(self.year) == 4:
            date = datetime.strptime(self.year, '%Y')

        # 2-digit year:
        elif len(self.year) == 2:
            date = datetime.strptime(self.year, '%y')

        semester = self.semester.lower()

        # TODO: What should "winter" map to?

        if semester == 'fall':      month = 9
        elif semester == 'winter':  month = 1
        elif semester == 'spring':  month = 1
        elif semester == 'summer':  month = 6

        # Thread in the month.
        return date.replace(month=month)


    class Meta:
        database = config.get_table_db('document_date_semester')
