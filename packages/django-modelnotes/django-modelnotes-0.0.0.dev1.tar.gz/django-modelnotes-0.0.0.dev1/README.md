# django-modelnotes
A django-modelnotes is a reusable django application for adding notes to models. 

_**This app is still under development**_ 


| |                                                |
|--------------|------------------------------------------------|
| Author       | David Slusser                                  |
| Description  | A django application for adding notes to models. |
| Requirements | `Python 3.x`<br>`Django 3.x`                   |

# Documentation


# Installation
- install via pip
 ```shell script
pip install django-modelnotes
```
- add notes to your INSTALLED_APPS
```python
    INSTALLED_APPS = [
        ...
        'modelnotes',
    ]
```
- to include views to manage notes, add the following to your project-level urls.py:
```python
   
    urlpatterns = [
        ...
        path('modelnotes/', include('modelnotes.urls', )),
    ]
```

- run migrations
 ```shell script
 python ./manage.py migrate modelnotes
```

# Usage
add to models via GenericRelation
```python
from modelnotes.models import ModelNoteField

class MyModel(models.Model):
    ...
    notes = ModelNoteField()
```

# License 
django-modelnotes is licensed under the MIT license (see the LICENSE file for details).


# Features 
- included admin page with search, filters, and bulk editing
- variable scope; notes can be scoped to private, group or public
- permission controls available; notes can be set with read, edit, and delete permissions
- list views and bootstrap-based templates included
