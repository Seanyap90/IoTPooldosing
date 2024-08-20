var count1;
var counter1;
var count2;
var counter2;
var count3;
var counter3;


//var led = new Gpio(18, 'out');


function resetEverything1()
{
	$("#counter1, #myButton03").hide();
	$('#myButton02').show();
	clearInterval(counter1);  
	console.log("Reset1");
	//led.writeSync(0);
}

function resetEverything2()
{
	$("#counter2, #myButton05").hide();
	$('#myButton04').show();
	clearInterval(counter2);  
}

function resetEverything3()
{
	$("#counter3, #myButton07").hide();
	$('#myButton06').show();
	clearInterval(counter3);  
}

$(document).ready(function(){
	resetEverything1();
	resetEverything2();
	resetEverything3();
	
	//LED 1
	$('#myButton02').click(function(){
		$('#myButton02').hide();
		$('#myButton03').show();
		console.log("LED 1 on");
		//led.writeSync(1);
		$('#counter1').animate({width: 'toggle'});
		count1=10;
		counter1=setInterval(timer1, 1000);
		function timer1(){
		document.getElementById("secs1").innerHTML=count1 + " secs";		
		
		if (count1 <= 0){
			$("#counter1, #myButton03").hide();
			$('#myButton02').show();
			clearInterval(counter1);
			return;  }
		count1=count1-1;
		}
	});

	$('#myButton03').click(function(){
		console.log("LED 1 off");
		resetEverything1();
	});
	
	//LED 2
	$('#myButton04').click(function(){
		$('#myButton04').hide();
		$('#myButton05').show();
		$('#counter2').animate({width: 'toggle'});
		count2=10;
		counter2=setInterval(timer2, 1000);
		function timer2(){
		count2=count2-1;
		if (count2 <= 0){
			$("#counter2, #myButton05").hide();
			$('#myButton04').show();
			clearInterval(counter2);
			return;  }
		document.getElementById("secs2").innerHTML=count2 + " secs";}
	});

	$('#myButton05').click(function(){
		resetEverything2();
	});
	
	//LED 3
	$('#myButton06').click(function(){
		$('#myButton06').hide();
		$('#myButton07').show();
		$('#counter3').animate({width: 'toggle'});
		count3=10;
		counter3=setInterval(timer3, 1000);
		function timer3(){
		count3=count3-1;
		if (count3 <= 0){
			$("#counter3, #myButton07").hide();
			$('#myButton06').show();
			clearInterval(counter3);
			return;  }
		document.getElementById("secs3").innerHTML=count3 + " secs";}
	});

	$('#myButton07').click(function(){
		resetEverything3();
	});
});
