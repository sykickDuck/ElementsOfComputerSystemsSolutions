const path = require("path");
const exec = require("child_process").exec;
const fs = require("fs");
const del = require("del");

test("Running tokenizer on Square dance project produces expected files", () => {
  const testContext = {
    //run jack tokenizer in following location
    testLocation: path.resolve("./testLocation"),
    //expected output for comparision
    expectedFiles: [
      path.resolve("../Square/MainT.xml"),
      path.resolve("../Square/SquareGameT.xml"),
      path.resolve("../Square/SquareT.xml")
    ],
    command: "tokenise",
    compilationTarget: `${path.resolve("../Square")}`
  };

  //currently expected files does effect results of test
  return makeDir(testContext)
    .then(runJcc)
    .then(getJccOutput)
    .then(reviewJccOutputWith)
    .then(deleteDir);

  //.catch(err => throw new Error(err));

  // if (fs.existsSync(testContext.testLocation)) {
  //   del(testContext.testLocation);
  //}

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

  function reviewJccOutputWith(options) {
    return new Promise((resolve, reject) => {
      options.expectedFiles.forEach(expectedFile => {
        expect(options.compilerOutput).toContain(path.basename(expectedFile));
      });
      resolve(options);
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

  function deleteDir(testContext) {
    if (fs.existsSync(testContext.testLocation)) {
      return del(testContext.testLocation);
    }
  }
});
