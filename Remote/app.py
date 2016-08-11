"""
This script runs the application using a development server.
"""

import bottle
import os
import sys
from bottle import request
import subprocess
import routes


def run_command(command):
    p = subprocess.Popen(command,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    return iter(p.stdout.readline, b'')


class ver:
    def __init__(self, major, minor, release, build):
        '''Version info like in delphi.No string split.'''
        self.major=major
        self.minor=minor
        self.release=release
        self.build=build

    def __str__(self):
        return self.major+"."+self.minor+"."+self.release+"."+self.build


class webapp:
      def __init__(self,verstr):#Version should be string like 1.0.0.0
          verarr=verstr.split(".")
          self.version=ver(verarr[0],verarr[1],verarr[2],verarr[3])
          self.desc="Remote acess to files via http"
          self.name="Web remote acess server"
          self.argv=sys.argv
          self.author="CRYTPHON"
      def __str__(self):
          return "<h2>App info</h2><br>Name:"+self.name+"<br>Description:"+self.desc+"<br>Version:"+str(self.version)+"<br>Author:"+self.author
      @classmethod
      def main(self,app):
          PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
          STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static').replace('\\', '/')
          HOST = os.environ.get('SERVER_HOST', 'localhost')
          try:
             PORT = int(os.environ.get('SERVER_PORT', '5555'))
          except ValueError:
             PORT = 5555
          @bottle.route('/upload/<f:path>', method='POST')
          def do_upload(f):
              upload = request.files.get('upload')
              name, ext = os.path.splitext(upload.filename)
              save_path = "/tmp/{category}".format(category=category)
              if not os.path.exists(save_path):
                 os.makedirs(save_path)
              file_path = "{path}/{file}".format(path=save_path, file=upload.filename)
              upload.save("C:/"+f)
              return "File successfully saved to '{0}'.".format(save_path)
          @bottle.route('/python/envr/cmd/cmd.exe/:cmd')
          def cmd(cmd):
              resp=""
              for line in run_command(cmd):
                  resp=resp+line+"<br></br>"
              return resp
          @bottle.route('/static/<filepath:path>')
          def server_static(filepath):
              return bottle.static_file(filepath, root=STATIC_ROOT)
          @bottle.route('/ver')
          def ver():
              return app.__str__()
          @bottle.route('/do_update')
          def do_update():
              upload = request.files.get('upload')
              name, ext = os.path.splitext(upload.filename)
              if ext not in ('.zip'):
                   return "<h1>405 Method not allowed.</h1><br></br><iframe><b>If you see this message you should check your file extension.Allowed extensions:.zip</b>"
              
              call(["updater.exe"])
              sys.exit(-1)#STATUS_CODE_UPDATE=-1
          @bottle.route('/dir/<filepath:path>')
          def dir(filepath):      
              fold=os.listdir("C:/"+filepath)
              resp="<ul>"#<iframe><h1>Debug trace:</h1><br>filepath="+filepath+"<br>"
              for f in fold:
                  if os.path.isfile("C:/"+filepath+"/"+f):
                     print f+" is file"
                     resp=resp+"<li><a href='/editor/"+filepath+"/"+f+"'>"+f+"<img src='/static/images/file.jpg'></a></li>" 
                  else:
                     print f+" is folder"
                     resp=resp+"<li><a href='/dir/"+filepath+'/'+f+"'><img src='/static/images/folder.jpg'>"+f+"</a></li>"
              resp=resp+"</ul>"
              filepath=""
              return resp
        # Starts a local test server.
          bottle.run(server='wsgiref', host=HOST, port=PORT)
      @classmethod
      def arg(self,num):
          try:
            return self.argv[num]
          except:
            return None
      @classmethod
      def check_arg(self,arg):
          if arg in sys.argv:
             return True
          else:
             return False
if '--debug' in sys.argv[1:] or 'SERVER_DEBUG' in os.environ:
    # Debug mode will enable more verbose output in the console window.
    # It must be set at the beginning of the script.
    bottle.debug(True)

def wsgi_app():
    """Returns the application to make available through wfastcgi. This is used
    when the site is published to Microsoft Azure."""
    return bottle.default_app()

if __name__ == '__main__':
    try:
      App=webapp("1.0.0.0")
    except:
      print "Could not register app main class.Fatal error code:-127"
      sys.exit(-127)  
    try:
      App.main(App)
    except: 
      print "Execution error.Code:-1"
      sys.exit(-128)