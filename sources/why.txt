Why do we need to do this?
==========================

The Django administration module (:mod:`django.contrib.admin`) uses two
decorators to ensure the user has permission to access a view:

* :func:`django.contrib.admin.sites.AdminSite.admin_view` to check that a user
  has a specific permission.

* :func:`django.contrib.admin.views.decorators.staff_member_required` to check
  if a user is a staff member.

The problem
-----------

These decorators provide login forms if neccessary. However, since these forms
are hard-coded, they do not fit in well with custom authentication backends.
The user is always prompted for a username and password, when the backend may
require, for example, an email address and password.

The error messages shown if the login fails are also hard-coded. This can be
extremely misleading to the user. For example, if using an email backend and
the user enters their password incorrectly, they are told::

    Usernames cannot contain the '@' character.

Finally, the decorators do not inform the user if they do not have the correct
permissions to access the view. Instead, they repeatedly prompt the user to log
in, even if they already successfully logged in. This is very confusing
behaviour, especially if the user has reason to believe they should be able to
access the view.

The solution
------------

We would like the view used to prompt the user to log in to be specified in the
settings, thus allowing it to be customised to fit the authentication backend
in use. Additionally, we would like the user to be informed when they do not
have the appropriate permissions to access the view. Hence, we need to modify
the behaviour of the administration module.

The most obvious way of achieving this is to edit the code of the module to
suit. However, this is only possible when we have the neccessary permissions to
do so, which will not be the case on the majority of web servers. Instead, we
will `monkey patch <http://en.wikipedia.org/wiki/Monkey_patch>`_ the code on
the fly.
