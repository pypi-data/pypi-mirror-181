v1.0.1 (2022-12-15)
===================

Bugfixes
--------

- Fixed crash of fit caused by incorrectly set value of I_clear/I_sys if `remove_I_trend` option was set to `False`. (`#15 <https://bitbucket.org/dkistdc/dkist-processing-pac/pull-requests/15>`__)


Documentation
-------------

- Add changelog to RTD left hand TOC to include rendered changelog in documentation build. (`#14 <https://bitbucket.org/dkistdc/dkist-processing-pac/pull-requests/14>`__)


v1.0.0 (2022-11-02)
===================

Misc
----

- Major version change for production release.



v0.9.0 (2022-11-01)
===================

Bugfixes
--------

- Add correction angles to R23 and R45 in telescope model to account for true telescope mount configuration. (`#13 <https://bitbucket.org/dkistdc/dkist-processing-pac/pull-requests/13>`__)


Misc
----

- Change import of QhullError due to upcoming scipy deprecation. (`#11 <https://bitbucket.org/dkistdc/dkist-processing-pac/pull-requests/11>`__)


v0.8.1 (2022-09-30)
===================

Misc
----

- Refactor to expose `dkist_processing_pac.fitter.fitter_parameters.TELESCOPE_PARAMS` for other libraries (namely `dkist-processing-common`). (`#12 <https://bitbucket.org/dkistdc/dkist-processing-pac/pull-requests/12>`__)


v0.8.0 (2022-06-13)
===================

Features
--------

- Implement two-stage fitting method where Calibration Unit parameters are fit from a single globally-average bin and then fixed for the fits of each local bin's modulation matrix (`#10 <https://bitbucket.org/dkistdc/dkist-processing-pac/pull-requests/10>`__)


v0.7.0 (2022-06-03)
===================

Misc
----

- Complete rewrite to convert SV code to Data Center context (`#9 <https://bitbucket.org/dkistdc/dkist-processing-pac/pull-requests/9>`__)


v0.6.2 (2022-04-28)
===================

Features
--------

- Relaxed version to FITS specification to move to SPEC0122 Rev F.

v0.6.1 (2022-04-27)
===================

Bugfixes
--------

- Don't modify dresser polarizer and retarder values when using it to initialize a `CalibrationSequence` object

v0.6.0 (2022-04-19)
===================

Features
--------

- Include `lmfit` `MinimizerResult` objects in return from `FittingFramework.run_core` (`#7 <https://bitbucket.org/dkistdc/dkist-processing-pac/pull-requests/7>`__)
- Refactor to create `FittingFramework.prepare_model_objects` function (`#7 <https://bitbucket.org/dkistdc/dkist-processing-pac/pull-requests/7>`__)


Documentation
-------------

- Add changelog and towncrier machinery (`#5 <https://bitbucket.org/dkistdc/dkist-processing-pac/pull-requests/5>`__)


v0.5.1 (2022-03-31)
===================

Misc
----

- Don't throw annoying telescope db warnings if there is only 1 time listed in db (`#4 <https://bitbucket.org/dkistdc/dkist-processing-pac/pull-requests/4>`__)


v0.5.0 (2022-03-24)
===================

Bugfixes
--------

- "Q_in" now *always* fixed to 0 if `use_M12` flag is set in fit mode (`#3 <https://bitbucket.org/dkistdc/dkist-processing-pac/pull-requests/3>`__)


v0.4.1 (2022-03-10)
===================

Features
--------

- Added more fit_modes (`M12_fitUV`, `fit_QUV`, `no_T`, `use_M12`, and `use_M12_globalRet_globalTrans`)

v0.4.0 (2022-03-10)
===================

Features
--------

- Single Calibration Sequence steps now expected to come from separate IPs (`#2 <https://bitbucket.org/dkistdc/dkist-processing-pac/pull-requests/2>`__)


Bugfixes
--------

- Use "none" instead of 0 for angle in headers when GOS optic not in the beam (`#2 <https://bitbucket.org/dkistdc/dkist-processing-pac/pull-requests/2>`__)


v0.3.5 (2022-02-22)
===================

First version to touch DKIST summit data
