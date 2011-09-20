# A virtual env must be activated for this to work.

python_version="python2.5"

if [[ ! $VIRTUAL_ENV ]]; then 
    echo "You must first activate the virtualenv"
    exit 1
fi
if [[ ! `ls settings.py` ]]; then 
    echo "You must be in the base directory of the project (where settings.py sits)."
    exit 1
fi

here=`pwd`
venv_src=$VIRTUAL_ENV/src
venv_installed=$VIRTUAL_ENV/lib/$python_version/site-packages
make_link="ln -f -s"

echo "Linking installed apps:"
$make_link $venv_src/django-tip/django 
$make_link $venv_src/djangotoolbox-tip/djangotoolbox 
$make_link $venv_src/django-autoload-tip/autoload
$make_link $venv_src/django-dbindexer-tip/dbindexer
$make_link $venv_src/djangoappengine-tip djangoappengine
$make_link $venv_installed/model_utils
$make_link $venv_installed/uni_form
$make_link $venv_installed/markdown
$make_link $venv_src/django-oembed/oembed
echo "Linking static media:"
$make_link $here/static site_media/
$make_link $venv_src/django-tip/django/contrib/admin/media site_media/admin
$make_link $venv_installed/uni_form/static/uni_form site_media/uni_form
echo "---"
echo "Here are the results:"
find . -type l | xargs ls -l
echo 
echo "---"
echo "Here are the symbolic links to be git ignored:"
find .  -type l -maxdepth 1
echo 
echo "---"
echo "Now deactivate the virtualenv and update .gitignore if necessary."
echo

