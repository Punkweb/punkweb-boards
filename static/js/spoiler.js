$(function() {
  $(document).ready(function() {
    $('.dropdown').click(function() {
      $(this).children('.dropdown__content').toggle();
    });
    $('.spoiler__open').click(function() {
      $(this).siblings('.spoiler__content').toggle();
    });
  });
});
