import * as d3 from 'd3';
import { isNumber, chain, merge } from 'lodash'

export const useD3 = () => {
  /**
   * Creates a bar chart using D3.js.
   * 
   * @async
   * @function createBarChart
   * @param {Object[]} data - The data to be used for the bar chart.
   * @param {string} sortKey - The key by which the data should be sorted.
   * @param {string} xLabel - The key for the x-axis labels.
   * @param {string} barColor - The color of the bars.
   * @param {string} xAxisTitle - The title for the x-axis.
   * @param {boolean} [removeDomain=true] - Whether to remove the domain line from the y-axis.
   * @param {number} [svgWidth=900] - The width of the SVG element.
   * @param {number} [elHeight=500] - The height of the SVG element.
   * @param {number} [marginTop=30] - The top margin for the chart.
   * @param {number} [marginRight=0] - The right margin for the chart.
   * @param {number} [marginBottom=30] - The bottom margin for the chart.
   * @param {number} [marginLeft=40] - The left margin for the chart.
   * @param {number} [chartWidth=900] - The width of the chart area.
   * @param {number} [chartHeight=450] - The height of the chart area.
   * @returns {Promise<SVGSVGElement>} - A promise that resolves to the SVG element representing the bar chart.
   * 
   * @example
   * const data = [
   *   { name: "A", value: 30 },
   *   { name: "B", value: 80 },
   *   { name: "C", value: 45 }
   * ];
   * const chart = await createBarChart(data, 'value', 'name', '#69b3a2', 'Names', true);
   * document.body.append(chart);
   */
  async function createBarChart (
    data, sortKey, xLabel, 
    barColor = '#f1f5f9', xAxisTitle, chartTitle,
    removeDomain = true,
    elWidth = 900, elHeight = 500,
    marginTop = 30, marginRight = 0, marginBottom = 30, marginLeft = 40,
    chartWidth = 900, chartHeight = 450,
  ) {

      const svg = d3.create('svg')
        .attr("width", elWidth)
        .attr("height", elHeight)
        .attr("viewBox", [0, 0, elWidth, elHeight])
        .attr("style", "max-width: 100%; height: auto;");

      // Create a tooltip element
      const tooltip = d3.select("body").append("div")
        .attr("class", "tooltip")
        .attr("class", "bg-slate-600")
        .style("position", "absolute")
        .style("color", "white")
        .style("border", "1px solid #ccc")
        .style("padding", "10px")
        .style("cursor", "pointer")
      
      // Generate x-scale
      const x = d3.scaleBand()
        .domain(d3.groupSort(data, ([d]) => -d[sortKey], (d) => d[xLabel]))
        // .range([0, chartWidth])
        .range([marginLeft, chartWidth - marginRight])
        .padding(0.1)

      // Generate y-scale
      const y = d3.scaleLinear()
        .domain([0, d3.max(data, d => d[sortKey])])
        .range([chartHeight - marginBottom, marginTop])

      // Add rectangles
      svg.append("g")
        .attr("fill", function (d) { return barColor })
          .selectAll()
          .data(data)
            .join("rect")
            .attr("x", d => x(d[xLabel]))
            .attr("y", d => y(d[sortKey]))
            .attr("height", d=> y(0) - y(d[sortKey]))
            .attr("width", x.bandwidth())
            .on("mouseover", (event, d) => {
              tooltip
                .style("display", "block")
                .html(`
                  <div class="flex flex-col">
                    <div class="flex gap-1">
                      <span class="font-proportional text-sm">Rank:</span>
                      <span class="font-tabular font-bold text-sm">${d['rank'] ? d['rank'] : null}</span>
                    </div>
                    <div class="flex gap-1">
                      <span class="font-proportional text-sm">Count:</span>
                      <span class="font-tabular font-bold text-sm">${d[sortKey] ? d[sortKey] : null}</span>
                    </div>
                    <div class="flex gap-1">
                      <span class="font-proportional text-sm">Rating:</span>
                      <span class="font-tabular font-bold text-sm">${d?.rating ? d['rating'] : null}</span>
                    </div>
                    <div class="flex gap-1">
                      <span class="font-proportional text-sm">Classic Rating:</span>
                      <span class="font-tabular font-bold text-sm">${d?.classic_rating ? d['classic_rating'] : null}</span>
                    </div>
                  </div>
                `);
              
              event.target.style.stroke = "black"
              event.target.style["stroke-width"] = 1.75
            })
            .on("mousemove", event => {
              tooltip.style("left", (event.pageX + 10) + "px")
                .style("top", (event.pageY - 5) + "px");
            })
            .on("mouseout", (event) => {
              tooltip.style("display", "none");
              event.target.style.stroke = "none"
            });
      
      // Add x-axis
      svg.append("g")
        .attr("transform", `translate(0,${chartHeight - marginBottom})`)
        .call(d3.axisBottom(x).tickSizeOuter(0))
          .append("text")
            .attr("x", 900 / 2)
            .attr("y", 40)
            .attr("class", 'font-tabular')
            .attr("font-size", "12px")
            .attr("fill", "currentColor")
            .attr("text-anchor", "middle")
            .text(xAxisTitle);
      
      // Add y-axis
      svg.append("g")
        .attr("transform", `translate(${marginLeft},0)`)
        .call(d3.axisLeft(y).tickFormat((y) => (y).toFixed()))
        .call(g => {
          if (removeDomain) g.select(".domain").remove()
        })
        .call(g => g.append("text")
            .attr("x", 0)
            .attr("y", 15)
            .attr("class", "font-proportional")
            .attr("font-size", '18px')
            .attr("fill", "currentColor")
            .attr("text-anchor", "start")
            .text(chartTitle));
      
      return svg.node();
    }

  async function createScatterPlot (
    data, xKey, yKey, 
    pointColor = '#f1f5f9', xAxisTitle, chartTitle,
    removeDomain = true,
    elWidth = 900, elHeight = 500,
    marginTop = 30, marginRight = 0, marginBottom = 30, marginLeft = 40,
    chartWidth = 1000, chartHeight = 450,
  ) {
    const svg = d3.create('svg')
        .attr("width", elWidth)
        .attr("height", elHeight)
        .attr("viewBox", [0, 0, elWidth, elHeight])
        .attr("style", "max-width: 100%; height: auto;");
    
    // Generate x-scale
    const x = d3.scaleLinear()
      .domain([0, d3.max(data, (d) => d[xKey])])
      .range([marginLeft, chartWidth - marginRight])

    // Generate y-scale
    const y = d3.scaleLinear()
      .domain([0, d3.max(data, d => d[yKey])])
      .range([chartHeight - marginBottom, marginTop])

    // Add dots
    svg.append('g')
    .selectAll("dot")
    .data(data)
    .enter()
    .append("circle")
      .attr("cx", function (d) { return x(d[xKey]); } )
      .attr("cy", function (d) { return y(d[yKey]); } )
      .attr("r", 1.5)
      .style("fill", pointColor)
    
     // Add x-axis
     svg.append("g")
     .attr("transform", `translate(0,${chartHeight - marginBottom})`)
     .call(d3.axisBottom(x).tickSizeOuter(0))
       .append("text")
         .attr("x", 900 / 2)
         .attr("y", 40)
         .attr("class", 'font-tabular')
         .attr("font-size", "12px")
         .attr("fill", "currentColor")
         .attr("text-anchor", "middle")
         .text(xAxisTitle);
   
   // Add y-axis
   svg.append("g")
     .attr("transform", `translate(${marginLeft},0)`)
     .call(d3.axisLeft(y).tickFormat((y) => (y).toFixed()))
     .call(g => {
       if (removeDomain) g.select(".domain").remove()
     })
     .call(g => g.append("text")
         .attr("x", 0)
         .attr("y", 15)
         .attr("class", "font-proportional")
         .attr("font-size", '18px')
         .attr("fill", "currentColor")
         .attr("text-anchor", "start")
         .text(chartTitle));
    
    return svg.node()
  }

  async function createHistogram (
    data, xBin, yKey, 
    barColor = '#f1f5f9', xAxisTitle, chartTitle,
    removeDomain = true,
    svgWidth = 900, svgHeight = 500,
    marginTop = 30, marginRight = 0, marginBottom = 30, marginLeft = 40,
    chartWidth = 1000, chartHeight = 450,
  ) {
    const margin = {
      top: marginTop,
      right: marginRight,
      left: marginLeft,
      bottom: marginBottom
    };
    const width = svgWidth - (margin.left + margin.right);
    const height = svgHeight - (margin.top + margin.bottom );

    const svg = d3.create('svg')
      .attr("width", svgWidth)
      .attr("height", svgHeight)
      .attr("viewBox", [0, 0, chartWidth, chartHeight])
      .attr("style", "max-width: 100%; height: auto;")

    // x-axis
    const x = d3.scaleLinear()
      .domain([60, d3.max(data, (d) => d[xBin]?.upper ? d[xBin]?.upper : d[xBin]?.lower )])
      .range([margin.left, width - margin.right]);

    const xAxis = d3.axisBottom(x)
      .tickValues(data.map(d => d[xBin].lower))
      .tickFormat((d, i) => i === xTickValues.length - 1 ? "infinity" : data[i]?._id);
      
    const xAxisGroup = svg.append("g")
      .attr("transform", `translate(0,${chartHeight - 25})`)
      .call(d3.axisBottom(x)
          .tickSizeOuter(0)
          .tickFormat( function (d) { return ( d === 180 ) ? '180+' : d})
        )
      .append("text")
         .attr("x", 900 / 2)
         .attr("y", 40)
         .attr("class", 'font-tabular')
         .attr("font-size", "12px")
         .attr("fill", "currentColor")
         .attr("text-anchor", "middle")
         .text(xAxisTitle);
    
    xAxisGroup.selectAll('.tick line')
      .filter((d, i, nodes) => i === nodes.length - 1) // Select the last tick line
      .attr("x2", 100); // Extend the last tick line to the right by 10 units (adjust as needed)

    // bins
    const bins = d3.bin()
      .thresholds(data?.length)
      .value((d) => d[xBin]?.lower) // just selects how to split data based on values 
    const histogram = bins(data).map(bin => {
      const flattenedBin = {
        x0: bin.x0,
        x1: bin.x1,
      };
      if (bin.length > 0) {
        Object.assign(flattenedBin, bin[0])
      } else {
        Object.assign(flattenedBin, {
          count: 0,
          _id: `${flattenedBin.x0}-${flattenedBin.x1}`
        })
      }
      return flattenedBin
    })
    
    // y-axis
    const y = d3.scaleLinear()
      .domain([0, d3.max(histogram, d => d.count)])
      .range([height - margin.bottom, margin.top])

    svg.append("g")
      .attr("transform", `translate(${margin.left},0)`)
      .call(d3.axisLeft(y))
      .call(g => {
        if (removeDomain) g.select(".domain").remove()
        // g.append("text")
        //   .attr("y", height / 2)
        //   .attr("x", -marginLeft - 5)
        //   .attr("class", "font-tabular")
        //   .attr("font-size", '18px')
        //   .attr("fill", "currentColor")
        //   .attr("text-anchor", "start")
        //   .attr("transform", `rotate(${marginLeft},${height/4},180)`)
        //   .text("Count")
      })
      .call(g => g.append("text")
          .attr("x", 0)
          .attr("y", -2.5)
          .attr("class", "font-proportional")
          .attr("font-size", '24px')
          .attr("fill", "currentColor")
          .attr("text-anchor", "start")
          .text(chartTitle));
    
    // append all rectangles to svg element
    svg.selectAll("rect")
      .data(histogram)
      .enter()
      .append("rect")
      .attr("x", d => x(d.x0))
      .attr("y", d => y(d.count))
      .attr("width", d => x(d.x1) - x(d.x0) - 1)
      .attr("height", d => height - margin.bottom - y(d.count))
      .style("fill", barColor);
    
    return svg.node()
    // create histogram here
  }

  return {
    createBarChart,
    createScatterPlot,
    createHistogram,
  }
}

export default useD3;