const contents = document.getElementsByClassName("contents");
let section = contents[0]


/* Drop down selection */
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
    drawDropdown(response)
  });

let drawDropdown = function (data) {
  let dropdown = document.createElement("select");

  // Table Header
  let emptySelector = document.createElement("option");
  emptySelector.textContent = "Please Select"
  dropdown.append(emptySelector)

  for (let deviceModuleIndex in data) {
    const deviceModule = data[deviceModuleIndex]

    let optionElement = document.createElement("option");
    optionElement.textContent = deviceModule.device + " - " + deviceModule.name

    optionElement.addEventListener('select', function (e) {
      console.log("Draw data")
    });

    dropdown.append(optionElement);
  }

  // Add the drpdown to the page
  section.append(dropdown);
};

/* Table visual */

let loadTableData = function () {
  const urlDeviceModuleReading = section.getAttribute("data-json-feed")
  let endpointDeviceModuleReading = new Request(urlDeviceModuleReading);
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
  let table = document.createElement("table");

  // Table Header
  let headerRow = document.createElement("tr");

  for (let heading in data.headings) {

    let headerItem = document.createElement("th");
    headerItem.textContent = data.headings[heading]
    headerRow.append(headerItem);
  }

  table.append(headerRow);

  // Table Contents
  for (let row in data.readings) {
    let contentRow = document.createElement("tr");
    for (let reading in data.readings[row]) {
      let contentItem = document.createElement("td");
      contentItem.textContent = data.readings[row][reading]
      contentRow.append(contentItem);
    }
    table.append(contentRow);
  }

  // Add the table to the page
  section.append(table);
}


/* TODO - On select click, load the table with the reading data */
// Bind dropdown click
// reloadTable: destroy and rebuild
