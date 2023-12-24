<template>
  <v-responsive>
    <Loading v-if="this.userData === null" loadingComponentChoice="Dots" />
    <div v-else-if="this.userData.notFound === true" class="flex-row">
      <div class="card padding-3">
        <h2>404: User Not Found</h2>
      </div>
    </div>
    <div v-else class="flex-row">
      <div class="card">
        <div class="flex-column no-wrap">
          <img
            :src="this.userData.avatar_url"
            :alt="this.userData.name"
            class="avatar"
          />
          <v-btn
            variant="plain"
            v-if="this.userData.blog"
            :href="this.userData.blog"
            target="_blank"
            >Visit Blog</v-btn
          >
        </div>
        <div class="user-info">
          <h2>{{ this.userData.name }}</h2>
          <p class="margin-bottom">{{ this.userData.bio }}</p>
          <ul class="margin-bottom">
            <li>
              <strong>Followers:&nbsp;</strong> {{ this.userData.followers }}
            </li>
            <li>
              <strong>Following:&nbsp;</strong> {{ this.userData.following }}
            </li>
            <li>
              <strong>Repositories:&nbsp;</strong>
              {{ this.userData.public_repos }}
            </li>
          </ul>
          <ul class="second-desc margin-bottom">
            <li v-if="this.userData.location">
              <strong>Location:&nbsp;</strong> {{ this.userData.location }}
            </li>
          </ul>
          <ul class="margin-bottom">
            <li v-if="this.userData.created_at">
              <strong>Created:&nbsp;</strong> {{ this.userData.created_at }}
            </li>
          </ul>
          <Loading
            v-if="this.userRepos === null"
            loadingComponentChoice="Dots"
          />
          <v-chip-group v-else class="flex-row">
            <v-chip
              v-for="repo in this.userRepos"
              :key="repo.id"
              :href="repo.html_url"
              target="_blank"
              >{{ repo.name }}</v-chip
            >
          </v-chip-group>
        </div>
        <div class="external-buttons-column">
          <v-btn
            variant="plain"
            icon="mdi-github"
            class="card-external-buttons"
            v-if="this.userData.html_url"
            :href="this.userData.html_url"
            target="_blank"
          ></v-btn>
          <v-btn
            variant="plain"
            icon="mdi-chart-donut"
            class="card-external-buttons"
            target="_blank"
            @click="openPieChartModal"
          ></v-btn>
          <v-btn
            variant="plain"
            icon="mdi-chart-bar"
            class="card-external-buttons"
            target="_blank"
          ></v-btn>
          <v-btn
            variant="plain"
            icon="mdi-twitter"
            class="card-external-buttons"
            v-if="this.userData.twitter_username"
            :href="'https://twitter.com/' + this.userData.twitter_username"
            target="_blank"
          ></v-btn>
        </div>
      </div>
    </div>
  </v-responsive>
  <PieChartModal
    v-if="this.pieChartModalOpen"
    :username="this.username"
    :reload-watcher="this.reloadWatcher"
    ref="pieChartModal"
  />
</template>

<script>
import PieChartModal from "../modals/PieChartModal.vue";
import Loading from "./Loading.vue";
import moment from "moment";

export default {
  name: "user-component",
  components: {
    Loading,
    PieChartModal,
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
    exampleUsernames: {
      type: Set,
      required: true,
    },
  },
  data: function () {
    return { userData: null, userRepos: null, pieChartModalOpen: false };
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

          if (
            this.userData.message === "Not Found" ||
            this.username === "" ||
            this.username === null
          ) {
            this.userData = {
              notFound: true,
            };
            return;
          }

          this.exampleUsernames.add(this.username.toLowerCase());
          if (this.exampleUsernames.size > 20) {
            this.exampleUsernames.delete(
              this.exampleUsernames.values().next().value
            );
          }
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
          process.env.VUE_APP_BACKEND_ROOT_ENDPOINT + `users/${username}`
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
    scrollToPieChartModal() {
      this.$refs.pieChartModal.$el.scrollIntoView({ behavior: "smooth" });
    },
    openPieChartModal() {
      this.pieChartModalOpen = !this.pieChartModalOpen;

      // Scroll to PieChartModal when opening
      if (this.pieChartModalOpen) {
        this.$nextTick(() => {
          this.scrollToPieChartModal();
        });
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
  max-width: min(85vw, 800px);
  background-color: gainsboro;
  color: black;
  border-radius: 30px;
  box-shadow: 0 5px 10px rgba(154, 160, 185, 0.05),
    0 15px 40px rgba(0, 0, 0, 0.1);
  display: flex;
  padding: 3rem;
  padding-right: 0;
  font-size: 16px;
  margin: 20px auto;
}

.padding-3 {
  padding: 3rem;
}

.avatar {
  border-radius: 30%;
  border: 6px solid gray;
  height: 150px;
  width: 150px;
  margin-bottom: 5px;
}

.user-info {
  /* color: #000; */
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

.margin-bottom {
  margin-bottom: 0.3rem;
}

.margin-right-auto {
  margin-right: auto;
}

.external-buttons-column {
  position: relative;
  top: -40px;
  right: -50px;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  /* padding: 0px 15px; */
  color: white;
  margin: 0;
}
.card-external-buttons {
  margin: 0;
  margin-bottom: 10px;
}

.flex-row {
  display: flex;
  flex-direction: row;
  justify-content: center;
}

.flex-column {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.no-wrap {
  flex-wrap: nowrap;
}

@media (max-width: 768px) {
  .card {
    flex-direction: column;
    align-items: center;
    padding: 1rem;
    max-width: 90vw;
  }

  ul.second-desc {
    display: none;
  }

  .user-form {
    max-width: 400px;
  }
  .external-buttons-column {
    flex-direction: row;
    color: black;
    margin-right: auto;
    display: inline-block;
    top: 0;
    right: 0;
  }
  .user-info {
    /* color: #000; */
    margin: auto;
  }
}

@media (max-width: 450px) {
  .user-info ul {
    /* display: none; */
    flex-wrap: wrap;
  }
}
</style>
