# GeoScript QGIS Plugin Specification

## Plugin: ro_ancpi_plugin
**QGIS Plugin for Romanian Cadastral Data Access**

### Features
1. **Parcel Download (g6)** - Download cadastral parcel geometries from ETERRA 3
2. **Orthophoto (o5)** - Download orthophotoplans from GEOPORTAL
3. **Topo Maps (i5)** - Download topographic maps
4. **Admin Boundaries (u5)** - Download administrative boundaries
5. **Intravilan Limits (u6)** - Download urban area boundaries
6. **Overlap Check (v6)** - Verify property overlaps
7. **Request Status (ipk)** - Check cadastral request status
8. **Update Check (gupdate)** - Check for plugin updates

### API Endpoints
```python
ETERRA_PROXY = "https://eterra.ancpi.ro/eterra/proxy"
GEOPORTAL_BASE = "https://geoportal.ancpi.ro"
ARCGIS_SERVICES = f"{GEOPORTAL_BASE}/arcgis/rest/services"
```

### UI Design
User-friendly dockable panel with:
- Tabbed interface for each function
- Search by county/locality/parcel number
- Interactive map selection
- Progress indicators
- Results preview

### Authentication
Uses anonymous proxy access (no login required for basic data)