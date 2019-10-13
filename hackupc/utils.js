//google-chrome --disable-web-security -–allow-file-access-from-files --user-data-dir http://127.0.0.1/hackupc/predict.php 


function saveCanvas(imgs_data, i, canvas_img_data) {
    // var canvas_img_data = pad.getSignatureImage(); // canvas.toDataURL('image/png');
	var img_data = canvas_img_data.replace(/^data:image\/(png|jpg);base64,/, "");
	imgs_data[i] = img_data;
}

function resizeArray(list, N) {
    if (list.length <= N) return list;
    rate = list.length/N; // > 1
    
    newlist = [];
    listCounter = 0;
    
    for (let r = 0.; r < list.length; r += rate) {
        console.log(listCounter, list[parseInt(r, 10)].substring(54, 85));
        newlist[listCounter++] = list[parseInt(r, 10)];
    }
    
    // Handle precision errors
    while (newlist.length > N) newlist.pop();
    return newlist;
}

function save2Image(imgs_data, author) {
    // UUID is the time right now
    let uuid = $.now();
    
    imgs_data = resizeArray(imgs_data, 20);
    console.log(imgs_data.length);
    
    if (author == "") author = "Predict";
    
    // Save each image individually
	imgs_data.forEach(function (img_data, i) {
        $.ajax({
    		url: 'save_sign.php',
    		data: {
    			img_data: img_data,
    			author: author,
    			uuid: uuid,
    			id: i
    		},
    		type: 'post',
    		success: function (response) {
    		    console.log(i, response);
    		},
    		error: function () {
    			console.log('Error in saving the image')
    		}
    	}); 
	});
	
	if (author != "Predict") {
    	// Save to zip
    	$.ajax({
    		url: 'zip.php',
    		data: { author: author },
    		type: 'post',
    		success: function () {
    		    console.log('Folder ' + author + ' compressed');
    		}
    	});
	} else {
		let ngrow8k = 'http://71f34c6b.ngrok.io';
		fetch(ngrow8k)
			.then((response) => response.json())
			.then((data) => {
				console.log(data)
				alert(data.winner)
				document.write('<html><body><p>' + data.winner + '</p></body></html>');
			})
	}
}
