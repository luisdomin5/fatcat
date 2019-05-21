
import sys
import json
import datetime
import warnings
from bs4 import BeautifulSoup

import fatcat_client
from .common import EntityImporter, clean, LANG_MAP_MARC

# TODO: more entries?
JSTOR_CONTRIB_MAP = {
    'author': 'author',
    'editor': 'editor',
    'translator': 'translator',
    'illustrator': 'illustrator',
}

class JstorImporter(EntityImporter):
    """
    Importer for JSTOR bulk XML metadata (eg, from their Early Journals
    Collection)
    """

    def __init__(self, api, issn_map_file, **kwargs):

        eg_desc = kwargs.get('editgroup_description',
            "Automated import of JSTOR XML metadata")
        eg_extra = kwargs.get('editgroup_extra', dict())
        eg_extra['agent'] = eg_extra.get('agent', 'fatcat_tools.JstorImporter')
        super().__init__(api,
            issn_map_file=issn_map_file,
            editgroup_description=eg_desc,
            editgroup_extra=eg_extra,
            **kwargs)

        self.create_containers = kwargs.get('create_containers')

        self.read_issn_map_file(issn_map_file)

    def want(self, obj):
        return True

    def parse_record(self, article):

        journal_meta = article.front.find("journal-meta")
        article_meta = article.front.find("article-meta")

        extra = dict()
        extra_jstor = dict()

        # JSTOR journal-id
        journal_ids = [j.string for j in journal_meta.find_all('journal-id')]
        if journal_ids:
            extra_jstor['journal_ids'] = journal_ids

        journal_title = journal_meta.find("journal-title").string
        publisher = journal_meta.find("publisher-name").string
        issn = journal_meta.find("issn")
        if issn:
            issn = issn.string
            if len(issn) == 8:
                issn = "{}-{}".format(issn[0:4], issn[4:8])
            else:
                assert len(issn) == 9

        issnl = self.issn2issnl(issn)
        container_id = None
        if issnl:
            container_id = self.lookup_issnl(issnl)

        # create container if it doesn't exist
        if (container_id is None and self.create_containers and (issnl is not None)
                and journal_title):
            ce = fatcat_client.ContainerEntity(
                issnl=issnl,
                publisher=publisher,
                container_type=self.map_container_type(release_type),
                name=clean(journal_title, force_xml=True),
                extra=journal_extra)
            ce_edit = self.create_container(ce)
            container_id = ce_edit.ident
            self._issnl_id_map[issnl] = container_id

        doi = article_meta.find("article-id", {"pub-id-type": "doi"})
        if doi:
            doi = doi.string.lower().strip()

        jstor_id = article_meta.find("article-id", {"pub-id-type": "jstor"})
        if jstor_id:
            jstor_id = jstor_id.string

        title = article_meta.find("article-title")
        if title:
            title = title.string.strip()
            if title.endswith('.'):
                title = title[:-1]

        contribs = []
        cgroup = article_meta.find("contrib-group")
        if cgroup:
            for c in cgroup.find_all("contrib"):
                given = c.find("given-names")
                surname = c.find("surname")
                if given and surname:
                    name = "{} {}".format(given.string, surname.string)
                elif surname:
                    name = surname.string
                else:
                    name = None
                role = JSTOR_CONTRIB_MAP.get(c['contrib-type'])
                if not role and c['contrib-type']:
                    sys.stderr.write("NOT IN JSTOR_CONTRIB_MAP: {}".format(c['contrib-type']))
                contribs.append(fatcat_client.ReleaseContrib(
                    role=JSTOR_CONTRIB_MAP.get(c['contrib-type']),
                    raw_name=clean(name),
                    given_name=clean(given.string),
                    surname=clean(surname.string),
                ))

        release_year = None
        release_date = None
        pub_date = article_meta.find('pub-date')
        if pub_date and pub_date.year:
            release_year = int(pub_date.year.string)
            if pub_date.month and pub_date.day:
                release_date = datetime.date(
                    release_year,
                    int(pub_date.month.string),
                    int(pub_date.day.string))
                if release_date.day == 1 and release_date.month == 1:
                    # suspect jan 1st dates get set by JSTOR when actual
                    # date not known (citation needed), so drop them
                    release_date = None
        
        volume = None
        if article_meta.volume:
            volume = article_meta.volume.string or None

        issue = None
        if article_meta.issue:
            issue = article_meta.issue.string or None

        pages = None
        if article_meta.find("page-range"):
            pages = article_meta.find("page-range").string
        elif article_meta.fpage:
            pages = article_meta.fpage.string

        language = None
        cm = article_meta.find("custom-meta")
        if cm.find("meta-name").string == "lang":
            language = cm.find("meta-value").string
            language = LANG_MAP_MARC.get(language)
            if not language:
                warnings.warn("MISSING MARC LANG: {}".format(cm.find("meta-value").string))

        release_type = "article-journal"
        if "[Abstract]" in title:
            # TODO: strip the "[Abstract]" bit?
            release_type = "abstract"
        elif "[Editorial" in title:
            release_type = "editorial"
        elif "[Letter" in title:
            release_type = "letter"
        elif "[Poem" in title or "[Photograph" in title:
            release_type = None

        if title.startswith("[") and title.endswith("]"):
            # strip brackets if that is all that is there (eg, translation or non-english)
            title = title[1:-1]

        # JSTOR issue-id
        if article_meta.find('issue-id'):
            issue_id = clean(article_meta.find('issue-id').string)
            if issue_id:
                extra_jstor['issue_id'] = issue_id

        # everything in JSTOR is published
        release_stage = "published"

        # extra:
        #   withdrawn_date
        #   translation_of
        #   subtitle
        #   aliases
        #   container_name
        #   group-title
        #   pubmed: retraction refs
        if extra_jstor:
            extra['jstor'] = extra_jstor
        if not extra:
            extra = None

        re = fatcat_client.ReleaseEntity(
            #work_id
            title=title,
            #original_title
            release_type=release_type,
            release_stage=release_stage,
            release_date=release_date,
            release_year=release_year,
            ext_ids=fatcat_client.ReleaseExtIds(
                doi=doi,
                jstor=jstor_id,
            ),
            volume=volume,
            issue=issue,
            pages=pages,
            publisher=publisher,
            language=language,
            #license_slug

            # content, mimetype, lang
            #abstracts=abstracts,

            contribs=contribs,

            # key, year, container_name, title, locator
            # extra: volume, authors, issue, publisher, identifiers
            #refs=refs,

            #   name, type, publisher, issnl
            #   extra: issnp, issne, original_name, languages, country
            container_id=container_id,

            extra=extra,
        )
        return re

    def try_update(self, re):

        # first, lookup existing by JSTOR id (which much be defined)
        existing = None
        try:
            existing = self.api.lookup_release(jstor=re.ext_ids.jstor)
        except fatcat_client.rest.ApiException as err:
            if err.status != 404:
                raise err

        # then try DOI lookup if there is one (try JSTOR prefix+jstor_id if
        # there isn't a DOI set)
        if not existing:
            doi = re.ext_ids.doi
            if not doi:
                doi = "10.2307/{}".format(re.ext_ids.jstor)
            try:
                existing = self.api.lookup_release(doi=doi)
            except fatcat_client.rest.ApiException as err:
                if err.status != 404:
                    raise err

        if existing and existing.ext_ids.jstor:
            # don't update if it already has JSTOR ID
            self.counts['exists'] += 1
            return False
        elif existing:
            # but do update if only DOI was set
            existing.ext_ids.jstor = re.ext_ids.jstor
            existing.extra['jstor'] = re.extra['jstor']
            self.api.update_release(self.get_editgroup_id(), existing.ident, existing)
            self.counts['update'] += 1
            return False

        return True

    def insert_batch(self, batch):
        self.api.create_release_auto_batch(fatcat_client.ReleaseAutoBatch(
            editgroup=fatcat_client.Editgroup(
                description=self.editgroup_description,
                extra=self.editgroup_extra),
            entity_list=batch))

    def parse_file(self, handle):

        # 1. open with beautiful soup
        soup = BeautifulSoup(handle, "xml")

        # 2. iterate over articles, call parse_article on each
        for article in soup.find_all("article"):
            resp = self.parse_record(article)
            print(json.dumps(resp))
            #sys.exit(-1)

if __name__=='__main__':
    parser = JstorImporter(None, None)
    parser.parse_file(open(sys.argv[1]))