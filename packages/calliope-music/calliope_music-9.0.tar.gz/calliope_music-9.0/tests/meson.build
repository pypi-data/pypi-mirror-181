calliope_source_dir = top_source_dir / 'calliope'
run_target('pylint',
  command: [run_from_source_tree, top_source_dir, top_build_dir,
    pylint, '--rcfile', join_paths(top_source_dir, 'pylintrc'),
    calliope_source_dir])

skip_test = find_program('../scripts/skip_test', required: true)

tracker_testutils = dependency('tracker-testutils-3.0', required: get_option('tracker'))
if tracker_testutils.found()
  tracker_sandbox_cmd = find_program(tracker_testutils.get_variable(pkgconfig: 'command'))
  tracker_sandbox_python_path = tracker_testutils.get_variable(pkgconfig: 'python_path')
else
  tracker_sandbox_cmd = ''
  tracker_sandbox_python_path = ''
endif

tests = [
  'test_bandcamp.py',
  'test_cache.py',
  'test_cli.py',
  'test_core.py',
  'test_diff.py',
  'test_export.py',
  'test_import_pls.py',
  'test_import_xspf_jspf.py',
  'test_lastfm_history.py',
  'test_listenbrainz.py',
  'test_listenbrainz_history.py',
  'test_musicbrainz.py',
  'test_select.py',
  'test_sync.py',
  'test_spotify.py',
  'test_validate.py',
]

tracker_tests = [
  'test_tracker.py',
  'test_tracker_search.py',
]

run_from_source_tree_args = [top_source_dir, top_build_dir, pytest.path(), '--capture=no']
foreach t: tests
  timeout = 30
  if t == 'test_cache.py'
    timeout = 240
  endif
  test(t, run_from_source_tree,
    args: run_from_source_tree_args + [join_paths('tests', t)],
    # We can put a pytest.ini file in this directory to configure pytest.
    workdir: top_source_dir,
    timeout: timeout
  )
endforeach

foreach t: tracker_tests
  if modules.get('enable_tracker')
    test(t, run_from_source_tree,
      args: run_from_source_tree_args + [join_paths('tests', t)],
      env: { 'TRACKERTESTUTILS_DIR': tracker_sandbox_python_path },
      workdir: top_source_dir)
  else
    test(t, skip_test)
  endif
  # FIXME: mark test as skipped if we can't run it.
endforeach
