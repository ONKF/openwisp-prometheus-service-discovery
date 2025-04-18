openwisp-prometheus-service-discovery
=====================================

This service talks to an OpenWISP instance and returns the inventory so it can be consumed by prometheus via http service discovery.

background
----------

This service is based of the need to use OpenWISP for accesspoint management but simultaneously reuse exisiting prometheus monitoring infrastructure.

It uses the OpenWISP API to get the inventory (including organization and location data) and exposes it in a format suiteable for `prometheus service discovery`.

assumptions
-----------

* there is a `prometheus-node-exporter-lua` listening on `9100/tcp` on every device
* prometheus is able to route into the `management` network of the devices (is able to use communicate to the `Management IP`)

locations
----------

We want to use the location data provied by OpenWISP.
Therefore the service queries the location of every device and adds the following labels (if available)

* `__meta_location`
* `__meta_latitude`
* `__meta_longitude`

quick start
-----------

```sh
git clone https://github.com/ONKF/openwisp-prometheus-service-discovery
cd openwisp-prometheus-service-discovery
docker compose up
```

The service will be available on `8080/tcp`. Visit it in your browser to get a prometheus configuration snippet and live execute queries.

development environment
-----------------------

```sh
git clone https://github.com/ONKF/openwisp-prometheus-service-discovery
cd openwisp-prometheus-service-discovery
python3 -m venv environment/
pip3 install -r environment.txt
./main.py
```