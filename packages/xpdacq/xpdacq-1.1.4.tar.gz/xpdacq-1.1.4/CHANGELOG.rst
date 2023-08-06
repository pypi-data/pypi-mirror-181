xpdAcq Change Log
-----------------

.. current developments

v1.1.4
====================

**Added:**

* Added two functionalities from the old xpdacq back. glbl['dk_window'] = 300.0 will set the max_age in the first dark frame preprocessor to be 300.0 * 60.0 second. glbl['frame_acq_time'] = 0.1 will set the xpd_configuration['area_det'] frame acquisition time to be 0.1 s.



v1.1.3
====================

**Added:**

* Add the `xpdacq.twodetectors.TwoDectectors` module. It contains the plans to collect XRD and PDF on two detectors.

**Fixed:**

* Fixed the bug in scan plans. It now has the correct order of dimensions.



vv0.6.2
====================

**Added:**

* Add the `xpdacq.twodetectors.TwoDectectors` module. It contains the plans to collect XRD and PDF on two detectors.

**Fixed:**

* Fixed the bug in scan plans. It now has the correct order of dimensions.



v1.1.2
====================

**Fixed:**

* Add the missing data files for `simulators` module in the pypi release.



v1.1.1
====================

**Changed:**

* Change all databroker clients to `v2` version.

**Fixed:**

* Fix bugs caused by API changes in `databroker`. Make sure the package compatible with `databroker 2.0` and `bluesky 1.10`.



v1.1.0
====================

**Added:**

* Add `CalibPreprocessor` to record calibration data and put the data in the `calib` data stream.

* Add `DarkPreprocessor` to add taking dark frame steps into the plan, snapshot the dark frame and add it in the `dark` data stream.

* Add `ShutterPreprocessor` to open the shutter before the trigger of detector and close it after the wait.

* Add `xpdcaq.simulators` module. It contains the simulated devices for testing.

* Add `UserInterface` to create the objects necessary in the ipython session.

**Deprecated:**

* `periodic_dark` and `take_dark` are no longer used in `CustomizeRunEngine`. The dark frame is taken care by `DarkPreprocessor`.

* Setting `frame_acq_time` no longer changes the detector acquire time immmediately. The value will be read and used to set the acquire time when using the xpdacq customizd plans, like `ct`, `Tlist`, `Tramp` and `tseries`.

* `CustomizedRunEngine` no longer loads the calibration data at the `open_run`. The calibration data is handled by `CalibPreprocessor`.

* `auto_load_calib` no longer used in the global setting since the `CustomizedRunEngine` no longers loads the calibration data.

* `inner_shutter_control` is no longer used in the xpdacq customized plans. The shutter control is given to `ShutterPreprocessor`.

**Fixed:**

* Skip the outdated tests and make CI tests run smoothly.



v1.0.1
====================

**Added:**

* Remind users to tune the `glbl['auto_load_calib']` before using the `count_with_calib`.

**Fixed:**

* Fix the issue that the shutter will open before the dark run when using `count_with_calib`.



v1.0.0
====================

**Added:**

* Add `xpdacq.factory.BasicPlans` for the multi-detector plan for both XRD and PDF data collection in one run.

* Add `xpdacq.factory.MultiDistPlans` for the moving detector measurement for both XRD and PDF data collection in one run.

* Add `xpdacq.devices.CalibrationData`, a class to store the calibration data of a detector in configuration attributes.

* Add `xpdacq.beamtime.load_calibration_md`, a helper function to load calibration data

* Add `xpdacq.beamtime.count_with_calib`, a helper function to build multiple-calibration plan

**Fixed:**

* Fix the bugs for python 3.9 ``TypeError: dict.popitem() takes no arguments (1 given)``.

* Fix the bugs for xpdconf 0.4.5 that the default calibration metadata file is poni file instead of yaml file.



v0.12.0
====================

**Added:**

* A tool to inject metadata using the preprocessors.

* Add dependency on the pyopenxl

**Changed:**

* Translation of scan plans no longer injects the sample metadata

**Removed:**

* Remove dependency on the xlrd

**Fixed:**

* Fix the bug that bsui cannot start because of the importing from pyFAI.gui

* Fix the bug that translation of samples and plans can give None or a list unexpectedly

* Fix the bug that the sample metadata is not injected in the start documents.


v0.11.0
====================

**Added:**

* Add `xpdacq_mutator` as a plan mutator for the xpd experiments. `xrun` will use it in `__call___`

**Changed:**

* Optimized import

* Clean up redundant code

* Fix code style issues
* No longer import from xpdan in 999-load2.py

* Use temporary v2 databroker instread of v0 databroker in 999-load2.py

**Fixed:**

* Fix bugs in tests

* Fix the filter_band warnings



v0.10.4
====================

**Fixed:**

* fix yaml load synthax for pyyaml > 3.13



v0.10.1
====================

**Changed:**

* promote ``_close_shutter_stub`` and ``_open_shutter_stub`` to non-private
* use ``close_shutter_stub`` and ``open_shutter_stub`` where possible
* ``_configurate_area_det`` now yields properly



v0.10.0
====================

**Added:**

* Explicitly block user from starting new beamtime in the same python session
  after ``_end_beamtime`` has been run.

**Fixed:**

* Guard ``images_per_set`` because ``dexela`` detector doesn't have it



v0.9.1
====================

**Changed:**

* Don't release xpdAcq until new calibration has been written

**Fixed:**

* use shuter stubs in ``_shutter_step`` so the shutter delay is supported



v0.9.0
====================

**Changed:**

* `endbeamtime` process renames the local `xpdUser` to
  `xpdUser_<archive_name>` first before archiving and transferring
  file to remote location. This is to make sure the next beamtime
  will not be blocked by the backup process of last beamtime.

**Fixed:**

* Try except for new pyFAI calibration api vs old



v0.8.3
====================

**Added:**

* ``bt.robot_all`` to have a listing of all samples in the current mag
* ScanPlan API doc in https://xpdacq.github.io/xpdAcq/api_doc.html
* Add shutter sleep so in-situ works


**Changed:**

* Robot scan plan now has checkpoints, allowing better pausing


**Fixed:**

* Robot print statments now work properly

* Removed bad zip for robot




v0.8.2
====================

**Added:**

* ``swap`` capability to the ``glbl`` so that vars can be swapped out via
  context manager


**Changed:**

* ``Beamtime.robot_location_number`` takes in a geometry to specify the sample
  geometry
* Reduce summary field of callable argument in ``ScanPlan`` with only
  its ``__name__``. Before it use ``__repr__`` which includes hash and
  special characters that is prone to generate illegal filename for yaml.


**Removed:**

* Exception for non-robot multi-sample experiments, since they could happen
  and we do support this behavior


**Fixed:**

* ``per_step`` argument in ``Tlist``. Before this argument is always
  overridden by default.




v0.8.1
====================

**Added:**

Shutter control in ``tseries`` scan plan. By default, the shutter will only be open before collecting the data and close afterwards for protecting sample. Default behavior can be overridden by passing argument ``auto_shutter=False`` while creating scan plan. Please use ``tseries?`` in ``ipython`` session for full doc.




v0.8.0rc2
====================

**Changed:**

* xpdAcq now outsources ``glbl`` configuration management to xpdConf
* Run CI on conda-forge ``xpdconf``


**Removed:**

* ``load_configuration`` (which is now in xpdConf)


**Fixed:**

* Pull release notes prepend from GitHub




v0.8.0rc
====================

**Fixed:**

* Use simulation config if all else fails




v0.7.2
====================

**Added:**

* Changelogs are now displayed in the docs homepage and
  as their own page.
* xrun now can take a list of scans and run them in order
* Preliminary robot functionality, requiring location information


**Changed:**

* Moved to configuration file driven ``xpdacq_conf.py`` for greater flexability
* All doc ``rst`` files are passed through a jinja2 renderer
  before being built into docs. This will allow for greater
  flexability while writing the docs.


**Deprecated:**

* ``run_mask_builder`` function and relevant metadata injections.
    Dynamic mask is generated by ``xpdAn`` per run and mask server-client
    relationship will be tracked in analysis pipeline.


**Fixed:**

* Error in the docs where sphinx was finding the templates.




v0.7.1
====================

**Added:**

* Requirements folder


**Changed:**

* Release template now uses proper version in license
* Travis now uses the requirements folder


**Deprecated:**

* Replace most ``shutil`` functionalities with native Unix commands
  called by ``subprocess`` to have a clear picture on the system response.


**Fixed:**

* Add ``--timeout`` option to rsync during ``_end_beamtime`` to allow
  temporally disconnect.

* Exclude hidden files from the ``_end_beamtime`` archival. Those files
  are mainly used as configurations by local applications and are less
  likely to be reusable even if user requests them.




v0.7.0
====================

**Added:**

None

* Filter positions are recorded in metadata on each xrun.
* Added verification step: Beamline scientists must verify longterm beamline config file at the start of a new beamtime.

* Automatically display current filter positions (``In`` or ``Out``) from for every ``xrun``.


**Changed:**

* Change the filepath structure in ``glbl`` to align with the update
  at XPD. All ``xf28id1`` -> ``xf28id2``, including hostname and
  nfs-mount drives.


**Deprecated:**

* Remove static mask injection. Mask is now handled by the analysis
  pipeline dynamically.


**Fixed:**

* Instruction in ``run_calibration``. There is a specific print statement
  to tell the user to finish the interactive calibration process in the
  analysis terminal.

* Fix ``_end_beamtime``. Details about the fixes are:

  * Use rsync while archiving ``xpdUser`` so that user can see
    the progress. (rsync lists files have been transferred)

  * More sophisticated logic when flushing xpdUser directory.
    Now the function will tell the user to close files used by
    the current process, instead of throwing an error and failing
    the process.

  * Some cleaning in the logic. Program will remove the remote
    archive if user doesn't confirm to flush the local directory
    so that we could potentially avoid having multiple copies at
    the remote location.


v0.6.0
====================

This is a stable release of ``xpdAcq`` software.

This version is fully documented and extensively tested.

New features introduced to this version:

* Integration with automated data reduction pipeline. Now live visualization and
  automated data-saving is supported. For the details about the pipeline, please
  refer to `xpdAn documentation <http://xpdacq.github.io/xpdAn/>`_.


* Advanced shutter control logic for temperature-ramping scan plan,
  ``Tlist`` and ``Tramp``. By default, shutter will remain closed in
  between exposures, which prevent detector from burning. This behavior can
  be overridden, leaving the fast shutter open for the entire scan.
  Please refer to the function docstring by typing ``Tlist?`` or
  ``Tramp?`` in the ``collection`` terminal for more details.


* Refined metadata logic. We implement ``client-server`` logic which
  would largely enhance the linking between associated scans. For
  more details, please refer to :ref:`client_server_md`.


* Now programs takes in user defined folder tag so that it's easier to
  separate data into subfolders with memorable names. Please refer to
  :ref:`folder_tag`.


* Current version supports following built-in scans:

  .. code-block:: none

    single-frame (ct)
    time-series (tseries)
    temperature-series scans (Tramp)
    temperature-list scans (Tlist)


  Additional built-in scan types will be added in future releases.


v0.5.2
====================

This is a stable release of ``xpdAcq`` software.

Addition to all the features of ``v0.5.0``, new features introduced to this version are:

  * functionality to reload beamtime configuration when reenter into ``ipython`` session

  * improved logic of importing metadata from a spreadsheet, information is parsed in a
    way that facilitates data driven studies.

  * new ScanPlan: temperature list scan ``Tlist``. User can collect data at desired
    temperature points.

``v0.5.2`` supports following built-in scans:

.. code-block:: none

  single-frame (ct)
  time-series (tseries)
  temperature-series scans (Tramp)
  temperature-list scans (Tlist)

Additional built-in scan types will be added in future releases.

``v0.5.2`` also supports following automated logics :

  * :ref:`automated dark subtraction <auto_dark>`

  * :ref:`automated calibration capture <auto_calib>`

  * :ref:`automated mask per image <auto_mask>`

This version is fully documented and extensively tested.


v0.5.0
====================

This is a stable release of ``xpdAcq`` software.

New features introduced to this version:

  * flexibility of running customized ``bluesky`` plans while keeping ``xpdAcq`` dark collection logic.

  * ability of importing metadata from a spreadsheet, open the door for data driven studies.

  * data reduction tools:

    * azimuthal integration using ``pyFAI`` as the back-end
    * auto-masking based on statistics on pixel counts

``v0.5.0`` supports three kinds of built-in scans:

.. code-block:: none

  single-frame (ct)
  time-series (tseries)
  temperature-series scans (Tramp)

Additional built-in scan types will be added in future releases.

``v0.5.0`` supports following automated logics :

  * :ref:`automated dark subtraction <auto_dark>`

  * :ref:`automated calibration capture <auto_calib>`

  * :ref:`automated mask per image <auto_mask>`

This version is fully documented and extensively tested.

v0.3.0
====================

This is the first full, stable, release, of xpdAcq software.
It offers functionality to acquire data at XPD but with very limited
tools yet to analyze it.
Future releases will focus more on analysis functionalities.
``v0.3.0`` is still a limited functionality release in that it only supports three kinds of scans:

.. code-block:: none

  single-frame (ct)
  time-series (tseries)
  temperature-series scans (Tramp)

Additional scan types will be added in future releases.

However, it does support:
 * automated dark subtraction
 * automated calibration capture.

This version is fully documented and extensively tested.



