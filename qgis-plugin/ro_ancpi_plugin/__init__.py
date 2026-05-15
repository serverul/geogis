# -*- coding: utf-8 -*-
"""
GeoScript QGIS Plugin

Based on reverse engineered GeoScript AutoCAD plugin
Provides access to Romanian cadastral data (ETERRA 3, GEOPORTAL ANCPI)
"""

import os
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtCore import QSettings

# Import the main plugin class
from .ro_ancpi_plugin import GeoScriptPlugin


def classFactory(iface):
    """Load the plugin class"""
    return GeoScriptPlugin(iface)