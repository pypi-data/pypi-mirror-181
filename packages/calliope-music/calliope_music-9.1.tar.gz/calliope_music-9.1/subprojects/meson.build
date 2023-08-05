sources = files('__init__.py')

python.install_sources(
    sources,
    subdir: 'calliope/subprojects')

calliope_module_sources += sources

if not get_option('direct_install') or modules.get('enable_bandcamp')
  install_subdir(
    'bandcamp_api',
    exclude_directories: ['.git'],
    exclude_files: ['.gitignore', 'LICENSE', 'README.md'],
    install_dir: python.get_install_dir() / 'calliope' / 'subprojects')
endif

if not get_option('direct_install') or modules.get('enable_lastfm')
  install_subdir(
      'lastfmclient/lastfmclient',
      exclude_directories: ['.git'],
      exclude_files: ['.gitignore', 'LICENSE', 'README.md'],
      install_dir: python.get_install_dir() / 'calliope' / 'subprojects')
endif

if not get_option('direct_install') or modules.get('enable_listenbrainz')
  install_subdir(
      'pylistenbrainz/pylistenbrainz',
      exclude_directories: ['tests'],
      install_dir: python.get_install_dir() / 'calliope' / 'subprojects')
endif
