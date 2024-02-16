const contents = document.getElementsByClassName("contents")[0];
let section = contents

let deviceModuleEndpoint = ""

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

  // const url = section.getAttribute("data-json-feed")
  const url = "http://localhost:8000//api/v1/device-module-readings/"
  const endpoint = new URL(url);
  endpoint.searchParams.append("device_module", deviceModuleId);

  // FIXME: Need data output and need headings from Schema

  // const urlDeviceModuleReading =
  let endpointDeviceModuleReading = new Request(endpoint);

  response = fetch(endpointDeviceModuleReading)
    .then((response) => {
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      return response.json();
    })
    .then((response) => {
      drawTable(response, deviceModuleId)
    });
}


let drawTable = function (dataset, deviceModuleId) {
  // First empty the table container
  tableContainer.textContent = ""

  let table = document.createElement("table");

  // Table Header
  let headerRow = document.createElement("tr");

  // TODO: Build the header rows from the schema, or build a full list in th
  // Could use the schema, what about historic data that may violate it,
  // Built as a ist because the pagination would hammer the device modiule
  const headingFields = dataset[0];

  // TODO: Build the header rows from the schema, or build a full list in the backend and supply in the response
  // Could use the schema, what about historic data that may violate it,
  // Built as a ist because the pagination would hammer the device modiule

  schema = deviceModuleSchemaMap[deviceModuleId]

  let dataFields = []
  if (schema) {
    extra_fields = Object.keys(schema.properties)
    dataFields = [...dataFields, ...extra_fields];
    dataFields = [...new Set(dataFields)]
  }

  // FIXME: Need human readable headings, probably needs to come from the BE to be
  for (let heading in headingFields) {

    if (heading == "data") {

      for (let headingIndex in dataFields) {
        const heading = dataFields[headingIndex]
        let headerItem = document.createElement("th");
        headerItem.textContent = heading
        headerRow.append(headerItem);
      }
    } else {
      let headerItem = document.createElement("th");
      headerItem.textContent = heading
      headerRow.append(headerItem);
    }
  }

  table.append(headerRow);

  // Table Contents
  for (let rowIndex in dataset) {
    const row = dataset[rowIndex]
    let contentRow = document.createElement("tr");
    for (let reading in row) {
      const fieldValue = row[reading]
      if (typeof fieldValue == "object") {
        for (let dataFieldIndex in dataFields) {
          let contentItem = document.createElement("td");
          const dataField = dataFields[dataFieldIndex]

          // FIXME: Need to change the null value in the project to be an empty object
          let mydict = {}
          if (fieldValue != null) {
            if (fieldValue.hasOwnProperty(dataField)) {
              contentItem.textContent = fieldValue[dataField]
            }
          }

          contentRow.append(contentItem);
        }
      } else {
        let contentItem = document.createElement("td");
        contentItem.textContent = row[reading]
        contentRow.append(contentItem);
      }
    }
    table.append(contentRow);
  }

  // Add the table to the page
  tableContainer.append(table);
}
