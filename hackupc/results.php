<html>
	<head>
	    <meta name="viewport" content="width=400">
	   
		<script src="https://code.jquery.com/jquery-3.4.1.min.js"></script>
		<script src="./jquery.signaturepad.min.js"></script> 
		<script src="https://github.com/niklasvh/html2canvas/releases/download/0.4.1/html2canvas.js"></script>
		
		<script src='utils.js'></script>
		<link rel="stylesheet" type="text/css" href="//fonts.googleapis.com/css?family=Open+Sans" />
		<link href="./css/basic.css" rel="stylesheet" />
	</head>
	<body>
		<div id="signArea" >
			<h2 class="tag-ingo">Results</h2>

			<img src="../Predict/0.png" />
			<br /><br />
			
			<div>It is... <strong><span id='winner'></span></strong>'s! (<span id='maxprob'></span>%)</div>
			<div>With average of <span id='avgprob'></span>%</div>
			<br />
			
			<a href='./predict.php'>Back to predict</a><br />
			<a href='./'>Back to main</a>
		</div>
		
		<script>
			$(document).ready(function() {
				let searchParams = new URLSearchParams(window.location.search);
				console.log(searchParams);
				
				$('#winner').html(searchParams.get('winner'));
				$('#maxprob').html(parseFloat(searchParams.get('maxprob') * 100).toFixed(2));
				$('#avgprob').html(parseFloat(searchParams.get('avgprop') * 100).toFixed(2));
				
				let maxNumPhotos = parseInt(searchParams.get('numphotos'), 10);
				let i = 0;
				
				console.log(maxNumPhotos);
				
				let sign_animation = setInterval(function() {
					if (i >= maxNumPhotos) clearInterval(sign_animation);
					$('img').attr("src", "../Predict/" + i + ".png");
					i = i + 1;
				}, 200);
			});
		</script>
	</body>
</html>
