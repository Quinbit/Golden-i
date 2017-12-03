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
                    <select class="form-control border-input">
                      <option v-for="s in startups">{{ s }}</option>
                    </select>
                  </div>
                </div>

              </div>

              <div>
                <button type="submit" class="btn btn-warning btn-fill btn-wd" @click.prevent="updateProfile">
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
        startups: [
          'http://hackthenorth.com',
          'http://youtube.com',
          'http://github.com'
        ]
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
