/**
 * LeetCode Visualiser — Premium Dashboard Chart Renderer & Animations
 * Renders ApexCharts from JSON data injected via window.__CHART_DATA__
 * Implements Motion One for 60fps Framer Motion style animations.
 */

(function () {
  'use strict';

  // Wait for DOM
  document.addEventListener('DOMContentLoaded', function () {
    var data = window.__CHART_DATA__;
    
    // 1. Initialize Animations
    initAnimations();

    if (!data) return;

    // 2. Initialize Charts
    if (window.__COMPARE_MODE__) {
      renderCompareCharts(data);
    } else {
      renderProfileCharts(data);
    }
  });

  // ==================== Animations ====================
  function initAnimations() {
    // --- Counter Animations (No external dependencies) ---
    const counters = document.querySelectorAll('.counter-animate');
    counters.forEach(counter => {
      const rawTarget = counter.getAttribute('data-target');
      const target = parseFloat(rawTarget);
      
      if (isNaN(target)) {
        counter.textContent = rawTarget || '0';
        return;
      }

      const duration = 1500;
      const startTime = performance.now();
      
      function updateCounter(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        const ease = progress === 1 ? 1 : 1 - Math.pow(2, -10 * progress);
        const currentVal = target * ease;
        
        if (target % 1 !== 0) {
          counter.textContent = currentVal.toFixed(1);
        } else {
          counter.textContent = Math.round(currentVal).toLocaleString();
        }
        
        if (progress < 1) {
          requestAnimationFrame(updateCounter);
        } else {
          if (target % 1 !== 0) {
            counter.textContent = target.toFixed(1);
          } else {
            counter.textContent = target.toLocaleString();
          }
        }
      }
      requestAnimationFrame(updateCounter);
    });

    // --- Motion One Animations ---
    if (typeof motion === 'undefined' && typeof Motion === 'undefined') return;
    const motionLib = typeof motion !== 'undefined' ? motion : Motion;
    const { animate, stagger, inView } = motionLib;

    // --- Landing Page Animations ---
    const heroTitle = document.getElementById('hero-title');
    if (heroTitle) {
      animate(heroTitle, { opacity: [0, 1], y: [40, 0] }, { duration: 0.8, easing: [0.22, 1, 0.36, 1] });
      animate('#hero-pill', { opacity: [0, 1], y: [20, 0], scale: [0.9, 1] }, { duration: 0.6, delay: 0.1 });
      animate('#hero-subtitle', { opacity: [0, 1], y: [20, 0] }, { duration: 0.6, delay: 0.2 });
      animate('#hero-form', { opacity: [0, 1], y: [20, 0] }, { duration: 0.6, delay: 0.3 });
      animate('#hero-actions', { opacity: [0, 1], y: [20, 0] }, { duration: 0.6, delay: 0.4 });
    }

    const featureCards = document.querySelectorAll('.feature-card');
    if (featureCards.length > 0) {
      inView('#features-section', () => {
        animate(
          featureCards,
          { opacity: [0, 1], y: [40, 0] },
          { delay: stagger(0.15), duration: 0.6, easing: [0.22, 1, 0.36, 1] }
        );
      });
    }

    // --- Profile Dashboard Animations ---
    const profileHeader = document.getElementById('profile-header');
    if (profileHeader) {
      animate(profileHeader, { opacity: [0, 1], scale: [0.95, 1], y: [30, 0] }, { duration: 0.7, easing: [0.22, 1, 0.36, 1] });
    }

    const statCards = document.querySelectorAll('.stat-card');
    if (statCards.length > 0) {
      animate(
        statCards,
        { opacity: [0, 1], y: [30, 0] },
        { delay: stagger(0.1, { start: 0.2 }), duration: 0.6, easing: [0.22, 1, 0.36, 1] }
      );
    }

    const chartCards = document.querySelectorAll('.chart-card');
    if (chartCards.length > 0) {
      animate(
        chartCards,
        { opacity: [0, 1], y: [40, 0] },
        { delay: stagger(0.15, { start: 0.4 }), duration: 0.6, easing: [0.22, 1, 0.36, 1] }
      );
    }

    // --- Compare Page (Battle Mode) Animations ---
    const battleHeader = document.getElementById('battle-header');
    if (battleHeader) {
      animate(battleHeader, { opacity: [0, 1], y: [40, 0] }, { duration: 0.8, easing: [0.22, 1, 0.36, 1] });
    }

    const battleCards = document.getElementById('battle-cards');
    if (battleCards && battleCards.children.length > 0) {
      animate(
        battleCards.children,
        { opacity: [0, 1], scale: [0.9, 1], x: (i) => (i === 0 ? [-50, 0] : [50, 0]) },
        { delay: stagger(0.2, { start: 0.3 }), duration: 0.7, easing: [0.22, 1, 0.36, 1] }
      );
    }

    const battleCharts = document.getElementById('battle-charts');
    if (battleCharts) {
      animate(battleCharts, { opacity: [0, 1], y: [40, 0] }, { duration: 0.8, delay: 0.6, easing: [0.22, 1, 0.36, 1] });
    }

  }

  // ==================== Chart Helpers ====================
  function isDark() {
    return document.documentElement.getAttribute('data-theme') !== 'light';
  }

  function baseOpts() {
    var dark = isDark();
    // Vercel/Linear dark theme matching
    var gridBorder = dark ? 'rgba(255,255,255,0.06)' : 'rgba(0,0,0,0.06)';
    var textPrim = dark ? '#ededed' : '#09090b';
    var textSec = dark ? '#a1a1aa' : '#52525b';

    return {
      chart: {
        background: 'transparent',
        toolbar: { show: false },
        fontFamily: 'Inter, sans-serif',
        animations: {
          enabled: true,
          easing: 'easeinout',
          speed: 600,
          dynamicAnimation: { enabled: true, speed: 300 }
        }
      },
      theme: { mode: dark ? 'dark' : 'light' },
      grid: {
        borderColor: gridBorder,
        strokeDashArray: 4,
        padding: { top: 0, right: 10, bottom: 0, left: 10 }
      },
      tooltip: {
        theme: dark ? 'dark' : 'light',
        style: { fontFamily: 'Inter, sans-serif', fontSize: '13px' }
      },
      legend: {
        fontFamily: 'Inter, sans-serif',
        fontSize: '12px',
        fontWeight: 500,
        labels: { colors: textSec },
        markers: { radius: 12 }
      },
      xaxis: {
        labels: {
          style: {
            colors: textSec,
            fontFamily: 'Inter, sans-serif',
            fontSize: '11px',
            fontWeight: 500
          }
        },
        axisBorder: { show: false },
        axisTicks: { show: false }
      },
      yaxis: {
        labels: {
          style: {
            colors: textSec,
            fontFamily: 'Inter, sans-serif',
            fontSize: '11px',
            fontWeight: 500
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
    var dark = isDark();
    var strokeColor = dark ? '#0a0a0a' : '#ffffff';

    // Problems donut
    if (data.problems) {
      renderChart('#chart-problems', {
        chart: { type: 'donut', height: 280 },
        series: data.problems.series,
        labels: data.problems.labels,
        colors: ['#00b8a3', '#ffc01e', '#ef4743'], // Easy, Medium, Hard
        plotOptions: {
          pie: {
            expandOnClick: true,
            donut: {
              size: '70%',
              labels: {
                show: true,
                name: { show: true, fontSize: '13px', fontWeight: 500, color: dark ? '#a1a1aa' : '#52525b' },
                value: { show: true, fontSize: '24px', fontWeight: 700, color: dark ? '#ededed' : '#09090b', fontFamily: 'Outfit, sans-serif' },
                total: {
                  show: true,
                  label: 'Total',
                  color: dark ? '#a1a1aa' : '#52525b',
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
        stroke: { width: 3, colors: [strokeColor] },
        dataLabels: {
          enabled: true,
          formatter: function (val, opts) {
            return opts.w.config.series[opts.seriesIndex];
          },
          style: { fontSize: '14px', fontWeight: 700, colors: ['#ffffff'] },
          dropShadow: { enabled: false }
        },
        legend: { position: 'bottom', itemMargin: { horizontal: 10, vertical: 5 } }
      });
    }

    // Languages donut
    if (data.languages) {
      var langColors = ['#6366f1', '#06b6d4', '#10b981', '#f59e0b', '#f43f5e', '#8b5cf6', '#ec4899', '#14b8a6', '#f97316', '#a855f7'];
      var langTotal = data.languages.series.reduce(function (a, b) { return a + b; }, 0);
      renderChart('#chart-languages', {
        chart: { type: 'donut', height: 280 },
        series: data.languages.series,
        labels: data.languages.labels,
        colors: langColors.slice(0, data.languages.labels.length),
        plotOptions: {
          pie: {
            donut: {
              size: '70%',
              labels: {
                show: true,
                name: { show: true, fontSize: '13px', fontWeight: 500, color: dark ? '#a1a1aa' : '#52525b' },
                value: { show: true, fontSize: '24px', fontWeight: 700, color: dark ? '#ededed' : '#09090b', fontFamily: 'Outfit, sans-serif' },
                total: {
                  show: true,
                  label: 'Total Submissions',
                  fontSize: '12px',
                  fontWeight: 500,
                  color: dark ? '#a1a1aa' : '#52525b',
                  formatter: function (w) {
                    return w.globals.seriesTotals.reduce(function (a, b) { return a + b; }, 0);
                  }
                }
              }
            }
          }
        },
        stroke: { width: 3, colors: [strokeColor] },
        dataLabels: { enabled: false },
        legend: {
          position: 'right',
          fontSize: '12px',
          fontWeight: 500,
          labels: { colors: dark ? '#a1a1aa' : '#52525b' },
          markers: { radius: 12 },
          height: 260,
          formatter: function (seriesName, opts) {
            var val = opts.w.globals.series[opts.seriesIndex];
            var pct = langTotal > 0 ? (val / langTotal * 100).toFixed(1) : '0.0';
            return seriesName + ' — ' + val + ' (' + pct + '%)';
          },
          itemMargin: { vertical: 4 }
        }
      });
    }

    // Contest line chart
    if (data.contest) {
      var contestData = data.contest;
      var len = contestData.categories.length;
      var maxShow = 40;
      var cats = len > maxShow ? contestData.categories.slice(len - maxShow) : contestData.categories;
      var ranks = len > maxShow ? contestData.rankings.slice(len - maxShow) : contestData.rankings;
      var ratings = len > maxShow ? contestData.ratings.slice(len - maxShow) : contestData.ratings;
      var deltas = len > maxShow ? contestData.rating_deltas.slice(len - maxShow) : contestData.rating_deltas;

      renderChart('#chart-contest', {
        chart: { type: 'area', height: 320 },
        series: [
          { name: 'Rating', data: ratings }
        ],
        fill: {
          type: 'gradient',
          gradient: {
            shadeIntensity: 1,
            opacityFrom: 0.4,
            opacityTo: 0.05,
            stops: [0, 100]
          }
        },
        xaxis: {
          categories: cats,
          labels: { show: false }, // Hide x-axis labels for a cleaner look like Vercel
          tooltip: { enabled: false }
        },
        yaxis: [
          {
            title: { text: 'Contest Rating', style: { fontSize: '12px', fontWeight: 500 } },
            labels: {
              style: { fontSize: '11px', colors: dark ? '#a1a1aa' : '#52525b' },
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
            var deltaColor = delta > 0 ? '#10b981' : delta < 0 ? '#ef4743' : '#a1a1aa';
            
            return '<div style="padding:12px;font-family:Inter,sans-serif;">' +
              '<div style="font-size:11px;color:#a1a1aa;margin-bottom:8px;font-weight:600;text-transform:uppercase;">' + cats[idx] + '</div>' +
              '<div style="font-size:24px;font-weight:700;font-family:Outfit,sans-serif;line-height:1;margin-bottom:8px;">' + rating + ' <span style="font-size:14px;color:' + deltaColor + ';font-family:Inter,sans-serif;vertical-align:middle;">(' + deltaStr + ')</span></div>' +
              '<div style="font-size:12px;color:#a1a1aa;font-weight:500;">Rank: <span style="color:#ededed;font-weight:600;">' + rank.toLocaleString() + '</span></div>' +
              '</div>';
          }
        },
        stroke: { width: 3, curve: 'smooth' },
        colors: ['#6366f1'],
        markers: { size: 0, hover: { size: 6, strokeWidth: 3, strokeColors: strokeColor } },
        legend: { show: false }
      });
    }

    // Skills bar charts
    if (data.skills && data.skills.length > 0) {
      var container = document.getElementById('skills-charts-container');
      if (container) {
        container.innerHTML = '';
        data.skills.forEach(function (skill, index) {
          var maxBars = 12;
          var cats = skill.categories.slice(0, maxBars);
          var vals = skill.series.slice(0, maxBars);

          var cardDiv = document.createElement('div');
          cardDiv.className = 'card chart-card';
          cardDiv.innerHTML = '<div class="chart-header"><p class="chart-title">' + escapeHtml(skill.title) + '</p></div><div class="chart-wrapper" id="chart-skills-' + index + '"></div>';
          container.appendChild(cardDiv);

          renderChart('#chart-skills-' + index, {
            chart: { type: 'bar', height: Math.max(200, cats.length * 30) },
            series: [{ name: 'Problems', data: vals }],
            xaxis: { categories: cats },
            plotOptions: {
              bar: {
                horizontal: true,
                borderRadius: 4,
                barHeight: '40%',
              }
            },
            colors: ['#06b6d4'],
            dataLabels: {
              enabled: true,
              offsetX: 24,
              style: { fontSize: '11px', fontWeight: 600, colors: [dark ? '#ededed' : '#09090b'] }
            }
          });
        });
      }
    }
  }

  // ==================== Compare Charts ====================

  function renderCompareCharts(data) {
    var dark = isDark();

    // Problem comparison (Radar Chart for Battle Mode)
    if (data.problems) {
      renderChart('#chart-compare-problems', {
        chart: { type: 'radar', height: 360, toolbar: { show: false } },
        series: [
          { name: data.problems.username1, data: data.problems.series1 },
          { name: data.problems.username2, data: data.problems.series2 }
        ],
        labels: data.problems.labels,
        colors: ['#6366f1', '#f59e0b'],
        stroke: { width: 2, curve: 'smooth' },
        fill: { opacity: 0.2 },
        markers: { size: 4, hover: { size: 7 } },
        yaxis: { show: false }, // Hide internal y-axis for cleaner look
        xaxis: {
          labels: {
            style: {
              colors: dark ? '#a1a1aa' : '#52525b',
              fontSize: '12px',
              fontFamily: 'Inter, sans-serif',
              fontWeight: 600
            }
          }
        },
        dataLabels: { enabled: false },
        legend: { position: 'top', horizontalAlign: 'center', fontSize: '14px', fontWeight: 600 }
      });
    }

    // Skills comparison
    if (data.skills && data.skills.length > 0) {
      var container = document.getElementById('compare-skills-container');
      if (container) {
        container.innerHTML = '';
        data.skills.forEach(function (skill, index) {
          var maxBars = 12;
          var cats = skill.categories.slice(0, maxBars);
          var s1 = skill.series1.slice(0, maxBars);
          var s2 = skill.series2.slice(0, maxBars);

          var cardDiv = document.createElement('div');
          cardDiv.className = 'card chart-card';
          cardDiv.innerHTML = '<div class="chart-header"><p class="chart-title">' + escapeHtml(skill.title) + '</p></div><div class="chart-wrapper" id="chart-compare-skills-' + index + '"></div>';
          container.appendChild(cardDiv);

          renderChart('#chart-compare-skills-' + index, {
            chart: { type: 'bar', height: Math.max(240, cats.length * 35) },
            series: [
              { name: skill.username1, data: s1 },
              { name: skill.username2, data: s2 }
            ],
            xaxis: { categories: cats },
            plotOptions: {
              bar: {
                horizontal: true,
                borderRadius: 3,
                barHeight: '60%'
              }
            },
            colors: ['#6366f1', '#f59e0b'],
            dataLabels: { enabled: false },
            legend: { position: 'top', horizontalAlign: 'right' }
          });
        });
      }
    }

    // Contest comparison
    if (data.contest) {
      var cd = data.contest;
      var maxShow = 40;
      var len = cd.categories.length;
      var cats = len > maxShow ? cd.categories.slice(len - maxShow) : cd.categories;
      var rat1 = len > maxShow ? cd.ratings1.slice(len - maxShow) : cd.ratings1;
      var rat2 = len > maxShow ? cd.ratings2.slice(len - maxShow) : cd.ratings2;

      renderChart('#chart-compare-contest', {
        chart: { type: 'line', height: 360 },
        series: [
          { name: cd.username1, data: rat1 },
          { name: cd.username2, data: rat2 }
        ],
        xaxis: {
          categories: cats,
          labels: { show: false },
          tooltip: { enabled: false }
        },
        yaxis: {
          title: { text: 'Rating', style: { fontSize: '12px', fontWeight: 500 } },
          labels: {
            style: { fontSize: '11px', colors: dark ? '#a1a1aa' : '#52525b' },
            formatter: function (val) { return Math.round(val); }
          }
        },
        stroke: { width: 3, curve: 'smooth' },
        colors: ['#6366f1', '#f59e0b'],
        markers: { size: 0, hover: { size: 6 } },
        legend: { position: 'top', horizontalAlign: 'right' },
        tooltip: {
          shared: true,
          theme: dark ? 'dark' : 'light'
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
