from ctypes import *
import os

def format_sql(request):
  PATH_TO_LIB = os.path.dirname(os.path.realpath(__file__)) + '/libnativeimpl.so'
  lib = cdll.LoadLibrary(PATH_TO_LIB)
  if lib == 0 :
    return("load lib failed.")

  thread = c_void_p(None)
  rc = lib.graal_create_isolate(None, None, byref(thread))
  if rc != 0 :
    return("error on isolate creation or attach")

  if request.method != 'POST':
    lib.Java_org_pkg_apinative_Native_hello.restype = c_char_p
    lib.Java_org_pkg_apinative_Native_hello.argtype = (c_void_p)
    hello = lib.Java_org_pkg_apinative_Native_hello(thread)
    return hello.decode('utf8')
  else:
    sql = request.get_data(as_text = True)
    lib.format_sql.restype = c_char_p
    lib.format_sql.argtypes = (c_void_p, c_char_p)
    formatted = lib.format_sql(thread, sql.encode('utf-8'))
    return formatted.decode('utf8')
