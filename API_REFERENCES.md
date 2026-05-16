# ANCPI API References

Structured API endpoints for Romanian cadastral data, discovered through reverse engineering of ETERRA 3 and GEOPORTAL.

## Base URLs

| Environment | URL | Auth Required |
|-------------|-----|---------------|
| Production | `https://eterra.ancpi.ro` | ❌ For public endpoints |
| GEOPORTAL | `https://geoportal.ancpi.ro` | ❌ For map services |
| ArcGIS REST | `https://geoportal.ancpi.ro/arcgis/rest/services` | ❌ Public read |

## Public Anonymous Endpoints

These endpoints work **without authentication**:

### ETERRA 3 Proxy Endpoints

```
POST https://eterra.ancpi.ro/eterra/proxy/parcel
```

Request body:
```json
{
  "judet": "B",      // County code (B=Bucuresti, C=Cluj, etc.)
  "localitate": "123456",  // Locality SIRUTA code
  "nr": "123"        // Parcel number
}
```

---

```
POST https://eterra.ancpi.ro/eterra/proxy/imobile
```

Request body:
```json
{
  "judet": "B",
  "localitate": "123456",
  "nr": "123"
}
```

---

```
POST https://eterra.ancpi.ro/eterra/proxy/geometry
```

Returns geometry data in GML format.

Request body:
```json
{
  "judet": "B",
  "localitate": "123456",
  "geom": "POLYGON(...)"
}
```

---

```
POST https://eterra.ancpi.ro/eterra/proxy/intravilan
```

Request body:
```json
{
  "judet": "B"  // County code
}
```

---

### GEOPORTAL WFS Services

```
GET https://geoportal.ancpi.ro/arcgis/rest/services/
```

Available services:
- Orthophoto 2015-2024
- Topographic maps (1:5000, 1:10000, 1:25000)
- Administrative boundaries
- Hydrographic network
- Transportation network

Example for map tiles:
```
GET https://geoportal.ancpi.ro/arcgis/rest/services/ORTO_2020/MapServer/tile/{level}/{row}/{col}
```

## Authenticated Endpoints

Requires ANCPI account login. These return 401 without valid session.

```
POST https://eterra.ancpi.ro/api/proxy/parcel
POST https://eterra.ancpi.ro/api/proxy/imobile
GET  https://eterra.ancpi.ro/api/user/info
```

Session cookie: `ASP.NET_SessionId` (from login)

## Quick Integration Snippets

### Python (requests)

```python
import requests

def get_parcel(judet, localitate, nr):
    url = "https://eterra.ancpi.ro/eterra/proxy/parcel"
    payload = {
        "judet": judet[:2].upper() if len(judet) > 2 else judet,
        "localitate": localitate,
        "nr": nr
    }
    response = requests.post(url, json=payload, timeout=30)
    return response.content if response.status_code == 200 else None
```

### cURL

```bash
curl -X POST https://eterra.ancpi.ro/eterra/proxy/parcel \
  -H "Content-Type: application/json" \
  -d '{"judet":"B","localitate":"6001","nr":"123"}'
```

### JavaScript (fetch)

```javascript
async function getParcel(judet, localitate, nr) {
  const response = await fetch('https://eterra.ancpi.ro/eterra/proxy/parcel', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({judet, localitate, nr})
  });
  return response.ok ? response.arrayBuffer() : null;
}
```

## County Codes Reference

| Code | County |
|------|--------|
| B | Bucuresti |
| C | Cluj |
| CT | Constanta |
| DJ | Dolj |
| G | Giurgiu |
| GL | Galati |
| HD | Hunedoara |
| HR | Harghita |
| IF | Ilfov |
| IS | Ialomita |
| MH | Mehedinti |
| MM | Maramures |
| MS | Musat |
| NT | Neamt |
| PH | Prahova |
| SB | Sibiu |
| SJ | Salaj |
| TM | Timis |
| TL | Tulcea |
| TR | Teleorman |
| VL | Valcea |
| VN | Vrancea |

## Rate Limits

- Anonymous proxies: ~30 requests/minute recommended
- Excessive requests may trigger temporary IP throttling
- No official rate limit documentation (reverse engineered)

## Notes

- All coordinates are in EPSG:3857 (Web Mercator) or EPSG:4326 (WGS84)
- Data formats: GML, GeoJSON, Shapefile (depending on endpoint)
- Last verified: May 2026