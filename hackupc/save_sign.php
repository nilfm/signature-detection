<?php
	$author = $_POST['author'];
	$img_data = $_POST['img_data'];
	$uuid = $_POST['uuid'];
	$id = $_POST['id'];
	
	if ($author != "Predict") {
	    $path_author = '../ImageData/' . $author;
	    $path_sign = $path_author . '/' . $uuid;
	    
	    if (!is_dir($path_author)) mkdir($path_author);
    	if (!is_dir($path_sign)) mkdir($path_sign);
	} else {
	    $path_sign = '../Predict';
	}
	
    $filename = $path_sign . '/' . $id . '.png';
    file_put_contents($filename, base64_decode($img_data));
?>
