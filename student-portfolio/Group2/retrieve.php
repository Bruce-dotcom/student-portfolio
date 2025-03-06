<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Student Data</title>
    <link rel="stylesheet" href="">
</head>
<body>

<div class="container">
    <h2>Registered Students</h2>

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

    // Define the base URL for attachments
    $base_url = 'http://yourwebsite.com/uploads/'; // Modify this to your actual base URL

    // Prepare a select statement
    $sql = "SELECT id, name, email, phone, course, attachment, attach FROM students";
    $result = mysqli_query($conn, $sql);

    // Check if there are results
    if (mysqli_num_rows($result) > 0) {
        // Output data in a table
        echo "<table border='1'>
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Phone</th>
                    <th>Course</th>
                    <th>Attachment</th>
                    <th>Photo</th>
                    <th>Actions</th>
                    
                    
                </tr>";

        // Fetch each row and display it
        while ($row = mysqli_fetch_assoc($result)) {
            echo "<tr>
                    <td>" . htmlspecialchars($row['id']) . "</td>
                    <td>" . htmlspecialchars($row['name']) . "</td>
                    <td>" . htmlspecialchars($row['email']) . "</td>
                    <td>" . htmlspecialchars($row['phone']) . "</td>
                    <td>" . htmlspecialchars($row['course']) . "</td>
                    <td><a href='" . htmlspecialchars($row['attachment']) . "' target=''>View Document</a></td>
                    <td><a href='" . htmlspecialchars( $row['attach']) . "' target='_blank'>View Photo</a></td>
                     <td>
                        <a href='update.php?id=" . urlencode($row['id']) . "'>Update</a> | 
                        <a href='delete.php?id=" . urlencode($row['id']) . "' onclick='return confirm(\"Are you sure you want to delete this record?\");'>Delete</a>
                    </td>
                  </tr>";
        }
        echo "</table>";
    } else {
        echo "<h3>No records found.</h3>";
    }

    // Close connection
    mysqli_close($conn);
    ?>
</div>

</body>
</html>
