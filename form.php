<!DOCTYPE html>
<html>
<head>
    <title>Network Configuration Tool</title>
</head>
<body>
    <h2>Request an IP Address</h2>
    <form action="process.php" method="post">
        <label for="mac">MAC Address:</label>
        <input type="text" id="mac" name="mac" required pattern="([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})"><br><br>

        <label for="dhcp">DHCP Version:</label>
        <select id="dhcp" name="dhcp">
            <option value="DHCPv4">DHCPv4</option>
            <option value="DHCPv6">DHCPv6</option>
        </select><br><br>

        <input type="submit" value="Request IP">
    </form>
</body>
</html>
