Changelog
=============


All notable changes to this project will be documented here.

`Development`_
--------------

.. note:: Changes noted in this subsection are to be released in the next version.
        If you're keen to check something out before its released, you can use a
        `development install <installation.html#development-installation>`__.

`0.1.0`_
--------------

`0.0.4`_
--------------

* Added :mod:`pyrolite_meltsutil.data`
* Data examples of finished experiments added to
  :mod:`pyrolite_meltsutil.data.data_examples`
* Updated automated docs example
* Added documentation example table styling with custom CSS
* Updated :mod:`pyrolite_meltsutil.env` to use data via
  :mod:`pyrolite_meltsutil.data.environment`
* Updated meltsfile export utility to be able to export variables encoded as
  lists, sets or tuples within singular :class:`pandas.DataFrame` columns
* Fixed a parsing issue for :func:`pyrolite_meltsutil.parse.from_melts_cstr`
  to deal with NaN/0.0/-0.0

:mod:`pyrolite_meltsutil.automation`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Split out :mod:`~pyrolite_meltsutil.automation` into submodule and
  organised files (
  :mod:`~pyrolite_meltsutil.automation.naming`,
  :mod:`~pyrolite_meltsutil.automation.org`,
  :mod:`~pyrolite_meltsutil.automation.process`,
  :mod:`~pyrolite_meltsutil.automation.timing`)
* Added timeouts for automated experiments within
  :class:`~pyrolite_meltsutil.automation.process.MeltsProcess`
* Started using hashes of configuration for indexing experiments to
  identify which are identical and avoid duplication
  (:class:`~pyrolite_meltsutil.automation.naming.exp_hash`,
  :class:`~pyrolite_meltsutil.automation.naming.exp_name`)
* Split out the indexes of the experiment grid (:code:`configs` &
  :code:`composition`, which together form a grid of :code:`experiments`)
* Made sure that experiment grids contain unique experiments - i.e. no duplication.
* Added :func:`pyrolite_meltsutil.automation.MeltsExperiment.dump` to serialize
  configuration for a series of experiments.

:mod:`pyrolite_meltsutil.tables`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Updated table read functions
* Converted tables to a submodule including
  :mod:`~pyrolite_meltsutil.tables.load`: and
  :mod:`~pyrolite_meltsutil.tables.util`
* Added :func:`~pyroilite_meltsutil.tables.load.convert_thermo_names` to convert
  with single-letter thermodynamic parameter names (including V/volume, which would
  conflict with vanadium, S/entropy which would conflict with sulfur and H/enthalpy
  which could potentially conflict with hydrogen).
* Added :func:`~pyrolite_meltsutil.tables.load.aggregate_tables` to aggregate all
  experiments within a directory to a single :class:`~pandas.DataFrame`
* Defaults updated to lowercase column names.
* Added :func:`~pyrolite_meltsutil.tables.load.import_batch_config` for importing
  configurations exported on run, in order to use relevant metadata.
* Bugfixes for inconsistent table widths with specific phases, where
  a column name is not added for :code:`structure` (nepheline, kalsilite, alloys)
* Added :func:`~pyrolite_meltsutil.tables.load.read_phase_table`
  for reading in phase tables.
* Added :func:`~pyrolite_meltsutil.tables.load.phasetable_from_phasemain` and
  :func:`~pyrolite_meltsutil.tables.load.phasetable_from_alphameltstxt` for reading
  phase tables from the `phasemain.txt` and `alphaMELTS_tbl.txt` files, respectively
* Added automatic detection of fractionation (i.e. where experiment mass changes
  beyond a threshold)
* Updated table percentages to be formatted as 0-100% (rather than fractional 0-1.)

:mod:`pyrolite_meltsutil.vis`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Added submodule for visualisation components
* Added styling functions in :mod:`~pyrolite_meltsutil.vis.style`
* Added SCSS function in :mod:`~pyrolite_meltsutil.vis.scss`
* Added :func:`~pyrolite_meltsutil.vis.templates.plot_xy_phase_groupby` and the
  convenience functions
  :func:`~pyrolite_meltsutil.vis.templates.plot_phasevolumes` and
  :func:`~pyrolite_meltsutil.vis.templates.plot_phasemasses`
* Added :func:`~pyrolite_meltsutil.vis.style.phaseID_marker` and updated
  :func:`pyrolite_meltsutil.vis.style.phaseID_linestyle` for modulating styling
  based on ID.

:mod:`pyrolite_meltsutil.util`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Added :func:`pyrolite_meltsutil.util.general.pyrolite_meltsutil_datafolder`
  to identify the relevant data folder.
* Added :func:`pyrolite_meltsutil.util.synthetic.isobaricGaleMORBexample`
  for generating a :class:`~pandas.DataFrame` based on the Gale (2013) MORB dataset
  for general use with :mod:`pyrolite_meltsutil`.
* Added :func:`~pyrolite_meltsutil.util.general.get_local_example`
  for loading examples installed with :code:`alphaMELTS`, and
  :func:`~pyrolite_meltsutil.util.general.get_local_link` for identifying the
  link files created upon :code:`alphaMELTS` installation.
* Added :func:`~pyrolite_meltsutil.util.general.get_data_example` to get the
  folder of an example already-finished experiment folder


`0.0.2`_
--------------

* Split out the :mod:`pyrolite-meltsutil` project from :mod:`pyrolite`
* Updated and refactored documentation


.. _Development: https://github.com/morganjwilliams/pyrolite/compare/0.0.2...develop
.. _0.0.2: https://github.com/morganjwilliams/pyrolite/compare/0.0.1...0.0.2
