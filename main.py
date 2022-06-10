from PyQt5 import QtWidgets
from controller import MainWindowController

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindowController ()
    ui.UISetup ()
    ui.show ()
    sys.exit(app.exec_())