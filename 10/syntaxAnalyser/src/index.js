//TODO: Sort out indentation mess below
//	Extract file code into seperate object?
//	Would need to be resuable when writing compiler
// Supported comment types: /** */ /* */ //

const program = require("commander");
const fs = require("fs");
const readline = require("readline");
const path = require("path");

module.exports = () => {
  program
    .version("1.0.0")
    .description("Compiler for the Jack computer language")
    .usage("[options] file/directory")
    .command("analyse <dir>")
    .action(function(dir, options) {
      fs.stat(dir, function(err, file) {
        if (err) {
          if (err.code == "ENOENT") {
            console.log("Does not exist.");
          }
        } else {
          if (file.isFile()) {
            const rl = readline.createInterface({
              input: fs.createReadStream(dir),
              crlfDelay: Infinity
            });
            var i = 0;
            rl.on("line", line => {
              i++;
              console.log("i incremented to " + i);
            });
            console.log(i + " lines in this file");
          } else if (file.isDirectory()) {
            console.log("Directory found.");
          }
        }
      });
    });

  program.command("tokenise <dir>").action(function(dir, options) {
    console.log(`tokenising ${dir}`);
    console.log(`Running in: ${process.cwd()}`);

    fs.readdir(dir, (err, dirContents) => {
      console.log(dirContents);
      const jackFiles = dirContents
        ? dirContents.filter(file => {
            return path.extname(file) == ".jack";
          })
        : [];
      console.log(jackFiles);

      jackFiles.forEach(file => {
        const tokenXmlFileName = path.basename(file).replace(".jack", "T.xml");
        fs.writeFile(tokenXmlFileName, "", err => {});
      });
    });
  });
  program.parse(process.argv);
};
