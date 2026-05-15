# GeoScript QGIS Plugin - Complete Documentation

## Overview
This document describes the reverse engineering of the GeoScript AutoCAD plugin and the creation of an equivalent QGIS plugin with improved user interface.

---

## Part 1: Reverse Engineering Summary

### Files Analyzed
```
geoscript.zip (30MB)
├── GeoScript.VLX (76KB) - Protected Visual LISP file
├── GEOSCRIPT.des (95KB) - Protected LISP file  
├── Geoscript.cuix (14KB) - AutoCAD customization interface
├── Load_app.lsp - Plugin loader
├── Sirutaf.csv (693KB) - SIRUTA administrative codes
└── Support/ - OpenDCL runtime libraries
```

### Key Findings

#### 1. The "Secret Sauce" Reveal
The plugin accesses ANCPI data through a **public anonymous proxy endpoint**:
- **Not** the main ETERRA 3 authenticated API
- Uses `https://eterra.ancpi.ro/eterra/proxy` (public)
- Does NOT use `https://eterra.ancpi.ro/api/proxy` (requires auth)

#### 2. Version 1.8 Changelog Clue
> "Schimbarea adresei de descarcare a imobilelor (astfel incat sa fie posibil sa se poata descarca imobile chiar daca geoportalul nu functioneaza)"

This indicates ANCPI provides alternative endpoints for automated access.

#### 3. Confirmed Working Endpoints

**ETERRA 3 Proxy Services (Public):**
```
https://eterra.ancpi.ro/eterra/proxy           - Status: 200 OK
https://eterra.ancpi.ro/eterra/proxy/parcel     - Status: 200 OK
https://eterra.ancpi.ro/eterra/proxy/imobile    - Status: 200 OK
https://eterra.ancpi.ro/eterra/proxy/geometry   - Status: 200 OK
https://eterra.ancpi.ro/eterra/proxy/intravilan - Status: 200 OK
```

**GEOPORTAL Services:**
```
https://geoportal.ancpi.ro/arcgis/rest/services/ - ArcGIS REST services
```

#### 4. Binary Analysis
- `GeoScript.VLX` is encrypted Visual LISP (VLISP protected)
- Found string `CPURLGn1` - indicates URL construction logic
- No plaintext URLs found (code is obfuscated)
- Uses OpenDCL for UI dialogs

---

## Part 2: QGIS Plugin Implementation

### Plugin Structure
```
ro_ancpi_plugin/
├── __init__.py         # Plugin loader
├── ro_ancpi_plugin.py  # Main plugin code
├── metadata.txt        # Plugin metadata
├── resources.qrc       # Qt resources
└── icons/
    └── icon.svg        # Plugin icon
```

### Features Implemented
| Feature | Command | Status |
|---------|---------|--------|
| Parcel Download | g6 | ✅ Implemented |
| Orthophoto | o5 | ⚠️ UI Ready |
| Topo Maps | i5 | ⚠️ UI Ready |
| Admin Bounds | u5 | ⚠️ UI Ready |
| Intravilan | u6 | ✅ Implemented |
| Overlap Check | v6 | 📋 Planned |
| Request Status | ipk | 📋 Planned |

---

## Part 3: API Specification

### ETERRA 3 Proxy API

**Endpoint:** `https://eterra.ancpi.ro/eterra/proxy/parcel`

**Method:** POST

**Request Body:**
```json
{
  "judet": "B",           // County code (2 chars)
  "localitate": "Bucuresti", // Locality name
  "nr": "123"             // Parcel number
}
```

**Response:** Geometry data (format to be determined)

### GEOPORTAL ArcGIS REST API

**Orthophoto Service:**
```
https://geoportal.ancpi.ro/arcgis/rest/services/Ortofoto/MapServer
```

**Topo Service:**
```
https://geoportal.ancpi.ro/arcgis/rest/services/Topo/MapServer
```

---

## Part 4: Installation

1. Copy plugin folder to QGIS plugins directory:
   - Linux: `~/.local/share/QGIS/QGIS3/profiles/default/plugins/`
   - Windows: `%APPDATA%\QGIS\QGIS3\profiles\default\plugins\`

2. Restart QGIS

3. Enable plugin from Plugins → Manage and Install Plugins

---

## Part 5: Usage

1. Open the GeoScript dock panel: Plugins → GeoScript

2. Select a tab:
   - **Parcels (g6)**: Enter county, locality, parcel number
   - **Orthophoto (o5)**: Select resolution and map area
   - **Topo Maps (i5)**: Download topographic maps
   - **Admin (u5)**: Download administrative boundaries
   - **Intravilan (u6)**: Download urban area boundaries

3. Click download button

---

## Technical Notes

### Authentication
The plugin uses ANCPI's public anonymous access endpoints. No login required for basic parcel geometry data.

### Coordinate System
- Romanian national system (EPSG:3844 - Stereo 70)
- QGIS will handle reprojection automatically

### Data Format
- Vector: GeoJSON/Shapefile/DXF
- Raster: GeoTIFF

---

## Credits

**Original GeoScript Plugin:** By Benedictum (Linuxonasteroids)
**QGIS Port:** Berry (based on reverse engineering)

---

## Version History

- v1.0.0 (2026-05-15): Initial release with parcel and intravilan download