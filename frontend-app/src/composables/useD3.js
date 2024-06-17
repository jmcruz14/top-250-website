import * as d3 from 'd3';
import { isNumber, chain } from 'lodash'

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
   * @param {number} [elWidth=900] - The width of the SVG element.
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

  return {
    createBarChart
  }
}

export default useD3;