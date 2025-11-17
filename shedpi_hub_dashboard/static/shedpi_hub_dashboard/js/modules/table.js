import {getSchemaDataFields} from "./utils.js";


/* Table visual */

class dataTable {
  constructor() {
    this.dataset = [];

    this.container = document.getElementById("tableContainer");
  }

  headerItem(heading) {
    let headerItem = document.createElement("th");
    headerItem.textContent = heading
    headerItem.setAttribute("scope", "col")
    return headerItem
  }

  drawHeader(table, schema) {
    let thead = document.createElement("thead");

    // Table Header
    let headerRow = document.createElement("tr");

    // TODO: Build the header rows from the schema, or build a full list in th
    // Could use the schema, what about historic data that may violate it,
    // Built as a ist because the pagination would hammer the device modiule
    const headingFields = this.dataset[0];

    // TODO: Build the header rows from the schema, or build a full list in the backend and supply in the response
    // Could use the schema, what about historic data that may violate it,
    // Built as a ist because the pagination would hammer the device modiule

    let dataFields = getSchemaDataFields(schema)

    // FIXME: Need human readable headings, probably needs to come from the BE to be
    for (let heading in headingFields) {

      if (heading == "data") {

        for (let headingIndex in dataFields) {
          const heading = dataFields[headingIndex]
          let headerItem = this.headerItem(heading)
          headerRow.append(headerItem);
        }
      } else {
        let headerItem = this.headerItem(heading)
        headerRow.append(headerItem);
      }
    }

    thead.append(headerRow);
    table.append(thead);

    return dataFields
  }

  drawBody(table, dataFields) {
    let tbody = document.createElement("tbody");

    for (let rowIndex in this.dataset) {
      const row = this.dataset[rowIndex]
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
      tbody.append(contentRow)
    }

    table.append(tbody);
  }


  draw(dataset, schema) {
    // FIXME: Destroy??
    // First empty the table container
    this.destroy()
    const table = this.create()

    this.dataset = dataset

    let dataFields = this.drawHeader(table, schema)
    this.drawBody(table, dataFields)

    this.container.append(table);
  }

  create() {
    this.container.classList.add('table-responsive');
    this.container.classList.add('small');

    let table = document.createElement("table");
    table.classList.add('table');
    table.classList.add('table-striped');
    table.classList.add('table-sm');

    return table
  }

  destroy() {
    this.container.textContent = ""
  }
}

export {dataTable};
