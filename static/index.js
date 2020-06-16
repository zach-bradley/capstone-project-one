let $calories =  parseInt($('#total_calories').attr("data-amount"))
let $carbs = parseInt($('#carbs').attr("data-amount"))
let $fat = parseInt($('#fat').attr("data-amount"))
let $protein = parseInt($('#fat').attr("data-amount"))

let total = $carbs + $fat + $protein;
let list = [$carbs, $fat, $protein]

let makePie = function(){
  let $div = $("#pie");
  const width = $div[0]['offsetWidth'];
  const height = $div[0]["offsetHeight"];
  let margin;
  if(width < 400){
    margin = 0
  }
  else {
    margin = 40
  }
  console.log(width, height)
  const radius = Math.min(width, height) / 2 - margin;

  let svg = d3.select('#pie')
    .append("svg")
      .attr("width", width)
      .attr("height", height)    
      .attr("preserveAspectRatio", "xMinYMin meet")
      .attr("viewBox", `0 0 ${width} ${height}`)
      .attr("class", "chart")
    .append("g")
      .attr("transform", "translate(" + width / 2 + "," +height / 2 + ")");

  let data = {
    "fat" : $fat,
    "carbs" : $carbs,
    "protein" : $protein
  }

  let color = d3.scaleOrdinal()
    .domain(data)
    .range(["#fffc2e", "#2e3fff", "#ff2934"])

  let pie = d3.pie()
    .value(d => d.value)

  let data_ready = pie(d3.entries(data))

  svg
    .selectAll('chart')
    .data(data_ready)
    .enter()
    .append('path')
    .attr('d', d3.arc()
      .innerRadius(50)        
      .outerRadius(radius)
    )
    .attr('fill', d => color(d.data.key))
    .attr("stroke", "black")
    .style("stroke-width", "2px")
    .style("opacity", 0.7)


  let arc = d3.arc()
    .innerRadius(radius * 0.6)       
    .outerRadius(radius * 0.8)

  let outerArc = d3.arc()
    .innerRadius(radius * 1.2)
    .outerRadius(radius * 1.2)

    svg
    .selectAll('allPolylines')
    .data(data_ready)
    .enter()
    .append('polyline')
      .attr("stroke", "black")
      .style("fill", "none")
      .attr("stroke-width", 1)
      .attr('points', function(d) {
        var posA = arc.centroid(d) 
        var posB = outerArc.centroid(d) 
        var posC = outerArc.centroid(d); 
        var midangle = d.startAngle + (d.endAngle - d.startAngle) / 2 
        posC[0] = radius * 1.1 * (midangle < Math.PI ? 1 : -1); 
        return [posA, posB, posC]
      })

  // Add the polylines between chart and labels:
  svg
    .selectAll('allLabels')
    .data(data_ready)
    .enter()
    .append('text')
      .text( d =>  d.data.key + ": " + d.data.value +"g" )
      .attr('transform', function(d) {
          var pos = outerArc.centroid(d);
          var midangle = d.startAngle + (d.endAngle - d.startAngle) / 2
          pos[0] = radius * 1.2 * (midangle < Math.PI ? 1 : -1);
          return 'translate(' + pos + ')';
      })
      .style('text-anchor', function(d) {
          var midangle = d.startAngle + (d.endAngle - d.startAngle) / 2
          return (midangle < Math.PI ? 'start' : 'end')
      })

  svg.append('text')
      .attr("text-anchor", "middle")
      .text(total +"g total") 
}

$(document).ready(makePie);