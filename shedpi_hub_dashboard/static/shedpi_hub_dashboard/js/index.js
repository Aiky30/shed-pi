const contents = document.getElementsByClassName("contents")[0];
let section = contents

let deviceModuleEndpoint = ""

// Global store for the device modules, with schema
let storeDeviceModules = []
let deviceModuleSchemaMap = {}

/* Shared utils */
function getSchemaDataFields(deviceModuleId) {
  schema = deviceModuleSchemaMap[deviceModuleId]
  let dataFields = []
  if (schema) {
    extra_fields = Object.keys(schema.properties)
    dataFields = [...dataFields, ...extra_fields];
    dataFields = [...new Set(dataFields)]
  }
  return dataFields
}

/* Chart visual */

class LineChart {
  constructor() {
    this.container = document.getElementById("chartContainer");
  }

  mapDataSet(dataset, deviceModuleId) {
    let data = []
    const dataFields = getSchemaDataFields(deviceModuleId)

    for (let rowIndex in dataset) {
      const row = dataset[rowIndex]

      let chartRow = {}

      for (let rowHeading in row) {
        const fieldValue = row[rowHeading]

        if (typeof fieldValue == "object") {
          for (let dataFieldIndex in dataFields) {
            const dataField = dataFields[dataFieldIndex]

            if (fieldValue != null) {
              if (fieldValue.hasOwnProperty(dataField)) {
                // FIXME: Should be rowHeading
                chartRow["value"] = fieldValue[dataField]
              }
            }

          }
        } else if (rowHeading == "created_at") {
          // Created at date column
          chartRow["date"] = new Date(fieldValue)
        }
      }

      data.push(chartRow)
    }

    return data
  }

  draw(dataset, deviceModuleId) {
    this.destroy()

    let data = this.mapDataSet(dataset, deviceModuleId);

    // Declare the chart dimensions and margins.
    const width = 928;
    const height = 500;
    const marginTop = 20;
    const marginRight = 30;
    const marginBottom = 30;
    const marginLeft = 40;

    // Declare the x (horizontal position) scale.
    const x = d3.scaleUtc(d3.extent(data, d => d.date), [marginLeft, width - marginRight]);

    // Declare the y (vertical position) scale.
    const y = d3.scaleLinear([0, d3.max(data, d => d.value)], [height - marginBottom, marginTop]);

    // Declare the line generator.
    const line = d3.line()
      .x(d => x(d.date))
      .y(d => y(d.value));

    // Create the SVG container.
    const svg = d3.create("svg")
      .attr("width", width)
      .attr("height", height)
      .attr("viewBox", [0, 0, width, height])
      .attr("style", "max-width: 100%; height: auto; height: intrinsic;");

    // Add the x-axis.
    svg.append("g")
      .attr("transform", `translate(0,${height - marginBottom})`)
      .call(d3.axisBottom(x).ticks(width / 80).tickSizeOuter(0));

    // Add the y-axis, remove the domain line, add grid lines and a label.
    svg.append("g")
      .attr("transform", `translate(${marginLeft},0)`)
      .call(d3.axisLeft(y).ticks(height / 40))
      .call(g => g.select(".domain").remove())
      .call(g => g.selectAll(".tick line").clone()
        .attr("x2", width - marginLeft - marginRight)
        .attr("stroke-opacity", 0.1))
      .call(g => g.append("text")
        .attr("x", -marginLeft)
        .attr("y", 10)
        .attr("fill", "currentColor")
        .attr("text-anchor", "start")
        .text("↑ Value"));

    // Append a path for the line.
    svg.append("path")
      .attr("fill", "none")
      .attr("stroke", "steelblue")
      .attr("stroke-width", 1.5)
      .attr("d", line(data));

    let container = document.getElementById("chartContainer");
    // Append the SVG element.
    this.container.append(svg.node());

  }

  destroy() {
    this.container.replaceChildren();
  }
}

let chart = new LineChart()


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
    drawDropdown();
    bindFormSubmision();
    // Build schema map

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


/* Table visual */

// TOOD: Get a line chart working: https://visjs.github.io/vis-timeline/docs/graph2d/

// Create table container
const tableContainer = document.createElement("div");
section.append(tableContainer);

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

  response = fetch(endpointDeviceModuleReading)
    .then((response) => {
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      return response.json();
    })
    .then((response) => {
      drawTable(response, deviceModuleId)

      chart.draw(response, deviceModuleId)
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
