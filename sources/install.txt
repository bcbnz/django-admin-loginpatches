Installation
============

Basic installation
------------------

1. Copy the ``admin_loginpatches`` directory into your project directory.
2. Add ``admin_loginpatches.middleware.AdminLoginPatchesMiddleware`` to the
   top of the :setting:`MIDDLEWARE_CLASSES` list in your project settings.
3. Add the ``admin_loginpatches/templates`` directory to the
   :setting:`TEMPLATE_DIRS` list in your project settings.

Login view
----------

The view that will be displayed when an unauthenticated user attempts to access
an administration page is given by the :setting:`ADMIN_LOGIN_VIEW` setting. If
this is not specified, it defaults to ``django.contrib.auth.views.login``, the
login view supplied as part of the :mod:`django.contrib.auth` module. When
called, this will be passed the :class:`django.http.HttpRequest` instance
corresponding to the users request, plus any keyword arguments specified by the
:setting:`ADMIN_LOGIN_ARGS` setting.

One addition will be made to the :class:`HttpRequest` passed to the view: the
URL to redirect to after login will be added to the :class:`GET` attribute. The
key for this URL is the value specified by
:attr:`django.contrib.auth.REDIRECT_FIELD_NAME`. It is worth noting that the
``django.contrib.auth.views.login`` view handles this redirect seamlessly. The
logic they use is::

    from django.contrib.auth import REDIRECT_FIELD_NAME

    def login(request):
        redirect_to = request.REQUEST.get(REDIRECT_FIELD_NAME, '')

        ....

        if form.is_valid():
            if not redirect_to or ' ' in redirect_to:
                redirect_to = settings.LOGIN_REDIRECT_URL
            elif '//' in redirect_to and re.match(r'[^\?]*//', redirect_to):
                    redirect_to = settings.LOGIN_REDIRECT_URL
            return HttpResponseRedirect(redirect_to)

Note that the view is responsible for passing the redirection URL through any
form submission where neccessary; this is why the above logic uses
``request.REQUEST`` as opposed to ``request.GET`` or ``request.POST``. If the
view can be reached from elsewhere, you should also check that the redirection
URL is valid.

Templates
---------

There are three occasions when an error message will be displayed to the user:
if their account is inactive, if they do not have staff status, or if they do
not have the neccessary permission to access a page. The names of the templates
used to tell the user this are given in the :setting:`ADMIN_LOGIN_INACTIVE_TEMPLATE`,
:setting:`ADMIN_LOGIN_NOTSTAFF_TEMPLATE` and :setting:`ADMIN_LOGIN_NOPERMISSION_TEMPLATE`
settings respectively.

The default settings use the templates provided in the ``admin_loginpatches/templates``
directory. If you wish to customise the templates:

1. Create your templates based upon the provided templates.
2. Configure Django to find these templates. See the `Django template language
   documentation <http://docs.djangoproject.com/en/dev/ref/templates/api/>`_
   for further details.
3. If neccessary, adjust the :setting:`ADMIN_LOGIN_*_TEMPLATE` settings to
   point to your templates.
