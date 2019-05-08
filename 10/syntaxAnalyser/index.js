
const program = require('commander');
const fs = require('fs');
module.exports = () => {

program
	.version('1.0.0')
	.description('Compiler for the Jack computer language')
   	.usage('[options] file/directory')
   	.command('anaylse <dir>')
   	.action(function(dir, options) {
	
	       	console.log('Analyse this! Dir: ' + dir + ' options:' + options);			
		fs.stat(dir, function(err, file) {
    			if (err) {
        			if (err.code == 'ENOENT') {
            			console.log('Does not exist.');
        			}
   			} else {
        			if (file.isFile()) {
        				fs.readFile(dir, 'utf8', function(err, fileContents) {
    						if (err) throw err;
    						console.log(fileContents)
					});
				} else if (file.isDirectory()) {
            				console.log('Directory found.');
        			}
    			}
		});
    	});

   	program.parse(process.argv);
}
