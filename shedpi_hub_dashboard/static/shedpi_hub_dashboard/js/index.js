
const contents = document.getElementsByClassName("contents");
let section = contents[0]

const url = section.getAttribute("data-json-feed")
const myRequest = new Request(url);

let drawTable = function (data) {
  let table = document.createElement("table");

  // Table Header
  let headerRow = document.createElement("tr");

  for(let heading in data.headings) {

    let headerItem = document.createElement("th");
    headerItem.textContent = data.headings[heading]
    headerRow.append(headerItem);
  }

  table.append(headerRow);

  // Table Contents
  for(let row in data.readings) {
    let contentRow = document.createElement("tr");
    for(let reading in data.readings[row]) {
      let contentItem = document.createElement("td");
      contentItem.textContent = data.readings[row][reading]
      contentRow.append(contentItem);
    }
    table.append(contentRow);
  }

  // Add the table to the page
  section.append(table);
}


response = fetch(myRequest)
  .then((response) => {
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    return response.json();
  })
  .then((response) => {
    drawTable(response)
  });