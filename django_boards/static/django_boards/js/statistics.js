$(function() {
  $(document).ready(function() {
    var dowPostsChartCtx = document.getElementById('dowPostsChart').getContext('2d');
    var subcategoryThreadsChartCtx = document.getElementById('subcategoryThreadsChart').getContext('2d');

    var dowPostsChart = new Chart(dowPostsChartCtx, {
      type: 'line',
      data: {
        labels: [
          'Sunday', 'Monday', 'Tuesday', 'Wednesday',
          'Thursday', 'Friday', 'Saturday'
        ],
        datasets: [
          {
            label: "Posts",
            backgroundColor: 'rgba(255, 0, 0, .2)',
            borderColor: 'rgb(255, 0, 0)',
            data: [],
          },
          {
            label: "Threads",
            backgroundColor: 'rgba(0, 0, 255, .2)',
            borderColor: 'rgb(0, 0, 255)',
            data: [],
            fill: true
          },
        ]
      },
      options: {}
    });

    var subcategoryThreadsChart = new Chart(subcategoryThreadsChartCtx,{
      type: 'pie',
      data: {
        datasets: [{
          data: []
        }],
        labels: []
      },
      options: {}
    });

    function updateDowPostsChart(data) {
      var threads = Array(7).fill(0);
      var posts = Array(7).fill(0);
      data.threads_by_dow.forEach(function(chunk) {
        threads[parseInt(chunk.chunk)] = chunk.count_threads;
      });
      data.posts_by_dow.forEach(function(chunk) {
        posts[parseInt(chunk.chunk)] = chunk.count_posts;
      });
      dowPostsChart.data.datasets[1].data = threads;
      dowPostsChart.data.datasets[0].data = posts;
      dowPostsChart.update();
    }

    function getRandomColor() {
      var letters = '0123456789ABCDEF'.split('');
      var color = '#';
      for (var i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
      }
      return color;
    }

    function updateSubcategoryThreadsChart(data) {
      var subcategories = [];
      var labels = [];
      data.threads_in_subcategories.forEach(function(chunk) {
        if (chunk.count_threads > 0) {
          subcategories.push(chunk.count_threads);
          labels.push(chunk.name);
        }
      });
      var backgroundColors = Array(subcategories.length);
      for (var i = 0; i < backgroundColors.length; i++) {
        backgroundColors[i] = getRandomColor();
      }
      subcategoryThreadsChart.data.datasets[0].data = subcategories;
      subcategoryThreadsChart.data.datasets[0].backgroundColor = backgroundColors;
      subcategoryThreadsChart.data.labels = labels;
      subcategoryThreadsChart.update();
    }

    function getStats() {
      $.get('/board/api/statistics/', function(data) {
        updateDowPostsChart(data);
        updateSubcategoryThreadsChart(data);
      });
    }

    getStats();
  });
});
