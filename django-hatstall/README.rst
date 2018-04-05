========
Hatstall
========

Hatstall is a Django app to manage the identities in Sorting Hat. You can
edit, list, merge, unmerge and enroll the identities in SortingHat.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "hatstall" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'hatstall',
    ]

2. Include the hatstall URLconf in your project urls.py like this::

    path('hatstall/', include('hatstall.urls')),

3. Start the development server.

5. Visit http://127.0.0.1:8000/hatstall/ to use it.
