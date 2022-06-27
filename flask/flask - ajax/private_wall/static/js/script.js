$(document).ready(function(){

    
    $("#first_name").keyup(function(){
        var data= $("#reg-form").serialize()
        console.log(data)
        $.ajax({
            method:"POST",
            url: "/first-name",
            data:data
        }).done(function(res){
            console.log(res.split("_valid"))
            if(res.includes("_valid")){
                $("#first-name").html(res.split("_valid")).css("color", "#a5d6a7")
            }
            if(res.includes("_not_valid"))
                $("#first-name").html(res.split("_not_valid")).css("color", "#ef9a9a")
        })
    })

    $(".send-message").submit(function(){
        $.ajax({
            method:"POST",
            url: $(this).attr('action'),
            data:$(this).serialize()
        }).done((res)=>{// used arrow function to use _this of the parent
            console.log(res)
            $('#sent-number').html(`You have send ${res} messages so far:`)
            $('textarea', this).val("")
        }).fail(function(err){
        })
        return false;
    })

    $(".delete-message").submit(function(){
        $.ajax({
            method:"GET",
            url: $(this).attr('action'),
            data:$(this).serialize()
        }).done((res)=>{
            if (res ==="_danger"){
                location.href = '/danger';
            }else{
                $(this).remove()
            }
        }).fail(function(err){
        })
        return false;
    })

})