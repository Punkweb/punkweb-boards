$(function() {
  $(document).ready(function() {
    // TODO: make this actually work
    // $(':not(.dropdown)').click(function() {
    //   $('.dropdown__content').hide();
    // });
    $('.dropdown').click(function() {
      $(this).children('.dropdown__content').toggle("100", "swing");
    });
    // $('.spoiler__open').click(function() {
    //   $(this).siblings('.spoiler__content').slideToggle();
    // });
    $('.spoiler__open').click(function(){
      if ($(this).siblings('.spoiler__content').css('visibility') == 'hidden') {
        $(this).siblings('.spoiler__content').css('visibility', 'visible');
        $(this).siblings('.spoiler__content').css('height', 'auto');
      } else {
        $(this).siblings('.spoiler__content').css('visibility', 'hidden');
        $(this).siblings('.spoiler__content').css('height', '0');
      }
    });
  });
});
