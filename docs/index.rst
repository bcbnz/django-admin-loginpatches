=========================
django-admin-loginpatches
=========================

By default, `Django`_ requires a username and password for a user to log in.
Alternative login methods, such as with an email address and passwords or via
an LDAP server, can be implemented by using a custom authentication backend.
The Django administrative interface can use these custom backends. However,
the logon forms and corresponding error messages are hard-coded, often leading
to a confusing user interface when a custom backend is used. This project fixes
this by altering the behaviour of the administrative interface to allow the
login forms and messages to be customisable just like the backend.

This documentation describes the problems with the default behaviour, how the
project fixes it, how to obtain and install the code on your own Django
website, and how to customise its behaviour.

.. _`Django`: http://www.djangoproject.com

Contents:
=========

.. toctree::
   :maxdepth: 2

   why
   how
   obtain
   install
   settings
   gpl3

License
=======

Copyright (C) 2010 Blair Bonnett

django-admin-loginpatches is free software: you can redistribute it
and/or modify it under the terms of the GNU General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

django-admin-loginpatches is distributed in the hope that it will be
useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

Version 3 of the GNU General Public License is available :ref:`here <gpl3>`,
or online (along with any later versions) at http://www.gnu.org/licenses/.
