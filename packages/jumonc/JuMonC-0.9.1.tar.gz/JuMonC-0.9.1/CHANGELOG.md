# Changelog JuMonC


## [0.9.1] - 2022-12-14
### Added
- parameter LOCAL_ONLY
- parameter FLASK_DEBUG
- parameter INIT_FILE
- optional sleep in mpi wait for commands, to reduce CPU load during idle
- additional information available in cache searches
  - total pages
  - total entries fitting search

### Changed
- streamlined internal MPI communication, to reduce send data

### Fixed
- for python versions < 3.10 JuMoNC depends on typing-extension
- logging was not setup correctly for use with mpi
- links in cache searches for further pages were not including the path parameter


## [0.9.0] - 2022-11-13
### Added
- More avaiable CPU information
    - frequency
    - percentage utilization
- More avaiable job information:
    - hostname
- Additional option for network query
    - total, sums up chosen option over all interfaces
- Additional option for gpu query
    - pcie throughput
- Scheduling functionality added
- Parameter in REST API to only retrieve chache id
- Added parameter to v1/cache/list to allow to filter results
- Added example that shows more use cases `examples/03_expanded_overview_dashboard`

### Changed
- internal mpi communication
- DB minor version bump to 1.1.0
- REST-API version bump to 1.1.0

### Fixed
- Correct error message when a wrong id for cache retrival is supplied
- Disable disk plugin, in case of problems with psutil
- JuMonC port reachable from extern node


## [0.8.0] - 2022-06-22
### Changed
- Plugins
    - now using pluggy as plugin manager
    - [example plugin](https://gitlab.jsc.fz-juelich.de/coec/jumonc-logparser)


## [0.7.1] - 2022-05-23
### Fixed
- PyPi extra GPU was not available


## [0.7.0] - 2022-05-23
### Added
- GPU monitoring
    - only Nvidia GPUs
    - needs pynvml
    - PyPi extra target: GPU

### Fixed
- Internal MPI bug
- Sppeling mistake in cache error messages


## [0.6.0] - 2022-05-09
### Changed
- Code changed to fullfill changed CI
- using dynamic strings instead of varchar in cache DB
- removed unneeded IDs in DB, instead use composite keys

### Added
- It is now possible to use https connections with JuMonC for encrypted connections. See: [Readme Encryption](https://gitlab.jsc.fz-juelich.de/coec/jumonc#encryption)
- PyPi extras
- Cache access from REST-API
- CMD arguments to format REST-API cache output
- CMD argument to set path for DB
- DB version und version check


## [0.5.0] - 2022-04-29
### Added
- cache to retrieve old results based on a sql database


## [0.4.2] - 2022-04-19
### Changed
- Fixed error in user plugin


## [0.4.1] - 2022-04-19
### Changed
- Fixed error in disk plugin when missing (the optional dependency) psutil
