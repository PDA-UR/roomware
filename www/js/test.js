var PythonShell = require('python-shell');

var options = {
    mode: 'text',
    pythonOptions: ['-u'],
    scriptPath: './bin/beamer.py'
  };

function test(){
 "use strict"
 PythonShell.run('my_script.py', options, function (err, results) {
  if (err) throw err;
  // results is an array consisting of messages collected during execution
  console.log('results: %j', results);
});
 
}