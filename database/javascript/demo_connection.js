var mysql = require('mysql');
var fs = require('fs');

var con = mysql.createConnection({
    host: "localhost",
    user: "tate",
    password: "pass123",
    database: "x1_guardian"
});

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
            console.log(result);
        });
    });
    return results;
}

function getAllVals() {
    con.connect(function(err) {
        if (err) throw err;
        con.query("SELECT * FROM position_data", function(err, result, fileds) {
            if (err) throw err;
            fs.open("log.csv", "w", function (err, file) {
                if (err) throw err;
            });
            fs.appendFile("log.csv", "ID,Link_x,Link_y,Laser_x,Laser_y,Time\n", function (err) {
                if (err) throw err;
            });
            for (var i = 0; i < result.length; i++) {
                result[i] = JSON.stringify(result[i]);
                result[i] = result[i].replace(/[{}]/g, "");
                var split_result = result[i].split(",");
                var final_string = "";
                for (var j = 0; j < split_result.length; j++) {
                    split_result[j] = split_result[j].replace( /^.+["a-zA-Z]:/, "");
                    split_result[j] = split_result[j].replace( /"/g, "");
                    final_string = final_string.concat(split_result[j], ",");
                }
                final_string = final_string.slice(0, -1);
                final_string = final_string.concat("\n");
                console.log(final_string);
                fs.appendFile('log.csv', final_string, function (err) {
                    if (err) throw err;
                });
            }
        });
    });
}
