import configparser
import json
from dateutil import parser

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
    if request.method == 'POST':
        err = merge(request.POST.getlist('uuid'))
    return redirect('/profiles/list')

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
        err = update_profile(sh_db, identity_id, request.POST)
    return HttpResponse(render_profile(sh_db, identity_id, request, err))

def update_enrollment(request, identity_id, organization):
    """
    Update profile enrollment dates
    It first removes old enrollment
    and creates a new one (base on the new dates)
    """
    err = None
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    if request.method != 'POST':
        return redirect('profiles/list')
    sh_db_cfg = "shdb.cfg"
    db = sortinghat_db_conn(sh_db_cfg)
    old_start_date = parser.parse(request.POST.get('old_start_date'))
    old_end_date = parser.parse(request.POST.get('old_end_date'))
    start_date = parser.parse(request.POST.get('start_date'))
    end_date = parser.parse(request.POST.get('end_date'))
    sortinghat.api.delete_enrollment(db, identity_id, organization, old_start_date, old_end_date)
    sortinghat.api.add_enrollment(db, identity_id, organization, start_date, end_date)
    return redirect('/profiles/' + identity_id)

def unenroll_profile(request, identity_id, organization_info):
    """
    Un-enroll a profile uuid from an organization
    """
    err = None
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    if request.method == 'POST':
        return redirect('/profiles/' + identity_id)
    sh_db_cfg = "shdb.cfg"
    db = sortinghat_db_conn(sh_db_cfg)
    org_name = organization_info.split('_')[0]
    org_start = parser.parse(organization_info.split('_')[1])
    org_end = parser.parse(organization_info.split('_')[2])
    sortinghat.api.delete_enrollment(db, identity_id, org_name, org_start, org_end)
    return redirect('/profiles/' + identity_id)

def enroll_to_profile(request, identity_id, organization):
    """
    Enroll a profile uuid into an organization
    """
    err = None
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    if request.method == 'POST':
        return redirect('/profiles/' + identity_id)
    sh_db_cfg = "shdb.cfg"
    db = sortinghat_db_conn(sh_db_cfg)
    try:
        sortinghat.api.add_enrollment(db, identity_id, organization)
        err = None
    except sortinghat.exceptions.AlreadyExistsError as error:
        err = error
    return redirect('/profiles/' + identity_id)

def merge_to_profile(request, identity_id):
    """
    Merge a list of unique profiles to the profile
    """
    err = None
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    if request.method != 'POST':
        return redirect('/profiles/' + identity_id)
    uuids = request.POST.getlist('uuid')
    uuids.append(identity_id)
    err = merge(uuids)
    return redirect('/profiles/' + identity_id)

def unmerge(request, profile_uuid, identity_id):
    """
    Unmerge a given identity from a unique identity, creating a new unique identity
    """
    err = None
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    if request.method != 'GET':
        return redirect('/profiles/' + profile_uuid)
    sh_db_cfg = "shdb.cfg"
    db = sortinghat_db_conn(sh_db_cfg)
    sortinghat.api.move_identity(db, identity_id, identity_id)
    with db.connect() as session:
        edit_identity = session.query(Identity).filter(Identity.uuid == identity_id).first()
        uid_profile_name = edit_identity.name
        uid_profile_email = edit_identity.email
        sortinghat.api.edit_profile(db, identity_id, name=uid_profile_name, email=uid_profile_email)
    session.expunge_all()
    return redirect('/profiles/' + profile_uuid)

def organizations(request):
    """
    Render organizations page
    """
    err = None
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    sh_db_cfg = "shdb.cfg"
    db = sortinghat_db_conn(sh_db_cfg)
    if request.method == 'POST':
        try:
            sortinghat.api.add_organization(db, request.POST.get('name'))
        except sortinghat.exceptions.AlreadyExistsError as error:
            err = error
    orgs = sortinghat.api.registry(db)
    domains = sortinghat.api.domains(db)
    context = {
        "orgs": orgs, "domains": domains, "err":err
    }
    template = loader.get_template('organizations/organizations.html')
    return HttpResponse(template.render(context, request))

def about_render(request, err=None):
    """
    Render index page
    """
    context = {
        "err":err
    }
    template = loader.get_template('about/about.html')
    return HttpResponse(template.render(context, request))

#
# HELPER METHODS FOR VIEWS
#

def merge(uuids):
    """
    Merge a set of profiles given the list of uuids
    """
    sh_db_cfg = "shdb.cfg"
    db = sortinghat_db_conn(sh_db_cfg)
    if len(uuids) > 1:
        for uuid in uuids[:-1]:
            sortinghat.api.merge_unique_identities(db, uuid, uuids[-1])
            err = None
    else:
        err = "You need at least 2 profiles to merge them"
    return err

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

def update_profile(db, uuid, profile_data):
    """
    Update profile
    """
    try:
        sortinghat.api.edit_profile(db, uuid, name=profile_data['name'],\
            email=profile_data['email'], is_bot=profile_data['bot'] == 'True',\
            country=profile_data['country'])
        err = None
    except sortinghat.exceptions.NotFoundError as error:
        err = error
    except sortinghat.exceptions.WrappedValueError as error:
        err = error
    return err
