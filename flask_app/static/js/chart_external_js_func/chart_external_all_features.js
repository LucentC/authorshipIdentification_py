//Drag&Drop feature
$(function() {
    $( "#x-axis, #y-axis, #z-axis, #sortable" ).sortable({
      connectWith: ".connectedSortable",
      revert: true,
    receive: function(event, ui) {
            var $this = $(this);
            if ($this.children('li').length > 1 && $this.attr('id')!="sortable1") {
                $(ui.sender).sortable('cancel');
            }
        }
    }).disableSelection();

    $( "#sortable1" ).sortable({
      connectWith: ".connectedSortable",
      revert: true
    }).disableSelection();

});

