<?php
    $dirname = "./imgs/";
    array_map('unlink', glob("$dirname/*.*"));
    rmdir($dirname);
?>