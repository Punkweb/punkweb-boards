$(function() {
  $(document).ready(function() {
    $('.spoiler__open').click(function() {
      $(this).siblings('.spoiler__content').toggle();
    });
  });
});
