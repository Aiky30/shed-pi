import {LineChart} from "./modules/chart.js";

let chart = new LineChart()

// TODO: DB Entry that controls this config, the page will then spit them out onto the page via backend,
//      we then loop through each class with config embedded
const widgetConfig = {
  // "type": "",
  "deviceModuleId": "a62408c2-bc89-48e2-8c23-9494bbf33cb7",
  "startDate": "2024-01-25",
  "endDate": "2024-02-24",
}


class Widget {
  constructor(config) {
    this.container = document.getElementById("chartContainer");
    this.config = widgetConfig
  }

  async getDeviceData() {
    let data;
    const urlDeviceModule = "/api/v1/device-module/" + this.config.deviceModuleId
    let endpointDeviceModule = new Request(urlDeviceModule);

    await fetch(endpointDeviceModule)
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        return response.json();
      })
      .then((response) => {
        data = response

        return response
      });
    return data
  }

  async getDeviceReadings() {
    let data;

    // const url = section.getAttribute("data-json-feed")
    const url = window.location.origin + "/api/v1/device-module-readings/"
    const endpoint = new URL(url);
    endpoint.searchParams.append("device_module", this.config.deviceModuleId);
    endpoint.searchParams.append("format", "json");
    endpoint.searchParams.append("start", this.config.startDate);
    endpoint.searchParams.append("end", this.config.endDate);

    let endpointDeviceModuleReading = new Request(endpoint);

    await fetch(endpointDeviceModuleReading)
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        return response.json();
      })
      .then((response) => {
        data = response

        return response
      });
    return data
  }

  async render() {
    const deviceData = await this.getDeviceData()
    const deviceReadings = await this.getDeviceReadings()

    chart.draw(deviceReadings, deviceData.schema)
  }
}

const widget = new Widget(widgetConfig)
widget.render()
