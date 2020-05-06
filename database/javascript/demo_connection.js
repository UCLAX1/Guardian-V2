var mysql = require('mysql');
var fs = require('fs');

lastNVals = function(count){
    return new Promise(function(resolve, reject){
        var con = mysql.createConnection({
            host: "localhost",
            user: "tate",
            password: "pass123",
            database: "x1_guardian"
        });
        con.query("SELECT * FROM position_data ORDER BY id DESC LIMIT ?", [count], function(err, results) {
            con.end();
            if(results === undefined){
                 reject(new Error("Error rows is undefined"));             
            } else {  
                var parsed_results = [];  
                if(results.length){
                    var line = JSON.stringify(results);
                    lines = line.split("},");
                    for (var i = 0; i < lines.length; i++) {
                        lines[i] = lines[i].replace( /[{}\[\]"]/g, "");
                        var split_string = lines[i].split(",");
                        var final_string = "";
                        for (var j = 0; j < split_string.length; j++) {
                            split_string[j] = split_string[j].replace( /^.+["a-zA-Z]:/, "");
                            final_string = final_string.concat(split_string[j], ",");
                        }
                        final_string = final_string.slice(0, -1);
                        parsed_results.push(final_string);
                    }
                 }             
                resolve(parsed_results);             
            }
        }
    )}
)}

lastNVals(5) 
.then(function(results){   
    render(results) 
}) 
.catch(function(err){   
    console.log("Promise rejection error: "+err); 
})  
render = function(results){ 
    console.log(results);  
}

getAllVals = function(){
    return new Promise(function(resolve, reject){
        var con = mysql.createConnection({
            host: "localhost",
            user: "tate",
            password: "pass123",
            database: "x1_guardian"
        });
        con.query("SELECT * FROM position_data", function(err, results) {
            con.end();
            if(results === undefined){
                 reject(new Error("Error rows is undefined"));             
            } else {  
                var returned_string = "";  
                if(results.length){
                    var line = JSON.stringify(results);
                    lines = line.split("},");
                    for (var i = 0; i < lines.length; i++) {
                        lines[i] = lines[i].replace( /[{}\[\]"]/g, "");
                        var split_string = lines[i].split(",");
                        var final_string = "";
                        for (var j = 0; j < split_string.length; j++) {
                            split_string[j] = split_string[j].replace( /^.+["a-zA-Z]:/, "");
                            final_string = final_string.concat(split_string[j], ",");
                        }
                        final_string = final_string.slice(0, -1);
                        returned_string = returned_string.concat(final_string, '\n');
                        final_string = final_string.slice(0, -1);
                    }
                 }             
                resolve(returned_string);             
            }
        }
    )}
)}

getAllVals() 
.then(function(results){   
    render(results) 
}) 
.catch(function(err){   
    console.log("Promise rejection error: "+err); 
})  
render = function(results){ 
    console.log(results);  
}
