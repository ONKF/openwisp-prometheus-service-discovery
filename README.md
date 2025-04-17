openwisp-prometheus-service-discovery
=====================================

middleware to integrate `OpenWISP` into `prometheus` via `service-discovery`

---

**DISCLAIMER**: WORK IN PROGRESS

---

quick start
-----------

```sh
git clone https://github.com/ONKF/openwisp-prometheus-service-discovery
cd openwisp-prometheus-service-discovery
docker build -t openwisp-prometheus-service-discovery:latest .
docker run -p 8080:8080 -it penwisp-prometheus-service-discovery:latest
curl -v http://127.0.0.1:8080?url=<openwisp_url>&token=<api_token>
```