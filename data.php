<?php

$numLines = intval($_REQUEST["numLines"]);

exec("tail -n " . $numLines . " /var/log/nginx/allapps.log > data.json");
echo file_get_contents("data.json");