const contents = document.getElementsByClassName("contents")[0];
let section = contents

let deviceModuleEndpoint = "/api/v1/device-module-readings/"

// Global store for the device modules, with schema
let storeDeviceModules = []
let deviceModuleSchemaMap = {}

/* Drop down selection */
// Create dropdown container
const deviceModuleSelectorContainer = document.createElement("div");
section.append(deviceModuleSelectorContainer);

const urlDeviceModule = "/api/v1/device-module/"
let endpointDeviceModule = new Request(urlDeviceModule);
response = fetch(endpointDeviceModule)
  .then((response) => {
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    return response.json();
  })
  .then((response) => {
    storeDeviceModules = response
    drawDropdown()

    // Build schema map

  });

let drawDropdown = function () {
  let data = storeDeviceModules
  let dropdown = document.createElement("select");

  // Table Header
  let emptySelector = document.createElement("option");
  emptySelector.textContent = "Please Select"
  dropdown.append(emptySelector)

  dropdown.addEventListener('change', function (e) {
    optionId = this.selectedOptions[0].id

    if (optionId) {
      loadTableData(optionId)
    }
  });

  for (let deviceModuleIndex in data) {
    const deviceModule = data[deviceModuleIndex]

    let optionElement = document.createElement("option");
    optionElement.textContent = deviceModule.device + " - " + deviceModule.name
    optionElement.id = deviceModule.id

    // Build schema map
    deviceModuleSchemaMap[deviceModule.id] = deviceModule.schema

    dropdown.append(optionElement);
  }

  // Add the drpdown to the page
  deviceModuleSelectorContainer.append(dropdown);
};

/* Table visual */

// Create table container
const tableContainer = document.createElement("div");
section.append(tableContainer);

let loadTableData = function (deviceModuleId) {

  // TODO: Get data based on deviceModuleId
  // Endpoint: http://127.0.0.1:8000/api/v1/device-module-readings/
  // device_module = deviceModuleId
  // FIXME: Build the query string using the js libraries
  const endpoint = deviceModuleEndpoint + "?device_module=" + deviceModuleId
  // FIXME: Pass a reversed full url through
  // const urlDeviceModuleReading = section.getAttribute("data-json-feed")
  let endpointDeviceModuleReading = new Request(endpoint);

  response = fetch(endpointDeviceModuleReading)
    .then((response) => {
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      return response.json();
    })
    .then((response) => {
      drawTable(response)
    });
}


let drawTable = function (data) {
  // First empty the table container
  tableContainer.textContent = ""

  let table = document.createElement("table");

  // Table Header
  let headerRow = document.createElement("tr");

  // TODO: Build the header rows from the data, for now use the first row.
  //  For other projects this was supplied in the endpoint
  // Could use the schema, what about historic data that may violate it,
  // we only validate this when historic data is updated
  // Built as a ist because the pagination would hammer the device modiule

  let deviceModules = storeDeviceModules


  console.log("Drawing table with data: ", data)

  for (let heading in data[0]) {

    let headerItem = document.createElement("th");
    headerItem.textContent = heading
    headerRow.append(headerItem);
  }

  table.append(headerRow);

  // Table Contents
  for (let row in data) {
    let contentRow = document.createElement("tr");
    for (let reading in data[row]) {
      let contentItem = document.createElement("td");
      contentItem.textContent = data[row][reading]
      contentRow.append(contentItem);
    }
    table.append(contentRow);
  }

  // Add the table to the page
  tableContainer.append(table);
}
