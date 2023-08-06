=====
Html Generator
=====

Html Generator is a Django app for converting markdown text to html and displaying it in a template.
Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "html_generator" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'html_generator.apps.HtmlGeneratorConfig',
    ]

2. Include the html_generator URLconf in your project urls.py like this::

    path('html_gen/', include('html_generator.urls')),

3. Run ``python manage.py migrate`` to create the html_generator models.

4. Start the development server and visit http://127.0.0.1:8000/html_gen/ for an unstyled form that can be included in any template.

5. Turning in that form will redirect you to its detail view where you will see the markdown you inputed displayed as html

6. change the Markdown_form_view's http redirect reverse from "html_generator:page", to the app and template you want to display your html on and add 