
import os
import subprocess

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    GIT_REVISION = subprocess.check_output(["git", "describe", "--always"]).strip()
    # This is, effectively, the QA/PROD flag
    FATCAT_DOMAIN = os.environ.get("FATCAT_DOMAIN", default="qa.fatcat.wiki")
    ELASTIC_BACKEND = os.environ.get("ELASTIC_BACKEND", default="https://search.fatcat.wiki")
    ELASTIC_INDEX = os.environ.get("ELASTIC_INDEX", default="fatcat")

    # "Event more verbose" debug options. SECRET_KEY is bogus.
    #SQLALCHEMY_ECHO = True
    #SECRET_KEY = "kuhy0284hflskjhg01284"
    #DEBUG = True
