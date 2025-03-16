<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $mac = escapeshellarg($_POST["mac"]);
    $dhcp = escapeshellarg($_POST["dhcp"]);

    // Run the Python script
    $command = "python3 network_config.py $mac $dhcp";
    $output = shell_exec($command);

    if ($output) {
        $result = json_decode($output, true);
        
        if (isset($result["error"])) {
            echo "<p>Error: " . htmlspecialchars($result["error"]) . "</p>";
        } else {
            echo "<h2>Assigned IP Details</h2>";
            echo "<p>MAC Address: " . htmlspecialchars($result["mac_address"]) . "</p>";
            echo "<p>Assigned IP: " . htmlspecialchars($result["assigned_ip"]) . "</p>";
            echo "<p>Lease Time: " . htmlspecialchars($result["lease_time"]) . "</p>";
        }
    } else {
        echo "<p>Error: Could not retrieve response from DHCP server.</p>";
    }
} else {
    echo "<p>Error: Invalid request.</p>";
}

// Get and display the public IP address (always displayed)
$publicIP = trim(shell_exec('curl -4 ifconfig.io'));
if (!empty($publicIP)) {
    echo "<p><strong>Public IP Address:</strong> " . htmlspecialchars($publicIP) . "</p>";
} else {
    echo "<p><strong>Could not retrieve public IP address.</strong></p>";
}

?>
