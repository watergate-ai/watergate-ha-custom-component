# Watergate Integration for Home Assistant

[![hacs][hacsbadge]](hacs)

## Description

The `watergate` component provides an integration with Watergate's local API service. It adds sensors for metrics like water flow, pressure, and valve state, and provides device actions such as opening/closing the valve and monitoring device telemetry.

Currently we are in the process of integrating this component in Home Assistan core. It will be available soon there.

> ⚠️ **Note:** Ensure that you have enabled a Local API in Watergatge mobile application.

> ⚠️ **Note:** Make sure your Home Assistant Local Network address is reachable from Sonic network.

## Installation

There are two ways this integration can be installed into [Home Assistant](https://www.home-assistant.io).

The easiest and recommended way is to install the integration using [HACS](https://hacs.xyz), which makes future updates easy to track and install.

1. Go to HACS ➤ Integrations ➤ Custom repositories ➤ Add custom repository in Home Assistant, and enter the URL of this GitHub repository.
2. Choose the Integration category for the component to appear under integrations.
3. Restart Home Assistant.
4. Add the integration to Home Assistant (see **Configuration**).

Alternatively, installation can be done manually by copying the files in this repository into the `custom_components` directory in the Home Assistant configuration directory:

1. Open the configuration directory of your Home Assistant installation.
2. If you do not have a `custom_components` directory, create it.
3. In the `custom_components` directory, create a new directory called `watergate`.
4. Copy all files from the `custom_components/watergate/` directory in this repository into the `watergate` directory.
5. Restart Home Assistant.
6. Add the integration to Home Assistant (see **Configuration**).

## Configuration

Configuration is done through the Home Assistant UI.

To add the integration, go to **Settings ➤ Devices & Services ➤ Integrations**, click **➕ Add Integration**, and search for "Watergate".

### Configuration Variables

**IP address**

- (string)(Required) Ip address of your device.


[hacs]: https://github.com/custom-components/hacs
[hacsbadge]: https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge
