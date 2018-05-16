$(function() {
  $(document).ready(function() {
    $('.post-editor').sceditor({
      format: 'bbcode',
      toolbar: 'bold,italic,underline,strike|bulletlist,orderedlist,center,horizontalrule|font,size,color,quote,code,link,image,emoticon|date,time|source,maximize,removeformat',
      style: '/static/punkweb_boards/scss/editor.css',
      fonts: 'Inconsolata,Courier New,Open Sans,Montserrat,Sans-serif,Serif,Storybook,Times New Roman,Winterland',
      autoExpand: true,
      emoticonsEnabled: false,
      emoticonsCompat: true,
      emoticonsRoot: '/media/precise_bbcode/smilies/',
      emoticons: {
        ':gd:': 'gd.jpg',
      }
    });
  });
});
