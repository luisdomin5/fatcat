# coding: utf-8

"""
    fatcat

    A scalable, versioned, API-oriented catalog of bibliographic entities and file metadata  # noqa: E501

    OpenAPI spec version: 0.1.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from fatcat_client.models.release_contrib import ReleaseContrib  # noqa: F401,E501
from fatcat_client.models.release_ref import ReleaseRef  # noqa: F401,E501


class ReleaseEntity(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'refs': 'list[ReleaseRef]',
        'contribs': 'list[ReleaseContrib]',
        'language': 'str',
        'publisher': 'str',
        'pages': 'str',
        'issue': 'str',
        'volume': 'str',
        'isbn13': 'str',
        'doi': 'str',
        'release_date': 'date',
        'release_status': 'str',
        'release_type': 'str',
        'container_id': 'str',
        'work_id': 'str',
        'title': 'str',
        'state': 'str',
        'ident': 'str',
        'revision': 'int',
        'redirect': 'str',
        'editgroup_id': 'int',
        'extra': 'object'
    }

    attribute_map = {
        'refs': 'refs',
        'contribs': 'contribs',
        'language': 'language',
        'publisher': 'publisher',
        'pages': 'pages',
        'issue': 'issue',
        'volume': 'volume',
        'isbn13': 'isbn13',
        'doi': 'doi',
        'release_date': 'release_date',
        'release_status': 'release_status',
        'release_type': 'release_type',
        'container_id': 'container_id',
        'work_id': 'work_id',
        'title': 'title',
        'state': 'state',
        'ident': 'ident',
        'revision': 'revision',
        'redirect': 'redirect',
        'editgroup_id': 'editgroup_id',
        'extra': 'extra'
    }

    def __init__(self, refs=None, contribs=None, language=None, publisher=None, pages=None, issue=None, volume=None, isbn13=None, doi=None, release_date=None, release_status=None, release_type=None, container_id=None, work_id=None, title=None, state=None, ident=None, revision=None, redirect=None, editgroup_id=None, extra=None):  # noqa: E501
        """ReleaseEntity - a model defined in Swagger"""  # noqa: E501

        self._refs = None
        self._contribs = None
        self._language = None
        self._publisher = None
        self._pages = None
        self._issue = None
        self._volume = None
        self._isbn13 = None
        self._doi = None
        self._release_date = None
        self._release_status = None
        self._release_type = None
        self._container_id = None
        self._work_id = None
        self._title = None
        self._state = None
        self._ident = None
        self._revision = None
        self._redirect = None
        self._editgroup_id = None
        self._extra = None
        self.discriminator = None

        if refs is not None:
            self.refs = refs
        if contribs is not None:
            self.contribs = contribs
        if language is not None:
            self.language = language
        if publisher is not None:
            self.publisher = publisher
        if pages is not None:
            self.pages = pages
        if issue is not None:
            self.issue = issue
        if volume is not None:
            self.volume = volume
        if isbn13 is not None:
            self.isbn13 = isbn13
        if doi is not None:
            self.doi = doi
        if release_date is not None:
            self.release_date = release_date
        if release_status is not None:
            self.release_status = release_status
        if release_type is not None:
            self.release_type = release_type
        if container_id is not None:
            self.container_id = container_id
        self.work_id = work_id
        self.title = title
        if state is not None:
            self.state = state
        if ident is not None:
            self.ident = ident
        if revision is not None:
            self.revision = revision
        if redirect is not None:
            self.redirect = redirect
        if editgroup_id is not None:
            self.editgroup_id = editgroup_id
        if extra is not None:
            self.extra = extra

    @property
    def refs(self):
        """Gets the refs of this ReleaseEntity.  # noqa: E501


        :return: The refs of this ReleaseEntity.  # noqa: E501
        :rtype: list[ReleaseRef]
        """
        return self._refs

    @refs.setter
    def refs(self, refs):
        """Sets the refs of this ReleaseEntity.


        :param refs: The refs of this ReleaseEntity.  # noqa: E501
        :type: list[ReleaseRef]
        """

        self._refs = refs

    @property
    def contribs(self):
        """Gets the contribs of this ReleaseEntity.  # noqa: E501


        :return: The contribs of this ReleaseEntity.  # noqa: E501
        :rtype: list[ReleaseContrib]
        """
        return self._contribs

    @contribs.setter
    def contribs(self, contribs):
        """Sets the contribs of this ReleaseEntity.


        :param contribs: The contribs of this ReleaseEntity.  # noqa: E501
        :type: list[ReleaseContrib]
        """

        self._contribs = contribs

    @property
    def language(self):
        """Gets the language of this ReleaseEntity.  # noqa: E501

        Two-letter RFC1766/ISO639-1 language code, with extensions  # noqa: E501

        :return: The language of this ReleaseEntity.  # noqa: E501
        :rtype: str
        """
        return self._language

    @language.setter
    def language(self, language):
        """Sets the language of this ReleaseEntity.

        Two-letter RFC1766/ISO639-1 language code, with extensions  # noqa: E501

        :param language: The language of this ReleaseEntity.  # noqa: E501
        :type: str
        """

        self._language = language

    @property
    def publisher(self):
        """Gets the publisher of this ReleaseEntity.  # noqa: E501


        :return: The publisher of this ReleaseEntity.  # noqa: E501
        :rtype: str
        """
        return self._publisher

    @publisher.setter
    def publisher(self, publisher):
        """Sets the publisher of this ReleaseEntity.


        :param publisher: The publisher of this ReleaseEntity.  # noqa: E501
        :type: str
        """

        self._publisher = publisher

    @property
    def pages(self):
        """Gets the pages of this ReleaseEntity.  # noqa: E501


        :return: The pages of this ReleaseEntity.  # noqa: E501
        :rtype: str
        """
        return self._pages

    @pages.setter
    def pages(self, pages):
        """Sets the pages of this ReleaseEntity.


        :param pages: The pages of this ReleaseEntity.  # noqa: E501
        :type: str
        """

        self._pages = pages

    @property
    def issue(self):
        """Gets the issue of this ReleaseEntity.  # noqa: E501


        :return: The issue of this ReleaseEntity.  # noqa: E501
        :rtype: str
        """
        return self._issue

    @issue.setter
    def issue(self, issue):
        """Sets the issue of this ReleaseEntity.


        :param issue: The issue of this ReleaseEntity.  # noqa: E501
        :type: str
        """

        self._issue = issue

    @property
    def volume(self):
        """Gets the volume of this ReleaseEntity.  # noqa: E501


        :return: The volume of this ReleaseEntity.  # noqa: E501
        :rtype: str
        """
        return self._volume

    @volume.setter
    def volume(self, volume):
        """Sets the volume of this ReleaseEntity.


        :param volume: The volume of this ReleaseEntity.  # noqa: E501
        :type: str
        """

        self._volume = volume

    @property
    def isbn13(self):
        """Gets the isbn13 of this ReleaseEntity.  # noqa: E501


        :return: The isbn13 of this ReleaseEntity.  # noqa: E501
        :rtype: str
        """
        return self._isbn13

    @isbn13.setter
    def isbn13(self, isbn13):
        """Sets the isbn13 of this ReleaseEntity.


        :param isbn13: The isbn13 of this ReleaseEntity.  # noqa: E501
        :type: str
        """

        self._isbn13 = isbn13

    @property
    def doi(self):
        """Gets the doi of this ReleaseEntity.  # noqa: E501


        :return: The doi of this ReleaseEntity.  # noqa: E501
        :rtype: str
        """
        return self._doi

    @doi.setter
    def doi(self, doi):
        """Sets the doi of this ReleaseEntity.


        :param doi: The doi of this ReleaseEntity.  # noqa: E501
        :type: str
        """

        self._doi = doi

    @property
    def release_date(self):
        """Gets the release_date of this ReleaseEntity.  # noqa: E501


        :return: The release_date of this ReleaseEntity.  # noqa: E501
        :rtype: date
        """
        return self._release_date

    @release_date.setter
    def release_date(self, release_date):
        """Sets the release_date of this ReleaseEntity.


        :param release_date: The release_date of this ReleaseEntity.  # noqa: E501
        :type: date
        """

        self._release_date = release_date

    @property
    def release_status(self):
        """Gets the release_status of this ReleaseEntity.  # noqa: E501


        :return: The release_status of this ReleaseEntity.  # noqa: E501
        :rtype: str
        """
        return self._release_status

    @release_status.setter
    def release_status(self, release_status):
        """Sets the release_status of this ReleaseEntity.


        :param release_status: The release_status of this ReleaseEntity.  # noqa: E501
        :type: str
        """

        self._release_status = release_status

    @property
    def release_type(self):
        """Gets the release_type of this ReleaseEntity.  # noqa: E501


        :return: The release_type of this ReleaseEntity.  # noqa: E501
        :rtype: str
        """
        return self._release_type

    @release_type.setter
    def release_type(self, release_type):
        """Sets the release_type of this ReleaseEntity.


        :param release_type: The release_type of this ReleaseEntity.  # noqa: E501
        :type: str
        """

        self._release_type = release_type

    @property
    def container_id(self):
        """Gets the container_id of this ReleaseEntity.  # noqa: E501


        :return: The container_id of this ReleaseEntity.  # noqa: E501
        :rtype: str
        """
        return self._container_id

    @container_id.setter
    def container_id(self, container_id):
        """Sets the container_id of this ReleaseEntity.


        :param container_id: The container_id of this ReleaseEntity.  # noqa: E501
        :type: str
        """

        self._container_id = container_id

    @property
    def work_id(self):
        """Gets the work_id of this ReleaseEntity.  # noqa: E501


        :return: The work_id of this ReleaseEntity.  # noqa: E501
        :rtype: str
        """
        return self._work_id

    @work_id.setter
    def work_id(self, work_id):
        """Sets the work_id of this ReleaseEntity.


        :param work_id: The work_id of this ReleaseEntity.  # noqa: E501
        :type: str
        """
        if work_id is None:
            raise ValueError("Invalid value for `work_id`, must not be `None`")  # noqa: E501

        self._work_id = work_id

    @property
    def title(self):
        """Gets the title of this ReleaseEntity.  # noqa: E501


        :return: The title of this ReleaseEntity.  # noqa: E501
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title):
        """Sets the title of this ReleaseEntity.


        :param title: The title of this ReleaseEntity.  # noqa: E501
        :type: str
        """
        if title is None:
            raise ValueError("Invalid value for `title`, must not be `None`")  # noqa: E501

        self._title = title

    @property
    def state(self):
        """Gets the state of this ReleaseEntity.  # noqa: E501


        :return: The state of this ReleaseEntity.  # noqa: E501
        :rtype: str
        """
        return self._state

    @state.setter
    def state(self, state):
        """Sets the state of this ReleaseEntity.


        :param state: The state of this ReleaseEntity.  # noqa: E501
        :type: str
        """
        allowed_values = ["wip", "active", "redirect", "deleted"]  # noqa: E501
        if state not in allowed_values:
            raise ValueError(
                "Invalid value for `state` ({0}), must be one of {1}"  # noqa: E501
                .format(state, allowed_values)
            )

        self._state = state

    @property
    def ident(self):
        """Gets the ident of this ReleaseEntity.  # noqa: E501


        :return: The ident of this ReleaseEntity.  # noqa: E501
        :rtype: str
        """
        return self._ident

    @ident.setter
    def ident(self, ident):
        """Sets the ident of this ReleaseEntity.


        :param ident: The ident of this ReleaseEntity.  # noqa: E501
        :type: str
        """

        self._ident = ident

    @property
    def revision(self):
        """Gets the revision of this ReleaseEntity.  # noqa: E501


        :return: The revision of this ReleaseEntity.  # noqa: E501
        :rtype: int
        """
        return self._revision

    @revision.setter
    def revision(self, revision):
        """Sets the revision of this ReleaseEntity.


        :param revision: The revision of this ReleaseEntity.  # noqa: E501
        :type: int
        """

        self._revision = revision

    @property
    def redirect(self):
        """Gets the redirect of this ReleaseEntity.  # noqa: E501


        :return: The redirect of this ReleaseEntity.  # noqa: E501
        :rtype: str
        """
        return self._redirect

    @redirect.setter
    def redirect(self, redirect):
        """Sets the redirect of this ReleaseEntity.


        :param redirect: The redirect of this ReleaseEntity.  # noqa: E501
        :type: str
        """

        self._redirect = redirect

    @property
    def editgroup_id(self):
        """Gets the editgroup_id of this ReleaseEntity.  # noqa: E501


        :return: The editgroup_id of this ReleaseEntity.  # noqa: E501
        :rtype: int
        """
        return self._editgroup_id

    @editgroup_id.setter
    def editgroup_id(self, editgroup_id):
        """Sets the editgroup_id of this ReleaseEntity.


        :param editgroup_id: The editgroup_id of this ReleaseEntity.  # noqa: E501
        :type: int
        """

        self._editgroup_id = editgroup_id

    @property
    def extra(self):
        """Gets the extra of this ReleaseEntity.  # noqa: E501


        :return: The extra of this ReleaseEntity.  # noqa: E501
        :rtype: object
        """
        return self._extra

    @extra.setter
    def extra(self, extra):
        """Sets the extra of this ReleaseEntity.


        :param extra: The extra of this ReleaseEntity.  # noqa: E501
        :type: object
        """

        self._extra = extra

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, ReleaseEntity):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
