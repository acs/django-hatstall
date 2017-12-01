import configparser
import json

import sortinghat.api

from sortinghat.db.database import Database
from sortinghat.db.model import UniqueIdentity
from sortinghat.db.model import Identity

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader

#
# VIEWS
#


def index(request):
    return HttpResponse("Hello, world. You're at the profiles index.")

def list(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    sh_db_cfg = "shdb.cfg"
    sh_db = sortinghat_db_conn(sh_db_cfg)
    # uuids = render_profiles(sh_db, request)
    # return HttpResponse("Listing all profiles: " + json.dumps(uuids))
    return HttpResponse(render_profiles(sh_db, request))

def identity(request, identity_id):
    err = None
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    sh_db_cfg = "shdb.cfg"
    sh_db = sortinghat_db_conn(sh_db_cfg)
    if request.method == 'POST':
        err = update_profile(identity_id, request.form)
    return HttpResponse(render_profile(sh_db, identity_id, request, err))


#
# HELPER METHODS FOR VIEWS
#


def parse_shdb_config_file(filename):
    """
    Returns SortingHat database settings (user, password, name, host) to
    connect to it later
    """
    shdb_config = configparser.ConfigParser()
    shdb_config.read(filename)
    shdb_user = shdb_config.get('SHDB_Settings', 'user')
    shdb_pass = shdb_config.get('SHDB_Settings', 'password')
    shdb_name = shdb_config.get('SHDB_Settings', 'name')
    shdb_host = shdb_config.get('SHDB_Settings', 'host')

    return shdb_user, shdb_pass, shdb_name, shdb_host


def sortinghat_db_conn(filename):
    """
    Returns Sorting Hat database object to work with
    """
    shdb_user, shdb_pass, shdb_name, shdb_host = parse_shdb_config_file(filename)
    sortinghat_db = Database(user=shdb_user, password=shdb_pass, database=shdb_name, host=shdb_host)

    return sortinghat_db


def render_profiles(db, request, err=None):
    """
    Render profiles page
    """
    unique_identities = []
    with db.connect() as session:
        for u_identity in session.query(UniqueIdentity):
            uuid_dict = u_identity.to_dict()
            enrollments = []
            for enrollment in u_identity.enrollments:
                enrollments.append(enrollment.organization.name)
            uuid_dict['enrollments'] = enrollments
            unique_identities.append(uuid_dict)
    session.expunge_all()
    template = loader.get_template('profiles/profiles.html')
    context = {
        "uids":unique_identities, "err":err
    }
    return template.render(context, request)
    # return unique_identities
    # return render(request, 'profiles.html', {})
    # return render_template('profiles.html', uids=unique_identities, err=err)

def render_profile(db, profile_uuid, request, err=None):
    """
    Render unique identity profile page
    It shows also sections to add enrollments and merge remaining
    identities
    """
    orgs = sortinghat.api.registry(db)
    remaining_identities = []
    profile_enrollments = []
    with db.connect() as session:
        profile_info = session.query(UniqueIdentity).\
            filter(UniqueIdentity.uuid == profile_uuid).first()
        profile_identities = [x.id for x in profile_info.identities]
        for identity in session.query(Identity).filter(Identity.id.notin_(profile_identities)):
            remaining_identities.append(identity)
        for enrollment in profile_info.enrollments:
            profile_enrollments.append(enrollment)
        session.expunge_all()
    context = {
        "profile": profile_info.to_dict(), "orgs": orgs, "identities": remaining_identities, "enrollments": profile_info.enrollments, "err":err
    }
    template = loader.get_template('profiles/profile.html')
    return template.render(context, request)