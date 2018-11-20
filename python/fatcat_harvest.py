#!/usr/bin/env python3

import sys
import argparse
import datetime
from fatcat_tools.harvest import HarvestCrossrefWorker, HarvestDataciteWorker,\
    HarvestArxivWorker, HarvestPubmedWorker, HarvestDoajArticleWorker,\
    HarvestDoajJournalWorker

def run_crossref(args):
    worker = HarvestCrossrefWorker(
        kafka_hosts=args.kafka_hosts,
        produce_topic="fatcat-{}.crossref".format(args.env),
        state_topic="fatcat-{}.crossref-state".format(args.env),
        contact_email=args.contact_email,
        start_date=args.start_date,
        end_date=args.end_date)
    worker.run()

def run_datacite(args):
    worker = HarvestDataciteWorker(
        kafka_hosts=args.kafka_hosts,
        produce_topic="fatcat-{}.datacite".format(args.env),
        state_topic="fatcat-{}.datacite-state".format(args.env),
        contact_email=args.contact_email,
        start_date=args.start_date,
        end_date=args.end_date)
    worker.run()

def run_arxiv(args):
    worker = HarvestArxivWorker(
        kafka_hosts=args.kafka_hosts,
        produce_topic="fatcat-{}.arxiv".format(args.env),
        state_topic="fatcat-{}.arxiv-state".format(args.env),
        start_date=args.start_date,
        end_date=args.end_date)
    worker.run()

def run_pubmed(args):
    worker = HarvestPubmedWorker(
        kafka_hosts=args.kafka_hosts,
        produce_topic="fatcat-{}.pubmed".format(args.env),
        state_topic="fatcat-{}.pubmed-state".format(args.env),
        start_date=args.start_date,
        end_date=args.end_date)
    worker.run()

def run_doaj_article(args):
    worker = HarvestDoajArticleWorker(
        kafka_hosts=args.kafka_hosts,
        produce_topic="fatcat-{}.doaj-article".format(args.env),
        state_topic="fatcat-{}.doaj-article-state".format(args.env),
        start_date=args.start_date,
        end_date=args.end_date)
    worker.run()

def run_doaj_journal(args):
    worker = HarvestDoajJournalWorker(
        kafka_hosts=args.kafka_hosts,
        produce_topic="fatcat-{}.doaj-journal".format(args.env),
        state_topic="fatcat-{}.doaj-journal-state".format(args.env),
        start_date=args.start_date,
        end_date=args.end_date)
    worker.run()


def mkdate(raw):
    return datetime.datetime.strptime(raw, "%Y-%m-%d").date()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug',
        action='store_true',
        help="enable debug logging")
    parser.add_argument('--kafka-hosts',
        default="localhost:9092",
        help="list of Kafka brokers (host/port) to use")
    parser.add_argument('--env',
        default="qa",
        help="Kafka topic namespace to use (eg, prod, qa)")
    parser.add_argument('--start-date',
        default=None, type=mkdate,
        help="begining of harvest period")
    parser.add_argument('--end-date',
        default=None, type=mkdate,
        help="end of harvest period")
    parser.add_argument('--contact-email',
        default="undefined",    # better?
        help="contact email to use in API header")
    parser.add_argument('--continuous',
        default=False,
        help="continue harvesting indefinitely in a loop?")
    subparsers = parser.add_subparsers()

    sub_crossref = subparsers.add_parser('crossref')
    sub_crossref.set_defaults(func=run_crossref)

    sub_datacite = subparsers.add_parser('datacite')
    sub_datacite.set_defaults(func=run_datacite)

    sub_arxiv = subparsers.add_parser('arxiv')
    sub_arxiv.set_defaults(func=run_arxiv)

    sub_pubmed = subparsers.add_parser('pubmed')
    sub_pubmed.set_defaults(func=run_pubmed)

    # DOAJ stuff disabled because API range-requests are broken
    #sub_doaj_article = subparsers.add_parser('doaj-article')
    #sub_doaj_article.set_defaults(func=run_doaj_article)
    #sub_doaj_journal = subparsers.add_parser('doaj-journal')
    #sub_doaj_journal.set_defaults(func=run_doaj_journal)

    args = parser.parse_args()
    if not args.__dict__.get("func"):
        print("tell me what to do!")
        sys.exit(-1)
    args.func(args)

if __name__ == '__main__':
    main()