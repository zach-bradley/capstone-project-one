let $calories =  parseInt($('#total_calories').attr("data-amount"))
let $carbs = parseInt($('#carbs').attr("data-amount"))
let $fat = parseInt($('#fat').attr("data-amount"))
let $protein = parseInt($('#fat').attr("data-amount"))
let legendRectSize = 18;                                
let legendSpacing = 4; 

let total = $carbs + $fat + $protein;
let list = [$carbs, $fat, $protein]

let makePie = function(){
  let $div = $("#pie");
  const width = $div[0]['offsetWidth'];
  const height = $div[0]["offsetHeight"];
  let margin;
  if(width < 400){
    margin = 30
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
      .innerRadius(65)        
      .outerRadius(radius)
    )
    .attr('fill', d => color(d.data.key))
    .attr('data-legend', function(d) {return d.name})
    .attr("stroke", "black")
    .style("stroke-width", "2px")
    .style("opacity", 0.7)


  let arc = d3.arc()
    .innerRadius(radius * 1.5)       
    .outerRadius(radius * 0.5)

  let outerArc = d3.arc()
    .innerRadius(radius * 1.5)
    .outerRadius(radius * 0.8)
  
  let legend = svg.selectAll('.data-legend')
    .data(color.domain())
    .enter()                                               
          .append('g')                                           
          .attr('class', 'legend')                              
          .attr('transform', function(d, i) {                   
            var height = legendRectSize + legendSpacing;         
            var offset =  height * color.domain().length / 2;     
            var horz = -2 * legendRectSize;                      
            var vert = i * height - offset;                      
            return 'translate(' + horz + ',' + vert + ')';       
          });                                                    

        legend.append('rect')                                    
          .attr('width', legendRectSize)                          
          .attr('height', legendRectSize)                         
          .style('fill', color)                                   
          .style('stroke', color);                                
          
        legend.append('text')                                    
          .attr('x', legendRectSize + legendSpacing)              
          .attr('y', legendRectSize - legendSpacing)              
          .text(function(d) { return d; });               
}

$(document).ready(makePie);
$(window).on("resize", function(){
  $("svg").remove();
  makePie();
});