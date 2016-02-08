# This is python 2 code :(
import os # from universe import everything...
import inspect
import shutil
import errno

class Installer(object):
    def __init__(self):
        self.run_dir = os.path.dirname(os.path.realpath(__file__)) # __file__ namespace
        self.install_dir = os.environ['HOME'] + "/.bin/"

    def who_called(self):
        return inspect.stack()[2][3]

    def make_dir(self):
         if os.path.exists(self.install_dir):
             print self.message("install dir exists, not modifying.")
         else:
             os.mkdir(self.install_dir)
             print self.message("Creating %s" % self.install_dir)

    def install_scripts(self):
        script_dir = self.run_dir + '/scripts/*'

        shutil.copyfile(script_dir,self.install_dir)

        # try:
        #     shutil.copytree(script_dir, self.install_dir)
        # except OSError as e:
        #     # If the error was caused because the source wasn't a directory
        #     if e.errno == errno.ENOTDIR:
        #         shutil.copy(script_dir, self.install_dir)
        #     else:
        #         print('Directory not copied. Error: %s' % e)



    def message(self,message):
        caller = self.who_called()
        if (caller == 'make_dir'):
            print "[DIR] " + message
        elif (caller == 'install_scripts'):
            print "[COPY] " + message
        elif (caller == 'add_path'):
            print "[ENV] " + message
        else:
            os.exit('Unhandled exception in message()!')






install_handle = Installer()
# install_handle.make_dir()
install_handle.install_scripts()
