Templates
=========

As noted in the :ref:`settings documentation <settings>`, there are three
templates used by this project:

* ``admin/inactive.html`` for an inactive user,
* ``admin/not_staff.html`` when the user is not a staff member, and
* ``admin/permission_error.html`` when the user does not have permission to
  access a page.

These templates are provided in the ``admin_loginpatches/templates`` directory.
To use them, you need to tell Django how to find them. There are two methods of
doing this:

1. Add the ``admin_loginpatches/templates`` directory to the
   :setting:`TEMPLATE_DIRS` setting.
2. Add this project to your :setting:`INSTALLED_APPS` setting and make sure the
   :class:`app_directories.Loader` template loaded is used.

The first method is preferred as this project is not strictly an application
(it does not provide any models or views). Alternatively, you can define your
own templates based upon the ones provided and make these accessible by the
Django template loader. See the `Django template language documentation
<http://docs.djangoproject.com/en/dev/ref/templates/api/>`_ for further details
on the Django template system.
