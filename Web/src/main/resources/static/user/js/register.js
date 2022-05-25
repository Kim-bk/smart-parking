/**
 * 
 */
$(document).ready(function(){
	$("#province").change(function(){
		var select = document.getElementById("province");
		var value = select.options[select.selectedIndex].value;
		
		
		$.ajax({
			url :"/user/district",
			type : "GET",
			data : {province_id:value},
			success: function(html_value){
				var output ="";
				$.each(html_value, function(index, value){
					output +="<option value="+value.id+">"+value.name+"</option>";
					$("#district").html(output);
				});
			},
			error: function(){
				alert("ban da bi loi")
			}
		})
	})
	$('#district').change(function(){
		var select = document.getElementById("district");
		var value = select.options[select.selectedIndex].value;
		$.ajax({
			url :"/user/ward",
			type :"GET",
			data : {district_id:value},
			success: function(html_value){
			var output="";
			$.each(html_value,function(index,value){
				output += "<option value="+value.id+">"+value.name+"</option>";
				$("#ward").html(output);
			})
			},
			error: function(){
				alert("ban da bi loi")
			}
		})
			
		});
	
})