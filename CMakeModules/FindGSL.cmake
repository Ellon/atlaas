find_package(PkgConfig)

# find gsl (for gdal wrapper)
pkg_check_modules(PC_GSL REQUIRED gsl)
set(GSL_DEFINITIONS ${PC_GSL_CFLAGS_OTHER})
find_path(GSL_INCLUDE_DIR gsl/gsl_math.h
    HINTS ${PC_GSL_INCLUDEDIR} ${PC_GSL_INCLUDE_DIRS}
    PATH_SUFFIXES gsl)
find_library(GSL_LIBRARY NAME gsl
    HINTS ${PC_GSL_LIBDIR} ${PC_GSL_LIBRARY_DIRS} )
set(GSL_INCLUDE_DIRS ${GSL_INCLUDE_DIR})
set(GSL_LIBRARIES ${GSL_LIBRARY})
##

include(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(GSL DEFAULT_MSG GSL_LIBRARY GSL_INCLUDE_DIR)
