# Calliope release process

Prerequisites:

  * A PyPI account that is Collaborator of calliope-music PyPI project.

Steps:

  1. Check version number in `meson.build` is correct. Commit changes if
     needed.

  2. Check that `docs/changelog.rst` is up to date. (We should be updating
     this as we go).

  3. Commit and push any changes.

  4. Create a Git tag, manually replacing $VERSION with the correct version number:

         git tag -a -m "Release $VERSION" $VERSION

  5. Clean old builds from the Git tree:

         rm -R ./dist
    
  6. Build and upload the package:

         python3 -m pip install --upgrade build twine
         python3 -m build
         python3 -m twine upload dist/*

  7. Push the tag:

         git push --tags

For more detail, see: https://packaging.python.org/tutorials/packaging-projects/
