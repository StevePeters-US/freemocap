import logging
from pathlib import Path
from typing import Union

from PyQt6.QtCore import pyqtSignal, QFileSystemWatcher
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QWidget
from pyqtgraph.parametertree import Parameter, ParameterTree

from freemocap.parameter_info_models.recording_info_model import (
    RecordingInfoModel,
)
from freemocap.system.paths_and_files_names import get_most_recent_recording_path

logger = logging.getLogger(__name__)


class sensor_widget(QWidget):
   print('Sensor Widget activated')
