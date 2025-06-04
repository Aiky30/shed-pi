import {dataTable} from "./modules/table.js";
import {LineChart} from "./modules/chart.js";

/*
Design of the widgets:

Dashboard Controls
- Filter by day, week, month

All widgets
 - Select fields to map the data to
 - Type of widget

Temperature probe:
 - Average of the day
 - All entries for the day
*/

const contents = document.getElementsByClassName("contents")[0];
let section = contents

// Global store for the device modules, with schema
let storeDeviceModules = []
let deviceModuleSchemaMap = {}

let chart = new LineChart()
let table = new dataTable()

/* Drop down selection */
// Create dropdown container
const deviceModuleSelectorContainer = document.createElement("div");
section.append(deviceModuleSelectorContainer);

const urlDeviceModule = "/api/v1/device-module/"
let endpointDeviceModule = new Request(urlDeviceModule);
let response = fetch(endpointDeviceModule)
  .then((response) => {
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    return response.json();
  })
  .then((response) => {
    storeDeviceModules = response
    drawDropdown();
    bindFormSubmision();
  });

let drawDropdown = function () {
  let data = storeDeviceModules
  let dropdown = document.getElementById("form-dropdown");

  // Empty the dropdown items
  dropdown.innerHTML = '';

  let emptySelector = document.createElement("option");
  emptySelector.textContent = "Please Select"
  dropdown.append(emptySelector)

  for (let deviceModuleIndex in data) {
    const deviceModule = data[deviceModuleIndex]

    let optionElement = document.createElement("option");
    optionElement.textContent = deviceModule.device + " - " + deviceModule.name
    optionElement.id = deviceModule.id

    // Build schema map
    deviceModuleSchemaMap[deviceModule.id] = deviceModule.schema

    dropdown.append(optionElement);
  }
}

/* Form submission */

let bindFormSubmision = function () {
  let submitControl = document.getElementById("form-submit");
  let dropdown = document.getElementById("form-dropdown");

  submitControl.addEventListener('click', function (e) {
    e.preventDefault()

    // TODO: Run field validation

    let optionId = dropdown.selectedOptions[0].id

    // Start and end
    let startField = document.getElementById("startDate");
    let endField = document.getElementById("endDate");

    if (optionId) {
      loadTableData(optionId, startField.value, endField.value)
    }
  });
};


let loadTableData = function (deviceModuleId, startDate, endDate) {

  // const url = section.getAttribute("data-json-feed")
  const url = window.location.origin + "/api/v1/device-module-readings/"
  const endpoint = new URL(url);
  endpoint.searchParams.append("device_module", deviceModuleId);
  endpoint.searchParams.append("format", "json");
  endpoint.searchParams.append("start", startDate);
  endpoint.searchParams.append("end", endDate);

  // FIXME: Need data output and need headings from Schema

  // const urlDeviceModuleReading =
  let endpointDeviceModuleReading = new Request(endpoint);

  let response = fetch(endpointDeviceModuleReading)
    .then((response) => {
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      return response.json();
    })
    .then((response) => {
      const schema = deviceModuleSchemaMap[deviceModuleId]

      table.draw(response, schema)
      chart.draw(response, schema)
    });
}
