django-admin-visualsearch
=========================

Replace for standard search input in django admin interface.

![Example of usage](https://raw.github.com/unk2k/django-admin-visualsearch/master/screenshoot.png)

Install
-------

For install you can use pip:
```
pip install django-admin-visualsearch
```


Usage
-------

models.py

```
from django.db import models

class Author(models.Model):
    first_name = ....
    last_name = ....
  
class Books(models.Model):
    title = ....
    author = models.ManyToManyField(Author)
```

admin.py

```
from visualsearch import VisualSearchAdmin
from django.contrib import admin
from books.models import Books

class BooksAdmin(VisualSearchAdmin, admin.ModelAdmin):
    visualsearch_fields = {
        'title': u'Book title',
        'author__first_name__last_name': u'Author',
    }

admin.site.register(Books, BooksAdmin)
```

django-admin-visualsearch split "author__first_name__last_name" and find usage keys (author__first_name, author__last_name).
For related fields you must use specifical subfield for search (for example: author__first_name).

Note
-------

If you use visualsearch, you don't use other standart filter in admin interface cls
