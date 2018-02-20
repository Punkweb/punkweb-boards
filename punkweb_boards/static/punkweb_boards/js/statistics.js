$(function() {
  $(document).ready(function() {
    var thisWeeksPostsChartCtx = document.getElementById('thisWeeksPostsChart').getContext('2d');
    var thisWeeksNewMembersCtx = document.getElementById('thisWeeksNewMembersChart').getContext('2d');
    var subcategoryThreadsChartCtx = document.getElementById('subcategoryThreadsChart').getContext('2d');

    var thisWeeksPostsChart = new Chart(thisWeeksPostsChartCtx, {
      type: 'line',
      data: {
        labels: [
          'Sunday', 'Monday', 'Tuesday', 'Wednesday',
          'Thursday', 'Friday', 'Saturday'
        ],
        datasets: [
          {
            label: 'New Posts',
            backgroundColor: 'rgba(255, 0, 0, .2)',
            borderColor: 'rgb(255, 0, 0)',
            data: [],
          },
          {
            label: 'New Threads',
            backgroundColor: 'rgba(0, 0, 255, .2)',
            borderColor: 'rgb(0, 0, 255)',
            data: [],
            fill: true
          },
        ]
      },
      options: {}
    });

    var thisWeeksNewMembersChart = new Chart(thisWeeksNewMembersCtx, {
      type: 'line',
      data: {
        labels: [
          'Sunday', 'Monday', 'Tuesday', 'Wednesday',
          'Thursday', 'Friday', 'Saturday'
        ],
        datasets: [
          {
            label: 'New Members',
            data: [],
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

    function getRandomColor() {
      var letters = '0123456789ABCDEF'.split('');
      var color = '#';
      for (var i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
      }
      return color;
    }

    function updateThisWeeksPostsChart(data) {
      var threads = Array(7).fill(0);
      var posts = Array(7).fill(0);
      data.new_threads_this_week.forEach(function(chunk) {
        threads[parseInt(chunk.chunk)] = chunk.count_threads;
      });
      data.new_posts_this_week.forEach(function(chunk) {
        posts[parseInt(chunk.chunk)] = chunk.count_posts;
      });
      thisWeeksPostsChart.data.datasets[1].data = threads;
      thisWeeksPostsChart.data.datasets[0].data = posts;
      thisWeeksPostsChart.update();
    }

    function updateThisWeeksNewMembersChart(data) {
      var members = Array(7).fill(0);
      data.new_members_this_week.forEach(function(chunk) {
        members[parseInt(chunk.chunk)] = chunk.count_members;
      });
      var backgroundColor = getRandomColor();
      thisWeeksNewMembersChart.data.datasets[0].data = members;
      thisWeeksNewMembersChart.data.datasets[0].backgroundColor = backgroundColor;
      thisWeeksNewMembersChart.data.datasets[0].borderColor = backgroundColor;
      thisWeeksNewMembersChart.update();
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
        updateThisWeeksPostsChart(data);
        updateThisWeeksNewMembersChart(data);
        updateSubcategoryThreadsChart(data);
      });
    }

    getStats();
  });
});
