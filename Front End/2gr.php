
<?php
$mystring = '/var/www/2gr.py';
$command = escapeshellcmd($mystring);
$output = shell_exec($command);
echo $output;
?>


