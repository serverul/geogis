# -*- coding: utf-8 -*-
"""
GeoScript QGIS Plugin - Romanian Cadastral Data Access

Based on reverse engineered GeoScript AutoCAD plugin
"""

import os
import json
import requests
from qgis.PyQt.QtWidgets import (
    QDialog, QDockWidget, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QComboBox, QTextEdit, QProgressBar,
    QMessageBox, QFormLayout, QGroupBox, QAction
)
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtCore import Qt, QSettings
from qgis.core import (
    QgsProject, QgsVectorLayer, QgsFeature, QgsGeometry,
    QgsPointXY, QgsFields, QgsField, QgsWkbTypes
)
from qgis.gui import QgsMapToolEmitPoint

# API Configuration
ETERRA_PROXY = "https://eterra.ancpi.ro/eterra/proxy"
GEOPORTAL_BASE = "https://geoportal.ancpi.ro"
ARCGIS_REST = f"{GEOPORTAL_BASE}/arcgis/rest/services"

# SIRUTA codes cache
SIRUTA_CODELIST = {}

class GeoScriptDock(QDockWidget):
    """Main dockable widget for GeoScript functionality"""
    
    def __init__(self, iface):
        super().__init__()
        self.iface = iface
        self.setWindowTitle("GeoScript - Romanian Cadastral Data")
        self.setMinimumWidth(400)
        
        # Main tab widget
        self.tabs = QTabWidget()
        self.setWidget(self.tabs)
        
        # Create tabs
        self.create_parcel_tab()
        self.create_orthophoto_tab()
        self.create_topo_tab()
        self.create_admin_tab()
        self.create_intravilan_tab()
        
        # Load SIRUTA codes
        self.load_siruta_codes()
    
    def load_siruta_codes(self):
        """Load SIRUTA codes from embedded data"""
        # In production, this would load from Sirutaf.csv
        pass
    
    def create_parcel_tab(self):
        """Create parcel download tab"""
        widget = QWidget()
        layout = QFormLayout(widget)
        
        self.county_combo = QComboBox()
        self.county_combo.addItems(["Bucuresti", "Ilfov", "Prahova", "Cluj", "Timis"])
        
        self.locality_input = QLineEdit()
        self.parcel_input = QLineEdit()
        
        self.download_btn = QPushButton("Download Parcel (g6)")
        self.download_btn.clicked.connect(self.download_parcel)
        
        layout.addRow(QLabel("County:"), self.county_combo)
        layout.addRow(QLabel("Locality:"), self.locality_input)
        layout.addRow(QLabel("Parcel Number:"), self.parcel_input)
        layout.addRow(self.download_btn)
        
        self.tabs.addTab(widget, "Parcels (g6)")
    
    def create_orthophoto_tab(self):
        """Create orthophoto download tab"""
        widget = QWidget()
        layout = QFormLayout(widget)
        
        self.resolution_combo = QComboBox()
        self.resolution_combo.addItems(["0.5m", "1m", "2m", "5m"])
        
        self.orthophoto_btn = QPushButton("Download Orthophoto (o5)")
        self.orthophoto_btn.clicked.connect(self.download_orthophoto)
        
        layout.addRow(QLabel("Resolution:"), self.resolution_combo)
        layout.addRow(self.orthophoto_btn)
        layout.addRow(QLabel("Select area on map after clicking"))
        
        self.tabs.addTab(widget, "Orthophoto (o5)")
    
    def create_topo_tab(self):
        """Create topographic maps tab"""
        widget = QWidget()
        layout = QFormLayout(widget)
        
        self.topo_btn = QPushButton("Download Topo Map (i5)")
        self.topo_btn.clicked.connect(self.download_topo)
        
        layout.addRow(self.topo_btn)
        
        self.tabs.addTab(widget, "Topo Maps (i5)")
    
    def create_admin_tab(self):
        """Create administrative boundaries tab"""
        widget = QWidget()
        layout = QFormLayout(widget)
        
        self.admin_level_combo = QComboBox()
        self.admin_level_combo.addItems(["County", "Municipality", "Commune"])
        
        self.admin_btn = QPushButton("Download Admin Boundaries (u5)")
        self.admin_btn.clicked.connect(self.download_admin)
        
        layout.addRow(QLabel("Level:"), self.admin_level_combo)
        layout.addRow(self.admin_btn)
        
        self.tabs.addTab(widget, "Admin (u5)")
    
    def create_intravilan_tab(self):
        """Create intravilan limits tab"""
        widget = QWidget()
        layout = QFormLayout(widget)
        
        self.intravilan_county = QComboBox()
        self.intravilan_county.addItems(["Bucuresti", "Ilfov"])
        
        self.intravilan_btn = QPushButton("Download Intravilan (u6)")
        self.intravilan_btn.clicked.connect(self.download_intravilan)
        
        layout.addRow(QLabel("County:"), self.intravilan_county)
        layout.addRow(self.intravilan_btn)
        
        self.tabs.addTab(widget, "Intravilan (u6)")
    
    def download_parcel(self):
        """Download parcel geometry using ETERRA proxy"""
        county = self.county_combo.currentText()
        locality = self.locality_input.text()
        parcel = self.parcel_input.text()
        
        if not locality or not parcel:
            QMessageBox.warning(self, "Input Error", "Please fill locality and parcel number")
            return
        
        try:
            # Use anonymous proxy endpoint
            url = f"{ETERRA_PROXY}/parcel"
            payload = {
                "judet": county[:2].upper(),  # County code
                "localitate": locality,
                "nr": parcel
            }
            
            response = requests.post(url, json=payload, timeout=30)
            
            if response.status_code == 200:
                self.process_and_add_layer(response.content, "Parcels")
            else:
                QMessageBox.critical(self, "Error", f"Download failed: {response.status_code}")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
    
    def download_orthophoto(self):
        """Download orthophoto from GEOPORTAL"""
        QMessageBox.information(self, "Info", "Select area on map for orthophoto extraction")
        # Implementation for map selection
    
    def download_topo(self):
        """Download topographic map"""
        QMessageBox.information(self, "Info", "Topo map download coming soon")
    
    def download_admin(self):
        """Download administrative boundaries"""
        QMessageBox.information(self, "Info", "Admin boundaries download coming soon")
    
    def download_intravilan(self):
        """Download intravilan limits"""
        county = self.intravilan_county.currentText()
        
        try:
            url = f"{ETERRA_PROXY}/intravilan"
            payload = {"judet": county[:2].upper()}
            
            response = requests.post(url, json=payload, timeout=30)
            
            if response.status_code == 200:
                self.process_and_add_layer(response.content, "Intravilan")
            else:
                QMessageBox.critical(self, "Error", f"Download failed: {response.status_code}")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
    
    def process_and_add_layer(self, data, layer_name):
        """Process downloaded data and add to QGIS"""
        # Placeholder for actual data processing
        # Would implement GeoJSON/Shapefile/DXF parsing
        QMessageBox.information(self, "Success", f"{layer_name} downloaded successfully")


class GeoScriptPlugin:
    """Main plugin class for QGIS"""
    
    def __init__(self, iface):
        self.iface = iface
        self.dock = None
        self.action = None
    
    def initGui(self):
        """Initialize GUI components"""
        # FIXED for QGIS 3.x - create QAction instead of passing QIcon directly
        icon = QIcon(":/plugins/ro_ancpi_plugin/icon.svg")
        self.action = QAction(icon, "ANCPI GeoScript", self.iface.mainWindow())
        self.action.triggered.connect(self.show_dock)
        
        self.iface.addToolBarIcon(self.action)
        
        # Also add to menu
        self.iface.addPluginToMenu("&ANCPI GeoScript", self.action)
        
        # Create dock widget
        self.dock = GeoScriptDock(self.iface)
        self.iface.addDockWidget(Qt.RightDockWidgetArea, self.dock)
    
    def show_dock(self):
        """Show the dock widget"""
        if self.dock:
            self.dock.show()
    
    def unload(self):
        """Unload plugin"""
        if self.dock:
            self.iface.removeDockWidget(self.dock)
        if self.action:
            self.iface.removeToolBarIcon(self.action)
            self.iface.removePluginMenu("&ANCPI GeoScript", self.action)