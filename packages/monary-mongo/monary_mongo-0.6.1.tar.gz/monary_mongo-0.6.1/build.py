import os
import pkgconfig
import warnings
from distutils.errors import CCompilerError, DistutilsExecError, DistutilsPlatformError
from distutils.command.build_ext import build_ext
from setuptools import Extension

class BuildFailed(Exception):
    pass


class ExtBuilder(build_ext):

    def run(self):
        try:
            build_ext.run(self)
        except (DistutilsPlatformError, FileNotFoundError):
            raise BuildFailed('File not found. Could not compile C extension.')

    def build_extension(self, ext):
        try:
            build_ext.build_extension(self, ext)
        except (CCompilerError, DistutilsExecError, DistutilsPlatformError, ValueError):
            raise BuildFailed('Could not compile C extension.')


def build(setup_kwargs):
    """
    This function is mandatory in order to build the extensions.
    """
    
    DEBUG = False
    CFLAGS = ["-fPIC", "-O2"]
    if not DEBUG:
        CFLAGS.append("-DNDEBUG")

    libraries = ["bson-1.0", "crypto", "ssl", "sasl2", "mongoc-1.0"]
        
    settings = {
        'export_symbols': ["monary_init",
                        "monary_cleanup",
                        "monary_connect",
                        "monary_disconnect",
                        "monary_use_collection",
                        "monary_destroy_collection",
                        "monary_alloc_column_data",
                        "monary_free_column_data",
                        "monary_set_column_item",
                        "monary_query_count",
                        "monary_init_query",
                        "monary_init_aggregate",
                        "monary_load_query",
                        "monary_close_query",
                        "monary_create_write_concern",
                        "monary_destroy_write_concern",
                        "monary_insert"],
        'sources': [os.path.join("monary_mongo", "cmonary.c")],
    }

    if pkgconfig.exists("libmongoc-1.0"):
        pkgcfg = pkgconfig.parse("libmongoc-1.0")
        settings['include_dirs'] = list(pkgcfg['include_dirs'])
        settings['library_dirs'] = list(pkgcfg['library_dirs'])
        settings['libraries'] = list(pkgcfg['libraries'])
        settings['define_macros'] = list(pkgcfg['define_macros'])
    else:
        warnings.warn(("WARNING: unable to find libmongoc-1.0 with pkgconfig"))

    ext_modules = [
        Extension('monary_mongo.libcmonary',
            extra_compile_args  = CFLAGS,
            include_dirs        = settings['include_dirs'],
            libraries           = settings['libraries'],
            library_dirs        = settings['library_dirs'],
            export_symbols      = settings['export_symbols'],
            sources             = settings['sources']),
    ]

    # Get README info
    try:
        with open("README.rst") as fd:
            readme_content = fd.read()
    except:
        readme_content = ""
    
    setup_kwargs.update(
        {"ext_modules": ext_modules, "cmdclass": {"build_ext": ExtBuilder}}
    )
