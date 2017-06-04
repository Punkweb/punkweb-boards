$(function() {
  $(document).ready(function() {
    $('.post-editor').sceditor({
      plugins: 'bbcode',
      toolbar: 'bold,italic,underline,strike|bulletlist,orderedlist,center,horizontalrule|font,size,color,quote,link,image,emoticon|date,time|source,maximize,removeformat',
      style: '/static/scss/_editor.min.css',
      fonts: 'Arial,Arial Black,Comic Sans MS,Courier New,Georgia,Impact,Sans-serif,Serif,Storybook,Times New Roman,Trebuchet MS,Truckin,Verdana',
      autoExpand: true,
      emoticonsEnabled: true,
      emoticonsCompat: true,
      emoticonsRoot: '/media/precise_bbcode/smilies/',
      emoticons: {
        dropdown: {
          ":gd:": "gd.png",
          ":gimli:": "gimli.jpg",
          ":cool:": "cool.png",
          ":tool:": "tool.jpg",
          ":git:": "git.png"
        },
        hidden: {}
      }
    });
  });
});
