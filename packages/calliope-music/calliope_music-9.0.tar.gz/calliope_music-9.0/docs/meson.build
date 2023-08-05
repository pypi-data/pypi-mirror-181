sphinx_sources = [
  'conf.py',
  'basics.rst',
  'changelog.rst',
  'index.rst',
  'format.rst',
  'reference-cli.rst',
  '_static/custom.css',
  '_static/uk.me.afuera.Calliope.png',
  'getting-data.rst',
  'getting-data/local.rst',
  'getting-data/online.rst',
  'getting-data/api-keys.rst',
  'making-playlists.rst',
  'examples.rst',
  'examples/simple.rst',
  'examples/listen-history.rst',
  'examples/similar-tracks.rst',
  'examples/misc.rst',
]

output_dir = meson.current_build_dir()

docs_html = custom_target('docs',
  build_by_default: true,
  command: [run_from_source_tree, top_source_dir, top_build_dir,
            sphinx_build, '-M', 'html', meson.current_source_dir(),
            output_dir, '-W'],
  depend_files: sphinx_sources + calliope_module_sources + calliope_jsonschema + calliope_example_sources,
  # We only list one output.
  output: ['html']
)
