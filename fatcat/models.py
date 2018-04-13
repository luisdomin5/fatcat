
"""
states for identifiers:
- pre-live: points to a rev (during edit/accept period)
- live: points to a rev
- redirect: live, points to upstream rev, also points to redirect id
    => if live and redirect non-null, all other fields copied from redirect target
- deleted: live, but doesn't point to a rev

possible refactors:
- '_rev' instead of '_rev'
- use mixins for entities
"""

from fatcat import db


### Inter-Entity Relationships ###############################################

class WorkContrib(db.Model):
    __tablename__ = "work_contrib"
    work_rev= db.Column(db.ForeignKey('work_rev.id'), nullable=False, primary_key=True)
    creator_ident_id = db.Column(db.ForeignKey('creator_ident.id'), nullable=False, primary_key=True)
    type = db.Column(db.String, nullable=True)
    stub = db.Column(db.String, nullable=True)

    creator = db.relationship("CreatorIdent")
    work = db.relationship("WorkRev")

class ReleaseContrib(db.Model):
    __tablename__ = "release_contrib"
    release_rev = db.Column(db.ForeignKey('release_rev.id'), nullable=False, primary_key=True)
    creator_ident_id = db.Column(db.ForeignKey('creator_ident.id'), nullable=False, primary_key=True)
    type = db.Column(db.String, nullable=True)
    stub = db.Column(db.String, nullable=True)

    creator = db.relationship("CreatorIdent")
    release = db.relationship("ReleaseRev")

class ReleaseRef(db.Model):
    __tablename__ = "release_ref"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    release_rev = db.Column(db.ForeignKey('release_rev.id'), nullable=False)
    target_release_ident_id = db.Column(db.ForeignKey('release_ident.id'), nullable=True)
    index = db.Column(db.Integer, nullable=True)
    stub = db.Column(db.String, nullable=True)
    doi = db.Column(db.String, nullable=True)

    release = db.relationship("ReleaseRev")
    target = db.relationship("ReleaseIdent")

class FileRelease(db.Model):
    __tablename__ = "file_release"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    file_rev= db.Column(db.ForeignKey('file_rev.id'), nullable=False)
    release_ident_id = db.Column(db.ForeignKey('release_ident.id'), nullable=False)

    release = db.relationship("ReleaseIdent")
    file = db.relationship("FileRev")


### Entities #################################################################

class WorkRev(db.Model):
    __tablename__ = 'work_rev'
    id = db.Column(db.Integer, primary_key=True)
    edit_id = db.Column(db.ForeignKey('work_edit.id'))
    extra_json = db.Column(db.ForeignKey('extra_json.sha1'), nullable=True)

    title = db.Column(db.String)
    work_type = db.Column(db.String)
    primary_release_id = db.Column(db.ForeignKey('release_ident.id'), nullable=True)

    creators = db.relationship('WorkContrib', lazy='subquery',
        backref=db.backref('works', lazy=True))

class WorkIdent(db.Model):
    """
    If rev_id is null, this was deleted.
    If redirect_id is not null, this has been merged with the given id. In this
        case rev_id is a "cached" copy of the redirect's rev_id, as
        an optimization. If the merged work is "deleted", rev_id can be
        null and redirect_id not-null.
    """
    __tablename__ = 'work_ident'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    live = db.Column(db.Boolean, nullable=False, default=False)
    rev_id = db.Column(db.ForeignKey('work_rev.id'), nullable=True)
    redirect_id = db.Column(db.ForeignKey('work_ident.id'), nullable=True)
    revision = db.relationship("WorkRev")

class WorkEdit(db.Model):
    __tablename__ = 'work_edit'
    id = db.Column(db.Integer, primary_key=True)
    ident_id = db.Column(db.ForeignKey('work_ident.id'), nullable=True)
    rev_id = db.Column(db.ForeignKey('work_rev.id'), nullable=True)
    redirect_id = db.Column(db.ForeignKey('work_ident.id'), nullable=True)
    edit_group = db.Column(db.ForeignKey('edit_group.id'), nullable=True)
    extra_json = db.Column(db.ForeignKey('extra_json.sha1'), nullable=True)


class ReleaseRev(db.Model):
    __tablename__ = 'release_rev'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    edit_id = db.Column(db.ForeignKey('release_edit.id'))
    extra_json = db.Column(db.ForeignKey('extra_json.sha1'), nullable=True)

    work_ident_id = db.ForeignKey('work_ident.id')
    container_ident_id = db.Column(db.ForeignKey('container_ident.id'), nullable=True)
    title = db.Column(db.String, nullable=False)
    license = db.Column(db.String, nullable=True)   # TODO: oa status foreign key
    release_type = db.Column(db.String)             # TODO: foreign key
    date = db.Column(db.String, nullable=True)      # TODO: datetime
    doi = db.Column(db.String, nullable=True)       # TODO: identifier table
    volume = db.Column(db.String, nullable=True)
    pages = db.Column(db.String, nullable=True)
    issue = db.Column(db.String, nullable=True)

    #work = db.relationship("WorkIdent", lazy='subquery')
    container = db.relationship("ContainerIdent", lazy='subquery')
    creators = db.relationship('ReleaseContrib', lazy='subquery')
    refs = db.relationship('ReleaseRef', lazy='subquery')

class ReleaseIdent(db.Model):
    __tablename__ = 'release_ident'
    id = db.Column(db.Integer, primary_key=True)
    live = db.Column(db.Boolean, nullable=False, default=False)
    rev_id = db.Column(db.ForeignKey('release_rev.id'))
    redirect_id = db.Column(db.ForeignKey('release_ident.id'), nullable=True)
    revision = db.relationship("ReleaseRev")

class ReleaseEdit(db.Model):
    __tablename__ = 'release_edit'
    id = db.Column(db.Integer, primary_key=True)
    ident_id = db.Column(db.ForeignKey('release_ident.id'), nullable=True)
    rev_id = db.Column(db.ForeignKey('release_rev.id'), nullable=True)
    redirect_id = db.Column(db.ForeignKey('release_ident.id'), nullable=True)
    edit_group = db.Column(db.ForeignKey('edit_group.id'), nullable=True)
    extra_json = db.Column(db.ForeignKey('extra_json.sha1'), nullable=True)


class CreatorRev(db.Model):
    __tablename__ = 'creator_rev'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    edit_id = db.Column(db.ForeignKey('creator_edit.id'))
    extra_json = db.Column(db.ForeignKey('extra_json.sha1'), nullable=True)

    name = db.Column(db.String)
    sortname = db.Column(db.String)
    orcid = db.Column(db.String)            # TODO: identifier table

class CreatorIdent(db.Model):
    __tablename__ = 'creator_ident'
    id = db.Column(db.Integer, primary_key=True)
    live = db.Column(db.Boolean, nullable=False, default=False)
    rev_id = db.Column(db.ForeignKey('creator_rev.id'))
    redirect_id = db.Column(db.ForeignKey('creator_ident.id'), nullable=True)
    revision = db.relationship("CreatorRev")

class CreatorEdit(db.Model):
    __tablename__ = 'creator_edit'
    id = db.Column(db.Integer, primary_key=True)
    ident_id = db.Column(db.ForeignKey('creator_ident.id'), nullable=True)
    rev_id = db.Column(db.ForeignKey('creator_rev.id'), nullable=True)
    redirect_id = db.Column(db.ForeignKey('creator_ident.id'), nullable=True)
    edit_group = db.Column(db.ForeignKey('edit_group.id'), nullable=True)
    extra_json = db.Column(db.ForeignKey('extra_json.sha1'), nullable=True)


class ContainerRev(db.Model):
    __tablename__ = 'container_rev'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    edit_id = db.Column(db.ForeignKey('container_edit.id'))
    extra_json = db.Column(db.ForeignKey('extra_json.sha1'), nullable=True)

    name = db.Column(db.String)
    #XXX: container_ident_id = db.Column(db.ForeignKey('container_ident.id'))
    publisher = db.Column(db.String)        # TODO: foreign key
    sortname = db.Column(db.String)
    issn = db.Column(db.String)             # TODO: identifier table

class ContainerIdent(db.Model):
    __tablename__ = 'container_ident'
    id = db.Column(db.Integer, primary_key=True)
    live = db.Column(db.Boolean, nullable=False, default=False)
    rev_id = db.Column(db.ForeignKey('container_rev.id'))
    redirect_id = db.Column(db.ForeignKey('container_ident.id'), nullable=True)
    revision = db.relationship("ContainerRev")

class ContainerEdit(db.Model):
    __tablename__ = 'container_edit'
    id = db.Column(db.Integer, primary_key=True)
    ident_id = db.Column(db.ForeignKey('container_ident.id'), nullable=True)
    rev_id = db.Column(db.ForeignKey('container_rev.id'), nullable=True)
    redirect_id = db.Column(db.ForeignKey('container_ident.id'), nullable=True)
    edit_group = db.Column(db.ForeignKey('edit_group.id'), nullable=True)
    extra_json = db.Column(db.ForeignKey('extra_json.sha1'), nullable=True)


class FileRev(db.Model):
    __tablename__ = 'file_rev'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    edit_id = db.Column(db.ForeignKey('file_edit.id'))
    extra_json = db.Column(db.ForeignKey('extra_json.sha1'), nullable=True)

    size = db.Column(db.Integer)
    sha1 = db.Column(db.Integer)            # TODO: hash table... only or in addition?
    url = db.Column(db.Integer)             # TODO: URL table
    releases = db.relationship('FileRelease', lazy='subquery')

class FileIdent(db.Model):
    __tablename__ = 'file_ident'
    id = db.Column(db.Integer, primary_key=True)
    live = db.Column(db.Boolean, nullable=False, default=False)
    rev_id = db.Column('revision', db.ForeignKey('file_rev.id'))
    redirect_id = db.Column(db.ForeignKey('file_ident.id'), nullable=True)
    revision = db.relationship("FileRev")

class FileEdit(db.Model):
    __tablename__ = 'file_edit'
    id = db.Column(db.Integer, primary_key=True)
    ident_id = db.Column(db.ForeignKey('file_ident.id'), nullable=True)
    rev_id = db.Column(db.ForeignKey('file_rev.id'), nullable=True)
    redirect_id = db.Column(db.ForeignKey('file_ident.id'), nullable=True)
    edit_group = db.Column(db.ForeignKey('edit_group.id'), nullable=True)
    extra_json = db.Column(db.ForeignKey('extra_json.sha1'), nullable=True)


### Editing #################################################################

#class Edit(db.Model):
#    __tablename__ = 'edit'
#    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#    edit_group = db.Column(db.ForeignKey('edit_group.id'), nullable=True)
#    editor = db.Column(db.ForeignKey('editor.id'), nullable=False)
#    comment = db.Column(db.String, nullable=True)
#    extra_json = db.Column(db.ForeignKey('extra_json.sha1'), nullable=True)
#    # WARNING: polymorphic. Represents the ident that should end up pointing to
#    # this revision.
#    entity_ident = db.Column(db.Integer, nullable=True)
#    entity_rev = db.Column(db.Integer, nullable=True)
#    entity_redirect = db.Column(db.Integer, nullable=True)

class EditGroup(db.Model):
    __tablename__ = 'edit_group'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    editor = db.Column(db.ForeignKey('editor.id'))
    description = db.Column(db.String)
    editor = db.Column(db.ForeignKey('editor.id'), nullable=False)

class Editor(db.Model):
    __tablename__ = 'editor'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String)
    group = db.Column(db.String)


### Other ###################################################################

class ChangelogEntry(db.Model):
    __tablename__= 'changelog'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    edit_group_id = db.Column(db.ForeignKey('edit_group.id'))
    timestamp = db.Column(db.Integer)

class ExtraJson(db.Model):
    __tablename__ = 'extra_json'
    sha1 = db.Column(db.String, primary_key=True)
    json = db.Column(db.String)
