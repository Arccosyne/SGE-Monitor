#! /usr/bin/env python

#Grid Engine Monitor
#
#This is a grahpical frontend monitor for SGE with a HTTP-based backend

import os
import json
import requests

#Fetch data from backend on SGE server

r = requests.get('http://<SERVER IP>:8080')
status = json.loads(r.text)

q = requests.get('http://<>SERVER IP:8080/full')
s = q.text
full = s.split('\n')

total = status['total']
available = status['available']
unavailable = status['unavailable']
disabled = status['disabled']
errors = status['errors']
working = status['working']
pqueue = status['pqueue']
qqueue = status['qqueue']
gpuqueue = status['gpuqueue']
jobswaiting = status['jobswaiting']
au = status['au']
adu = status['adu']
aduE = status['aduE']
E = status['E']
d = disabled 

down = (int(unavailable) * 100) / int(total)
availablepercent = 100 - down
free = int(total) - int(working) 
workingdrill = (int(working) * 100) / (int(total) - int(down))
availabledrill = 100 - int(workingdrill)

print """
<html>
<head>
  <title>SGE Grid</title>

  <script  src="http://ajax.googleapis.com/ajax/libs/jquery/1.8.2/jquery.min.js"></script>
  <script  src="https://code.highcharts.com/highcharts.js"></script>
  <script  src="https://code.highcharts.com/modules/exporting.js"></script>

  <link rel="stylesheet" type="text/css" href="//code.jquery.com/ui/1.11.2/themes/smoothness/jquery-ui.css">
  <link rel="stylesheet" type="text/css" href="//cdn.datatables.net/plug-ins/1.10.7/integration/jqueryui/dataTables.jqueryui.css">

  <script type="text/javascript" src="//code.jquery.com/jquery-1.11.1.min.js"></script>
  <script type="text/javascript" src="//cdn.datatables.net/1.10.7/js/jquery.dataTables.min.js"></script>
  <script type="text/javascript" src="//cdn.datatables.net/plug-ins/1.10.7/integration/jqueryui/dataTables.jqueryui.js"></script>

  <script type="text/javascript" class="init">
  } );
  </script>
</head>

<body>

<div id="usechartcontainer" style="min-width: 310px; height: 400px; max-width: 600px; margin: 0 auto"></div>
<script>
$(function () {

    // Radialize the colors
    Highcharts.getOptions().colors = Highcharts.map(Highcharts.getOptions().colors, function (color) {
        return {
            radialGradient: {
                cx: 0.5,
                cy: 0.3,
                r: 0.7
            },
            stops: [
                [0, color],
                [1, Highcharts.Color(color).brighten(-0.3).get('rgb')] // darken
            ]
        };
    });

    // Build chart 1
    var chart = new Highcharts.Chart({
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false,
            type: 'pie',
            renderTo: 'usechartcontainer'
        },
        credits: {
            enabled: false
        },
        tooltip: {
            pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    enabled: true,
                    format: '<b>{point.name}</b>: {point.percentage:.1f} %',
                    style: {
                        color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
                    },
                    connectorColor: 'silver'
                }
            }
        },
        series: [{
            name: 'User Share',
            data: [
"""

#Generate use share graph

users = {}
STRING = []
for line in full:
   if len(line) >= 1:
      A = line.split()
#      print A[3]
      if A[3] in users:
         users[A[3]] += 1
      else:
         users[A[3]] = 1

for user in users:
   STRING.append("{ name: '%s', y: %s }" % (user,users[user]))
print ','.join(STRING)

print """
            ]
        }]
    });

// Create the chart 2
    var chart2 = new Highcharts.Chart({
        chart: {
            type: 'pie'
        },
        title: {
            text: 'Availability'
        },
        subtitle: {
            text: 'Click slices for additional verbosity'
        },
        plotOptions: {
            series: {
                dataLabels: {
                    enabled: true,
                    format: '{point.name}: {point.y:.1f}%'
                }
            }
        },

        tooltip: {
            headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
            pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y:.2f}%</b> of total<br/>'
        },
        series: [{
            name: 'Nodes',
            colorByPoint: true,
            data: [{
                name: 'Available',
                y: """

print str(availablepercent) + ","
print """
                drilldown: 'Available'
            }, {
                name: 'Down',
                y: """

print str(down) + ","
print """
                drilldown: 'Down'
            }]
        }],
        drilldown: {
            series: [{
                name: 'Available',
                id: 'Available',
                data: [
                    ['Free', """
print str(availabledrill) + "],"
print """
		   ['Working', """
print str(workingdrill) + "],"
print """
                ]
            }, {
                name: 'Error Code:',
                id: 'Down',
                data: [
                    ['au', """
print au + "],"
print """
                    ['adu', """
print adu + "],"
print """
                    ['aduE', """
print aduE + "],"
print """
                    ['E', """
print E + "],"
print """
		    ['d', """
print d + "]"
print """
                ]
            }]
        }
    });
});

        </script>
        </head>
        <body>
<script src="https://code.highcharts.com/highcharts.js"></script>
<script src="https://code.highcharts.com/modules/data.js"></script>
<script src="https://code.highcharts.com/modules/drilldown.js"></script>

<div id="drilldowncontainer" style="min-width: 310px; max-width: 600px; height: 400px; margin: 0 auto"></div>

"""

#############################

#Specify fields in table

TABLE = ''
TABLE += '<table id="t01" class="display" width="100%">\n'
TABLE += '<thead>\n'
TABLE += '<tr>\n'
TABLE += '  <th>Job ID</th>\n'
TABLE += '  <th>Prior</th>\n'
TABLE += '  <th>Name</th>\n'
TABLE += '  <th>User</th>\n'
TABLE += '  <th>Status</th>\n'
TABLE += '  <th>Submitted</th>\n'
TABLE += '  <th>Submit time</th>\n'
TABLE += '  <th>Queue</th>\n'
TABLE += '  <th>Cores</th>\n'
TABLE += '</tr>\n'
TABLE += '</thead>\n'
TABLE += '<tbody>\n'

#Parse input into rows

for i in full:
  if len(i) >= 1:
    TABLE += '<tr>\n'
    part = i.split() 
    for item in part:
       TABLE += '<td> %s </td>\n' % item
    TABLE += '</tr>\n'

TABLE += '</tbody>\n'
TABLE += '</table>\n'

#Import client side scripts

print """

  <script  src="http://ajax.googleapis.com/ajax/libs/jquery/1.8.2/jquery.min.js"></script>
  <script  src="https://code.highcharts.com/highcharts.js"></script>
  <script  src="https://code.highcharts.com/modules/exporting.js"></script>


  <link rel="stylesheet" type="text/css" href="//code.jquery.com/ui/1.11.2/themes/smoothness/jquery-ui.css">
  <link rel="stylesheet" type="text/css" href="//cdn.datatables.net/plug-ins/1.10.7/integration/jqueryui/dataTables.jqueryui.css">

  <script type="text/javascript" src="//code.jquery.com/jquery-1.11.1.min.js"></script>
  <script type="text/javascript" src="//cdn.datatables.net/1.10.7/js/jquery.dataTables.min.js"></script>
  <script type="text/javascript" src="//cdn.datatables.net/plug-ins/1.10.7/integration/jqueryui/dataTables.jqueryui.js"></script>

  <script type="text/javascript" class="init">
  $(document).ready(function() {
        $('#t01').dataTable({"pageLength": 10});

  } );
  </script>


"""

#Create statistics chart

print """
<link rel="stylesheet" type="text/css" href="new.css">
<div class="datagrid"><table>
<tbody><tr><td>Total nodes</td><td>{a}</td></tr>
<tr class="alt"><td>Available nodes</td><td>{b}</td></tr>
<tr><td>Nodes with job (working)</td><td>{c}</td></tr>
<tr class="alt"><td>Admin disabled nodes</a></td><td>{d}</td></tr>
<tr><td>Nodes with error</a></td><td>{e}</td></tr>
<tr class="alt"><td>Jobs working in P queue</td><td>{f}</td></tr>
<tr><td>Nodes working in Q queue</td><td>{g}</td></tr>
<tr class="alt"><td>Jobs working in GPU queue</td><td>{h}</td></tr>
<tr><td><a href="queue.php">Jobs waiting for free node</a><td>{i}</td></tr>
</tbody>
</table></div>
<br>
<br>
""".format(a=total, b=available, c=working, d=disabled, e=errors, f=pqueue, g=qqueue, h=gpuqueue, i=jobswaiting)

#Output the table to screen

print TABLE
print """
</body>
</html>
"""
