$("#author_sel:checkbox").change(function(){
    if ($(this).is(":checked"))
        $("#author_select_list").show();
});
