$(function() {
  $(document).ready(function() {
    $('.dropdown').click(function() {
      $(this).children('.dropdown__content').toggle("100", 'swing');
    });
    $(document).on('click', '.spoiler__open', function() {
      $(this).siblings('.spoiler__content').toggle("100", 'swing');
    });
  });
});
