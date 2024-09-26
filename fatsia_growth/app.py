import os
import sys
import logging
import argparse

from PyQt5 import QtWidgets, QtCore


from fatsia_growth.app_info import __appname__
from fatsia_growth.views.mainwindow import MainWindow
from fatsia_growth.config import get_config
from fatsia_growth import configs as fatsiagrowth_configs
from fatsia_growth.utils.logger import logger, ColoredFormatter, ColoredLogger


def main():
    """App entry point"""

    #TODO: parameter here
    parser = argparse.ArgumentParser()
    
    parser.add_argument(
        "--logger-level",
        default="info",
        choices=["debug", "info", "warning", "fatal", "error"],
        help="logger level",
    )
    default_config_file = os.path.join(
        os.path.expanduser("~"), ".fatsiagrowthrc"
    )
    parser.add_argument(
        "--config",
        dest="config",
        help=(
            "config file or yaml-format string (default:"
            f" {default_config_file})"
        ),
        default=default_config_file,
    )
    
    
    args = parser.parse_args()
    
    # Set up the logger
    logger.setLevel(getattr(logging, args.logger_level.upper()))
    if not logger.hasHandlers():
        # This block ensures that the logger has a handler after class change
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)
        formatter = ColoredFormatter(ColoredLogger.FORMAT)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
    config_from_args = args.__dict__
    config_file_or_yaml = config_from_args.pop("config")
    fatsiagrowth_configs.current_config_file = config_file_or_yaml
    
    config = get_config(config_file_or_yaml, config_from_args)
    
    logger.info(f"Using config: {config}")
    
    # Enable scaling for high dpi screens
    QtWidgets.QApplication.setAttribute(
        QtCore.Qt.AA_EnableHighDpiScaling, True
    )  # enable highdpi scaling
    QtWidgets.QApplication.setAttribute(
        QtCore.Qt.AA_UseHighDpiPixmaps, True
    )  # use highdpi icons
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    
    # Create the Qt app
    app = QtWidgets.QApplication(sys.argv)
    # app.processEvents()
    app.setApplicationName(__appname__)
    
    window = MainWindow(
        app=app,
        config=config,
    )
    window.show()

    window.showMaximized()
    window.raise_()
    
    # Run the app
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
    
    

