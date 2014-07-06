# Texture

A layer of convention atop Fabric with a focus on maintaining Fabric's
functionality.

*The default tasks currently only support an **Ubuntu 14.04 LTS (Trusty Tahr)** instance(s).*

## Structure

- Tasks        - Standard Fabric tasks
- Roles        - Standard Fabric roles
- Strategies   - deployment methods
- Patches      - software installations, similar to cookbooks
- Applications - deployable applications

## Applications

    |-- /www/apps # or another base dir
    |   |-- example_app
    |   |   |-- releases
    |   |   |   |-- 1
    |   |   |   |-- 2
    |   |   |   |-- ...
    |   |   |-- shared
    |   |   |-- current

## Strategies

default strategies include copy (git and symlink to come soon)

## Patches

- apache2
- nginx
