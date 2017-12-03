<template>
    <div class="row">
      <div class="col-lg-4 col-md-5">
        <div class="card">
          <div class="header">
            <h4 class="title">Current Activity</h4>
          </div>

          <div class="content text-center text-warning">
            <h5 v-if="isIdle">Crawler is idle</h5>
            <h5 v-else class="text-danger">Crawler is currently searching</h5>
            <button type="button" class="btn btn-sm btn-icon btn-warning" @click="refresh"><i class="fa fa-refresh"></i></button>
          </div>

        </div>
      </div>
      <div class="col-lg-8 col-md-7">
        <div class="card">
          <div class="header">
            <h4 class="title">Start Activity</h4>
          </div>

          <div class="content">
            <form>
              <div class="row">

                <div class="col-xs-10 col-xs-offset-1">
                  <div class="form-group">
                    <label>Keywords</label>
                    <input type="text" class="form-control border-input" placeholder="Enter keywords to search here" v-model="newActivity.keywords">
                  </div>

                  <div class="form-group">
                    <label>Number of pages</label>
                    <input type="number" class="form-control border-input" placeholder="Choose number of pages to search" v-model="newActivity.pages">
                    <p class="form-text text-muted">More pages may give better results, but will take longer to crawl.</p>
                  </div>
                </div>

              </div>

              <p class="text-danger text-center" v-if="!isIdle">Please wait for the crawler to become idle before starting a new activity.</p>

              <div class="text-center">
                <button type="submit" class="btn btn-warning btn-fill btn-wd" @click.prevent="startCrawler" :disabled="!isIdle">
                  Start Activity
                </button>
              </div>
              <div class="clearfix"></div>
            </form>
          </div>
        </div>
      </div>
    </div>
</template>
<script>
  import EditProfileForm from './UserProfile/EditProfileForm.vue'
  import UserCard from './UserProfile/UserCard.vue'
  import MembersCard from './UserProfile/MembersCard.vue'
  import axios from 'axios'
  export default {
    components: {
      EditProfileForm,
      UserCard,
      MembersCard
    },
    created () {
      this.refresh()
    },
    methods: {
      startCrawler () {
        if (!this.isIdle) return

        if (this.newActivity.keywords.length > 0) {
          // Perform keyword search
          let pages = 1
          if (this.newActivity.pages > 1) {
            pages = this.newActivity.pages
          }

          let endpoint = 'http://67.205.156.166:6996/crawl/'
          endpoint += encodeURIComponent(this.newActivity.keywords)
          endpoint += '/' + pages
          axios.post(endpoint, { withCredentials: true })
          this.isIdle = false
          this.currentActivity = this.newActivity.keywords
          this.newActivity.keywords = ''
          this.newActivity.pages = 0
        }
      },
      refresh () {
        // Create the XHR object.
        function createCORSRequest (method, url) {
          var xhr = new XMLHttpRequest()
          if ('withCredentials' in xhr) {
            // XHR for Chrome/Firefox/Opera/Safari.
            xhr.open(method, url, true)
          } else if (typeof XDomainRequest !== 'undefined') {
            // XDomainRequest for IE.
            xhr = new XDomainRequest()
            xhr.open(method, url)
          } else {
            // CORS not supported.
            xhr = null
          }
          return xhr
        }

        var url = 'http://morrisjchen.com:4242/crawl_status'

        var xhr = createCORSRequest('GET', url)
        if (!xhr) {
          alert('CORS not supported')
          return
        }

        // Response handlers.
        xhr.onload = () => {
          var text = xhr.responseText
          console.log(text)
          var json = JSON.parse(text)
          console.log(json)
          if (json.status === 'busy') {
            this.isIdle = false
          } else {
            this.isIdle = true
          }
        }

        xhr.onerror = function () {
          alert('Woops, there was an error making the request.')
        }

        xhr.send()
      }
    },
    data () {
      return {
        isIdle: true,
        currentActivity: 'trump',
        newActivity: {
          keywords: '',
          pages: 0
        }
      }
    }
  }

</script>
<style scoped>
.or {
  height: 93px;
  line-height: 93px;
}
[type="submit"] {
  margin-top: 1em;
  margin-bottom: 2em;
}
</style>
