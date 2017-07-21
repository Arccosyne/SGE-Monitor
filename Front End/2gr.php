
<?php
$mystring = '/var/www/scmods/andrew/2gr.py';
$command = escapeshellcmd($mystring);
$output = shell_exec($command);
echo $output;
?>


