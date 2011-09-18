# A virtual env must be activated for this to work.
if [[ ! $VIRTUAL_ENV ]]; then 
    echo "You must first activate the virtualenv"
    exit 1
fi
if [[ ! `ls settings.py` ]]; then 
    echo "You must be in the base directory of the project (where settings.py sits)."
    exit 1
fi

ln -i -s $VIRTUAL_ENV/src/django-tip/django 
ln -i -s $VIRTUAL_ENV/src/djangotoolbox-tip/djangotoolbox 
ln -i -s $VIRTUAL_ENV/src/django-autoload-tip/autoload
ln -i -s $VIRTUAL_ENV/src/django-dbindexer-tip/dbindexer
ln -i -s $VIRTUAL_ENV/src/djangoappengine-tip djangoappengine
echo "---"
echo "Here are the results:"
find . -type l -maxdepth 1 | xargs ls -l
echo 
echo "---"
echo "Here are the symbolic links to be git ignored:"
find .  -type l -maxdepth 1
echo 
echo "---"
echo "Now deactivate the virtualenv and update .gitignore if necessary."
echo

