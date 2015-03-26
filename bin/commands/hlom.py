

import click
import numpy as np
import csv

from osp.common.config import config
from osp.citations.hlom.models.record import HLOM_Record
from osp.citations.hlom.models.citation import HLOM_Citation
from osp.citations.hlom.dataset import Dataset
from osp.citations.hlom.jobs.query import query
from peewee import create_model_tables
from playhouse.postgres_ext import ServerSide
from clint.textui.progress import bar


@click.group()
def cli():
    pass


@cli.command()
def init_db():

    """
    Create the database tables.
    """

    create_model_tables([
        HLOM_Record,
        HLOM_Citation,
    ], fail_silently=True)


@cli.command()
@click.option('--page_size', default=10000)
def insert_records(page_size):

    """
    Write the records into the database.
    """

    HLOM_Record.insert_records(page_size)


@cli.command()
def queue_queries():

    """
    Queue citation extraction queries.
    """

    for record in ServerSide(HLOM_Record.select()):
        config.rq.enqueue(query, record.id)


@cli.command()
@click.argument('out_path', type=click.Path())
def csv_text_counts(out_path):

    """
    Write a CSV with text -> assignment count.
    """

    out_file = open(out_path, 'w')

    # CSV writer.
    cols = ['title', 'author', 'count']
    writer = csv.DictWriter(out_file, cols)
    writer.writeheader()

    query = HLOM_Citation.text_counts()
    count = query.count()

    rows = []
    for c in bar(query.naive().iterator(),
                 expected_size=count):

        rows.append({
            'title':  c.record.pymarc.title(),
            'author': c.record.pymarc.author(),
            'count':  c.count
        })

    writer.writerows(rows)


# TODO|dev


@cli.command()
def write_citation_count():

    """
    Cache citation counts.
    """

    HLOM_Record.write_citation_count()


@cli.command()
def write_deduping_hash():

    """
    Cache deduping hashes.
    """

    HLOM_Record.write_deduping_hash()


@cli.command()
def write_teaching_rank():

    """
    Cache teaching ranks.
    """

    HLOM_Record.write_teaching_rank()
