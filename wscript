#!/usr/bin/python3
"""
Script for waf build system.
"""

import os
from waflib.Tools.compiler_cxx import cxx_compiler
#TODO: enable cppcheck option
#import waftools

APPNAME = 'xxhash'
VERSION = '0.0.1'

cxx_compiler['linux'] = ['clang++']

def options(ctx):
    """
    Loads project options and needed code modules.
    """

    ctx.load('compiler_cxx')
    ctx.add_option('-a', '--avx', dest='avx', action="store_true", default=False,
                   help="Compile with AVX support. True/False")
    #ctx.load('cppcheck', tooldir=waftools.location)

def configure(ctx):
    """
    Configures Clang C++ compiler options.
    """

    ctx.load('compiler_cxx')

    ctx.env.append_value('CXXFLAGS',
                         ['-std=c++17', '-Wall', '-Werror', '-O3',
                          '-DNDEBUG'])

    if ctx.options.avx == True:
        print('Applications and libraries will be built with AVX support.')
        ctx.env.append_value('CXXFLAGS', ['-mavx', '-DAVX=TRUE'])

def build(bld):
    """
    Compiles dependencies and builds executables of the project.
    """

    bld(name = 'xxhash_includes',
        includes = './xxhash',
        export_includes = './xxhash'
    )

    bld.stlib(name = 'xxhash',
        features = 'cxx cxxstlib',
        target='xxhash',
        includes='../xxhash',
        source=bld.path.ant_glob('xxhash/**/*.cpp')
        #use=['tartarus_includes', 'tartarus', 'minerva_includes', 'cryptopp']
    )    






    # bld.objects(source='src/codes.cpp', target='codes')
    # bld.program(source='example/main.cpp',includes=['../src/'], target='app', use=['codes'])

    # bld(features='cxx cxxprogram',
    #     source='tests/CodesTest.cpp',
    #     target='apptest',
    #     includes=['include/', '../src/'],
    #     export_includes=['include/', '../src/'],
    #     libpath=['lib'],
    #     linkflags=['-pthread'],
    #     use=['hammingcode', 'hammingbytes', 'gtest'])

    # if '-mavx' in bld.env['CXXFLAGS']:
    #     bld(features='cxx cxxprogram',
    #         source='tests/AVXtest.cpp',
    #         target='avxtest',
    #         includes=['include/', '../src/'],
    #         export_includes=['include/', '../src/'],
    #         libpath=['lib']
    #     )

def test(ctx):
    """
    Runs all the tests.
    """

    utils.exec_command(ctx, './build/apptest')


def docs(ctx):
    """
    Produces documentation using Doxygen.
    """

    utils.exec_command(ctx, 'doxygen Doxyfile')

def distclean(ctx):
    """
    Cleans build files.
    """

    utils.delete(ctx, 'build')
    utils.delete(ctx, 'resolve_symlinks')
    utils.delete(ctx, 'resolved_dependencies')
    utils.delete(ctx, 'codewrapper-0.0.1.tar.bz2')
    utils.exec_command(ctx, 'rm build_current')
