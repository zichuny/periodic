$(document).ready(function () {
    $("#chaxun").bind("click", function () {
        $.ajax({
            type: "GET",
            url: "/author/data_fresh/",
            dataType: "json",
            data:{'ititle': $("#u128_input").val(),'ishenyue':$("#u127_input  option:selected").val(),
                'ibegintime':Date.parse($("#u130_input").val()),'iendtime':Date.parse($("#u163_input").val())},
            success: function (data) {
                var d = data["da"];
                var str="";
                for (var i = 0; i < d.length; i++)
                {
                    str +="<tr><td><a href=\"/author/modify/?artid="+d[i][4]+"&authorid="+d[i][5]+"\">" +d[i][0] + "</a></td><td>"+ d[i][1] + "</td><td>" + d[i][2] + "</td><td>"+d[i][3]+"</td></tr>";
                    console.log(str);
                }
                $("#artList").html(str);
            },
        });
    });
});