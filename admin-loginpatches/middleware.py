# This file is part of django-admin-loginpatches, a project to patch
# the Django admin login interface to better support custom
# authentication backends.
# Copyright (C) 2010 Blair Bonnett
#
# django-admin-loginpatches is free software: you can redistribute it
# and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
#
# django-admin-loginpatches is distributed in the hope that it will
# be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with django-admin-loginpatches.  If not, see
# <http://www.gnu.org/licenses/>.

from functools import wraps

import django.contrib.admin.views.decorators
import django.contrib.admin.sites
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.conf import settings
from django.core.urlresolvers import get_callable
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.functional import update_wrapper
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect


def staff_member_required(view_func):
    def _checklogin(request, *args, **kwargs):
        # Not logged in
        if not request.user.is_authenticated():
            login_view = getattr(settings, 'ADMIN_LOGIN_VIEW',
                                 'django.contrib.auth.views.login')
            login_args = getattr(settings, 'ADMIN_LOGIN_ARGS', {})
            view = get_callable(login_view)
            request.GET._mutable = True
            request.GET[REDIRECT_FIELD_NAME] = request.get_full_path()
            request.GET._mutable = False
            return view(request, **login_args)

        # Inactive user. This *should* be handled by the login form, and
        # inactive users *shouldn't* have staff permission, but lets make
        # absolutely sure.
        if not request.user.is_active:
            template = getattr(settings, 'ADMIN_LOGIN_INACTIVE_TEMPLATE',
                               'admin/inactive.html')
            context = {
                'title': _('Inactive account'),
                'message': _('Your account is not active.'),
            }
            return render_to_response(template, context,
                                      context_instance=RequestContext(request))

        # Not a staff member
        if not request.user.is_staff:
            template = getattr(settings, 'ADMIN_LOGIN_NOTSTAFF_TEMPLATE',
                               'admin/not_staff.html')
            context = {
                'title': _('Not staff'),
                'message': _('You need to be a staff member to view this page.'),
            }
            return render_to_response(template, context,
                                      context_instance=RequestContext(request))

        # User is good to go
        return view_func(request, *args, **kwargs)

    return wraps(view_func)(_checklogin)

def admin_view(self, view, cacheable=False):
    def inner(request, *args, **kwargs):
        # Not logged in
        if not request.user.is_authenticated():
            login_view = getattr(settings, 'ADMIN_LOGIN_VIEW',
                                 'django.contrib.auth.views.login')
            login_args = getattr(settings, 'ADMIN_LOGIN_ARGS', {})
            loginview = get_callable(login_view)
            request.GET._mutable = True
            request.GET[REDIRECT_FIELD_NAME] = request.get_full_path()
            request.GET._mutable = False
            return loginview(request, **login_args)

        # Inactive user. This *should* be handled by the login form, and
        # inactive users *shouldn't* have staff permission, but lets make
        # absolutely sure.
        if not request.user.is_active:
            template = getattr(settings, 'ADMIN_LOGIN_INACTIVE_TEMPLATE',
                               'admin/inactive.html')
            context = {
                'title': _('Inactive account'),
                'message': _('Your account is not active.'),
            }
            return render_to_response(template, context,
                                      context_instance=RequestContext(request))

        # Don't have permission to do this
        if not self.has_permission(request):
            template = getattr(settings, 'ADMIN_LOGIN_NOPERMISSION_TEMPLATE',
                               'admin/permission_error.html')
            context = {
                'title': _('Permission error'),
                'message': _('You do not have permission to view this page.'),
            }
            return render_to_response(template, context,
                                      context_instance=RequestContext(request))

        # We're good to go
        return view(request, *args, **kwargs)
    if not cacheable:
        inner = never_cache(inner)
    if not getattr(view, 'csrf_exempt', False):
        inner = csrf_protect(inner)
    return update_wrapper(inner, view)

class AdminLoginPatchesMiddleware:
    """The admin_view and staff_member_required decorators don't fit work well
    with custom authentication backends. This middleware class replaces the
    default decorators with custom versions which allow better customisation.

    To ensure this substitution occurs on every request, it is recommended this
    middleware is placed at the top of the list. It never stops a request and
    so will not interfere with other middleware.

    """
    def process_request(self, request):
        django.contrib.admin.views.decorators.staff_member_required = staff_member_required
        django.contrib.admin.sites.AdminSite.admin_view = admin_view
        django.contrib.admin.sites.site = django.contrib.admin.sites.AdminSite()
        return None
