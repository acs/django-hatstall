import configparser
import math
from dateutil import parser

import sortinghat.api

from sortinghat.db.database import Database
from sortinghat.db.model import UniqueIdentity
from sortinghat.db.model import Identity

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from django.utils.datastructures import MultiValueDictKeyError

#
# VIEWS
#

# Global vars
current_page = 1
current_page_profile = 1
shdb_user = ""
shdb_pass = ""
shdb_name = ""
shdb_host = ""
shsearch = ""
shsearch_profile = ""
table_length = 10
table_length_profile = 1


def index(request):
    if request.method == 'POST':
        err = merge(request.POST.getlist('uuid'))
    return redirect('/profiles/list')


def list(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    if (not shdb_name) or (not shdb_name) or (not shdb_host):
        return redirect('/shdb/params')
    # sh_db_cfg = "shdb.cfg"
    sh_db = sortinghat_db_conn()
    # uuids = render_profiles(sh_db, request)
    # return HttpResponse("Listing all profiles: " + json.dumps(uuids))
    return HttpResponse(render_profiles(sh_db, request))


def identity(request, identity_id):
    err = None
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    if (not shdb_name) or (not shdb_name) or (not shdb_host):
        return redirect('/shdb/params')
    sh_db = sortinghat_db_conn()
    if request.method == 'POST' and "shsearch" not in request.POST and "table_length" not in request.POST\
            and "page" not in request.POST:
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
    if (not shdb_name) or (not shdb_name) or (not shdb_host):
        return redirect('/shdb/params')
    if request.method != 'POST':
        return redirect('profiles/list')
    db = sortinghat_db_conn()
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
    if (not shdb_name) or (not shdb_name) or (not shdb_host):
        return redirect('/shdb/params')
    if request.method == 'POST':
        return redirect('/profiles/' + identity_id)
    db = sortinghat_db_conn()
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
    if (not shdb_name) or (not shdb_name) or (not shdb_host):
        return redirect('/shdb/params')
    if request.method == 'POST':
        return redirect('/profiles/' + identity_id)
    db = sortinghat_db_conn()
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
    if (not shdb_name) or (not shdb_name) or (not shdb_host):
        return redirect('/shdb/params')
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
    if (not shdb_name) or (not shdb_name) or (not shdb_host):
        return redirect('/shdb/params')
    if request.method != 'GET':
        return redirect('/profiles/' + profile_uuid)
    db = sortinghat_db_conn()
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
    if (not shdb_name) or (not shdb_name) or (not shdb_host):
        return redirect('/shdb/params')
    db = sortinghat_db_conn()
    if request.method == 'POST':
        try:
            sortinghat.api.add_organization(db, request.POST.get('name'))
        except sortinghat.exceptions.AlreadyExistsError as error:
            err = error
    orgs = sortinghat.api.registry(db)
    context = {
        "orgs": orgs, "err": err
    }
    template = loader.get_template('organizations/organizations.html')
    return HttpResponse(template.render(context, request))


def get_shdb_params(request, err=None):
    """
    Render organizations page
    """
    global shdb_user
    global shdb_pass
    global shdb_name
    global shdb_host
    if request.method == 'POST':
        shdb_user = request.POST.get('shdb_user_form')
        shdb_pass = request.POST.get('shdb_pass_form')
        shdb_name = request.POST.get('shdb_name_form')
        shdb_host = request.POST.get('shdb_host_form')
        try:
            db = sortinghat_db_conn()
        except sortinghat.exceptions.DatabaseError as error:
            err = error

    if shdb_user and shdb_name and shdb_host and not err:
        return redirect('/profiles/list')
    context = {
        "err": err
    }
    template = loader.get_template('shdb/shdb_form.html')
    return HttpResponse(template.render(context, request))


def about_render(request, err=None):
    """
    Render index page
    """
    context = {
        "err": err
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
    db = sortinghat_db_conn()
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


def sortinghat_db_conn():
    """
    Returns Sorting Hat database object to work with
    """
    # shdb_user, shdb_pass, shdb_name, shdb_host = parse_shdb_config_file(filename)
    sortinghat_db = Database(user=shdb_user, password=shdb_pass, database=shdb_name, host=shdb_host)

    return sortinghat_db


def render_profiles(db, request, err=None):
    """
    Render profiles page
    """
    global shsearch
    global table_length
    global current_page
    unique_identities = []
    sh_db = sortinghat_db_conn()
    err = None
    if request.method == 'POST':
        if "shsearch" in request.POST:
            shsearch = request.POST.get('shsearch')
            current_page = 1
        elif "page" in request.POST:
            current_page = int(request.POST.get('page'))
        elif "table_length" in request.POST:
            table_length = int(request.POST.get('table_length'))
            current_page = 1
    else:
        shsearch = ""
        current_page = 1
        table_length = 10

    offset = 0 + (table_length * (current_page - 1))
    try:
        # Code from api of sortinghat
        uidentities, uicount = sortinghat.api.search_unique_identities_slice(sh_db, shsearch, offset, table_length)
        n_pages = math.ceil(uicount / table_length)
        unique_identities = []
        for uid in uidentities:
            uid_dict = uid.to_dict()
            uid_dict.update({"last_modified": uid.last_modified})
            # Add enrollments to a new property 'roles'
            enrollments = sortinghat.api.enrollments(sh_db, uid.uuid)
            uid.roles = enrollments
            enrollments = []
            for enrollment in uid.roles:
                enrollments.append(enrollment.organization.name)
            uid_dict['enrollments'] = enrollments
            unique_identities.append(uid_dict)
    except sortinghat.exceptions.NotFoundError as error:
        err = error
    template = loader.get_template('profiles/profiles.html')
    context = {
        "uids": unique_identities, "n_pages": n_pages, "current_page": current_page,
        "shsearch": shsearch, "table_length": table_length, "err": err
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
    global shsearch_profile
    global table_length_profile
    global current_page_profile
    orgs = sortinghat.api.registry(db)
    profile_enrollments = []
    with db.connect() as session:
        profile_info = session.query(UniqueIdentity). \
            filter(UniqueIdentity.uuid == profile_uuid).first()
        for enrollment in profile_info.enrollments:
            profile_enrollments.append(enrollment)
        countries = sortinghat.api.countries(db)
        session.expunge_all()

    if request.method == 'POST' and "name" not in request.POST and "email" not in request.POST\
            and "bot" not in request.POST and "country" not in request.POST:
        if "shsearch" in request.POST:
            shsearch_profile = request.POST.get('shsearch')
            current_page_profile = 1
        elif "page" in request.POST:
            current_page_profile = int(request.POST.get('page'))
        elif "table_length" in request.POST:
            table_length_profile = int(request.POST.get('table_length'))
            current_page_profile = 1
        show_table = True
    else:
        shsearch_profile = ""
        current_page_profile = 1
        table_length_profile = 10
        show_table = ""

    unique_identities = []
    n_pages = 1
    if show_table:
        offset = 0 + (table_length_profile * (current_page_profile - 1))
        try:
            # Code from api of sortinghat
            uidentities, uicount = sortinghat.api.search_unique_identities_slice(db, shsearch_profile, offset, table_length_profile)
            n_pages = math.ceil(uicount / table_length_profile)
            for uid in uidentities:
                uid_dict = uid.to_dict()
                uid_dict.update({"last_modified": uid.last_modified})
                # Add enrollments to a new property 'roles'
                enrollments = sortinghat.api.enrollments(db, uid.uuid)
                uid.roles = enrollments
                enrollments = []
                for enrollment in uid.roles:
                    enrollments.append(enrollment.organization.name)
                uid_dict['enrollments'] = enrollments
                unique_identities.append(uid_dict)
        except sortinghat.exceptions.NotFoundError as error:
            err = error
    context = {
        "profile": profile_info.to_dict(), "orgs": orgs, "unique_identities": unique_identities, "n_pages": n_pages,
        "current_page": current_page_profile, "shsearch": shsearch_profile, "table_length": table_length_profile,
        "show_table": show_table, "enrollments": profile_info.enrollments, "countries": countries, "err": err
    }
    template = loader.get_template('profiles/profile.html')
    return template.render(context, request)


def update_profile(db, uuid, profile_data):
    """
    Update profile
    """
    try:
        if 'bot' in profile_data:
            user_bot = profile_data['bot']
        else:
            user_bot = 'False'
        sortinghat.api.edit_profile(db, uuid, name=profile_data['name'],
                                    email=profile_data['email'], is_bot=user_bot == 'True',
                                    country_code=profile_data['country'])
        err = None
    except sortinghat.exceptions.NotFoundError as error:
        err = error
    except sortinghat.exceptions.WrappedValueError as error:
        err = error
    except MultiValueDictKeyError as error:
        err = "The {} can not be empty. Select one.".format(error.args[0])
    return err
