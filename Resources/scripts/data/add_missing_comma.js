// Check if a csv has all required commas

var fs  = require("fs");

var allLines = fs.readFileSync('./data/v2/csv/pokemon_moves.csv').toString().split('\n');

allLines.forEach(function (line) {
    var count = (line.match(/,/g) || []).length;
    if (count === 5) {
        line = line + ","
    }else if ( count === 6) {
        console.log('found mastery')
    } else if (count < 5) {
        console.log('?')
    }
    fs.appendFileSync("./data/v2/csv/pokemon_moves1.csv", line.toString() + "\n");
});
