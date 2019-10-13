<?php
	//The URL that we want to GET.
	$url = 'home/nil/HackUPC/SignatureDetection/Python/predict.py'
	//Use file_get_contents to GET the URL in question.
	$contents = file_get_contents($url);
	echo $contents
?>
