<?php
	$author = $_POST['author'];
	$img_data = $_POST['img_data'];
	
	$img = base64_decode($img_data);
	file_put_contents('./imgs/'.$author.'_'. time() .'.png', $img);

	$files = array_diff(scandir('./imgs'), array('.', '..'));
	foreach ($files as $file) {
		echo $file . '\n';
	}
?>