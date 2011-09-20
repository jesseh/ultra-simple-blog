Ultra Simple Blog
=================

This is a test project. I've focused solely on the backend and done almost no work on the front end. In developing this blog I tried to leverage the new class-based views for maximum code efficiency.

The article content may use Markdown syntax. 

Any urls in the article content to videos at places like youtube, viddler and vimeo will be converted into an embedded viewer. See https://github.com/ixc/django-oembed/blob/master/oembed/fixtures/initial_data.json for the list of links that are handled.

Demo
----
The ultra simple blog is running at http://ultrasimpleblog.appspot.com.

Expected Behavior
-----------------
*This is the list of expected (and tested) behavior is generated using the './manage.py expectations' management command.*

- Article should:

  - leave the published date unset before being published.
  - set the published date when first published.
  - set the published date remains stable when re published.
  - should have an admin view.

- Article views should:

  - require login for create.
  - create.
  - require login for edit.
  - edit.
  - require login for delete.
  - delete.

- Article index view should:

  - be paginated.
  - only show published pages.
  
- Article unpublished index view should:

  - require login.
  - be paginated.
  - only show unpublished pages.

- Article detail view should:

  - be viewable without login if article is published.
  - require login if article is not published.

*I have not tested behaviors that are baked into the class-based generic views.*



Installation
------------

The Ultra Simple Blog runs on Google App Engine. As such, it has some quirks about where files should go. Here are the steps to get it working:

- Create a new virtualenv with --no-site-packages. I also set my python to by version 2.5 in the virtualenv, but I'm not sure if that makes a difference.

- Activate the virtualenv and the 'pip install -r requirements.txt' to clone and otherwise load all the dependencies.

- From the ultrasimpleblog_project directory run 'bash scripts/create_symlinks.sh' to link all the just-installed packages and static files into the project as required by GAE.

- Finally, deactivate the virtualenv, or use another terminal, and run the app with './manage.py runserver' as usual.

If you want to hack on this project you'll need to both keep the requirments.txt file up to date AND the create_symlinks.sh script. Be sure to create links for both the packages and any static files they contain.

