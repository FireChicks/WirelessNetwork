var mysql      = require('mysql2');
var connection = mysql.createConnection({
  host     : 'localhost',
  user     : 'root',
  password : '', // passward
  database : 'attend_board'
});
 
connection.connect();
 
module.exports = connection;