import os

curr_dir = os.path.dirname(os.path.realpath(__file__))

app_folder = os.path.join(curr_dir, 'dist/Jinseng.app/Contents/Frameworks')

def delete_qt_debug_files():
    for root, dirs, files in os.walk(app_folder):
        for f in files:
            if f.lower().endswith("_debug"):
                file_path = os.path.join(root, f)
                os.remove(file_path)
                print "Deleted %s" % file_path

if __name__ == '__main__':
    delete_qt_debug_files()