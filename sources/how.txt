How we'll do this
=================

We want to replace the default decorators with our custom versions for every
request. To do so, we will create a middleware class and use the
:func:`process_request` function to perform the replacement.

Middleware
----------

Each time a request, response, view or exception is handled, Django calls each
class in the :setting:`MIDDLEWARE_CLASSES` setting with the details. This
allows this input, output or environment to be modified independently of the
standard Django procesing.

See the `Django middleware documentation <http://docs.djangoproject.com/en/dev/topics/http/middleware/>`_
for more information on middleware.

:func:`admin_view` decorator
----------------------------

In Django 1.2, the :func:`admin_view` is defined as follows::

    class AdminSite(object):
        def admin_view(self, view, cacheable=False):

            def inner(request, *args, **kwargs):
                if not self.has_permission(request):
                    return self.login(request)
                return view(request, *args, **kwargs)

            if not cacheable:
                inner = never_cache(inner)

            if not getattr(view, 'csrf_exempt', False):
                inner = csrf_protect(inner)

            return update_wrapper(inner, view)

The :func:`AdminSite.login()` function displays and processes the login form.
In order to change the behaviour of the decorator as desired, we need to alter
the :func:`inner` sub-function to match the following behaviour::

    def inner(request, *args, **kwargs):
        # Delegate to the login view specified in settings
        if not request.user.is_authenticated():
            ....

        # Delegate to the "your account is inactive" view specified in settings
        if not request.user.is_active:
            ....

        # Delegate to the "you don't have permission" view specified in settings
        if not self.has_permissions(request):
            ....

        # Have permission, generate the view
        return view(request, *args, **kwargs)

:func:`staff_member_required` decorator
---------------------------------------

The :func:`staff_member_required` decorator follows the same pattern as
:func:`admin_view` except that it uses :attr:`request.user.is_staff`
instead of :func:`self.has_permissions` as the permission test. Our version of
it will also behave in the same fashion as our version of :func:`admin_view`.

AdminLoginPatchesMiddleware
---------------------------

With the replacement functions written, the final step is to actually perform
the replacement. This is performed by the :func:`process_request` function of
the middleware, which is called by Django for each request it receives. The
documentation for the middleware class is given below.

.. class:: admin_loginpatches.middleware.AdminLoginPatchesMiddleware

   A Django middleware class designed to monkey patch the
   :mod:`django.contrib.admin` module to better support custom authentication
   backends.

   **This should be placed as the first middleware class to be executed.
   Otherwise, any other middleware which uses the decorators will use the
   default versions rather than the custom versions.**

   .. function:: process_request(request)

      Called for each request, this function performs the following steps:

      * Replace :func:`django.contrib.admin.sites.AdminSite.admin_view` with a
        custom version.
      * Replace :func:`django.contrib.admin.views.decorators.staff_member_required`
        with a custom version.
      * Replace the existing :attr:`django.contrib.admin.sites.site` (an
        instance of :class:`django.contrib.sites.AdminSite`) with an instance
        containing the new :func:`admin_view` decorator.
