Settings
========

.. setting:: ADMIN_LOGIN_VIEW

ADMIN_LOGIN_VIEW
----------------

Default: ``'django.contrib.auth.views.login'``

This is the view that will be used to present the login form to the user when
needed. It should be given as a string which represents an importable Django
view.

.. setting:: ADMIN_LOGIN_ARGS

ADMIN_LOGIN_ARGS
----------------

Default: ``{}`` (Empty dictionary)

A dictionary of keyword arguments to be passed to the login view whenever it is
called.

.. setting:: ADMIN_LOGIN_INACTIVE_TEMPLATE

ADMIN_LOGIN_INACTIVE_TEMPLATE
-----------------------------

Default: ``'admin/inactive.html'``

The name of the template to be rendered when the users account is inactive. The
template is given both a :class:`RequestContext` and the following context:

* ``title``: The title of the page
* ``message``: A message explaining the problem.

In theory, this template will never be used as a user with an inactive account
should not be allowed to log in. However, it is present as an extra safety
check.

.. setting:: ADMIN_LOGIN_NOTSTAFF_TEMPLATE

ADMIN_LOGIN_NOTSTAFF_TEMPLATE
-----------------------------

Default: ``'admin/not_staff.html'``

The name of the template to be rendered when the user does not have the
required staff status. The template is given both a :class:`RequestContext` and
the following context:

* ``title``: The title of the page
* ``message``: A message explaining the problem.

.. setting:: ADMIN_LOGIN_NOPERMISSION_TEMPLATE

ADMIN_LOGIN_NOPERMISSION_TEMPLATE
---------------------------------

Default: ``'admin/permission_error.html'``

The name of the template to be rendered when the user does not have the
permission required to view the page. The template is given both a
:class:`RequestContext` and the following context:

* ``title``: The title of the page
* ``message``: A message explaining the problem.
