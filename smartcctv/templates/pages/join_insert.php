<?php
$servername = "localhost";
$username = "root";
$password = "Sammaru!213";
$dbname = "cctv";
$port = "3306";
//create connection
$conn = new mysqli($servername, $username, $password, $dbname, $port);
//check connection
if($conn -> connect_error){
    die("Connection failed : " + $conn -> connect_error);
	}
	mysqli_select_db($conn, $dbname) or die('DB selection failed');
	$sql = "INSERT INTO user (email, name, password) values('$emali', '$name', '$password');";
	$result = $conn->query($sql);
	$name = $_POST['name'];
	$email = $_POST['email'];
	$password = $_POST['password'];
	if($conn->query($sql) === TRUE){
	    echo "New record created successfully";
		}else{
		    echo "Error: " . $sql . "<br>" . $conn->error;
			}

	$conn->close();
?>
