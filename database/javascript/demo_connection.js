var mysql = require('mysql');
var fs = require('fs');

var con = mysql.createConnection({
    host: "localhost",
    user: "tate",
    password: "pass123",
    database: "x1_guardian"
});

// lastNVals(int count)
//   return array of count last values in desc order

function lastNVals(count) {
    var results = [];
    con.connect(function(err) {
        if (err) throw err;
        var sel = "SELECT * FROM position_data ORDER BY id DESC LIMIT ";
        sel = sel.concat(count.toString());
        con.query(sel, function(err, result, fields) {
            if (err) throw err;
            result = JSON.stringify(result);
            results.push(result);
            // console.log(result);
        });
        // var sel = "SELECT id FROM position_data ORDER BY id DESC LIMIT ";
        // var command = sel.concat(count.toString());
        // con.query(command, function(err, result, fields) {
        //     if (err) throw err;
        //     result = JSON.stringify(result);
        //     console.log(result);
            
        // });
    });
    // con.end((err) => {});
    return results;
}

// getAllVals()
//   download csv/

function getAllVals() {
    con.connect(function(err) {
        if (err) throw err;
        con.query("SELECT * FROM position_data", function(err, result, fileds) {
            if (err) throw err;
            fs.open("log.csv", "w", function (err, file) {
                if (err) throw err;
            });
            // need to format the lines for csv still
            for (var i = 0; i < result.length; i++) {
                result[i] = JSON.stringify(result[i]);
                // string parsing stuff: 
                //    remove { } at beginning and end
                //    split string into array at ,
                //    remove everything up to and including first :
                //    put array back into , separated string
                //    remove all quotes
                result[i] = result[i].replace(/[{}]/g, "");
                var split_result = result[i].split(",");
                var final_string = "yeet";
                for (var j = 0; j < split_result.length; j++) {
                    //console.log(split_result[j].replace( /^.+["a-zA-Z]:/, ""));
                    // works
                    split_result[j] = split_result[j].replace( /^.+["a-zA-Z]:/, "");
                    // works
                    split_result[j] = split_result[j].replace( /"/g, "");
                    final_string.concat(split_result[j], ",");
                }
                final_string[final_string.length-1] = '\n';
                console.log(final_string);
                fs.appendFile('log.csv', final_string, function (err) {
                    if (err) throw err;
                });
            }
        });
    });
}

getAllVals();
// var yeet = lastNVals(5);
// console.log(yeet);