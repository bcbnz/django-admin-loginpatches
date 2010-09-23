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
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.functional import update_wrapper
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.cache import never_cache


def staff_member_required(view_func):
    """Decorator used to protect pages requiring staff status. Used as a
    replacement for the django.contrib.admin.views.decorators version as that
    does not use the login URL specified in the settings (and hence gives
    misleading errors when custom authentication backends are used).

    This requires a LOGIN_URL to be specified in the settings, and for the
    view providing this login to accept a 'next' parameter giving the URL to
    redirect to after login.

    Two templates are also required:
    * admin/inactive.html informs the user their account is inactive
    * admin/not_staff.html informs the user they do not have staff status

    The context provided to both these templates is as follows:
    * title - a title for the page
    * message - error message to display to the user

    """
    def _checklogin(request, *args, **kwargs):
        # Not logged in
        if not request.user.is_authenticated():
            from django.conf import settings
            from django.contrib.auth import REDIRECT_FIELD_NAME
            login_url = settings.LOGIN_URL
            path = urlquote(request.get_full_path())
            redirect_path = '%s?%s=%s' % (login_url, REDIRECT_FIELD_NAME, path)
            return HttpResponseRedirect(redirect_path)

        # Inactive user. This *should* be handled by the login form, and
        # inactive users *shouldn't* have staff permission, but lets make
        # absolutely sure.
        if not request.user.is_active:
            context = {
                'message': _('Your user account is not active.'),
                'title': _('Inactive account'),
            }
            return render_to_response('admin/inactive.html', context,
                                      context_instance=RequestContext(request))

        # Not a staff member
        if not request.user.is_staff:
            context = {
                'message': _('Staff status is required to access this page.'),
                'title': _('Not a staff member'),
            }
            return render_to_response('admin/not_staff.html', context,
                                      context_instance=RequestContext(request))

        # User is good to go
        return view_func(request, *args, **kwargs)

    return wraps(view_func)(_checklogin)

def admin_view(self, view, cacheable=False):
    def inner(request, *args, **kwargs):
        # Not logged in
        if not request.user.is_authenticated():
            from django.conf import settings
            from django.contrib.auth import REDIRECT_FIELD_NAME
            login_url = settings.LOGIN_URL
            path = urlquote(request.get_full_path())
            redirect_path = '%s?%s=%s' % (login_url, REDIRECT_FIELD_NAME, path)
            return HttpResponseRedirect(redirect_path)

        # Inactive user. This *should* be handled by the login form, and
        # inactive users *shouldn't* have staff permission, but lets make
        # absolutely sure.
        if not request.user.is_active:
            context = {
                'message': _('Your user account is not active.'),
                'title': _('Inactive account'),
            }
            return render_to_response('admin/inactive.html', context,
                                      context_instance=RequestContext(request))

        # Don't have permission to do this
        if not self.has_permission(request):
            context = {
                'message': _('You do not have permission to view this page.'),
                'title': _('Permission error'),
            }
            return render_to_response('admin/permission_error.html', context,
                                      context_instance=RequestContext(request))

        # We're good to go
        return view(request, *args, **kwargs)
    if not cacheable:
        inner = never_cache(inner)
    return update_wrapper(inner, view)

class AdminLoginPatchesMiddleware:
    """Middleware to better integrate the email authentication backend into
    the admin site. The default staff_member_required decorator used to protect
    admin pages provides its own login form. This gives misleading error
    messages (for example, 'Usernames may not contain @'). Also, if a user is
    inactive or doesn't have staff status, it keeps prompting them to login
    rather than telling them what the real issue is.

    This middleware replaces the default decorator with a custom version which
    redirects to the LOGIN_URL specified in the settings when needed. It also
    tells the user if they don't have staff status so they know what the issue
    is.

    To ensure this substitution occurs on every request, it is recommended this
    middleware is placed at the top of the list. It never stops a request and
    so will not interfere with other middleware.

    """
    def process_request(self, request):
        django.contrib.admin.views.decorators.staff_member_required = staff_member_required
        django.contrib.admin.sites.AdminSite.admin_view = admin_view
        django.contrib.admin.sites.site = django.contrib.admin.sites.AdminSite()
        return None
