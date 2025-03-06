<!DOCTYPE html>
<html>

<head>
    <title>Insert Page</title>
</head>

<body>

    <?php
    // Server connection details
    $servername = "localhost";
    $username = "root";
    $password = "";
    $dbname = "Schools";

    // Create connection
    $conn = mysqli_connect($servername, $username, $password, $dbname);
    
    // Check connection
    if ($conn === false) {
        die("ERROR: Could not connect. " . mysqli_connect_error());
    }

    // Check if the form is submitted
    if ($_SERVER["REQUEST_METHOD"] == "POST") {
        // Taking values from the form data
        $name = trim($_REQUEST['name']);
        $email = trim($_REQUEST['email']);
        $phone = trim($_REQUEST['phone']);
        $course = trim($_REQUEST['course']);
        $attachment = trim($_REQUEST['attachment']);
        $attach = trim($_REQUEST['attach']);

        // Validate inputs
        if (empty($name) || empty($email) || empty($phone) || empty($course) || empty($attachment) || empty($attach)) {
            die("All fields are required.");
        }

        // Prepare an insert statement
        $sql = "INSERT INTO students (name, email, phone, course, attachment, attach) VALUES (?, ?, ?, ?, ?, ?)";
        $stmt = mysqli_prepare($conn, $sql);

        // Bind variables to the prepared statement
        mysqli_stmt_bind_param($stmt, "ssssss", $name, $email, $phone, $course, $attachment, $attach);

        // Execute the prepared statement
        if (mysqli_stmt_execute($stmt)) {
            echo "<h3>Data stored in the database successfully. ";
            echo "<a href='retrieve.php'>View Registered Students</a>"; 
        } else {
            echo "ERROR: Could not execute $sql. " . mysqli_error($conn);
        }

        // Close statement
        mysqli_stmt_close($stmt);
    }

    // Close connection
    mysqli_close($conn);
    ?>

</body>

</html>
