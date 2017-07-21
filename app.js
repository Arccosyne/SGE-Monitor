//This is the backend server for SGEMon 
//Config as required, Launch with "nodejs app.js >sgemon/log&" 
//Andrew Damin

//Setup logging
var moment = require('moment');
var winston = require('winston');
var now = moment();

//Setup HTTP Listener and add SSL/TLS
var https = require('https');
var http = require('http');
var fs = require('fs');

var privateKey = fs.readFileSync('<CERTIFICATE KEY>.key', 'utf8');
//if (error !== null) {
//   winston.log('error', 'Could not open SSL key!');
//   }
var certificate  = fs.readFileSync('<CERTIFICATE>.pem', 'utf8');
//if (error !== null) {
//   winston.log('error', 'Could not open SSL certificate!');
//   }
var credentials = {key: privateKey, cert: certificate};
var express = require('express');
var app = express();

var httpServer = http.createServer(app);
var httpsServer = https.createServer(credentials, app);

httpServer.listen(8080);
   console.log('Web server listening on port 8080');
httpsServer.listen(8443);
   console.log('Web server listening on port 8443');

var exec = require('child_process').exec;
var stats = {}
var full = ""

//Generate data fields

stats.timestamp = now.format ('HH:mm:ss DD-MM-YYYY');

exec('qstat -f | sed "n; d" | tail -n+2 | wc -l | tr -d \'\\n\'', function(error, stdout, stderr) {
    stats.total = stdout;
    if (error !== null) {
	winston.log('warn', 'Could not fetch total nodes statistic from the grid engine daemon!')
    }
});
exec('qstat -f | sed "n; d" | awk -F" " \'$6 == "" { print $1 }\' | wc -l | tr -d \'\\n\'', function(error, stdout, stderr) {
    stats.available = stdout;
    if (error !== null) {
	winston.log('warn', 'Could not fetch available nodes statistic from the grid engine daemon!')
    }
});

exec('qstat -f | sed "n; d" | awk \'$6 != ""\' | tail -n +2 | wc -l | tr -d \'\\n\'', function(error, stdout, stderr) {
    stats.unavailable  = stdout;
    if (error !== null) {
	winston.log('warn', 'Could not fetch unavailable nodes statistic from the grid engine daemon!')
    }
});

exec('qstat -f | sed "n; d" | awk \'$6 ~ "d"\' | wc -l | tr -d \'\\n\'', function(error, stdout, stderr) {
    stats.disabled = stdout;
    if (error !== null) {
	winston.log('warn', 'Could not fetch total disabled statistic from the grid engine daemon!')
    }
});

exec('qstat -f | sed "n; d" | awk \'$6 !~ "d"\' | awk \'$6 != ""\' | wc -l | tr -d \'\\n\'', function(error, stdout, stderr) {
    stats.errors = stdout;
    if (error !== null) {
	winston.log('warn', 'Could not fetch error\'d nodes statistic from the grid engine daemon!')	
    }
});

exec('qstat -u "*" | tail -n+3 | awk \'$5 !~ "q"\' | wc -l | tr -d \'\\n\'', function(error, stdout, stderr) {
    stats.working = stdout;
    if (error !== null) {
	winston.log('warn', 'Could not fetch working nodes statistic from the grid engine daemon!')
    }
});

exec('qstat -u "*" | tail -n+3 | awk \'$8 ~ "ton.p"\' | wc -l | tr -d \'\\n\'', function(error, stdout, stderr) {
    stats.pqueue = stdout;
    if (error !== null) {
	winston.log('warn', 'Could not fetch total jobs in p queue statistic from the grid engine daemon!')
    }
});

exec('qstat -u "*" | tail -n+3 | awk \'$8 ~ "ton.q"\' | wc -l | tr -d \'\\n\'', function(error, stdout, stderr) {
    stats.qqueue = stdout;
    if (error !== null) {
	winston.log('warn', 'Could not fetch total jobs in q queue statistic from the grid engine daemon!')
    }
});

exec('qstat -u "*" | tail -n+3 | awk \'$8 ~ "ton.gpu"\' | wc -l | tr -d \'\\n\'', function(error, stdout, stderr) {
    stats.gpuqueue = stdout;
    if (error !== null) {
	winston.log('warn', 'Could not fetch total jobs in GPU queue statistic from the grid engine daemon!')
    }
});

exec('qstat -u "*" | tail -n+3 | awk \'$5 ~ "qw"\' | wc -l | tr -d \'\\n\'', function(error, stdout, stderr) {
    stats.jobswaiting  = stdout;
    if (error !== null) {
	winston.log('warn', 'Could not fetch total jobs waiting statistic from the grid engine daemon!')
    }
});

exec('qstat -f | sed "n; d" | awk \'$6 == "au"\' | wc -l | tr -d \'\\n\'', function(error, stdout, stderr) {
    stats.au = stdout;
    if (error !== null) {
	winston.log('warn', 'Could not fetch total au statistic from the grid engine daemon!')
    }
});

exec('qstat -f | sed "n; d" | awk \'$6 == "adu"\' | wc -l | tr -d \'\\n\'', function(error, stdout, stderr) {
    stats.adu = stdout;
    if (error !== null) {
	winston.log('warn', 'Could not fetch total adu statistic from the grid engine daemon!')
    }
});

exec('qstat -f | sed "n; d" | awk \'$6 == "aduE"\' | wc -l | tr -d \'\\n\'', function(error, stdout, stderr) {
    stats.aduE = stdout;
    if (error !== null) {
	winston.log('warn', 'Could not fetch total aduE statistic from the grid engine daemon!')
    }
});

exec('qstat -f | sed "n; d" | awk \'$6 == "E"\' | wc -l | tr -d \'\\n\'', function(error, stdout, stderr) {
    stats.E = stdout;
    if (error !== null) {
	winston.log('warn', 'Could not fetch total E statistic from the grid engine daemon!')
    }
});

exec('qstat -u "*" | awk \'$5 == "r"\'', function(error, stdout, stderr) {
    full = stdout;
    if (error !== null) {
	winston.log('warn', 'Could not fetch full running jobs statistics from the grid engine daemon!')
    }
});

exec('qstat -f | sed "n; d" | tail -n +2 | awk \'$6 != ""\'', function(error, stdout, stderr) {
    issues = stdout;
    if (error !== null) {
	winston.log('warn', 'Could not fetch total nodes with any issue statistic from the grid engine daemon!')
    }
});

exec('qstat -u "*" | tail -n+3 | awk \'$5 ~ "qw"\'', function(error, stdout, stderr) {
    queue = stdout;
    if (error !== null) {
        winston.log('warn', 'Could not fetch list of jobs in queue from the grid engine daemon!')
    }
});

//Configure HTTP outputs
app.get('/', function(req, res) {
   res.send(stats);
   winston.log('info', 'Recieved request for SGE statistics', now.format ('HH:mm:ss DD-MM-YYYY'))
});

app.get('/full', function(req, res) {
   res.send(full);
   winston.log('info', 'Recieved request for running jobs', now.format ('HH:mm:ss DD-MM-YYYY'))
});

app.get('/issues', function(req, res) {
   res.send(issues);
   winston.log('info', 'Recieved request for a list of nodes with problems', now.format ('HH:mm:ss DD-MM-YYYY'))
});

app.get('/queue', function(req, res) {
   res.send(queue);
   winston.log('info', 'Recieved request for a list of jobs in queue', now.format ('HH:mm:ss DD-MM-YYYY'))
});
