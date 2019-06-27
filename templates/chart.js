
document.addEventListener("DOMContentLoaded", function(event) {
    var gameData = {{gamelog|safe}}; 
    var data = parseDatas(gameData)
    drawChart(data['points'],d3.scaleOrdinal(d3.schemeCategory10),'Points')
    drawChart(data['asttov'],d3.scaleOrdinal(d3.schemeDark2),'Assists and Turnovers')
    drawChart(data['stlblk'],d3.scaleOrdinal(d3.schemeAccent),'Steals and Blocks')
    drawChart(data['pct'],d3.scaleOrdinal(d3.schemeSet1),'Field Goal Percentage')
    drawChart(data['reb'],d3.scaleOrdinal(d3.schemeSet3),'Rebounds')
    drawChart(data['fg3'],d3.scaleOrdinal(d3.schemeDark2),'3 Pointers')
    });

function parseDatas(gameData){
    var arr = [];

    var pts = [];
    pts['name'] = 'Points';
    pts['values'] = [];
    var reb = [];   
    reb['name'] = 'Rebounds';
    reb['values'] = [];
    var ast = [];   
    ast['name'] = 'Assists';
    ast['values'] = [];
    var fg3 = [];   
    fg3['name'] = '3 Pointers';
    fg3['values'] = [];
    var stl = [];   
    stl['name'] = 'Steals';
    stl['values'] = [];
    var blk = [];   
    blk['name'] = 'Blocks';
    blk['values'] = [];
    var tov = [];   
    tov['name'] = 'Turnovers';
    tov['values'] = [];
    var fg_pct = [];   
    fg_pct['name'] = 'Field Goal Percentage';
    fg_pct['values'] = [];
    var ft_pct = [];   
    ft_pct['name'] = 'Free Throw Percentage';
    ft_pct['values'] = [];
    
    var i;
    for (i = 0; i < gameData.length; i++){
        pts['values'].push({
            date: new Date(gameData[i].gamedate),
            value: gameData[i].pts
        });
        reb['values'].push({
            date: new Date(gameData[i].gamedate),
            value: gameData[i].reb
        });
        ast['values'].push({
            date: new Date(gameData[i].gamedate),
            value: gameData[i].ast
        });
        fg3['values'].push({
            date: new Date(gameData[i].gamedate),
            value: gameData[i].fg3m
        });
        stl['values'].push({
            date: new Date(gameData[i].gamedate),
            value: gameData[i].stl
        });
        blk['values'].push({
            date: new Date(gameData[i].gamedate),
            value: gameData[i].blk
        });
        tov['values'].push({
            date: new Date(gameData[i].gamedate),
            value: gameData[i].tov
        });
        fg_pct['values'].push({
            date: new Date(gameData[i].gamedate),
            value: gameData[i].fg_pct
        });
        ft_pct['values'].push({
            date: new Date(gameData[i].gamedate),
            value: gameData[i].ft_pct
        });

    }
    arr['points'] = [];
    arr['reb'] = [];
    arr['asttov'] = [];
    arr['stlblk']=[];
    arr['pct'] = [];
    arr['fg3'] = [];
    arr['points'].push(pts);
    arr['asttov'].push(ast);
    arr['reb'].push(reb);
    arr['fg3'].push(fg3);
    arr['stlblk'].push(blk);
    arr['stlblk'].push(stl);
    arr['asttov'].push(tov);
    arr['pct'].push(fg_pct);
    return arr;
}
function drawChart(data,colo,txt){
var width = 500;
  var height = 300;
  var margin = 50;
  var duration = 250;
  
  var lineOpacity = "0.7";
  var lineOpacityHover = "0.85";
  var otherLinesOpacityHover = "0.1";
  var lineStroke = "1px";
  var lineStrokeHover = "2px";
  
  var circleOpacity = '0.9';
  var circleOpacityOnLineHover = "0.25"
  var circleRadius = 3;
  var circleRadiusHover = 6;
  


var maxValue = 0;
for (var i = 0; i < data.length; i++){
  var temp = d3.max(data[i].values, d => d.value);
  if(temp > maxValue){
    maxValue = temp;
  }
}

  
  /* Scale */
  var xScale = d3.scaleTime()
    .domain(d3.extent(data[0].values, d => d.date))
    .range([0, width-margin]);
  
  var yScale = d3.scaleLinear()
    .domain([0, maxValue+.5])
    .range([height-margin, 0]);
  
  var color = colo;
  
  /* Add SVG */
  var svg = d3.select("#chart").append("svg")
    .attr("width", (width+margin)+"px")
    .attr("height", (height+margin)+"px")
    .append('g')
    .attr("transform", `translate(${margin}, ${margin})`);
  
  
  /* Add line into SVG */
  var line = d3.line()
    .x(d => xScale(d.date))
    .y(d => yScale(d.value));
  
  let lines = svg.append('g')
    .attr('class', 'lines');
  
  lines.selectAll('.line-group')
    .data(data).enter()
    .append('g')
    .attr('class', 'line-group')  
    .on("mouseover", function(d, i) {
        svg.append("text")
          .attr("class", "title-text")
          .style("fill", color(i))        
          .text(d.name)
          .attr("text-anchor", "middle")
          .attr("x", (width-margin)/2)
          .attr("y", 12);
      })
    .on("mouseout", function(d) {
        svg.select(".title-text").remove();
      })
    .append('path')
    .attr('class', 'line')  
    .attr('d', d => line(d.values))
    .style('stroke', (d, i) => color(i))
    .style('opacity', lineOpacity)
    .style('stroke-width', 1.5)
    .on("mouseover", function(d) {
        d3.selectAll('.line')
                      .style('opacity', otherLinesOpacityHover);
        d3.selectAll('.circle')
                      .style('opacity', circleOpacityOnLineHover);
        d3.select(this)
          .style('opacity', lineOpacityHover)
          .style("stroke-width", lineStrokeHover)
          .style("cursor", "pointer");
      })
    .on("mouseout", function(d) {
        d3.selectAll(".line")
                      .style('opacity', lineOpacity);
        d3.selectAll('.circle')
                      .style('opacity', circleOpacity);
        d3.select(this)
          .style("stroke-width", lineStroke)
          .style("cursor", "none");
      });
  
  
  /* Add circles in the line */
  lines.selectAll("circle-group")
    .data(data).enter()
    .append("g")
    .style("fill", (d, i) => color(i))
    .selectAll("circle")
    .data(d => d.values).enter()
    .append("g")
    .attr("class", "circle")  
    .on("mouseover", function(d) {
        d3.select(this)     
          .style("cursor", "pointer")
          .append("text")
          .attr("class", "text")
          .text(`${d.value}`)
          .attr("x", d => xScale(d.date) + 5)
          .attr("y", d => yScale(d.value) - 10);
      })
    .on("mouseout", function(d) {
        d3.select(this)
          .style("cursor", "none")  
          .transition()
          .duration(duration)
          .selectAll(".text").remove();
      })
    .append("circle")
    .attr("cx", d => xScale(d.date))
    .attr("cy", d => yScale(d.value))
    .attr("r", circleRadius)
    .style('opacity', circleOpacity)
    .on("mouseover", function(d) {
          d3.select(this)
            .transition()
            .duration(duration)
            .attr("r", circleRadiusHover);
        })
      .on("mouseout", function(d) {
          d3.select(this) 
            .transition()
            .duration(duration)
            .attr("r", circleRadius);  
        });
  
  
  /* Add Axis into SVG */
  var xAxis = d3.axisBottom(xScale).ticks(5);
  var yAxis = d3.axisLeft(yScale).ticks(5);
  
  svg.append("g")
    .attr("class", "x axis")
    .attr("transform", `translate(0, ${height-margin})`)
    .call(xAxis);
  
  svg.append("g")
    .attr("class", "y axis")
    .call(yAxis)
    .append('text')
    .attr("y", 15)
    .attr("transform", "rotate(-90)")
    .attr("fill", "#000")
    .text("Values");

    svg.append("text")
        .attr("x", (width / 2))             
        .attr("y", 0)
        .attr("text-anchor", "middle")  
        .style("font-size", "16px") 
        .style("text-decoration", "underline")  
        .text(txt);

}
