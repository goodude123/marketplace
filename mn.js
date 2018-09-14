//slide effect nałożony na menu
$(document).ready(function(){
$("#men").hide();
	$("#menu_linki").mouseenter(function(){
		$("#menu_linki").css("color", "white");
	});
	$("#menu_linki").mouseleave(function(){
		$("#menu_linki").css("color", "#ffcc66");
	});
	$("#menu_linki").ready(function(){
        $("#men").slideToggle("slow");
    });
	$("#menu_linki").click(function(){
        $("#men").slideToggle("slow");
    });
	
	
//podświetlanie aktualnego kafelka podstrony
	var pyk1;
	var pyk2;
	var pyk3;
	
	$("#pod1").click(function(){
	pyk1 = true;
	
	if(pyk1==true){
		$("#pod1").css("background-color", "white");
	}
	if(pyk2==true || pyk3==true){
	$("#pod2, #pod3").css("background-color", "#ffcc66");
	}
	});
	
	
	$("#pod2").click(function(){
	pyk2 = true;
	
	if(pyk2==true){
		$("#pod2").css("background-color", "white");
	}
	if(pyk1==true || pyk3==true){
	$("#pod1, #pod3").css("background-color", "#ffcc66");
	}
	});
	
	
	$("#pod3").click(function(){
	pyk3 = true;
	
	if(pyk3==true){
		$("#pod3").css("background-color", "white");
	}
	if(pyk1==true || pyk2==true){
	$("#pod1, #pod2").css("background-color", "#ffcc66");
	}
	});
	
	
});
