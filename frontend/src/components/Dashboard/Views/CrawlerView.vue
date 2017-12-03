<template>
    <div class="row">
      <div class="col-lg-4 col-md-5">
        <div class="card">
          <div class="header">
            <h4 class="title">Current Activity</h4>
          </div>

          <div class="content text-center text-warning" v-if="isIdle">
            <h5>Crawler is idle</h5>
          </div>

          <div class="content text-center text-warning" v-else>
            <h5>Crawler is searching for keywords:<br><code>{{ keywords }}</code></h5>
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

                <div class="col-md-5">
                  <fg-input type="text"
                            label="Keywords"
                            placeholder="Enter keywords to search here"
                            v-model="newActivity.keywords">
                  </fg-input>
                </div>

                <div class="col-md-2 text-center text-muted or">
                  OR
                </div>

                <div class="col-md-5">
                  <fg-input type="text"
                            label="URL"
                            placeholder="Enter a Facebook URL to search"
                            v-model="newActivity.url">
                  </fg-input>
                </div>

              </div>

              <p class="text-danger text-center" v-if="!isIdle">Please wait for the crawler to become idle before starting a new activity.</p>

              <div class="text-center">
                <button type="submit" class="btn btn-warning btn-fill btn-wd" @click.prevent="updateProfile" :disabled="!isIdle">
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
  export default {
    components: {
      EditProfileForm,
      UserCard,
      MembersCard
    },
    data () {
      return {
        isIdle: false,
        keywords: 'trump',
        newActivity: {
          keywords: '',
          url: ''
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
