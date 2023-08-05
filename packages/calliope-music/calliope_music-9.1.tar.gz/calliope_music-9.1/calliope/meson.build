sources = files(
  '__init__.py',
  '__main__.py',
  'cache.py',
  'cli.py',
  'config.py',
  'database.py',
  'interface.py',
  'playlist.py',
  'resolvers.py',
  'sync_operation.py',
  'utils.py',
)

jsonschema = files(
  'playlist-item.jsonschema',
)

python.install_sources(
    sources + jsonschema,
    subdir: 'calliope')

if get_option('direct_install')
  configure_file(
    input: 'modules.conf.in',
    output: 'modules.conf',
    configuration: modules,
    install_dir: join_paths(python.get_install_dir(), 'calliope'))
endif

configure_file(
    input: 'main.py.in',
    output: 'cpe',
    configuration: cdata,
    install_dir: get_option('bindir'))

# Sources for the whole 'calliope' module. This variable is appended to by the
# meson.build files inside the package subdirectories.
calliope_module_sources = sources
calliope_jsonschema = jsonschema

subdir('beets')
subdir('diff')
subdir('export')
subdir('import_')
subdir('shuffle')
subdir('stat')
subdir('sync')
subdir('validate')

if not get_option('direct_install') or modules.get('enable_bandcamp')
  subdir('bandcamp')
endif

if not get_option('direct_install') or modules.get('enable_lastfm')
  subdir('lastfm')
endif

if not get_option('direct_install') or modules.get('enable_listenbrainz')
  subdir('listenbrainz')
endif

if not get_option('direct_install') or modules.get('enable_musicbrainz')
  subdir('musicbrainz')
endif

if not get_option('direct_install') or modules.get('enable_play')
  subdir('play')
endif

if not get_option('direct_install') or modules.get('enable_select')
  subdir('select')
endif

if not get_option('direct_install') or modules.get('enable_spotify')
  subdir('spotify')
endif

if not get_option('direct_install') or modules.get('enable_suggest')
  subdir('suggest')
endif

if not get_option('direct_install') or modules.get('enable_tracker')
  subdir('tracker')
endif

if not get_option('direct_install') or modules.get('enable_youtube')
  subdir('youtube')
endif

subdir('subprojects')
