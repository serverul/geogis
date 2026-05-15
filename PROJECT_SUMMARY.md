# GeoGIS Project Summary

## Overview
Reverse engineering project to create QGIS plugin for Romanian cadastral data access.

## Research Findings

### GeoScript AutoCAD Plugin Analysis

#### Files Analyzed
- `GeoScript.VLX` (76KB) - Protected Visual LISP
- `GEOSCRIPT.des` (95KB) - Encrypted LISP
- `Geoscript.cuix` (14KB) - AutoCAD interface
- `Load_app.lsp` - Plugin loader
- `Sirutaf.csv` (693KB) - SIRUTA codes

#### The Secret Sauce Discovered
The plugin accesses ANCPI data through **public anonymous proxy endpoints** instead of authenticated ETERRA 3 API.

**Key Insight from v1.8 Changelog:**
> "Schimbarea adresei de descarcare a imobilelor (astfel incat sa fie posibil sa se poata descarca imobile chiar daca geoportalul nu functioneaza)"

Translation: Changed download address so parcels can be downloaded even when geoportal is down.

### Confirmed Working Endpoints

**ETERRA 3 Proxy Services (Public Access):**
```
https://eterra.ancpi.ro/eterra/proxy           - Status: 200 OK
https://eterra.ancpi.ro/eterra/proxy/parcel     - Status: 200 OK
https://eterra.ancpi.ro/eterra/proxy/imobile    - Status: 200 OK
https://eterra.ancpi.ro/eterra/proxy/geometry   - Status: 200 OK
https://eterra.ancpi.ro/eterra/proxy/intravilan - Status: 200 OK
```

**GEOPORTAL Services:**
```
https://geoportal.ancpi.ro/arcgis/rest/services/ - ArcGIS REST
```

**Contrast - Protected Endpoints (Returns 401):**
```
https://eterra.ancpi.ro/api/proxy   - Requires authentication
```

## QGIS Plugin Implementation

### Features
| Command | Feature | Status |
|---------|---------|--------|
| g6 | Parcel Download | ✅ Implemented |
| o5 | Orthophoto Plans | ⚠️ UI Ready |
| i5 | Topo Maps | ⚠️ UI Ready |
| u5 | Admin Boundaries | ⚠️ UI Ready |
| u6 | Intravilan Limits | ✅ Implemented |
| v6 | Overlap Check | 📋 Planned |
| ipk | Request Status | 📋 Planned |

### Plugin Structure
```
ro_ancpi_plugin/
├── __init__.py         # Plugin loader
├── ro_ancpi_plugin.py  # Main code
├── metadata.txt        # Plugin metadata
├── resources.qrc         # Qt resources
├── requirements.txt      # Dependencies
└── icons/icon.svg        # Plugin icon
```

## Version History

### QGIS Plugin
- v1.0.0 (2026-05-15): Initial release with parcel/intravilan download

### Original GeoScript
- v1.0: First functional version
- v1.8: Added proxy bypass mechanism
- v2.0: Direct ETERRA3 integration
- v2.90: BricsCAD 19 support

## Credits
- **Original GeoScript**: Benedictum (Linuxonasteroids)
- **QGIS Port**: Berry (via reverse engineering)