import {getSchemaDataFields} from "./utils.js";

/* Chart visual */

class LineChart {
  constructor() {
    this.container = document.getElementById("chartContainer");
  }

  mapDataSet(dataset, schema) {
    let data = []
    const dataFields = getSchemaDataFields(schema)

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

  draw(dataset, schema) {
    this.destroy()

    let data = this.mapDataSet(dataset, schema);

    // Declare the chart dimensions and margins.
    const width = this.container.clientWidth;
    const height = this.container.clientHeight;
    const marginTop = 20;
    const marginRight = 30;
    const marginBottom = 30;
    const marginLeft = 40;

    // Declare the x (horizontal position) scale.
    const x = d3.scaleUtc(d3.extent(data, d => d.date), [marginLeft, width - marginRight]);

    // Declare the y (vertical position) scale.
    //    + converts a string to a number
    const y = d3.scaleLinear(d3.extent(data, d => +d.value), [height - marginBottom, marginTop]);

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

      // y-axis label
      .call(g => g.append("text")
        .attr("x", -marginLeft)
        .attr("y", 100)
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
    d3.select("svg").selectAll('*').remove()

    this.container.replaceChildren();
  }
}

export {LineChart};
