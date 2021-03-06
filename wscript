import Options
from os import unlink, link
from os.path import exists 

APPNAME = 'zeromq.node'
VERSION = "1.1.0"

def set_options(opt):
    opt.tool_options("compiler_cxx")

def configure(conf):
    conf.check_tool("compiler_cxx")
    conf.check_tool("node_addon")
    conf.check_cfg(atleast_pkgconfig_version='0.0.0', mandatory=True, errmsg='pkg-config was not found')
    conf.check_cfg(package='libzmq', uselib_store='ZMQ', atleast_version='3.1.0', args='--cflags --libs')
    conf.check(lib='uuid', uselib_store='UUID')

def build(bld):
    obj = bld.new_task_gen("cxx", "shlib", "node_addon")
    obj.cxxflags = ["-Wall", "-Werror"]
    obj.target = "binding"
    obj.source = "binding.cc"
    obj.uselib = "ZMQ"

def shutdown():
  # HACK to get binding.node out of build directory.
  # better way to do this?
  if exists('./binding.node'): unlink('./binding.node')
  if Options.commands['build']:
    if exists('./build/default/binding.node'):
      link('./build/default/binding.node', './binding.node')
    elif exists('./build/Release/binding.node'):
      link('./build/Release/binding.node', './binding.node')
    else:
      raise Exception("Cannot locate build binding.node")

