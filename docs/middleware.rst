Middleware
==========

In Django, middleware is called for each request and response. It can be used
to modify the input and/or output independently of the views. We use it to
modify some of the built-in behaviour of the Django administration interface
(``django.contrib.admin``) to better integrate it with the custom backend.

See the `Django middleware documentation <http://docs.djangoproject.com/en/dev/topics/http/middleware/>`_
for more information on middleware.

EmailAuthMiddleware
-------------------

.. class:: admin_loginpatches.middleware.EmailAuthMiddleware

   Many of the views in the Django administration interface use the
   ``admin_view`` decorator from the ``django.contrib.admin.sites.AdminSite``
   class to ensure that the user has the necessary permissions. Other views
   (such as the administration documentation) use the ``staff_member_required``
   decorator from the ``django.contrib.admin.views.decorators`` module to check
   that the user is a staff member.

   The problem with this is that both decorators provide their own login forms
   rather than using the ``LOGIN_URL`` specified in the settings. These have
   hard-coded field names (so the user is prompted for a username rather than a
   password). They also give misleading error messages; for example, if the
   user enters their password wrong they are told that their username cannot
   contain the '@' character. Finally, if they successfully log in but don't
   have the correct permission, they are prompted to log in again rather than
   being told what the problem is.

   This piece of middleware overcomes this by replacing the decorators with
   custom versions. They redirects the user to the settings ``LOGIN_URL`` when
   needed, allowing any customisations made to the login view (such as custom
   authentication forms) to be used. If the user is logged in but doesn't have
   the required permission to access page, the ``admin/permission_error.html``
   template is used to inform the user. If staff status is required and they
   don't have it, the ``admin/not_staff.html`` template is used. As a sanity
   check, it checks that they have an active account (this should have been
   done by the login view) and, if not, tells them so using the
   ``admin/inactive.html`` template.

   **It is recommended that you place this as the first piece of middleware to
   be used. Otherwise, earlier middleware may use the decorators prior to them
   being updated, thus ruining the backend integration.**

   For this to work correctly, you must:

   * Configure ``LOGIN_URL`` in your settings to point to your login view.

   * Ensure your login view correctly handles the ``next`` parameter to
     redirect the user to the appropriate page after login.

   * Make the ``admin/inactive.html``, ``admin/permission_fail.html`` and
     ``admin/not_staff.html`` templates available to the Django template
     loader. Templates are provided in the ``email_auth/templates`` directory
     of the project, or you can create your own using these as a guide.

   .. function:: process_request(request)

      Django calls this function for every request made. It replaces the
      ``django.contrib.admin.views.decorators.staff_member_required`` and
      ``django.contrib.admin.sites.AdminSite.admin_view`` decorators with
      custom versions. It also regenerates the default admin site
      (``django.contrib.admin.sites.site``) to match.
