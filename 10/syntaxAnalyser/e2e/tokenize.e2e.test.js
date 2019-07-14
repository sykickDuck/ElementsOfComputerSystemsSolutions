const path = require("path");
const exec = require("child_process").exec;
const fs = require("fs");
const del = require("del");

const testJcc = require("./e2e-utils");

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
    compilationTarget: `${path.resolve("../Square")}`,
    assertion: reviewJccOutputWith
  };

  //currently expected files does effect results of test
  return testJcc(testContext);
});

function reviewJccOutputWith(options) {
  return new Promise((resolve, reject) => {
    options.expectedFiles.forEach(expectedFile => {
      expect(options.compilerOutput).toContain(path.basename(expectedFile));
    });
    resolve(options);
  });
}
