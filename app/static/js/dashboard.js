/**
 * LeetCode Visualiser — Dashboard Chart Renderer
 * Renders ApexCharts from JSON data injected via window.__CHART_DATA__
 */

(function () {
  'use strict';

  // Wait for DOM
  document.addEventListener('DOMContentLoaded', function () {
    var data = window.__CHART_DATA__;
    if (!data) return;

    if (window.__COMPARE_MODE__) {
      renderCompareCharts(data);
    } else {
      renderProfileCharts(data);
    }
  });

  // ==================== Helpers ====================

  function isDark() {
    return document.documentElement.getAttribute('data-theme') !== 'light';
  }

  function baseOpts() {
    var dark = isDark();
    return {
      chart: {
        background: 'transparent',
        toolbar: { show: false },
        fontFamily: 'Inter, sans-serif',
        animations: {
          enabled: true,
          easing: 'easeinout',
          speed: 400,
          dynamicAnimation: { enabled: false }
        }
      },
      theme: { mode: dark ? 'dark' : 'light' },
      grid: {
        borderColor: dark ? 'rgba(148,163,184,0.1)' : 'rgba(15,23,42,0.06)',
        strokeDashArray: 3
      },
      tooltip: {
        theme: dark ? 'dark' : 'light',
        style: { fontFamily: 'Inter, sans-serif' }
      },
      legend: {
        fontFamily: 'Inter, sans-serif',
        fontSize: '12px',
        labels: { colors: dark ? '#94a3b8' : '#475569' }
      },
      xaxis: {
        labels: {
          style: {
            colors: dark ? '#64748b' : '#334155',
            fontFamily: 'Inter, sans-serif',
            fontSize: '11px'
          }
        }
      },
      yaxis: {
        labels: {
          style: {
            colors: dark ? '#64748b' : '#94a3b8',
            fontFamily: 'Inter, sans-serif',
            fontSize: '11px'
          }
        }
      }
    };
  }

  function merge(a, b) {
    var result = {};
    for (var k in a) {
      if (a.hasOwnProperty(k)) {
        if (typeof a[k] === 'object' && a[k] !== null && !Array.isArray(a[k]) && b && typeof b[k] === 'object' && b[k] !== null && !Array.isArray(b[k])) {
          result[k] = merge(a[k], b[k]);
        } else {
          result[k] = a[k];
        }
      }
    }
    for (var k2 in b) {
      if (b.hasOwnProperty(k2) && !(k2 in result)) {
        result[k2] = b[k2];
      }
    }
    return result;
  }

  var charts = [];

  function renderChart(selector, options) {
    var el = document.querySelector(selector);
    if (!el) return null;
    el.innerHTML = '';
    var opts = merge(options, baseOpts());
    var chart = new ApexCharts(el, opts);
    chart.render();
    charts.push(chart);
    return chart;
  }

  // Global re-render for theme toggle
  window.reRenderCharts = function () {
    var data = window.__CHART_DATA__;
    if (!data) return;
    charts.forEach(function (c) { try { c.destroy(); } catch (e) {} });
    charts = [];
    if (window.__COMPARE_MODE__) {
      renderCompareCharts(data);
    } else {
      renderProfileCharts(data);
    }
  };

  // ==================== Profile Charts ====================

  function renderProfileCharts(data) {
    // Problems donut
    if (data.problems) {
      renderChart('#chart-problems', {
        chart: { type: 'donut', height: 300 },
        series: data.problems.series,
        labels: data.problems.labels,
        colors: data.problems.colors,
        plotOptions: {
          pie: {
            donut: {
              size: '60%',
              labels: {
                show: true,
                name: { show: true, fontSize: '14px', fontWeight: 600 },
                value: { show: true, fontSize: '20px', fontWeight: 700 },
                total: {
                  show: true,
                  label: 'Total',
                  fontSize: '13px',
                  fontWeight: 500,
                  formatter: function (w) {
                    return w.globals.seriesTotals.reduce(function (a, b) { return a + b; }, 0);
                  }
                }
              }
            }
          }
        },
        stroke: { width: 2, colors: [isDark() ? '#1e293b' : '#ffffff'] },
        dataLabels: {
          enabled: true,
          formatter: function (val, opts) {
            return opts.w.config.series[opts.seriesIndex];
          },
          style: { fontSize: '13px', fontWeight: 700 },
          dropShadow: { enabled: false }
        },
        legend: { position: 'bottom' }
      });
    }

    // Languages donut
    if (data.languages) {
      var langColors = ['#6366f1', '#06b6d4', '#10b981', '#f59e0b', '#f43f5e', '#8b5cf6', '#ec4899', '#14b8a6', '#f97316', '#a855f7'];
      var langTotal = data.languages.series.reduce(function (a, b) { return a + b; }, 0);
      renderChart('#chart-languages', {
        chart: { type: 'donut', height: 320 },
        series: data.languages.series,
        labels: data.languages.labels,
        colors: langColors.slice(0, data.languages.labels.length),
        plotOptions: {
          pie: {
            donut: {
              size: '65%',
              labels: {
                show: true,
                name: { show: true, fontSize: '14px', fontWeight: 600 },
                value: { show: true, fontSize: '20px', fontWeight: 700 },
                total: {
                  show: true,
                  label: 'Total',
                  fontSize: '13px',
                  fontWeight: 500,
                  formatter: function (w) {
                    return w.globals.seriesTotals.reduce(function (a, b) { return a + b; }, 0);
                  }
                }
              }
            }
          }
        },
        stroke: { width: 2, colors: [isDark() ? '#1e293b' : '#ffffff'] },
        dataLabels: { enabled: false },
        legend: {
          position: 'right',
          fontSize: '13px',
          fontWeight: 500,
          offsetY: 0,
          height: 280,
          markers: { width: 10, height: 10, radius: 3, offsetX: -4 },
          formatter: function (seriesName, opts) {
            var val = opts.w.globals.series[opts.seriesIndex];
            var pct = langTotal > 0 ? (val / langTotal * 100).toFixed(1) : '0.0';
            return seriesName + '  —  ' + val + ' (' + pct + '%)';
          },
          itemMargin: { vertical: 4 }
        }
      });
    }

    // Contest line chart
    if (data.contest) {
      var contestData = data.contest;
      var len = contestData.categories.length;
      // Show last 30 contests max for readability
      var maxShow = 30;
      var cats = len > maxShow ? contestData.categories.slice(len - maxShow) : contestData.categories;
      var ranks = len > maxShow ? contestData.rankings.slice(len - maxShow) : contestData.rankings;
      var ratings = len > maxShow ? contestData.ratings.slice(len - maxShow) : contestData.ratings;
      var deltas = len > maxShow ? contestData.rating_deltas.slice(len - maxShow) : contestData.rating_deltas;

      renderChart('#chart-contest', {
        chart: { type: 'line', height: 340 },
        series: [
          { name: 'Ranking', data: ranks },
          { name: 'Rating', data: ratings }
        ],
        xaxis: {
          categories: cats,
          labels: { rotate: -45, rotateAlways: len > 10, style: { fontSize: '10px' } },
          tooltip: { enabled: false }
        },
        yaxis: [
          {
            title: { text: 'Ranking', style: { fontSize: '12px' } },
            reversed: true,
            labels: {
              style: { fontSize: '11px' },
              formatter: function (val) { return Math.round(val); }
            }
          },
          {
            opposite: true,
            title: { text: 'Rating', style: { fontSize: '12px' } },
            labels: {
              style: { fontSize: '11px' },
              formatter: function (val) { return Math.round(val); }
            }
          }
        ],
        tooltip: {
          shared: true,
          custom: function (opts) {
            var idx = opts.dataPointIndex;
            var rank = ranks[idx];
            var rating = ratings[idx];
            var delta = deltas[idx];
            var deltaStr = delta > 0 ? '+' + delta : String(delta);
            var deltaColor = delta > 0 ? '#10b981' : delta < 0 ? '#f43f5e' : '#94a3b8';
            var dark = isDark();
            var bg = dark ? '#1e293b' : '#ffffff';
            var text = dark ? '#e2e8f0' : '#1e293b';
            var border = dark ? '#334155' : '#e2e8f0';
            return '<div style="padding:8px 12px;background:' + bg + ';border:1px solid ' + border + ';border-radius:8px;font-family:Inter,sans-serif;font-size:12px;color:' + text + ';">' +
              '<div style="font-weight:600;margin-bottom:4px;">' + cats[idx] + '</div>' +
              '<div>Ranking: <b>' + rank + '</b></div>' +
              '<div>Rating: <b>' + rating + '</b> <span style="color:' + deltaColor + ';font-weight:600;">(' + deltaStr + ')</span></div>' +
              '</div>';
          }
        },
        stroke: { width: [2, 2], curve: 'smooth' },
        colors: ['#6366f1', '#10b981'],
        markers: { size: 3, hover: { size: 5 } },
        legend: { position: 'top' }
      });
    }

    // Skills bar charts
    if (data.skills && data.skills.length > 0) {
      var container = document.getElementById('skills-charts-container');
      if (container) {
        container.innerHTML = '';
        data.skills.forEach(function (skill, index) {
          // Take top 15 for readability
          var maxBars = 15;
          var cats = skill.categories.slice(0, maxBars);
          var vals = skill.series.slice(0, maxBars);

          var cardDiv = document.createElement('div');
          cardDiv.className = 'card chart-card';
          cardDiv.innerHTML = '<p class="chart-title">' + escapeHtml(skill.title) + '</p><div class="chart-wrapper" id="chart-skills-' + index + '"></div>';
          container.appendChild(cardDiv);

          renderChart('#chart-skills-' + index, {
            chart: { type: 'bar', height: Math.min(300, 40 + cats.length * 22) },
            series: [{ name: 'Problems Solved', data: vals }],
            xaxis: { categories: cats },
            plotOptions: {
              bar: {
                horizontal: true,
                borderRadius: 4,
                barHeight: '60%',
                dataLabels: { position: 'top' }
              }
            },
            colors: ['#6366f1'],
            dataLabels: {
              enabled: true,
              offsetX: 20,
              style: { fontSize: '11px', fontWeight: 600, colors: [isDark() ? '#e2e8f0' : '#1e293b'] }
            }
          });
        });
      }
    }
  }

  // ==================== Compare Charts ====================

  function renderCompareCharts(data) {
    // Problem comparison grouped bar
    if (data.problems) {
      renderChart('#chart-compare-problems', {
        chart: { type: 'bar', height: 300 },
        series: [
          { name: data.problems.username1, data: data.problems.series1 },
          { name: data.problems.username2, data: data.problems.series2 }
        ],
        xaxis: { categories: data.problems.labels },
        colors: ['#6366f1', '#f59e0b'],
        plotOptions: {
          bar: { borderRadius: 6, columnWidth: '55%' }
        },
        dataLabels: {
          enabled: true,
          style: { fontSize: '12px', fontWeight: 700 }
        }
      });
    }

    // Skills comparison
    if (data.skills && data.skills.length > 0) {
      var container = document.getElementById('compare-skills-container');
      if (container) {
        container.innerHTML = '';
        data.skills.forEach(function (skill, index) {
          var maxBars = 15;
          var cats = skill.categories.slice(0, maxBars);
          var s1 = skill.series1.slice(0, maxBars);
          var s2 = skill.series2.slice(0, maxBars);

          var cardDiv = document.createElement('div');
          cardDiv.className = 'card chart-card';
          cardDiv.innerHTML = '<p class="chart-title">' + escapeHtml(skill.title) + '</p><div class="chart-wrapper" id="chart-compare-skills-' + index + '"></div>';
          container.appendChild(cardDiv);

          renderChart('#chart-compare-skills-' + index, {
            chart: { type: 'bar', height: Math.min(320, 60 + cats.length * 24) },
            series: [
              { name: skill.username1, data: s1 },
              { name: skill.username2, data: s2 }
            ],
            xaxis: { categories: cats },
            plotOptions: {
              bar: {
                horizontal: true,
                borderRadius: 3,
                barHeight: '55%'
              }
            },
            colors: ['#6366f1', '#f59e0b'],
            dataLabels: {
              enabled: true,
              style: { fontSize: '10px', fontWeight: 600 }
            }
          });
        });
      }
    }

    // Contest comparison — line chart (ratings over common contests)
    if (data.contest) {
      var cd = data.contest;
      var maxShow = 30;
      var len = cd.categories.length;
      var cats = len > maxShow ? cd.categories.slice(len - maxShow) : cd.categories;
      var rat1 = len > maxShow ? cd.ratings1.slice(len - maxShow) : cd.ratings1;
      var rat2 = len > maxShow ? cd.ratings2.slice(len - maxShow) : cd.ratings2;

      renderChart('#chart-compare-contest', {
        chart: { type: 'line', height: 340 },
        series: [
          { name: cd.username1 + ' Rating', data: rat1 },
          { name: cd.username2 + ' Rating', data: rat2 }
        ],
        xaxis: {
          categories: cats,
          labels: { rotate: -45, rotateAlways: len > 8, style: { fontSize: '10px' } },
          tooltip: { enabled: false }
        },
        yaxis: {
          title: { text: 'Rating', style: { fontSize: '12px' } },
          labels: {
            style: { fontSize: '11px' },
            formatter: function (val) { return Math.round(val); }
          }
        },
        stroke: { width: [2, 2], curve: 'smooth' },
        colors: ['#6366f1', '#f59e0b'],
        markers: { size: 3, hover: { size: 5 } },
        legend: { position: 'top' },
        tooltip: {
          shared: true,
          custom: function (opts) {
            var idx = opts.dataPointIndex;
            var r1 = rat1[idx];
            var r2 = rat2[idx];
            var dark = isDark();
            var bg = dark ? '#1e293b' : '#ffffff';
            var text = dark ? '#e2e8f0' : '#1e293b';
            var border = dark ? '#334155' : '#e2e8f0';
            return '<div style="padding:8px 12px;background:' + bg + ';border:1px solid ' + border + ';border-radius:8px;font-family:Inter,sans-serif;font-size:12px;color:' + text + ';">' +
              '<div style="font-weight:600;margin-bottom:4px;">' + cats[idx] + '</div>' +
              '<div><span style="color:#6366f1;">●</span> ' + cd.username1 + ': <b>' + r1 + '</b></div>' +
              '<div><span style="color:#f59e0b;">●</span> ' + cd.username2 + ': <b>' + r2 + '</b></div>' +
              '</div>';
          }
        }
      });
    }
  }

  function escapeHtml(str) {
    var div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  }

})();
