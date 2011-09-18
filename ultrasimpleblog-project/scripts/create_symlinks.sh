# A virtual env must be activated for this to work.
if [[ ! $VIRTUAL_ENV ]]; then 
    echo "You must first activate the virtualenv"
    exit 1
fi
if [[ ! `ls settings.py` ]]; then 
    echo "You must be in the base directory of the project (where settings.py sits)."
    exit 1
fi
here = `pwd`

echo
echo "Linking installed apps:"
ln -f -s $VIRTUAL_ENV/src/django-tip/django 
ln -f -s $VIRTUAL_ENV/src/djangotoolbox-tip/djangotoolbox 
ln -f -s $VIRTUAL_ENV/src/django-autoload-tip/autoload
ln -f -s $VIRTUAL_ENV/src/django-dbindexer-tip/dbindexer
ln -f -s $VIRTUAL_ENV/src/djangoappengine-tip djangoappengine
echo
echo "Linking static media:"
ln -f -s $here/static site_media/
ln -f -s $VIRTUAL_ENV/src/django-tip/django/contrib/admin/media site_media/admin
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

