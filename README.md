# 2022_elasticsearch
Django-haystack-elasticsearch

Cài đặt haystack-django-elasticsearch theo hướng dẫn tại: https://django-haystack.readthedocs.io/en/master/tutorial.html

Step by steps:
B1: Tạo project django 
B2: Thêm app 'myapp'
    Thêm models
        from django.db import models
        
        from django.contrib.auth.models import User


        class Note(models.Model):
            user = models.ForeignKey(User, on_delete=models.CASCADE)
            pub_date = models.DateTimeField()
            title = models.CharField(max_length=200)
            body = models.TextField()

            def __unicode__(self):
                return self.title```

B3: install django-haystack version elasticsearch
    ```pip install "django-haystack[elasticsearch]"```

B4: Thêm haystack vào install_app
  ```
  INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',

        # Added.
        'haystack',

        # Then your usual apps...
        'myapp',
    ]
    ```
B5: makemigrations và migrate

B6: Thêm haystack_connection ( Ở đây sử dụng elasticsearch 7)

        ```HAYSTACK_CONNECTIONS = {
            'default': {
                'ENGINE': 'haystack.backends.elasticsearch7_backend.Elasticsearch7SearchEngine',
                'URL': 'http://127.0.0.1:9200/',
                'INDEX_NAME': 'haystack',
            },
        }```
        
B7: Thêm file search_indexes.py, path: myapp/search_indexes.py
        ```import datetime
        from haystack import indexes
        from myapp.models import Note


        class NoteIndex(indexes.SearchIndex, indexes.Indexable):
            text = indexes.CharField(document=True, use_template=True)
            author = indexes.CharField(model_attr='user')
            pub_date = indexes.DateTimeField(model_attr='pub_date')

            def get_model(self):
                return Note

            def index_queryset(self, using=None):
                """Used when the entire index for model is updated."""
                return self.get_model().objects.filter(pub_date__lte=datetime.datetime.now())```
  
B8: Thêm note_text.txt file path: templates/search/indexes/myapp/note_text.txt
          ```{{ object.title }}
          {{ object.user.get_full_name }}
          {{ object.body }}```
          
B9: Thêm urlconf
        ```path('search/', include('haystack.urls')),```

B10: Thêm file base.html, path: myapp/templates/search/base.html
        ```<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>{% block title %}{% endblock %}</title>
        </head>
        <body>
        {% block content %}
        {% endblock %}
        </body>
        </html>```
B11: Thêm search template
            ```{% extends 'base.html' %}

            {% block content %}
                <h2>Search</h2>

                <form method="get" action=".">
                    <table>
                        {{ form.as_table }}
                        <tr>
                            <td>&nbsp;</td>
                            <td>
                                <input type="submit" value="Search">
                            </td>
                        </tr>
                    </table>

                    {% if query %}
                        <h3>Results</h3>

                        {% for result in page.object_list %}
                            <p>
                                <a href="{{ result.object.get_absolute_url }}">{{ result.object.title }}</a>
                            </p>
                        {% empty %}
                            <p>No results found.</p>
                        {% endfor %}

                        {% if page.has_previous or page.has_next %}
                            <div>
                                {% if page.has_previous %}<a href="?q={{ query }}&amp;page={{ page.previous_page_number }}">{% endif %}&laquo; Previous{% if page.has_previous %}</a>{% endif %}
                                |
                                {% if page.has_next %}<a href="?q={{ query }}&amp;page={{ page.next_page_number }}">{% endif %}Next &raquo;{% if page.has_next %}</a>{% endif %}
                            </div>
                        {% endif %}
                    {% else %}
                        {# Show some example queries to run, maybe query syntax, something else? #}
                    {% endif %}
                </form>
            {% endblock %}```

B12: Thêm view

        ```from django.shortcuts import render
        from myapp.models import Note
        # Create your views here.
        def search_view(request):
            context = {
                'title': "Tìm kiếm nhanh"
            }
            return render(request, 'search/search.html', context)

        # Create your views here.
        def read_body(request, id):
            note_body = Note.objects.get(id=id)
            context = {
                'title': note_body.title,
                'note_body': note_body
            }
            return render(request, 'search/read_body.html', context)```


