<template>
  <v-responsive>
    <Loading v-if="this.userData === null" loadingComponentChoice="Dots" />
    <v-card v-else class="card">
      <div>
        <img
          :src="this.userData.avatar_url"
          :alt="this.userData.name"
          class="avatar"
        />
      </div>
      <div class="user-info">
        <h2>{{ this.userData.name }}</h2>
        <p>{{ this.userData.bio }}</p>
        <ul>
          <li><strong>Followers </strong> : {{ this.userData.followers }}</li>
          <li><strong>Following </strong> : {{ this.userData.following }}</li>
          <li>
            <strong>Repositories </strong> : {{ this.userData.public_repos }}
          </li>
        </ul>
        <ul class="second-desc">
          <li v-if="this.userData.twitter_username">
            <strong>Twitter</strong> : {{ this.userData.twitter_username }}
          </li>
          <li v-if="this.userData.location">
            <strong>Location</strong> : {{ this.userData.location }}
          </li>
        </ul>
        <ul>
          <!-- make date look normal -->
          <li v-if="this.userData.created_at">
            <strong>Created</strong> : {{ this.userData.created_at }}
          </li>
          <v-btn
            class="margin-left"
            v-if="this.userData.blog"
            :href="this.userData.blog"
            >Visit Blog</v-btn
          >
        </ul>
        <Loading v-if="this.userRepos === null" loadingComponentChoice="Dots" />
        <div v-else class="repos">
          <a
            v-for="repo in this.userRepos"
            :key="repo.id"
            :href="repo.html_url"
            target="_blank"
            class="repo"
            >{{ repo.name }}</a
          >
        </div>

        <div id="repos"></div>
      </div>
    </v-card>
  </v-responsive>
</template>

<script>
import Loading from "./Loading.vue";
import moment from "moment";

export default {
  name: "user-component",
  components: {
    Loading,
  },
  props: {
    username: {
      type: String,
      required: true,
    },
    reloadWatcher: {
      type: Number,
      required: true,
    },
  },
  data: function () {
    return { userData: null, userRepos: null };
  },
  mounted() {
    console.log("mounted");
    console.log(this.username);
    console.log(this.userData);
    this.load();
  },
  methods: {
    load() {
      this.userData = null;
      this.fetchUserData(this.username)
        .then((response) => response.json())
        .then((data) => {
          this.userData = data;
          console.log(this.userData);
          moment.defaultFormat = "DD.MM.YYYY, HH:mm";

          this.userData.created_at = moment(this.userData.created_at).format(
            "llll"
          );
          console.log(this.userData.created_at);
        })
        .catch((error) => {
          console.error("Error:", error);
        });
      this.fetchReposData(this.username)
        .then((response) => response.json())
        .then((data) => {
          this.userRepos = data;
          console.log(this.userRepos);
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    },
    async fetchUserData(username) {
      try {
        return await fetch(
          process.env.VUE_APP_BACKEND_ROOT_ENDPOINT + `${username}`
        );
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    },
    async fetchReposData(username) {
      try {
        return await fetch(
          process.env.VUE_APP_BACKEND_ROOT_ENDPOINT + `${username}/repos/10`
        );
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    },
  },
  watch: {
    reloadWatcher() {
      this.load();
    },
  },
};
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Poppins:wght@200;400&display=swap");

* {
  box-sizing: border-box;
}
.card {
  max-width: 800px;
  background-color: gainsboro;
  color: #000;
  border-radius: 20px;
  box-shadow: 0 5px 10px rgba(154, 160, 185, 0.05),
    0 15px 40px rgba(0, 0, 0, 0.1);
  display: flex;
  padding: 3rem;
  font-size: 16px;
  margin: auto;
  margin-top: 20px;
}

.avatar {
  border-radius: 10%;
  border: 10px solid #2a2a72;
  height: 150px;
  width: 150px;
}

.user-info {
  color: #000;
  margin-left: 2rem;
}

.user-info h2 {
  margin-top: 0;
}

.user-info ul {
  list-style-type: none;
  display: flex;
  justify-content: space-between;
  padding: 0;
  max-width: 500px;
}

.user-info ul li {
  display: flex;
  align-items: center;
}

.user-info ul li strong {
  font-size: 0.9rem;
  margin-left: 0.5rem;
}

.repo {
  text-decoration: none;
  color: #fff;
  background-color: #212a72;
  font-size: 0.7rem;
  padding: 0.25rem 0.5rem;
  margin-right: 0.5rem;
  margin-bottom: 0.5rem;
  display: inline-block;
}

.blog-button {
  padding: 5px 10px;
  text-decoration: none;
  color: #000;
  text-align: center;
  border: 1px solid #000;
  background-color: #ddd;
}

.margin-left {
  margin-left: 1rem;
}

@media (max-width: 768px) {
  .card {
    flex-direction: column;
    align-items: center;
    padding: 1rem;
  }

  ul.second-desc {
    display: none;
  }

  .user-form {
    max-width: 400px;
  }
}

@media (max-width: 450px) {
  .user-info ul {
    display: none;
  }
}
</style>
