from ctypes import *
import os

def hello_world(request):
  PATH_TO_LIB = os.path.dirname(os.path.realpath(__file__)) + '/libnativeimpl.so'
  lib = cdll.LoadLibrary(PATH_TO_LIB)

  thread = c_void_p(None)

  rc = lib.graal_create_isolate(None, None, byref(thread))

  if rc != 0 :
    return("error on isolate creation or attach")

  lib.Java_org_pkg_apinative_Native_hello.restype = c_char_p
  hello = lib.Java_org_pkg_apinative_Native_hello(thread)
  return hello.decode('utf8')
