<?php
session_start(); // Start a new session

// Server connection details
$servername = "localhost";
$username = "root"; // Your database username
$password = ""; // Your database password
$dbname = "Schools"; // Your database name

// Create connection
$conn = mysqli_connect($servername, $username, $password, $dbname);

// Check connection
if ($conn === false) {
    die("ERROR: Could not connect. " . mysqli_connect_error());
}

// Check if the form is submitted
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Taking values from the form data
    $username = trim($_POST['username']);
    $password = trim($_POST['password']);

    // Validate inputs
    if (empty($username) || empty($password)) {
        die("Username and password are required.");
    }

    // Prepare a select statement
    $sql = "SELECT id, password FROM users WHERE username = ?";
    $stmt = mysqli_prepare($conn, $sql);
    
    // Bind the username to the prepared statement
    mysqli_stmt_bind_param($stmt, "s", $username);

    // Execute the statement
    mysqli_stmt_execute($stmt);

    // Store the result
    mysqli_stmt_store_result($stmt);
    
    // Check if the user exists
    if (mysqli_stmt_num_rows($stmt) == 1) {
        // Bind result variables
        mysqli_stmt_bind_result($stmt, $id, $hashed_password);
        mysqli_stmt_fetch($stmt);

        // Verify the password
        if (password_verify($password, $hashed_password)) {
            // Password is correct, start a session
            $_SESSION['username'] = $username;
            $_SESSION['id'] = $id;
            echo "Login successful! Welcome, " . htmlspecialchars($username) . ".";
            // Redirect to a protected page or dashboard
            // header("Location: dashboard.php");
            exit;
        } else {
            echo "ERROR: Incorrect password.";
        }
    } else {
        echo "ERROR: No account found with that username.";
    }

    // Close statement
    mysqli_stmt_close($stmt);
}

// Close connection
mysqli_close($conn);
?>
