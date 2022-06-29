$(document).ready(function(){

	for (let i = 0;i<6;i++){
	
	$("#edit"+i).on('click',function(event){
	alert("hello");
		event.preventDefault();
		$('#edit').modal()
		});
		
}
})
