<template>
    <div class="row">
      <div class="col-xs-12">
        <div class="card">
          <div class="header">
            <h4 class="title">Run Social Media Tests</h4>
          </div>

          <div class="content">
            <form>
              <div class="row">

                <div class="col-xs-4">
                  <div class="form-group">
                    <label>Select Startup</label>
                    <select class="form-control border-input" v-model="link">
                      <template v-for="a in crawlerActivity">
                        <option v-for="link in a.recommendations">{{ link }}</option>
                      </template>
                    </select>
                  </div>
                </div>

                <div class="col-xs-8">
                  <div class="form-group">
                    <label>Description</label>
                    <input type="text" class="form-control border-input" placeholder="Enter description for post" v-model="description">
                  </div>
                </div>

              </div>

              <div>
                <button type="submit" class="btn btn-warning btn-fill btn-wd" @click.prevent="startActivity">
                  Start Activity
                </button>
              </div>
              <div class="clearfix"></div>
            </form>
          </div>

          <hr>

          <h4 v-for="post in fbStatus"><a :href="post.link" target="_blank">{{ post.description }}</a> - {{ post.likes }} likes</h4>

        </div>
      </div>
    </div>
</template>
<script>
  import EditProfileForm from './UserProfile/EditProfileForm.vue'
  import UserCard from './UserProfile/UserCard.vue'
  import MembersCard from './UserProfile/MembersCard.vue'
  export default {
    components: {
      EditProfileForm,
      UserCard,
      MembersCard
    },
    methods: {
      startActivity () {
        // Create the XHR object.
        function createCORSRequest (method, url, data) {
          var xhr = new XMLHttpRequest()
          if ('withCredentials' in xhr) {
            // XHR for Chrome/Firefox/Opera/Safari.
            xhr.open(method, url, true)
            xhr.setRequestHeader('Content-Type', 'application/json')
            xhr.send(JSON.stringify(data))
          } else if (typeof XDomainRequest !== 'undefined') {
            // XDomainRequest for IE.
            xhr = new XDomainRequest()
            xhr.open(method, url)
            xhr.setRequestHeader('Content-Type', 'application/json')
            xhr.send(JSON.stringify(data))
          } else {
            // CORS not supported.
            xhr = null
          }
          return xhr
        }

        var url = 'http://morrisjchen.com:4242/fb_new_post'

        var xhr = createCORSRequest('POST', url, {
          description: this.description,
          link: this.link,
          id: Math.round(Math.random() * 1000000)
        })
        if (!xhr) {
          alert('CORS not supported')
          return
        }

        // Response handlers.
        xhr.onerror = function () {
          alert('Woops, there was an error making the request.')
        }

        xhr.send()
      }
    },
    created () {
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

      var url = 'http://morrisjchen.com:4242/get_gui'

      var xhr = createCORSRequest('GET', url)
      if (!xhr) {
        alert('CORS not supported')
        return
      }

      // Response handlers.
      xhr.onload = () => {
        var text = xhr.responseText
        var json = JSON.parse(text)

        this.crawlerActivity = json.map(act => {
          return {
            id: act._id,
            tag: act.tag,
            keywords: act.keywords,
            names: act.names,
            recommendations: act.links === null ? ['http://hackthenorth.com'] : act.links,
            loading: false
          }
        })
      }

      xhr.onerror = function () {
        alert('Woops, there was an error making the request.')
      }

      xhr.send()

      // FB status

      url = 'http://morrisjchen.com:4242/get_fb_status'

      var xhr2 = createCORSRequest('GET', url)
      if (!xhr2) {
        alert('CORS not supported')
        return
      }

      // Response handlers.
      xhr2.onload = () => {
        var text = xhr2.responseText
        var json = JSON.parse(text)
        this.fbStatus = json
      }

      xhr2.onerror = function () {
        alert('Woops, there was an error making the request.')
      }

      xhr2.send()
    },
    data () {
      return {
        crawlerActivity: {},
        description: '',
        link: '',
        fbStatus: []
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
.card {
  padding: 2em;
}
</style>
