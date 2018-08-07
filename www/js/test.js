var PythonShell = require('python-shell');

var options = {
    mode: 'text',
    pythonPath: '/usr/bin/python',
    pythonOptions: ['-u'],
    scriptPath: './bin',
    args: ['value1', 'value2', 'value3']
  };

function test(){
console.log("test.js")
 "use strict"
 PythonShell.run('beamer.py', options, function (err, results) {
  if (err) throw err;
  // results is an array consisting of messages collected during execution
  console.log('results: %j', results);
});
 
}