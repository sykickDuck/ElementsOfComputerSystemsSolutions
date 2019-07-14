const path = require("path");
const exec = require("child_process").exec;
const fs = require("fs");
const del = require("del");

function testJcc(testContext) {
  return makeDir(testContext)
    .then(runJcc)
    .then(getJccOutput)
    .then(makeAssertion)
    .then(deleteDir);
}

function runJcc(options) {
  return new Promise((resolve, reject) => {
    exec(
      `node ${path.resolve("bin/jcc")} ${options.command} ${
        options.compilationTarget
      }`,
      { cwd: options.testLocation },
      (error, stdout, stderr) => {
        if (!error) {
          resolve(options);
        } else {
          reject(
            new Error(`-------Start of Error-------
            Jcc failed with code: ${error.code} 
            stdout: ${stdout}
            stderr: ${stderr}
            -------End of Error-------`)
          );
        }
      }
    );
  });
}

function getJccOutput(options) {
  return new Promise((resolve, reject) => {
    fs.readdir(options.testLocation, function(err, files) {
      if (err) reject(err);
      else {
        options.compilerOutput = files;
        resolve(options);
      }
    });
  });
}

function makeDir(testOptions) {
  return new Promise((resolve, reject) => {
    if (!fs.existsSync(testOptions.testLocation)) {
      fs.mkdir(testOptions.testLocation, err => {
        if (err) {
          reject(err);
        } else resolve(testOptions);
      });
    } else resolve(testOptions);
  });
}

function makeAssertion(testContext) {
  return testContext.assertion(testContext);
}

function deleteDir(testContext) {
  if (fs.existsSync(testContext.testLocation)) {
    return del(testContext.testLocation);
  }
}

module.exports = testJcc;
