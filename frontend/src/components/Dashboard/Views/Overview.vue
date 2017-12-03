<template>
  <div>

    <!--Stats cards-->
    <div class="row">
      <div class="col-lg-3 col-sm-6" v-for="stats in statsCards">
        <stats-card>
          <div class="icon-big text-center" :class="`icon-${stats.type}`" slot="header">
            <i :class="stats.icon"></i>
          </div>
          <div class="numbers" slot="content">
            <p>{{stats.title}}</p>
            {{stats.value}}
          </div>
          <div class="stats" slot="footer">
            <i :class="stats.footerIcon"></i> {{stats.footerText}}
          </div>
        </stats-card>
      </div>
    </div>

    <!--Charts-->
    <div class="row">

      <div class="col-md-12">
        <div class="card card-plain">
          <h2>Crawler Activity</h2>
        </div>
      </div>

      <div class="col-md-12" v-for="a in crawlerActivity">
        <div class="card crawlerActivity">
          <div class="row">
            <div class="col-xs-6">
              <h3><a :href="a.link" target="_blank">{{ a.link }}</a></h3>
            </div>

            <div class="col-xs-6 text-right">
              <h5 class="text-muted keywords">
                <template v-for="(k, i) in a.keywords">
                  {{ k }}
                  <template v-if="i != a.keywords.length - 1">,</template>
                </template>
              </h5>

              <button class="btn btn-warning btn-fill btn-wd" v-if="a.recommendations.length == 0 && !a.loading" @click="request(a)">
                Request Analysis
              </button>

              <button class="btn btn-warning btn-fill btn-wd" v-if="a.loading" disabled>Loading...</button>
            </div>

            <div class="col-xs-12" v-if="a.recommendations.length > 0 || a.loading">
              <hr>

              <div class="text-center text-muted" v-if="a.loading">
                Estimated time: 20 min
              </div>

              <ul class="list-inline recommendations" v-else>
                <li v-for="rec in a.recommendations"><a :href="rec" target="_blank">{{ rec }}</a></li>
              </ul>
            </div>

          </div>
        </div>
      </div>

    </div>

  </div>
</template>
<script>
  import StatsCard from 'components/UIComponents/Cards/StatsCard.vue'
  import ChartCard from 'components/UIComponents/Cards/ChartCard.vue'
  export default {
    components: {
      StatsCard,
      ChartCard
    },
    methods: {
      request (a) {
        a.loading = true
        setTimeout(() => {
          a.loading = false
          a.recommendations = [
            'https://hackthenorth.com',
            'https://youtube.com',
            'https://github.com'
          ]
        }, 2000)
      }
    },
    /**
     * Chart data used to render stats, charts. Should be replaced with server data
     */
    data () {
      return {
        crawlerActivity: [
          {
            link: 'https://facebook.com/posts/123',
            keywords: ['violence', 'mass', 'domestic', 'turbo', 'queen'],
            recommendations: [
              'https://hackthenorth.com',
              'https://youtube.com',
              'https://github.com'
            ],
            loading: false
          },
          {
            link: 'https://facebook.com/posts/jato',
            keywords: ['one', 'two', 'three', 'four', 'five'],
            recommendations: [],
            loading: false
          },
          {
            link: 'https://facebook.com/posts/touche',
            keywords: ['bounce', 'charisma', 'toupe', 'maestro', 'tarama'],
            recommendations: [],
            loading: false
          }
        ],
        statsCards: [
          {
            type: 'warning',
            icon: 'ti-server',
            title: 'Posts Analyzed',
            value: '117',
            footerText: 'Updated 2 mins ago',
            footerIcon: 'ti-reload'
          },
          {
            type: 'success',
            icon: 'ti-wallet',
            title: 'Startups Found',
            value: '17',
            footerText: 'Updated 2 mins ago',
            footerIcon: 'ti-reload'
          },
          {
            type: 'danger',
            icon: 'ti-pulse',
            title: 'Problems Found',
            value: '212',
            footerText: 'Updated 2 mins ago',
            footerIcon: 'ti-reload'
          },
          {
            type: 'info',
            icon: 'ti-twitter-alt',
            title: 'SM Activity',
            value: '+45',
            footerText: 'Likes, Shares, Reacts',
            footerIcon: 'ti-calendar'
          }
        ],
        usersChart: {
          data: {
            labels: ['9:00AM', '12:00AM', '3:00PM', '6:00PM', '9:00PM', '12:00PM', '3:00AM', '6:00AM'],
            series: [
              [287, 385, 490, 562, 594, 626, 698, 895, 952],
              [67, 152, 193, 240, 387, 435, 535, 642, 744],
              [23, 113, 67, 108, 190, 239, 307, 410, 410]
            ]
          },
          options: {
            low: 0,
            high: 1000,
            showArea: true,
            height: '245px',
            axisX: {
              showGrid: false
            },
            lineSmooth: this.$Chartist.Interpolation.simple({
              divisor: 3
            }),
            showLine: true,
            showPoint: false
          }
        },
        activityChart: {
          data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            series: [
              [542, 543, 520, 680, 653, 753, 326, 434, 568, 610, 756, 895],
              [230, 293, 380, 480, 503, 553, 600, 664, 698, 710, 736, 795]
            ]
          },
          options: {
            seriesBarDistance: 10,
            axisX: {
              showGrid: false
            },
            height: '245px'
          }
        },
        preferencesChart: {
          data: {
            labels: ['62%', '32%', '6%'],
            series: [62, 32, 6]
          },
          options: {}
        }
      }
    }
  }
</script>
<style scoped>
h3 {
  margin-left: 1em;
  margin-top: 0;
  margin-bottom: 0;
  height: 118px;
  line-height: 118px;
}
.keywords {
  margin-right: 1em;
}
.crawlerActivity {
  padding: 1em;
}
.btn {
  margin: 1em;
}
hr {
  margin: 1em;
}
.recommendations {
  margin-left: 1em;
}
</style>
