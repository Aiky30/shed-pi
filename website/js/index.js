
contents = document.getElementsByClassName("contents");


const myRequest = new Request("dummy_data.json");

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
  contents[0].append(table);
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