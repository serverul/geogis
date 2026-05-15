# GeoGIS - Romanian Geospatial Tools

A collection of geospatial tools for accessing Romanian cadastral and map data from ANCPI services.

## 🚀 QGIS Plugin

**[ro_ancpi_plugin](qgis-plugin/ro_ancpi_plugin/)** - QGIS plugin for Romanian Cadastral Data

Access ETERRA 3 and GEOPORTAL ANCPI without authentication!

### Features
- **Parcel Download (g6)** - Download cadastral parcel geometries from ETERRA 3
- **Orthophoto Plans (o5)** - Download orthophoto images from GEOPORTAL
- **Topographic Maps (i5)** - Download topo maps
- **Admin Boundaries (u5)** - Download administrative boundaries
- **Intravilan Limits (u6)** - Download urban area boundaries
- **Overlap Verification (v6)** - Property overlap checking
- **Request Status (ipk)** - Check cadastral request status

### Installation
```bash
# Copy plugin to QGIS directory
cp -r qgis-plugin/ro_ancpi_plugin ~/.local/share/QGIS/QGIS3/profiles/default/plugins/
```

Restart QGIS and enable via Plugins → GeoScript.

## 🔍 Technical Details

### The "Secret Sauce"
This plugin uses ANCPI's **public anonymous proxy endpoints** that don't require login:

```python
# Public proxy (no auth required)
https://eterra.ancpi.ro/eterra/proxy/parcel   → 200 OK

# Authenticated API (requires login)  
https://eterra.ancpi.ro/api/proxy            → 401 Unauthorized
```

### API Endpoints Discovered
| Service | Endpoint | Status |
|---------|----------|--------|
| ETERRA Parcel | `/eterra/proxy/parcel` | ✅ Public |
| ETERRA Imobile | `/eterra/proxy/imobile` | ✅ Public |
| ETERRA Geometry | `/eterra/proxy/geometry` | ✅ Public |
| Intravilan | `/eterra/proxy/intravilan` | ✅ Public |
| GEOPORTAL | `/arcgis/rest/services/` | ✅ Public |

## 📚 Documentation
- [Plugin Specification](qgis-plugin/ro_ancpi_plugin/PLUGIN_SPEC.md)
- [Plugin README](qgis-plugin/ro_ancpi_plugin/README.md)

## 🤝 Contributing
Pull requests welcome! See [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) for research findings.

## 📄 License
See [LICENSE](LICENSE) file.