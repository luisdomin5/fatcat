
"""
Helpers for doing elasticsearch queries (used in the web interface; not part of
the formal API)
"""

import sys
import datetime
from dataclasses import dataclass
from typing import List, Optional, Any

from flask import abort, flash
import elasticsearch
from elasticsearch_dsl import Search, Q
import elasticsearch_dsl.response

from fatcat_web import app

@dataclass
class ReleaseQuery:
    q: Optional[str] = None
    limit: Optional[int] = None
    offset: Optional[int] = None
    fulltext_only: bool = False
    container_id: Optional[str] = None

    @classmethod
    def from_args(cls, args) -> 'ReleaseQuery':

        query_str = args.get('q') or '*'

        container_id = args.get('container_id')
        # TODO: as filter, not in query string
        if container_id:
            query_str += ' container_id:"{}"'.format(container_id)

        # TODO: where are container_issnl queries actually used?
        issnl = args.get('container_issnl')
        if issnl and query_str:
            query_str += ' container_issnl:"{}"'.format(issnl)

        offset = args.get('offset', '0')
        offset = max(0, int(offset)) if offset.isnumeric() else 0

        return ReleaseQuery(
            q=query_str,        
            offset=offset,
            fulltext_only=bool(args.get('fulltext_only')),
            container_id=container_id,
        )

@dataclass
class GenericQuery:
    q: Optional[str] = None
    limit: Optional[int] = None
    offset: Optional[int] = None

    @classmethod
    def from_args(cls, args) -> 'GenericQuery':
        query_str = args.get('q')
        if not query_str:
            query_str = '*'
        offset = args.get('offset', '0')
        offset = max(0, int(offset)) if offset.isnumeric() else 0

        return GenericQuery(
            q=query_str,
            offset=offset,
        )

@dataclass
class SearchHits:
    count_returned: int
    count_found: int
    offset: int
    limit: int
    deep_page_limit: int
    query_time_ms: int
    results: List[Any]


def results_to_dict(response: elasticsearch_dsl.response.Response) -> List[dict]:
    """
    Takes a response returns all the hits as JSON objects.

    Also handles surrogate strings that elasticsearch returns sometimes,
    probably due to mangled data processing in some pipeline. "Crimes against
    Unicode"; production workaround
    """

    results = []
    for h in response:
        r = h._d_
        # print(h.meta._d_)
        results.append(r)

    for h in results:
        for key in h:
            if type(h[key]) is str:
                h[key] = h[key].encode("utf8", "ignore").decode("utf8")
    return results

def wrap_es_execution(search: Search) -> Any:
    """
    Executes a Search object, and converts various ES error types into
    something we can pretty print to the user.
    """
    try:
        resp = search.execute()
    except elasticsearch.exceptions.RequestError as e:
        # this is a "user" error
        print("elasticsearch 400: " + str(e.info), file=sys.stderr)
        if e.info.get("error", {}).get("root_cause", {}):
            raise ValueError(str(e.info["error"]["root_cause"][0].get("reason")))
        else:
            raise ValueError(str(e.info))
    except elasticsearch.exceptions.TransportError as e:
        # all other errors
        print("elasticsearch non-200 status code: {}".format(e.info), file=sys.stderr)
        raise IOError(str(e.info))
    return resp

def do_container_search(
    query: GenericQuery, deep_page_limit: int = 2000
) -> SearchHits:

    search = Search(using=app.es_client, index=app.config['ELASTICSEARCH_CONTAINER_INDEX'])

    search = search.query(
        "query_string",
        query=query.q,
        default_operator="AND",
        analyze_wildcard=True,
        allow_leading_wildcard=False,
        lenient=True,
        fields=["biblio"],
    )

    # Sanity checks
    limit = min((int(query.limit or 25), 100))
    offset = max((int(query.offset or 0), 0))
    if offset > deep_page_limit:
        # Avoid deep paging problem.
        offset = deep_page_limit

    search = search[offset : (offset + limit)]

    resp = wrap_es_execution(search)
    results = results_to_dict(resp)

    return SearchHits(
        count_returned=len(results),
        count_found=int(resp.hits.total),
        offset=offset,
        limit=limit,
        deep_page_limit=deep_page_limit,
        query_time_ms=int(resp.took),
        results=results,
    )

def do_release_search(
    query: ReleaseQuery, deep_page_limit: int = 2000
) -> SearchHits:

    search = Search(using=app.es_client, index=app.config['ELASTICSEARCH_RELEASE_INDEX'])

    # availability filters
    if query.fulltext_only:
        search = search.filter("term", in_ia=True)

    # Below, we combine several queries to improve scoring.

    # this query use the fancy built-in query string parser
    basic_biblio = Q(
        "query_string",
        query=query.q,
        default_operator="AND",
        analyze_wildcard=True,
        allow_leading_wildcard=False,
        lenient=True,
        fields=[
            "title^2",
            "biblio",
        ],
    )
    has_fulltext = Q("term", in_ia=True)
    poor_metadata = Q(
        "bool",
        should=[
            # if these fields aren't set, metadata is poor. The more that do
            # not exist, the stronger the signal.
            Q("bool", must_not=Q("exists", field="title")),
            Q("bool", must_not=Q("exists", field="release_year")),
            Q("bool", must_not=Q("exists", field="release_type")),
            Q("bool", must_not=Q("exists", field="release_stage")),
        ],
    )

    search = search.query(
        "boosting",
        positive=Q("bool", must=basic_biblio, should=[has_fulltext],),
        negative=poor_metadata,
        negative_boost=0.5,
    )

    # Sanity checks
    limit = min((int(query.limit or 25), 100))
    offset = max((int(query.offset or 0), 0))
    if offset > deep_page_limit:
        # Avoid deep paging problem.
        offset = deep_page_limit

    search = search[offset : (offset + limit)]

    resp = wrap_es_execution(search)
    results = results_to_dict(resp)

    for h in results:
        # Ensure 'contrib_names' is a list, not a single string
        if type(h['contrib_names']) is not list:
            h['contrib_names'] = [h['contrib_names'], ]
        h['contrib_names'] = [name.encode('utf8', 'ignore').decode('utf8') for name in h['contrib_names']]

    return SearchHits(
        count_returned=len(results),
        count_found=int(resp.hits.total),
        offset=offset,
        limit=limit,
        deep_page_limit=deep_page_limit,
        query_time_ms=int(resp.took),
        results=results,
    )

def get_elastic_container_random_releases(ident, limit=5):
    """
    Returns a list of releases from the container.
    """

    assert limit > 0 and limit <= 100

    search = Search(using=app.es_client, index=app.config['ELASTICSEARCH_RELEASE_INDEX'])
    search = search.query(
        'bool',
        must=[
            Q('term', container_id=ident),
            Q('range', release_year={ "lte": datetime.datetime.today().year }),
        ]
    )
    search = search.sort('-in_web', '-release_date')
    search = search.params(request_cache=True)
    search = search[:int(limit)]

    resp = wrap_es_execution(search)
    results = results_to_dict(resp)

    return results

def get_elastic_entity_stats():
    """
    TODO: files, filesets, webcaptures (no schema yet)

    Returns dict:
        changelog: {latest: {index, datetime}}
        release: {total, refs_total}
        papers: {total, in_web, in_oa, in_kbart, in_web_not_kbart}
    """

    stats = {}

    # release totals
    search = Search(using=app.es_client, index=app.config['ELASTICSEARCH_RELEASE_INDEX'])
    search = search.params(request_cache=True)
    search.aggs.bucket(
        'release_ref_count',
        'sum',
        field='ref_count',
    )
    search = search[:0]  # pylint: disable=unsubscriptable-object

    resp = wrap_es_execution(search)

    stats['release'] = {
        "total": int(resp.hits.total),
        "refs_total": int(resp.aggregations.release_ref_count.value),
    }

    # paper counts
    search = Search(using=app.es_client, index=app.config['ELASTICSEARCH_RELEASE_INDEX'])
    search = search.query(
        'terms',
        release_type=[
            "article-journal",
            "paper-conference",
            # "chapter",
            # "thesis",
        ],
    )
    search = search.params(request_cache=True)
    search.aggs.bucket(
        'paper_like',
        'filters',
        filters={
            "in_web": { "term": { "in_web": "true" } },
            "is_oa": { "term": { "is_oa": "true" } },
            "in_kbart": { "term": { "in_kbart": "true" } },
            "in_web_not_kbart": { "bool": { "filter": [
                { "term": { "in_web": "true" } },
                { "term": { "in_kbart": "false" } },
            ]}},
        }
    )
    search = search[:0]

    resp = wrap_es_execution(search)
    buckets = resp.aggregations.paper_like.buckets
    stats['papers'] = {
        'total': resp.hits.total,
        'in_web': buckets.in_web.doc_count,
        'is_oa': buckets.is_oa.doc_count,
        'in_kbart': buckets.in_kbart.doc_count,
        'in_web_not_kbart': buckets.in_web_not_kbart.doc_count,
    }

    # container counts
    search = Search(using=app.es_client, index=app.config['ELASTICSEARCH_CONTAINER_INDEX'])
    search = search.params(request_cache=True)
    search.aggs.bucket(
        'release_ref_count',
        'sum',
        field='ref_count',
    )
    search = search[:0]  # pylint: disable=unsubscriptable-object

    resp = wrap_es_execution(search)
    stats['container'] = {
        "total": resp.hits.total,
    }

    return stats

def get_elastic_container_stats(ident, issnl=None):
    """
    Returns dict:
        ident
        issnl (optional)
        total
        in_web
        in_kbart
        preserved
    """

    search = Search(using=app.es_client, index=app.config['ELASTICSEARCH_RELEASE_INDEX'])
    search = search.params(request_cache=True)
    search = search.query(
        'term',
        container_id=ident,
    )
    search.aggs.bucket(
        'container_stats',
        'filters',
        filters={
            "in_web": {
                "term": { "in_web": True },
            },
            "in_kbart": {
                "term": { "in_kbart": True },
            },
            "is_preserved": {
                "term": { "is_preserved": True },
            },
        },
    )
    search = search[:0]

    resp = wrap_es_execution(search)

    buckets = resp.aggregations.container_stats.buckets
    stats = {
        'ident': ident,
        'issnl': issnl,
        'total': resp.hits.total,
        'in_web': buckets['in_web']['doc_count'],
        'in_kbart': buckets['in_kbart']['doc_count'],
        'is_preserved': buckets['is_preserved']['doc_count'],
    }

    return stats

def get_elastic_container_histogram(ident):
    """
    Fetches a stacked histogram

    Filters to the past 500 years (at most), or about 1000 values.

    Returns a list of tuples:
        (year, in_ia, count)
    """

    search = Search(using=app.es_client, index=app.config['ELASTICSEARCH_RELEASE_INDEX'])
    search = search.params(request_cache='true')
    search = search.query(
        'bool',
        must=[
            Q("range", release_year={
                "gte": datetime.datetime.today().year - 499,
                "lte": datetime.datetime.today().year,
            }),
        ],
        filter=[
            Q("bool", minimum_should_match=1, should=[
                Q("match", container_id=ident),
            ]),
        ],
    )
    search.aggs.bucket(
        'year_in_ia',
        'composite',
        size=1000,
        sources=[
            {"year": {
                "histogram": {
                    "field": "release_year",
                    "interval": 1,
                },
            }},
            {"in_ia": {
                "terms": {
                    "field": "in_ia",
                },
            }},
        ],
    )
    search = search[:0]

    resp = wrap_es_execution(search)

    buckets = resp.aggregations.year_in_ia.buckets
    vals = [(h['key']['year'], h['key']['in_ia'], h['doc_count'])
            for h in buckets]
    vals = sorted(vals)
    return vals
