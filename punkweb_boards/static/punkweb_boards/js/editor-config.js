$(function() {
  $(document).ready(function() {
    $('.post-editor').sceditor({
      format: 'bbcode',
      icons: 'material',
      toolbar: 'bold,italic,underline,strike|bulletlist,orderedlist,center,horizontalrule|font,size,color,quote,code,link,image|date,time|source,maximize,removeformat',
      style: '/static/punkweb_boards/scss/editor.css',
      fonts: 'Arial,Arial Black,Comic Sans MS,Inconsolata,Courier New,Georgia,Impact,Open Sans,Montserrat,Sans-serif,Serif,Times New Roman,Trebuchet MS,Verdana',
      autoExpand: true,
      emoticonsEnabled: false,
      emoticonsCompat: true,
      emoticonsRoot: '/media/precise_bbcode/smilies/'
    });
  });
});
